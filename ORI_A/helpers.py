from time import strptime

def integer_to_timestamp(secs: int) -> str:
    """Convert `secs` to a hh:mm:ss timestamp"""
    if not isinstance(secs, int):
        raise TypeError(f"expected int, got {type(secs).__name__}")
    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def timestamp_to_integer(timestamp: str) -> int:
    """Convert a timestamp (hh:mm:ss) to an amount of seconds"""
    time = strptime(timestamp, "%H:%M:%S")
    return time.tm_hour * 3600 + time.tm_min * 60 + time.tm_sec
