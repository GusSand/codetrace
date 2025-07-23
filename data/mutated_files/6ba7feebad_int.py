from typing import TypeAlias
__typ9 : TypeAlias = "bytes"
__typ4 : TypeAlias = "str"
__typ6 : TypeAlias = "dict"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ10:
    def __tmp10(__tmp2, address, datacenter: __typ4 = 'dc1'):
        __tmp2.address = address
        __tmp2.datacenter = datacenter


class __typ7:
    def __tmp10(__tmp2, address: __typ4, port: int, tags: List[__typ4]):
        __tmp2.address = address
        __tmp2.port = port
        __tmp2.tags = tags


class __typ2:
    def __tmp10(__tmp2, last_index: <FILL>, response):
        __tmp2.last_index = last_index
        __tmp2.response = response


class __typ5(json.JSONEncoder):
    def default(__tmp2, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ4(int(obj.total_seconds())) + 's'
            else:
                return __typ4(obj.total_seconds() / 60) + 'm'

        return super(__typ5, __tmp2).default(obj)


class __typ3:
    def __tmp10(__tmp2, __tmp12, __tmp6):
        __tmp2._client = __tmp12
        __tmp2._base_url = __tmp6

    async def register(__tmp2, __tmp4,
                       __tmp3: __typ4,
                       kinds: List[__typ4],
                       address: __typ4,
                       port: int,
                       deregister_critical: timedelta,
                       __tmp5: timedelta) :

        data = json.dumps({'ID': __tmp4,
                           'Name': __tmp3,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': __tmp5}
                           }, __tmp7=__typ5)

        __tmp6 = __tmp2._base_url + '/agent/service/register'
        async with __tmp2._client.put(__tmp6, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp9(__tmp2, __tmp4: __typ4) -> None:
        __tmp6 = __tmp2._base_url + '/agent/service/deregister/' + __tmp4
        async with __tmp2._client.put(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp14(__tmp2, __tmp8: __typ4) -> None:
        __tmp6 = __tmp2._base_url + '/agent/check/pass/' + __tmp8
        async with __tmp2._client.put(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1:
    def __tmp10(__tmp2, __tmp12: aiohttp.ClientSession, __tmp6: __typ4):
        __tmp2._client = __tmp12
        __tmp2._base_url = __tmp6

    async def create_or_update(__tmp2, __tmp13: __typ4, value: __typ9) -> None:
        __tmp6 = __tmp2._base_url + '/kv/' + __tmp13
        async with __tmp2._client.put(__tmp6, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp2, __tmp13, recurse=True) -> __typ6:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp6 = __tmp2._base_url + '/kv/' + __tmp13
        async with __tmp2._client.get(__tmp6, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp2, __tmp13: __typ4) -> None:
        __tmp6 = __tmp2._base_url + '/kv/' + __tmp13
        async with __tmp2._client.delete(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()


class __typ0():
    def __tmp10(__tmp2, __tmp12: aiohttp.ClientSession, __tmp6: __typ4):
        __tmp2._client = __tmp12
        __tmp2._base_url = __tmp6

    async def service(__tmp2, __tmp3: __typ4, index, __tmp1) :
        __tmp6 = f'{__tmp2._base_url}/health/checks/{__tmp3}'
        params = {'index': index,
                  'wait': __tmp2.__convert_time(__tmp1)}

        async with __tmp2._client.get(__tmp6, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp4 = response['ServiceID']
                address = __tmp4[(__tmp4.find('@') + 1):(__tmp4.find(':'))]
                port = __tmp4[(__tmp4.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ7(address, port, tags))
            return __typ2(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp2, time: timedelta):
        if time.total_seconds() < 60:
            return __typ4(int(time.total_seconds())) + 's'
        else:
            return __typ4(time.total_seconds() / 60) + 'm'


class __typ8():
    def __tmp10(__tmp2):
        __tmp2._client = None
        __tmp2._base_url = None
        __tmp2._service_endpoint = None
        __tmp2._key_value_endpoint = None
        __tmp2._health_endpoint = None

    @property
    def service(__tmp2) -> __typ3:
        return __tmp2._service_endpoint

    @property
    def __tmp15(__tmp2) :
        return __tmp2._key_value_endpoint

    @property
    def __tmp0(__tmp2) -> __typ0:
        return __tmp2._health_endpoint

    @classmethod
    async def create(__tmp7, __tmp11: __typ10) -> 'ConsulClient':
        __tmp2 = __tmp7()
        __tmp2._base_url = f'{__tmp11.address}/v1/'
        __tmp2._client = aiohttp.ClientSession()
        __tmp2._service_endpoint = __typ3(__tmp2._client, __tmp2._base_url)
        __tmp2._key_value_endpoint = __typ1(__tmp2._client, __tmp2._base_url)
        __tmp2._health_endpoint = __typ0(__tmp2._client, __tmp2._base_url)
        return __tmp2

    async def close(__tmp2):
        await __tmp2._client.close()
