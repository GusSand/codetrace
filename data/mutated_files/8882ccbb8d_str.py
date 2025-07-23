from typing import TypeAlias
__typ6 : TypeAlias = "dict"
__typ8 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
import datetime
import json
from datetime import timedelta
from typing import List

import aiohttp


class __typ9:
    def __tmp12(__tmp0, address, datacenter: str = 'dc1'):
        __tmp0.address = address
        __tmp0.datacenter = datacenter


class ServiceEntry:
    def __tmp12(__tmp0, address, port, tags):
        __tmp0.address = address
        __tmp0.port = port
        __tmp0.tags = tags


class __typ3:
    def __tmp12(__tmp0, last_index, response):
        __tmp0.last_index = last_index
        __tmp0.response = response


class __typ5(json.JSONEncoder):
    def default(__tmp0, __tmp2):
        if isinstance(__tmp2, datetime.timedelta):
            if __tmp2.total_seconds() < 60:
                return str(__typ0(__tmp2.total_seconds())) + 's'
            else:
                return str(__tmp2.total_seconds() / 60) + 'm'

        return super(__typ5, __tmp0).default(__tmp2)


class __typ4:
    def __tmp12(__tmp0, __tmp14, __tmp7):
        __tmp0._client = __tmp14
        __tmp0._base_url = __tmp7

    async def __tmp1(__tmp0, __tmp5,
                       cluster_name,
                       __tmp4,
                       address: <FILL>,
                       port: __typ0,
                       deregister_critical: timedelta,
                       __tmp6) :

        data = json.dumps({'ID': __tmp5,
                           'Name': cluster_name,
                           'Tags': __tmp4,
                           'Address': address,
                           'Port': port,
                           'Check': {
                               'DeregisterCriticalServiceAfter': deregister_critical,
                               'TTL': __tmp6}
                           }, __tmp8=__typ5)

        __tmp7 = __tmp0._base_url + '/agent/service/register'
        async with __tmp0._client.put(__tmp7, data=data) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp11(__tmp0, __tmp5: str) :
        __tmp7 = __tmp0._base_url + '/agent/service/deregister/' + __tmp5
        async with __tmp0._client.put(__tmp7) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp3(__tmp0, check_id) :
        __tmp7 = __tmp0._base_url + '/agent/check/pass/' + check_id
        async with __tmp0._client.put(__tmp7) as resp:
            if resp.status != 200:
                raise Exception()


class __typ2:
    def __tmp12(__tmp0, __tmp14, __tmp7):
        __tmp0._client = __tmp14
        __tmp0._base_url = __tmp7

    async def create_or_update(__tmp0, __tmp16: str, value) -> None:
        __tmp7 = __tmp0._base_url + '/kv/' + __tmp16
        async with __tmp0._client.put(__tmp7, data=value) as resp:
            if resp.status != 200:
                raise Exception()

    async def __tmp9(__tmp0, __tmp16, recurse=True) :
        params = None
        if recurse:
            params = {'recurse': ''}
        __tmp7 = __tmp0._base_url + '/kv/' + __tmp16
        async with __tmp0._client.get(__tmp7, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            return await resp.json()

    async def delete(__tmp0, __tmp16: str) :
        __tmp7 = __tmp0._base_url + '/kv/' + __tmp16
        async with __tmp0._client.delete(__tmp7) as resp:
            if resp.status != 200:
                raise Exception()


class __typ1():
    def __tmp12(__tmp0, __tmp14, __tmp7):
        __tmp0._client = __tmp14
        __tmp0._base_url = __tmp7

    async def __tmp10(__tmp0, cluster_name, __tmp17, blocking_wait_time) :
        __tmp7 = f'{__tmp0._base_url}/health/checks/{cluster_name}'
        params = {'index': __tmp17,
                  'wait': __tmp0.__convert_time(blocking_wait_time)}

        async with __tmp0._client.get(__tmp7, params=params) as resp:
            if resp.status != 200:
                raise Exception()
            statuses = []
            for response in await resp.json():
                __tmp5 = response['ServiceID']
                address = __tmp5[(__tmp5.find('@') + 1):(__tmp5.find(':'))]
                port = __tmp5[(__tmp5.find(':') + 1):]
                tags = response['ServiceTags']
                statuses.append(ServiceEntry(address, port, tags))
            return __typ3(__typ0(resp.headers['X-Consul-Index']), statuses)

    def __convert_time(__tmp0, time):
        if time.total_seconds() < 60:
            return str(__typ0(time.total_seconds())) + 's'
        else:
            return str(time.total_seconds() / 60) + 'm'


class __typ7():
    def __tmp12(__tmp0):
        __tmp0._client = None
        __tmp0._base_url = None
        __tmp0._service_endpoint = None
        __tmp0._key_value_endpoint = None
        __tmp0._health_endpoint = None

    @property
    def __tmp10(__tmp0) -> __typ4:
        return __tmp0._service_endpoint

    @property
    def key_value_storage(__tmp0) :
        return __tmp0._key_value_endpoint

    @property
    def health(__tmp0) :
        return __tmp0._health_endpoint

    @classmethod
    async def __tmp15(__tmp8, __tmp13) :
        __tmp0 = __tmp8()
        __tmp0._base_url = f'{__tmp13.address}/v1/'
        __tmp0._client = aiohttp.ClientSession()
        __tmp0._service_endpoint = __typ4(__tmp0._client, __tmp0._base_url)
        __tmp0._key_value_endpoint = __typ2(__tmp0._client, __tmp0._base_url)
        __tmp0._health_endpoint = __typ1(__tmp0._client, __tmp0._base_url)
        return __tmp0

    async def close(__tmp0):
        await __tmp0._client.close()
