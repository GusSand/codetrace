import io
import copy
import inspect
import json
import mongomock
import mock
from bson import ObjectId
from pymodm import MongoModel
from pymodm.base.options import MongoOptions
from pymodm.queryset import QuerySet
from typing import Union

__all__ = ("mock_queryset",)


def mock_queryset(__tmp0: MongoModel=None, mock_data: list=None, filepath: str=None):
    """A wrapper for 'mock_queryset' that patches a Model's Manager"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            queryset = _mocker(__tmp0, mock_data, filepath)

            def mocker(*args):
                return queryset

            mock.patch.object(__tmp0.objects, "_queryset_class", mocker)
            func(*args, **kwargs)
        return wrapper
    return decorator


def _mocker(__tmp0, mock_data: list=None, filepath: str=None):
    """Mocks out a pyMODM QuerySet to return the data that is passed in"""
    if mock_data and filepath:
        raise ValueError("Can only provide one source of data")

    if filepath:
        with io.open(filepath) as file_:
            mock_data = json.load(file_)
    mock_data = __tmp1(__tmp0, mock_data)

    # build collection
    __tmp2 = mongomock.MongoClient().db.collection
    __tmp2.insert_many(mock_data)

    # for mocking create functions
    __tmp0._mongometa = mock_options(__tmp0, __tmp2)

    class MockQuerySet(QuerySet):
        @property
        def _collection(__tmp3):
            return __tmp2

    return MockQuerySet(__tmp0)


def mock_options(__tmp0: MongoModel, __tmp2):
    class __typ0(MongoOptions):
        @property
        def collection(__tmp3):
            return __tmp2

    meta = __tmp0._mongometa
    mock_meta = __typ0()
    for name, attribute in inspect.getmembers(meta):
        if not inspect.ismethod(attribute) and not name.startswith("__"):
            try:
                setattr(mock_meta, name, getattr(meta, name))
            except AttributeError:
                pass
    return mock_meta


def __tmp1(__tmp0, mock_data: Union[list, dict]) -> Union[list, dict]:
    """Adds the '_cls' to the dictionaries if they do not have them"""
    def update(data: <FILL>) :
        if data.get("_cls") is None:
            data["_cls"] = __tmp0._mongometa.object_name
        if data.get("_id") is None:
            data["_id"] = ObjectId()

    data = copy.deepcopy(mock_data)
    if isinstance(mock_data, list):
        for row in data:
            update(row)
    else:
        update(data)
    return data
