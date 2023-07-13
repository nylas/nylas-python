from typing import get_args


def _get_generic_type(instance, base_class):
    """
    Extracts the generic type associated with a specific base class of an instance.

    Parameters:
    instance (object): The instance of a class.
    base_class (type): The base class to search for in the instance.

    Returns:
    type: The generic type associated with the base_class if found; None otherwise.
    """
    try:
        generic_base = [
            base
            for base in instance.__class__.__orig_bases__
            if base.__origin__ is base_class
        ]
    except AttributeError:
        return None

    if generic_base:
        return get_args(generic_base[0])[0]
    else:
        return None
