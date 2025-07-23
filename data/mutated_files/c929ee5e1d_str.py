import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp12(__tmp2, address, datacenter: str = 'dc1'):
        __tmp2.address = address
        __tmp2.datacenter = datacenter


class ServiceEntry:
    def __tmp12(__tmp2, address: str, port, tags):
        __tmp2.address = address
        __tmp2.port = port
        __tmp2.tags = tags


class QueryResult:
    def __tmp12(__tmp2, last_index, response):
        __tmp2.last_index = last_index
        __tmp2.response = response


class __typ0(json.JSONEncoder):
    def default(__tmp2, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(int(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(__typ0, __tmp2).default(obj)


class ServiceEndpoint:
    def __tmp12(__tmp2, __tmp13, __tmp8):
        __tmp2._client = __tmp13
        __tmp2._base_url = __tmp8

    async def __tmp4(__tmp2, __tmp7: str,
                       __tmp3,
                       __tmp6,
                       address,
                       port,
                       deregister_critical,
                       service_ttl) -> None:

        data = json.dumps({'ID': __tmp7,
                           'Name': __tmp3,
                           'Tags': __tmp6,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, __tmp9=__typ0)

        __tmp8 = __tmp2._base_url + '/agent/service/register'
        async with __tmp2._client.put(__tmp8, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp2, __tmp7) -> None:
        __tmp8 = __tmp2._base_url + '/agent/service/deregister/' + __tmp7
        async with __tmp2._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp2, __tmp11) -> None:
        __tmp8 = __tmp2._base_url + '/agent/check/pass/' + __tmp11
        async with __tmp2._client.put(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp12(__tmp2, __tmp13, __tmp8: str):
        __tmp2._client = __tmp13
        __tmp2._base_url = __tmp8

    async def __tmp16(__tmp2, __tmp5, value) :
        __tmp8 = __tmp2._base_url + '/kv/' + __tmp5
        async with __tmp2._client.put(__tmp8, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp14(__tmp2, __tmp5, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp8 = __tmp2._base_url + '/kv/' + __tmp5
        async with __tmp2._client.get(__tmp8, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp2, __tmp5: <FILL>) -> None:
        __tmp8 = __tmp2._base_url + '/kv/' + __tmp5
        async with __tmp2._client.delete(__tmp8) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp12(__tmp2, __tmp13: aiohttp.ClientSession, __tmp8):
        __tmp2._client = __tmp13
        __tmp2._base_url = __tmp8

    async def __tmp10(__tmp2, __tmp3, __tmp15, __tmp1) :
        __tmp8 = f'{__tmp2._base_url}/health/checks/{__tmp3}'
        params = {'index': __tmp15,
                  'wait': __tmp2.__convert_time(__tmp1)}

        async with __tmp2._client.get(__tmp8, params=params) as resp:
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

    def __convert_time(__tmp2, time):
        if time.total_seconds() < 60:
            return str(int(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp12(__tmp2):
        __tmp2._client = None
        __tmp2._base_url = None
        __tmp2._service_endpoint = None
        __tmp2._key_value_endpoint = None
        __tmp2._health_endpoint = None

    @property
    def __tmp10(__tmp2) :
        return __tmp2._service_endpoint

    @property
    def key_value_storage(__tmp2) -> KeyValueEndpoint:
        return __tmp2._key_value_endpoint

    @property
    def __tmp0(__tmp2) :
        return __tmp2._health_endpoint

    @classmethod
    async def create(__tmp9, config) :
        __tmp2 = __tmp9()
        __tmp2._base_url = f'{config.address}/v1/'
        __tmp2._client = aiohttp.ClientSession()
        __tmp2._service_endpoint = ServiceEndpoint(__tmp2._client, __tmp2._base_url)
        __tmp2._key_value_endpoint = KeyValueEndpoint(__tmp2._client, __tmp2._base_url)
        __tmp2._health_endpoint = HealthEndpoint(__tmp2._client, __tmp2._base_url)
        return __tmp2

    async def close(__tmp2):
        await __tmp2._client.close()
