from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
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

def __tmp3() :
    i = 0

    def __tmp2() :
        nonlocal i
        i += 1
        return i

    return __tmp2

def __tmp7() :
    '''
        Use like this:

        NEXT_ID = sequencer()
        message_id = NEXT_ID('message')
    '''
    seq_dict = dict()  # type: Dict[str, Callable[[], int]]

    def __tmp2(__tmp10) :
        if __tmp10 not in seq_dict:
            seq_dict[__tmp10] = __tmp3()
        seq = seq_dict[__tmp10]
        return seq()

    return __tmp2

'''
NEXT_ID is a singleton used by an entire process, which is
almost always reasonable.  If you want to have two parallel
sequences, just use different `name` values.

This object gets created once and only once during the first
import of the file.
'''

NEXT_ID = __tmp7()

def __tmp8(__tmp6) :
    try:
        n = __typ1(__tmp6)
    except ValueError:
        return False

    return n <= 999999999

class __typ2:
    def __tmp4(__tmp1) :
        __tmp1.map = dict()  # type: Dict[Any, int]
        __tmp1.cnt = 0

    def __tmp5(__tmp1, __tmp9: <FILL>) :
        return __tmp9 in __tmp1.map

    def __tmp0(__tmp1, __tmp9) :
        if __tmp9 in __tmp1.map:
            return __tmp1.map[__tmp9]

        if __tmp8(__tmp9):
            our_id = __typ1(__tmp9)
            if __tmp1.cnt > 0:
                raise Exception('mixed key styles')
        else:
            __tmp1.cnt += 1
            our_id = __tmp1.cnt

        __tmp1.map[__tmp9] = our_id
        return our_id
