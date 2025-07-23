from typing import TypeAlias
__typ1 : TypeAlias = "int"
from threading import Thread
from pymitter import EventEmitter
from typing import List, Dict, Any, Tuple, NamedTuple, Callable, TYPE_CHECKING
from persimmon.view.pins import Pin  # For typing only
import logging


logger = logging.getLogger(__name__)

# backend types
InputEntry = NamedTuple('InputEntry', [('origin', __typ1),
                                       ('pin', 'Pin'),
                                       ('block', __typ1)])
BlockEntry = NamedTuple('BlockEntry', [('inputs', List[__typ1]),
                                       ('function', Callable[..., None]),
                                       ('outputs', List[__typ1])])
OutputEntry = NamedTuple('OutputEntry', [('destinations', List[__typ1]),
                                         ('pin', 'Pin'),
                                         ('block', __typ1)])
__typ0 = NamedTuple('IR', [('blocks', Dict[__typ1, BlockEntry]),
                       ('inputs', Dict[__typ1, InputEntry]),
                       ('outputs', Dict[__typ1, OutputEntry])])

class __typ2(EventEmitter):
    def exec_graph(self, ir: __typ0):
        self.ir = ir
        Thread(target=self._exec_graph_parallel).start()

    def _exec_graph_parallel(self):
        """ Execution algorithm, introduces all blocks on a set, when a block
        is executed it is taken out of the set until the set is empty. """
        __tmp0 = set(self.ir.blocks.keys())  # All blocks are unseen at start
        # All output pins along their respectives values
        seen = {}  # type: Dict[int, Any]
        while __tmp0:
            __tmp0, seen = self._exec_block(__tmp0.pop(), __tmp0, seen)
        logger.info('Execution done')
        self.emit('graph_executed')

    def _exec_block(self, current: __typ1, __tmp0: <FILL>,
                    seen) :
        """ Execute a block, if any dependency is not yet executed we
        recurse into it first. """
        logger.debug('Executing block {}'.format(current))
        current_block = self.ir.blocks[current]
        for in_pin in map(lambda x: self.ir.inputs[x], current_block.inputs):
            origin = in_pin.origin
            if origin not in seen:
                dependency = self.ir.outputs[origin].block
                __tmp0.remove(dependency)
                __tmp0, seen = self._exec_block(dependency, __tmp0, seen)
            in_pin.pin.val = seen[origin]

        current_block.function()
        self.emit('block_executed', current)
        logger.debug('Block {} executed'.format(current))

        for out_id in current_block.outputs:
            seen[out_id] = self.ir.outputs[out_id].pin.val
        return __tmp0, seen

