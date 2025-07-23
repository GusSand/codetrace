from typing import TypeAlias
__typ0 : TypeAlias = "int"
from datetime import datetime
import logging
import json
from time import sleep

import requests


def load_config():
    """Load and return the config from file."""
    with open('config.json') as f:
        return json.load(f)


def __tmp0(session_token: str = None) -> requests.Session:
    """Create a new requests session with the session token as a cookie."""
    __tmp3 = requests.Session()
    if session_token:
        __tmp3.cookies.set('session', session_token)
    return __tmp3


def __tmp4(__tmp1: __typ0) -> None:
    """Sleep for the duration."""
    logging.debug(f'Waiting for {__tmp1} seconds')
    sleep(__tmp1)


def timestamp_to_datetime(__tmp2: <FILL>) -> datetime:
    """Converts a Tildes timestamp to a datetime object."""
    return datetime.strptime(__tmp2, '%Y-%m-%dT%H:%M:%SZ')


def get_url(__tmp3, url: str) -> requests.Response:
    """Get a url and wait if blocked."""
    attempts = 0
    while True:
        try:
            resp = __tmp3.get(url)
            if resp.status_code == 200:
                return resp
        except Exception as e:
            logging.debug(f'Exception hitting {url}: {str(e)}')
        attempts += 1
        if attempts == 5:
            logging.error(f'Could not get {url}, continuous failures')
        logging.debug('Received non-200 response, waiting 2 seconds')
        __tmp4(2)
