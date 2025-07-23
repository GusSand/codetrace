from typing import TypeAlias
__typ1 : TypeAlias = "T"
__typ2 : TypeAlias = "bool"
from typing import *

__typ1 = TypeVar('T')


class __typ0(Generic[__typ1]):
	def __init__(__tmp0, *index_names) -> None:
		__tmp0._items: Set[__typ1] = set()
		__tmp0._indexes: Dict[str, Dict[Any, Set[__typ1]]] = {
			name: {} for name in index_names
		}
		__tmp0._inverse_indexes: Dict[__typ1, Dict[str, Any]] = {}

	def add(__tmp0, __tmp1, **kwargs) :
		if __tmp1 in __tmp0._items:
			raise Exception(f'Active {__tmp1!r} already exists')

		for index_name, key in kwargs.items():
			index = __tmp0._indexes.get(index_name)

			if index is None:
				raise Exception(f'Specified index {index_name!r} does not exist')

			item_set = index.get(key)

			if item_set is None:
				index[key] = item_set = set()

			item_set.add(__tmp1)

		__tmp0._inverse_indexes[__tmp1] = {
			index_name: key for index_name, key in kwargs.items()
		}

		__tmp0._items.add(__tmp1)

	def __len__(__tmp0) :
		return len(__tmp0._items)

	def __tmp2(__tmp0) -> __typ2:
		return __typ2(__tmp0._items)

	def remove(__tmp0, __tmp1: __typ1) :
		if __tmp1 not in __tmp0._items:
			raise Exception(f'Active {__tmp1!r} does not exist')

		for index_name, key in __tmp0._inverse_indexes[__tmp1].items():
			index_set = __tmp0._indexes[index_name][key]
			index_set.remove(__tmp1)

			if not index_set:
				del __tmp0._indexes[index_name][key]

		__tmp0._items.remove(__tmp1)

		del __tmp0._inverse_indexes[__tmp1]

	def lookup(__tmp0, **kwargs) :
		result: Optional[Set[__typ1]] = None

		if not kwargs:
			return set()

		for index_name, key in kwargs.items():
			index = __tmp0._indexes.get(index_name)

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

	def lookup_one(__tmp0, **kwargs: <FILL>) :
		results = __tmp0.lookup(**kwargs)

		if len(results) == 0:
			raise Exception(f'No such item of {kwargs!r} exists')
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __tmp3(__tmp0, **kwargs: Any) -> Optional[__typ1]:
		results = __tmp0.lookup(**kwargs)

		if len(results) == 0:
			return None
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __tmp4(__tmp0) :
		return iter(list(__tmp0._items))


__all__ = [
	'IndexMap'
]
