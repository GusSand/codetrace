from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import List
from typing import Optional
from typing import Tuple

from .. import data
from ..db import db
from ..io import manual_input


def __tmp0(
    __tmp2: data.Data, __tmp5: __typ0, __tmp3, __tmp1: Optional[float] = None
) -> Tuple[__typ0, List[float]]:
    """Calculate atomic concentration of impurity.
    API for manual parameters setting.

    Parameters
    ----------
    impurity : name of the impurity
    matrix : name of the matrix

    Returns
    -------
    List of points of element atomic concentration [cm^{-3}]

    """
    if __tmp1 is None:
        __tmp1 = db.get_ia(__tmp5)

    element = db._strip_ion(__tmp5)

    __tmp4 = manual_input.read_float(message="Input RSF: ")
    concentration = __tmp6(
        __tmp2.points[__tmp5], __tmp1, __tmp2.points[__tmp3], __tmp4
    )
    return element, concentration


def __tmp6(
    __tmp5: List[float], __tmp1: <FILL>, __tmp3: List[float], __tmp4: float
) :
    """Calculate concentration of element

    Parameters
    ----------
    impurity : list of points of impurity ion impulses/sec
    ia : isotopic abundance of the impurity
    matrix : list of points of matrix ion impulses/sec
    rsf : Relative Sensitivity Factor for the impurity in the matrix

    Returns
    -------
    List of points of element atomic concentration [cm^{-3}]

    """
    assert len(__tmp5) == len(
        __tmp3
    ), "Impurity and matrix lists must be the same length!"
    return [i / __tmp1 / 100 / m * __tmp4 for i, m in zip(__tmp5, __tmp3)]
