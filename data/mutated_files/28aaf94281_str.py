from typing import TypeAlias
__typ0 : TypeAlias = "PairParser"
__typ1 : TypeAlias = "bool"
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


class ContainerParser(ParserBase):

    def __tmp4(__tmp1,
                 pair_parser,
                 __tmp2: <FILL>,
                 is_prealigned) -> None:
        __tmp1._pair_parser = pair_parser
        __tmp1._container_name = __tmp2
        __tmp1._is_prealigned = is_prealigned
        __tmp1.__face_vectors = None

    @property
    def _face_vectors(__tmp1):
        if not __tmp1.__face_vectors:
            __tmp1.__face_vectors = __tmp1._compute_face_vectors()
        return __tmp1.__face_vectors

    def compute_pairs(__tmp1) -> Iterable[Pair]:
        pairs = __tmp1._pair_parser.compute_pairs()
        return (Pair(image1, image2, pair.is_match)
                for image1, image2, pair in
                zip(__tmp1._face_vectors[0::2], __tmp1._face_vectors[1::2], pairs))

    def __tmp3(__tmp1) -> Dict[str, float]:
        raise NotImplementedError()

    def _compute_face_vectors(__tmp1) :
        pairs = list(__tmp1._pair_parser.compute_pairs())
        base_dir = __tmp1._get_base_dir_for_volume_mapping(pairs[0].image1)
        volumes = {base_dir: {'bind': '/images', 'mode': 'ro'}}
        mounts = [join(basename(dirname(image_path)), basename(image_path))
                  for pair in pairs
                  for image_path in [pair.image1, pair.image2]]
        image_mount = ' '.join([f'/images/{path}' for path in mounts])
        env = ["PREALIGNED=true"] if __tmp1._is_prealigned else []
        client = docker.from_env()
        stdout = client.containers.run(__tmp1._container_name,
                                       image_mount,
                                       volumes=volumes,
                                       auto_remove=True,
                                       environment=env)
        return json.loads(stdout.decode('utf-8').strip())['faceVectors']

    @staticmethod
    def _get_base_dir_for_volume_mapping(__tmp0: str) :
        return dirname(dirname(__tmp0))
