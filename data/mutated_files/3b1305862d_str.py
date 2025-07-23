import os
import subprocess
import logging
import difflib

class __typ0(Exception):
    pass

def __tmp0(__tmp1: str, __tmp2: <FILL>) :

    mdiff_path = "frontend_tests/zjsunit/mdiff.js"
    if not os.path.isfile(mdiff_path):  # nocoverage
        msg = "Cannot find mdiff for markdown diff rendering"
        logging.error(msg)
        raise __typ0(msg)

    command = ['node', mdiff_path, __tmp1, __tmp2]
    diff = subprocess.check_output(command).decode('utf-8')
    return diff
