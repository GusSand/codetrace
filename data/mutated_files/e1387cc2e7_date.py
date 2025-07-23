""" get_comic_links module

Defines functions used to generate
download links

"""

from datetime import date, timedelta
from typing import Generator

BASE_URL: str = "https://garfield.com/comic/"


def get_comic_links(__tmp0, __tmp1) :
    """
    Returns list of HTTP links leading to Garfield comics
    within given range
    :param start_date: date
    :param end_date: date
    :return: Generator
    """
    for date_counter in range(int((__tmp1 - __tmp0).days + 1)):
        yield BASE_URL + date_to_url(__tmp0 + timedelta(date_counter))


def date_to_url(date_val: <FILL>) :
    """
    Convert date to YYYY/MM/DD in str format
    :param date_val: date
    :return: string
    """
    return date_val.strftime('%Y/%m/%d')
