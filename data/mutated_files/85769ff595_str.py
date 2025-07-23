from typing import TypeAlias
__typ2 : TypeAlias = "Any"
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

    def __tmp1() :
        nonlocal i
        i += 1
        return i

    return __tmp1

def __tmp5() -> Callable[[str], __typ0]:
    '''
        Use like this:

        NEXT_ID = sequencer()
        message_id = NEXT_ID('message')
    '''
    seq_dict = dict()  # type: Dict[str, Callable[[], int]]

    def __tmp1(__tmp8: <FILL>) -> __typ0:
        if __tmp8 not in seq_dict:
            seq_dict[__tmp8] = _seq()
        seq = seq_dict[__tmp8]
        return seq()

    return __tmp1

'''
NEXT_ID is a singleton used by an entire process, which is
almost always reasonable.  If you want to have two parallel
sequences, just use different `name` values.

This object gets created once and only once during the first
import of the file.
'''

NEXT_ID = __tmp5()

def __tmp6(__tmp4: __typ2) -> __typ1:
    try:
        n = __typ0(__tmp4)
    except ValueError:
        return False

    return n <= 999999999

class __typ3:
    def __tmp3(__tmp2) :
        __tmp2.map = dict()  # type: Dict[Any, int]
        __tmp2.cnt = 0

    def has(__tmp2, __tmp7) -> __typ1:
        return __tmp7 in __tmp2.map

    def __tmp0(__tmp2, __tmp7) -> __typ0:
        if __tmp7 in __tmp2.map:
            return __tmp2.map[__tmp7]

        if __tmp6(__tmp7):
            our_id = __typ0(__tmp7)
            if __tmp2.cnt > 0:
                raise Exception('mixed key styles')
        else:
            __tmp2.cnt += 1
            our_id = __tmp2.cnt

        __tmp2.map[__tmp7] = our_id
        return our_id
