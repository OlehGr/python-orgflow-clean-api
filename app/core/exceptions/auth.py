from .base import BasicMessageError


class UnauthorizedError(BasicMessageError):
    def __init__(self, message: str = "Не авторизован") -> None:
        super().__init__(message, 401)
