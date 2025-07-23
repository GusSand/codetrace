from typing import TypeAlias
__typ0 : TypeAlias = "T"
# pyre-strict
import json
from typing import TypeVar, Generic, TYPE_CHECKING, Optional, Dict, Any, Union

import requests
from requests import Response

from lowerpines.exceptions import (
    InvalidOperationException,
    GroupMeApiException,
    TimeoutException,
    UnauthorizedException,
)

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI

__typ0 = TypeVar("T")

# TODO Model JSON better
__typ1 = Dict[str, Any]


class Request(Generic[__typ0]):
    def __tmp1(__tmp0, gmi: "GMI") -> None:
        __tmp0.gmi = gmi
        nullable_result = __tmp0.execute()
        if nullable_result is not None:
            __tmp0.result: __typ0 = __tmp0.parse(nullable_result)
        else:
            json_dump_dir = __tmp0.gmi.write_json_to
            if json_dump_dir is not None:
                from test.dump_json import dump_json

                dump_json(json_dump_dir, __tmp0, nullable_result)

    base_url = "https://api.groupme.com/v3"

    def url(__tmp0) :
        raise NotImplementedError  # pragma: no cover

    def mode(__tmp0) -> str:
        raise NotImplementedError  # pragma: no cover

    def parse(__tmp0, response: __typ1) -> __typ0:
        raise NotImplementedError  # pragma: no cover

    def args(__tmp0) -> Union[__typ1, bytes]:
        return {}

    def execute(__tmp0) -> Optional[__typ1]:
        params = {}
        headers = {
            "X-Access-Token": __tmp0.gmi.access_token,
            "User-Agent": "GroupYouLibrary/1.0",
        }
        args = __tmp0.args()
        if __tmp0.mode() == "GET" and isinstance(args, dict):
            params.update(args)
            r = requests.get(url=__tmp0.url(), params=params, headers=headers)
        elif __tmp0.mode() == "POST" and isinstance(args, dict):
            headers["Content-Type"] = "application/json"
            r = requests.post(
                url=__tmp0.url(),
                params=params,
                headers=headers,
                data=json.dumps(__tmp0.args()),
            )
        elif __tmp0.mode() == "POST_RAW" and isinstance(args, bytes):
            r = requests.post(
                url=__tmp0.url(), params=params, headers=headers, data=__tmp0.args()
            )
        else:
            raise InvalidOperationException()
        __tmp0.error_check(r)
        string_content = r.content.decode("utf-8")
        if not string_content or string_content.isspace():
            return None
        else:
            return __tmp0.extract_response(r)

    def error_check(__tmp0, request: <FILL>) -> None:
        code = int(request.status_code)
        if 399 < code < 500:
            request_string = (
                str(__tmp0.mode())
                + " "
                + str(__tmp0.url())
                + " with data:\n"
                + str(__tmp0.args())
            )
            try:
                errors = request.json()["meta"]["errors"]
                if "request timeout" in errors:
                    raise TimeoutException("Timeout for " + request_string)
                elif "unauthorized" in errors:
                    raise UnauthorizedException(
                        "Not authorized to perform " + request_string
                    )
                text = "(JSON): " + str(errors)
            except ValueError:
                text = "(TEXT): " + str(request.text)
            raise GroupMeApiException(
                "Unknown error " + text + " for " + request_string
            )

    def extract_response(__tmp0, response: Response) -> __typ1:
        response = response.json()["response"]

        json_dump_dir = __tmp0.gmi.write_json_to
        if json_dump_dir is not None:
            from test.dump_json import dump_json

            dump_json(json_dump_dir, __tmp0, response)

        return response  # type: ignore
