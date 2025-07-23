import os
import sys
import json
import select

import requests
import argparse

from urllib.parse import urlparse
from dataclasses import dataclass, field
from python_pipes import read_stdin_lines

# Disable SSL Warnings
requests.packages.urllib3.disable_warnings()


class UnknownException(Exception):
    pass


class InvalidJsonFormat(Exception):
    pass


class InvalidProxyFormat(Exception):
    pass


@dataclass
class Request:

    url: str
    body: str = None
    method: str = "GET"
    version: str = "1.1"
    headers: dict = field(default_factory=dict)

    @classmethod
    def from_json(__tmp5, __tmp10: str) :
        # Load json data
        try:
            loaded_json = json.loads(__tmp10)
        except json.decoder.JSONDecodeError:
            raise InvalidJsonFormat("Input value doesn't has valid JSON")

        return __tmp5(**loaded_json["request"])

    def __tmp4(__tmp2):
        __tmp2.method = __tmp2.method.lower()

        # Filter headers
        __tmp2.headers = {
            x: y for x, y in __tmp2.headers.items() if x[0].isalpha()
        }


def __tmp9(__tmp7: <FILL>) :
    """Check proxy format and return the tuple:

    (SCHEME: PROXY_URL)
    """
    proxy_schemes = ("http", "https", "socks")

    scheme, netloc, path, *_ = urlparse(__tmp7)

    if not scheme:
        raise InvalidProxyFormat(
            f"Proxy must include one of these schemes: "
            f"{','.join(proxy_schemes)}"
        )

    if not any(scheme.startswith(x) for x in proxy_schemes):
        raise InvalidProxyFormat(
            f"Proxy must starts with one of them: {','.join(proxy_schemes)}"
        )

    # check for proxy port
    try:
        host, port = netloc.split(":")
    except ValueError:
        raise InvalidProxyFormat("Proxy must include host and port "
                                 "(HOST:PORT)")

    return scheme, __tmp7


def __tmp3(__tmp6, __tmp0) -> str:
    #
    # Load json request
    #
    req = Request.from_json(__tmp6)

    # Prepare input proxy
    proxy_scheme, proxy_url = __tmp9(__tmp0.PROXY)
    proxies = {
        "https": proxy_url,
        "http": proxy_url
    }

    #
    # Get request method
    #
    try:
        method = getattr(requests, req.method)
    except AttributeError:
        raise InvalidProxyFormat("Not allowed method")

    # Perform query
    if req.method == "get":
        params = dict(
            url=req.url,
            headers=req.headers,
            proxies=proxies
        )
    else:
        params = dict(
            url=req.url,
            headers=req.headers,
            data=req.body,
            proxies=proxies
        )

    # Remove SSL Verification
    params["verify"] = False

    response = method(**params)

    return req.url, response


def __tmp8(__tmp0):
    quiet = __tmp0.quiet or False
    debug = __tmp0.debug or False

    # -------------------------------------------------------------------------
    # Read info by stdin or parameter
    # -------------------------------------------------------------------------
    for has_stdin_pipe, has_stdout_pipe, json_line in read_stdin_lines():
        if not has_stdin_pipe:
            raise FileNotFoundError(
                "Input data must be entered as a UNIX pipeline. For example: "
                "'cat info.json | tool-name'")

        try:
            request_url, response = __tmp3(json_line, __tmp0)
        except (InvalidJsonFormat, InvalidProxyFormat) as e:
            if debug:
                print(f"   > Error while processing input data: {e}")
            continue

        # You're being piped or redirected
        if has_stdout_pipe:

            # Info for next piped command
            sys.stdout.write(f"{json_line}\n")
            sys.stdout.flush()

        if not quiet:

            if has_stdout_pipe:
                console_print = sys.stderr.write
                console_flush = sys.stderr.flush
            else:
                console_print = sys.stdout.write
                console_flush = sys.stdout.flush

            console_print(f"[*] Request sent: '{request_url}'\n\r")
            console_flush()


def __tmp1():
    parser = argparse.ArgumentParser(
        description='Read requests from stdin and send them to a remote proxy'
    )
    parser.add_argument("PROXY", help="proxy in format: SCHEME://HOST:PORT")
    parser.add_argument("-q", "--quiet",
                        help="don't display any information in stdout",
                        action="store_true",
                        default=False)
    parser.add_argument("--debug",
                        help="enable debug mode",
                        action="store_true",
                        default=False)
    parsed_cli = parser.parse_args()

    try:
        __tmp8(parsed_cli)
    except Exception as e:
        print(f"[!!] {e}", file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    __tmp1()
