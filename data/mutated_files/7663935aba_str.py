from typing import TypeAlias
__typ5 : TypeAlias = "dict"
__typ8 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ9:
    def __tmp21(__tmp0, address: str, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class __typ6:
    def __tmp21(__tmp0, address: str, port: __typ0, tags: List[str]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ3:
    def __tmp21(__tmp0, last_index: __typ0, response: List[__typ6]):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, __tmp16):
        if isinstance(__tmp16, datetime.timedelta):
            if __tmp16.total_seconds() < 60:
                return str(__typ0(__tmp16.total_seconds())) + 's'
            else:
                return str(__tmp16.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(__tmp16)


class __typ4:
    def __tmp21(__tmp0, __tmp22: aiohttp.ClientSession, __tmp10: str):
        __tmp0._client = __tmp22
        __tmp0._base_url = __tmp10

    async def __tmp8(__tmp0, __tmp9: str,
                       __tmp15: str,
                       __tmp18: List[str],
                       address,
                       port: __typ0,
                       __tmp20,
                       __tmp19: timedelta) -> None:

        data = json.dumps({'ID': __tmp9,
                           'Name': __tmp15,
                           'Tags': __tmp18,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp20,
                               'TTL': __tmp19}
                           }, __tmp11=DateTimeEncoder)

        __tmp10 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp10, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp0, __tmp9: str) :
        __tmp10 = __tmp0._base_url + '/agent/service/deregister/' + __tmp9
        async with __tmp0._client.put(__tmp10) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp24(__tmp0, __tmp1: str) -> None:
        __tmp10 = __tmp0._base_url + '/agent/check/pass/' + __tmp1
        async with __tmp0._client.put(__tmp10) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp21(__tmp0, __tmp22: aiohttp.ClientSession, __tmp10: str):
        __tmp0._client = __tmp22
        __tmp0._base_url = __tmp10

    async def __tmp6(__tmp0, __tmp4, __tmp17: __typ8) -> None:
        __tmp10 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.put(__tmp10, data=__tmp17) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp5(__tmp0, __tmp4: <FILL>, recurse=True) -> __typ5:
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


class __typ1():
    def __tmp21(__tmp0, __tmp22, __tmp10):
        __tmp0._client = __tmp22
        __tmp0._base_url = __tmp10

    async def __tmp12(__tmp0, __tmp15: str, __tmp23: __typ0, __tmp14: timedelta) -> __typ3:
        __tmp10 = f'{__tmp0._base_url}/health/checks/{__tmp15}'
        params = {'index': __tmp23,
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
                statuses.append(__typ6(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ7():
    def __tmp21(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def __tmp12(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def __tmp25(__tmp0) -> __typ2:
        return __tmp0._key_value_endpoint

    @property
    def __tmp7(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def __tmp13(__tmp11, __tmp3: __typ9) -> 'ConsulClient':
        __tmp0 = __tmp11()
        __tmp0._base_url = f'{__tmp3.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ4(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
