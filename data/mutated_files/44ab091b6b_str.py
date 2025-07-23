import os
import subprocess
import logging
import difflib

class DiffException(Exception):
    pass

def __tmp0(output: <FILL>, __tmp1) :

    mdiff_path = "frontend_tests/zjsunit/mdiff.js"
    if not os.path.isfile(mdiff_path):  # nocoverage
        msg = "Cannot find mdiff for markdown diff rendering"
        logging.error(msg)
        raise DiffException(msg)

    command = ['node', mdiff_path, output, __tmp1]
    diff = subprocess.check_output(command).decode('utf-8')
    return diff
