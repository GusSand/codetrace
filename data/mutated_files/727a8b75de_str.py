""" download_image module

Defines download_image function

"""
import requests
from requests import Response


def __tmp0(__tmp2, __tmp1: <FILL>) -> None:
    """
    :param loc: location (directory) to save the file
    :param url: location (HTTP address) of the image
    :return: None
    """
    res: Response = requests.get(__tmp1)
    res.raise_for_status()
    with open(__tmp2, 'w+b') as image_file:
        for chunk in res.iter_content(100000):
            image_file.write(chunk)
