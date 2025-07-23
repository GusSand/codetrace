from typing import TypeAlias
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ5:
    def __tmp5(__tmp1, address: str, datacenter: str = 'dc1'):
        __tmp1.address = address
        __tmp1.datacenter = datacenter


class ServiceEntry:
    def __tmp5(__tmp1, address: str, port, tags: List[str]):
        __tmp1.address = address
        __tmp1.port = port
        __tmp1.tags = tags


class __typ3:
    def __tmp5(__tmp1, last_index, response):
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


class ServiceEndpoint:
    def __tmp5(__tmp1, __tmp6, url):
        __tmp1._client = __tmp6
        __tmp1._base_url = url

    async def __tmp2(__tmp1, __tmp3: <FILL>,
                       cluster_name: str,
                       kinds,
                       address,
                       port,
                       deregister_critical,
                       service_ttl) :

        data = json.dumps({'ID': __tmp3,
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

    async def deregister(__tmp1, __tmp3) :
        url = __tmp1._base_url + '/agent/service/deregister/' + __tmp3
        async with __tmp1._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp1, __tmp4) :
        url = __tmp1._base_url + '/agent/check/pass/' + __tmp4
        async with __tmp1._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp5(__tmp1, __tmp6, url):
        __tmp1._client = __tmp6
        __tmp1._base_url = url

    async def create_or_update(__tmp1, __tmp7: str, value) :
        url = __tmp1._base_url + '/kv/' + __tmp7
        async with __tmp1._client.put(url, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp1, __tmp7, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        url = __tmp1._base_url + '/kv/' + __tmp7
        async with __tmp1._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp1, __tmp7) :
        url = __tmp1._base_url + '/kv/' + __tmp7
        async with __tmp1._client.delete(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp5(__tmp1, __tmp6, url):
        __tmp1._client = __tmp6
        __tmp1._base_url = url

    async def service(__tmp1, cluster_name, index, __tmp0) -> __typ3:
        url = f'{__tmp1._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp1.__convert_time(__tmp0)}

        async with __tmp1._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp3 = response['ServiceID']
                address = __tmp3[(__tmp3.find('@') + 1):(__tmp3.find(':'))]
                port = __tmp3[(__tmp3.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp1, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp5(__tmp1):
        __tmp1._client = None
        __tmp1._base_url = None
        __tmp1._service_endpoint = None
        __tmp1._key_value_endpoint = None
        __tmp1._health_endpoint = None

    @property
    def service(__tmp1) :
        return __tmp1._service_endpoint

    @property
    def __tmp8(__tmp1) :
        return __tmp1._key_value_endpoint

    @property
    def health(__tmp1) :
        return __tmp1._health_endpoint

    @classmethod
    async def create(cls, config) :
        __tmp1 = cls()
        __tmp1._base_url = f'{config.address}/v1/'
        __tmp1._client = aiohttp.ClientSession()
        __tmp1._service_endpoint = ServiceEndpoint(__tmp1._client, __tmp1._base_url)
        __tmp1._key_value_endpoint = __typ2(__tmp1._client, __tmp1._base_url)
        __tmp1._health_endpoint = __typ1(__tmp1._client, __tmp1._base_url)
        return __tmp1

    async def close(__tmp1):
        await __tmp1._client.close()
