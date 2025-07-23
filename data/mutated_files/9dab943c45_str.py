from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import Any
from typing import List
from typing import Tuple

import cmd2
from lib import data
from lib.io import manual_input
from lib.math import depth


class DepthCalculation(cmd2.Cmd):

    """Depth calculation window"""

    def __init__(__tmp1, datafile: data.Data):
        super().__init__(__tmp1)

        __tmp1._datafile = datafile

        __tmp2 = __tmp1._set_layers_value()
        __tmp3, indexes = __tmp1._determine_structure(__tmp2)
        __tmp1._calculate(__tmp3, indexes)

    def _set_layers_value(__tmp1) :
        """Input the number of layers in structure

        Returns
        -------
        Int number of layers in structure

        """
        __tmp2 = manual_input.read_int(message="Input layers number: ")
        while __tmp2 <= 0:
            __tmp1.poutput("Layers value must be positive!")
            __tmp2 = manual_input.read_int(message="Input layers number: ")
        return __tmp2

    def _determine_structure(__tmp1, __tmp2: __typ0):
        if __tmp2 == 1:
            arguments = __tmp1._set_args_for_homostructure()
        else:
            arguments = __tmp1._set_args_to_heterostructure(__tmp2)
        return arguments

    def _set_args_for_homostructure(__tmp1) -> Tuple[float, None]:
        """TODO: Docstring for _set_args_to_homostructure.
        Returns
        -------
        TODO

        """
        __tmp1.poutput("Calculating depth for homostructure")
        __tmp3 = manual_input.read_float(message="Input speed: ")
        indexes = None
        return __tmp3, indexes

    def _set_args_to_heterostructure(
        __tmp1, __tmp2
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
        __tmp3 = __tmp1._get_list_of_values(
            __tmp2, __tmp0="float", message="Input speed of the layer: "
        )
        indexes = __tmp1._get_list_of_values(
            __tmp2, __tmp0="int", message="Input index of layer changing: "
        )
        return __tmp3, indexes

    def _get_list_of_values(
        __tmp1, __tmp2: __typ0, __tmp0, message: <FILL>
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
        if __tmp0 == "int":  # if we reading indexes
            read_value = manual_input.read_int
            n = __tmp2 - 1
        else:  # if we reading speed
            read_value = manual_input.read_float
            n = __tmp2

        values: List[Any] = []
        for _ in range(n):
            value = read_value(message=message)
            while value <= 0 or value in values:
                __tmp1.poutput("Value must be positive and do not repeat")
                value = read_value(message=message)
            values.append(value)
        return values

    def _calculate(__tmp1, __tmp3: Any, indexes: List[__typ0] = None):
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
            __tmp1._datafile.points["Time"], __tmp3, indexes
        )
