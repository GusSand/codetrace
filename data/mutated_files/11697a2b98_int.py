from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import Any
from typing import List
from typing import Tuple

import cmd2
from lib import data
from lib.io import manual_input
from lib.math import depth


class DepthCalculation(cmd2.Cmd):

    """Depth calculation window"""

    def __init__(__tmp1, __tmp2):
        super().__init__(__tmp1)

        __tmp1._datafile = __tmp2

        __tmp4 = __tmp1._set_layers_value()
        __tmp5, indexes = __tmp1._determine_structure(__tmp4)
        __tmp1._calculate(__tmp5, indexes)

    def _set_layers_value(__tmp1) -> int:
        """Input the number of layers in structure

        Returns
        -------
        Int number of layers in structure

        """
        __tmp4 = manual_input.read_int(__tmp0="Input layers number: ")
        while __tmp4 <= 0:
            __tmp1.poutput("Layers value must be positive!")
            __tmp4 = manual_input.read_int(__tmp0="Input layers number: ")
        return __tmp4

    def _determine_structure(__tmp1, __tmp4: <FILL>):
        if __tmp4 == 1:
            arguments = __tmp1._set_args_for_homostructure()
        else:
            arguments = __tmp1._set_args_to_heterostructure(__tmp4)
        return arguments

    def _set_args_for_homostructure(__tmp1) :
        """TODO: Docstring for _set_args_to_homostructure.
        Returns
        -------
        TODO

        """
        __tmp1.poutput("Calculating depth for homostructure")
        __tmp5 = manual_input.read_float(__tmp0="Input speed: ")
        indexes = None
        return __tmp5, indexes

    def _set_args_to_heterostructure(
        __tmp1, __tmp4
    ) :
        """TODO: Docstring for _set_args_to_heterostructure.

        Parameters
        ----------
        layers : TODO

        Returns
        -------
        TODO

        """
        __tmp1.poutput("Calculating depth for heterostructure")
        __tmp5 = __tmp1._get_list_of_values(
            __tmp4, __tmp3="float", __tmp0="Input speed of the layer: "
        )
        indexes = __tmp1._get_list_of_values(
            __tmp4, __tmp3="int", __tmp0="Input index of layer changing: "
        )
        return __tmp5, indexes

    def _get_list_of_values(
        __tmp1, __tmp4, __tmp3, __tmp0
    ) :
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
        if __tmp3 == "int":  # if we reading indexes
            read_value = manual_input.read_int
            n = __tmp4 - 1
        else:  # if we reading speed
            read_value = manual_input.read_float
            n = __tmp4

        values: List[Any] = []
        for _ in range(n):
            value = read_value(__tmp0=__tmp0)
            while value <= 0 or value in values:
                __tmp1.poutput("Value must be positive and do not repeat")
                value = read_value(__tmp0=__tmp0)
            values.append(value)
        return values

    def _calculate(__tmp1, __tmp5, indexes: List[int] = None):
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
        __tmp1._datafile.points["Depth"] = depth.calculate(
            __tmp1._datafile.points["Time"], __tmp5, indexes
        )
