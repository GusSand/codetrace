from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "MotionEvent"
__typ0 : TypeAlias = "Connection"
from persimmon.view.pins.pin import Pin  # MYPY HACK
from persimmon.view.util import Connection
from kivy.lang import Builder
from kivy.graphics import Ellipse, Color
from kivy.properties import ObjectProperty
from kivy.input import MotionEvent
import logging


Builder.load_file('persimmon/view/pins/inpin.kv')
logger = logging.getLogger(__name__)

class InputPin(Pin):
    origin = ObjectProperty(allownone=True)

    # Kivy touch methods override
    def __tmp5(__tmp0, __tmp3: __typ1) :
        if (__tmp0.collide_point(*__tmp3.pos) and __tmp3.button == 'left' and
            not __tmp0.origin):
            logger.info('Creating connection')
            __tmp3.ud['cur_line'] = __typ0(start=__tmp0,
                                              color=__tmp0.color)
            __tmp0.origin = __tmp3.ud['cur_line']
            # Add to blackboard
            __tmp0.block.parent.parent.parent.connections.add_widget(__tmp3.ud['cur_line'])
            __tmp0._circle_pin()
            return True
        else:
            return False

    def __tmp8(__tmp0, __tmp3) -> __typ2:
        if ('cur_line' in __tmp3.ud.keys() and __tmp3.button == 'left' and
                __tmp0.collide_point(*__tmp3.pos)):
            if (__tmp3.ud['cur_line'].end and
                __tmp0.typesafe(__tmp3.ud['cur_line'].end)):
                __tmp0.connect_pin(__tmp3.ud['cur_line'])
                #logger.info('Establishing connection')
                #touch.ud['cur_line'].finish_connection(self)
                #self.origin = touch.ud['cur_line']
                #self._circle_pin()
            else:
                logger.info('Deleting connection')
                __tmp3.ud['cur_line'].delete_connection()
            return True
        else:
            return False

    def __tmp4(__tmp0, __tmp6: __typ0):
        if __tmp0.origin:
            __tmp0.origin = None
            # Undo pin circling
            __tmp0.funbind('pos', __tmp0._bind_circle)
            __tmp0.canvas.remove(__tmp0.circle)
            del __tmp0.circle
        else:
            logger.error('Deleting connection not fully formed')

    def connect_pin(__tmp0, __tmp6):
        logger.info('Finish connection')
        __tmp6.finish_connection(__tmp0)
        __tmp0.origin = __tmp6
        __tmp0._circle_pin()

    def typesafe(__tmp0, __tmp7: <FILL>) -> __typ2:
        return super().typesafe(__tmp7) and __tmp0.origin == None

    def _circle_pin(__tmp0):
        if hasattr(__tmp0, 'circle'):
            logger.error('Circling pin twice')
            return
        with __tmp0.canvas:
            Color(*__tmp0.color)
            __tmp0.circle = Ellipse(pos=__tmp0.pos, size=__tmp0.size)
        __tmp0.fbind('pos', __tmp0._bind_circle)

    def _bind_circle(__tmp0, __tmp2, __tmp1):
        __tmp0.circle.pos = __tmp0.pos

