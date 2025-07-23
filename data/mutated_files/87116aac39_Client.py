from typing import TypeAlias
__typ3 : TypeAlias = "float"
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "Conversation"
__typ0 : TypeAlias = "int"
from asyncio import sleep as async_sleep
import asyncio
import pytest
from typing import *

from webswitch.router.errors import RouterError
from webswitch.client import Client, ResponseException, ResponseTimeoutException
from webswitch.channel_server import Conversation, add_action, ChannelClient

from .common import *


class __typ4(ChannelServerBase):
	@add_action(params={'arg': __typ2})
	async def __tmp8(__tmp0, __tmp18: __typ2, client: 'ChannelClient', convo) -> None:

		response = await convo.send_and_recv({'foo1': f'You said {__tmp18}', 'foo2': f'is {__tmp18}'})

		__tmp18 = response.get('arg')

		assert __tmp18, 'arg was not in response'
		assert __tmp18 == 'ok', 'response was not "ok"'

		response = await convo.send_and_recv({'data': 'What is 2+2?'}, expect_params={'arg': __typ0})

		__tmp18 = response.get('arg')

		assert __tmp18 == 4, 'Incorrect response'

	@add_action()
	async def __tmp9(__tmp0, client: 'ChannelClient', convo: __typ1) -> None:
		raise RouterError(error_types='foo', message='something happened!')

	@add_action(params={'timeout': __typ3})
	async def __tmp2(__tmp0, __tmp17: __typ3, client: 'ChannelClient', convo: __typ1) -> None:
		await async_sleep(__tmp17)
		await convo.send({'data': 'all done!'})


@pytest.fixture(name='get_server', scope='function')
def __tmp10(__tmp5: __typ0) -> Callable[[], __typ4]:
	def __tmp15() -> __typ4:
		return __typ4(__tmp5)

	return __tmp15


@pytest.mark.asyncio
async def __tmp13(__tmp1: Client) -> None:
	convo = __tmp1.convo('whoami')

	reply = await convo.send_and_expect({})

	my_id = reply.data.get('id')

	assert my_id, 'Did not receive an ID from whoami'
	assert isinstance(my_id, __typ0), 'Is not int'


@pytest.mark.asyncio
async def test_async_raise(__tmp1: Client) -> None:
	convo = __tmp1.convo('async_raise')

	with pytest.raises(ResponseException) as excinfo:
		await convo.send_and_expect({})

	assert 'foo' in excinfo.value.error_types


@pytest.mark.asyncio
async def __tmp4(__tmp1: Client) -> None:
	convo = __tmp1.convo('test_conversation')
	response = await convo.send_and_expect({'arg': 'yo'})

	assert response.data.get('foo1') == 'You said yo'
	assert response.data.get('foo2') == 'is yo'

	response = await convo.send_and_expect({'arg': 'ok'})

	assert response.data.get('data') == 'What is 2+2?'

	await convo.send(data=dict(__tmp18=4))


@pytest.mark.asyncio
async def __tmp14(__tmp1: Client) -> None:
	convo = __tmp1.convo('client_timeout_test')

	with pytest.raises(ResponseTimeoutException) as excinfo:
		await convo.send_and_expect({'timeout': 0.2}, __tmp17=0.1)

@pytest.mark.asyncio
async def __tmp7(__tmp1: <FILL>) :
	convo = __tmp1.convo('this_action_is_fake')

	with pytest.raises(ResponseException) as excinfo:
		await convo.send_and_expect({})

	assert excinfo.match('Invalid action')


@pytest.mark.parametrize("count", [10, 5])
@pytest.mark.asyncio
async def __tmp6(__tmp16, __tmp11: Callable[[], Client], __tmp3: Callable[[], __typ4]) -> None:
	with __tmp3() as server:
		clients = []

		for i in range(__tmp16):
			clients.append(__tmp11())

		await asyncio.gather(*(c.__aenter__() for c in clients))

		collected_ids = set()

		for client in clients:
			message = await client.convo('whoami').send_and_expect({})
			assert 'id' in message.data
			collected_ids.add(message.data['id'])

		client1 = clients[0]

		message = await client1.convo('enum_clients').send_and_expect({})

		await asyncio.gather(*(c.__aexit__(None, None, None) for c in clients))

		data = message.data

		assert isinstance(data, dict)
		assert 'client_ids' in data
		assert isinstance(data['client_ids'], list)

		enum_ids = set(data['client_ids'])

		assert enum_ids == collected_ids


@pytest.mark.asyncio
async def __tmp12(__tmp11, __tmp3: Callable[[], __typ4]) -> None:
	with __tmp3():
		async with __tmp11() as client1, __tmp11() as client2:
			await client1.convo('send').send({
				'targets': [client2.client_id],
				'data': {'msg': 'yo'}
			})

			response = await client2.convo(None).expect(2.0)

			assert response.data.get('msg') == 'yo'
			assert response.data.get('sender_id') == client1.client_id

# TODO: Test active source cancelling
# TODO: On both Client- and Channel-side, should register all timeouts so that upon server close
# TODO: all pending timeouts are cancelled
