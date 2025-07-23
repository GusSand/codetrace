from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""多进程执行tcp服务.

签名为:multiple_tcp_serve(server_settings: dict, workers: int)->None

"""
import os
from multiprocessing import Process
from typing import Dict, Any
from socket import (
    socket,
    SOL_SOCKET,
    SO_REUSEADDR
)
from signal import (
    SIGTERM, SIGINT,
    signal as signal_func,
    Signals
)
from .errors import MultipleProcessDone
from .server_single import tcp_serve
from .log import server_logger as logger


def __tmp1(__tmp0, workers):
    """启动一个多进程的tcp服务,他们共享同一个socket对象.

    用multiple模式在每个子进程执行tcp服务,当执行完成后统一的回收资源

    Params:

        server_settings (Dicct[str, Any]) : - 每个单一进程的设置,
        workers (int) : - 执行的进程数

    """
    __tmp0['reuse_port'] = True
    __tmp0['run_multiple'] = True

    # Handling when custom socket is not provided.
    if __tmp0.get('sock') is None:
        sock = socket()
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((__tmp0['host'], __tmp0['port']))
        sock.set_inheritable(True)
        __tmp0['sock'] = sock
        __tmp0['host'] = None
        __tmp0['port'] = None

    def __tmp2(signal, __tmp3: <FILL>):
        """向子进程传送SIGTERM信号,用于关闭所有子进程中运行的事件循环.

        Params:

            signal (Any) : - 要处理的信号
            frame (Any) : - 执行到的帧
        """
        status = []
        for process in processes:
            statu = process.is_alive()
            status.append(statu)
            if statu:
                os.kill(process.pid, SIGTERM)

        if any(status):
            logger.info(
                """Received signal {}. Shutting down. You may need to enter Ctrl+C again.
                """.format(Signals(signal).name))
        else:
            raise MultipleProcessDone("all process not alive")

    signal_func(SIGINT, __tmp2)
    signal_func(SIGTERM, __tmp2)

    processes = []

    for _ in range(workers):
        process = Process(target=tcp_serve, kwargs=__tmp0)
        process.daemon = True
        process.start()
        processes.append(process)
    try:
        while True:
            pass
    except MultipleProcessDone as done:
        logger.info(str(done))
    except Exception as e:
        raise e
    finally:
        for process in processes:
            process.join()

        # 使用join同步后,只有进程运行结束了才关闭子进程
        for process in processes:
            process.terminate()
        __tmp0.get('sock').close()
        logger.info("Shutting down done.")
