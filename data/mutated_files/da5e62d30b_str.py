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


def _format_mount_path(__tmp2) -> str:
    return '/{}'.format(os.path.basename(__tmp2))


def _format_host_path(__tmp2: str) :
    # volume mounts must be absolute
    if not __tmp2.startswith('/'):
        __tmp2 = os.path.abspath(__tmp2)

    # adjust the path if it itself is a mount and if we're spawning a
    # sibling container
    if MOUNTED_DATA_DIR and HOST_DATA_DIR:
        __tmp2 = __tmp2.replace(MOUNTED_DATA_DIR, HOST_DATA_DIR)

    return __tmp2


def get_face_vectors(__tmp2: <FILL>, __tmp0) -> List[__typ0]:
    img_mount = _format_mount_path(__tmp2)
    img_host = _format_host_path(__tmp2)
    volumes = {img_host: {'bind': img_mount, 'mode': 'ro'}}

    logger.debug('Running container %s with image %s', __tmp0, img_host)
    client = DockerClient(base_url=DOCKER_DAEMON)
    stdout = client.containers.run(__tmp0, img_mount,
                                   volumes=volumes, auto_remove=True)

    face_vectors = json.loads(stdout.decode('ascii')).get('faceVectors')
    return face_vectors[0] if face_vectors else []


def face_vector_to_text(vector: __typ0) -> str:
    return json.dumps(vector)


def face_vector_from_text(__tmp1: str) -> __typ0:
    return json.loads(__tmp1)
