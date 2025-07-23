from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError
from LMNFlask import app
from typing import Union
# from utils.database.schema import schema
schema = ["SELECT * FROM lmn_note"]

DB_URL = app.config["DB_CONN"]
engine = create_engine(DB_URL, echo=True)


def __tmp0(__tmp3, params: Union[list, tuple]=None) :
    """ executes a single command with no return value """
    with engine.connect() as conn:
        if params is not None:
            try:
                conn.execute(__tmp3, params)
            except SQLAlchemyError as e:
                print(e)
        else:
            try:
                conn.execute(__tmp3)
            except SQLAlchemyError as e:
                print(e)


def __tmp1(__tmp3: <FILL>, params: Union[list, tuple]=None) -> Union[tuple, None]:
    """ executes a single command and returns a data set """
    with engine.connect() as conn:
        if params is not None:
            try:
                rs = conn.execute(__tmp3).fetchall()
                print(rs)
                if len(rs) > 0:
                    return rs
                else:
                    return None
            except SQLAlchemyError as e:
                print(e)
        else:
            try:
                rs = conn.execute(__tmp3).fetchall()
                print(rs)
                if len(rs) > 0:
                    return rs
                else:
                    return None
            except SQLAlchemyError as e:
                print(e)


def __tmp2():
    for __tmp3 in schema:
        print(__tmp0(__tmp3))


if __name__ == '__main__':
    __tmp2()

