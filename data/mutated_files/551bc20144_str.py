import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp5(__tmp0, address: str, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp5(__tmp0, address: str, port, tags: List[str]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class QueryResult:
    def __tmp5(__tmp0, last_index: int, response: List[ServiceEntry]):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(int(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(obj)


class __typ0:
    def __tmp5(__tmp0, __tmp6, url: <FILL>):
        __tmp0._client = __tmp6
        __tmp0._base_url = url

    async def register(__tmp0, __tmp3,
                       __tmp1,
                       __tmp2,
                       address: str,
                       port,
                       deregister_critical: timedelta,
                       service_ttl: timedelta) -> None:

        data = json.dumps({'ID': __tmp3,
                           'Name': __tmp1,
                           'Tags': __tmp2,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, __tmp4=DateTimeEncoder)

        url = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(url, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp0, __tmp3: str) -> None:
        url = __tmp0._base_url + '/agent/service/deregister/' + __tmp3
        async with __tmp0._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp7(__tmp0, check_id) -> None:
        url = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1:
    def __tmp5(__tmp0, __tmp6, url: str):
        __tmp0._client = __tmp6
        __tmp0._base_url = url

    async def create_or_update(__tmp0, key: str, value: bytes) :
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.put(url, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp0, key, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, key) -> None:
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.delete(url) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp5(__tmp0, __tmp6: aiohttp.ClientSession, url):
        __tmp0._client = __tmp6
        __tmp0._base_url = url

    async def service(__tmp0, __tmp1, index: int, blocking_wait_time: timedelta) :
        url = f'{__tmp0._base_url}/health/checks/{__tmp1}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp3 = response['ServiceID']
                address = __tmp3[(__tmp3.find('@') + 1):(__tmp3.find(':'))]
                port = __tmp3[(__tmp3.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return QueryResult(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return str(int(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp5(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def service(__tmp0) -> __typ0:
        return __tmp0._service_endpoint

    @property
    def key_value_storage(__tmp0) :
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) -> HealthEndpoint:
        return __tmp0._health_endpoint

    @classmethod
    async def create(__tmp4, config: ConsulClientConfiguration) -> 'ConsulClient':
        __tmp0 = __tmp4()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ0(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = HealthEndpoint(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
