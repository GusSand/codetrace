from typing import TypeAlias
__typ1 : TypeAlias = "set"
__typ0 : TypeAlias = "int"
from threading import Thread
from pymitter import EventEmitter
from typing import List, Dict, Any, Tuple, NamedTuple, Callable, TYPE_CHECKING
from persimmon.view.pins import Pin  # For typing only
import logging


logger = logging.getLogger(__name__)

# backend types
InputEntry = NamedTuple('InputEntry', [('origin', __typ0),
                                       ('pin', 'Pin'),
                                       ('block', __typ0)])
BlockEntry = NamedTuple('BlockEntry', [('inputs', List[__typ0]),
                                       ('function', Callable[..., None]),
                                       ('outputs', List[__typ0])])
OutputEntry = NamedTuple('OutputEntry', [('destinations', List[__typ0]),
                                         ('pin', 'Pin'),
                                         ('block', __typ0)])
IR = NamedTuple('IR', [('blocks', Dict[__typ0, BlockEntry]),
                       ('inputs', Dict[__typ0, InputEntry]),
                       ('outputs', Dict[__typ0, OutputEntry])])

class Backend(EventEmitter):
    def __tmp3(__tmp1, ir: <FILL>):
        __tmp1.ir = ir
        Thread(target=__tmp1._exec_graph_parallel).start()

    def _exec_graph_parallel(__tmp1):
        """ Execution algorithm, introduces all blocks on a set, when a block
        is executed it is taken out of the set until the set is empty. """
        unseen = __typ1(__tmp1.ir.blocks.keys())  # All blocks are unseen at start
        # All output pins along their respectives values
        __tmp2 = {}  # type: Dict[int, Any]
        while unseen:
            unseen, __tmp2 = __tmp1._exec_block(unseen.pop(), unseen, __tmp2)
        logger.info('Execution done')
        __tmp1.emit('graph_executed')

    def _exec_block(__tmp1, __tmp0, unseen,
                    __tmp2) -> Tuple[__typ1, Dict[__typ0, Any]]:
        """ Execute a block, if any dependency is not yet executed we
        recurse into it first. """
        logger.debug('Executing block {}'.format(__tmp0))
        current_block = __tmp1.ir.blocks[__tmp0]
        for in_pin in map(lambda x: __tmp1.ir.inputs[x], current_block.inputs):
            origin = in_pin.origin
            if origin not in __tmp2:
                dependency = __tmp1.ir.outputs[origin].block
                unseen.remove(dependency)
                unseen, __tmp2 = __tmp1._exec_block(dependency, unseen, __tmp2)
            in_pin.pin.val = __tmp2[origin]

        current_block.function()
        __tmp1.emit('block_executed', __tmp0)
        logger.debug('Block {} executed'.format(__tmp0))

        for out_id in current_block.outputs:
            __tmp2[out_id] = __tmp1.ir.outputs[out_id].pin.val
        return unseen, __tmp2

