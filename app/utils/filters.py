import datetime

def format_date(value, format="%B %d, %Y"):
    """Format a datetime string or object."""
    if isinstance(value, str):
        value = datetime.datetime.fromisoformat(value)
    return value.strftime(format)

def format_date_time(value, format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.fromisoformat(value).strftime(format)
