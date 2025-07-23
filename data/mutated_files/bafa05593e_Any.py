from typing import TypeAlias
__typ1 : TypeAlias = "str"
from typing import List, Union, Any


class RouterError(Exception):
	def __init__(__tmp0, error_types, message, **data: <FILL>) :
		super(RouterError, __tmp0).__init__()
		__tmp0.message = message
		__tmp0.error_types = [error_types] if isinstance(error_types, __typ1) else error_types
		__tmp0.error_data = data

	def __tmp2(__tmp0) :
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


class __typ3(RouterError):
	def __init__(__tmp0, message, **data) :
		super(__typ3, __tmp0).__init__(message=message, **{'error_types': 'response', **data})


class __typ2(RouterError):
	def __init__(__tmp0, message, **data) :
		super(__typ2, __tmp0).__init__(message=message, **{'error_types': 'connection', **data})


class __typ0(RouterError):
	def __init__(__tmp0, message, **data) :
		super(__typ0, __tmp0).__init__(message=message, **{'error_types': 'server', **data})


__all__ = [
	'RouterError',
	'RouterResponseError',
	'RouterConnectionError',
	'RouterServerError',
]
