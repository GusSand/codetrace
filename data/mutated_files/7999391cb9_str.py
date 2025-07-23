import logging
import pkg_resources
from typing import List, Dict, Union

from derex import runner  # type: ignore

logger = logging.getLogger(__name__)


def __tmp0(__tmp1: <FILL>) -> str:
    return pkg_resources.resource_filename(__name__, f"compose/files/path/{__tmp1}")


class DemoServices:
    @staticmethod
    @runner.hookimpl
    def compose_options() :
        options = ["-f", __tmp0("demo.yml")]
        return {
            "options": options,
            "name": "demo",
            "priority": ">base",
            "variant": "openedx",
        }
