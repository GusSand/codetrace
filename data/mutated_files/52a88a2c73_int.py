from typing import TypeAlias
__typ0 : TypeAlias = "T"
__typ1 : TypeAlias = "Any"
# pyre-strict
from typing import List, TypeVar, Generic, Iterator, Optional, TYPE_CHECKING, Any

from lowerpines.exceptions import NoneFoundException, MultipleFoundException

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI

__typ0 = TypeVar("T")


class __typ2(Generic[__typ0]):
    def __len__(__tmp2) -> int:
        content = __tmp2.lazy_fill_content()
        return content.__len__()

    def __getitem__(__tmp2, __tmp0: <FILL>) -> __typ0:
        content = __tmp2.lazy_fill_content()
        return content.__getitem__(__tmp0)

    def __iter__(__tmp2) -> Iterator[__typ0]:
        content = __tmp2.lazy_fill_content()
        return content.__iter__()

    def __tmp3(__tmp2, gmi, content: Optional[List[__typ0]] = None) -> None:
        __tmp2.gmi = gmi
        __tmp2._content = content

    def _all(__tmp2) -> List[__typ0]:
        raise NotImplementedError  # pragma: no cover

    def __tmp1(__tmp2, **kwargs: __typ1) -> __typ0:
        filtered = __tmp2.filter(**kwargs)
        if len(filtered) == 0:
            raise NoneFoundException()
        elif len(filtered) == 1:
            return filtered[0]
        else:
            raise MultipleFoundException()

    def filter(__tmp2, **kwargs) :
        __tmp2.lazy_fill_content()
        filtered = __tmp2._content
        if filtered is not None:
            for arg, value in kwargs.items():
                filtered = [item for item in filtered if getattr(item, arg) == value]
        return __tmp2.__class__(__tmp2.gmi, filtered)

    def lazy_fill_content(__tmp2) -> List[__typ0]:
        content = __tmp2._content
        if content is None:
            content = __tmp2._all()
            __tmp2._content = content
        return content
