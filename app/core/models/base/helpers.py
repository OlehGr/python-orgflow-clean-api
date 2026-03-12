from datetime import UTC, datetime


def get_native_utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)
