from __future__ import annotations


class TransportError(Exception):
    """Базовая ошибка транспорта"""


class TransportTimeoutError(TransportError):
    pass


class TransportNetworkError(TransportError):
    pass
