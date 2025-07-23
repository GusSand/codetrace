from typing import TypeAlias
__typ6 : TypeAlias = "Iterator"
__typ5 : TypeAlias = "Any"
__typ1 : TypeAlias = "str"
__typ4 : TypeAlias = "Table"
__typ0 : TypeAlias = "scoped_session"
"""handles database session and data-type across app."""
from __future__ import annotations

import re
import traceback
from abc import ABCMeta
from typing import Any, Dict, Iterator, Tuple, Type, Union

from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.sql.sqltypes import Enum, SchemaType, TypeDecorator

from exceptions import EnumParsingException, FailedToSpawnDBSession


class __typ2(DeclarativeMeta, ABCMeta):
    """Empty class to create a mixin between DeclarativeMeta and ABCMeta."""

    pass


Base = declarative_base(metaclass=DeclarativeMeta)
Base.query = None
db_engine = None


def create_session(db_string: __typ1, drop_tables: bool = False) -> __typ0:
    """
    Create a new DB session using the scoped_session that SQLAlchemy provides.

    :param db_string: The connection string.
    :type db_string: str
    :param drop_tables: Drop existing tables?
    :type drop_tables: bool
    :return: A SQLAlchemy session object
    :rtype: sqlalchemy.orm.scoped_session
    """
    import os
    global db_engine, Base

    try:
        # In testing, we want to maintain same memory variable
        if db_engine is None or 'TESTING' not in os.environ or os.environ['TESTING'] == 'False':
            db_engine = create_engine(db_string, convert_unicode=True)
        db_session = __typ0(sessionmaker(bind=db_engine))
        Base.query = db_session.query_property()

        if drop_tables:
            Base.metadata.drop_all(bind=db_engine)

        Base.metadata.create_all(bind=db_engine)

        return db_session
    except SQLAlchemyError:
        traceback.print_exc()
        raise FailedToSpawnDBSession()


class __typ9(object):
    """Define a fixed symbol tied to a parent class."""

    def __init__(__tmp0, cls_: __typ5, name, value: __typ1, description: __typ1) -> None:
        """Initialize EnumSymbol with class, name, value and description."""
        __tmp0.cls_ = cls_
        __tmp0.name = name
        __tmp0.value = value
        __tmp0.description = description

    def __tmp5(__tmp0) :
        """
        Allow unpickling to return the symbol linked to the DeclEnum class.

        :return: method and object reference to unpickle with
        :rtype: method, (class, attribute)
        """
        return getattr, (__tmp0.cls_, __tmp0.name)

    def __tmp6(__tmp0) -> __typ6:
        """
        Provide iterator for the class.

        :return: iterator
        :rtype: iter
        """
        return iter([__tmp0.value, __tmp0.description])

    def __tmp7(__tmp0) -> __typ1:
        """
        Define object representation when used with display method such as print.

        :return: object representation
        :rtype: str
        """
        return f"<{__tmp0.name}>"


class __typ3(type):
    """Generate new DeclEnum classes."""

    def __init__(__tmp0, __tmp4: __typ1, bases: Union[Tuple[Type[__typ8]], Tuple[Type[object]]],
                 __tmp9: Dict[__typ1, Union[__typ1, Tuple[__typ1, __typ1], classmethod, staticmethod]]) -> None:
        """Initialize EnumMeta with class, name, value and description."""
        __tmp0._reg: Dict
        __tmp0._reg = reg = __tmp0._reg.copy()
        for k, v in __tmp9.items():
            if isinstance(v, tuple):
                sym = reg[v[0]] = __typ9(__tmp0, k, *v)
                setattr(__tmp0, k, sym)
        return type.__init__(__tmp0, __tmp4, bases, __tmp9)

    def __tmp6(__tmp0) -> __typ6:
        """
        Provide iterator for the class.

        :return: iterator
        :rtype: iter
        """
        return iter(__tmp0._reg.values())


class __typ8(object, metaclass=__typ3):
    """Declarative enumeration."""

    _reg: Dict = {}

    @classmethod
    def from_string(__tmp3, value: __typ1) -> __typ9:
        """
        Get value from _reg dict of the class.

        :param value: dict key
        :type value: string
        :raises ValueError: if value is not a valid key
        :return: dict element for key value
        :rtype: dynamic
        """
        try:
            return __tmp3._reg[value]
        except KeyError:
            print(f"Invalid value for {__tmp3.__name__}: {value}")
            raise EnumParsingException

    @classmethod
    def values(__tmp3):
        """
        Get list of keys for the _reg dict of the class.

        :return: list of dictionary keys
        :rtype: set
        """
        return __tmp3._reg.keys()

    @classmethod
    def db_type(__tmp3) -> __typ7:
        """Get type of database."""
        return __typ7(__tmp3)


class __typ7(SchemaType, TypeDecorator):
    """Declarative enumeration type."""

    def __init__(__tmp0, enum) -> None:
        __tmp0.enum = enum
        __tmp0.impl = Enum(
            *enum.values(),
            name="ck{0}".format(re.sub('([A-Z])', lambda m: "_" + m.group(1).lower(), enum.__name__))
        )

    def _set_table(__tmp0, __tmp2: <FILL>, column: __typ4) -> None:
        __tmp0.impl._set_table(__tmp2, column)

    def copy(__tmp0) -> __typ7:
        """Get enumeration type of self."""
        return __typ7(__tmp0.enum)

    def __tmp1(__tmp0, value: __typ9, dialect: SQLiteDialect_pysqlite) :
        """Get process bind parameter."""
        if value is None:
            return None
        return value.value

    def __tmp8(__tmp0, value: __typ1, dialect: SQLiteDialect_pysqlite) -> __typ9:
        """Get process result value."""
        if value is None:
            return None
        return __tmp0.enum.from_string(value.strip())
