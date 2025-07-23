from typing import TypeAlias
__typ0 : TypeAlias = "Callable"
__typ1 : TypeAlias = "Session"
import functools
import logging
from contextlib import contextmanager
from typing import Callable, List
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import joinedload, relationship, scoped_session, sessionmaker
from sqlalchemy.orm.session import Session
from .config import DATABASE_URI, NOTICE_COUNTER
from .models import Base, Book, Chat, Location


class SQLManager(object):
    """Manager sessions.

    :member session_maker: Attached :obj: sessionmaker.
    :type session_maker: :obj:sessionmaker.
    """

    def __init__(__tmp0):
        Chat.books = relationship("Book")
        engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        __tmp0.session_maker = scoped_session(session_factory)

    @contextmanager
    def create_session(__tmp0):
        """Create session to talk to database, rollback and raise error if failed.
        """
        session = __tmp0.session_maker
        try:
            yield session
        except Exception as identifier:
            logging.exception(identifier)
            session.rollback()
            raise identifier
        finally:
            session.close()
            __tmp0.session_maker.remove()


def load_session(func: __typ0):
    """Load new session and add session as the first argument of `func`.

    :param func: Target function.
    :type func: function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        """See `load_session`
        """
        with args[0].sql_manager.create_session() as __tmp2:
            return func(__tmp2, *args[1:], **kw)
    return wrapper


class SQLHandler(object):
    """Handler for SQL requests.
    """

    def __init__(__tmp0, sql_manager=None):
        __tmp0.sql_manager = sql_manager

    @load_session
    def __tmp3(__tmp2) :
        return __tmp2.query(Chat).options(joinedload('books')).all()

    @load_session
    def __tmp5(__tmp2: __typ1, __tmp6: Book):
        """
        Decrease `notice_counter` by 1 and
        delete reocrd if `notice_counter` is 0."""
        online_book = __tmp2.query(Book).filter(Book.id == __tmp6.id).filter(
            Book.location == __tmp6.location).filter(Book.chat_id == __tmp6.chat_id).one()
        online_book.notice_counter -= 1
        if online_book.notice_counter == 0:
            logging.warning(f"LibraryMonitor: Delete book `{__tmp6}`")
            __tmp2.delete(online_book)
        __tmp2.commit()

    @load_session
    def reset_notice_counter(__tmp2, __tmp6: <FILL>):
        """
        Reset `notice_counter` to `NOTICE_COUNTER`."""
        online_book = __tmp2.query(Book).filter(Book.id == __tmp6.id).filter(
            Book.location == __tmp6.location).filter(Book.chat_id == __tmp6.chat_id).one()
        online_book.notice_counter = NOTICE_COUNTER
        __tmp2.commit()

    @load_session
    def add_book(__tmp2: __typ1, __tmp4: str, __tmp1: str, chat_id: int, location) -> bool:
        if __tmp2.query(exists().where(Chat.id == chat_id)).scalar() is not None and \
                __tmp2.query(exists().where(Location.name == location)).scalar() is not None and \
                __tmp2.query(Book).filter(Book.id == __tmp4).filter(
                        Book.location == location).filter(Book.chat_id == chat_id).scalar() is None:
            # such chat exists
            new_book = Book(name=__tmp1, id=__tmp4,
                            location=location, chat_id=chat_id)
            __tmp2.add(new_book)
            __tmp2.commit()
            return True
        else:
            return False
