from datetime import datetime


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    if not dt:
        return ""
    return dt.strftime(fmt)
