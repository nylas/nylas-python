from __future__ import division
from datetime import datetime, timedelta


def timestamp_from_dt(dt, epoch=datetime(1970, 1, 1)):
    """
    Convert a datetime to a timestamp.
    https://stackoverflow.com/a/8778548/141395
    """
    # For offset-aware datetime objects, convert them first before performing delta
    if dt.tzinfo is not None and dt.utcoffset() is not None:
        dt = dt.replace(tzinfo=None) - dt.utcoffset()

    delta = dt - epoch

    return int(delta.total_seconds() / timedelta(seconds=1).total_seconds())


def create_request_body(data, datetime_attrs):
    """
    Given a dictionary of data, and a dictionary of datetime attributes,
    return a new dictionary that is suitable for a request. It converts
    any datetime attributes that may be present to their timestamped
    equivalent, and it filters out any attributes set to "None".
    """
    if not data:
        return data

    new_data = {}
    for key, value in data.items():
        if key in datetime_attrs and isinstance(value, datetime):
            new_key = datetime_attrs[key]
            new_data[new_key] = timestamp_from_dt(value)
        elif value is not None:
            new_data[key] = value

    return new_data


def convert_metadata_pairs_to_array(data):
    """
    Given a dictionary of metadata pairs, convert it to key-value pairs
    in the format the Nylas API expects: "events?metadata_pair=<key>:<value>"
    """
    if not data:
        return data

    metadata_pair = []
    for key, value in data.items():
        metadata_pair.append(key + ":" + value)

    return metadata_pair
