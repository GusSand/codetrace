from typing import TypeAlias
__typ0 : TypeAlias = "str"
from pathlib import Path

from skimage import exposure
from skimage import io
import numpy as np

allowed_file_extensions = ['.png', '.jpg', '.jpeg']


def __tmp6(__tmp9, __tmp4: __typ0):
    __tmp2 = Path(__tmp9)
    __tmp10 = Path(__tmp4)

    inputfiles = []

    for extension in allowed_file_extensions:
        inputfiles.extend(list(__tmp2.glob('**/*' + extension)))

    for __tmp8 in inputfiles:
        abs_file_path = Path.absolute(__tmp8)
        __tmp7 = __typ0(abs_file_path)
        output_file_name = __tmp0(__tmp8, __tmp2, __tmp10)
        print('normalizing image: {} to: {}'.format(__tmp8, output_file_name))

        img_output = __tmp3(__tmp7)
        ensure_dir_exists_for_file(output_file_name)
        save_image(__typ0(output_file_name), img_output)


def __tmp3(__tmp7: __typ0) :
    __tmp5 = io.imread(__tmp7)
    img_output = exposure.equalize_adapthist(__tmp5)
    return img_output


def save_image(__tmp7: __typ0, __tmp5):
    io.imsave(__tmp7, __tmp5)


def __tmp0(__tmp8: Path, __tmp2: Path, __tmp10) \
        -> Path:

    parent_dir = __tmp8.parent

    if not __tmp2.samefile(Path(parent_dir)):
        parent_dir_name = parent_dir.stem
        output_file_name = __tmp10.joinpath(parent_dir_name, __tmp8.name)
    else:
        output_file_name = __tmp10.joinpath(__tmp8.name)

    return output_file_name


def ensure_dir_exists_for_file(__tmp1: <FILL>):
    output_parent_dir = __tmp1.parent

    if not Path.exists(output_parent_dir):
        Path.mkdir(output_parent_dir)
