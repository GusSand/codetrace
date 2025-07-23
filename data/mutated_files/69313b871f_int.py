from typing import TypeAlias
__typ1 : TypeAlias = "set"
from threading import Thread
from pymitter import EventEmitter
from typing import List, Dict, Any, Tuple, NamedTuple, Callable, TYPE_CHECKING
from persimmon.view.pins import Pin  # For typing only
import logging


logger = logging.getLogger(__name__)

# backend types
InputEntry = NamedTuple('InputEntry', [('origin', int),
                                       ('pin', 'Pin'),
                                       ('block', int)])
BlockEntry = NamedTuple('BlockEntry', [('inputs', List[int]),
                                       ('function', Callable[..., None]),
                                       ('outputs', List[int])])
OutputEntry = NamedTuple('OutputEntry', [('destinations', List[int]),
                                         ('pin', 'Pin'),
                                         ('block', int)])
__typ0 = NamedTuple('IR', [('blocks', Dict[int, BlockEntry]),
                       ('inputs', Dict[int, InputEntry]),
                       ('outputs', Dict[int, OutputEntry])])

class __typ2(EventEmitter):
    def __tmp4(__tmp0, ir):
        __tmp0.ir = ir
        Thread(target=__tmp0._exec_graph_parallel).start()

    def _exec_graph_parallel(__tmp0):
        """ Execution algorithm, introduces all blocks on a set, when a block
        is executed it is taken out of the set until the set is empty. """
        __tmp1 = __typ1(__tmp0.ir.blocks.keys())  # All blocks are unseen at start
        # All output pins along their respectives values
        __tmp3 = {}  # type: Dict[int, Any]
        while __tmp1:
            __tmp1, __tmp3 = __tmp0._exec_block(__tmp1.pop(), __tmp1, __tmp3)
        logger.info('Execution done')
        __tmp0.emit('graph_executed')

    def _exec_block(__tmp0, __tmp2: <FILL>, __tmp1,
                    __tmp3) :
        """ Execute a block, if any dependency is not yet executed we
        recurse into it first. """
        logger.debug('Executing block {}'.format(__tmp2))
        current_block = __tmp0.ir.blocks[__tmp2]
        for in_pin in map(lambda x: __tmp0.ir.inputs[x], current_block.inputs):
            origin = in_pin.origin
            if origin not in __tmp3:
                dependency = __tmp0.ir.outputs[origin].block
                __tmp1.remove(dependency)
                __tmp1, __tmp3 = __tmp0._exec_block(dependency, __tmp1, __tmp3)
            in_pin.pin.val = __tmp3[origin]

        current_block.function()
        __tmp0.emit('block_executed', __tmp2)
        logger.debug('Block {} executed'.format(__tmp2))

        for out_id in current_block.outputs:
            __tmp3[out_id] = __tmp0.ir.outputs[out_id].pin.val
        return __tmp1, __tmp3

