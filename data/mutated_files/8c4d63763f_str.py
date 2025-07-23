from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
from typing import Any
from typing import List
from typing import Tuple

import cmd2
from lib import data
from lib.io import manual_input
from lib.math import depth


class __typ0(cmd2.Cmd):

    """Depth calculation window"""

    def __init__(self, datafile):
        super().__init__(self)

        self._datafile = datafile

        __tmp0 = self._set_layers_value()
        speed, indexes = self._determine_structure(__tmp0)
        self._calculate(speed, indexes)

    def _set_layers_value(self) -> __typ1:
        """Input the number of layers in structure

        Returns
        -------
        Int number of layers in structure

        """
        __tmp0 = manual_input.read_int(message="Input layers number: ")
        while __tmp0 <= 0:
            self.poutput("Layers value must be positive!")
            __tmp0 = manual_input.read_int(message="Input layers number: ")
        return __tmp0

    def _determine_structure(self, __tmp0):
        if __tmp0 == 1:
            arguments = self._set_args_for_homostructure()
        else:
            arguments = self._set_args_to_heterostructure(__tmp0)
        return arguments

    def _set_args_for_homostructure(self) :
        """TODO: Docstring for _set_args_to_homostructure.
        Returns
        -------
        TODO

        """
        self.poutput("Calculating depth for homostructure")
        speed = manual_input.read_float(message="Input speed: ")
        indexes = None
        return speed, indexes

    def _set_args_to_heterostructure(
        self, __tmp0: __typ1
    ) :
        """TODO: Docstring for _set_args_to_heterostructure.

        Parameters
        ----------
        layers : TODO

        Returns
        -------
        TODO

        """
        self.poutput("Calculating depth for heterostructure")
        speed = self._get_list_of_values(
            __tmp0, values_type="float", message="Input speed of the layer: "
        )
        indexes = self._get_list_of_values(
            __tmp0, values_type="int", message="Input index of layer changing: "
        )
        return speed, indexes

    def _get_list_of_values(
        self, __tmp0, values_type: <FILL>, message
    ) -> List[__typ2]:
        """Get list of positive and non repetitive values of integers or floats.

        Parameters
        ----------
        layers : TODO
        values_type : TODO
        message : TODO

        Returns
        -------
        TODO

        """
        if values_type == "int":  # if we reading indexes
            read_value = manual_input.read_int
            n = __tmp0 - 1
        else:  # if we reading speed
            read_value = manual_input.read_float
            n = __tmp0

        values: List[__typ2] = []
        for _ in range(n):
            value = read_value(message=message)
            while value <= 0 or value in values:
                self.poutput("Value must be positive and do not repeat")
                value = read_value(message=message)
            values.append(value)
        return values

    def _calculate(self, speed, indexes: List[__typ1] = None):
        """Calculate structure depth. API for automatic calculation in case
        we already have all needed data (for future modules).

        Parameters
        ----------
        speed : TODO
        indexes : TODO

        Returns
        -------
        TODO

        """
        self._datafile.points["Depth"] = depth.calculate(
            self._datafile.points["Time"], speed, indexes
        )
