from typing import TypeAlias
__typ0 : TypeAlias = "pipe"
import inspect

from .pdatastructures import PRecord
from .pbase import Source, Transformer, Sink, pipex_hash
from typing import Iterator, Any


def __tmp5(__tmp0):
    if getattr(__tmp0, 'pass_through', False):
        return ''
    __tmp3 = __tmp0.__class__
    return pipex_hash(
        __tmp3.__module__ + "." + __tmp3.__name__,
        *[
            segment
            for pair in sorted(__tmp0.__dict__.items(), key=lambda item: item[0])
            for segment in pair
        ]
    )

SOURCE_MEMBERS = set(__tmp7 for __tmp7, _ in inspect.getmembers(Source) if not __tmp7.startswith("_"))
TRANSFORMER_MEMBERS = set(__tmp7 for __tmp7, _ in inspect.getmembers(Transformer) if not __tmp7.startswith("_"))
SINK_MEMBERS = set(__tmp7 for __tmp7, _ in inspect.getmembers(Sink) if not __tmp7.startswith("_"))

class BaseMeta(type):
    def __getattribute__(__tmp3, __tmp7):
        if issubclass(__tmp3, Source) and __tmp7 in SOURCE_MEMBERS:
            return getattr(__tmp3(), __tmp7)
        elif issubclass(__tmp3, Transformer) and __tmp7 in TRANSFORMER_MEMBERS:
            return getattr(__tmp3(), __tmp7)
        elif issubclass(__tmp3, Sink) and __tmp7 in SINK_MEMBERS:
            return getattr(__tmp3(), __tmp7)
        return super().__getattribute__(__tmp7)

class __typ2(BaseMeta, Source):
    def generate_precords(__tmp3, our) :
        return __tmp3().generate_precords(our)


class __typ1(BaseMeta, Transformer):
    def transform(__tmp3, our, __tmp4) :
        return __tmp3().transform(our, __tmp4)

class SinkMeta(BaseMeta, Sink):
    def process(__tmp3, our, __tmp4) :
        return __tmp3().process(our, __tmp4)


class source(Source, metaclass=__typ2):
    channel_name = 'default'

    def generate(__tmp0) :
        raise NotImplementedError

    def generate_precords(__tmp0, our) :
        for object in __tmp0.generate():
            yield PRecord.from_object(object, __tmp0.channel_name)

    def __tmp5(__tmp0):
        return __tmp5(__tmp0)

class __typ0(Transformer, metaclass=__typ1):
    def transform(__tmp0, our, __tmp4) :
        raise NotImplementedError

    def __tmp6(__tmp0):
        __tmp3 = __tmp0.__class__
        if __tmp3.__module__.startswith("pipex."):
            return __tmp3.__module__.replace(".operators.funcs", "") + "." + __tmp3.__name__
        else:
            return __tmp3.__module__ + "." + __tmp3.__name__

    def __tmp5(__tmp0):
        return __tmp5(__tmp0)


class pipe_map(__typ0):
    def filter(__tmp0, value: Any) :
        return True

    def map(__tmp0, value: <FILL>) -> Any:
        return value

    def transform(__tmp0, our, __tmp4) -> Iterator[PRecord]:
        fn = __tmp0.map
        for __tmp1 in __tmp4:
            value = __tmp1.value
            if not __tmp0.filter(value): continue
            new_value = fn(value)
            yield __tmp1.with_value(new_value)


class sink(Sink, metaclass=SinkMeta):
    def save(__tmp0, __tmp1):
        raise NotImplementedError

    def process(__tmp0, our, __tmp2) :
        for __tmp1 in __tmp2.generate_precords(our):
            __tmp0.save(__tmp1)
            yield __tmp1

    def __tmp5(__tmp0):
        return __tmp5(__tmp0)

class value_sink(sink):
    def save(__tmp0, __tmp1):
        __tmp0.save_value(__tmp1.value)

    def save_value(__tmp0, __tmp1):
        raise NotImplementedError
