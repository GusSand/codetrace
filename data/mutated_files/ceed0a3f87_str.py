from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ3 : TypeAlias = "Any"
__typ0 : TypeAlias = "int"
import asyncio
import logging
import threading
from typing import Optional, List, Any

import websockets
from websockets import WebSocketServerProtocol

from ..logger import g_logger


class __typ2:
	def __init__(__tmp1) -> None:
		__tmp1.connections: List[__typ1] = []
		__tmp1._lock = threading.Lock()
		__tmp1.last_connection_id = 0

	def generate_id(__tmp1) -> __typ0:
		with __tmp1._lock:
			__tmp1.last_connection_id += 1
			return __tmp1.last_connection_id

	def add(__tmp1, __tmp5: 'Connection') :
		with __tmp1._lock:
			__tmp1.connections.append(__tmp5)
			__tmp5.in_pool = True

	def remove(__tmp1, __tmp5: 'Connection') -> None:
		with __tmp1._lock:
			__tmp1.connections.remove(__tmp5)

	def __tmp4(__tmp1) -> __typ4:
		with __tmp1._lock:
			return __typ4(__tmp1.connections)

	def __tmp2(__tmp1) -> __typ0:
		with __tmp1._lock:
			return len(__tmp1.connections)

	def __tmp0(__tmp1) -> List['Connection']:
		with __tmp1._lock:
			return __tmp1.connections[:]

	def close(__tmp1, __tmp3: <FILL>) -> None:
		with __tmp1._lock:
			for conn in __tmp1.connections:
				conn.close(__tmp3=__tmp3)


class __typ1(object):
	def __init__(
		__tmp1,
		conn_list: __typ2,
		event_loop: asyncio.AbstractEventLoop,
		ws: WebSocketServerProtocol = None,
		**extra_kwargs: __typ3
	) -> None:
		__tmp1.extra = extra_kwargs
		__tmp1.ws: WebSocketServerProtocol = ws
		__tmp1.event_loop = event_loop
		__tmp1.conn_list = conn_list

		__tmp1.closed = False
		__tmp1._close_issued = False
		__tmp1._close_event = asyncio.Event(loop=__tmp1.event_loop)

		__tmp1.close_reason: Optional[str] = None
		__tmp1.close_code: Optional[__typ0] = None
		__tmp1.in_pool = False

		__tmp1.conn_id = conn_list.generate_id()

		__tmp1._close_lock = threading.Lock()

		__tmp1.logger = g_logger.getChild(f'Connection:{__tmp1.conn_id}')
		__tmp1.logger.debug(f'Created connection {__tmp1!r}')

	@property
	def close_issued(__tmp1) -> __typ4:
		return __tmp1._close_issued

	def __tmp11(__tmp1, __tmp7: 'Connection') -> None:
		"""
		Copy contents of normal Connection object to subclass instance of Connection.
		:param subclassed_object:
		:return:
		"""
		if __tmp1.conn_list is not __tmp7.conn_list:
			raise Exception('Cannot copy to sub-class of different router')

		for v in ('extra', 'ws', 'closed', 'in_pool', 'close_reason', 'close_code', 'conn_id', 'conn_list'):
			my_value = getattr(__tmp1, v)
			setattr(__tmp7, v, my_value)

	def __tmp8(__tmp1) -> str:
		if __tmp1.ws:
			addr, port, *_ = __tmp1.ws.remote_address

			tags = [
				f'id:{__tmp1.conn_id}',
				f'remote:{addr}:{port}',
			]
		else:
			tags = [f'id:{__tmp1.conn_id}', 'broadcast']

		if __tmp1._close_issued:
			tags.append('closed')

		return 'Connection({})'.format(','.join(tags))

	def __tmp10(__tmp1) -> str:
		if __tmp1.ws:
			tags = [
				f'id:{__tmp1.conn_id}',
			]
		else:
			tags = [f'id:{__tmp1.conn_id}', 'broadcast']

		if __tmp1._close_issued:
			tags.append('closed')

		return 'Connection({})'.format(','.join(tags))

	def close(__tmp1, code: __typ0 = 1000, __tmp3: str = '') -> None:
		with __tmp1._close_lock:
			if __tmp1._close_issued:
				__tmp1.logger.warning('Close already issued')
				return

			__tmp1._close_issued = True
			__tmp1.logger.debug('Issuing close')

		__tmp1.close_code = code or 1000
		__tmp1.close_reason = __tmp3 or ''

		async def async_callback() -> __typ4:
			with __tmp1._close_lock:
				__tmp1._close_issued = True

			if __tmp1.closed:
				__tmp1.logger.warning('Close callback cancelled since already closed')
				return True

			if __tmp1.in_pool:
				__tmp1.conn_list.remove(__tmp1)

			try:
				await __tmp1.ws.close(code=__tmp1.close_code, __tmp3=__tmp1.close_reason)
			except websockets.InvalidState:  # Expected if connection closed first
				pass
			except Exception as e:
				__tmp1.logger.error(f'Exception while attempting to close connection: {e!r}')

			__tmp1._close_event.set()

			__tmp1.logger.debug(f'Closed with code {__tmp1.close_code} and reason {__tmp1.close_reason}')

			__tmp1.closed = True

			return True

		def __tmp6() -> None:
			__tmp1.logger.debug('Scheduling close callback')
			__tmp1.close_future = asyncio.ensure_future(async_callback(), loop=__tmp1.event_loop)

		__tmp1.event_loop.call_soon_threadsafe(__tmp6)

	async def __tmp9(__tmp1) -> None:
		__tmp1.logger.debug('Waiting closed')
		await __tmp1._close_event.wait()
		__tmp1.logger.debug('Close arrived')


__all__ = [
	'ConnectionList',
	'Connection',
]
