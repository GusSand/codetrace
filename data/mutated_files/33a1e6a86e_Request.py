from typing import TypeAlias
__typ1 : TypeAlias = "str"
import logging
import mimetypes
import os
import socket
import typing
from queue import Empty, Queue
from threading import Thread
from typing import Callable, List, Tuple

from .request import Request
from .response import Response

LOGGER = logging.getLogger(__name__)

__typ0 = Callable[[Request], Response]


class HTTPWorker(Thread):
    def __init__(__tmp0, connection_queue: Queue, handlers: List[Tuple[__typ1, __typ0]]) :
        super().__init__(daemon=True)

        __tmp0.connection_queue = connection_queue
        __tmp0.handlers = handlers
        __tmp0.running = False

    def stop(__tmp0) :
        __tmp0.running = False

    def __tmp8(__tmp0) :
        __tmp0.running = True
        while __tmp0.running:
            try:
                __tmp4, __tmp6 = __tmp0.connection_queue.get(timeout=1)
            except Empty:
                continue

            try:
                __tmp0.handle_client(__tmp4, __tmp6)
            except Exception:
                LOGGER.exception("Unhandled error in handle_client.")
                continue
            finally:
                __tmp0.connection_queue.task_done()

    def handle_client(__tmp0, __tmp4, __tmp6) :
        with __tmp4:
            try:
                request = Request.from_socket(__tmp4)
            except Exception:
                LOGGER.warning("Failed to parse request.", exc_info=True)
                response = Response(status="400 Bad Request", content="Bad Request")
                response.send(__tmp4)
                return

            # Force clients to send their request bodies on every
            # request rather than making the handlers deal with this.
            if "100-continue" in request.headers.get("expect", ""):
                response = Response(status="100 Continue")
                response.send(__tmp4)

            for __tmp9, __tmp3 in __tmp0.handlers:
                if request.path.startswith(__tmp9):
                    try:
                        request = request._replace(path=request.path[len(__tmp9):])
                        response = __tmp3(request)
                        response.send(__tmp4)
                    except Exception as e:
                        LOGGER.exception("Unexpected error from handler %r.", __tmp3)
                        response = Response(status="500 Internal Server Error", content="Internal Error")
                        response.send(__tmp4)
                    finally:
                        break
            else:
                response = Response(status="404 Not Found", content="Not Found")
                response.send(__tmp4)


class HTTPServer:
    def __init__(__tmp0, host="127.0.0.1", port=9000, worker_count=16) -> None:
        __tmp0.handlers: List[Tuple[__typ1, __typ0]] = []
        __tmp0.host = host
        __tmp0.port = port
        __tmp0.worker_count = worker_count
        __tmp0.worker_backlog = worker_count * 8
        __tmp0.connection_queue: Queue = Queue(__tmp0.worker_backlog)

    def __tmp5(__tmp0, __tmp9, __tmp3) :
        """Mount a request handler at a particular path.  Handler
        prefixes are tested in the order that they are added so the
        first match "wins".
        """
        __tmp0.handlers.append((__tmp9, __tmp3))

    def __tmp2(__tmp0) :
        workers = []
        for _ in range(__tmp0.worker_count):
            worker = HTTPWorker(__tmp0.connection_queue, __tmp0.handlers)
            worker.start()
            workers.append(worker)

        with socket.socket() as server_sock:
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((__tmp0.host, __tmp0.port))
            server_sock.listen(__tmp0.worker_backlog)
            LOGGER.info("Listening on %s:%d...", __tmp0.host, __tmp0.port)

            while True:
                try:
                    __tmp0.connection_queue.put(server_sock.accept())
                except KeyboardInterrupt:
                    break

        for worker in workers:
            worker.stop()

        for worker in workers:
            worker.join(timeout=30)


def __tmp7(__tmp1: __typ1) -> __typ0:
    """Generate a request handler that serves file off of disk
    relative to server_root.
    """

    def __tmp3(request: <FILL>) :
        path = request.path
        if request.path == "/":
            path = "/index.html"

        abspath = os.path.normpath(os.path.join(__tmp1, path.lstrip("/")))
        if not abspath.startswith(__tmp1):
            return Response(status="404 Not Found", content="Not Found")

        try:
            content_type, encoding = mimetypes.guess_type(abspath)
            if content_type is None:
                content_type = "application/octet-stream"

            if encoding is not None:
                content_type += f"; charset={encoding}"

            body_file = open(abspath, "rb")
            response = Response(status="200 OK", body=body_file)
            response.headers.add("content-type", content_type)
            return response
        except FileNotFoundError:
            return Response(status="404 Not Found", content="Not Found")

    return __tmp3
