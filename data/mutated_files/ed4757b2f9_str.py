from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "SQLiteDialect_pysqlite"
__typ4 : TypeAlias = "Iterator"
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


class __typ1(DeclarativeMeta, ABCMeta):
    """Empty class to create a mixin between DeclarativeMeta and ABCMeta."""

    pass


Base = declarative_base(metaclass=DeclarativeMeta)
Base.query = None
db_engine = None


def create_session(__tmp2: str, drop_tables: bool = False) :
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
            db_engine = create_engine(__tmp2, convert_unicode=True)
        db_session = scoped_session(sessionmaker(bind=db_engine))
        Base.query = db_session.query_property()

        if drop_tables:
            Base.metadata.drop_all(bind=db_engine)

        Base.metadata.create_all(bind=db_engine)

        return db_session
    except SQLAlchemyError:
        traceback.print_exc()
        raise FailedToSpawnDBSession()


class __typ5(object):
    """Define a fixed symbol tied to a parent class."""

    def __init__(__tmp0, cls_, name: str, value: <FILL>, description) -> None:
        """Initialize EnumSymbol with class, name, value and description."""
        __tmp0.cls_ = cls_
        __tmp0.name = name
        __tmp0.value = value
        __tmp0.description = description

    def __reduce__(__tmp0) -> Tuple[__typ2, Tuple[__typ2, str]]:
        """
        Allow unpickling to return the symbol linked to the DeclEnum class.

        :return: method and object reference to unpickle with
        :rtype: method, (class, attribute)
        """
        return getattr, (__tmp0.cls_, __tmp0.name)

    def __tmp3(__tmp0) -> __typ4:
        """
        Provide iterator for the class.

        :return: iterator
        :rtype: iter
        """
        return iter([__tmp0.value, __tmp0.description])

    def __tmp4(__tmp0) -> str:
        """
        Define object representation when used with display method such as print.

        :return: object representation
        :rtype: str
        """
        return f"<{__tmp0.name}>"


class EnumMeta(type):
    """Generate new DeclEnum classes."""

    def __init__(__tmp0, classname: str, bases: Union[Tuple[Type[DeclEnum]], Tuple[Type[object]]],
                 __tmp6) :
        """Initialize EnumMeta with class, name, value and description."""
        __tmp0._reg: Dict
        __tmp0._reg = reg = __tmp0._reg.copy()
        for k, v in __tmp6.items():
            if isinstance(v, tuple):
                sym = reg[v[0]] = __typ5(__tmp0, k, *v)
                setattr(__tmp0, k, sym)
        return type.__init__(__tmp0, classname, bases, __tmp6)

    def __tmp3(__tmp0) -> __typ4:
        """
        Provide iterator for the class.

        :return: iterator
        :rtype: iter
        """
        return iter(__tmp0._reg.values())


class DeclEnum(object, metaclass=EnumMeta):
    """Declarative enumeration."""

    _reg: Dict = {}

    @classmethod
    def from_string(__tmp1, value: str) :
        """
        Get value from _reg dict of the class.

        :param value: dict key
        :type value: string
        :raises ValueError: if value is not a valid key
        :return: dict element for key value
        :rtype: dynamic
        """
        try:
            return __tmp1._reg[value]
        except KeyError:
            print(f"Invalid value for {__tmp1.__name__}: {value}")
            raise EnumParsingException

    @classmethod
    def values(__tmp1):
        """
        Get list of keys for the _reg dict of the class.

        :return: list of dictionary keys
        :rtype: set
        """
        return __tmp1._reg.keys()

    @classmethod
    def db_type(__tmp1) -> __typ3:
        """Get type of database."""
        return __typ3(__tmp1)


class __typ3(SchemaType, TypeDecorator):
    """Declarative enumeration type."""

    def __init__(__tmp0, enum: __typ2) -> None:
        __tmp0.enum = enum
        __tmp0.impl = Enum(
            *enum.values(),
            name="ck{0}".format(re.sub('([A-Z])', lambda m: "_" + m.group(1).lower(), enum.__name__))
        )

    def _set_table(__tmp0, table: Column, __tmp5: Table) -> None:
        __tmp0.impl._set_table(table, __tmp5)

    def copy(__tmp0) :
        """Get enumeration type of self."""
        return __typ3(__tmp0.enum)

    def process_bind_param(__tmp0, value, dialect) :
        """Get process bind parameter."""
        if value is None:
            return None
        return value.value

    def process_result_value(__tmp0, value: str, dialect: __typ0) -> __typ5:
        """Get process result value."""
        if value is None:
            return None
        return __tmp0.enum.from_string(value.strip())
