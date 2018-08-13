import datetime


def generate_proper_date_from_date(dt_object, date_format):
    """Generate consistent results from a date object."""
    return datetime.datetime.strptime(dt_object.strftime(date_format), date_format)


def generate_proper_date_from_string(str_object, date_format):
    """Generate consistent results from a string object."""
    return datetime.datetime.strptime(str_object, date_format)


def handle_date(target_date, date_format):
    """Globally used to handle dates in forms that they come in."""
    if isinstance(target_date, str):
        if target_date.lower() == 'now':
            return generate_proper_date_from_date(datetime.datetime.now(), date_format)
        else:
            return generate_proper_date_from_string(target_date, date_format)
    else:
        return generate_proper_date_from_date(target_date, date_format)
