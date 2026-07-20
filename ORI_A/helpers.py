def integer_to_timestamp(secs: int) -> str:
    """Convert `secs` to a hh:mm:ss timestamp"""
    hours, remainder = divmod(secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"
