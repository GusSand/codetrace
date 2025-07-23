import os

from .. import data


def save(path: <FILL>, __tmp0):
    """TODO: Docstring for save.

    Parameters
    ----------
    path : TODO

    Returns
    -------
    TODO

    """
    if os.path.isdir(path):
        __tmp0.points.to_csv(
            path_or_buf=os.path.abspath(path) + "/" + __tmp0.name + ".csv",
            index=False,
        )
    else:
        __tmp0.points.to_csv(path_or_buf=os.path.abspath(path) + ".csv", index=False)
