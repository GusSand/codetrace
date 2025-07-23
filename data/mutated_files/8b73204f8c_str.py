from typing import TypeAlias
__typ0 : TypeAlias = "Any"
from typing import List, Union, Any


class RouterError(Exception):
	def __init__(__tmp0, error_types: Union[List[str], str], message: str, **data: __typ0) :
		super(RouterError, __tmp0).__init__()
		__tmp0.message = message
		__tmp0.error_types = [error_types] if isinstance(error_types, str) else error_types
		__tmp0.error_data = data

	def __repr__(__tmp0) -> str:
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


class RouterResponseError(RouterError):
	def __init__(__tmp0, message: str, **data) :
		super(RouterResponseError, __tmp0).__init__(message=message, **{'error_types': 'response', **data})


class RouterConnectionError(RouterError):
	def __init__(__tmp0, message: <FILL>, **data) -> None:
		super(RouterConnectionError, __tmp0).__init__(message=message, **{'error_types': 'connection', **data})


class __typ1(RouterError):
	def __init__(__tmp0, message, **data) :
		super(__typ1, __tmp0).__init__(message=message, **{'error_types': 'server', **data})


__all__ = [
	'RouterError',
	'RouterResponseError',
	'RouterConnectionError',
	'RouterServerError',
]
