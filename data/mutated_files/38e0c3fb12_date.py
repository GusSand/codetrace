from typing import TypeAlias
__typ0 : TypeAlias = "str"
""" get_comic_links module

Defines functions used to generate
download links

"""

from datetime import date, timedelta
from typing import Generator

BASE_URL: __typ0 = "https://garfield.com/comic/"


def get_comic_links(start_date: <FILL>, __tmp0) -> Generator[__typ0, None, None]:
    """
    Returns list of HTTP links leading to Garfield comics
    within given range
    :param start_date: date
    :param end_date: date
    :return: Generator
    """
    for date_counter in range(int((__tmp0 - start_date).days + 1)):
        yield BASE_URL + date_to_url(start_date + timedelta(date_counter))


def date_to_url(date_val: date) -> __typ0:
    """
    Convert date to YYYY/MM/DD in str format
    :param date_val: date
    :return: string
    """
    return date_val.strftime('%Y/%m/%d')
