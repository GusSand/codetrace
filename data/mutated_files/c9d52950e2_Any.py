from typing import TypeAlias
__typ1 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
from typing import Any, Callable, Dict

'''
This module helps you set up a bunch
of sequences, similar to how database
sequences work.

You need to be a bit careful here, since
you're dealing with a big singleton, but
for data imports that's usually easy to
manage.  See hipchat.py for example usage.
'''

def _seq() -> Callable[[], __typ0]:
    i = 0

    def __tmp0() -> __typ0:
        nonlocal i
        i += 1
        return i

    return __tmp0

def sequencer() :
    '''
        Use like this:

        NEXT_ID = sequencer()
        message_id = NEXT_ID('message')
    '''
    seq_dict = dict()  # type: Dict[str, Callable[[], int]]

    def __tmp0(__tmp5: str) -> __typ0:
        if __tmp5 not in seq_dict:
            seq_dict[__tmp5] = _seq()
        seq = seq_dict[__tmp5]
        return seq()

    return __tmp0

'''
NEXT_ID is a singleton used by an entire process, which is
almost always reasonable.  If you want to have two parallel
sequences, just use different `name` values.

This object gets created once and only once during the first
import of the file.
'''

NEXT_ID = sequencer()

def __tmp3(__tmp2: <FILL>) -> __typ1:
    try:
        n = __typ0(__tmp2)
    except ValueError:
        return False

    return n <= 999999999

class IdMapper:
    def __init__(__tmp1) -> None:
        __tmp1.map = dict()  # type: Dict[Any, int]
        __tmp1.cnt = 0

    def has(__tmp1, __tmp4: Any) -> __typ1:
        return __tmp4 in __tmp1.map

    def get(__tmp1, __tmp4: Any) -> __typ0:
        if __tmp4 in __tmp1.map:
            return __tmp1.map[__tmp4]

        if __tmp3(__tmp4):
            our_id = __typ0(__tmp4)
            if __tmp1.cnt > 0:
                raise Exception('mixed key styles')
        else:
            __tmp1.cnt += 1
            our_id = __tmp1.cnt

        __tmp1.map[__tmp4] = our_id
        return our_id
