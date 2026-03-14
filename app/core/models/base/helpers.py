import base64
import os
from datetime import UTC, datetime


def get_native_utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def get_b64encode_token(size: int = 16) -> str:
    return base64.urlsafe_b64encode(os.urandom(size)).rstrip(b"=").decode()
