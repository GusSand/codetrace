from typing import TypeAlias
__typ4 : TypeAlias = "Dict"
__typ0 : TypeAlias = "str"
import json
import uuid
from copy import deepcopy
from typing import *

from .router.errors import RouterError


class __typ3(Exception):
	pass


class ReservedKeyError(__typ3):
	pass


class __typ1(json.JSONEncoder):
	def default(__tmp0, __tmp1: Any) -> Any:
		if isinstance(__tmp1, uuid.UUID):
			return __typ0(__tmp1)

		return super(__typ1, __tmp0).default(__tmp1)


class __typ2(object):
	_RESERVED_KEYS = {'success', 'error', 'error_data', '__final'}

	def __tmp3(
		__tmp0,
		data: Optional[__typ4] = None,
		success: Optional[bool] = None,
		error: Optional[__typ0] = None,
		error_data: Optional[__typ4] = None,
		*, is_final: bool = False,
	) :
		__tmp0.data: __typ4 = deepcopy(data) if data is not None else {}

		__typ2.verify_reserved_use(__tmp0.data)

		__tmp0.success: Optional[bool] = success
		__tmp0.error: Optional[__typ0] = error
		__tmp0.error_data: Optional[__typ4] = error_data
		__tmp0.is_final: bool = is_final

	def load(__tmp0, json_data: __typ4) -> 'Message':
		__tmp0.data = deepcopy(json_data)

		__tmp0.success = json_data.get('success')
		__tmp0.error = json_data.get('error')
		__tmp0.error_data = json_data.get('error_data')
		__tmp0.is_final = bool(json_data.get('__final'))

		for key in ('success', 'error', 'error_data'):
			if key in __tmp0.data:
				del __tmp0.data[key]

		return __tmp0

	@classmethod
	def verify_reserved_use(__tmp2, data: __typ4) -> None:
		if set(data.keys()) & __tmp2._RESERVED_KEYS:
			raise ReservedKeyError()

	@classmethod
	def __tmp6(__tmp2, __tmp4: BaseException) -> 'Message':
		if isinstance(__tmp4, RouterError):
			error_data = __tmp4.error_data.copy()

			# Try to decode error data, if successful then we can serialize it
			# if not then turn it into a repr'd string and send that instead.
			for key, value in error_data.items():
				try:
					json.dumps(value, __tmp2=__typ1)
				except TypeError:
					error_data[key] = repr(value)

			if not error_data.get('exc_class'):
				error_data['exc_class'] = __tmp4.__class__.__name__

			error_data['error_types'] = __tmp4.error_types

			return __typ2(success=False, error=__tmp4.message, error_data=error_data)

		return __typ2(success=False, error=__typ0(__tmp4), error_data={'data': repr(__tmp4)})

	def _render_tags(__tmp0) -> List[__typ0]:
		tags = []

		if __tmp0.success is not None:
			tags.append(f'success={__tmp0.success}')

		if __tmp0.error:
			tags.append(f'error={__tmp0.error}')

		return tags

	def __str__(__tmp0) -> __typ0:
		tags = ' '.join(__tmp0._render_tags())
		return f'Message({tags}): {__tmp0.data!r}'

	def __tmp5(__tmp0) -> __typ0:
		return __typ0(__tmp0)

	def extend(__tmp0, **kwargs: <FILL>) -> 'Message':
		__tmp0.data.update(**kwargs)
		return __tmp0

	def __tmp7(__tmp0) -> 'Message':
		copy = __typ2()
		copy.__dict__ = deepcopy(__tmp0.__dict__)

		return copy

	def json(__tmp0, **extra: Any) -> __typ0:
		payload = {
			**__tmp0.data,
			**extra,
		}

		if __tmp0.success is not None:
			payload['success'] = __tmp0.success

		if __tmp0.error or (__tmp0.success is not None and not __tmp0.success):
			payload['error'] = __tmp0.error

		if __tmp0.error_data:
			payload['error_data'] = __tmp0.error_data

		if __tmp0.is_final:
			payload['__final'] = True

		return json.dumps(payload, __tmp2=__typ1)


__all__ = ['Message']
