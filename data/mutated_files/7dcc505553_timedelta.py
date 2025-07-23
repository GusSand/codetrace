from typing import TypeAlias
__typ4 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp5(__tmp1, address: __typ4, datacenter: __typ4 = 'dc1'):
        __tmp1.address = address
        __tmp1.datacenter = datacenter


class __typ6:
    def __tmp5(__tmp1, address: __typ4, port, tags: List[__typ4]):
        __tmp1.address = address
        __tmp1.port = port
        __tmp1.tags = tags


class __typ3:
    def __tmp5(__tmp1, last_index, response: List[__typ6]):
        __tmp1.last_index = last_index
        __tmp1.response = response


class __typ5(json.JSONEncoder):
    def default(__tmp1, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ4(__typ0(obj.total_seconds())) + 's'
            else:
                return __typ4(obj.total_seconds() / 60) + 'm'

        return super(__typ5, __tmp1).default(obj)


class ServiceEndpoint:
    def __tmp5(__tmp1, __tmp6, __tmp4: __typ4):
        __tmp1._client = __tmp6
        __tmp1._base_url = __tmp4

    async def register(__tmp1, __tmp2,
                       cluster_name,
                       kinds: List[__typ4],
                       address,
                       port,
                       deregister_critical: <FILL>,
                       __tmp3: timedelta) -> None:

        data = json.dumps({'ID': __tmp2,
                           'Name': cluster_name,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': __tmp3}
                           }, cls=__typ5)

        __tmp4 = __tmp1._base_url + '/agent/service/register'
        async with __tmp1._client.put(__tmp4, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp1, __tmp2) :
        __tmp4 = __tmp1._base_url + '/agent/service/deregister/' + __tmp2
        async with __tmp1._client.put(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp1, check_id) -> None:
        __tmp4 = __tmp1._base_url + '/agent/check/pass/' + check_id
        async with __tmp1._client.put(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp5(__tmp1, __tmp6: aiohttp.ClientSession, __tmp4):
        __tmp1._client = __tmp6
        __tmp1._base_url = __tmp4

    async def create_or_update(__tmp1, __tmp8: __typ4, value) -> None:
        __tmp4 = __tmp1._base_url + '/kv/' + __tmp8
        async with __tmp1._client.put(__tmp4, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp1, __tmp8: __typ4, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp4 = __tmp1._base_url + '/kv/' + __tmp8
        async with __tmp1._client.get(__tmp4, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp1, __tmp8) :
        __tmp4 = __tmp1._base_url + '/kv/' + __tmp8
        async with __tmp1._client.delete(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp5(__tmp1, __tmp6, __tmp4):
        __tmp1._client = __tmp6
        __tmp1._base_url = __tmp4

    async def service(__tmp1, cluster_name: __typ4, __tmp9: __typ0, __tmp0) :
        __tmp4 = f'{__tmp1._base_url}/health/checks/{cluster_name}'
        params = {'index': __tmp9,
                  'wait': __tmp1.__convert_time(__tmp0)}

        async with __tmp1._client.get(__tmp4, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp2 = response['ServiceID']
                address = __tmp2[(__tmp2.find('@') + 1):(__tmp2.find(':'))]
                port = __tmp2[(__tmp2.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ6(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp1, time):
        if time.total_seconds() < 60:
            return __typ4(__typ0(time.total_seconds())) + 's'
        else:
            return __typ4(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp5(__tmp1):
        __tmp1._client = None
        __tmp1._base_url = None
        __tmp1._service_endpoint = None
        __tmp1._key_value_endpoint = None
        __tmp1._health_endpoint = None

    @property
    def service(__tmp1) :
        return __tmp1._service_endpoint

    @property
    def key_value_storage(__tmp1) :
        return __tmp1._key_value_endpoint

    @property
    def health(__tmp1) :
        return __tmp1._health_endpoint

    @classmethod
    async def __tmp7(cls, config: ConsulClientConfiguration) :
        __tmp1 = cls()
        __tmp1._base_url = f'{config.address}/v1/'
        __tmp1._client = aiohttp.ClientSession()
        __tmp1._service_endpoint = ServiceEndpoint(__tmp1._client, __tmp1._base_url)
        __tmp1._key_value_endpoint = __typ2(__tmp1._client, __tmp1._base_url)
        __tmp1._health_endpoint = __typ1(__tmp1._client, __tmp1._base_url)
        return __tmp1

    async def close(__tmp1):
        await __tmp1._client.close()
