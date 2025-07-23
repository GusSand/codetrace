from typing import TypeAlias
__typ0 : TypeAlias = "Client"
from asyncio import sleep as async_sleep
import asyncio
import pytest
from typing import *

from webswitch.router.errors import RouterError
from webswitch.client import Client, ResponseException, ResponseTimeoutException
from webswitch.channel_server import Conversation, add_action, ChannelClient

from .common import *


class ClientTestingServer(ChannelServerBase):
	@add_action(params={'arg': str})
	async def __tmp8(__tmp0, __tmp13, client: 'ChannelClient', convo: <FILL>) -> None:

		response = await convo.send_and_recv({'foo1': f'You said {__tmp13}', 'foo2': f'is {__tmp13}'})

		__tmp13 = response.get('arg')

		assert __tmp13, 'arg was not in response'
		assert __tmp13 == 'ok', 'response was not "ok"'

		response = await convo.send_and_recv({'data': 'What is 2+2?'}, expect_params={'arg': int})

		__tmp13 = response.get('arg')

		assert __tmp13 == 4, 'Incorrect response'

	@add_action()
	async def __tmp10(__tmp0, client: 'ChannelClient', convo: Conversation) :
		raise RouterError(error_types='foo', message='something happened!')

	@add_action(params={'timeout': float})
	async def __tmp4(__tmp0, timeout: float, client: 'ChannelClient', convo) -> None:
		await async_sleep(timeout)
		await convo.send({'data': 'all done!'})


@pytest.fixture(name='get_server', scope='function')
def get_server_fixture(__tmp3) :
	def func() :
		return ClientTestingServer(__tmp3)

	return func


@pytest.mark.asyncio
async def __tmp5(__tmp1: __typ0) -> None:
	convo = __tmp1.convo('whoami')

	reply = await convo.send_and_expect({})

	my_id = reply.data.get('id')

	assert my_id, 'Did not receive an ID from whoami'
	assert isinstance(my_id, int), 'Is not int'


@pytest.mark.asyncio
async def test_async_raise(__tmp1: __typ0) :
	convo = __tmp1.convo('async_raise')

	with pytest.raises(ResponseException) as excinfo:
		await convo.send_and_expect({})

	assert 'foo' in excinfo.value.error_types


@pytest.mark.asyncio
async def __tmp11(__tmp1) :
	convo = __tmp1.convo('test_conversation')
	response = await convo.send_and_expect({'arg': 'yo'})

	assert response.data.get('foo1') == 'You said yo'
	assert response.data.get('foo2') == 'is yo'

	response = await convo.send_and_expect({'arg': 'ok'})

	assert response.data.get('data') == 'What is 2+2?'

	await convo.send(data=dict(__tmp13=4))


@pytest.mark.asyncio
async def __tmp6(__tmp1) :
	convo = __tmp1.convo('client_timeout_test')

	with pytest.raises(ResponseTimeoutException) as excinfo:
		await convo.send_and_expect({'timeout': 0.2}, timeout=0.1)

@pytest.mark.asyncio
async def test_unknown_action(__tmp1) -> None:
	convo = __tmp1.convo('this_action_is_fake')

	with pytest.raises(ResponseException) as excinfo:
		await convo.send_and_expect({})

	assert excinfo.match('Invalid action')


@pytest.mark.parametrize("count", [10, 5])
@pytest.mark.asyncio
async def __tmp9(count: int, __tmp12: Callable[[], __typ0], __tmp7) :
	with __tmp7() as server:
		clients = []

		for i in range(count):
			clients.append(__tmp12())

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
async def __tmp2(__tmp12, __tmp7) -> None:
	with __tmp7():
		async with __tmp12() as client1, __tmp12() as client2:
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
