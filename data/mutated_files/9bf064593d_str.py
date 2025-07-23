from typing import TypeAlias
__typ1 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp7(__tmp0, address, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp7(__tmp0, address: str, port, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ0:
    def __tmp7(__tmp0, last_index, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(__typ1(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(obj)


class ServiceEndpoint:
    def __tmp7(__tmp0, __tmp9: aiohttp.ClientSession, __tmp5: str):
        __tmp0._client = __tmp9
        __tmp0._base_url = __tmp5

    async def __tmp1(__tmp0, __tmp4,
                       cluster_name: str,
                       __tmp3: List[str],
                       address,
                       port,
                       deregister_critical,
                       service_ttl: timedelta) -> None:

        data = json.dumps({'ID': __tmp4,
                           'Name': cluster_name,
                           'Tags': __tmp3,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, cls=DateTimeEncoder)

        __tmp5 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp5, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp6(__tmp0, __tmp4: <FILL>) :
        __tmp5 = __tmp0._base_url + '/agent/service/deregister/' + __tmp4
        async with __tmp0._client.put(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp11(__tmp0, check_id: str) :
        __tmp5 = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp7(__tmp0, __tmp9: aiohttp.ClientSession, __tmp5):
        __tmp0._client = __tmp9
        __tmp0._base_url = __tmp5

    async def create_or_update(__tmp0, key: str, __tmp2) -> None:
        __tmp5 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.put(__tmp5, data=__tmp2) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp10(__tmp0, key: str, recurse=True) -> dict:
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp5 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.get(__tmp5, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, key: str) :
        __tmp5 = __tmp0._base_url + '/kv/' + key
        async with __tmp0._client.delete(__tmp5) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp7(__tmp0, __tmp9: aiohttp.ClientSession, __tmp5):
        __tmp0._client = __tmp9
        __tmp0._base_url = __tmp5

    async def service(__tmp0, cluster_name: str, index, blocking_wait_time: timedelta) :
        __tmp5 = f'{__tmp0._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(__tmp5, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp4 = response['ServiceID']
                address = __tmp4[(__tmp4.find('@') + 1):(__tmp4.find(':'))]
                port = __tmp4[(__tmp4.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ0(__typ1(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time: timedelta):
        if time.total_seconds() < 60:
            return str(__typ1(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp7(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def service(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def __tmp12(__tmp0) -> KeyValueEndpoint:
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def create(cls, __tmp8: ConsulClientConfiguration) -> 'ConsulClient':
        __tmp0 = cls()
        __tmp0._base_url = f'{__tmp8.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = ServiceEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = KeyValueEndpoint(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = HealthEndpoint(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
