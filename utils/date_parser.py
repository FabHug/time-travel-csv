from datetime import datetime

# List of possible datetime formats to support
datetime_formats = [
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%Y/%m/%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y.%m.%d",
    "%d.%m.%Y",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%Y/%m/%d %H:%M",
    "%d/%m/%Y %H:%M",
    "%m/%d/%Y %H:%M",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
    "%Y.%m.%d %H:%M",
    "%d.%m.%Y %H:%M",
    "%Y.%m.%d %H:%M:%S",
    "%d.%m.%Y %H:%M:%S",
]

def try_parse_date(date_str):
    """Try to parse a date string using multiple formats."""
    if not date_str or not date_str.strip():
        return None
    
    for fmt in datetime_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None

def format_date_for_output(date_obj):
    """Format a datetime object to the standard output format."""
    return date_obj.strftime("%d-%m-%Y %H:%M") 