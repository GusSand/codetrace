from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
__typ1 : TypeAlias = "str"
from datetime import datetime
import logging
import json
from time import sleep

import requests


def __tmp2():
    """Load and return the config from file."""
    with open('config.json') as f:
        return json.load(f)


def create_http_session(session_token: __typ1 = None) :
    """Create a new requests session with the session token as a cookie."""
    __tmp1 = requests.Session()
    if session_token:
        __tmp1.cookies.set('session', session_token)
    return __tmp1


def __tmp3(__tmp0: <FILL>) -> None:
    """Sleep for the duration."""
    logging.debug(f'Waiting for {__tmp0} seconds')
    sleep(__tmp0)


def __tmp4(timestamp: __typ1) -> __typ0:
    """Converts a Tildes timestamp to a datetime object."""
    return __typ0.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')


def get_url(__tmp1: requests.Session, url: __typ1) -> requests.Response:
    """Get a url and wait if blocked."""
    attempts = 0
    while True:
        try:
            resp = __tmp1.get(url)
            if resp.status_code == 200:
                return resp
        except Exception as e:
            logging.debug(f'Exception hitting {url}: {__typ1(e)}')
        attempts += 1
        if attempts == 5:
            logging.error(f'Could not get {url}, continuous failures')
        logging.debug('Received non-200 response, waiting 2 seconds')
        __tmp3(2)
