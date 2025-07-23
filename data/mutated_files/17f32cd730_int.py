from typing import TypeAlias
__typ0 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp17(__tmp0, address: __typ0, datacenter: __typ0 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp17(__tmp0, address, port: <FILL>, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class QueryResult:
    def __tmp17(__tmp0, last_index, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, __tmp13):
        if isinstance(__tmp13, datetime.timedelta):
            if __tmp13.total_seconds() < 60:
                return __typ0(int(__tmp13.total_seconds())) + 's'
            else:
                return __typ0(__tmp13.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(__tmp13)


class ServiceEndpoint:
    def __tmp17(__tmp0, __tmp18, __tmp8: __typ0):
        __tmp0._client = __tmp18
        __tmp0._base_url = __tmp8

    async def __tmp6(__tmp0, __tmp7,
                       __tmp12,
                       __tmp15: List[__typ0],
                       address,
                       port,
                       __tmp16,
                       service_ttl) :

        data = json.dumps({'ID': __tmp7,
                           'Name': __tmp12,
                           'Tags': __tmp15,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp16,
                               'TTL': service_ttl}
                           }, __tmp9=DateTimeEncoder)

        __tmp8 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp8, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp0, __tmp7) :
        __tmp8 = __tmp0._base_url + '/agent/service/deregister/' + __tmp7
        async with __tmp0._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, check_id) :
        __tmp8 = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp17(__tmp0, __tmp18: aiohttp.ClientSession, __tmp8: __typ0):
        __tmp0._client = __tmp18
        __tmp0._base_url = __tmp8

    async def __tmp4(__tmp0, __tmp3, __tmp14: bytes) :
        __tmp8 = __tmp0._base_url + '/kv/' + __tmp3
        async with __tmp0._client.put(__tmp8, data=__tmp14) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp0, __tmp3, recurse=True) :
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
    def __tmp17(__tmp0, __tmp18, __tmp8):
        __tmp0._client = __tmp18
        __tmp0._base_url = __tmp8

    async def __tmp10(__tmp0, __tmp12: __typ0, __tmp19, __tmp11) :
        __tmp8 = f'{__tmp0._base_url}/health/checks/{__tmp12}'
        params = {'index': __tmp19,
                  'wait': __tmp0.__convert_time(__tmp11)}

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
            return QueryResult(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return __typ0(int(time.total_seconds())) + 's'
        else:
            return __typ0(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp17(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def __tmp10(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def __tmp20(__tmp0) :
        return __tmp0._key_value_endpoint

    @property
    def __tmp5(__tmp0) -> __typ1:
        return __tmp0._health_endpoint

    @classmethod
    async def create(__tmp9, __tmp1) :
        __tmp0 = __tmp9()
        __tmp0._base_url = f'{__tmp1.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = ServiceEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = KeyValueEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
