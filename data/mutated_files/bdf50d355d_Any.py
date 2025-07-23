from typing import TypeAlias
__typ0 : TypeAlias = "bool"
import asyncio
import logging
import threading
from typing import Optional, List, Any

import websockets
from websockets import WebSocketServerProtocol

from ..logger import g_logger


class ConnectionList:
	def __tmp6(__tmp0) -> None:
		__tmp0.connections: List[Connection] = []
		__tmp0._lock = threading.Lock()
		__tmp0.last_connection_id = 0

	def generate_id(__tmp0) :
		with __tmp0._lock:
			__tmp0.last_connection_id += 1
			return __tmp0.last_connection_id

	def __tmp5(__tmp0, __tmp3) -> None:
		with __tmp0._lock:
			__tmp0.connections.append(__tmp3)
			__tmp3.in_pool = True

	def remove(__tmp0, __tmp3: 'Connection') -> None:
		with __tmp0._lock:
			__tmp0.connections.remove(__tmp3)

	def __tmp2(__tmp0) :
		with __tmp0._lock:
			return __typ0(__tmp0.connections)

	def __tmp8(__tmp0) -> int:
		with __tmp0._lock:
			return len(__tmp0.connections)

	def copy(__tmp0) -> List['Connection']:
		with __tmp0._lock:
			return __tmp0.connections[:]

	def close(__tmp0, __tmp1) :
		with __tmp0._lock:
			for conn in __tmp0.connections:
				conn.close(__tmp1=__tmp1)


class Connection(object):
	def __tmp6(
		__tmp0,
		conn_list,
		event_loop: asyncio.AbstractEventLoop,
		ws: WebSocketServerProtocol = None,
		**extra_kwargs: <FILL>
	) -> None:
		__tmp0.extra = extra_kwargs
		__tmp0.ws: WebSocketServerProtocol = ws
		__tmp0.event_loop = event_loop
		__tmp0.conn_list = conn_list

		__tmp0.closed = False
		__tmp0._close_issued = False
		__tmp0._close_event = asyncio.Event(loop=__tmp0.event_loop)

		__tmp0.close_reason: Optional[str] = None
		__tmp0.close_code: Optional[int] = None
		__tmp0.in_pool = False

		__tmp0.conn_id = conn_list.generate_id()

		__tmp0._close_lock = threading.Lock()

		__tmp0.logger = g_logger.getChild(f'Connection:{__tmp0.conn_id}')
		__tmp0.logger.debug(f'Created connection {__tmp0!r}')

	@property
	def __tmp9(__tmp0) -> __typ0:
		return __tmp0._close_issued

	def __tmp12(__tmp0, subclassed_object: 'Connection') -> None:
		"""
		Copy contents of normal Connection object to subclass instance of Connection.
		:param subclassed_object:
		:return:
		"""
		if __tmp0.conn_list is not subclassed_object.conn_list:
			raise Exception('Cannot copy to sub-class of different router')

		for v in ('extra', 'ws', 'closed', 'in_pool', 'close_reason', 'close_code', 'conn_id', 'conn_list'):
			my_value = getattr(__tmp0, v)
			setattr(subclassed_object, v, my_value)

	def __tmp7(__tmp0) -> str:
		if __tmp0.ws:
			addr, port, *_ = __tmp0.ws.remote_address

			tags = [
				f'id:{__tmp0.conn_id}',
				f'remote:{addr}:{port}',
			]
		else:
			tags = [f'id:{__tmp0.conn_id}', 'broadcast']

		if __tmp0._close_issued:
			tags.append('closed')

		return 'Connection({})'.format(','.join(tags))

	def __tmp11(__tmp0) -> str:
		if __tmp0.ws:
			tags = [
				f'id:{__tmp0.conn_id}',
			]
		else:
			tags = [f'id:{__tmp0.conn_id}', 'broadcast']

		if __tmp0._close_issued:
			tags.append('closed')

		return 'Connection({})'.format(','.join(tags))

	def close(__tmp0, code: int = 1000, __tmp1: str = '') :
		with __tmp0._close_lock:
			if __tmp0._close_issued:
				__tmp0.logger.warning('Close already issued')
				return

			__tmp0._close_issued = True
			__tmp0.logger.debug('Issuing close')

		__tmp0.close_code = code or 1000
		__tmp0.close_reason = __tmp1 or ''

		async def __tmp10() -> __typ0:
			with __tmp0._close_lock:
				__tmp0._close_issued = True

			if __tmp0.closed:
				__tmp0.logger.warning('Close callback cancelled since already closed')
				return True

			if __tmp0.in_pool:
				__tmp0.conn_list.remove(__tmp0)

			try:
				await __tmp0.ws.close(code=__tmp0.close_code, __tmp1=__tmp0.close_reason)
			except websockets.InvalidState:  # Expected if connection closed first
				pass
			except Exception as e:
				__tmp0.logger.error(f'Exception while attempting to close connection: {e!r}')

			__tmp0._close_event.set()

			__tmp0.logger.debug(f'Closed with code {__tmp0.close_code} and reason {__tmp0.close_reason}')

			__tmp0.closed = True

			return True

		def __tmp4() -> None:
			__tmp0.logger.debug('Scheduling close callback')
			__tmp0.close_future = asyncio.ensure_future(__tmp10(), loop=__tmp0.event_loop)

		__tmp0.event_loop.call_soon_threadsafe(__tmp4)

	async def wait_closed(__tmp0) -> None:
		__tmp0.logger.debug('Waiting closed')
		await __tmp0._close_event.wait()
		__tmp0.logger.debug('Close arrived')


__all__ = [
	'ConnectionList',
	'Connection',
]
