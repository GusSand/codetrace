from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Functionality to get public keys from a public key store"""
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from typing import Tuple

from syncr_backend.constants import TRACKER_OK_RESULT
from syncr_backend.constants import TrackerRequest
from syncr_backend.external_interface.dht_util import \
    get_dht
from syncr_backend.external_interface.store_exceptions import (
    IncompleteConfigError
)
from syncr_backend.external_interface.store_exceptions import (
    UnsupportedOptionError
)
from syncr_backend.external_interface.tracker_util import (
    send_request_to_tracker
)
from syncr_backend.util.fileio_util import load_config_file
from syncr_backend.util.log_util import get_logger


logger = get_logger(__name__)


async def get_public_key_store(node_id) -> "PublicKeyStore":
    """
    Provides a PublicKeyStore either by means of DHT or tracker depending
    on config file

    :param node_id: This node's node id
    :raises UnsupportedOptionError: If the config specifies an unknown DPS type
    :raises IncompleteConfigError: If the config does not have the necessary \
            values
    :return: PublicKeyStore
    """
    config_file = await load_config_file()

    try:
        logger.debug("Keystore is of type %s", config_file['type'])
        if config_file['type'] == 'tracker':
            pks = TrackerKeyStore(
                node_id, config_file['ip'], int(config_file['port']),
            )
            return pks
        elif config_file['type'] == 'dht':
            return DHTKeyStore(
                node_id,
                list(
                    zip(
                        config_file['bootstrap_ips'],
                        config_file['bootstrap_ports'],
                    ),
                ),
                config_file['listen_port'],
            )
        else:
            raise UnsupportedOptionError()
    except KeyError:
        raise IncompleteConfigError()


class PublicKeyStore(ABC):
    """Abstract base class for storage and retrieval of public keys"""

    @abstractmethod
    async def __tmp2(__tmp0, __tmp6: <FILL>) -> bool:
        """
        Add a key to the PKS

        :param key: The key
        :return: bool of whether it was successful
        """
        pass

    @abstractmethod
    async def __tmp1(
        __tmp0, __tmp7,
    ) :
        """
        Request a key from the PKS

        :param request_node_id: The node id to look up
        :return: A tuple of success and a key string
        """
        pass


class DHTKeyStore(PublicKeyStore):
    def __tmp4(
        __tmp0,
        node_id: bytes, bootstrap_list,
        __tmp5: int,
    ) -> None:
        """
        Sets up tracker key store

        :param node_id: node id and SHA256 hash
        :param bootstrap_list: list of ip,port to bootstrap connect to dht
        """
        __tmp0.node_id = node_id
        __tmp0.node_instance = get_dht()

    async def __tmp2(__tmp0, __tmp6: bytes) -> bool:
        """
        Sets the public key of the this node on the DHT

        :param key: 4096 RSA public key
        :return: boolean on success of setting key
        """
        try:
            await __tmp0.node_instance.set(__tmp0.node_id, __tmp6)
            return True
        except Exception:
            return False

    async def __tmp1(
        __tmp0,
        __tmp7,
    ) :
        """
        Asks DHT for the public key of a given node for sake of signature
        verification

        :param request_node_id: SHA256 hash
        :return: boolean (success of getting key), 2048 RSA public key \
                (if boolean is True)
        """

        result = __typ0(await __tmp0.node_instance.get(__tmp7), 'utf-8')
        if result is not None:
            return True, result
        else:
            return False, ""


class TrackerKeyStore(PublicKeyStore):
    """Tracker based implementation of the public key store"""

    def __tmp4(__tmp0, node_id: bytes, __tmp3: __typ0, port: int) -> None:
        """
        Sets up a TrackerKeyStore with the trackers ip and port and the id of
        the given node

        :param node_id: SHA256 hash
        :param ip: string of ipv4 or ipv6
        :param port: port for the tracker connection
        """
        __tmp0.node_id = node_id
        __tmp0.tracker_ip = __tmp3
        __tmp0.tracker_port = port

    async def __tmp2(__tmp0, __tmp6) :
        """
        Sets the public key of the this node on the tracker

        :param key: 4096 RSA public key
        :return: boolean on success of setting key
        """
        request = {
            'request_type': int(TrackerRequest.POST_KEY),
            'node_id': __tmp0.node_id,
            'data': __tmp6,
        }

        response = await send_request_to_tracker(
            request, __tmp0.tracker_ip,
            __tmp0.tracker_port,
        )
        logger.debug("tracker set key response: %s", response)
        if response.get('result') == TRACKER_OK_RESULT:
            return True
        else:
            return False

    async def __tmp1(
        __tmp0, __tmp7: bytes,
    ) :
        """
        Asks tracker for the public key of a given node for sake of signature
        verification

        :param request_node_id: SHA256 hash
        :return: boolean (success of getting key), 2048 RSA public key \
                (if boolean is True)
        """
        request = {
            'request_type': int(TrackerRequest.GET_KEY),
            'node_id': __tmp7,
        }

        response = await send_request_to_tracker(
            request, __tmp0.tracker_ip,
            __tmp0.tracker_port,
        )
        logger.debug("tracker get key response: %s", response)
        if response.get('result') == TRACKER_OK_RESULT:
            return True, response.get('data')
        else:
            return False, 'NO PUBLIC KEY AVAILABLE'
