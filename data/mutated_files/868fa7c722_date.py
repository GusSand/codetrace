from typing import TypeAlias
__typ0 : TypeAlias = "str"
""" get_comic_links module

Defines functions used to generate
download links

"""

from datetime import date, timedelta
from typing import Generator

BASE_URL: __typ0 = "https://garfield.com/comic/"


def get_comic_links(start_date, end_date: <FILL>) :
    """
    Returns list of HTTP links leading to Garfield comics
    within given range
    :param start_date: date
    :param end_date: date
    :return: Generator
    """
    for date_counter in range(int((end_date - start_date).days + 1)):
        yield BASE_URL + __tmp0(start_date + timedelta(date_counter))


def __tmp0(__tmp1) :
    """
    Convert date to YYYY/MM/DD in str format
    :param date_val: date
    :return: string
    """
    return __tmp1.strftime('%Y/%m/%d')
