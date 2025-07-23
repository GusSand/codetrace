from typing import TypeAlias
__typ8 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ9:
    def __tmp18(__tmp0, address, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class __typ6:
    def __tmp18(__tmp0, address: str, port, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ3:
    def __tmp18(__tmp0, last_index, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ5(json.JSONEncoder):
    def default(__tmp0, __tmp14):
        if isinstance(__tmp14, datetime.timedelta):
            if __tmp14.total_seconds() < 60:
                return str(__typ0(__tmp14.total_seconds())) + 's'
            else:
                return str(__tmp14.total_seconds() / 60) + 'm'

        return super(__typ5, __tmp0).default(__tmp14)


class __typ4:
    def __tmp18(__tmp0, __tmp19, __tmp8):
        __tmp0._client = __tmp19
        __tmp0._base_url = __tmp8

    async def __tmp6(__tmp0, __tmp7: str,
                       __tmp13,
                       __tmp16,
                       address: str,
                       port,
                       __tmp17,
                       service_ttl) :

        data = json.dumps({'ID': __tmp7,
                           'Name': __tmp13,
                           'Tags': __tmp16,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp17,
                               'TTL': service_ttl}
                           }, __tmp9=__typ5)

        __tmp8 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp8, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp0, __tmp7) :
        __tmp8 = __tmp0._base_url + '/agent/service/deregister/' + __tmp7
        async with __tmp0._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, __tmp1) :
        __tmp8 = __tmp0._base_url + '/agent/check/pass/' + __tmp1
        async with __tmp0._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp18(__tmp0, __tmp19, __tmp8):
        __tmp0._client = __tmp19
        __tmp0._base_url = __tmp8

    async def create_or_update(__tmp0, __tmp5, __tmp15) :
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp5
        async with __tmp0._client.put(__tmp8, data=__tmp15) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp4(__tmp0, __tmp5, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp5
        async with __tmp0._client.get(__tmp8, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp5) :
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp5
        async with __tmp0._client.delete(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp18(__tmp0, __tmp19, __tmp8: <FILL>):
        __tmp0._client = __tmp19
        __tmp0._base_url = __tmp8

    async def __tmp10(__tmp0, __tmp13, __tmp20, __tmp12) :
        __tmp8 = f'{__tmp0._base_url}/health/checks/{__tmp13}'
        params = {'index': __tmp20,
                  'wait': __tmp0.__convert_time(__tmp12)}

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

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ7():
    def __tmp18(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def __tmp10(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def __tmp21(__tmp0) :
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def __tmp11(__tmp9, __tmp3) :
        __tmp0 = __tmp9()
        __tmp0._base_url = f'{__tmp3.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ4(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
