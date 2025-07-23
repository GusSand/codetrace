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
    def __tmp3(__tmp1, address: <FILL>, datacenter: str = 'dc1'):
        __tmp1.address = address
        __tmp1.datacenter = datacenter


class ServiceEntry:
    def __tmp3(__tmp1, address, port: __typ0, tags: List[str]):
        __tmp1.address = address
        __tmp1.port = port
        __tmp1.tags = tags


class QueryResult:
    def __tmp3(__tmp1, last_index: __typ0, response: List[ServiceEntry]):
        __tmp1.last_index = last_index
        __tmp1.response = response


class __typ4(json.JSONEncoder):
    def default(__tmp1, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(__typ0(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(__typ4, __tmp1).default(obj)


class __typ3:
    def __tmp3(__tmp1, __tmp4: aiohttp.ClientSession, url):
        __tmp1._client = __tmp4
        __tmp1._base_url = url

    async def register(__tmp1, service_id: str,
                       cluster_name: str,
                       kinds: List[str],
                       address,
                       port,
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
                           }, cls=__typ4)

        url = __tmp1._base_url + '/agent/service/register'
        async with __tmp1._client.put(url, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp1, service_id: str) :
        url = __tmp1._base_url + '/agent/service/deregister/' + service_id
        async with __tmp1._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp2(__tmp1, check_id: str) -> None:
        url = __tmp1._base_url + '/agent/check/pass/' + check_id
        async with __tmp1._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp3(__tmp1, __tmp4: aiohttp.ClientSession, url):
        __tmp1._client = __tmp4
        __tmp1._base_url = url

    async def __tmp6(__tmp1, key: str, value: __typ7) -> None:
        url = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.put(url, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp5(__tmp1, key: str, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        url = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp1, key: str) -> None:
        url = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.delete(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp3(__tmp1, __tmp4, url):
        __tmp1._client = __tmp4
        __tmp1._base_url = url

    async def service(__tmp1, cluster_name: str, index: __typ0, blocking_wait_time: timedelta) :
        url = f'{__tmp1._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp1.__convert_time(blocking_wait_time)}

        async with __tmp1._client.get(url, params=params) as resp:
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

    def __convert_time(__tmp1, time: timedelta):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ6():
    def __tmp3(__tmp1):
        __tmp1._client = None
        __tmp1._base_url = None
        __tmp1._service_endpoint = None
        __tmp1._key_value_endpoint = None
        __tmp1._health_endpoint = None

    @property
    def service(__tmp1) -> __typ3:
        return __tmp1._service_endpoint

    @property
    def key_value_storage(__tmp1) -> __typ2:
        return __tmp1._key_value_endpoint

    @property
    def __tmp0(__tmp1) -> __typ1:
        return __tmp1._health_endpoint

    @classmethod
    async def create(cls, config: __typ8) -> 'ConsulClient':
        __tmp1 = cls()
        __tmp1._base_url = f'{config.address}/v1/'
        __tmp1._client = aiohttp.ClientSession()
        __tmp1._service_endpoint = __typ3(__tmp1._client, __tmp1._base_url)
        __tmp1._key_value_endpoint = __typ2(__tmp1._client, __tmp1._base_url)
        __tmp1._health_endpoint = __typ1(__tmp1._client, __tmp1._base_url)
        return __tmp1

    async def close(__tmp1):
        await __tmp1._client.close()
