import asyncio
import time
from typing import Any
from typing import Dict  # NOQA
from typing import List
from typing import Tuple

from kademlia.network import Server  # type: ignore
from kademlia.storage import ForgetfulStorage  # type: ignore

from syncr_backend.constants import TRACKER_DROP_AVAILABILITY_TTL
from syncr_backend.util import crypto_util
from syncr_backend.util.log_util import get_logger


logger = get_logger(__name__)

_node_instance = None


def __tmp1() :
    """
    returns the node_instance of the dht

    :raises TypeError: when the DHT has not been initialized
    :return: The DHT Server
    """
    global _node_instance
    if _node_instance is None:
        raise TypeError("DHT has not been initilized")
    return _node_instance


def __tmp3(
    bootstrap_ip_port_pair_list,
    __tmp5: int,
) -> None:
    """
    connects to the distributed hash table
    if no bootstrap ip port pair list is given, it starts a new dht

    :param bootstrap_ip_port_pair_list: list of ip port tuples to connect to \
            the dht
    :param listen_port: port to listen on
    :return: instance of server
    """
    global _node_instance

    get_logger("kademlia")

    logger.debug("set up DHT: %s", str(bootstrap_ip_port_pair_list))

    node = Server(storage=DropPeerDHTStorage())
    node.listen(__tmp5)
    loop = asyncio.get_event_loop()
    if len(bootstrap_ip_port_pair_list) > 0:
        loop.run_until_complete(node.bootstrap(bootstrap_ip_port_pair_list))

    _node_instance = node


class DropPeerDHTStorage(ForgetfulStorage):
    """
    Extension of the default kademlia storage module

    It is different in that when given a list of bytes, it checks to see if
    it is an encoded set. If it is, it unions it with the rest of the
    sets
    """

    def __init__(__tmp0) -> None:
        __tmp0.timeouts = {}  # type: Dict[Tuple[int, Tuple[Any, int, str]], int]

        super().__init__()

    def cull_peerlist(__tmp0, __tmp4) -> None:
        """
        Cull peerlist at key of out of date entries
        If entry at key is not a peerlist, do nothing

        :param key: key of peerlist
        """
        current_time = int(time.time())
        item = __tmp0.data[__tmp4][1]
        itempeerlist = crypto_util.decode_peerlist(item)
        if itempeerlist is not None:
            itempeerlist = list(
                filter(
                    lambda x: (
                        ((__tmp4, x) not in __tmp0.timeouts) or
                        (
                            current_time - __tmp0.timeouts[(__tmp4, x)] <
                            TRACKER_DROP_AVAILABILITY_TTL
                        )
                    ),
                    itempeerlist,
                ),
            )
            timeout_key_list = list(
                filter(
                    lambda x: __tmp0.timeouts[x] < TRACKER_DROP_AVAILABILITY_TTL,
                    __tmp0.timeouts,
                ),
            )
            timeout_value_list = list(
                map(lambda x: __tmp0.timeouts[x], timeout_key_list),
            )
            __tmp0.timeouts = dict(zip(timeout_key_list, timeout_value_list))

    def __getitem__(__tmp0, __tmp4: Any) -> Any:
        """
        Gets item from storage

        If item is an encoded peerlist, it culls outdated values

        :param key: key to access value in dht
        """
        __tmp0.cull_peerlist(__tmp4)
        return super().__getitem__(__tmp4)

    def __setitem__(__tmp0, __tmp4: <FILL>, __tmp2: Any) :
        """
        :param key: key to look up in dht
        :param value: value to put in dht under key
        """
        valuepeer = crypto_util.decode_peerlist(__tmp2)
        if valuepeer is not None:
            __tmp0.timeouts[(__tmp4, valuepeer[0])] = int(time.time())
            if __tmp4 in __tmp0.data:
                peerlist = crypto_util.decode_peerlist(
                    __tmp0.data[__tmp4][1],
                )
                if peerlist is not None:
                    # remove duplicates and encode
                    new_peerlist = crypto_util.encode_peerlist(
                        list(set(peerlist + valuepeer)),
                    )
                    return super().__setitem__(__tmp4, new_peerlist)

            return super().__setitem__(
                __tmp4,
                crypto_util.encode_peerlist(valuepeer),
            )

        return super().__setitem__(__tmp4, __tmp2)
