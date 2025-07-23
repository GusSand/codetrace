import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp21(__tmp0, address, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp21(__tmp0, address, port: int, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class QueryResult:
    def __tmp21(__tmp0, last_index: int, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, __tmp16):
        if isinstance(__tmp16, datetime.timedelta):
            if __tmp16.total_seconds() < 60:
                return str(int(__tmp16.total_seconds())) + 's'
            else:
                return str(__tmp16.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(__tmp16)


class ServiceEndpoint:
    def __tmp21(__tmp0, __tmp22: aiohttp.ClientSession, __tmp10):
        __tmp0._client = __tmp22
        __tmp0._base_url = __tmp10

    async def __tmp8(__tmp0, __tmp9: str,
                       __tmp15,
                       __tmp18: List[str],
                       address,
                       port,
                       __tmp20,
                       __tmp19) :

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

    async def __tmp2(__tmp0, __tmp9) :
        __tmp10 = __tmp0._base_url + '/agent/service/deregister/' + __tmp9
        async with __tmp0._client.put(__tmp10) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp24(__tmp0, __tmp1: str) -> None:
        __tmp10 = __tmp0._base_url + '/agent/check/pass/' + __tmp1
        async with __tmp0._client.put(__tmp10) as resp:
            if resp.status != 200:
                raise Exception()


class __typ0:
    def __tmp21(__tmp0, __tmp22: aiohttp.ClientSession, __tmp10):
        __tmp0._client = __tmp22
        __tmp0._base_url = __tmp10

    async def __tmp6(__tmp0, __tmp4: <FILL>, __tmp17) -> None:
        __tmp10 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.put(__tmp10, data=__tmp17) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp5(__tmp0, __tmp4: str, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp10 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.get(__tmp10, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp4: str) -> None:
        __tmp10 = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.delete(__tmp10) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp21(__tmp0, __tmp22, __tmp10):
        __tmp0._client = __tmp22
        __tmp0._base_url = __tmp10

    async def __tmp12(__tmp0, __tmp15, __tmp23, __tmp14) -> QueryResult:
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
                statuses.append(ServiceEntry(address, port, tags))
            return QueryResult(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return str(int(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
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
    def __tmp25(__tmp0) :
        return __tmp0._key_value_endpoint

    @property
    def __tmp7(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def __tmp13(__tmp11, __tmp3) -> 'ConsulClient':
        __tmp0 = __tmp11()
        __tmp0._base_url = f'{__tmp3.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = ServiceEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ0(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = HealthEndpoint(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
