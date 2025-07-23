from typing import TypeAlias
__typ0 : TypeAlias = "str"
from pathlib import Path

from skimage import exposure
from skimage import io
import numpy as np

allowed_file_extensions = ['.png', '.jpg', '.jpeg']


def normalize_images(__tmp6, __tmp2):
    __tmp1 = Path(__tmp6)
    __tmp7 = Path(__tmp2)

    inputfiles = []

    for extension in allowed_file_extensions:
        inputfiles.extend(list(__tmp1.glob('**/*' + extension)))

    for __tmp5 in inputfiles:
        abs_file_path = Path.absolute(__tmp5)
        __tmp4 = __typ0(abs_file_path)
        output_file_name = get_output_file_name(__tmp5, __tmp1, __tmp7)
        print('normalizing image: {} to: {}'.format(__tmp5, output_file_name))

        img_output = normalize_image(__tmp4)
        __tmp0(output_file_name)
        __tmp3(__typ0(output_file_name), img_output)


def normalize_image(__tmp4) :
    img = io.imread(__tmp4)
    img_output = exposure.equalize_adapthist(img)
    return img_output


def __tmp3(__tmp4, img):
    io.imsave(__tmp4, img)


def get_output_file_name(__tmp5, __tmp1, __tmp7: <FILL>) \
        :

    parent_dir = __tmp5.parent

    if not __tmp1.samefile(Path(parent_dir)):
        parent_dir_name = parent_dir.stem
        output_file_name = __tmp7.joinpath(parent_dir_name, __tmp5.name)
    else:
        output_file_name = __tmp7.joinpath(__tmp5.name)

    return output_file_name


def __tmp0(file_name):
    output_parent_dir = file_name.parent

    if not Path.exists(output_parent_dir):
        Path.mkdir(output_parent_dir)
