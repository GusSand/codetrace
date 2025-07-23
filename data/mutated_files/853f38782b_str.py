""" get_imgs_src module

Defines get_imgs_src function

"""
from typing import List

import requests
from requests import Response

from bs4 import BeautifulSoup


def __tmp0(url: <FILL>, **kwargs) :
    """
    Fetches all src attributes from image elements
    within div with class comic-display
    :param url: str
    :param kwargs: ageGated
    :return: List[str]
    """
    res: Response = requests.get(url, cookies={'age-gated': kwargs.get('age_gated')})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    comic_el = soup.select('div.comic-display img')
    return [img['src'] for img in comic_el]
