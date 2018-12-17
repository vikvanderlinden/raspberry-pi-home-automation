from datetime import datetime, timedelta


def get_time(time=None, delta=0):
    """Returns the current time"""
    if time is None:
        time = datetime.now()
    elif isinstance(time, str):
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    plus_time = time + timedelta(seconds=delta)

    return to_seconds(plus_time)

def to_seconds(time):
    """Converts a given time to seconds"""
    if isinstance(time, int):
        time = datetime.strptime(str(time), "%Y%m%d%H%M%S")

    return int(time.timestamp())
