from typing import List
from typing import Tuple

import pandas as pd

from .. import data


def asc(filename: str) -> data.Data:
    """Reader for raw data from CAMECA IMS-7f.

    :filename: file to read
    :returns: data object, containing name, points and etc

    """
    with open(filename, "r") as file:
        __tmp3 = []
        for line in file.read().splitlines():
            __tmp3.append(line)
    name = _find_file_name(__tmp3)
    __tmp2, bad_points = _cut_header_and_points(__tmp3)
    header = _reshape_ion_string(__tmp2)
    __tmp1 = __tmp0(bad_points)
    __tmp1 = pd.DataFrame(__tmp1, columns=header)
    return data.Data(name=name, __tmp1=__tmp1)


def _find_file_name(__tmp3: List[str]) -> str:
    """Find filename, writen inside file itself.

    :raw_text: raw opened data
    :returns: filename

    """
    raw_name_string = __tmp3[2]
    name = raw_name_string.split()[-1]
    return name.split(".")[0]


def _cut_header_and_points(__tmp3: List[str]) -> Tuple[str, List[str]]:
    """Cut ion names and datapoints from opened file.

    :raw_data: raw opened data
    :returns: header string, points

    """
    start_line = __tmp3.index("*** DATA START ***") + 3
    end_line = __tmp3.index("*** DATA END ***") - 1
    header = __tmp3[start_line]
    __tmp1 = __tmp3[start_line + 2 : end_line]
    return header, __tmp1


def _reshape_ion_string(__tmp2: <FILL>) :
    """Create list of columns for pandas.DataFrame.

    :header: string with ion names
    :returns: list of columns

    """
    header = [ion.replace(" ", "") for ion in filter(None, __tmp2.split("\t"))]
    header.insert(0, "Time")
    return header


def __tmp0(__tmp1: List[str]) -> List[List[float]]:
    """Reshape strings with points to float, remove unnecessary points

    :points: strings with data needed
    :returns: array for future pandas.DataFrame

    """
    grid, data = [], []
    for line in __tmp1:
        x, *y = map(float, line.split())
        # delete remain time columns
        y = y[0::2]
        grid.append(x)
        data.append(y)

    # insert time column into array
    for i, j in enumerate(grid):
        data[i].insert(0, grid[i])
    return data
