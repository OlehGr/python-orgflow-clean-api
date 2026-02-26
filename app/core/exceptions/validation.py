from app.core.exceptions.base import BasicMessageError


class ValidationError(BasicMessageError):
    def __init__(self, message: str, code: int = 401) -> None:
        super().__init__(message, code)
