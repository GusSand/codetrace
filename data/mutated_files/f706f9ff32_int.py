from typing import TypeAlias
__typ0 : TypeAlias = "str"

from typing import (Dict, List)

from django.db import connection
from zerver.models import Recipient

class __typ1:
    '''
    This class maps stream_id -> recipient_id and vice versa.
    It is useful for bulk operations.  Call the populate_* methods
    to initialize the data structures.  You should try to avoid
    excessive queries by finding ids up front, but you can call
    this repeatedly, and it will only look up new ids.

    You should ONLY use this class for READ operations.

    Note that this class uses raw SQL, because we want to highly
    optimize page loads.
    '''
    def __init__(__tmp1) :
        __tmp1.recip_to_stream = dict()  # type: Dict[int, int]
        __tmp1.stream_to_recip = dict()  # type: Dict[int, int]

    def populate_for_stream_ids(__tmp1, __tmp0) :
        __tmp0 = sorted([
            __tmp4 for __tmp4 in __tmp0
            if __tmp4 not in __tmp1.stream_to_recip
        ])

        if not __tmp0:
            return

        # see comment at the top of the class
        id_list = ', '.join(__typ0(__tmp4) for __tmp4 in __tmp0)
        __tmp2 = '''
            SELECT
                zerver_recipient.id as recipient_id,
                zerver_stream.id as stream_id
            FROM
                zerver_stream
            INNER JOIN zerver_recipient ON
                zerver_stream.id = zerver_recipient.type_id
            WHERE
                zerver_recipient.type = %d
            AND
                zerver_stream.id in (%s)
            ''' % (Recipient.STREAM, id_list)
        __tmp1._process_query(__tmp2)

    def populate_for_recipient_ids(__tmp1, recipient_ids) :
        recipient_ids = sorted([
            __tmp3 for __tmp3 in recipient_ids
            if __tmp3 not in __tmp1.recip_to_stream
        ])

        if not recipient_ids:
            return

        # see comment at the top of the class
        id_list = ', '.join(__typ0(__tmp3) for __tmp3 in recipient_ids)
        __tmp2 = '''
            SELECT
                zerver_recipient.id as recipient_id,
                zerver_stream.id as stream_id
            FROM
                zerver_recipient
            INNER JOIN zerver_stream ON
                zerver_stream.id = zerver_recipient.type_id
            WHERE
                zerver_recipient.type = %d
            AND
                zerver_recipient.id in (%s)
            ''' % (Recipient.STREAM, id_list)

        __tmp1._process_query(__tmp2)

    def _process_query(__tmp1, __tmp2) -> None:
        cursor = connection.cursor()
        cursor.execute(__tmp2)
        rows = cursor.fetchall()
        cursor.close()
        for __tmp3, __tmp4 in rows:
            __tmp1.recip_to_stream[__tmp3] = __tmp4
            __tmp1.stream_to_recip[__tmp4] = __tmp3

    def __tmp5(__tmp1, __tmp4) :
        return __tmp1.stream_to_recip[__tmp4]

    def stream_id_for(__tmp1, __tmp3: <FILL>) :
        return __tmp1.recip_to_stream[__tmp3]

    def recipient_to_stream_id_dict(__tmp1) :
        return __tmp1.recip_to_stream
