from typing import TypeAlias
__typ0 : TypeAlias = "Path"
from pathlib import Path

from skimage import exposure
from skimage import io
import numpy as np

allowed_file_extensions = ['.png', '.jpg', '.jpeg']


def normalize_images(inputdirectory: str, __tmp1):
    inputpath = __typ0(inputdirectory)
    __tmp2 = __typ0(__tmp1)

    inputfiles = []

    for extension in allowed_file_extensions:
        inputfiles.extend(list(inputpath.glob('**/*' + extension)))

    for __tmp3 in inputfiles:
        abs_file_path = __typ0.absolute(__tmp3)
        file_path = str(abs_file_path)
        output_file_name = get_output_file_name(__tmp3, inputpath, __tmp2)
        print('normalizing image: {} to: {}'.format(__tmp3, output_file_name))

        img_output = normalize_image(file_path)
        ensure_dir_exists_for_file(output_file_name)
        save_image(str(output_file_name), img_output)


def normalize_image(file_path: <FILL>) -> np.ndarray:
    img = io.imread(file_path)
    img_output = exposure.equalize_adapthist(img)
    return img_output


def save_image(file_path: str, img: np.ndarray):
    io.imsave(file_path, img)


def get_output_file_name(__tmp3: __typ0, inputpath: __typ0, __tmp2: __typ0) \
        -> __typ0:

    parent_dir = __tmp3.parent

    if not inputpath.samefile(__typ0(parent_dir)):
        parent_dir_name = parent_dir.stem
        output_file_name = __tmp2.joinpath(parent_dir_name, __tmp3.name)
    else:
        output_file_name = __tmp2.joinpath(__tmp3.name)

    return output_file_name


def ensure_dir_exists_for_file(__tmp0: __typ0):
    output_parent_dir = __tmp0.parent

    if not __typ0.exists(output_parent_dir):
        __typ0.mkdir(output_parent_dir)
