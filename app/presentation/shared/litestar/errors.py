from app.core.exceptions.base import BasicMessageError
from litestar import Request, Response
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR


def internal_error_handler(request: Request, exception: Exception) -> Response[dict]:
    if isinstance(exception, BasicMessageError):
        return Response(
            content={"message": str(exception)},
            status_code=exception.code,
        )

    request.logger.error(str(exception))
    return Response(
        content={"message": f"Приходите завтра... {exception!s}"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
