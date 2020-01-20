from __future__ import division
from datetime import datetime

try:
    from dateutil.rrule import rrulebase, rruleset
except ImportError:
    rrulebase = rruleset = None


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


if rrulebase:

    def convert_rrules_to_strings(data, rrule_attrs):
        """
        Given a dictionary of data, and a dict of rrule attributes,
        return a new dictionary that converts any rrule attributes that may
        be present to their string equivalent.
        """
        if not data:
            return data

        new_data = {}
        for key, value in data.items():
            if key in rrule_attrs and isinstance(value, rrulebase):
                new_key = rrule_attrs[key]
                if isinstance(value, rruleset):
                    new_data[new_key] = [str(rrule) for rrule in value]
                else:
                    new_data[new_key] = [str(value)]
            else:
                new_data[key] = value

        return new_data


else:
    # can't import dateutil, so this is a no-op
    def convert_rrules_to_strings(data, rrule_attrs):
        return data


def convert_data(data, cls):
    datetime_attrs = getattr(cls, "datetime_attrs", [])
    rrule_attrs = getattr(cls, "rrule_attrs", [])

    d1 = convert_datetimes_to_timestamps(data, datetime_attrs)
    d2 = convert_rrules_to_strings(d1, rrule_attrs)
    return d2
