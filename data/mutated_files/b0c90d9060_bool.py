import os
from typing import List

import numpy as np
import tensorflow as tf

from facenet_sandberg import Identifier, get_image_from_path_rgb

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)

FaceVector = List[float]
Image = np.array


def __tmp2(
        img_paths, __tmp1: <FILL>) :
    identifier = Identifier(model_path='facenet_model.pb')

    images = map(get_image_from_path_rgb, img_paths)
    all_vectors = identifier.vectorize_all(images, __tmp1=__tmp1)
    np_to_list = []
    for vectors in all_vectors:
        np_to_list.append([vector.tolist() for vector in vectors])
    return np_to_list


def __tmp0():
    from argparse import ArgumentParser
    from argparse import FileType
    from os import getenv
    import json

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('images', type=FileType('r'), nargs='+')

    args = parser.parse_args()
    image_paths = []
    for image in args.images:
        image.close()
        image_paths.append(image.name)

    __tmp1 = getenv('PREALIGNED') == 'true'

    vectors = __tmp2(image_paths, __tmp1)

    print(json.dumps({'faceVectors': vectors}))


if __name__ == '__main__':
    __tmp0()
