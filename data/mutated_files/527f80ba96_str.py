from typing import TypeAlias
__typ0 : TypeAlias = "float"
import os
import sqlite3

DATABASE = os.path.join(os.path.dirname(__file__), "../db/ia.db3")


def __tmp0(ion: <FILL>) :
    symbols = [symbol for symbol in ion if symbol.isalpha()]
    element = "".join(symbols)
    return element


def __tmp2(__tmp1) -> __typ0:
    """TODO: Docstring for get_value.

    :key: TODO
    :returns: TODO

    """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        request = f"SELECT abundance FROM abundance WHERE species IS '{__tmp1}'"
        cursor.execute(request)
        result = cursor.fetchone()[0]
    return result
