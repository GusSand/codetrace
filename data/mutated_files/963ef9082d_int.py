from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


class InvalidVariantHeader(Exception):
    pass


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--bind-host", type=__typ0, help="Address to bind the server to.", default="localhost"
)
@click.option("--bind-port", type=int, help="Port to listen on", default=45484)
@click.version_option(version=black.__version__)
def main(__tmp0, __tmp5: <FILL>) -> None:
    logging.basicConfig(level=logging.INFO)
    app = __tmp2()
    ver = black.__version__
    black.out(f"blackd version {ver} listening on {__tmp0} port {__tmp5}")
    web.run_app(app, host=__tmp0, port=__tmp5, handle_signals=True, print=None)


def __tmp2() :
    app = web.Application()
    __tmp3 = ProcessPoolExecutor()

    cors = aiohttp_cors.setup(app)
    resource = cors.add(app.router.add_resource("/"))
    cors.add(
        resource.add_route("POST", partial(__tmp1, __tmp3=__tmp3)),
        {
            "*": aiohttp_cors.ResourceOptions(
                allow_headers=(*BLACK_HEADERS, "Content-Type"), expose_headers="*"
            )
        },
    )

    return app


async def __tmp1(__tmp6, __tmp3) :
    try:
        if __tmp6.headers.get(VERSION_HEADER, "1") != "1":
            return web.Response(
                status=501, text="This server only supports protocol version 1"
            )
        try:
            line_length = int(
                __tmp6.headers.get(LINE_LENGTH_HEADER, black.DEFAULT_LINE_LENGTH)
            )
        except ValueError:
            return web.Response(status=400, text="Invalid line length header value")

        if PYTHON_VARIANT_HEADER in __tmp6.headers:
            __tmp4 = __tmp6.headers[PYTHON_VARIANT_HEADER]
            try:
                pyi, versions = parse_python_variant_header(__tmp4)
            except InvalidVariantHeader as e:
                return web.Response(
                    status=400,
                    text=f"Invalid value for {PYTHON_VARIANT_HEADER}: {e.args[0]}",
                )
        else:
            pyi = False
            versions = set()

        skip_string_normalization = bool(
            __tmp6.headers.get(SKIP_STRING_NORMALIZATION_HEADER, False)
        )
        fast = False
        if __tmp6.headers.get(FAST_OR_SAFE_HEADER, "safe") == "fast":
            fast = True
        mode = black.FileMode(
            target_versions=versions,
            is_pyi=pyi,
            line_length=line_length,
            string_normalization=not skip_string_normalization,
        )
        req_bytes = await __tmp6.content.read()
        charset = __tmp6.charset if __tmp6.charset is not None else "utf8"
        req_str = req_bytes.decode(charset)
        loop = asyncio.get_event_loop()
        formatted_str = await loop.run_in_executor(
            __tmp3, partial(black.format_file_contents, req_str, fast=fast, mode=mode)
        )
        return web.Response(
            content_type=__tmp6.content_type, charset=charset, text=formatted_str
        )
    except black.NothingChanged:
        return web.Response(status=204)
    except black.InvalidInput as e:
        return web.Response(status=400, text=__typ0(e))
    except Exception as e:
        logging.exception("Exception during handling a request")
        return web.Response(status=500, text=__typ0(e))


def parse_python_variant_header(__tmp4) -> Tuple[bool, Set[black.TargetVersion]]:
    if __tmp4 == "pyi":
        return True, set()
    else:
        versions = set()
        for version in __tmp4.split(","):
            if version.startswith("py"):
                version = version[len("py") :]
            major_str, *rest = version.split(".")
            try:
                major = int(major_str)
                if major not in (2, 3):
                    raise InvalidVariantHeader("major version must be 2 or 3")
                if len(rest) > 0:
                    minor = int(rest[0])
                    if major == 2 and minor != 7:
                        raise InvalidVariantHeader(
                            "minor version must be 7 for Python 2"
                        )
                else:
                    # Default to lowest supported minor version.
                    minor = 7 if major == 2 else 3
                version_str = f"PY{major}{minor}"
                if major == 3 and not hasattr(black.TargetVersion, version_str):
                    raise InvalidVariantHeader(f"3.{minor} is not supported")
                versions.add(black.TargetVersion[version_str])
            except (KeyError, ValueError):
                raise InvalidVariantHeader("expected e.g. '3.7', 'py3.5'")
        return False, versions


def __tmp7() -> None:
    freeze_support()
    black.patch_click()
    main()


if __name__ == "__main__":
    __tmp7()
