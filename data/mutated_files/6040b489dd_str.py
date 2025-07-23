from typing import TypeAlias
__typ4 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ5:
    def __tmp13(__tmp2, address: str, datacenter: str = 'dc1'):
        __tmp2.address = address
        __tmp2.datacenter = datacenter


class __typ3:
    def __tmp13(__tmp2, address: <FILL>, port: __typ0, tags: List[str]):
        __tmp2.address = address
        __tmp2.port = port
        __tmp2.tags = tags


class __typ1:
    def __tmp13(__tmp2, last_index: __typ0, response: List[__typ3]):
        __tmp2.last_index = last_index
        __tmp2.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp2, __tmp4):
        if isinstance(__tmp4, datetime.timedelta):
            if __tmp4.total_seconds() < 60:
                return str(__typ0(__tmp4.total_seconds())) + 's'
            else:
                return str(__tmp4.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp2).default(__tmp4)


class __typ2:
    def __tmp13(__tmp2, __tmp14, __tmp9: str):
        __tmp2._client = __tmp14
        __tmp2._base_url = __tmp9

    async def register(__tmp2, __tmp7: str,
                       __tmp3,
                       __tmp6,
                       address: str,
                       port,
                       deregister_critical: timedelta,
                       __tmp8: timedelta) -> None:

        data = json.dumps({'ID': __tmp7,
                           'Name': __tmp3,
                           'Tags': __tmp6,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': __tmp8}
                           }, __tmp10=DateTimeEncoder)

        __tmp9 = __tmp2._base_url + '/agent/service/register'
        async with __tmp2._client.put(__tmp9, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp12(__tmp2, __tmp7: str) :
        __tmp9 = __tmp2._base_url + '/agent/service/deregister/' + __tmp7
        async with __tmp2._client.put(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp2, check_id: str) :
        __tmp9 = __tmp2._base_url + '/agent/check/pass/' + check_id
        async with __tmp2._client.put(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp13(__tmp2, __tmp14, __tmp9):
        __tmp2._client = __tmp14
        __tmp2._base_url = __tmp9

    async def __tmp5(__tmp2, key: str, value: __typ4) -> None:
        __tmp9 = __tmp2._base_url + '/kv/' + key
        async with __tmp2._client.put(__tmp9, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp2, key: str, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp9 = __tmp2._base_url + '/kv/' + key
        async with __tmp2._client.get(__tmp9, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp2, key: str) -> None:
        __tmp9 = __tmp2._base_url + '/kv/' + key
        async with __tmp2._client.delete(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp13(__tmp2, __tmp14: aiohttp.ClientSession, __tmp9: str):
        __tmp2._client = __tmp14
        __tmp2._base_url = __tmp9

    async def __tmp11(__tmp2, __tmp3: str, index: __typ0, __tmp1) -> __typ1:
        __tmp9 = f'{__tmp2._base_url}/health/checks/{__tmp3}'
        params = {'index': index,
                  'wait': __tmp2.__convert_time(__tmp1)}

        async with __tmp2._client.get(__tmp9, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp7 = response['ServiceID']
                address = __tmp7[(__tmp7.find('@') + 1):(__tmp7.find(':'))]
                port = __tmp7[(__tmp7.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ3(address, port, tags))
            return __typ1(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp2, time: timedelta):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp13(__tmp2):
        __tmp2._client = None
        __tmp2._base_url = None
        __tmp2._service_endpoint = None
        __tmp2._key_value_endpoint = None
        __tmp2._health_endpoint = None

    @property
    def __tmp11(__tmp2) -> __typ2:
        return __tmp2._service_endpoint

    @property
    def __tmp16(__tmp2) :
        return __tmp2._key_value_endpoint

    @property
    def __tmp0(__tmp2) -> HealthEndpoint:
        return __tmp2._health_endpoint

    @classmethod
    async def __tmp15(__tmp10, config: __typ5) -> 'ConsulClient':
        __tmp2 = __tmp10()
        __tmp2._base_url = f'{config.address}/v1/'
        __tmp2._client = aiohttp.ClientSession()
        __tmp2._service_endpoint = __typ2(__tmp2._client, __tmp2._base_url)
        __tmp2._key_value_endpoint = KeyValueEndpoint(__tmp2._client, __tmp2._base_url)
        __tmp2._health_endpoint = HealthEndpoint(__tmp2._client, __tmp2._base_url)
        return __tmp2

    async def close(__tmp2):
        await __tmp2._client.close()
