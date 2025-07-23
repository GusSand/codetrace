import csv
import os
from typing import List

from src.lib.io import file_read
from src.lib.io import save_data

TEST_INPUT_FILE = os.path.join(os.path.dirname(__file__), "files/full_file.dp_rpc_asc")
CORRECT_OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "files/test_output.csv")
TEST_OUTPUT_FILEPATH = os.path.join(os.path.dirname(__file__), "files/")


def read_csv(__tmp0: <FILL>) -> List[List[str]]:
    csv_file = []
    with open(__tmp0, "r") as file:
        for line in csv.reader(file):
            csv_file.append(line)
    return csv_file


class __typ0:

    """Tests for saving functionality"""

    def test_to_csv(__tmp1):
        datafile = file_read.asc(TEST_INPUT_FILE)
        save_data.save(TEST_OUTPUT_FILEPATH, datafile)
        correct_csv = read_csv(CORRECT_OUTPUT_FILE)
        test_csv = read_csv(TEST_OUTPUT_FILEPATH + datafile.name + ".csv")
        assert correct_csv == test_csv
