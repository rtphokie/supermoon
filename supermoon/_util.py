from datetime import UTC, datetime


def as_utc(dt=None):
    """dt as a timezone aware datetime; None means now, naive datetimes are UTC"""
    if dt is None:
        return datetime.now(UTC)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt
