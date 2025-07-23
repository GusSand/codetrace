from typing import TypeAlias
__typ1 : TypeAlias = "Connection"
__typ0 : TypeAlias = "MotionEvent"
__typ3 : TypeAlias = "bool"
from persimmon.view.pins.circularbutton import CircularButton  # MYPY HACK
from persimmon.view.util import Type, AbstractWidget, Connection
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.graphics import Color, Ellipse, Line
from kivy.input import MotionEvent
from abc import abstractmethod

Builder.load_file('persimmon/view/pins/pin.kv')

class __typ2(CircularButton, metaclass=AbstractWidget):
    val = ObjectProperty(None, force_dispatch=True)
    block = ObjectProperty()
    type_ = ObjectProperty(Type.ANY)

    @abstractmethod
    def __tmp5(__tmp0, __tmp3: __typ0) :
        raise NotImplementedError

    @abstractmethod
    def on_touch_up(__tmp0, __tmp3) -> __typ3:
        raise NotImplementedError

    @abstractmethod
    def __tmp2(__tmp0, __tmp6: __typ1):
        raise NotImplementedError

    @abstractmethod
    def __tmp7(__tmp0, __tmp6):
        raise NotImplementedError

    def __tmp9(__tmp0, __tmp8: 'Pin') :
        """ Tells if a relation between two pins is typesafe. """
        if __tmp0.block == __tmp8.block or __tmp0.__class__ == __tmp8.__class__:
            return False
        elif __tmp0.type_ == Type.ANY or __tmp8.type_ == Type.ANY:
            return True  # Anything is possible with ANY
        else:
            return __tmp0.type_ == __tmp8.type_

    # Hack
    def __tmp1(__tmp0, __tmp4, value: <FILL>):
        """ If the kv lang was a bit smarted this would not be needed
        """
        __tmp0.color = value.value
