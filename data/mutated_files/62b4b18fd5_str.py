""" get_confirmation_cookie module

Defines functions used to fetch
age-gated cookie

"""

from http.cookiejar import CookieJar
from typing import Tuple

import requests
from requests import Response
from bs4 import BeautifulSoup

URL = "https://garfield.com"


def __tmp0() -> Tuple[str, CookieJar]:
    """
    Returns security token used to verify age as well
    as list of cookies returned by server
    :return: Tuple[str, CookieJar]
    """
    session = requests.Session()
    res: Response = session.get(URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    token = soup.select('input[name="_token"]')
    return token[0].attrs['value'], session.cookies


def get_age_gated(token: <FILL>, cookies: CookieJar) :
    """
    Returns age-gated cookie used by server to verify age
    :param token: str
    :param cookies: CookieJar
    :return: str
    """
    data = {
        '_token': token,
        'role': 'adult'
    }
    session = requests.Session()
    session.post(URL + "/agegate", data=data, cookies=cookies)
    return session.cookies.get_dict().get('age-gated')
