from typing import TypeAlias
__typ0 : TypeAlias = "float"
import os
import sqlite3

DATABASE = os.path.join(os.path.dirname(__file__), "../db/ia.db3")


def _strip_ion(__tmp1: str) -> str:
    symbols = [symbol for symbol in __tmp1 if symbol.isalpha()]
    element = "".join(symbols)
    return element


def __tmp0(key: <FILL>) -> __typ0:
    """TODO: Docstring for get_value.

    :key: TODO
    :returns: TODO

    """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        request = f"SELECT abundance FROM abundance WHERE species IS '{key}'"
        cursor.execute(request)
        result = cursor.fetchone()[0]
    return result
