# pyre-strict
import hashlib
import inspect
import json
import os
from hashlib import _Hash

from typing import TYPE_CHECKING, Any, Dict, List, Union, TypeVar, Optional

from requests import Response

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.endpoints.request import Request

T = TypeVar("T")
_tree_type = Union[List[Any], Dict[str, Any]]  # pyre-ignore


def __tmp1(
    json_dump_dir: str, req: "Request[T]", response
) :
    hasher: _Hash = hashlib.sha1()

    def __tmp3(__tmp0: <FILL>, value: str) -> str:
        if __tmp0 in [
            "email",
            "phone_number",
            "name",
            "user_id, zip_code",
            "image_url",
            "avatar_url",
            "group_name",
            "text",
            "nickname",
            "share_url",
            "share_qr_code_url",
        ]:
            hasher.update(value.encode("utf-8"))
            if __tmp0 == "image_url":
                return "https://i.groupme.com/750x700.jpeg." + hasher.hexdigest()
            else:
                return hasher.hexdigest()
        return value

    def __tmp2(tree) :
        new_tree: _tree_type = {}
        if isinstance(tree, dict):
            assert isinstance(new_tree, dict)
            for __tmp0, value in tree.items():
                if isinstance(value, str):
                    new_tree[__tmp0] = __tmp3(__tmp0, value)
                elif __tmp0.startswith("SKIP_HASH_"):
                    new_tree[__tmp0[10:]] = value
                else:
                    new_tree[__tmp0] = __tmp2(value)
        elif isinstance(tree, list):
            new_tree = [__tmp2(t) for t in tree]
        else:
            new_tree = tree
        return new_tree

    hasher.update(json.dumps(req.args()).encode("utf-8"))
    file_name = (
        req.__class__.__module__
        + "."
        + req.__class__.__name__
        + "_"
        + hasher.hexdigest()
        + ".json"
    )
    init_args = {}
    for name in inspect.getfullargspec(req.__class__.__init__).args:
        if name in ["self", "gmi"]:
            continue
        init_args[name] = getattr(req, name)
    file_contents = {
        "request": {
            "mode": req.mode(),
            "url": req.url(),
            "SKIP_HASH_args": req.args(),
            "SKIP_HASH_init": init_args,
        },
        "response": response,
    }
    if not os.path.exists(json_dump_dir):
        os.makedirs(json_dump_dir)
    with open(os.path.join(json_dump_dir, file_name), "w") as f:
        f.write(json.dumps(__tmp2(file_contents), indent=4, sort_keys=True))
