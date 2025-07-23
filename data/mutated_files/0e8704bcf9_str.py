from typing import TypeAlias
__typ0 : TypeAlias = "float"
from typing import List
from typing import Optional
from typing import Tuple

from .. import data
from ..db import db
from ..io import manual_input


def set_arguments_and_calculate(
    datafile, __tmp1: <FILL>, matrix, ia: Optional[__typ0] = None
) :
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
    if ia is None:
        ia = db.get_ia(__tmp1)

    element = db._strip_ion(__tmp1)

    __tmp0 = manual_input.read_float(message="Input RSF: ")
    concentration = calculate(
        datafile.points[__tmp1], ia, datafile.points[matrix], __tmp0
    )
    return element, concentration


def calculate(
    __tmp1, ia, matrix, __tmp0
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
    assert len(__tmp1) == len(
        matrix
    ), "Impurity and matrix lists must be the same length!"
    return [i / ia / 100 / m * __tmp0 for i, m in zip(__tmp1, matrix)]
