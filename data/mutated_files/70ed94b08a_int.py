from typing import TypeAlias
__typ5 : TypeAlias = "dict"
__typ4 : TypeAlias = "str"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ7:
    def __tmp5(__tmp0, address, datacenter: __typ4 = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp5(__tmp0, address, port, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ2:
    def __tmp5(__tmp0, last_index, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class DateTimeEncoder(json.JSONEncoder):
    def default(__tmp0, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return __typ4(int(obj.total_seconds())) + 's'
            else:
                return __typ4(obj.total_seconds() / 60) + 'm'

        return super(DateTimeEncoder, __tmp0).default(obj)


class __typ3:
    def __tmp5(__tmp0, __tmp6, __tmp4):
        __tmp0._client = __tmp6
        __tmp0._base_url = __tmp4

    async def register(__tmp0, service_id,
                       cluster_name,
                       __tmp2,
                       address,
                       port,
                       deregister_critical,
                       service_ttl) :

        data = json.dumps({'ID': service_id,
                           'Name': cluster_name,
                           'Tags': __tmp2,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': service_ttl}
                           }, cls=DateTimeEncoder)

        __tmp4 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp4, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def deregister(__tmp0, service_id) :
        __tmp4 = __tmp0._base_url + '/agent/service/deregister/' + service_id
        async with __tmp0._client.put(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp8(__tmp0, check_id) :
        __tmp4 = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1:
    def __tmp5(__tmp0, __tmp6, __tmp4):
        __tmp0._client = __tmp6
        __tmp0._base_url = __tmp4

    async def create_or_update(__tmp0, __tmp7, __tmp1) :
        __tmp4 = __tmp0._base_url + '/kv/' + __tmp7
        async with __tmp0._client.put(__tmp4, data=__tmp1) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp3(__tmp0, __tmp7: __typ4, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp4 = __tmp0._base_url + '/kv/' + __tmp7
        async with __tmp0._client.get(__tmp4, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp7: __typ4) :
        __tmp4 = __tmp0._base_url + '/kv/' + __tmp7
        async with __tmp0._client.delete(__tmp4) as resp:
            if resp.status != 200:
                raise Exception()


class __typ0():
    def __tmp5(__tmp0, __tmp6, __tmp4):
        __tmp0._client = __tmp6
        __tmp0._base_url = __tmp4

    async def service(__tmp0, cluster_name, index: <FILL>, blocking_wait_time) -> __typ2:
        __tmp4 = f'{__tmp0._base_url}/health/checks/{cluster_name}'
        params = {'index': index,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(__tmp4, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                service_id = response['ServiceID']
                address = service_id[(service_id.find('@') + 1):(service_id.find(':'))]
                port = service_id[(service_id.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ2(int(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return __typ4(int(time.total_seconds())) + 's'
        else:
            return __typ4(time.total_seconds() / 60) + 'm'


class __typ6():
    def __tmp5(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def service(__tmp0) :
        return __tmp0._service_endpoint

    @property
    def __tmp9(__tmp0) :
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def create(cls, config) :
        __tmp0 = cls()
        __tmp0._base_url = f'{config.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ3(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ0(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
