# pyre-strict
import json
import os
from importlib import import_module
from typing import Any, Dict, List, Optional, Type
from unittest import TestCase, mock

from lowerpines.endpoints.object import AbstractObject
from lowerpines.endpoints.request import JsonType
from lowerpines.gmi import GMI


class __typ0:
    def __init__(__tmp0, response_json) :
        __tmp0.response_json = response_json
        __tmp0.status_code = 200
        __tmp0.content: bytes = json.dumps(response_json).encode("utf-8")

    def json(__tmp0) :
        return {"response": __tmp0.response_json}


class TestReplayAll(TestCase):
    def setUp(__tmp0) :
        test_data_dir = "test_data"
        __tmp0.json_data: Dict[str, Any] = {}
        for file_name in os.listdir(test_data_dir):
            klass, _ = file_name.split("_")
            with open(os.path.join(test_data_dir, file_name), "r") as file_contents:
                __tmp0.json_data[klass] = json.load(file_contents)

    def test_all(__tmp0) :
        for name, recorded_data in __tmp0.json_data.items():
            with __tmp0.subTest(name=name, args=recorded_data["request"]["args"]):
                __tmp0.check_file(name, recorded_data)

    def check_file(__tmp0, name, recorded_data) :
        def mocked_requests_api_call(
            url: <FILL>,
            params,
            headers: List[str],
            data: Optional[str] = None,
        ) :
            if data is None:
                __tmp0.assertEqual(params, recorded_data["request"]["args"])
            else:
                __tmp0.assertEqual(json.loads(data), recorded_data["request"]["args"])
            __tmp0.assertTrue(url, recorded_data["request"]["url"])
            return __typ0(recorded_data["response"])

        name_split = name.split(".")
        module, klass_name = ".".join(name_split[:-1]), name_split[-1]
        klass = getattr(import_module(module), klass_name)
        if recorded_data["request"]["mode"] == "GET":
            patch_func = "get"
        else:
            patch_func = "post"
        with mock.patch("requests." + patch_func, side_effect=mocked_requests_api_call):
            instance = klass(GMI("test_gmi"), **recorded_data["request"]["init"])
            try:
                results = instance.result
            except AttributeError:
                results = None
            if isinstance(results, list):
                for result in results:
                    __tmp0.check_types(result)
            elif results is None:
                __tmp0.assertEqual(instance.parse(recorded_data["response"]), None)
            elif type(results) in [bool]:
                pass
            else:
                __tmp0.check_types(results)

    def check_types(__tmp0, klass) -> None:
        for key, expected in klass.__annotations__.items():
            actual = type(getattr(klass, key))

            # Make sure the key we're looking at is actually a Field
            if len(list(filter(lambda k: k.name == key, klass._fields))) == 0:
                continue

            matching_types = [expected]
            # Unions need to be deconstructed
            if repr(expected).startswith("typing.Union"):
                matching_types = expected.__args__

            # typing module types don't == with their runtime equivalents, need to clean those up
            # pyre-ignore
            matching_types_cleaned: List[Type[Any]] = []
            for matching_type in matching_types:
                if repr(matching_type).startswith("typing.List"):
                    matching_types_cleaned.append(list)
                elif repr(matching_type).startswith("typing.Dict"):
                    matching_types_cleaned.append(dict)
                elif repr(matching_type).startswith("typing.Optional"):
                    matching_types_cleaned.extend(matching_type.__args__)
                else:
                    matching_types_cleaned.append(matching_type)
            __tmp0.assertTrue(
                actual in matching_types_cleaned,
                f"{klass.__class__.__name__}.{key} expected {matching_types_cleaned} but got {type(getattr(klass, key))}",
            )
