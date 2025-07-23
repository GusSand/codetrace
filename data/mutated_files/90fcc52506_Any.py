from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
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

def __tmp2() :
    i = 0

    def __tmp0() -> __typ0:
        nonlocal i
        i += 1
        return i

    return __tmp0

def sequencer() -> Callable[[__typ1], __typ0]:
    '''
        Use like this:

        NEXT_ID = sequencer()
        message_id = NEXT_ID('message')
    '''
    seq_dict = dict()  # type: Dict[str, Callable[[], int]]

    def __tmp0(name) :
        if name not in seq_dict:
            seq_dict[name] = __tmp2()
        seq = seq_dict[name]
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

def is_int(key) :
    try:
        n = __typ0(key)
    except ValueError:
        return False

    return n <= 999999999

class IdMapper:
    def __tmp1(self) -> None:
        self.map = dict()  # type: Dict[Any, int]
        self.cnt = 0

    def has(self, their_id: Any) :
        return their_id in self.map

    def get(self, their_id: <FILL>) :
        if their_id in self.map:
            return self.map[their_id]

        if is_int(their_id):
            our_id = __typ0(their_id)
            if self.cnt > 0:
                raise Exception('mixed key styles')
        else:
            self.cnt += 1
            our_id = self.cnt

        self.map[their_id] = our_id
        return our_id
