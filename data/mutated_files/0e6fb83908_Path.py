from typing import TypeAlias
__typ0 : TypeAlias = "str"
from pathlib import Path

from skimage import exposure
from skimage import io
import numpy as np

allowed_file_extensions = ['.png', '.jpg', '.jpeg']


def __tmp7(__tmp10, __tmp4):
    __tmp1 = Path(__tmp10)
    __tmp11 = Path(__tmp4)

    inputfiles = []

    for extension in allowed_file_extensions:
        inputfiles.extend(list(__tmp1.glob('**/*' + extension)))

    for __tmp9 in inputfiles:
        abs_file_path = Path.absolute(__tmp9)
        __tmp8 = __typ0(abs_file_path)
        output_file_name = get_output_file_name(__tmp9, __tmp1, __tmp11)
        print('normalizing image: {} to: {}'.format(__tmp9, output_file_name))

        img_output = __tmp3(__tmp8)
        __tmp2(output_file_name)
        __tmp5(__typ0(output_file_name), img_output)


def __tmp3(__tmp8: __typ0) :
    __tmp6 = io.imread(__tmp8)
    img_output = exposure.equalize_adapthist(__tmp6)
    return img_output


def __tmp5(__tmp8, __tmp6):
    io.imsave(__tmp8, __tmp6)


def get_output_file_name(__tmp9, __tmp1: <FILL>, __tmp11) \
        :

    parent_dir = __tmp9.parent

    if not __tmp1.samefile(Path(parent_dir)):
        parent_dir_name = parent_dir.stem
        output_file_name = __tmp11.joinpath(parent_dir_name, __tmp9.name)
    else:
        output_file_name = __tmp11.joinpath(__tmp9.name)

    return output_file_name


def __tmp2(__tmp0):
    output_parent_dir = __tmp0.parent

    if not Path.exists(output_parent_dir):
        Path.mkdir(output_parent_dir)
