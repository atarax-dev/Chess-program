from datetime import datetime


def convert_datetime_to_str(datetime_object):
    str_object = str(datetime_object)[:10]
    return str_object


def convert_str_to_datetime(str_object):
    y, m, d = str_object.split("-")
    datetime_object = datetime(y, m, d)
    return datetime_object
