from typing import TypeAlias
__typ6 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ7:
    def __tmp20(__tmp0, address, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class __typ4:
    def __tmp20(__tmp0, address: str, port: __typ0, tags: List[str]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ2:
    def __tmp20(__tmp0, last_index, response: List[__typ4]):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ3(json.JSONEncoder):
    def default(__tmp0, __tmp15):
        if isinstance(__tmp15, datetime.timedelta):
            if __tmp15.total_seconds() < 60:
                return str(__typ0(__tmp15.total_seconds())) + 's'
            else:
                return str(__tmp15.total_seconds() / 60) + 'm'

        return super(__typ3, __tmp0).default(__tmp15)


class ServiceEndpoint:
    def __tmp20(__tmp0, __tmp21: aiohttp.ClientSession, __tmp9: str):
        __tmp0._client = __tmp21
        __tmp0._base_url = __tmp9

    async def __tmp7(__tmp0, __tmp8,
                       __tmp14: str,
                       __tmp17: List[str],
                       address,
                       port: __typ0,
                       __tmp19: timedelta,
                       __tmp18: timedelta) -> None:

        data = json.dumps({'ID': __tmp8,
                           'Name': __tmp14,
                           'Tags': __tmp17,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp19,
                               'TTL': __tmp18}
                           }, __tmp10=__typ3)

        __tmp9 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp9, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp0, __tmp8: str) -> None:
        __tmp9 = __tmp0._base_url + '/agent/service/deregister/' + __tmp8
        async with __tmp0._client.put(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp23(__tmp0, __tmp1) -> None:
        __tmp9 = __tmp0._base_url + '/agent/check/pass/' + __tmp1
        async with __tmp0._client.put(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp20(__tmp0, __tmp21: aiohttp.ClientSession, __tmp9: str):
        __tmp0._client = __tmp21
        __tmp0._base_url = __tmp9

    async def __tmp5(__tmp0, __tmp4: str, __tmp16: __typ6) :
        __tmp9 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.put(__tmp9, data=__tmp16) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp3(__tmp0, __tmp4, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp9 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.get(__tmp9, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp4: <FILL>) -> None:
        __tmp9 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.delete(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp20(__tmp0, __tmp21: aiohttp.ClientSession, __tmp9: str):
        __tmp0._client = __tmp21
        __tmp0._base_url = __tmp9

    async def __tmp11(__tmp0, __tmp14: str, __tmp22: __typ0, __tmp13: timedelta) -> __typ2:
        __tmp9 = f'{__tmp0._base_url}/health/checks/{__tmp14}'
        params = {'index': __tmp22,
                  'wait': __tmp0.__convert_time(__tmp13)}

        async with __tmp0._client.get(__tmp9, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp8 = response['ServiceID']
                address = __tmp8[(__tmp8.find('@') + 1):(__tmp8.find(':'))]
                port = __tmp8[(__tmp8.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ4(address, port, tags))
            return __typ2(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time: timedelta):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ5():
    def __tmp20(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def __tmp11(__tmp0) -> ServiceEndpoint:
        return __tmp0._service_endpoint

    @property
    def __tmp24(__tmp0) -> KeyValueEndpoint:
        return __tmp0._key_value_endpoint

    @property
    def __tmp6(__tmp0) -> __typ1:
        return __tmp0._health_endpoint

    @classmethod
    async def __tmp12(__tmp10, config: __typ7) -> 'ConsulClient':
        __tmp0 = __tmp10()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = ServiceEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = KeyValueEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
