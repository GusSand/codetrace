from typing import TypeAlias
__typ0 : TypeAlias = "Book"
"""Monitor book state in BUPT's library, send notice if available."""

import json
import logging
from typing import List, Dict
import requests
from .config import BOOK_PAGE_REFERER, BOOK_STATE_API, DAILY_REPORT_TEMPLATE, MESSAGE_TEMPLATE, NOTICE_COUNTER, TARGET_STATE
from .models import Book
from .queued_bot import create_queued_bot
from .sql_handler import SQLHandler, SQLManager


class __typ1(object):
    """
    >>> self.target_books[0].keys()
    ['name', 'id', 'location']"""

    def __tmp3(__tmp0, __tmp4: <FILL>):
        __tmp0.bot = create_queued_bot(__tmp4)
        __tmp0.sql_handler = SQLHandler(SQLManager())

    @staticmethod
    def update_book_states(__tmp6) :
        """
        Download and simplify book state dicts from server."""
        headers = {
            'Referer': BOOK_PAGE_REFERER.format(book_id=__tmp6.id)
        }
        params = {
            'rec_ctrl_id': __tmp6.id
        }
        books = []
        try:
            state_response = requests.post(
                BOOK_STATE_API, headers=headers, params=params)
            full_states = json.loads(state_response.text.split('@')[0])[0]['A']
            books = [
                {'state': current_book['circul_status'],
                 'location': current_book['guancang_dept'],
                 'due_date': current_book['due_date']}
                for current_book in full_states
                if __tmp6.location in current_book['guancang_dept']
                and current_book['circul_status'] == TARGET_STATE
            ]
        except Exception as identifier:
            logging.exception(identifier)
            logging.error(
                f'LibraryMonitor: Failed to update book state. (ID: {__tmp6.id})')
        return books

    def send_message(__tmp0, *, __tmp1, text: str):
        """
        Send message to """
        logging.info(f"Send message: `{text}`")
        __tmp0.bot.send_message(__tmp1=__tmp1, text=text)

    def __tmp2(__tmp0):
        """
        Send monitor report to users."""
        for chat in __tmp0.sql_handler.get_chats():
            __tmp0.send_message(
                __tmp1=chat.id,
                text=DAILY_REPORT_TEMPLATE.format(
                    book_counter=len(chat.books),
                    book_names="、".join(
                        [f'《{book.name}》' for book in chat.books])
                ))

    def __tmp5(__tmp0) :
        for chat in __tmp0.sql_handler.get_chats():
            for __tmp6 in chat.books:
                logging.info(
                    f"LibraryMonitor: Updating book state. ({__tmp6})")
                book_states = __tmp0.update_book_states(__tmp6)
                book_counter = len(book_states)
                if book_counter > 0:
                    logging.info(
                        f"LibraryMonitor: Book found. ({__tmp6})")
                    __tmp0.sql_handler.count_notice(__tmp6)
                    __tmp0.send_message(
                        __tmp1=chat.id,
                        text=MESSAGE_TEMPLATE.format(
                            book_location=book_states[0]['location'],
                            book_name=__tmp6.name,
                            book_id=__tmp6.id,
                            book_counter=book_counter,
                            notice_index=NOTICE_COUNTER - __tmp6.notice_counter + 1,
                            max_notice_index=NOTICE_COUNTER))
                else:
                    __tmp0.sql_handler.reset_notice_counter(__tmp6)
                    logging.info(
                        f"LibraryMonitor: Book NOT found. ({__tmp6})")

    def stop(__tmp0):
        """
        Stop bot and return."""
        __tmp0.bot.stop()
