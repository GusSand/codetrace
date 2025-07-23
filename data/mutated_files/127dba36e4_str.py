from typing import TypeAlias
__typ5 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp2(__tmp0, address: <FILL>, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp2(__tmp0, address, port: __typ0, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ2:
    def __tmp2(__tmp0, last_index: __typ0, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ3(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(__typ0(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(__typ3, __tmp0).default(obj)


class ServiceEndpoint:
    def __tmp2(__tmp0, __tmp3: aiohttp.ClientSession, url):
        __tmp0._client = __tmp3
        __tmp0._base_url = url

    async def register(__tmp0, service_id,
                       cluster_name,
                       kinds,
                       address: str,
                       port,
                       deregister_critical,
                       service_ttl: timedelta) -> None:

        data = json.dumps({'ID': service_id,
                           'Name': cluster_name,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, cls=__typ3)

        url = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(url, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp1(__tmp0, service_id) -> None:
        url = __tmp0._base_url + '/agent/service/deregister/' + service_id
        async with __tmp0._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp0, check_id: str) -> None:
        url = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp2(__tmp0, __tmp3, url: str):
        __tmp0._client = __tmp3
        __tmp0._base_url = url

    async def create_or_update(__tmp0, __tmp4, value) -> None:
        url = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.put(url, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp0, __tmp4, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        url = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp4) -> None:
        url = __tmp0._base_url + '/kv/' + __tmp4
        async with __tmp0._client.delete(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp2(__tmp0, __tmp3, url: str):
        __tmp0._client = __tmp3
        __tmp0._base_url = url

    async def service(__tmp0, cluster_name: str, index: __typ0, blocking_wait_time) :
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
            return __typ2(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ4():
    def __tmp2(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def service(__tmp0) -> ServiceEndpoint:
        return __tmp0._service_endpoint

    @property
    def key_value_storage(__tmp0) :
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def create(cls, config: ConsulClientConfiguration) -> 'ConsulClient':
        __tmp0 = cls()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = ServiceEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = KeyValueEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
