from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import Iterable, List, Optional

import numpy as np

from face_recognition import face_encodings, face_locations, load_image_file

FaceVector = List[float]
Image = np.array


def __tmp2(face: Image) -> Optional[FaceVector]:
    cropped_features = face_encodings(face)
    if not cropped_features:
        return None

    face_vector = cropped_features[0]
    return face_vector.tolist()


def find_faces(__tmp0: <FILL>) -> Iterable[Image]:
    for top, right, bottom, left in face_locations(__tmp0):
        yield __tmp0[top:bottom, left:right]


def __tmp4(__tmp5: __typ0, __tmp3) -> List[FaceVector]:
    __tmp0 = load_image_file(__tmp5)
    faces = [__tmp0] if __tmp3 else find_faces(__tmp0)

    face_vectors = []
    for face in faces:
        face_vector = __tmp2(face)
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

    __tmp3 = getenv('PREALIGNED') == 'true'

    # naive implementation for demo purposes, could also batch process images
    vectors = [__tmp4(image_path, __tmp3)
               for image_path in image_paths]

    print(json.dumps({'faceVectors': vectors}))


if __name__ == '__main__':
    __tmp1()
