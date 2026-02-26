from app.core.exceptions.base import BasicMessageError


class InvalidCaseError(BasicMessageError):
    def __init__(self, message: str, code: int = 400) -> None:
        super().__init__(message, code)
