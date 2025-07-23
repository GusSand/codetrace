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
__typ0 = Union[List[Any], Dict[str, Any]]  # pyre-ignore


def __tmp7(
    __tmp1, req: "Request[T]", __tmp4: Optional[Response]
) -> None:
    hasher: _Hash = hashlib.sha1()

    def __tmp0(__tmp6: str, __tmp2: <FILL>) -> str:
        if __tmp6 in [
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
            hasher.update(__tmp2.encode("utf-8"))
            if __tmp6 == "image_url":
                return "https://i.groupme.com/750x700.jpeg." + hasher.hexdigest()
            else:
                return hasher.hexdigest()
        return __tmp2

    def __tmp3(__tmp5: __typ0) -> __typ0:
        new_tree: __typ0 = {}
        if isinstance(__tmp5, dict):
            assert isinstance(new_tree, dict)
            for __tmp6, __tmp2 in __tmp5.items():
                if isinstance(__tmp2, str):
                    new_tree[__tmp6] = __tmp0(__tmp6, __tmp2)
                elif __tmp6.startswith("SKIP_HASH_"):
                    new_tree[__tmp6[10:]] = __tmp2
                else:
                    new_tree[__tmp6] = __tmp3(__tmp2)
        elif isinstance(__tmp5, list):
            new_tree = [__tmp3(t) for t in __tmp5]
        else:
            new_tree = __tmp5
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
        "response": __tmp4,
    }
    if not os.path.exists(__tmp1):
        os.makedirs(__tmp1)
    with open(os.path.join(__tmp1, file_name), "w") as f:
        f.write(json.dumps(__tmp3(file_contents), indent=4, sort_keys=True))
