from typing import TypeAlias
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp3(__tmp0, address: str, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp3(__tmp0, address: str, port: __typ0, tags: List[str]):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class QueryResult:
    def __tmp3(__tmp0, last_index: __typ0, response: List[ServiceEntry]):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(__typ0(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(obj)


class ServiceEndpoint:
    def __tmp3(__tmp0, __tmp4: aiohttp.ClientSession, url: str):
        __tmp0._client = __tmp4
        __tmp0._base_url = url

    async def __tmp1(__tmp0, service_id: str,
                       cluster_name: str,
                       kinds: List[str],
                       address: str,
                       port: __typ0,
                       deregister_critical: timedelta,
                       service_ttl: timedelta) -> None:

        data = json.dumps({'ID': service_id,
                           'Name': cluster_name,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, cls=DateTimeEncoder)

        url = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(url, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp0, service_id: str) -> None:
        url = __tmp0._base_url + '/agent/service/deregister/' + service_id
        async with __tmp0._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, __tmp2: str) -> None:
        url = __tmp0._base_url + '/agent/check/pass/' + __tmp2
        async with __tmp0._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp3(__tmp0, __tmp4: aiohttp.ClientSession, url):
        __tmp0._client = __tmp4
        __tmp0._base_url = url

    async def __tmp5(__tmp0, key: str, value: bytes) -> None:
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.put(url, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp0, key: str, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, key: str) -> None:
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.delete(url) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp3(__tmp0, __tmp4: aiohttp.ClientSession, url: str):
        __tmp0._client = __tmp4
        __tmp0._base_url = url

    async def service(__tmp0, cluster_name: str, index: __typ0, blocking_wait_time: <FILL>) -> QueryResult:
        url = f'{__tmp0._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                service_id = response['ServiceID']
                address = service_id[(service_id.find('@') + 1):(service_id.find(':'))]
                port = service_id[(service_id.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return QueryResult(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time: timedelta):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp3(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def service(__tmp0) -> ServiceEndpoint:
        return __tmp0._service_endpoint

    @property
    def key_value_storage(__tmp0) -> KeyValueEndpoint:
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) -> HealthEndpoint:
        return __tmp0._health_endpoint

    @classmethod
    async def create(cls, config: ConsulClientConfiguration) -> 'ConsulClient':
        __tmp0 = cls()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = ServiceEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = KeyValueEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = HealthEndpoint(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
