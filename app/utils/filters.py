import datetime

def format_date(value, format="%B %d, %Y"):
    """Format a datetime string or object."""
    if isinstance(value, str):
        value = datetime.datetime.fromisoformat(value)
    return value.strftime(format)

