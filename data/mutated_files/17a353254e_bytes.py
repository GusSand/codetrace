from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
"""Functionality to get public keys from a public key store"""
from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from typing import Tuple

from syncr_backend.constants import TRACKER_OK_RESULT
from syncr_backend.constants import TRACKER_REQUEST_GET_KEY
from syncr_backend.constants import TRACKER_REQUEST_POST_KEY
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


async def get_public_key_store(node_id) :
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
            pks = __typ0(
                node_id, config_file['ip'], int(config_file['port']),
            )
            return pks
        elif config_file['type'] == 'dht':
            return __typ2(
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


class __typ3(ABC):
    """Abstract base class for storage and retrieval of public keys"""

    @abstractmethod
    async def set_key(self, key) :
        """
        Add a key to the PKS

        :param key: The key
        :return: bool of whether it was successful
        """
        pass

    @abstractmethod
    async def request_key(
        self, __tmp0,
    ) -> Tuple[__typ4, Optional[__typ1]]:
        """
        Request a key from the PKS

        :param request_node_id: The node id to look up
        :return: A tuple of success and a key string
        """
        pass


class __typ2(__typ3):
    def __init__(
        self,
        node_id, bootstrap_list: List[Tuple[__typ1, int]],
        listen_port,
    ) :
        """
        Sets up tracker key store

        :param node_id: node id and SHA256 hash
        :param bootstrap_list: list of ip,port to bootstrap connect to dht
        """
        self.node_id = node_id
        self.node_instance = get_dht()

    async def set_key(self, key) -> __typ4:
        """
        Sets the public key of the this node on the DHT

        :param key: 4096 RSA public key
        :return: boolean on success of setting key
        """
        try:
            await self.node_instance.set(self.node_id, key)
            return True
        except Exception:
            return False

    async def request_key(
        self,
        __tmp0: bytes,
    ) :
        """
        Asks DHT for the public key of a given node for sake of signature
        verification

        :param request_node_id: SHA256 hash
        :return: boolean (success of getting key), 2048 RSA public key \
                (if boolean is True)
        """

        result = __typ1(await self.node_instance.get(__tmp0), 'utf-8')
        if result is not None:
            return True, result
        else:
            return False, ""


class __typ0(__typ3):
    """Tracker based implementation of the public key store"""

    def __init__(self, node_id, ip, port) -> None:
        """
        Sets up a TrackerKeyStore with the trackers ip and port and the id of
        the given node

        :param node_id: SHA256 hash
        :param ip: string of ipv4 or ipv6
        :param port: port for the tracker connection
        """
        self.node_id = node_id
        self.tracker_ip = ip
        self.tracker_port = port

    async def set_key(self, key: <FILL>) :
        """
        Sets the public key of the this node on the tracker

        :param key: 4096 RSA public key
        :return: boolean on success of setting key
        """
        request = {
            'request_type': TRACKER_REQUEST_POST_KEY,
            'node_id': self.node_id,
            'data': key,
        }

        response = await send_request_to_tracker(
            request, self.tracker_ip,
            self.tracker_port,
        )
        logger.debug("tracker set key response: %s", response)
        if response.get('result') == TRACKER_OK_RESULT:
            return True
        else:
            return False

    async def request_key(
        self, __tmp0,
    ) :
        """
        Asks tracker for the public key of a given node for sake of signature
        verification

        :param request_node_id: SHA256 hash
        :return: boolean (success of getting key), 2048 RSA public key \
                (if boolean is True)
        """
        request = {
            'request_type': TRACKER_REQUEST_GET_KEY,
            'node_id': __tmp0,
        }

        response = await send_request_to_tracker(
            request, self.tracker_ip,
            self.tracker_port,
        )
        logger.debug("tracker get key response: %s", response)
        if response.get('result') == TRACKER_OK_RESULT:
            return True, response.get('data')
        else:
            return False, 'NO PUBLIC KEY AVAILABLE'
