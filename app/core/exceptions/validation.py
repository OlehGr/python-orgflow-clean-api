from app.core.exceptions.base import BasicMessageError


class ConflictError(BasicMessageError):
    def __init__(self, message: str, code: int = 409) -> None:
        super().__init__(message, code)
