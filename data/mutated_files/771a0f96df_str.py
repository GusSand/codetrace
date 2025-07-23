from typing import List
from typing import Tuple

import pandas as pd

from .. import data


def asc(filename: <FILL>) :
    """Reader for raw data from CAMECA IMS-7f.

    :filename: file to read
    :returns: data object, containing name, points and etc

    """
    with open(filename, "r") as file:
        __tmp1 = []
        for line in file.read().splitlines():
            __tmp1.append(line)
    name = _find_file_name(__tmp1)
    bad_header, bad_points = _cut_header_and_points(__tmp1)
    header = _reshape_ion_string(bad_header)
    __tmp0 = _reshape_points(bad_points)
    __tmp0 = pd.DataFrame(__tmp0, columns=header)
    return data.Data(name=name, __tmp0=__tmp0)


def _find_file_name(__tmp1) :
    """Find filename, writen inside file itself.

    :raw_text: raw opened data
    :returns: filename

    """
    raw_name_string = __tmp1[2]
    name = raw_name_string.split()[-1]
    return name.split(".")[0]


def _cut_header_and_points(__tmp1: List[str]) :
    """Cut ion names and datapoints from opened file.

    :raw_data: raw opened data
    :returns: header string, points

    """
    start_line = __tmp1.index("*** DATA START ***") + 3
    end_line = __tmp1.index("*** DATA END ***") - 1
    header = __tmp1[start_line]
    __tmp0 = __tmp1[start_line + 2 : end_line]
    return header, __tmp0


def _reshape_ion_string(bad_header: str) -> List[str]:
    """Create list of columns for pandas.DataFrame.

    :header: string with ion names
    :returns: list of columns

    """
    header = [ion.replace(" ", "") for ion in filter(None, bad_header.split("\t"))]
    header.insert(0, "Time")
    return header


def _reshape_points(__tmp0) -> List[List[float]]:
    """Reshape strings with points to float, remove unnecessary points

    :points: strings with data needed
    :returns: array for future pandas.DataFrame

    """
    grid, data = [], []
    for line in __tmp0:
        x, *y = map(float, line.split())
        # delete remain time columns
        y = y[0::2]
        grid.append(x)
        data.append(y)

    # insert time column into array
    for i, j in enumerate(grid):
        data[i].insert(0, grid[i])
    return data
