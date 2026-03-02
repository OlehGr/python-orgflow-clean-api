from litestar import Request, Response
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.exceptions.base import BasicMessageError


def message_error_handler(request: Request, exception: Exception) -> Response[dict]:
    exception_str = str(exception)

    if isinstance(exception, BasicMessageError):
        return Response(
            content={"message": exception_str},
            status_code=exception.code,
        )

    request.logger.error(exception_str)
    return Response(
        content={"message": f"Приходите завтра... {exception_str}"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


def internal_error_handler(request: Request, exception: Exception) -> Response[dict]:
    exception_str = str(exception)
    request.logger.error(exception_str)
    return Response(
        content={"message": f"Приходите завтра... {exception_str}"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
