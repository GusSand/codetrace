from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "T"
__typ1 : TypeAlias = "bool"
from typing import *

__typ0 = TypeVar('T')


class IndexMap(Generic[__typ0]):
	def __tmp2(__tmp1, *index_names: <FILL>) :
		__tmp1._items: Set[__typ0] = set()
		__tmp1._indexes: Dict[str, Dict[__typ2, Set[__typ0]]] = {
			name: {} for name in index_names
		}
		__tmp1._inverse_indexes: Dict[__typ0, Dict[str, __typ2]] = {}

	def add(__tmp1, __tmp3, **kwargs) :
		if __tmp3 in __tmp1._items:
			raise Exception(f'Active {__tmp3!r} already exists')

		for index_name, key in kwargs.items():
			index = __tmp1._indexes.get(index_name)

			if index is None:
				raise Exception(f'Specified index {index_name!r} does not exist')

			item_set = index.get(key)

			if item_set is None:
				index[key] = item_set = set()

			item_set.add(__tmp3)

		__tmp1._inverse_indexes[__tmp3] = {
			index_name: key for index_name, key in kwargs.items()
		}

		__tmp1._items.add(__tmp3)

	def __len__(__tmp1) :
		return len(__tmp1._items)

	def __bool__(__tmp1) :
		return __typ1(__tmp1._items)

	def remove(__tmp1, __tmp3) :
		if __tmp3 not in __tmp1._items:
			raise Exception(f'Active {__tmp3!r} does not exist')

		for index_name, key in __tmp1._inverse_indexes[__tmp3].items():
			index_set = __tmp1._indexes[index_name][key]
			index_set.remove(__tmp3)

			if not index_set:
				del __tmp1._indexes[index_name][key]

		__tmp1._items.remove(__tmp3)

		del __tmp1._inverse_indexes[__tmp3]

	def lookup(__tmp1, **kwargs) :
		result: Optional[Set[__typ0]] = None

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

	def lookup_one(__tmp1, **kwargs) :
		results = __tmp1.lookup(**kwargs)

		if len(results) == 0:
			raise Exception(f'No such item of {kwargs!r} exists')
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __tmp0(__tmp1, **kwargs: __typ2) :
		results = __tmp1.lookup(**kwargs)

		if len(results) == 0:
			return None
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __iter__(__tmp1) :
		return iter(list(__tmp1._items))


__all__ = [
	'IndexMap'
]
