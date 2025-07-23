from typing import Optional, List, ForwardRef
from pydantic import ConstrainedStr, SecretStr, BaseModel
from pydantic.utils import validate_email
from dnslib import RR
from dnslib.dns import DNSError
from datetime import datetime


class ConstrainedSecretStr(ConstrainedStr):
    min_length: Optional[int] = 8
    max_length: Optional[int] = 1024

    @classmethod
    def validate(__tmp3, __tmp1) :
        return __tmp3(__tmp1)

    def __tmp4(__tmp0, __tmp1: <FILL>):
        __tmp0._secret_value = __tmp1

    def __repr__(__tmp0) -> str:
        return "SecretStr('**********')" if __tmp0._secret_value else "SecretStr('')"

    def __tmp6(__tmp0) -> str:
        return __tmp0.__repr__()

    def __tmp5(__tmp0) :
        return "**********" if __tmp0._secret_value else ""

    def __tmp2(__tmp0) :
        return __tmp0._secret_value


class ConstrainedTokenStr(ConstrainedSecretStr):
    max_length: Optional[int] = 2048


class ConstrainedEmailStr(ConstrainedStr):
    min_length: Optional[int] = 8
    max_length: Optional[int] = 255

    @classmethod
    def validate(__tmp3, v):
        v = super().validate(v)
        return validate_email(v)[1]


class __typ0(ConstrainedStr):
    min_length: Optional[int] = 8
    max_length: Optional[int] = 1024

    @classmethod
    def validate(__tmp3, v):
        v = super().validate(v)
        try:
            RR.fromZone(v)
        except Exception as e:
            msg = str(e)
            raise ValueError(f"could not cast record: {msg}")
        return v


class DnsServerData(BaseModel):
    id: int
    name: str
    zones: Optional[List[ForwardRef("ZoneData")]]
    created_at: datetime


class __typ3(BaseModel):
    id: int
    name: str
    zones: Optional[List[ForwardRef("ZoneData")]]
    created_at: datetime


class DnsRecordData(BaseModel):
    id: int
    record: str
    sort: int
    zone_id: int
    # zone: Optional[ZoneData]


class __typ2(BaseModel):
    id: int
    ip: str
    domain: str
    is_active: bool
    dns_server_id: Optional[int]
    dns_server: Optional[DnsServerData]
    dns_records: Optional[List[DnsRecordData]]
    http_server_id: Optional[int]
    http_server: Optional[__typ3]
    created_at: datetime


class DnsRequestData(BaseModel):
    id: int
    name: str
    zone_id: int = None
    source_address: str
    source_port: int
    type: str
    protocol: str
    dns_server_id: int
    created_at: datetime
    raw_request: str
    dns_server: Optional[DnsServerData]


class HttpRequestData(BaseModel):
    id: int
    name: str
    path: str
    zone_id: int = None
    source_address: str
    source_port: int
    type: str
    protocol: str
    raw_request: str
    http_server_id: int
    http_server: Optional[__typ3]
    created_at: datetime


class ApiTokenData(BaseModel):
    id: int
    scopes: str
    is_active: bool
    expires_at: datetime
    dns_server_id: Optional[int] = None
    dns_server: Optional[DnsServerData]
    http_server_id: Optional[int] = None
    http_server: Optional[__typ3]
    created_at: datetime


class __typ1(ApiTokenData):
    token: str


DnsServerData.update_forward_refs()
__typ3.update_forward_refs()
