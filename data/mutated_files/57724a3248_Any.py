from typing import TypeAlias
__typ0 : TypeAlias = "T"
# pyre-strict
from typing import List, TypeVar, Generic, Iterator, Optional, TYPE_CHECKING, Any

from lowerpines.exceptions import NoneFoundException, MultipleFoundException

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI

__typ0 = TypeVar("T")


class AbstractManager(Generic[__typ0]):
    def __len__(__tmp1) -> int:
        content = __tmp1.lazy_fill_content()
        return content.__len__()

    def __getitem__(__tmp1, key: int) -> __typ0:
        content = __tmp1.lazy_fill_content()
        return content.__getitem__(key)

    def __iter__(__tmp1) -> Iterator[__typ0]:
        content = __tmp1.lazy_fill_content()
        return content.__iter__()

    def __init__(__tmp1, gmi: "GMI", content: Optional[List[__typ0]] = None) -> None:
        __tmp1.gmi = gmi
        __tmp1._content = content

    def _all(__tmp1) :
        raise NotImplementedError  # pragma: no cover

    def __tmp0(__tmp1, **kwargs: <FILL>) -> __typ0:
        filtered = __tmp1.filter(**kwargs)
        if len(filtered) == 0:
            raise NoneFoundException()
        elif len(filtered) == 1:
            return filtered[0]
        else:
            raise MultipleFoundException()

    def filter(__tmp1, **kwargs: Any) -> "AbstractManager[T]":
        __tmp1.lazy_fill_content()
        filtered = __tmp1._content
        if filtered is not None:
            for arg, value in kwargs.items():
                filtered = [item for item in filtered if getattr(item, arg) == value]
        return __tmp1.__class__(__tmp1.gmi, filtered)

    def lazy_fill_content(__tmp1) :
        content = __tmp1._content
        if content is None:
            content = __tmp1._all()
            __tmp1._content = content
        return content
