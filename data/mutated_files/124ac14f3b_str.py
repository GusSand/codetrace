from typing import TypeAlias
__typ2 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class ConsulClientConfiguration:
    def __tmp8(__tmp1, address, datacenter: str = 'dc1'):
        __tmp1.address = address
        __tmp1.datacenter = datacenter


class ServiceEntry:
    def __tmp8(__tmp1, address, port, tags):
        __tmp1.address = address
        __tmp1.port = port
        __tmp1.tags = tags


class __typ0:
    def __tmp8(__tmp1, last_index, response):
        __tmp1.last_index = last_index
        __tmp1.response = response


class __typ1(json.JSONEncoder):
    def default(__tmp1, obj):
        if isinstance(obj, datetime.timedelta):
            if obj.total_seconds() < 60:
                return str(__typ2(obj.total_seconds())) + 's'
            else:
                return str(obj.total_seconds() / 60) + 'm'

        return super(__typ1, __tmp1).default(obj)


class ServiceEndpoint:
    def __tmp8(__tmp1, client: aiohttp.ClientSession, __tmp6):
        __tmp1._client = client
        __tmp1._base_url = __tmp6

    async def __tmp2(__tmp1, __tmp4,
                       __tmp3,
                       kinds,
                       address,
                       port: __typ2,
                       deregister_critical,
                       __tmp5: timedelta) :

        data = json.dumps({'ID': __tmp4,
                           'Name': __tmp3,
                           'Tags': kinds,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': __tmp5}
                           }, cls=__typ1)

        __tmp6 = __tmp1._base_url + '/agent/service/register'
        async with __tmp1._client.put(__tmp6, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp7(__tmp1, __tmp4) :
        __tmp6 = __tmp1._base_url + '/agent/service/deregister/' + __tmp4
        async with __tmp1._client.put(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()

    async def pass_ttl(__tmp1, check_id: <FILL>) :
        __tmp6 = __tmp1._base_url + '/agent/check/pass/' + check_id
        async with __tmp1._client.put(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()


class KeyValueEndpoint:
    def __tmp8(__tmp1, client, __tmp6):
        __tmp1._client = client
        __tmp1._base_url = __tmp6

    async def create_or_update(__tmp1, key, value) :
        __tmp6 = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.put(__tmp6, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp9(__tmp1, key, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp6 = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.get(__tmp6, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp1, key) -> None:
        __tmp6 = __tmp1._base_url + '/kv/' + key
        async with __tmp1._client.delete(__tmp6) as resp:
            if resp.status != 200:
                raise Exception()


class HealthEndpoint():
    def __tmp8(__tmp1, client, __tmp6):
        __tmp1._client = client
        __tmp1._base_url = __tmp6

    async def service(__tmp1, __tmp3, __tmp10, blocking_wait_time) :
        __tmp6 = f'{__tmp1._base_url}/health/checks/{__tmp3}'
        params = {'index': __tmp10,
                  'wait': __tmp1.__convert_time(blocking_wait_time)}

        async with __tmp1._client.get(__tmp6, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp4 = response['ServiceID']
                address = __tmp4[(__tmp4.find('@') + 1):(__tmp4.find(':'))]
                port = __tmp4[(__tmp4.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ0(__typ2(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp1, time):
        if time.total_seconds() < 60:
            return str(__typ2(time.total_seconds())) + 's'
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
    def service(__tmp1) :
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
        __tmp1._key_value_endpoint = KeyValueEndpoint(__tmp1._client, __tmp1._base_url)
        __tmp1._health_endpoint = HealthEndpoint(__tmp1._client, __tmp1._base_url)
        return __tmp1

    async def close(__tmp1):
        await __tmp1._client.close()
