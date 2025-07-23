from typing import List
from typing import Optional
from typing import Tuple

from .. import data
from ..db import db
from ..io import manual_input


def set_arguments_and_calculate(
    datafile, impurity: str, matrix: <FILL>, ia: Optional[float] = None
) -> Tuple[str, List[float]]:
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
        ia = db.get_ia(impurity)

    element = db._strip_ion(impurity)

    __tmp1 = manual_input.read_float(message="Input RSF: ")
    concentration = __tmp0(
        datafile.points[impurity], ia, datafile.points[matrix], __tmp1
    )
    return element, concentration


def __tmp0(
    impurity: List[float], ia, matrix, __tmp1
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
    assert len(impurity) == len(
        matrix
    ), "Impurity and matrix lists must be the same length!"
    return [i / ia / 100 / m * __tmp1 for i, m in zip(impurity, matrix)]
