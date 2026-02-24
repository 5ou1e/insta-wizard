from __future__ import annotations


class TransportError(Exception):
    """Base Transport Error."""


class TransportTimeoutError(TransportError):
    pass


class TransportNetworkError(TransportError):
    pass
