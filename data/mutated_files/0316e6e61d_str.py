from typing import TypeAlias
__typ2 : TypeAlias = "Any"
from typing import List, Union, Any


class __typ1(Exception):
	def __init__(__tmp0, error_types: Union[List[str], str], message, **data: __typ2) -> None:
		super(__typ1, __tmp0).__init__()
		__tmp0.message = message
		__tmp0.error_types = [error_types] if isinstance(error_types, str) else error_types
		__tmp0.error_data = data

	def __tmp1(__tmp0) -> str:
		errors = ','.join(__tmp0.error_types)
		return (
			f'RouterError('
			f'message={__tmp0.message!r},'
			f'error_type={errors},'
			f'data={__tmp0.error_data!r})'
		)

	def __str__(__tmp0) :
		errors = ','.join(__tmp0.error_types)
		return f"({errors}): {__tmp0.message}"


class __typ3(__typ1):
	def __init__(__tmp0, message: str, **data: __typ2) -> None:
		super(__typ3, __tmp0).__init__(message=message, **{'error_types': 'response', **data})


class __typ4(__typ1):
	def __init__(__tmp0, message, **data: __typ2) -> None:
		super(__typ4, __tmp0).__init__(message=message, **{'error_types': 'connection', **data})


class __typ0(__typ1):
	def __init__(__tmp0, message: <FILL>, **data: __typ2) -> None:
		super(__typ0, __tmp0).__init__(message=message, **{'error_types': 'server', **data})


__all__ = [
	'RouterError',
	'RouterResponseError',
	'RouterConnectionError',
	'RouterServerError',
]
