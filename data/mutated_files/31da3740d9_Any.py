from typing import TypeAlias
__typ0 : TypeAlias = "bool"
from typing import *

T = TypeVar('T')


class IndexMap(Generic[T]):
	def __init__(__tmp0, *index_names) :
		__tmp0._items: Set[T] = set()
		__tmp0._indexes: Dict[str, Dict[Any, Set[T]]] = {
			name: {} for name in index_names
		}
		__tmp0._inverse_indexes: Dict[T, Dict[str, Any]] = {}

	def add(__tmp0, item, **kwargs) :
		if item in __tmp0._items:
			raise Exception(f'Active {item!r} already exists')

		for index_name, key in kwargs.items():
			index = __tmp0._indexes.get(index_name)

			if index is None:
				raise Exception(f'Specified index {index_name!r} does not exist')

			item_set = index.get(key)

			if item_set is None:
				index[key] = item_set = set()

			item_set.add(item)

		__tmp0._inverse_indexes[item] = {
			index_name: key for index_name, key in kwargs.items()
		}

		__tmp0._items.add(item)

	def __len__(__tmp0) :
		return len(__tmp0._items)

	def __bool__(__tmp0) :
		return __typ0(__tmp0._items)

	def remove(__tmp0, item) :
		if item not in __tmp0._items:
			raise Exception(f'Active {item!r} does not exist')

		for index_name, key in __tmp0._inverse_indexes[item].items():
			index_set = __tmp0._indexes[index_name][key]
			index_set.remove(item)

			if not index_set:
				del __tmp0._indexes[index_name][key]

		__tmp0._items.remove(item)

		del __tmp0._inverse_indexes[item]

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

	def lookup_one(__tmp0, **kwargs) :
		results = __tmp0.lookup(**kwargs)

		if len(results) == 0:
			raise Exception(f'No such item of {kwargs!r} exists')
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def try_lookup_one(__tmp0, **kwargs: <FILL>) :
		results = __tmp0.lookup(**kwargs)

		if len(results) == 0:
			return None
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __iter__(__tmp0) -> Iterator[T]:
		return iter(list(__tmp0._items))


__all__ = [
	'IndexMap'
]
