
from typing import Any, Dict, Optional

if False:
    from zerver.tornado.event_queue import ClientDescriptor

descriptors_by_handler_id = {}  # type: Dict[int, ClientDescriptor]

def __tmp3(__tmp0) :
    return descriptors_by_handler_id.get(__tmp0)

def __tmp1(__tmp0: int,
                                 __tmp2) :
    descriptors_by_handler_id[__tmp0] = __tmp2

def clear_descriptor_by_handler_id(__tmp0: <FILL>,
                                   __tmp2) :
    del descriptors_by_handler_id[__tmp0]
