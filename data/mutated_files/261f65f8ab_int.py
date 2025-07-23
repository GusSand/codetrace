from typing import TypeAlias
__typ7 : TypeAlias = "bytes"
__typ4 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ8:
    def __tmp9(__tmp0, address, datacenter: __typ4 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp9(__tmp0, address, port, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ2:
    def __tmp9(__tmp0, last_index: <FILL>, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ5(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ4(int(obj.total_seconds())) + 's'
            else:
                return __typ4(obj.total_seconds() / 60) + 'm'

        return super(__typ5, __tmp0).default(obj)


class __typ3:
    def __tmp9(__tmp0, __tmp10: aiohttp.ClientSession, __tmp6: __typ4):
        __tmp0._client = __tmp10
        __tmp0._base_url = __tmp6

    async def register(__tmp0, __tmp4,
                       __tmp1: __typ4,
                       __tmp3: List[__typ4],
                       address,
                       port,
                       deregister_critical: timedelta,
                       __tmp5) :

        data = json.dumps({'ID': __tmp4,
                           'Name': __tmp1,
                           'Tags': __tmp3,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': __tmp5}
                           }, __tmp7=__typ5)

        __tmp6 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp6, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp0, __tmp4: __typ4) :
        __tmp6 = __tmp0._base_url + '/agent/service/deregister/' + __tmp4
        async with __tmp0._client.put(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, __tmp8: __typ4) -> None:
        __tmp6 = __tmp0._base_url + '/agent/check/pass/' + __tmp8
        async with __tmp0._client.put(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1:
    def __tmp9(__tmp0, __tmp10, __tmp6):
        __tmp0._client = __tmp10
        __tmp0._base_url = __tmp6

    async def create_or_update(__tmp0, __tmp11, __tmp2) :
        __tmp6 = __tmp0._base_url + '/kv/' + __tmp11
        async with __tmp0._client.put(__tmp6, data=__tmp2) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp0, __tmp11, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp6 = __tmp0._base_url + '/kv/' + __tmp11
        async with __tmp0._client.get(__tmp6, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp11: __typ4) :
        __tmp6 = __tmp0._base_url + '/kv/' + __tmp11
        async with __tmp0._client.delete(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()


class __typ0():
    def __tmp9(__tmp0, __tmp10, __tmp6):
        __tmp0._client = __tmp10
        __tmp0._base_url = __tmp6

    async def service(__tmp0, __tmp1, index: int, blocking_wait_time) -> __typ2:
        __tmp6 = f'{__tmp0._base_url}/health/checks/{__tmp1}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(__tmp6, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp4 = response['ServiceID']
                address = __tmp4[(__tmp4.find('@') + 1):(__tmp4.find(':'))]
                port = __tmp4[(__tmp4.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ2(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return __typ4(int(time.total_seconds())) + 's'
        else:
            return __typ4(time.total_seconds() / 60) + 'm'


class __typ6():
    def __tmp9(__tmp0):
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
    def health(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def create(__tmp7, config) -> 'ConsulClient':
        __tmp0 = __tmp7()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ3(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ0(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
