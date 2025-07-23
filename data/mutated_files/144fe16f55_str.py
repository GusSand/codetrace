from typing import TypeAlias
__typ7 : TypeAlias = "Iterator"
__typ5 : TypeAlias = "Any"
__typ1 : TypeAlias = "SQLiteDialect_pysqlite"
__typ3 : TypeAlias = "Column"
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


def create_session(__tmp0: str, drop_tables: bool = False) :
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
            db_engine = create_engine(__tmp0, convert_unicode=True)
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

    def __init__(__tmp1, cls_, name, value, description) :
        """Initialize EnumSymbol with class, name, value and description."""
        __tmp1.cls_ = cls_
        __tmp1.name = name
        __tmp1.value = value
        __tmp1.description = description

    def __reduce__(__tmp1) :
        """
        Allow unpickling to return the symbol linked to the DeclEnum class.

        :return: method and object reference to unpickle with
        :rtype: method, (class, attribute)
        """
        return getattr, (__tmp1.cls_, __tmp1.name)

    def __iter__(__tmp1) :
        """
        Provide iterator for the class.

        :return: iterator
        :rtype: iter
        """
        return iter([__tmp1.value, __tmp1.description])

    def __repr__(__tmp1) :
        """
        Define object representation when used with display method such as print.

        :return: object representation
        :rtype: str
        """
        return f"<{__tmp1.name}>"


class __typ4(type):
    """Generate new DeclEnum classes."""

    def __init__(__tmp1, classname, bases: Union[Tuple[Type[__typ8]], Tuple[Type[object]]],
                 dict_) :
        """Initialize EnumMeta with class, name, value and description."""
        __tmp1._reg: Dict
        __tmp1._reg = reg = __tmp1._reg.copy()
        for k, v in dict_.items():
            if isinstance(v, tuple):
                sym = reg[v[0]] = __typ9(__tmp1, k, *v)
                setattr(__tmp1, k, sym)
        return type.__init__(__tmp1, classname, bases, dict_)

    def __iter__(__tmp1) :
        """
        Provide iterator for the class.

        :return: iterator
        :rtype: iter
        """
        return iter(__tmp1._reg.values())


class __typ8(object, metaclass=__typ4):
    """Declarative enumeration."""

    _reg: Dict = {}

    @classmethod
    def from_string(cls, value: <FILL>) :
        """
        Get value from _reg dict of the class.

        :param value: dict key
        :type value: string
        :raises ValueError: if value is not a valid key
        :return: dict element for key value
        :rtype: dynamic
        """
        try:
            return cls._reg[value]
        except KeyError:
            print(f"Invalid value for {cls.__name__}: {value}")
            raise EnumParsingException

    @classmethod
    def values(cls):
        """
        Get list of keys for the _reg dict of the class.

        :return: list of dictionary keys
        :rtype: set
        """
        return cls._reg.keys()

    @classmethod
    def db_type(cls) :
        """Get type of database."""
        return __typ6(cls)


class __typ6(SchemaType, TypeDecorator):
    """Declarative enumeration type."""

    def __init__(__tmp1, enum) -> None:
        __tmp1.enum = enum
        __tmp1.impl = Enum(
            *enum.values(),
            name="ck{0}".format(re.sub('([A-Z])', lambda m: "_" + m.group(1).lower(), enum.__name__))
        )

    def _set_table(__tmp1, table, column: Table) :
        __tmp1.impl._set_table(table, column)

    def copy(__tmp1) :
        """Get enumeration type of self."""
        return __typ6(__tmp1.enum)

    def process_bind_param(__tmp1, value, dialect) -> str:
        """Get process bind parameter."""
        if value is None:
            return None
        return value.value

    def process_result_value(__tmp1, value, dialect: __typ1) -> __typ9:
        """Get process result value."""
        if value is None:
            return None
        return __tmp1.enum.from_string(value.strip())
