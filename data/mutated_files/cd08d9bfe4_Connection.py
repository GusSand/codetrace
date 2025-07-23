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
    type_ = ObjectProperty(Type.ANY)

    @abstractmethod
    def on_touch_down(__tmp1, touch) :
        raise NotImplementedError

    @abstractmethod
    def on_touch_up(__tmp1, touch) -> bool:
        raise NotImplementedError

    @abstractmethod
    def on_connection_delete(__tmp1, __tmp2):
        raise NotImplementedError

    @abstractmethod
    def connect_pin(__tmp1, __tmp2: <FILL>):
        raise NotImplementedError

    def typesafe(__tmp1, other) :
        """ Tells if a relation between two pins is typesafe. """
        if __tmp1.block == other.block or __tmp1.__class__ == other.__class__:
            return False
        elif __tmp1.type_ == Type.ANY or other.type_ == Type.ANY:
            return True  # Anything is possible with ANY
        else:
            return __tmp1.type_ == other.type_

    # Hack
    def on_type_(__tmp1, __tmp0, value):
        """ If the kv lang was a bit smarted this would not be needed
        """
        __tmp1.color = value.value
