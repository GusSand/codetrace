from typing import TypeAlias
__typ2 : TypeAlias = "Type"
__typ1 : TypeAlias = "bool"
from persimmon.view.pins.circularbutton import CircularButton  # MYPY HACK
from persimmon.view.util import Type, AbstractWidget, Connection
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.graphics import Color, Ellipse, Line
from kivy.input import MotionEvent
from abc import abstractmethod

Builder.load_file('persimmon/view/pins/pin.kv')

class __typ0(CircularButton, metaclass=AbstractWidget):
    val = ObjectProperty(None, force_dispatch=True)
    block = ObjectProperty()
    type_ = ObjectProperty(__typ2.ANY)

    @abstractmethod
    def on_touch_down(__tmp2, __tmp1: MotionEvent) -> __typ1:
        raise NotImplementedError

    @abstractmethod
    def on_touch_up(__tmp2, __tmp1) -> __typ1:
        raise NotImplementedError

    @abstractmethod
    def __tmp0(__tmp2, __tmp3: <FILL>):
        raise NotImplementedError

    @abstractmethod
    def connect_pin(__tmp2, __tmp3: Connection):
        raise NotImplementedError

    def typesafe(__tmp2, other) -> __typ1:
        """ Tells if a relation between two pins is typesafe. """
        if __tmp2.block == other.block or __tmp2.__class__ == other.__class__:
            return False
        elif __tmp2.type_ == __typ2.ANY or other.type_ == __typ2.ANY:
            return True  # Anything is possible with ANY
        else:
            return __tmp2.type_ == other.type_

    # Hack
    def on_type_(__tmp2, instance, value):
        """ If the kv lang was a bit smarted this would not be needed
        """
        __tmp2.color = value.value
