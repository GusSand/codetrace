from typing import List, Union, Any


class __typ0(Exception):
	def __init__(__tmp0, error_types: Union[List[str], str], message, **data) -> None:
		super(__typ0, __tmp0).__init__()
		__tmp0.message = message
		__tmp0.error_types = [error_types] if isinstance(error_types, str) else error_types
		__tmp0.error_data = data

	def __repr__(__tmp0) :
		errors = ','.join(__tmp0.error_types)
		return (
			f'RouterError('
			f'message={__tmp0.message!r},'
			f'error_type={errors},'
			f'data={__tmp0.error_data!r})'
		)

	def __str__(__tmp0) -> str:
		errors = ','.join(__tmp0.error_types)
		return f"({errors}): {__tmp0.message}"


class RouterResponseError(__typ0):
	def __init__(__tmp0, message: str, **data) :
		super(RouterResponseError, __tmp0).__init__(message=message, **{'error_types': 'response', **data})


class __typ1(__typ0):
	def __init__(__tmp0, message, **data) -> None:
		super(__typ1, __tmp0).__init__(message=message, **{'error_types': 'connection', **data})


class RouterServerError(__typ0):
	def __init__(__tmp0, message: str, **data: <FILL>) -> None:
		super(RouterServerError, __tmp0).__init__(message=message, **{'error_types': 'server', **data})


__all__ = [
	'RouterError',
	'RouterResponseError',
	'RouterConnectionError',
	'RouterServerError',
]
