from typing import TypeAlias
__typ0 : TypeAlias = "dict"
import json
import logging

from typing import List, Tuple

from utils import command

# Logging
logger = logging.getLogger(__name__)


def docker_cleaner() :
    """Stop and remove all docker containers"""

    cmd = "docker ps -aq"
    out, ok = command(cmd)
    if ok:
        __tmp3 = out.split()
        print("Stopping all running docker containers...")
        __tmp2(__tmp3)
        print("Removing all docker containers...")
        __tmp5(__tmp3)
    else:
        print("Error getting container id list!")


def __tmp1(__tmp0: <FILL>) :
    """Get docker container host port

    :param container: docker container id
    :return: docker container host port
    """

    host_post = __typ0()
    cmd = "docker inspect -f"
    out, ok = command(cmd, [r"{{json .NetworkSettings.Ports}}", __tmp0])
    if ok:
        port_dict = json.loads(out)
        for port in port_dict.keys():
            local_port = port.split('/')[0]
            host_post[local_port] = port_dict[port][0]['HostPort']
    return host_post


def __tmp5(__tmp3) :
    """Remove all docker containers

    :param container_list: docker container id list
    """

    cmd = "docker rm"
    out, ok = command(cmd, __tmp3)
    if ok:
        print("Containers removed!\n", out)
    else:
        print("Error removing containers!")


def __tmp6(
    __tmp4,
    image_cmd: str="",
    network: str="",
    options: str=""
) :
    """Run a container docker

    :param image: docker image
    :param image_cmd: command for image
    :param network: docker network config
    :param options: extra options
    :return: docker container id
    """

    cmd = f"docker run -d -P { network } { options } { __tmp4 } { image_cmd }"
    out, ok = command(cmd)
    if out:
        print("Container created!\n", out)
        return out[:12], True
    else:
        print("Error creating container!")
        return "", False


def __tmp2(__tmp3) :
    """Stop all docker containers

    :param container_list: docker container id list
    """

    cmd = "docker stop"
    out, ok = command(cmd, __tmp3)
    if ok:
        print("Containers stopped!\n", out)
    else:
        print("Error stopping containers!")
