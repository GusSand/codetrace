from typing import TypeAlias
__typ0 : TypeAlias = "Path"
from pathlib import Path

from skimage import exposure
from skimage import io
import numpy as np

allowed_file_extensions = ['.png', '.jpg', '.jpeg']


def __tmp0(inputdirectory: str, outputdirectory: <FILL>):
    inputpath = __typ0(inputdirectory)
    __tmp2 = __typ0(outputdirectory)

    inputfiles = []

    for extension in allowed_file_extensions:
        inputfiles.extend(list(inputpath.glob('**/*' + extension)))

    for infile in inputfiles:
        abs_file_path = __typ0.absolute(infile)
        file_path = str(abs_file_path)
        output_file_name = get_output_file_name(infile, inputpath, __tmp2)
        print('normalizing image: {} to: {}'.format(infile, output_file_name))

        img_output = normalize_image(file_path)
        ensure_dir_exists_for_file(output_file_name)
        __tmp1(str(output_file_name), img_output)


def normalize_image(file_path) -> np.ndarray:
    img = io.imread(file_path)
    img_output = exposure.equalize_adapthist(img)
    return img_output


def __tmp1(file_path: str, img: np.ndarray):
    io.imsave(file_path, img)


def get_output_file_name(infile: __typ0, inputpath: __typ0, __tmp2: __typ0) \
        -> __typ0:

    parent_dir = infile.parent

    if not inputpath.samefile(__typ0(parent_dir)):
        parent_dir_name = parent_dir.stem
        output_file_name = __tmp2.joinpath(parent_dir_name, infile.name)
    else:
        output_file_name = __tmp2.joinpath(infile.name)

    return output_file_name


def ensure_dir_exists_for_file(file_name: __typ0):
    output_parent_dir = file_name.parent

    if not __typ0.exists(output_parent_dir):
        __typ0.mkdir(output_parent_dir)
