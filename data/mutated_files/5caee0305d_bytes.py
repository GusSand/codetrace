from typing import TypeAlias
__typ6 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ9:
    def __tmp9(__tmp0, address: __typ6, datacenter: __typ6 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class __typ7:
    def __tmp9(__tmp0, address: __typ6, port: __typ0, tags: List[__typ6]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ3:
    def __tmp9(__tmp0, last_index, response: List[__typ7]):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ5(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ6(__typ0(obj.total_seconds())) + 's'
            else:
                return __typ6(obj.total_seconds() / 60) + 'm'

        return super(__typ5, __tmp0).default(obj)


class __typ4:
    def __tmp9(__tmp0, __tmp10: aiohttp.ClientSession, __tmp5: __typ6):
        __tmp0._client = __tmp10
        __tmp0._base_url = __tmp5

    async def register(__tmp0, __tmp4: __typ6,
                       __tmp1,
                       __tmp3: List[__typ6],
                       address: __typ6,
                       port: __typ0,
                       __tmp7: timedelta,
                       service_ttl: timedelta) -> None:

        data = json.dumps({'ID': __tmp4,
                           'Name': __tmp1,
                           'Tags': __tmp3,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp7,
                               'TTL': service_ttl}
                           }, __tmp6=__typ5)

        __tmp5 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp5, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp8(__tmp0, __tmp4: __typ6) -> None:
        __tmp5 = __tmp0._base_url + '/agent/service/deregister/' + __tmp4
        async with __tmp0._client.put(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp11(__tmp0, check_id: __typ6) -> None:
        __tmp5 = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp9(__tmp0, __tmp10: aiohttp.ClientSession, __tmp5: __typ6):
        __tmp0._client = __tmp10
        __tmp0._base_url = __tmp5

    async def create_or_update(__tmp0, key: __typ6, __tmp2: <FILL>) -> None:
        __tmp5 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.put(__tmp5, data=__tmp2) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp0, key: __typ6, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp5 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.get(__tmp5, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, key: __typ6) -> None:
        __tmp5 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.delete(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp9(__tmp0, __tmp10: aiohttp.ClientSession, __tmp5: __typ6):
        __tmp0._client = __tmp10
        __tmp0._base_url = __tmp5

    async def service(__tmp0, __tmp1: __typ6, index: __typ0, blocking_wait_time: timedelta) -> __typ3:
        __tmp5 = f'{__tmp0._base_url}/health/checks/{__tmp1}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(__tmp5, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp4 = response['ServiceID']
                address = __tmp4[(__tmp4.find('@') + 1):(__tmp4.find(':'))]
                port = __tmp4[(__tmp4.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ7(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time: timedelta):
        if time.total_seconds() < 60:
            return __typ6(__typ0(time.total_seconds())) + 's'
        else:
            return __typ6(time.total_seconds() / 60) + 'm'


class __typ8():
    def __tmp9(__tmp0):
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
    def health(__tmp0) -> __typ1:
        return __tmp0._health_endpoint

    @classmethod
    async def create(__tmp6, config: __typ9) -> 'ConsulClient':
        __tmp0 = __tmp6()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ4(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
