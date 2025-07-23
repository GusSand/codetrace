from typing import TypeAlias
__typ3 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ4:
    def __tmp19(__tmp0, address, datacenter: __typ3 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp19(__tmp0, address, port: int, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ0:
    def __tmp19(__tmp0, last_index: int, response: List[ServiceEntry]):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ2(json.JSONEncoder):
    def default(__tmp0, __tmp16):
        if isinstance(__tmp16, datetime.timedelta):
            if __tmp16.total_seconds() < 60:
                return __typ3(int(__tmp16.total_seconds())) + 's'
            else:
                return __typ3(__tmp16.total_seconds() / 60) + 'm'

        return super(__typ2, __tmp0).default(__tmp16)


class __typ1:
    def __tmp19(__tmp0, __tmp20: aiohttp.ClientSession, __tmp10: __typ3):
        __tmp0._client = __tmp20
        __tmp0._base_url = __tmp10

    async def __tmp8(__tmp0, __tmp9,
                       __tmp15,
                       kinds,
                       address: __typ3,
                       port: <FILL>,
                       deregister_critical,
                       __tmp18) :

        data = json.dumps({'ID': __tmp9,
                           'Name': __tmp15,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': __tmp18}
                           }, __tmp11=__typ2)

        __tmp10 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp10, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp0, __tmp9) :
        __tmp10 = __tmp0._base_url + '/agent/service/deregister/' + __tmp9
        async with __tmp0._client.put(__tmp10) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp21(__tmp0, __tmp1) :
        __tmp10 = __tmp0._base_url + '/agent/check/pass/' + __tmp1
        async with __tmp0._client.put(__tmp10) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp19(__tmp0, __tmp20: aiohttp.ClientSession, __tmp10):
        __tmp0._client = __tmp20
        __tmp0._base_url = __tmp10

    async def __tmp6(__tmp0, __tmp4, __tmp17: bytes) -> None:
        __tmp10 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.put(__tmp10, data=__tmp17) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp5(__tmp0, __tmp4: __typ3, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp10 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.get(__tmp10, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp4) -> None:
        __tmp10 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.delete(__tmp10) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp19(__tmp0, __tmp20: aiohttp.ClientSession, __tmp10):
        __tmp0._client = __tmp20
        __tmp0._base_url = __tmp10

    async def __tmp12(__tmp0, __tmp15, index, __tmp14) -> __typ0:
        __tmp10 = f'{__tmp0._base_url}/health/checks/{__tmp15}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(__tmp14)}

        async with __tmp0._client.get(__tmp10, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp9 = response['ServiceID']
                address = __tmp9[(__tmp9.find('@') + 1):(__tmp9.find(':'))]
                port = __tmp9[(__tmp9.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ0(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return __typ3(int(time.total_seconds())) + 's'
        else:
            return __typ3(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp19(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def __tmp12(__tmp0) -> __typ1:
        return __tmp0._service_endpoint

    @property
    def __tmp22(__tmp0) -> KeyValueEndpoint:
        return __tmp0._key_value_endpoint

    @property
    def __tmp7(__tmp0) -> HealthEndpoint:
        return __tmp0._health_endpoint

    @classmethod
    async def __tmp13(__tmp11, __tmp3) :
        __tmp0 = __tmp11()
        __tmp0._base_url = f'{__tmp3.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = KeyValueEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = HealthEndpoint(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
