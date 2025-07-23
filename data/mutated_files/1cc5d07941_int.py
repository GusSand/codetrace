
from typing import Any, Dict, Optional

if False:
    from zerver.tornado.event_queue import ClientDescriptor

descriptors_by_handler_id = {}  # type: Dict[int, ClientDescriptor]

def __tmp0(__tmp2: int) -> Optional['ClientDescriptor']:
    return descriptors_by_handler_id.get(__tmp2)

def __tmp1(__tmp2: <FILL>,
                                 __tmp3: 'ClientDescriptor') -> None:
    descriptors_by_handler_id[__tmp2] = __tmp3

def __tmp4(__tmp2,
                                   __tmp3) -> None:
    del descriptors_by_handler_id[__tmp2]
