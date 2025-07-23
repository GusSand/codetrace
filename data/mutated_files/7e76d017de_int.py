from typing import TypeAlias
__typ1 : TypeAlias = "str"
from typing import Any
from typing import List
from typing import Tuple

import cmd2
from lib import data
from lib.io import manual_input
from lib.math import depth


class __typ0(cmd2.Cmd):

    """Depth calculation window"""

    def __init__(__tmp0, datafile):
        super().__init__(__tmp0)

        __tmp0._datafile = datafile

        __tmp1 = __tmp0._set_layers_value()
        __tmp2, indexes = __tmp0._determine_structure(__tmp1)
        __tmp0._calculate(__tmp2, indexes)

    def _set_layers_value(__tmp0) -> int:
        """Input the number of layers in structure

        Returns
        -------
        Int number of layers in structure

        """
        __tmp1 = manual_input.read_int(message="Input layers number: ")
        while __tmp1 <= 0:
            __tmp0.poutput("Layers value must be positive!")
            __tmp1 = manual_input.read_int(message="Input layers number: ")
        return __tmp1

    def _determine_structure(__tmp0, __tmp1: int):
        if __tmp1 == 1:
            arguments = __tmp0._set_args_for_homostructure()
        else:
            arguments = __tmp0._set_args_to_heterostructure(__tmp1)
        return arguments

    def _set_args_for_homostructure(__tmp0) :
        """TODO: Docstring for _set_args_to_homostructure.
        Returns
        -------
        TODO

        """
        __tmp0.poutput("Calculating depth for homostructure")
        __tmp2 = manual_input.read_float(message="Input speed: ")
        indexes = None
        return __tmp2, indexes

    def _set_args_to_heterostructure(
        __tmp0, __tmp1: <FILL>
    ) :
        """TODO: Docstring for _set_args_to_heterostructure.

        Parameters
        ----------
        layers : TODO

        Returns
        -------
        TODO

        """
        __tmp0.poutput("Calculating depth for heterostructure")
        __tmp2 = __tmp0._get_list_of_values(
            __tmp1, values_type="float", message="Input speed of the layer: "
        )
        indexes = __tmp0._get_list_of_values(
            __tmp1, values_type="int", message="Input index of layer changing: "
        )
        return __tmp2, indexes

    def _get_list_of_values(
        __tmp0, __tmp1, values_type: __typ1, message: __typ1
    ) -> List[Any]:
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
            n = __tmp1 - 1
        else:  # if we reading speed
            read_value = manual_input.read_float
            n = __tmp1

        values: List[Any] = []
        for _ in range(n):
            value = read_value(message=message)
            while value <= 0 or value in values:
                __tmp0.poutput("Value must be positive and do not repeat")
                value = read_value(message=message)
            values.append(value)
        return values

    def _calculate(__tmp0, __tmp2: Any, indexes: List[int] = None):
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
        __tmp0._datafile.points["Depth"] = depth.calculate(
            __tmp0._datafile.points["Time"], __tmp2, indexes
        )
