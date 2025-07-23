from typing import TypeAlias
__typ2 : TypeAlias = "Callable"
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

    def __init__(self):
        Chat.books = relationship("Book")
        engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        self.session_maker = scoped_session(session_factory)

    @contextmanager
    def create_session(self):
        """Create session to talk to database, rollback and raise error if failed.
        """
        session = self.session_maker
        try:
            yield session
        except Exception as identifier:
            logging.exception(identifier)
            session.rollback()
            raise identifier
        finally:
            session.close()
            self.session_maker.remove()


def load_session(func: __typ2):
    """Load new session and add session as the first argument of `func`.

    :param func: Target function.
    :type func: function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        """See `load_session`
        """
        with args[0].sql_manager.create_session() as __tmp1:
            return func(__tmp1, *args[1:], **kw)
    return wrapper


class __typ0(object):
    """Handler for SQL requests.
    """

    def __init__(self, sql_manager=None):
        self.sql_manager = sql_manager

    @load_session
    def __tmp0(__tmp1) :
        return __tmp1.query(Chat).options(joinedload('books')).all()

    @load_session
    def __tmp2(__tmp1: __typ1, target_book):
        """
        Decrease `notice_counter` by 1 and
        delete reocrd if `notice_counter` is 0."""
        online_book = __tmp1.query(Book).filter(Book.id == target_book.id).filter(
            Book.location == target_book.location).filter(Book.chat_id == target_book.chat_id).one()
        online_book.notice_counter -= 1
        if online_book.notice_counter == 0:
            logging.warning(f"LibraryMonitor: Delete book `{target_book}`")
            __tmp1.delete(online_book)
        __tmp1.commit()

    @load_session
    def reset_notice_counter(__tmp1, target_book):
        """
        Reset `notice_counter` to `NOTICE_COUNTER`."""
        online_book = __tmp1.query(Book).filter(Book.id == target_book.id).filter(
            Book.location == target_book.location).filter(Book.chat_id == target_book.chat_id).one()
        online_book.notice_counter = NOTICE_COUNTER
        __tmp1.commit()

    @load_session
    def add_book(__tmp1, book_id, book_name: <FILL>, chat_id, location) :
        if __tmp1.query(exists().where(Chat.id == chat_id)).scalar() is not None and \
                __tmp1.query(exists().where(Location.name == location)).scalar() is not None and \
                __tmp1.query(Book).filter(Book.id == book_id).filter(
                        Book.location == location).filter(Book.chat_id == chat_id).scalar() is None:
            # such chat exists
            new_book = Book(name=book_name, id=book_id,
                            location=location, chat_id=chat_id)
            __tmp1.add(new_book)
            __tmp1.commit()
            return True
        else:
            return False
