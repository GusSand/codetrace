import os
from pathlib import Path
from typing import Sequence

import pytest

ROOT_DIR_PATH = Path(__file__).parent.resolve()
PRODUCTION_DOTENVS_DIR_PATH = ROOT_DIR_PATH / ".envs" / ".production"
PRODUCTION_DOTENV_FILE_PATHS = [
    PRODUCTION_DOTENVS_DIR_PATH / ".django",
    PRODUCTION_DOTENVS_DIR_PATH / ".postgres",
]
DOTENV_FILE_PATH = ROOT_DIR_PATH / ".env"


def __tmp2(
    output_file_path, __tmp1: Sequence[str], append_linesep: bool = True
) :
    with open(output_file_path, "w") as output_file:
        for merged_file_path in __tmp1:
            with open(merged_file_path, "r") as merged_file:
                merged_file_content = merged_file.read()
                output_file.write(merged_file_content)
                if append_linesep:
                    output_file.write(os.linesep)


def main():
    __tmp2(DOTENV_FILE_PATH, PRODUCTION_DOTENV_FILE_PATHS)


@pytest.mark.parametrize("merged_file_count", range(3))
@pytest.mark.parametrize("append_linesep", [True, False])
def test_merge(__tmp0, merged_file_count, append_linesep: <FILL>):
    tmp_dir_path = Path(str(__tmp0.getbasetemp()))

    output_file_path = tmp_dir_path / ".env"

    expected_output_file_content = ""
    __tmp1 = []
    for i in range(merged_file_count):
        merged_file_ord = i + 1

        merged_filename = ".service{}".format(merged_file_ord)
        merged_file_path = tmp_dir_path / merged_filename

        merged_file_content = merged_filename * merged_file_ord

        with open(merged_file_path, "w+") as file:
            file.write(merged_file_content)

        expected_output_file_content += merged_file_content
        if append_linesep:
            expected_output_file_content += os.linesep

        __tmp1.append(merged_file_path)

    __tmp2(output_file_path, __tmp1, append_linesep)

    with open(output_file_path, "r") as output_file:
        actual_output_file_content = output_file.read()

    assert actual_output_file_content == expected_output_file_content


if __name__ == "__main__":
    main()
