from typing import TypeAlias
__typ0 : TypeAlias = "Executor"
__typ1 : TypeAlias = "int"
import asyncio
from concurrent.futures import Executor, ProcessPoolExecutor
from functools import partial
import logging
from multiprocessing import freeze_support
from typing import Set, Tuple

from aiohttp import web
import aiohttp_cors
import black
import click

# This is used internally by tests to shut down the server prematurely
_stop_signal = asyncio.Event()

VERSION_HEADER = "X-Protocol-Version"
LINE_LENGTH_HEADER = "X-Line-Length"
PYTHON_VARIANT_HEADER = "X-Python-Variant"
SKIP_STRING_NORMALIZATION_HEADER = "X-Skip-String-Normalization"
FAST_OR_SAFE_HEADER = "X-Fast-Or-Safe"

BLACK_HEADERS = [
    VERSION_HEADER,
    LINE_LENGTH_HEADER,
    PYTHON_VARIANT_HEADER,
    SKIP_STRING_NORMALIZATION_HEADER,
    FAST_OR_SAFE_HEADER,
]


class __typ2(Exception):
    pass


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--bind-host", type=str, help="Address to bind the server to.", default="localhost"
)
@click.option("--bind-port", type=__typ1, help="Port to listen on", default=45484)
@click.version_option(version=black.__version__)
def __tmp0(__tmp1: str, __tmp6: __typ1) -> None:
    logging.basicConfig(level=logging.INFO)
    app = __tmp5()
    ver = black.__version__
    black.out(f"blackd version {ver} listening on {__tmp1} port {__tmp6}")
    web.run_app(app, host=__tmp1, port=__tmp6, handle_signals=True, print=None)


def __tmp5() :
    app = web.Application()
    __tmp4 = ProcessPoolExecutor()

    cors = aiohttp_cors.setup(app)
    resource = cors.add(app.router.add_resource("/"))
    cors.add(
        resource.add_route("POST", partial(__tmp2, __tmp4=__tmp4)),
        {
            "*": aiohttp_cors.ResourceOptions(
                allow_headers=(*BLACK_HEADERS, "Content-Type"), expose_headers="*"
            )
        },
    )

    return app


async def __tmp2(__tmp8: web.Request, __tmp4) :
    try:
        if __tmp8.headers.get(VERSION_HEADER, "1") != "1":
            return web.Response(
                status=501, text="This server only supports protocol version 1"
            )
        try:
            line_length = __typ1(
                __tmp8.headers.get(LINE_LENGTH_HEADER, black.DEFAULT_LINE_LENGTH)
            )
        except ValueError:
            return web.Response(status=400, text="Invalid line length header value")

        if PYTHON_VARIANT_HEADER in __tmp8.headers:
            __tmp3 = __tmp8.headers[PYTHON_VARIANT_HEADER]
            try:
                pyi, versions = __tmp7(__tmp3)
            except __typ2 as e:
                return web.Response(
                    status=400,
                    text=f"Invalid value for {PYTHON_VARIANT_HEADER}: {e.args[0]}",
                )
        else:
            pyi = False
            versions = set()

        skip_string_normalization = bool(
            __tmp8.headers.get(SKIP_STRING_NORMALIZATION_HEADER, False)
        )
        fast = False
        if __tmp8.headers.get(FAST_OR_SAFE_HEADER, "safe") == "fast":
            fast = True
        mode = black.FileMode(
            target_versions=versions,
            is_pyi=pyi,
            line_length=line_length,
            string_normalization=not skip_string_normalization,
        )
        req_bytes = await __tmp8.content.read()
        charset = __tmp8.charset if __tmp8.charset is not None else "utf8"
        req_str = req_bytes.decode(charset)
        loop = asyncio.get_event_loop()
        formatted_str = await loop.run_in_executor(
            __tmp4, partial(black.format_file_contents, req_str, fast=fast, mode=mode)
        )
        return web.Response(
            content_type=__tmp8.content_type, charset=charset, text=formatted_str
        )
    except black.NothingChanged:
        return web.Response(status=204)
    except black.InvalidInput as e:
        return web.Response(status=400, text=str(e))
    except Exception as e:
        logging.exception("Exception during handling a request")
        return web.Response(status=500, text=str(e))


def __tmp7(__tmp3: <FILL>) -> Tuple[bool, Set[black.TargetVersion]]:
    if __tmp3 == "pyi":
        return True, set()
    else:
        versions = set()
        for version in __tmp3.split(","):
            if version.startswith("py"):
                version = version[len("py") :]
            major_str, *rest = version.split(".")
            try:
                major = __typ1(major_str)
                if major not in (2, 3):
                    raise __typ2("major version must be 2 or 3")
                if len(rest) > 0:
                    minor = __typ1(rest[0])
                    if major == 2 and minor != 7:
                        raise __typ2(
                            "minor version must be 7 for Python 2"
                        )
                else:
                    # Default to lowest supported minor version.
                    minor = 7 if major == 2 else 3
                version_str = f"PY{major}{minor}"
                if major == 3 and not hasattr(black.TargetVersion, version_str):
                    raise __typ2(f"3.{minor} is not supported")
                versions.add(black.TargetVersion[version_str])
            except (KeyError, ValueError):
                raise __typ2("expected e.g. '3.7', 'py3.5'")
        return False, versions


def __tmp9() -> None:
    freeze_support()
    black.patch_click()
    __tmp0()


if __name__ == "__main__":
    __tmp9()
