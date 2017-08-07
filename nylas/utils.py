from __future__ import division
from datetime import datetime, timedelta


def timestamp_from_dt(dt, epoch=datetime(1970,1,1)):
    """
    Convert a datetime to a timestamp.
    https://stackoverflow.com/a/8778548/141395
    """
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6
