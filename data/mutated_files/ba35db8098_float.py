from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import List
from typing import Optional
from typing import Tuple

from .. import data
from ..db import db
from ..io import manual_input


def __tmp0(
    datafile: data.Data, __tmp4: __typ0, __tmp2: __typ0, __tmp1: Optional[float] = None
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
        __tmp1 = db.get_ia(__tmp4)

    element = db._strip_ion(__tmp4)

    __tmp3 = manual_input.read_float(message="Input RSF: ")
    concentration = __tmp5(
        datafile.points[__tmp4], __tmp1, datafile.points[__tmp2], __tmp3
    )
    return element, concentration


def __tmp5(
    __tmp4, __tmp1: float, __tmp2, __tmp3: <FILL>
) -> List[float]:
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
    assert len(__tmp4) == len(
        __tmp2
    ), "Impurity and matrix lists must be the same length!"
    return [i / __tmp1 / 100 / m * __tmp3 for i, m in zip(__tmp4, __tmp2)]
