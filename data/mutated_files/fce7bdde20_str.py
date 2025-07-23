from typing import TypeAlias
__typ2 : TypeAlias = "Any"
from typing import List, Union, Any


class __typ0(Exception):
	def __init__(self, error_types: Union[List[str], str], message: str, **data: __typ2) -> None:
		super(__typ0, self).__init__()
		self.message = message
		self.error_types = [error_types] if isinstance(error_types, str) else error_types
		self.error_data = data

	def __repr__(self) :
		errors = ','.join(self.error_types)
		return (
			f'RouterError('
			f'message={self.message!r},'
			f'error_type={errors},'
			f'data={self.error_data!r})'
		)

	def __str__(self) -> str:
		errors = ','.join(self.error_types)
		return f"({errors}): {self.message}"


class __typ3(__typ0):
	def __init__(self, message: <FILL>, **data: __typ2) :
		super(__typ3, self).__init__(message=message, **{'error_types': 'response', **data})


class RouterConnectionError(__typ0):
	def __init__(self, message, **data: __typ2) -> None:
		super(RouterConnectionError, self).__init__(message=message, **{'error_types': 'connection', **data})


class __typ1(__typ0):
	def __init__(self, message: str, **data: __typ2) :
		super(__typ1, self).__init__(message=message, **{'error_types': 'server', **data})


__all__ = [
	'RouterError',
	'RouterResponseError',
	'RouterConnectionError',
	'RouterServerError',
]
