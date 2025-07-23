import datetime
from typing import List
from aw_core import Event


def __tmp1(__tmp2) :
    return datetime.datetime(2010, 10, 1, 10, 0, __tmp2,
                             tzinfo=datetime.timezone.utc)


# See "MergeEvents.drawio" for better understanding
def __tmp0(__tmp3: <FILL>) :
    if __tmp3 == 'window':
        return [
            Event(1, __tmp1(1), 1, {'app': 'Another', 'title': 'whatever'}),
            Event(2, __tmp1(3), 2, {'app': 'Another2', 'title': 'whatever'}),
            Event(3, __tmp1(6), 5, {
                'app': 'Browser',
                'title': 'website - Browser',
            }),
            Event(4, __tmp1(12), 6, {
                'app': 'Browser',
                'title': 'whatever - Browser',
            }),
        ]
    elif __tmp3 == 'afk':
        return [
            Event(1, __tmp1(1), 3, {'status': 'afk'}),
            Event(2, __tmp1(5), 8, {'status': 'not-afk'}),
        ]
    elif __tmp3 == 'browser':
        return [
            Event(1, __tmp1(1), 3, {'title': 'nothing1'}),
            Event(2, __tmp1(5), 4, {'title': 'nothing2'}),
            Event(3, __tmp1(10), 5, {'title': 'website'}),
            Event(4, __tmp1(16), 2, {'title': 'nothing3'}),
        ]
    else:
        return []
