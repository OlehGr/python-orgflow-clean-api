from app.core.exceptions.base import BasicMessageError


class PermissionDeniedError(BasicMessageError):
    def __init__(self, message: str, code: int = 403) -> None:
        super().__init__(message, code)
