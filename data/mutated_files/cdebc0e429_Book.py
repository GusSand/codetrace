from typing import TypeAlias
__typ0 : TypeAlias = "Session"
__typ1 : TypeAlias = "bool"
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

    def __tmp6(__tmp0):
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


def __tmp1(func: Callable):
    """Load new session and add session as the first argument of `func`.

    :param func: Target function.
    :type func: function.
    """
    @functools.wraps(func)
    def __tmp3(*args, **kw):
        """See `load_session`
        """
        with args[0].sql_manager.create_session() as __tmp4:
            return func(__tmp4, *args[1:], **kw)
    return __tmp3


class SQLHandler(object):
    """Handler for SQL requests.
    """

    def __tmp6(__tmp0, sql_manager=None):
        __tmp0.sql_manager = sql_manager

    @__tmp1
    def get_chats(__tmp4: __typ0) -> List[Chat]:
        return __tmp4.query(Chat).options(joinedload('books')).all()

    @__tmp1
    def __tmp7(__tmp4: __typ0, __tmp8: <FILL>):
        """
        Decrease `notice_counter` by 1 and
        delete reocrd if `notice_counter` is 0."""
        online_book = __tmp4.query(Book).filter(Book.id == __tmp8.id).filter(
            Book.location == __tmp8.location).filter(Book.chat_id == __tmp8.chat_id).one()
        online_book.notice_counter -= 1
        if online_book.notice_counter == 0:
            logging.warning(f"LibraryMonitor: Delete book `{__tmp8}`")
            __tmp4.delete(online_book)
        __tmp4.commit()

    @__tmp1
    def __tmp9(__tmp4: __typ0, __tmp8: Book):
        """
        Reset `notice_counter` to `NOTICE_COUNTER`."""
        online_book = __tmp4.query(Book).filter(Book.id == __tmp8.id).filter(
            Book.location == __tmp8.location).filter(Book.chat_id == __tmp8.chat_id).one()
        online_book.notice_counter = NOTICE_COUNTER
        __tmp4.commit()

    @__tmp1
    def add_book(__tmp4: __typ0, __tmp5: str, __tmp2: str, chat_id, location) -> __typ1:
        if __tmp4.query(exists().where(Chat.id == chat_id)).scalar() is not None and \
                __tmp4.query(exists().where(Location.name == location)).scalar() is not None and \
                __tmp4.query(Book).filter(Book.id == __tmp5).filter(
                        Book.location == location).filter(Book.chat_id == chat_id).scalar() is None:
            # such chat exists
            new_book = Book(name=__tmp2, id=__tmp5,
                            location=location, chat_id=chat_id)
            __tmp4.add(new_book)
            __tmp4.commit()
            return True
        else:
            return False
