from persimmon.view import blocks
from persimmon.view.pins import Pin, InputPin, OutputPin
from kivy.uix.bubble import Bubble
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, ListProperty
import inspect
import logging
from functools import reduce
from fuzzywuzzy import process
from typing import List, Optional
from kivy.input import MotionEvent
from kivy.uix.recycleview import RecycleView


Builder.load_file('persimmon/view/blocks/smart_bubble.kv')
logger = logging.getLogger(__name__)

class __typ0(RecycleView):
    """ Because pyinstaller bug. """
    def __init__(__tmp0, **kwargs):
        super().__init__(**kwargs)

class __typ1(Bubble):
    rv = ObjectProperty()
    ti = ObjectProperty()

    # TODO: cache instancing
    def __init__(__tmp0, backdrop, pin: Optional[Pin] = None, **kwargs) :
        super().__init__(**kwargs)
        __tmp0.y -= __tmp0.width  # type: ignore
        __tmp0.pin = pin
        __tmp0.backdrop = backdrop
        # Let's do some introspection, removing strings we do not care about
        block_members = map(lambda m: m[1], inspect.getmembers(blocks))
        block_cls = filter(lambda m: inspect.isclass(m) and
                           issubclass(m, blocks.Block) and
                           m != blocks.Block, block_members)
        # Kivy properties are not really static, so we need to instance blocks
        instances = (block() for block in block_cls)
        if pin:  # Context sensitive if we are connecting
            if issubclass(pin.__class__, InputPin):
                conn = pin.origin
            elif issubclass(pin.__class__, OutputPin):
                conn = pin.destinations[-1]
            else:
                raise AttributeError('Pin class where InPin or OutPin goes')
            conn.remove_info()
            instances = filter(__tmp0._is_suitable, instances)

        # This is how we pass information to each shown row
        __tmp0.rv.data = [{'cls_name': block.title, 'cls_': block.__class__,
                         'bub': __tmp0, 'backdrop': backdrop, 'pin': __tmp0.pin,
                         'block_pos': __tmp0.pos} for block in instances]
        __tmp0.cache = {data['cls_']: data['cls_name'] for data in __tmp0.rv.data}
        Clock.schedule_once(__tmp0.refocus, 0.3)

    def refocus(__tmp0, _):
        __tmp0.ti.focus = True

    def on_touch_down(__tmp0, touch: MotionEvent) -> bool:
        if not __tmp0.collide_point(*touch.pos):
            if __tmp0.pin:  # If there is a connection going on
                if issubclass(__tmp0.pin.__class__, InputPin):
                    if __tmp0.pin.origin:
                        __tmp0.pin.origin.delete_connection()
                elif __tmp0.pin.destinations:
                    __tmp0.pin.destinations[-1].delete_connection()
            if touch.button == 'left':
                __tmp0.dismiss()
                return True
            elif touch.button == 'right':
                __tmp0.x = touch.x
                __tmp0.y = touch.y - __tmp0.height
                return True
        return super().on_touch_down(touch)

    def dismiss(__tmp0):
        __tmp0.parent.remove_widget(__tmp0)

    def __tmp1(__tmp0, string: <FILL>):
        if string:
            results = process.extract(string, __tmp0.cache,
                                      limit=len(__tmp0.cache))
            __tmp0.rv.data = [{'cls_name': block[0], 'cls_': block[2],
                             'bub': __tmp0, 'backdrop': __tmp0.backdrop,
                             'pin': __tmp0.pin, 'block_pos': __tmp0.pos}
                            for block in results if block[1] > 50]
        else:
            __tmp0.rv.data = [{'cls_name': name, 'cls_': class_, 'bub': __tmp0,
                             'backdrop': __tmp0.backdrop, 'pin': __tmp0.pin,
                             'block_pos': __tmp0.pos}
                            for class_, name in __tmp0.cache.items()]

    def _is_suitable(__tmp0, block: blocks.Block) -> bool:
        return any(filter(lambda p: p.typesafe(__tmp0.pin),
                          block.output_pins + block.input_pins))

class Row(BoxLayout):
    cls_name = StringProperty()
    cls_ = ObjectProperty()
    bub = ObjectProperty()
    backdrop = ObjectProperty()
    block_pos = ListProperty()
    pin = ObjectProperty(allownone=True)

    def __tmp2(__tmp0):
        block = __tmp0.cls_(pos=__tmp0.block_pos)
        __tmp0.backdrop.block_div.add_widget(block)
        if __tmp0.pin:
            if issubclass(__tmp0.pin.__class__, InputPin):
                other_pin = __tmp0._suitable_pin(block.output_pins)
                conn = __tmp0.pin.origin
            else:
                other_pin = __tmp0._suitable_pin(block.input_pins)
                conn = __tmp0.pin.destinations[-1]
            logger.debug('Spawning block {} from bubble'.format(block))
            other_pin.connect_pin(conn)
        __tmp0.bub.dismiss()

    def _suitable_pin(__tmp0, pins: List[Pin]) -> Pin:
        return reduce(lambda p1, p2: p1 if p1.type_ == __tmp0.pin.type_ else p2,
                      pins)
