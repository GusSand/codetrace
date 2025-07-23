from typing import TypeAlias
__typ10 : TypeAlias = "bytes"
__typ7 : TypeAlias = "dict"
__typ0 : TypeAlias = "int"
__typ5 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ11:
    def __init__(__tmp0, address, datacenter: __typ5 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class __typ8:
    def __init__(__tmp0, address, port, tags: List[__typ5]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ3:
    def __init__(__tmp0, last_index, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ6(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ5(__typ0(obj.total_seconds())) + 's'
            else:
                return __typ5(obj.total_seconds() / 60) + 'm'

        return super(__typ6, __tmp0).default(obj)


class __typ4:
    def __init__(__tmp0, client, __tmp1):
        __tmp0._client = client
        __tmp0._base_url = __tmp1

    async def register(__tmp0, service_id,
                       cluster_name,
                       kinds,
                       address,
                       port: __typ0,
                       deregister_critical,
                       service_ttl: <FILL>) -> None:

        data = json.dumps({'ID': service_id,
                           'Name': cluster_name,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, cls=__typ6)

        __tmp1 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp1, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp0, service_id) -> None:
        __tmp1 = __tmp0._base_url + '/agent/service/deregister/' + service_id
        async with __tmp0._client.put(__tmp1) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, check_id) :
        __tmp1 = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(__tmp1) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __init__(__tmp0, client, __tmp1):
        __tmp0._client = client
        __tmp0._base_url = __tmp1

    async def create_or_update(__tmp0, key: __typ5, value) :
        __tmp1 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.put(__tmp1, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp0, key, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp1 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.get(__tmp1, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, key) :
        __tmp1 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.delete(__tmp1) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __init__(__tmp0, client, __tmp1: __typ5):
        __tmp0._client = client
        __tmp0._base_url = __tmp1

    async def service(__tmp0, cluster_name: __typ5, index, blocking_wait_time) :
        __tmp1 = f'{__tmp0._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(__tmp1, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                service_id = response['ServiceID']
                address = service_id[(service_id.find('@') + 1):(service_id.find(':'))]
                port = service_id[(service_id.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ8(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return __typ5(__typ0(time.total_seconds())) + 's'
        else:
            return __typ5(time.total_seconds() / 60) + 'm'


class __typ9():
    def __init__(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def service(__tmp0) -> __typ4:
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
        __tmp0._service_endpoint = __typ4(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
