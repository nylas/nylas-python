from __future__ import division
from datetime import datetime


def timestamp_from_dt(dt, epoch=datetime(1970, 1, 1)):
    """
    Convert a datetime to a timestamp.
    https://stackoverflow.com/a/8778548/141395
    """
    delta = dt - epoch
    # return delta.total_seconds()
    return delta.seconds + delta.days * 86400


def convert_datetimes_to_timestamps(data, datetime_attrs):
    """
    Given a dictionary of data, and a dictionary of datetime attributes,
    return a new dictionary that converts any datetime attributes that may
    be present to their timestamped equivalent.
    """
    if not data:
        return data

    new_data = {}
    for key, value in data.items():
        if key in datetime_attrs and isinstance(value, datetime):
            new_key = datetime_attrs[key]
            new_data[new_key] = timestamp_from_dt(value)
        else:
            new_data[key] = value

    return new_data
