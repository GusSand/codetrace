from typing import TypeAlias
__typ4 : TypeAlias = "Any"
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
from typing import *

T = TypeVar('T')


class __typ0(Generic[T]):
	def __tmp3(__tmp0, *index_names) :
		__tmp0._items: Set[T] = set()
		__tmp0._indexes: Dict[__typ2, Dict[__typ4, Set[T]]] = {
			name: {} for name in index_names
		}
		__tmp0._inverse_indexes: Dict[T, Dict[__typ2, __typ4]] = {}

	def add(__tmp0, __tmp1: <FILL>, **kwargs) :
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

	def __tmp4(__tmp0) :
		return len(__tmp0._items)

	def __tmp2(__tmp0) :
		return __typ3(__tmp0._items)

	def remove(__tmp0, __tmp1) :
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
		result: Optional[Set[T]] = None

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

	def lookup_one(__tmp0, **kwargs) -> T:
		results = __tmp0.lookup(**kwargs)

		if len(results) == 0:
			raise Exception(f'No such item of {kwargs!r} exists')
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def try_lookup_one(__tmp0, **kwargs) :
		results = __tmp0.lookup(**kwargs)

		if len(results) == 0:
			return None
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __iter__(__tmp0) :
		return iter(list(__tmp0._items))


__all__ = [
	'IndexMap'
]
