from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "bool"
from typing import Iterable, List, Optional

import numpy as np

from face_recognition import face_encodings, face_locations, load_image_file

FaceVector = List[float]
Image = np.array


def __tmp3(face: <FILL>) :
    cropped_features = face_encodings(face)
    if not cropped_features:
        return None

    face_vector = cropped_features[0]
    return face_vector.tolist()


def __tmp4(__tmp0) -> Iterable[Image]:
    for top, right, bottom, left in face_locations(__tmp0):
        yield __tmp0[top:bottom, left:right]


def get_face_vectors(__tmp5: __typ0, __tmp2) :
    __tmp0 = load_image_file(__tmp5)
    faces = [__tmp0] if __tmp2 else __tmp4(__tmp0)

    face_vectors = []
    for face in faces:
        face_vector = __tmp3(face)
        if face_vector:
            face_vectors.append(face_vector)
    return face_vectors


def __tmp1():
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

    __tmp2 = getenv('PREALIGNED') == 'true'

    # naive implementation for demo purposes, could also batch process images
    vectors = [get_face_vectors(image_path, __tmp2)
               for image_path in image_paths]

    print(json.dumps({'faceVectors': vectors}))


if __name__ == '__main__':
    __tmp1()
