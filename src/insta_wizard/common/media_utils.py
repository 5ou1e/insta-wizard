"""Shared utilities for image and video processing before upload."""

import os
import re
import subprocess
import tempfile
from typing import Literal


def get_image_size(image_bytes: bytes) -> tuple[int, int]:
    """Parse width and height from JPEG or PNG bytes without external dependencies."""
    if image_bytes[:2] == b"\xff\xd8":
        # JPEG: scan for SOF marker (C0, C1, C2)
        i = 2
        while i < len(image_bytes) - 9:
            if image_bytes[i] != 0xFF:
                break
            marker = image_bytes[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                height = int.from_bytes(image_bytes[i + 5 : i + 7], "big")
                width = int.from_bytes(image_bytes[i + 7 : i + 9], "big")
                return width, height
            segment_length = int.from_bytes(image_bytes[i + 2 : i + 4], "big")
            i += 2 + segment_length
    elif image_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        # PNG: width at offset 16, height at offset 20
        width = int.from_bytes(image_bytes[16:20], "big")
        height = int.from_bytes(image_bytes[20:24], "big")
        return width, height
    raise ValueError(
        "Cannot determine image dimensions: unsupported format (expected JPEG or PNG)."
    )


def get_video_metadata(video_bytes: bytes) -> tuple[int, int, int]:
    """Parse width, height, duration_ms from MP4/MOV bytes without external dependencies."""

    def find_box(data: bytes, box_type: bytes, pos: int = 0) -> tuple[int, int] | None:
        end = len(data)
        while pos <= end - 8:
            size = int.from_bytes(data[pos : pos + 4], "big")
            btype = data[pos + 4 : pos + 8]
            if size == 1:
                if pos + 16 > end:
                    break
                size = int.from_bytes(data[pos + 8 : pos + 16], "big")
                header = 16
            elif size == 0:
                header = 8
                size = end - pos
            else:
                if size < 8:
                    break
                header = 8
            data_start = pos + header
            data_len = size - header
            if btype == box_type:
                return data_start, data_len
            pos = data_start + data_len
        return None

    moov_r = find_box(video_bytes, b"moov")
    if not moov_r:
        raise ValueError("Cannot parse video: moov box not found")
    moov_start, moov_len = moov_r
    moov = video_bytes[moov_start : moov_start + moov_len]

    # duration from mvhd
    mvhd_r = find_box(moov, b"mvhd")
    if not mvhd_r:
        raise ValueError("Cannot parse video: mvhd box not found")
    d, _ = mvhd_r
    version = moov[d]
    if version == 0:
        timescale = int.from_bytes(moov[d + 12 : d + 16], "big")
        duration = int.from_bytes(moov[d + 16 : d + 20], "big")
    else:
        timescale = int.from_bytes(moov[d + 20 : d + 24], "big")
        duration = int.from_bytes(moov[d + 24 : d + 32], "big")
    duration_ms = int(duration * 1000 / timescale) if timescale else 0

    # width/height from the first video trak (non-zero dimensions)
    width = height = 0
    pos = 0
    while pos <= len(moov) - 8:
        size = int.from_bytes(moov[pos : pos + 4], "big")
        if size < 8:
            break
        if moov[pos + 4 : pos + 8] == b"trak":
            trak = moov[pos + 8 : pos + size]
            tkhd_r = find_box(trak, b"tkhd")
            if tkhd_r:
                t, _ = tkhd_r
                v = trak[t]
                if v == 0:
                    w = int.from_bytes(trak[t + 76 : t + 80], "big") >> 16
                    h = int.from_bytes(trak[t + 80 : t + 84], "big") >> 16
                else:
                    w = int.from_bytes(trak[t + 88 : t + 92], "big") >> 16
                    h = int.from_bytes(trak[t + 92 : t + 96], "big") >> 16
                if w > 0 and h > 0:
                    width, height = w, h
                    break
        pos += size

    if not width or not height or not duration_ms:
        raise ValueError(
            "Cannot determine video dimensions/duration: unsupported format (expected MP4)."
        )
    return width, height, duration_ms


def _probe_video(tmp_in: str, ffmpeg_exe: str) -> tuple[bool, bool, int, int]:
    """Return (needs_codec_fix, needs_ar_fix, width, height) by probing with ffmpeg."""
    result = subprocess.run(
        [ffmpeg_exe, "-i", tmp_in],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    for line in result.stderr.splitlines():
        if "Video:" not in line:
            continue
        needs_codec_fix = "h264" not in line or "yuv420p" not in line
        m = re.search(r",\s*(\d{2,5})x(\d{2,5})", line)
        if not m:
            return needs_codec_fix, False, 0, 0
        w, h = int(m.group(1)), int(m.group(2))
        ratio = w / h
        # Instagram limits: portrait max 9:16 (0.5625), landscape max 1.91:1
        needs_ar_fix = ratio < (9 / 16 - 0.005) or ratio > 1.915
        return needs_codec_fix, needs_ar_fix, w, h
    return True, False, 0, 0


def transcode_video_for_instagram(
    video_bytes: bytes,
    fit_mode: Literal["pad", "crop"] = "pad",
) -> bytes:
    """Re-encode to H.264 yuv420p using bundled ffmpeg. Skipped if already compatible.

    fit_mode controls what happens when aspect ratio is outside Instagram limits:
      "pad"  — add black bars (default)
      "crop" — crop to fit
    """
    try:
        import imageio_ffmpeg
    except ImportError as e:
        raise ImportError("moviepy is required for transcode video: pip install moviepy") from e

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    tmp_in = tmp_out = None
    try:
        f_in = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp_in = f_in.name
        f_in.write(video_bytes)
        f_in.flush()
        f_in.close()

        needs_codec_fix, needs_ar_fix, w, h = _probe_video(tmp_in, ffmpeg_exe)
        if not needs_codec_fix and not needs_ar_fix:
            return video_bytes

        vf_parts = []
        if needs_ar_fix and w and h:
            ratio = w / h
            if ratio < 9 / 16:  # too narrow / tall → fix width
                if fit_mode == "pad":
                    new_w = (round(h * 9 / 16) // 2) * 2
                    vf_parts.append(f"pad={new_w}:{h}:(ow-iw)/2:0:black")
                else:
                    new_h = (round(w * 16 / 9) // 2) * 2
                    vf_parts.append(f"crop={w}:{new_h}:0:(ih-oh)/2")
            else:  # too wide → fix height
                if fit_mode == "pad":
                    new_h = (round(w / 1.91) // 2) * 2
                    vf_parts.append(f"pad={w}:{new_h}:0:(oh-ih)/2:black")
                else:
                    new_w = (round(h * 1.91) // 2) * 2
                    vf_parts.append(f"crop={new_w}:{h}:(iw-ow)/2:0")
        # always enforce even dimensions (H.264 requirement)
        vf_parts.append("scale=trunc(iw/2)*2:trunc(ih/2)*2")

        f_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp_out = f_out.name
        f_out.close()

        subprocess.run(
            [
                ffmpeg_exe,
                "-y",
                "-i",
                tmp_in,
                "-vf",
                ",".join(vf_parts),
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "23",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-movflags",
                "+faststart",
                tmp_out,
            ],
            capture_output=True,
            check=True,
        )

        with open(tmp_out, "rb") as f:
            return f.read()
    finally:
        for path in (tmp_in, tmp_out):
            if path:
                try:
                    os.remove(path)
                except Exception:
                    pass


def extract_video_thumbnail(video_bytes: bytes) -> bytes:
    """Extract a JPEG thumbnail from the mid-frame of a video."""
    try:
        import imageio.v3 as iio
        import moviepy as mp
    except ImportError as e:
        raise ImportError(
            "moviepy is required for extract_video_thumbnail: pip install moviepy"
        ) from e

    tmp_path = None
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    try:
        tmp_path = f.name
        f.write(video_bytes)
        f.flush()
        f.close()

        with mp.VideoFileClip(tmp_path) as video:
            frame = video.get_frame(float(video.duration) / 2.0)
            return iio.imwrite("<bytes>", frame, extension=".jpg", quality=85)

    finally:
        try:
            f.close()
        except Exception:
            pass
        if tmp_path:
            try:
                os.remove(tmp_path)
            except Exception:
                pass
