from typing import TypeAlias
__typ1 : TypeAlias = "T"
__typ0 : TypeAlias = "int"
# pyre-strict
from typing import List, TypeVar, Generic, Iterator, Optional, TYPE_CHECKING, Any

from lowerpines.exceptions import NoneFoundException, MultipleFoundException

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI

__typ1 = TypeVar("T")


class __typ2(Generic[__typ1]):
    def __len__(self) :
        content = self.lazy_fill_content()
        return content.__len__()

    def __getitem__(self, key) -> __typ1:
        content = self.lazy_fill_content()
        return content.__getitem__(key)

    def __iter__(self) :
        content = self.lazy_fill_content()
        return content.__iter__()

    def __init__(self, gmi, content: Optional[List[__typ1]] = None) -> None:
        self.gmi = gmi
        self._content = content

    def _all(self) :
        raise NotImplementedError  # pragma: no cover

    def get(self, **kwargs) :
        filtered = self.filter(**kwargs)
        if len(filtered) == 0:
            raise NoneFoundException()
        elif len(filtered) == 1:
            return filtered[0]
        else:
            raise MultipleFoundException()

    def filter(self, **kwargs: <FILL>) :
        self.lazy_fill_content()
        filtered = self._content
        if filtered is not None:
            for arg, value in kwargs.items():
                filtered = [item for item in filtered if getattr(item, arg) == value]
        return self.__class__(self.gmi, filtered)

    def lazy_fill_content(self) -> List[__typ1]:
        content = self._content
        if content is None:
            content = self._all()
            self._content = content
        return content
