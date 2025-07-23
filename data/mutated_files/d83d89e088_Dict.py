from typing import TypeAlias
__typ0 : TypeAlias = "Any"
import json
import uuid
from copy import deepcopy
from typing import *

from .router.errors import RouterError


class MessageError(Exception):
	pass


class ReservedKeyError(MessageError):
	pass


class MessageJSONEncoder(json.JSONEncoder):
	def default(__tmp0, obj) :
		if isinstance(obj, uuid.UUID):
			return str(obj)

		return super(MessageJSONEncoder, __tmp0).default(obj)


class Message(object):
	_RESERVED_KEYS = {'success', 'error', 'error_data', '__final'}

	def __init__(
		__tmp0,
		data: Optional[Dict] = None,
		success: Optional[bool] = None,
		error: Optional[str] = None,
		error_data: Optional[Dict] = None,
		*, is_final: bool = False,
	) :
		__tmp0.data: Dict = deepcopy(data) if data is not None else {}

		Message.verify_reserved_use(__tmp0.data)

		__tmp0.success: Optional[bool] = success
		__tmp0.error: Optional[str] = error
		__tmp0.error_data: Optional[Dict] = error_data
		__tmp0.is_final: bool = is_final

	def load(__tmp0, json_data) :
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
	def verify_reserved_use(cls, data: <FILL>) :
		if set(data.keys()) & cls._RESERVED_KEYS:
			raise ReservedKeyError()

	@classmethod
	def error_from_exc(cls, exc) :
		if isinstance(exc, RouterError):
			error_data = exc.error_data.copy()

			# Try to decode error data, if successful then we can serialize it
			# if not then turn it into a repr'd string and send that instead.
			for key, value in error_data.items():
				try:
					json.dumps(value, cls=MessageJSONEncoder)
				except TypeError:
					error_data[key] = repr(value)

			if not error_data.get('exc_class'):
				error_data['exc_class'] = exc.__class__.__name__

			error_data['error_types'] = exc.error_types

			return Message(success=False, error=exc.message, error_data=error_data)

		return Message(success=False, error=str(exc), error_data={'data': repr(exc)})

	def _render_tags(__tmp0) :
		tags = []

		if __tmp0.success is not None:
			tags.append(f'success={__tmp0.success}')

		if __tmp0.error:
			tags.append(f'error={__tmp0.error}')

		return tags

	def __str__(__tmp0) :
		tags = ' '.join(__tmp0._render_tags())
		return f'Message({tags}): {__tmp0.data!r}'

	def __repr__(__tmp0) :
		return str(__tmp0)

	def extend(__tmp0, **kwargs) :
		__tmp0.data.update(**kwargs)
		return __tmp0

	def clone(__tmp0) :
		copy = Message()
		copy.__dict__ = deepcopy(__tmp0.__dict__)

		return copy

	def json(__tmp0, **extra) :
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

		return json.dumps(payload, cls=MessageJSONEncoder)


__all__ = ['Message']
