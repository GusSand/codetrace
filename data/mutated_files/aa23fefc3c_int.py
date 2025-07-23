
from typing import Any, Dict, Optional

if False:
    from zerver.tornado.event_queue import ClientDescriptor

descriptors_by_handler_id = {}  # type: Dict[int, ClientDescriptor]

def __tmp3(__tmp0: <FILL>) -> Optional['ClientDescriptor']:
    return descriptors_by_handler_id.get(__tmp0)

def set_descriptor_by_handler_id(__tmp0: int,
                                 __tmp1: 'ClientDescriptor') -> None:
    descriptors_by_handler_id[__tmp0] = __tmp1

def __tmp2(__tmp0,
                                   __tmp1: 'ClientDescriptor') -> None:
    del descriptors_by_handler_id[__tmp0]
