
from typing import (Dict, List)

from django.db import connection
from zerver.models import Recipient

class StreamRecipientMap:
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
    def __tmp10(__tmp1) :
        __tmp1.recip_to_stream = dict()  # type: Dict[int, int]
        __tmp1.stream_to_recip = dict()  # type: Dict[int, int]

    def populate_for_stream_ids(__tmp1, __tmp0) :
        __tmp0 = sorted([
            __tmp7 for __tmp7 in __tmp0
            if __tmp7 not in __tmp1.stream_to_recip
        ])

        if not __tmp0:
            return

        # see comment at the top of the class
        id_list = ', '.join(str(__tmp7) for __tmp7 in __tmp0)
        __tmp5 = '''
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
        __tmp1._process_query(__tmp5)

    def __tmp9(__tmp1, __tmp2) :
        __tmp2 = sorted([
            __tmp6 for __tmp6 in __tmp2
            if __tmp6 not in __tmp1.recip_to_stream
        ])

        if not __tmp2:
            return

        # see comment at the top of the class
        id_list = ', '.join(str(__tmp6) for __tmp6 in __tmp2)
        __tmp5 = '''
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

        __tmp1._process_query(__tmp5)

    def _process_query(__tmp1, __tmp5) :
        cursor = connection.cursor()
        cursor.execute(__tmp5)
        rows = cursor.fetchall()
        cursor.close()
        for __tmp6, __tmp7 in rows:
            __tmp1.recip_to_stream[__tmp6] = __tmp7
            __tmp1.stream_to_recip[__tmp7] = __tmp6

    def __tmp8(__tmp1, __tmp7: <FILL>) :
        return __tmp1.stream_to_recip[__tmp7]

    def __tmp4(__tmp1, __tmp6) :
        return __tmp1.recip_to_stream[__tmp6]

    def __tmp3(__tmp1) :
        return __tmp1.recip_to_stream
