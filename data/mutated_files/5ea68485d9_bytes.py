from typing import TypeAlias
__typ0 : TypeAlias = "str"
#!/usr/bin/env python
import argparse
import asyncio
import threading
from typing import List

from syncr_backend.external_interface.dht_util import initialize_dht
from syncr_backend.external_interface.drop_peer_store import send_drops_to_dps
from syncr_backend.init import drop_init
from syncr_backend.init import node_init
from syncr_backend.metadata.drop_metadata import send_my_pub_key
from syncr_backend.network.handle_frontend import setup_frontend_server
from syncr_backend.network.listen_requests import start_listen_server
from syncr_backend.util import crypto_util
from syncr_backend.util import drop_util
from syncr_backend.util.fileio_util import load_config_file
from syncr_backend.util.log_util import get_logger
# from syncr_backend.network import send_requests
logger = get_logger(__name__)


def parser() :
    input_args_parser = argparse.ArgumentParser(
        description="Run the backend, listening for incomming requests and "
        "periodically making necessary outgoing requests",
    )
    input_args_parser.add_argument(
        "ip",
        type=__typ0,
        nargs=1,
        help='ip to bind listening server',
    )
    input_args_parser.add_argument(
        "port",
        type=__typ0,
        nargs=1,
        help='port to bind listening server',
    )
    input_args_parser.add_argument(
        "--backendonly",
        action="store_true",
        help='runs only the backend if added as an option',
    )
    input_args_parser.add_argument(
        "--external_address",
        type=__typ0,
        help="Set this if the external address is different from the listen "
        "address",
    )
    input_args_parser.add_argument(
        "--external_port",
        type=int,
        help="Set this if the external port is different from the listen port",
    )
    input_args_parser.add_argument(
        "--debug_commands",
        type=__typ0,
        help="Command file to send debug commands",
    )
    return input_args_parser


def __tmp0() :
    """
    Runs the backend
    """
    arguments = parser().parse_args()
    if arguments.external_address is not None:
        ext_addr = arguments.external_address
    else:
        ext_addr = arguments.ip[0]
    if arguments.external_port is not None:
        ext_port = arguments.external_port
    else:
        ext_port = int(arguments.port[0])

    __tmp5 = asyncio.get_event_loop()

    # initilize dht
    config_file = __tmp5.run_until_complete(load_config_file())
    if config_file['type'] == 'dht':
        ip_port_list = list(
            zip(
                config_file['bootstrap_ips'],
                config_file['bootstrap_ports'],
            ),
        )
        initialize_dht(ip_port_list, config_file['listen_port'])

    __tmp5.create_task(send_my_pub_key())

    shutdown_flag = threading.Event()
    listen_server = __tmp5.run_until_complete(
        start_listen_server(arguments.ip[0], arguments.port[0]),
    )
    frontend_server = __tmp5.run_until_complete(
        setup_frontend_server(),
    )
    dps_send = __tmp5.create_task(
        send_drops_to_dps(ext_addr, ext_port, shutdown_flag),
    )
    sync_processor = __tmp5.create_task(
        drop_util.process_sync_queue(),
    )

    if not arguments.backendonly:
        if arguments.debug_commands is None:
            print("Not implemented")
        else:
            t = threading.Thread(
                target=__tmp6,
                __tmp2=[arguments.debug_commands, __tmp5],
            )
            t.start()
    try:
        __tmp5.run_forever()
    finally:
        shutdown_flag.set()
        listen_server.close()
        frontend_server.close()
        dps_send.cancel()
        sync_processor.cancel()
        __tmp5.run_until_complete(__tmp5.shutdown_asyncgens())
        __tmp5.stop()
        __tmp5.close()


def __tmp6(
    commands_file, __tmp5,
) :
    """
    Read and execute commands a list of semicolon separated commands as input

    :param commands: list of semicolon separated commands
    """
    with open(commands_file) as f:
        commands = f.read().replace('\n', '')

    commandlist = commands.split(';')
    for command in commandlist:

        __tmp2 = command.split(' ')
        logger.info("Ran Command %s", __tmp2)
        execute_function(__tmp2[0], __tmp2[1:], __tmp5)

    __tmp5.stop()


def execute_function(
    __tmp4, __tmp2: List[__typ0], __tmp5: asyncio.AbstractEventLoop,
) :
    """
    Runs a function with the given args

    :param function_name: string name of the function to run
    :param args: arguments for the function to run
    """
    # TODO: add real drop/metadata request commands that interface
    #  with the filesystem
    # TODO: handle exceptions for real
    # for functions that create or destroy the init directory
    if __tmp4 == "node_init":
        node_init.initialize_node(*__tmp2)
    elif __tmp4 == "node_force_init":
        node_init.force_initialize_node(*__tmp2)
    elif __tmp4 == "delete_node":
        node_init.delete_node_directory(*__tmp2)

    # drop functions
    elif __tmp4 == "drop_init":
        drop_init.initialize_drop(__tmp2[0])

    elif __tmp4 == "make_new_version":
        __tmp3 = crypto_util.b64decode(__tmp2[0].encode())
        task = asyncio.run_coroutine_threadsafe(
            drop_util.make_new_version(__tmp3),
            __tmp5,
        )
        task.result()
        # loop.call_soon_threadsafe(task)
        # while not task.done():
        #     time.sleep(10)

    elif __tmp4 == "sync_drop":
        __tmp3 = crypto_util.b64decode(__tmp2[0].encode())
        # takes drop_id as b64 and save+directory

        async def sync_wrapper(__tmp3: <FILL>, __tmp1) :

            await drop_util.sync_drop(__tmp3, __tmp1)

        task = asyncio.run_coroutine_threadsafe(
            sync_wrapper(__tmp3, __tmp2[1]),
            __tmp5,
        )
        task.result()

    else:
        print("Function [%s] not found" % (__tmp4))


if __name__ == '__main__':
    __tmp0()
