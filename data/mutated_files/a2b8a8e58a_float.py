from typing import TypeAlias
__typ1 : TypeAlias = "int"
import datetime
import calendar
from django.utils.timezone import utc as timezone_utc

class __typ0(Exception):
    pass

def verify_UTC(__tmp2: datetime.datetime) -> None:
    if __tmp2.tzinfo is None or __tmp2.tzinfo.utcoffset(__tmp2) != timezone_utc.utcoffset(__tmp2):
        raise __typ0("Datetime %s does not have a UTC timezone." % (__tmp2,))

def convert_to_UTC(__tmp2) -> datetime.datetime:
    if __tmp2.tzinfo is None:
        return __tmp2.replace(tzinfo=timezone_utc)
    return __tmp2.astimezone(timezone_utc)

def floor_to_hour(__tmp2: datetime.datetime) :
    verify_UTC(__tmp2)
    return datetime.datetime(*__tmp2.timetuple()[:4]) \
                   .replace(tzinfo=timezone_utc)

def floor_to_day(__tmp2: datetime.datetime) :
    verify_UTC(__tmp2)
    return datetime.datetime(*__tmp2.timetuple()[:3]) \
                   .replace(tzinfo=timezone_utc)

def ceiling_to_hour(__tmp2) -> datetime.datetime:
    floor = floor_to_hour(__tmp2)
    if floor == __tmp2:
        return floor
    return floor + datetime.timedelta(hours=1)

def __tmp0(__tmp2: datetime.datetime) :
    floor = floor_to_day(__tmp2)
    if floor == __tmp2:
        return floor
    return floor + datetime.timedelta(days=1)

def __tmp3(__tmp1: <FILL>) :
    return datetime.datetime.fromtimestamp(float(__tmp1), tz=timezone_utc)

def datetime_to_timestamp(__tmp2: datetime.datetime) :
    verify_UTC(__tmp2)
    return calendar.timegm(__tmp2.timetuple())
