from typing import TypeAlias
__typ1 : TypeAlias = "T"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
from typing import *

__typ1 = TypeVar('T')


class IndexMap(Generic[__typ1]):
	def __tmp5(__tmp1, *index_names) -> None:
		__tmp1._items: Set[__typ1] = set()
		__tmp1._indexes: Dict[str, Dict[Any, Set[__typ1]]] = {
			name: {} for name in index_names
		}
		__tmp1._inverse_indexes: Dict[__typ1, Dict[str, Any]] = {}

	def add(__tmp1, __tmp2: __typ1, **kwargs: Any) -> None:
		if __tmp2 in __tmp1._items:
			raise Exception(f'Active {__tmp2!r} already exists')

		for index_name, key in kwargs.items():
			index = __tmp1._indexes.get(index_name)

			if index is None:
				raise Exception(f'Specified index {index_name!r} does not exist')

			item_set = index.get(key)

			if item_set is None:
				index[key] = item_set = set()

			item_set.add(__tmp2)

		__tmp1._inverse_indexes[__tmp2] = {
			index_name: key for index_name, key in kwargs.items()
		}

		__tmp1._items.add(__tmp2)

	def __tmp7(__tmp1) -> __typ0:
		return len(__tmp1._items)

	def __tmp3(__tmp1) -> __typ2:
		return __typ2(__tmp1._items)

	def remove(__tmp1, __tmp2: __typ1) -> None:
		if __tmp2 not in __tmp1._items:
			raise Exception(f'Active {__tmp2!r} does not exist')

		for index_name, key in __tmp1._inverse_indexes[__tmp2].items():
			index_set = __tmp1._indexes[index_name][key]
			index_set.remove(__tmp2)

			if not index_set:
				del __tmp1._indexes[index_name][key]

		__tmp1._items.remove(__tmp2)

		del __tmp1._inverse_indexes[__tmp2]

	def lookup(__tmp1, **kwargs: <FILL>) -> Set[__typ1]:
		result: Optional[Set[__typ1]] = None

		if not kwargs:
			return set()

		for index_name, key in kwargs.items():
			index = __tmp1._indexes.get(index_name)

			if index is None:
				raise Exception(f'Specified index {index_name!r} does not exist')

			item_set = index.get(key)

			if not item_set:
				return set()

			if result is None:
				result = item_set.copy()
			else:
				result &= item_set

		assert result is not None

		return result

	def __tmp0(__tmp1, **kwargs: Any) -> __typ1:
		results = __tmp1.lookup(**kwargs)

		if len(results) == 0:
			raise Exception(f'No such item of {kwargs!r} exists')
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __tmp4(__tmp1, **kwargs: Any) -> Optional[__typ1]:
		results = __tmp1.lookup(**kwargs)

		if len(results) == 0:
			return None
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __tmp6(__tmp1) -> Iterator[__typ1]:
		return iter(list(__tmp1._items))


__all__ = [
	'IndexMap'
]
