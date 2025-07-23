from typing import TypeAlias
__typ7 : TypeAlias = "bytes"
__typ4 : TypeAlias = "dict"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ8:
    def __tmp4(__tmp0, address, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class __typ5:
    def __tmp4(__tmp0, address, port, tags: List[str]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class QueryResult:
    def __tmp4(__tmp0, last_index, response: List[__typ5]):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(__typ0(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(obj)


class __typ3:
    def __tmp4(__tmp0, client, __tmp2):
        __tmp0._client = client
        __tmp0._base_url = __tmp2

    async def register(__tmp0, __tmp1: str,
                       cluster_name,
                       kinds,
                       address: str,
                       port,
                       deregister_critical: timedelta,
                       service_ttl) -> None:

        data = json.dumps({'ID': __tmp1,
                           'Name': cluster_name,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, cls=DateTimeEncoder)

        __tmp2 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp2, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp0, __tmp1: str) -> None:
        __tmp2 = __tmp0._base_url + '/agent/service/deregister/' + __tmp1
        async with __tmp0._client.put(__tmp2) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, check_id: str) :
        __tmp2 = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(__tmp2) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp4(__tmp0, client: aiohttp.ClientSession, __tmp2):
        __tmp0._client = client
        __tmp0._base_url = __tmp2

    async def create_or_update(__tmp0, key: str, value: __typ7) :
        __tmp2 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.put(__tmp2, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp0, key: str, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp2 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.get(__tmp2, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, key: str) :
        __tmp2 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.delete(__tmp2) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp4(__tmp0, client, __tmp2: <FILL>):
        __tmp0._client = client
        __tmp0._base_url = __tmp2

    async def __tmp3(__tmp0, cluster_name, index: __typ0, blocking_wait_time) -> QueryResult:
        __tmp2 = f'{__tmp0._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(__tmp2, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp1 = response['ServiceID']
                address = __tmp1[(__tmp1.find('@') + 1):(__tmp1.find(':'))]
                port = __tmp1[(__tmp1.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ5(address, port, tags))
            return QueryResult(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ6():
    def __tmp4(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def __tmp3(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def key_value_storage(__tmp0) -> __typ2:
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def create(cls, config) :
        __tmp0 = cls()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ3(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
