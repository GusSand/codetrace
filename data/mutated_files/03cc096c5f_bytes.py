from typing import TypeAlias
__typ0 : TypeAlias = "dict"
__typ1 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp5(__tmp1, address, datacenter: __typ1 = 'dc1'):
        __tmp1.address = address
        __tmp1.datacenter = datacenter


class ServiceEntry:
    def __tmp5(__tmp1, address, port, tags):
        __tmp1.address = address
        __tmp1.port = port
        __tmp1.tags = tags


class QueryResult:
    def __tmp5(__tmp1, last_index: int, response):
        __tmp1.last_index = last_index
        __tmp1.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp1, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ1(int(obj.total_seconds())) + 's'
            else:
                return __typ1(obj.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp1).default(obj)


class ServiceEndpoint:
    def __tmp5(__tmp1, client, __tmp2):
        __tmp1._client = client
        __tmp1._base_url = __tmp2

    async def register(__tmp1, service_id,
                       cluster_name: __typ1,
                       kinds,
                       address,
                       port,
                       __tmp3,
                       service_ttl) :

        data = json.dumps({'ID': service_id,
                           'Name': cluster_name,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': __tmp3,
                               'TTL': service_ttl}
                           }, cls=DateTimeEncoder)

        __tmp2 = __tmp1._base_url + '/agent/service/register'
        async with __tmp1._client.put(__tmp2, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp1, service_id) :
        __tmp2 = __tmp1._base_url + '/agent/service/deregister/' + service_id
        async with __tmp1._client.put(__tmp2) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp1, check_id) :
        __tmp2 = __tmp1._base_url + '/agent/check/pass/' + check_id
        async with __tmp1._client.put(__tmp2) as resp:
            if resp.status != 200:
                raise Exception()


class __typ3:
    def __tmp5(__tmp1, client, __tmp2):
        __tmp1._client = client
        __tmp1._base_url = __tmp2

    async def create_or_update(__tmp1, key, value: <FILL>) :
        __tmp2 = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.put(__tmp2, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def read(__tmp1, key, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp2 = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.get(__tmp2, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp1, key) :
        __tmp2 = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.delete(__tmp2) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2():
    def __tmp5(__tmp1, client, __tmp2):
        __tmp1._client = client
        __tmp1._base_url = __tmp2

    async def __tmp4(__tmp1, cluster_name, index, blocking_wait_time) :
        __tmp2 = f'{__tmp1._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp1.__convert_time(blocking_wait_time)}

        async with __tmp1._client.get(__tmp2, params=params) as resp:
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

    def __convert_time(__tmp1, time):
        if time.total_seconds() < 60:
            return __typ1(int(time.total_seconds())) + 's'
        else:
            return __typ1(time.total_seconds() / 60) + 'm'


class ConsulClient():
    def __tmp5(__tmp1):
        __tmp1._client = None
        __tmp1._base_url = None
        __tmp1._service_endpoint = None
        __tmp1._key_value_endpoint = None
        __tmp1._health_endpoint = None

    @property
    def __tmp4(__tmp1) :
        return __tmp1._service_endpoint

    @property
    def key_value_storage(__tmp1) :
        return __tmp1._key_value_endpoint

    @property
    def __tmp0(__tmp1) :
        return __tmp1._health_endpoint

    @classmethod
    async def create(cls, config) :
        __tmp1 = cls()
        __tmp1._base_url = f'{config.address}/v1/'
        __tmp1._client = aiohttp.ClientSession()
        __tmp1._service_endpoint = ServiceEndpoint(__tmp1._client, __tmp1._base_url)
        __tmp1._key_value_endpoint = __typ3(__tmp1._client, __tmp1._base_url)
        __tmp1._health_endpoint = __typ2(__tmp1._client, __tmp1._base_url)
        return __tmp1

    async def close(__tmp1):
        await __tmp1._client.close()
