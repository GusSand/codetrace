"""link helper function for fetching the friendly meta data from url link"""
from __future__ import annotations
from typing import Any, Dict
import requests
from opengraph_py3 import OpenGraph # type: ignore


def __tmp0(__tmp2: <FILL>) :
    """get open graph meta data open open graph protocol

    The Open Graph Protocol: https://ogp.me/

    Args:
        url (str): the url of link

    Returns:
        Dict[str, Any]: the meta data
    """
    return OpenGraph(__tmp2=__tmp2)


def __tmp1(__tmp3) :
    """fetch_github_user_avatar_url

    refer to: https://docs.github.com/en/rest/users/users#get-a-user

    Args:
        name (str): the name of github user

    Returns:
        str: the avatar url of github user
    """
    source_avatar_url = f'https://api.github.com/users/{__tmp3}'

    header = {
        "accept": "application/vnd.github.v3+jso"
    }
    response = requests.get(source_avatar_url, headers=header)
    data = response.json()
    return data.get('avatar_url', None)