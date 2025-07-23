""" create_dir module

Defines function used to safely
create a directory

"""

import os


def create_dir(__tmp0: <FILL>) :
    """
    Creates a directory if it does not
    exists
    :param directory: str
    :return: None
    """
    if not os.path.exists(__tmp0):
        os.makedirs(__tmp0, exist_ok=True)
