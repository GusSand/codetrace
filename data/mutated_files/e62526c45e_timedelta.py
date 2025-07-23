from typing import TypeAlias
__typ8 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
__typ5 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ9:
    def __tmp17(__tmp0, address, datacenter: __typ5 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class __typ6:
    def __tmp17(__tmp0, address, port, tags: List[__typ5]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ3:
    def __tmp17(__tmp0, last_index, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, __tmp12):
        if isinstance(__tmp12, datetime.timedelta):
            if __tmp12.total_seconds() < 60:
                return __typ5(__typ0(__tmp12.total_seconds())) + 's'
            else:
                return __typ5(__tmp12.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(__tmp12)


class __typ4:
    def __tmp17(__tmp0, __tmp18, __tmp8):
        __tmp0._client = __tmp18
        __tmp0._base_url = __tmp8

    async def __tmp6(__tmp0, __tmp7,
                       __tmp11: __typ5,
                       __tmp14,
                       address,
                       port,
                       __tmp16,
                       __tmp15) :

        data = json.dumps({'ID': __tmp7,
                           'Name': __tmp11,
                           'Tags': __tmp14,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp16,
                               'TTL': __tmp15}
                           }, __tmp9=DateTimeEncoder)

        __tmp8 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp8, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp0, __tmp7) :
        __tmp8 = __tmp0._base_url + '/agent/service/deregister/' + __tmp7
        async with __tmp0._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, __tmp1: __typ5) :
        __tmp8 = __tmp0._base_url + '/agent/check/pass/' + __tmp1
        async with __tmp0._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp17(__tmp0, __tmp18, __tmp8):
        __tmp0._client = __tmp18
        __tmp0._base_url = __tmp8

    async def __tmp5(__tmp0, __tmp3, __tmp13: __typ8) :
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp3
        async with __tmp0._client.put(__tmp8, data=__tmp13) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp4(__tmp0, __tmp3, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp3
        async with __tmp0._client.get(__tmp8, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp3) :
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp3
        async with __tmp0._client.delete(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp17(__tmp0, __tmp18: aiohttp.ClientSession, __tmp8: __typ5):
        __tmp0._client = __tmp18
        __tmp0._base_url = __tmp8

    async def service(__tmp0, __tmp11, __tmp19, __tmp10) -> __typ3:
        __tmp8 = f'{__tmp0._base_url}/health/checks/{__tmp11}'
        params = {'index': __tmp19,
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
                statuses.append(__typ6(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time: <FILL>):
        if time.total_seconds() < 60:
            return __typ5(__typ0(time.total_seconds())) + 's'
        else:
            return __typ5(time.total_seconds() / 60) + 'm'


class __typ7():
    def __tmp17(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def service(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def __tmp20(__tmp0) -> __typ2:
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def create(__tmp9, config) :
        __tmp0 = __tmp9()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ4(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
