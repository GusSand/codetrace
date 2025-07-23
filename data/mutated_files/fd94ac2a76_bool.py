from typing import TypeAlias
__typ0 : TypeAlias = "PairParser"
__typ1 : TypeAlias = "str"
import json
from os.path import basename
from os.path import dirname
from os.path import join
from parser.pair import Pair
from parser.pair_parser import PairParser
from parser.parser_base import ParserBase
from typing import Dict
from typing import Iterable
from typing import List

import docker


class __typ2(ParserBase):

    def __init__(__tmp0,
                 pair_parser,
                 container_name,
                 is_prealigned: <FILL>) :
        __tmp0._pair_parser = pair_parser
        __tmp0._container_name = container_name
        __tmp0._is_prealigned = is_prealigned
        __tmp0.__face_vectors = None

    @property
    def _face_vectors(__tmp0):
        if not __tmp0.__face_vectors:
            __tmp0.__face_vectors = __tmp0._compute_face_vectors()
        return __tmp0.__face_vectors

    def compute_pairs(__tmp0) :
        pairs = __tmp0._pair_parser.compute_pairs()
        return (Pair(image1, image2, pair.is_match)
                for image1, image2, pair in
                zip(__tmp0._face_vectors[0::2], __tmp0._face_vectors[1::2], pairs))

    def compute_metrics(__tmp0) :
        raise NotImplementedError()

    def _compute_face_vectors(__tmp0) :
        pairs = list(__tmp0._pair_parser.compute_pairs())
        base_dir = __tmp0._get_base_dir_for_volume_mapping(pairs[0].image1)
        volumes = {base_dir: {'bind': '/images', 'mode': 'ro'}}
        mounts = [join(basename(dirname(image_path)), basename(image_path))
                  for pair in pairs
                  for image_path in [pair.image1, pair.image2]]
        image_mount = ' '.join([f'/images/{path}' for path in mounts])
        env = ["PREALIGNED=true"] if __tmp0._is_prealigned else []
        client = docker.from_env()
        stdout = client.containers.run(__tmp0._container_name,
                                       image_mount,
                                       volumes=volumes,
                                       auto_remove=True,
                                       environment=env)
        return json.loads(stdout.decode('utf-8').strip())['faceVectors']

    @staticmethod
    def _get_base_dir_for_volume_mapping(full_image_path) :
        return dirname(dirname(full_image_path))
