from typing import TypeAlias
__typ0 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __init__(__tmp0, address, datacenter: __typ0 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __init__(__tmp0, address: __typ0, port: <FILL>, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class QueryResult:
    def __init__(__tmp0, last_index, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ0(int(obj.total_seconds())) + 's'
            else:
                return __typ0(obj.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(obj)


class ServiceEndpoint:
    def __init__(__tmp0, client, url: __typ0):
        __tmp0._client = client
        __tmp0._base_url = url

    async def register(__tmp0, service_id: __typ0,
                       cluster_name,
                       kinds,
                       address,
                       port: int,
                       deregister_critical,
                       service_ttl) -> None:

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

    async def deregister(__tmp0, service_id: __typ0) -> None:
        url = __tmp0._base_url + '/agent/service/deregister/' + service_id
        async with __tmp0._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, check_id) :
        url = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __init__(__tmp0, client, url):
        __tmp0._client = client
        __tmp0._base_url = url

    async def create_or_update(__tmp0, key, value: bytes) :
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.put(url, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp0, key: __typ0, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, key: __typ0) :
        url = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.delete(url) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __init__(__tmp0, client: aiohttp.ClientSession, url: __typ0):
        __tmp0._client = client
        __tmp0._base_url = url

    async def service(__tmp0, cluster_name, index, blocking_wait_time: timedelta) :
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
            return QueryResult(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return __typ0(int(time.total_seconds())) + 's'
        else:
            return __typ0(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __init__(__tmp0):
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
