import os
import json


def _this_dir() :
    return os.path.dirname(os.path.abspath(__file__))


def _schema_dir() -> str:
    return os.path.join(os.path.dirname(_this_dir()), "aw_core", "schemas")


def __tmp0(__tmp1: <FILL>) -> dict:
    with open(os.path.join(_schema_dir(), __tmp1 + ".json")) as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    print(__tmp0("event"))
