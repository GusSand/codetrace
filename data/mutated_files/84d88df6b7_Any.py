"""
config unit test
"""
from typing import (
    Any,
    # Dict,
    Iterable,
)

import pytest

from wechaty_puppet import get_logger

# pylint: disable=C0103
log = get_logger('ConfigTest')

# pylint: disable=redefined-outer-name


# https://stackoverflow.com/a/57015304/1123955
@pytest.fixture(name='data', scope='module')
def __tmp1() :
    """ doc """
    yield 'test'


def __tmp0(
        __tmp2: <FILL>,
) -> None:
    """
    Unit Test for config function
    """
    print(__tmp2)

    assert __tmp2 == 'test', 'data should equals test'


def __tmp3() :
    """test"""
    assert get_logger, 'log should exist'
