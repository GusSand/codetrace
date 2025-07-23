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
    def validate(__tmp2, __tmp0: <FILL>) :
        return __tmp2(__tmp0)

    def __init__(__tmp1, __tmp0):
        __tmp1._secret_value = __tmp0

    def __repr__(__tmp1) :
        return "SecretStr('**********')" if __tmp1._secret_value else "SecretStr('')"

    def __str__(__tmp1) :
        return __tmp1.__repr__()

    def display(__tmp1) :
        return "**********" if __tmp1._secret_value else ""

    def get_secret_value(__tmp1) :
        return __tmp1._secret_value


class ConstrainedTokenStr(ConstrainedSecretStr):
    max_length: Optional[int] = 2048


class __typ0(ConstrainedStr):
    min_length: Optional[int] = 8
    max_length: Optional[int] = 255

    @classmethod
    def validate(__tmp2, v):
        v = super().validate(v)
        return validate_email(v)[1]


class __typ3(ConstrainedStr):
    min_length: Optional[int] = 8
    max_length: Optional[int] = 1024

    @classmethod
    def validate(__tmp2, v):
        v = super().validate(v)
        try:
            RR.fromZone(v)
        except Exception as e:
            msg = str(e)
            raise ValueError(f"could not cast record: {msg}")
        return v


class __typ4(BaseModel):
    id: int
    name: str
    zones: Optional[List[ForwardRef("ZoneData")]]
    created_at: datetime


class HttpServerData(BaseModel):
    id: int
    name: str
    zones: Optional[List[ForwardRef("ZoneData")]]
    created_at: datetime


class __typ6(BaseModel):
    id: int
    record: str
    sort: int
    zone_id: int
    # zone: Optional[ZoneData]


class ZoneData(BaseModel):
    id: int
    ip: str
    domain: str
    is_active: bool
    dns_server_id: Optional[int]
    dns_server: Optional[__typ4]
    dns_records: Optional[List[__typ6]]
    http_server_id: Optional[int]
    http_server: Optional[HttpServerData]
    created_at: datetime


class __typ2(BaseModel):
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
    dns_server: Optional[__typ4]


class __typ5(BaseModel):
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
    http_server: Optional[HttpServerData]
    created_at: datetime


class __typ1(BaseModel):
    id: int
    scopes: str
    is_active: bool
    expires_at: datetime
    dns_server_id: Optional[int] = None
    dns_server: Optional[__typ4]
    http_server_id: Optional[int] = None
    http_server: Optional[HttpServerData]
    created_at: datetime


class SensitiveApiTokenData(__typ1):
    token: str


__typ4.update_forward_refs()
HttpServerData.update_forward_refs()
