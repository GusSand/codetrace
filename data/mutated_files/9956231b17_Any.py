from typing import TypeAlias
__typ2 : TypeAlias = "Column"
__typ0 : TypeAlias = "str"
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


class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):
    """Empty class to create a mixin between DeclarativeMeta and ABCMeta."""

    pass


Base = declarative_base(metaclass=DeclarativeMeta)
Base.query = None
db_engine = None


def __tmp1(__tmp7: __typ0, drop_tables: bool = False) -> scoped_session:
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
            db_engine = create_engine(__tmp7, convert_unicode=True)
        db_session = scoped_session(sessionmaker(bind=db_engine))
        Base.query = db_session.query_property()

        if drop_tables:
            Base.metadata.drop_all(bind=db_engine)

        Base.metadata.create_all(bind=db_engine)

        return db_session
    except SQLAlchemyError:
        traceback.print_exc()
        raise FailedToSpawnDBSession()


class __typ3(object):
    """Define a fixed symbol tied to a parent class."""

    def __init__(__tmp0, cls_: Any, name, value, description) :
        """Initialize EnumSymbol with class, name, value and description."""
        __tmp0.cls_ = cls_
        __tmp0.name = name
        __tmp0.value = value
        __tmp0.description = description

    def __tmp8(__tmp0) :
        """
        Allow unpickling to return the symbol linked to the DeclEnum class.

        :return: method and object reference to unpickle with
        :rtype: method, (class, attribute)
        """
        return getattr, (__tmp0.cls_, __tmp0.name)

    def __tmp9(__tmp0) :
        """
        Provide iterator for the class.

        :return: iterator
        :rtype: iter
        """
        return iter([__tmp0.value, __tmp0.description])

    def __tmp10(__tmp0) :
        """
        Define object representation when used with display method such as print.

        :return: object representation
        :rtype: str
        """
        return f"<{__tmp0.name}>"


class EnumMeta(type):
    """Generate new DeclEnum classes."""

    def __init__(__tmp0, __tmp6, __tmp2,
                 __tmp13) :
        """Initialize EnumMeta with class, name, value and description."""
        __tmp0._reg: Dict
        __tmp0._reg = reg = __tmp0._reg.copy()
        for k, v in __tmp13.items():
            if isinstance(v, tuple):
                sym = reg[v[0]] = __typ3(__tmp0, k, *v)
                setattr(__tmp0, k, sym)
        return type.__init__(__tmp0, __tmp6, __tmp2, __tmp13)

    def __tmp9(__tmp0) -> Iterator:
        """
        Provide iterator for the class.

        :return: iterator
        :rtype: iter
        """
        return iter(__tmp0._reg.values())


class __typ1(object, metaclass=EnumMeta):
    """Declarative enumeration."""

    _reg: Dict = {}

    @classmethod
    def from_string(__tmp5, value: __typ0) :
        """
        Get value from _reg dict of the class.

        :param value: dict key
        :type value: string
        :raises ValueError: if value is not a valid key
        :return: dict element for key value
        :rtype: dynamic
        """
        try:
            return __tmp5._reg[value]
        except KeyError:
            print(f"Invalid value for {__tmp5.__name__}: {value}")
            raise EnumParsingException

    @classmethod
    def values(__tmp5):
        """
        Get list of keys for the _reg dict of the class.

        :return: list of dictionary keys
        :rtype: set
        """
        return __tmp5._reg.keys()

    @classmethod
    def __tmp4(__tmp5) -> DeclEnumType:
        """Get type of database."""
        return DeclEnumType(__tmp5)


class DeclEnumType(SchemaType, TypeDecorator):
    """Declarative enumeration type."""

    def __init__(__tmp0, enum: <FILL>) -> None:
        __tmp0.enum = enum
        __tmp0.impl = Enum(
            *enum.values(),
            name="ck{0}".format(re.sub('([A-Z])', lambda m: "_" + m.group(1).lower(), enum.__name__))
        )

    def _set_table(__tmp0, table, __tmp12: Table) -> None:
        __tmp0.impl._set_table(table, __tmp12)

    def copy(__tmp0) :
        """Get enumeration type of self."""
        return DeclEnumType(__tmp0.enum)

    def __tmp3(__tmp0, value: __typ3, dialect) :
        """Get process bind parameter."""
        if value is None:
            return None
        return value.value

    def __tmp11(__tmp0, value, dialect) -> __typ3:
        """Get process result value."""
        if value is None:
            return None
        return __tmp0.enum.from_string(value.strip())
