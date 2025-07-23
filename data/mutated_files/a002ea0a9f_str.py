from typing import TypeAlias
__typ5 : TypeAlias = "dict"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ6:
    def __tmp8(__tmp1, address, datacenter: str = 'dc1'):
        __tmp1.address = address
        __tmp1.datacenter = datacenter


class ServiceEntry:
    def __tmp8(__tmp1, address, port, tags):
        __tmp1.address = address
        __tmp1.port = port
        __tmp1.tags = tags


class __typ3:
    def __tmp8(__tmp1, last_index, response):
        __tmp1.last_index = last_index
        __tmp1.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp1, __tmp3):
        if isinstance(__tmp3, datetime.timedelta):
            if __tmp3.total_seconds() < 60:
                return str(__typ0(__tmp3.total_seconds())) + 's'
            else:
                return str(__tmp3.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp1).default(__tmp3)


class __typ4:
    def __tmp8(__tmp1, __tmp10, url):
        __tmp1._client = __tmp10
        __tmp1._base_url = url

    async def register(__tmp1, service_id,
                       __tmp2: <FILL>,
                       __tmp4,
                       address,
                       port,
                       __tmp6,
                       service_ttl) :

        data = json.dumps({'ID': service_id,
                           'Name': __tmp2,
                           'Tags': __tmp4,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp6,
                               'TTL': service_ttl}
                           }, __tmp5=DateTimeEncoder)

        url = __tmp1._base_url + '/agent/service/register'
        async with __tmp1._client.put(url, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp1, service_id) :
        url = __tmp1._base_url + '/agent/service/deregister/' + service_id
        async with __tmp1._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp1, check_id) :
        url = __tmp1._base_url + '/agent/check/pass/' + check_id
        async with __tmp1._client.put(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp8(__tmp1, __tmp10, url):
        __tmp1._client = __tmp10
        __tmp1._base_url = url

    async def create_or_update(__tmp1, __tmp11, value) :
        url = __tmp1._base_url + '/kv/' + __tmp11
        async with __tmp1._client.put(url, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp1, __tmp11, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        url = __tmp1._base_url + '/kv/' + __tmp11
        async with __tmp1._client.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp1, __tmp11) :
        url = __tmp1._base_url + '/kv/' + __tmp11
        async with __tmp1._client.delete(url) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp8(__tmp1, __tmp10, url):
        __tmp1._client = __tmp10
        __tmp1._base_url = url

    async def __tmp7(__tmp1, __tmp2, __tmp12, __tmp0) :
        url = f'{__tmp1._base_url}/health/checks/{__tmp2}'
        params = {'index': __tmp12,
                  'wait': __tmp1.__convert_time(__tmp0)}

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
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp1, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp8(__tmp1):
        __tmp1._client = None
        __tmp1._base_url = None
        __tmp1._service_endpoint = None
        __tmp1._key_value_endpoint = None
        __tmp1._health_endpoint = None

    @property
    def __tmp7(__tmp1) :
        return __tmp1._service_endpoint

    @property
    def __tmp13(__tmp1) :
        return __tmp1._key_value_endpoint

    @property
    def health(__tmp1) :
        return __tmp1._health_endpoint

    @classmethod
    async def create(__tmp5, __tmp9) :
        __tmp1 = __tmp5()
        __tmp1._base_url = f'{__tmp9.address}/v1/'
        __tmp1._client = aiohttp.ClientSession()
        __tmp1._service_endpoint = __typ4(__tmp1._client, __tmp1._base_url)
        __tmp1._key_value_endpoint = __typ2(__tmp1._client, __tmp1._base_url)
        __tmp1._health_endpoint = __typ1(__tmp1._client, __tmp1._base_url)
        return __tmp1

    async def close(__tmp1):
        await __tmp1._client.close()
