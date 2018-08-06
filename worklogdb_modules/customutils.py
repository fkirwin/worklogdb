import datetime


def generate_proper_date_from_date(dt_object, fmt):
    """Generate consistent results from a date object."""
    return datetime.datetime.strptime(dt_object.strftime(fmt), fmt)


def generate_proper_date_from_string(str_object, fmt):
    """Generate consistent results from a string object."""
    return datetime.datetime.strptime(str_object, fmt)
