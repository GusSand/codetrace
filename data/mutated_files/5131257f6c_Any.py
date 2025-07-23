from typing import *

T = TypeVar('T')


class IndexMap(Generic[T]):
	def __init__(__tmp1, *index_names: str) -> None:
		__tmp1._items: Set[T] = set()
		__tmp1._indexes: Dict[str, Dict[Any, Set[T]]] = {
			name: {} for name in index_names
		}
		__tmp1._inverse_indexes: Dict[T, Dict[str, Any]] = {}

	def add(__tmp1, item, **kwargs: <FILL>) :
		if item in __tmp1._items:
			raise Exception(f'Active {item!r} already exists')

		for index_name, key in kwargs.items():
			index = __tmp1._indexes.get(index_name)

			if index is None:
				raise Exception(f'Specified index {index_name!r} does not exist')

			item_set = index.get(key)

			if item_set is None:
				index[key] = item_set = set()

			item_set.add(item)

		__tmp1._inverse_indexes[item] = {
			index_name: key for index_name, key in kwargs.items()
		}

		__tmp1._items.add(item)

	def __tmp5(__tmp1) :
		return len(__tmp1._items)

	def __tmp2(__tmp1) -> bool:
		return bool(__tmp1._items)

	def remove(__tmp1, item: T) -> None:
		if item not in __tmp1._items:
			raise Exception(f'Active {item!r} does not exist')

		for index_name, key in __tmp1._inverse_indexes[item].items():
			index_set = __tmp1._indexes[index_name][key]
			index_set.remove(item)

			if not index_set:
				del __tmp1._indexes[index_name][key]

		__tmp1._items.remove(item)

		del __tmp1._inverse_indexes[item]

	def lookup(__tmp1, **kwargs: Any) :
		result: Optional[Set[T]] = None

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

	def __tmp0(__tmp1, **kwargs) -> T:
		results = __tmp1.lookup(**kwargs)

		if len(results) == 0:
			raise Exception(f'No such item of {kwargs!r} exists')
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __tmp3(__tmp1, **kwargs) -> Optional[T]:
		results = __tmp1.lookup(**kwargs)

		if len(results) == 0:
			return None
		elif len(results) > 1:
			raise Exception(f'More than one item of {kwargs!r} exists')

		return list(results)[0]

	def __tmp4(__tmp1) :
		return iter(list(__tmp1._items))


__all__ = [
	'IndexMap'
]
