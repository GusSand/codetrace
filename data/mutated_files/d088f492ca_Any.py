from typing import TypeAlias
__typ1 : TypeAlias = "str"
from typing import List, Union, Any


class __typ0(Exception):
	def __init__(__tmp0, error_types, message, **data) :
		super(__typ0, __tmp0).__init__()
		__tmp0.message = message
		__tmp0.error_types = [error_types] if isinstance(error_types, __typ1) else error_types
		__tmp0.error_data = data

	def __repr__(__tmp0) :
		errors = ','.join(__tmp0.error_types)
		return (
			f'RouterError('
			f'message={__tmp0.message!r},'
			f'error_type={errors},'
			f'data={__tmp0.error_data!r})'
		)

	def __tmp1(__tmp0) :
		errors = ','.join(__tmp0.error_types)
		return f"({errors}): {__tmp0.message}"


class RouterResponseError(__typ0):
	def __init__(__tmp0, message, **data) :
		super(RouterResponseError, __tmp0).__init__(message=message, **{'error_types': 'response', **data})


class RouterConnectionError(__typ0):
	def __init__(__tmp0, message, **data: <FILL>) :
		super(RouterConnectionError, __tmp0).__init__(message=message, **{'error_types': 'connection', **data})


class RouterServerError(__typ0):
	def __init__(__tmp0, message, **data) :
		super(RouterServerError, __tmp0).__init__(message=message, **{'error_types': 'server', **data})


__all__ = [
	'RouterError',
	'RouterResponseError',
	'RouterConnectionError',
	'RouterServerError',
]
