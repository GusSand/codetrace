from typing import TypeAlias
__typ7 : TypeAlias = "bytes"
__typ5 : TypeAlias = "dict"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ8:
    def __tmp12(__tmp2, address: str, datacenter: str = 'dc1'):
        __tmp2.address = address
        __tmp2.datacenter = datacenter


class ServiceEntry:
    def __tmp12(__tmp2, address, port, tags: List[str]):
        __tmp2.address = address
        __tmp2.port = port
        __tmp2.tags = tags


class QueryResult:
    def __tmp12(__tmp2, last_index, response: List[ServiceEntry]):
        __tmp2.last_index = last_index
        __tmp2.response = response


class __typ4(json.JSONEncoder):
    def default(__tmp2, __tmp4):
        if isinstance(__tmp4, datetime.timedelta):
            if __tmp4.total_seconds() < 60:
                return str(__typ0(__tmp4.total_seconds())) + 's'
            else:
                return str(__tmp4.total_seconds() / 60) + 'm'

        return super(__typ4, __tmp2).default(__tmp4)


class __typ3:
    def __tmp12(__tmp2, __tmp14, __tmp9: <FILL>):
        __tmp2._client = __tmp14
        __tmp2._base_url = __tmp9

    async def register(__tmp2, __tmp8,
                       __tmp3: str,
                       __tmp7: List[str],
                       address,
                       port,
                       __tmp10,
                       service_ttl) :

        data = json.dumps({'ID': __tmp8,
                           'Name': __tmp3,
                           'Tags': __tmp7,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp10,
                               'TTL': service_ttl}
                           }, cls=__typ4)

        __tmp9 = __tmp2._base_url + '/agent/service/register'
        async with __tmp2._client.put(__tmp9, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp11(__tmp2, __tmp8) :
        __tmp9 = __tmp2._base_url + '/agent/service/deregister/' + __tmp8
        async with __tmp2._client.put(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp5(__tmp2, check_id) :
        __tmp9 = __tmp2._base_url + '/agent/check/pass/' + check_id
        async with __tmp2._client.put(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp12(__tmp2, __tmp14, __tmp9):
        __tmp2._client = __tmp14
        __tmp2._base_url = __tmp9

    async def create_or_update(__tmp2, __tmp15: str, __tmp6: __typ7) :
        __tmp9 = __tmp2._base_url + '/kv/' + __tmp15
        async with __tmp2._client.put(__tmp9, data=__tmp6) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp2, __tmp15, recurse=True) -> __typ5:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp9 = __tmp2._base_url + '/kv/' + __tmp15
        async with __tmp2._client.get(__tmp9, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp2, __tmp15) -> None:
        __tmp9 = __tmp2._base_url + '/kv/' + __tmp15
        async with __tmp2._client.delete(__tmp9) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp12(__tmp2, __tmp14, __tmp9):
        __tmp2._client = __tmp14
        __tmp2._base_url = __tmp9

    async def service(__tmp2, __tmp3, __tmp16, __tmp1) :
        __tmp9 = f'{__tmp2._base_url}/health/checks/{__tmp3}'
        params = {'index': __tmp16,
                  'wait': __tmp2.__convert_time(__tmp1)}

        async with __tmp2._client.get(__tmp9, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp8 = response['ServiceID']
                address = __tmp8[(__tmp8.find('@') + 1):(__tmp8.find(':'))]
                port = __tmp8[(__tmp8.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return QueryResult(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp2, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ6():
    def __tmp12(__tmp2):
        __tmp2._client = None
        __tmp2._base_url = None
        __tmp2._service_endpoint = None
        __tmp2._key_value_endpoint = None
        __tmp2._health_endpoint = None

    @property
    def service(__tmp2) :
        return __tmp2._service_endpoint

    @property
    def key_value_storage(__tmp2) :
        return __tmp2._key_value_endpoint

    @property
    def __tmp0(__tmp2) :
        return __tmp2._health_endpoint

    @classmethod
    async def create(cls, __tmp13) -> 'ConsulClient':
        __tmp2 = cls()
        __tmp2._base_url = f'{__tmp13.address}/v1/'
        __tmp2._client = aiohttp.ClientSession()
        __tmp2._service_endpoint = __typ3(__tmp2._client, __tmp2._base_url)
        __tmp2._key_value_endpoint = __typ2(__tmp2._client, __tmp2._base_url)
        __tmp2._health_endpoint = __typ1(__tmp2._client, __tmp2._base_url)
        return __tmp2

    async def close(__tmp2):
        await __tmp2._client.close()
