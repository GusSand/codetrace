from typing import TypeAlias
__typ0 : TypeAlias = "str"
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

HandlerT = Callable[[Request], Response]


class HTTPWorker(Thread):
    def __init__(__tmp1, connection_queue: <FILL>, handlers: List[Tuple[__typ0, HandlerT]]) -> None:
        super().__init__(daemon=True)

        __tmp1.connection_queue = connection_queue
        __tmp1.handlers = handlers
        __tmp1.running = False

    def stop(__tmp1) -> None:
        __tmp1.running = False

    def __tmp5(__tmp1) -> None:
        __tmp1.running = True
        while __tmp1.running:
            try:
                __tmp3, client_addr = __tmp1.connection_queue.get(timeout=1)
            except Empty:
                continue

            try:
                __tmp1.handle_client(__tmp3, client_addr)
            except Exception:
                LOGGER.exception("Unhandled error in handle_client.")
                continue
            finally:
                __tmp1.connection_queue.task_done()

    def handle_client(__tmp1, __tmp3, client_addr) :
        with __tmp3:
            try:
                request = Request.from_socket(__tmp3)
            except Exception:
                LOGGER.warning("Failed to parse request.", exc_info=True)
                response = Response(status="400 Bad Request", content="Bad Request")
                response.send(__tmp3)
                return

            # Force clients to send their request bodies on every
            # request rather than making the handlers deal with this.
            if "100-continue" in request.headers.get("expect", ""):
                response = Response(status="100 Continue")
                response.send(__tmp3)

            for path_prefix, __tmp2 in __tmp1.handlers:
                if request.path.startswith(path_prefix):
                    try:
                        request = request._replace(path=request.path[len(path_prefix):])
                        response = __tmp2(request)
                        response.send(__tmp3)
                    except Exception as e:
                        LOGGER.exception("Unexpected error from handler %r.", __tmp2)
                        response = Response(status="500 Internal Server Error", content="Internal Error")
                        response.send(__tmp3)
                    finally:
                        break
            else:
                response = Response(status="404 Not Found", content="Not Found")
                response.send(__tmp3)


class HTTPServer:
    def __init__(__tmp1, host="127.0.0.1", port=9000, worker_count=16) :
        __tmp1.handlers: List[Tuple[__typ0, HandlerT]] = []
        __tmp1.host = host
        __tmp1.port = port
        __tmp1.worker_count = worker_count
        __tmp1.worker_backlog = worker_count * 8
        __tmp1.connection_queue: Queue = Queue(__tmp1.worker_backlog)

    def __tmp4(__tmp1, path_prefix, __tmp2) -> None:
        """Mount a request handler at a particular path.  Handler
        prefixes are tested in the order that they are added so the
        first match "wins".
        """
        __tmp1.handlers.append((path_prefix, __tmp2))

    def serve_forever(__tmp1) :
        workers = []
        for _ in range(__tmp1.worker_count):
            worker = HTTPWorker(__tmp1.connection_queue, __tmp1.handlers)
            worker.start()
            workers.append(worker)

        with socket.socket() as server_sock:
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((__tmp1.host, __tmp1.port))
            server_sock.listen(__tmp1.worker_backlog)
            LOGGER.info("Listening on %s:%d...", __tmp1.host, __tmp1.port)

            while True:
                try:
                    __tmp1.connection_queue.put(server_sock.accept())
                except KeyboardInterrupt:
                    break

        for worker in workers:
            worker.stop()

        for worker in workers:
            worker.join(timeout=30)


def serve_static(__tmp0) :
    """Generate a request handler that serves file off of disk
    relative to server_root.
    """

    def __tmp2(request) -> Response:
        path = request.path
        if request.path == "/":
            path = "/index.html"

        abspath = os.path.normpath(os.path.join(__tmp0, path.lstrip("/")))
        if not abspath.startswith(__tmp0):
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

    return __tmp2
