import re

from asyncpg import ForeignKeyViolationError, UniqueViolationError
from litestar import Request, Response
from litestar.status_codes import HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.exc import IntegrityError

from app.core.exceptions.base import BasicMessageError


def message_error_handler(request: Request, exception: Exception) -> Response:
    if not isinstance(exception, BasicMessageError):
        return _create_internal_error_response(request, exception)

    exception_str = str(exception)

    return Response(
        content={"message": exception_str},
        status_code=exception.code,
    )


def integrity_error_handler(request: Request, exception: Exception) -> Response:
    if not isinstance(exception, IntegrityError):
        return _create_internal_error_response(request, exception)

    error_message = str(exception.orig)

    for violation in [ForeignKeyViolationError, UniqueViolationError]:
        error_message = re.sub(f"{violation}:", "", error_message)

    error_message = re.sub(r'"', "'", error_message)
    error_message = re.sub(r"\n", " ", error_message)
    error_message = re.sub(r"\s+", " ", error_message).strip()

    return Response(
        content={"message": error_message},
        status_code=HTTP_409_CONFLICT,
    )


def internal_error_handler(request: Request, exception: Exception) -> Response:
    return _create_internal_error_response(request, exception)


def _create_internal_error_response(request: Request, exception: Exception) -> Response:
    exception_str = str(exception)
    request.logger.error(exception_str)
    return Response(
        content={"message": f"Приходите завтра... {exception_str}"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
