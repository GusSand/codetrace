from typing import TypeAlias
__typ4 : TypeAlias = "dict"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp16(__tmp0, address: str, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp16(__tmp0, address: str, port, tags: List[str]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ3:
    def __tmp16(__tmp0, last_index, response: List[ServiceEntry]):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, __tmp12):
        if isinstance(__tmp12, datetime.timedelta):
            if __tmp12.total_seconds() < 60:
                return str(__typ0(__tmp12.total_seconds())) + 's'
            else:
                return str(__tmp12.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(__tmp12)


class ServiceEndpoint:
    def __tmp16(__tmp0, __tmp17: aiohttp.ClientSession, __tmp8: str):
        __tmp0._client = __tmp17
        __tmp0._base_url = __tmp8

    async def __tmp6(__tmp0, __tmp7: str,
                       __tmp11,
                       __tmp14: List[str],
                       address: str,
                       port: __typ0,
                       __tmp15: timedelta,
                       service_ttl: timedelta) -> None:

        data = json.dumps({'ID': __tmp7,
                           'Name': __tmp11,
                           'Tags': __tmp14,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp15,
                               'TTL': service_ttl}
                           }, cls=DateTimeEncoder)

        __tmp8 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp8, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp0, __tmp7: <FILL>) -> None:
        __tmp8 = __tmp0._base_url + '/agent/service/deregister/' + __tmp7
        async with __tmp0._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, check_id: str) -> None:
        __tmp8 = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp16(__tmp0, __tmp17, __tmp8: str):
        __tmp0._client = __tmp17
        __tmp0._base_url = __tmp8

    async def __tmp4(__tmp0, __tmp3: str, __tmp13: bytes) :
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp3
        async with __tmp0._client.put(__tmp8, data=__tmp13) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp0, __tmp3: str, recurse=True) -> __typ4:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp3
        async with __tmp0._client.get(__tmp8, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp3: str) -> None:
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp3
        async with __tmp0._client.delete(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp16(__tmp0, __tmp17, __tmp8):
        __tmp0._client = __tmp17
        __tmp0._base_url = __tmp8

    async def __tmp9(__tmp0, __tmp11, __tmp18: __typ0, __tmp10: timedelta) -> __typ3:
        __tmp8 = f'{__tmp0._base_url}/health/checks/{__tmp11}'
        params = {'index': __tmp18,
                  'wait': __tmp0.__convert_time(__tmp10)}

        async with __tmp0._client.get(__tmp8, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp7 = response['ServiceID']
                address = __tmp7[(__tmp7.find('@') + 1):(__tmp7.find(':'))]
                port = __tmp7[(__tmp7.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time: timedelta):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp16(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def __tmp9(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def __tmp19(__tmp0) -> __typ2:
        return __tmp0._key_value_endpoint

    @property
    def __tmp5(__tmp0) -> __typ1:
        return __tmp0._health_endpoint

    @classmethod
    async def create(cls, __tmp1) -> 'ConsulClient':
        __tmp0 = cls()
        __tmp0._base_url = f'{__tmp1.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = ServiceEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
