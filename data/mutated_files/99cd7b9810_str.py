from typing import TypeAlias
__typ6 : TypeAlias = "dict"
__typ9 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ10:
    def __tmp10(__tmp2, address, datacenter: str = 'dc1'):
        __tmp2.address = address
        __tmp2.datacenter = datacenter


class __typ7:
    def __tmp10(__tmp2, address, port, tags):
        __tmp2.address = address
        __tmp2.port = port
        __tmp2.tags = tags


class __typ3:
    def __tmp10(__tmp2, last_index, response):
        __tmp2.last_index = last_index
        __tmp2.response = response


class __typ5(json.JSONEncoder):
    def default(__tmp2, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(__typ0(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(__typ5, __tmp2).default(obj)


class __typ4:
    def __tmp10(__tmp2, __tmp11, url: str):
        __tmp2._client = __tmp11
        __tmp2._base_url = url

    async def __tmp3(__tmp2, service_id,
                       cluster_name: str,
                       kinds,
                       address,
                       port,
                       __tmp8,
                       __tmp6: timedelta) :

        data = json.dumps({'ID': service_id,
                           'Name': cluster_name,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp8,
                               'TTL': __tmp6}
                           }, cls=__typ5)

        url = __tmp2._base_url + '/agent/service/register'
        async with __tmp2._client.put(url, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp9(__tmp2, service_id: str) :
        url = __tmp2._base_url + '/agent/service/deregister/' + service_id
        async with __tmp2._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp13(__tmp2, check_id) :
        url = __tmp2._base_url + '/agent/check/pass/' + check_id
        async with __tmp2._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp10(__tmp2, __tmp11, url):
        __tmp2._client = __tmp11
        __tmp2._base_url = url

    async def create_or_update(__tmp2, __tmp12, __tmp4: __typ9) :
        url = __tmp2._base_url + '/kv/' + __tmp12
        async with __tmp2._client.put(url, data=__tmp4) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp5(__tmp2, __tmp12, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        url = __tmp2._base_url + '/kv/' + __tmp12
        async with __tmp2._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp2, __tmp12: str) :
        url = __tmp2._base_url + '/kv/' + __tmp12
        async with __tmp2._client.delete(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp10(__tmp2, __tmp11: aiohttp.ClientSession, url: str):
        __tmp2._client = __tmp11
        __tmp2._base_url = url

    async def __tmp7(__tmp2, cluster_name: <FILL>, index, __tmp1: timedelta) :
        url = f'{__tmp2._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp2.__convert_time(__tmp1)}

        async with __tmp2._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                service_id = response['ServiceID']
                address = service_id[(service_id.find('@') + 1):(service_id.find(':'))]
                port = service_id[(service_id.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(__typ7(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp2, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ8():
    def __tmp10(__tmp2):
        __tmp2._client = None
        __tmp2._base_url = None
        __tmp2._service_endpoint = None
        __tmp2._key_value_endpoint = None
        __tmp2._health_endpoint = None

    @property
    def __tmp7(__tmp2) :
        return __tmp2._service_endpoint

    @property
    def __tmp14(__tmp2) -> __typ2:
        return __tmp2._key_value_endpoint

    @property
    def __tmp0(__tmp2) :
        return __tmp2._health_endpoint

    @classmethod
    async def create(cls, config: __typ10) :
        __tmp2 = cls()
        __tmp2._base_url = f'{config.address}/v1/'
        __tmp2._client = aiohttp.ClientSession()
        __tmp2._service_endpoint = __typ4(__tmp2._client, __tmp2._base_url)
        __tmp2._key_value_endpoint = __typ2(__tmp2._client, __tmp2._base_url)
        __tmp2._health_endpoint = __typ1(__tmp2._client, __tmp2._base_url)
        return __tmp2

    async def close(__tmp2):
        await __tmp2._client.close()
