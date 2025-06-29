import datetime

def serialize_datetime(value):
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    raise TypeError("Type not serializable")