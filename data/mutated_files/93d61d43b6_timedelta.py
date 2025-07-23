from typing import TypeAlias
__typ2 : TypeAlias = "int"
__typ0 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ3:
    def __tmp8(__tmp2, address: __typ0, datacenter: __typ0 = 'dc1'):
        __tmp2.address = address
        __tmp2.datacenter = datacenter


class __typ1:
    def __tmp8(__tmp2, address: __typ0, port: __typ2, tags: List[__typ0]):
        __tmp2.address = address
        __tmp2.port = port
        __tmp2.tags = tags


class QueryResult:
    def __tmp8(__tmp2, last_index: __typ2, response: List[__typ1]):
        __tmp2.last_index = last_index
        __tmp2.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp2, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ0(__typ2(obj.total_seconds())) + 's'
            else:
                return __typ0(obj.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp2).default(obj)


class ServiceEndpoint:
    def __tmp8(__tmp2, __tmp9: aiohttp.ClientSession, __tmp4: __typ0):
        __tmp2._client = __tmp9
        __tmp2._base_url = __tmp4

    async def register(__tmp2, __tmp3: __typ0,
                       cluster_name: __typ0,
                       kinds: List[__typ0],
                       address: __typ0,
                       port,
                       __tmp6: timedelta,
                       service_ttl: <FILL>) -> None:

        data = json.dumps({'ID': __tmp3,
                           'Name': cluster_name,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp6,
                               'TTL': service_ttl}
                           }, cls=DateTimeEncoder)

        __tmp4 = __tmp2._base_url + '/agent/service/register'
        async with __tmp2._client.put(__tmp4, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp7(__tmp2, __tmp3: __typ0) -> None:
        __tmp4 = __tmp2._base_url + '/agent/service/deregister/' + __tmp3
        async with __tmp2._client.put(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp2, check_id: __typ0) -> None:
        __tmp4 = __tmp2._base_url + '/agent/check/pass/' + check_id
        async with __tmp2._client.put(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp8(__tmp2, __tmp9: aiohttp.ClientSession, __tmp4: __typ0):
        __tmp2._client = __tmp9
        __tmp2._base_url = __tmp4

    async def create_or_update(__tmp2, key: __typ0, value: bytes) -> None:
        __tmp4 = __tmp2._base_url + '/kv/' + key
        async with __tmp2._client.put(__tmp4, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp2, key: __typ0, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp4 = __tmp2._base_url + '/kv/' + key
        async with __tmp2._client.get(__tmp4, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp2, key: __typ0) -> None:
        __tmp4 = __tmp2._base_url + '/kv/' + key
        async with __tmp2._client.delete(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp8(__tmp2, __tmp9: aiohttp.ClientSession, __tmp4: __typ0):
        __tmp2._client = __tmp9
        __tmp2._base_url = __tmp4

    async def __tmp5(__tmp2, cluster_name: __typ0, __tmp10: __typ2, __tmp1: timedelta) -> QueryResult:
        __tmp4 = f'{__tmp2._base_url}/health/checks/{cluster_name}'
        params = {'index': __tmp10,
                  'wait': __tmp2.__convert_time(__tmp1)}

        async with __tmp2._client.get(__tmp4, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp3 = response['ServiceID']
                address = __tmp3[(__tmp3.find('@') + 1):(__tmp3.find(':'))]
                port = __tmp3[(__tmp3.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ1(address, port, tags))
            return QueryResult(__typ2(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp2, time: timedelta):
        if time.total_seconds() < 60:
            return __typ0(__typ2(time.total_seconds())) + 's'
        else:
            return __typ0(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp8(__tmp2):
        __tmp2._client = None
        __tmp2._base_url = None
        __tmp2._service_endpoint = None
        __tmp2._key_value_endpoint = None
        __tmp2._health_endpoint = None

    @property
    def __tmp5(__tmp2) -> ServiceEndpoint:
        return __tmp2._service_endpoint

    @property
    def key_value_storage(__tmp2) :
        return __tmp2._key_value_endpoint

    @property
    def __tmp0(__tmp2) -> HealthEndpoint:
        return __tmp2._health_endpoint

    @classmethod
    async def create(cls, config: __typ3) -> 'ConsulClient':
        __tmp2 = cls()
        __tmp2._base_url = f'{config.address}/v1/'
        __tmp2._client = aiohttp.ClientSession()
        __tmp2._service_endpoint = ServiceEndpoint(__tmp2._client, __tmp2._base_url)
        __tmp2._key_value_endpoint = KeyValueEndpoint(__tmp2._client, __tmp2._base_url)
        __tmp2._health_endpoint = HealthEndpoint(__tmp2._client, __tmp2._base_url)
        return __tmp2

    async def close(__tmp2):
        await __tmp2._client.close()
