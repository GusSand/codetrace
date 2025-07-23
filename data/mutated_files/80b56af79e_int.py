from typing import TypeAlias
__typ0 : TypeAlias = "DnsRecordForZoneCreateForm"
from typing import List
from textwrap import dedent
from dnslib import RR, DNSRecord
from dnslib.dns import DNSError
from fastapi import APIRouter, Depends, Query
from boucanpy.core import only
from boucanpy.core.security import ScopedTo, TokenPayload
from boucanpy.core import SortQS, PaginationQS

from boucanpy.dns.parser import RecordParser

from boucanpy.core.dns_record import (
    DnsRecordsResponse,
    DnsRecordResponse,
    DnsRecordRepo,
    DnsRecordForZoneCreateForm,
    DnsRecordsDigResponse,
)
from boucanpy.core.zone import ZoneRepo

router = APIRouter()
options = {"prefix": "/zone/{zone_id}"}


@router.get(
    "/dns-record", name="zone.dns_record.index", response_model=DnsRecordsResponse
)
async def index(
    zone_id,
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:list")),
    includes: List[str] = Query(None),
):
    zone_repo.exists(id=zone_id, or_fail=True)

    includes = only(includes, ["zone"], values=True)

    pg, items = (
        dns_record_repo.loads("zone")
        .sort(sort_qs)
        .filter_by(zone_id=zone_id)
        .paginate(pagination)
        .includes(includes)
        .data()
    )
    return DnsRecordsResponse(pagination=pg, dns_records=items)


@router.get(
    "/dns-record/dig",
    name="zone.dns_record.dig.index",
    response_model=DnsRecordsDigResponse,
)
async def dig(
    zone_id: int,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:list")),
):
    zone = zone_repo.includes("dns_records").first_or_fail(id=zone_id).results()
    print(zone)
    print(zone.dns_records)
    # TODO: fix method
    rrs = RecordParser.from_zone(zone).get_rrs()
    dig = DNSRecord(rr=rrs).toZone()
    return DnsRecordsDigResponse(dig=dig)


@router.post(
    "/dns-record", name="zone.dns_record.store", response_model=DnsRecordsDigResponse
)
async def store(
    zone_id: <FILL>,
    __tmp0,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:create")),
):
    zone_repo.exists(id=zone_id, or_fail=True)

    data = only(dict(__tmp0), ["record", "sort"])
    data["zone_id"] = zone_id

    item = dns_record_repo.create(data).data()
    return DnsRecordResponse(dns_record=item)


@router.get(
    "/dns-record/{dns_record_id}",
    name="zone.dns_record.show",
    response_model=DnsRecordResponse,
)
async def __tmp1(
    zone_id,
    dns_record_id,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:show")),
    includes: List[str] = Query(None),
):
    zone_repo.exists(id=zone_id, or_fail=True)

    includes = only(includes, ["zone"], values=True)

    item = (
        dns_record_repo.loads("zone")
        .filter_by(zone_id=zone_id)
        .first_or_fail(id=dns_record_id)
        .includes(includes)
        .data()
    )

    return DnsRecordResponse(dns_record=item)


@router.put(
    "/dns-record/{dns_record_id}",
    name="zone.dns_record.update",
    response_model=DnsRecordResponse,
)
async def update(
    zone_id,
    dns_record_id,
    __tmp0: __typ0,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:create")),
):
    # TODO: use abort_for_input instead of or_fail
    zone_repo.exists(id=zone_id, or_fail=True)

    data = only(__tmp0, ["record", "sort"])

    item = dns_record_repo.first_or_fail(id=dns_record_id).update(data).data()

    return DnsRecordResponse(dns_record=item)
