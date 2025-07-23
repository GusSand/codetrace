from typing import TypeAlias
__typ1 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp11(__tmp1, address: __typ1, datacenter: __typ1 = 'dc1'):
        __tmp1.address = address
        __tmp1.datacenter = datacenter


class ServiceEntry:
    def __tmp11(__tmp1, address: __typ1, port: int, tags: List[__typ1]):
        __tmp1.address = address
        __tmp1.port = port
        __tmp1.tags = tags


class QueryResult:
    def __tmp11(__tmp1, last_index: int, response: List[ServiceEntry]):
        __tmp1.last_index = last_index
        __tmp1.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp1, __tmp4):
        if isinstance(__tmp4, datetime.timedelta):
            if __tmp4.total_seconds() < 60:
                return __typ1(int(__tmp4.total_seconds())) + 's'
            else:
                return __typ1(__tmp4.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp1).default(__tmp4)


class __typ0:
    def __tmp11(__tmp1, __tmp14: aiohttp.ClientSession, __tmp7: __typ1):
        __tmp1._client = __tmp14
        __tmp1._base_url = __tmp7

    async def __tmp3(__tmp1, __tmp6: __typ1,
                       __tmp2: __typ1,
                       kinds: List[__typ1],
                       address: __typ1,
                       port: int,
                       __tmp9: timedelta,
                       service_ttl: timedelta) -> None:

        data = json.dumps({'ID': __tmp6,
                           'Name': __tmp2,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp9,
                               'TTL': service_ttl}
                           }, cls=DateTimeEncoder)

        __tmp7 = __tmp1._base_url + '/agent/service/register'
        async with __tmp1._client.put(__tmp7, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp10(__tmp1, __tmp6: __typ1) -> None:
        __tmp7 = __tmp1._base_url + '/agent/service/deregister/' + __tmp6
        async with __tmp1._client.put(__tmp7) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp5(__tmp1, __tmp13: __typ1) -> None:
        __tmp7 = __tmp1._base_url + '/agent/check/pass/' + __tmp13
        async with __tmp1._client.put(__tmp7) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp11(__tmp1, __tmp14: aiohttp.ClientSession, __tmp7: __typ1):
        __tmp1._client = __tmp14
        __tmp1._base_url = __tmp7

    async def create_or_update(__tmp1, __tmp15: __typ1, value: bytes) -> None:
        __tmp7 = __tmp1._base_url + '/kv/' + __tmp15
        async with __tmp1._client.put(__tmp7, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp1, __tmp15, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp7 = __tmp1._base_url + '/kv/' + __tmp15
        async with __tmp1._client.get(__tmp7, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp1, __tmp15: __typ1) -> None:
        __tmp7 = __tmp1._base_url + '/kv/' + __tmp15
        async with __tmp1._client.delete(__tmp7) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp11(__tmp1, __tmp14: aiohttp.ClientSession, __tmp7: __typ1):
        __tmp1._client = __tmp14
        __tmp1._base_url = __tmp7

    async def __tmp8(__tmp1, __tmp2, __tmp16: int, __tmp0: timedelta) -> QueryResult:
        __tmp7 = f'{__tmp1._base_url}/health/checks/{__tmp2}'
        params = {'index': __tmp16,
                  'wait': __tmp1.__convert_time(__tmp0)}

        async with __tmp1._client.get(__tmp7, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp6 = response['ServiceID']
                address = __tmp6[(__tmp6.find('@') + 1):(__tmp6.find(':'))]
                port = __tmp6[(__tmp6.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return QueryResult(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp1, time: <FILL>):
        if time.total_seconds() < 60:
            return __typ1(int(time.total_seconds())) + 's'
        else:
            return __typ1(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp11(__tmp1):
        __tmp1._client = None
        __tmp1._base_url = None
        __tmp1._service_endpoint = None
        __tmp1._key_value_endpoint = None
        __tmp1._health_endpoint = None

    @property
    def __tmp8(__tmp1) -> __typ0:
        return __tmp1._service_endpoint

    @property
    def __tmp17(__tmp1) -> KeyValueEndpoint:
        return __tmp1._key_value_endpoint

    @property
    def health(__tmp1) :
        return __tmp1._health_endpoint

    @classmethod
    async def create(cls, __tmp12: ConsulClientConfiguration) -> 'ConsulClient':
        __tmp1 = cls()
        __tmp1._base_url = f'{__tmp12.address}/v1/'
        __tmp1._client = aiohttp.ClientSession()
        __tmp1._service_endpoint = __typ0(__tmp1._client, __tmp1._base_url)
        __tmp1._key_value_endpoint = KeyValueEndpoint(__tmp1._client, __tmp1._base_url)
        __tmp1._health_endpoint = HealthEndpoint(__tmp1._client, __tmp1._base_url)
        return __tmp1

    async def close(__tmp1):
        await __tmp1._client.close()
