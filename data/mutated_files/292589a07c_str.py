from typing import TypeAlias
__typ5 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ6:
    def __tmp9(__tmp1, address: str, datacenter: str = 'dc1'):
        __tmp1.address = address
        __tmp1.datacenter = datacenter


class ServiceEntry:
    def __tmp9(__tmp1, address: str, port: __typ0, tags: List[str]):
        __tmp1.address = address
        __tmp1.port = port
        __tmp1.tags = tags


class __typ1:
    def __tmp9(__tmp1, last_index: __typ0, response: List[ServiceEntry]):
        __tmp1.last_index = last_index
        __tmp1.response = response


class __typ3(json.JSONEncoder):
    def default(__tmp1, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(__typ0(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(__typ3, __tmp1).default(obj)


class __typ2:
    def __tmp9(__tmp1, client: aiohttp.ClientSession, __tmp5: str):
        __tmp1._client = client
        __tmp1._base_url = __tmp5

    async def register(__tmp1, service_id: str,
                       cluster_name: str,
                       __tmp3: List[str],
                       address: str,
                       port: __typ0,
                       deregister_critical: timedelta,
                       service_ttl: timedelta) -> None:

        data = json.dumps({'ID': service_id,
                           'Name': cluster_name,
                           'Tags': __tmp3,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, __tmp6=__typ3)

        __tmp5 = __tmp1._base_url + '/agent/service/register'
        async with __tmp1._client.put(__tmp5, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp8(__tmp1, service_id: str) -> None:
        __tmp5 = __tmp1._base_url + '/agent/service/deregister/' + service_id
        async with __tmp1._client.put(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp1, check_id: <FILL>) -> None:
        __tmp5 = __tmp1._base_url + '/agent/check/pass/' + check_id
        async with __tmp1._client.put(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp9(__tmp1, client: aiohttp.ClientSession, __tmp5: str):
        __tmp1._client = client
        __tmp1._base_url = __tmp5

    async def create_or_update(__tmp1, __tmp11: str, __tmp2: __typ5) -> None:
        __tmp5 = __tmp1._base_url + '/kv/' + __tmp11
        async with __tmp1._client.put(__tmp5, data=__tmp2) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp4(__tmp1, __tmp11: str, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp5 = __tmp1._base_url + '/kv/' + __tmp11
        async with __tmp1._client.get(__tmp5, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp1, __tmp11: str) -> None:
        __tmp5 = __tmp1._base_url + '/kv/' + __tmp11
        async with __tmp1._client.delete(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp9(__tmp1, client: aiohttp.ClientSession, __tmp5):
        __tmp1._client = client
        __tmp1._base_url = __tmp5

    async def __tmp7(__tmp1, cluster_name: str, __tmp12: __typ0, __tmp0: timedelta) -> __typ1:
        __tmp5 = f'{__tmp1._base_url}/health/checks/{cluster_name}'
        params = {'index': __tmp12,
                  'wait': __tmp1.__convert_time(__tmp0)}

        async with __tmp1._client.get(__tmp5, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                service_id = response['ServiceID']
                address = service_id[(service_id.find('@') + 1):(service_id.find(':'))]
                port = service_id[(service_id.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ1(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp1, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ4():
    def __tmp9(__tmp1):
        __tmp1._client = None
        __tmp1._base_url = None
        __tmp1._service_endpoint = None
        __tmp1._key_value_endpoint = None
        __tmp1._health_endpoint = None

    @property
    def __tmp7(__tmp1) -> __typ2:
        return __tmp1._service_endpoint

    @property
    def key_value_storage(__tmp1) :
        return __tmp1._key_value_endpoint

    @property
    def health(__tmp1) -> HealthEndpoint:
        return __tmp1._health_endpoint

    @classmethod
    async def __tmp10(__tmp6, config: __typ6) -> 'ConsulClient':
        __tmp1 = __tmp6()
        __tmp1._base_url = f'{config.address}/v1/'
        __tmp1._client = aiohttp.ClientSession()
        __tmp1._service_endpoint = __typ2(__tmp1._client, __tmp1._base_url)
        __tmp1._key_value_endpoint = KeyValueEndpoint(__tmp1._client, __tmp1._base_url)
        __tmp1._health_endpoint = HealthEndpoint(__tmp1._client, __tmp1._base_url)
        return __tmp1

    async def close(__tmp1):
        await __tmp1._client.close()
