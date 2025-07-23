from typing import TypeAlias
__typ9 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
__typ5 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ10:
    def __tmp16(__tmp0, address: __typ5, datacenter: __typ5 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class __typ7:
    def __tmp16(__tmp0, address: __typ5, port: __typ0, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ3:
    def __tmp16(__tmp0, last_index: __typ0, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ6(json.JSONEncoder):
    def default(__tmp0, __tmp13):
        if isinstance(__tmp13, datetime.timedelta):
            if __tmp13.total_seconds() < 60:
                return __typ5(__typ0(__tmp13.total_seconds())) + 's'
            else:
                return __typ5(__tmp13.total_seconds() / 60) + 'm'

        return super(__typ6, __tmp0).default(__tmp13)


class __typ4:
    def __tmp16(__tmp0, __tmp17: aiohttp.ClientSession, __tmp9):
        __tmp0._client = __tmp17
        __tmp0._base_url = __tmp9

    async def __tmp7(__tmp0, __tmp8: __typ5,
                       __tmp12,
                       kinds: List[__typ5],
                       address: __typ5,
                       port,
                       __tmp15: timedelta,
                       __tmp14: timedelta) -> None:

        data = json.dumps({'ID': __tmp8,
                           'Name': __tmp12,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp15,
                               'TTL': __tmp14}
                           }, cls=__typ6)

        __tmp9 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp9, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp0, __tmp8: __typ5) :
        __tmp9 = __tmp0._base_url + '/agent/service/deregister/' + __tmp8
        async with __tmp0._client.put(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp19(__tmp0, __tmp1: __typ5) :
        __tmp9 = __tmp0._base_url + '/agent/check/pass/' + __tmp1
        async with __tmp0._client.put(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp16(__tmp0, __tmp17, __tmp9: __typ5):
        __tmp0._client = __tmp17
        __tmp0._base_url = __tmp9

    async def __tmp6(__tmp0, __tmp4: __typ5, value: __typ9) -> None:
        __tmp9 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.put(__tmp9, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp5(__tmp0, __tmp4, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp9 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.get(__tmp9, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp4) -> None:
        __tmp9 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.delete(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp16(__tmp0, __tmp17: aiohttp.ClientSession, __tmp9: __typ5):
        __tmp0._client = __tmp17
        __tmp0._base_url = __tmp9

    async def service(__tmp0, __tmp12: __typ5, __tmp18: __typ0, __tmp11: <FILL>) -> __typ3:
        __tmp9 = f'{__tmp0._base_url}/health/checks/{__tmp12}'
        params = {'index': __tmp18,
                  'wait': __tmp0.__convert_time(__tmp11)}

        async with __tmp0._client.get(__tmp9, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp8 = response['ServiceID']
                address = __tmp8[(__tmp8.find('@') + 1):(__tmp8.find(':'))]
                port = __tmp8[(__tmp8.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ7(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time: timedelta):
        if time.total_seconds() < 60:
            return __typ5(__typ0(time.total_seconds())) + 's'
        else:
            return __typ5(time.total_seconds() / 60) + 'm'


class __typ8():
    def __tmp16(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def service(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def key_value_storage(__tmp0) :
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) -> __typ1:
        return __tmp0._health_endpoint

    @classmethod
    async def __tmp10(cls, __tmp3) :
        __tmp0 = cls()
        __tmp0._base_url = f'{__tmp3.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ4(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
