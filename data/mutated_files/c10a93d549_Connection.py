from persimmon.view.pins.pin import Pin  # MYPY HACK
from persimmon.view.util import Connection
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.graphics import Ellipse, Color

from kivy.input import MotionEvent

import logging


Builder.load_file('persimmon/view/pins/outpin.kv')
logger = logging.getLogger(__name__)

class OutputPin(Pin):
    destinations = ListProperty()

    def __init__(__tmp0, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(__tmp0, __tmp3) :
        if (__tmp0.collide_point(*__tmp3.pos) and __tmp3.button == 'left' and
                not __tmp0.destinations):
            logger.info('Creating connection')
            __tmp3.ud['cur_line'] = Connection(end=__tmp0,
                                              color=__tmp0.color)
            __tmp0.destinations.append(__tmp3.ud['cur_line'])
            # Add to blackboard
            __tmp0.block.parent.parent.parent.connections.add_widget(__tmp3.ud['cur_line'])
            __tmp0._circle_pin()
            return True
        else:
            return False

    def on_touch_up(__tmp0, __tmp3) -> bool:
        if ('cur_line' in __tmp3.ud.keys() and __tmp3.button == 'left' and
                __tmp0.collide_point(*__tmp3.pos)):
            if (__tmp3.ud['cur_line'].start and
                __tmp0.typesafe(__tmp3.ud['cur_line'].start)):
                __tmp0.connect_pin(__tmp3.ud['cur_line'])
                #logger.info('Establishing connection')
                #touch.ud['cur_line'].finish_connection(self)
                #self.destinations.append(touch.ud['cur_line'])
                #self._circle_pin()
            else:
                logger.info('Deleting connection')
                __tmp3.ud['cur_line'].delete_connection()
            return True
        else:
            return False

    def __tmp2(__tmp0, __tmp4: <FILL>):
        if __tmp4 in __tmp0.destinations:
            __tmp0.destinations.remove(__tmp4)
            # Undoing circling
            __tmp0.funbind('pos', __tmp0._bind_circle)
            __tmp0.canvas.remove(__tmp0.circle)
            del __tmp0.circle
        else:
            logger.error('Deleting connection not fully formed')

    def connect_pin(__tmp0, __tmp4):
        logger.info('Finish connection')
        __tmp4.finish_connection(__tmp0)
        __tmp0.destinations.append(__tmp4)
        __tmp0._circle_pin()

    def _circle_pin(__tmp0):
        if hasattr(__tmp0, 'circle'):
            logger.error('Circling pin twice')
            return
        with __tmp0.canvas:
            Color(*__tmp0.color)
            __tmp0.circle = Ellipse(pos=__tmp0.pos, size=__tmp0.size)
        __tmp0.fbind('pos', __tmp0._bind_circle)

    def _bind_circle(__tmp0, __tmp1, value):
        __tmp0.circle.pos = __tmp0.pos
