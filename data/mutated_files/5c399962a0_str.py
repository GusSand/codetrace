from typing import List
import json
import os

from docker import DockerClient

from faceanalysis.log import get_logger
from faceanalysis.settings import DOCKER_DAEMON
from faceanalysis.settings import HOST_DATA_DIR
from faceanalysis.settings import MOUNTED_DATA_DIR

__typ0 = List[float]
logger = get_logger(__name__)


def __tmp3(__tmp5: <FILL>) -> str:
    return '/{}'.format(os.path.basename(__tmp5))


def __tmp4(__tmp5) -> str:
    # volume mounts must be absolute
    if not __tmp5.startswith('/'):
        __tmp5 = os.path.abspath(__tmp5)

    # adjust the path if it itself is a mount and if we're spawning a
    # sibling container
    if MOUNTED_DATA_DIR and HOST_DATA_DIR:
        __tmp5 = __tmp5.replace(MOUNTED_DATA_DIR, HOST_DATA_DIR)

    return __tmp5


def get_face_vectors(__tmp5: str, __tmp2) -> List[__typ0]:
    img_mount = __tmp3(__tmp5)
    img_host = __tmp4(__tmp5)
    volumes = {img_host: {'bind': img_mount, 'mode': 'ro'}}

    logger.debug('Running container %s with image %s', __tmp2, img_host)
    client = DockerClient(base_url=DOCKER_DAEMON)
    stdout = client.containers.run(__tmp2, img_mount,
                                   volumes=volumes, auto_remove=True)

    face_vectors = json.loads(stdout.decode('ascii')).get('faceVectors')
    return face_vectors[0] if face_vectors else []


def face_vector_to_text(vector) -> str:
    return json.dumps(vector)


def __tmp1(__tmp0: str) -> __typ0:
    return json.loads(__tmp0)
