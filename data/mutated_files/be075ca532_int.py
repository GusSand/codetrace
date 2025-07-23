from fastapi import APIRouter, Depends, Query
from typing import List
from boucanpy.core.security import ScopedTo, TokenPayload
from boucanpy.core import logger, only, abort, abort_for_input

from boucanpy.core import SortQS, PaginationQS, BaseResponse
from boucanpy.core.dns_server import DnsServerRepo
from boucanpy.core.http_server import HttpServerRepo

from boucanpy.core.zone import (
    ZoneRepo,
    ZonesResponse,
    ZoneResponse,
    ZoneData,
    ZoneCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/zone", name="zone.index", response_model=ZonesResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:list")),
    includes: List[str] = Query(None),
):
    # TODO: bypasses a bunch of scopes, find a way to restrict access via scopes
    includes = only(includes, ["dns_server", "dns_records", "http_server"], values=True)

    pg, items = (
        zone_repo.loads(includes)
        .strict()
        .sort(sort_qs)
        .paginate(pagination)
        .includes(includes)
        .data()
    )
    return ZonesResponse(pagination=pg, zones=items)


@router.post("/zone", name="zone.store", response_model=ZoneResponse)
async def __tmp2(
    __tmp0,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:create")),
):

    data = only(dict(__tmp0), ["ip", "domain"])

    data["domain"] = data["domain"].lower()

    # Make sure domain is unique

    if zone_repo.exists(domain=data["domain"]):
        abort_for_input("domain", "A Zone with that domain already exists")

    zone_repo.clear()

    if __tmp0.dns_server_id:
        if dns_server_repo.exists(id=__tmp0.dns_server_id):
            data["dns_server_id"] = dns_server_repo.results().id

    if __tmp0.http_server_id:
        if http_server_repo.exists(id=__tmp0.http_server_id):
            data["http_server_id"] = http_server_repo.results().id

    zone = zone_repo.create(data).data()
    return ZoneResponse(zone=zone)


@router.get("/zone/{zone_id}", name="zone.show", response_model=ZoneResponse)
async def show(
    __tmp3: <FILL>,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:show")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["dns_server", "dns_records", "http_server"], values=True)

    zone = zone_repo.loads(includes).get_or_fail(__tmp3).includes(includes).data()
    return ZoneResponse(zone=zone)


# TODO: make custom update form for zone
@router.put("/zone/{zone_id}", name="zone.update", response_model=ZoneResponse)
async def update(
    __tmp3,
    __tmp0,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    http_server_repo: DnsServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:update")),
    includes: List[str] = Query(None),
):
    data = only(dict(__tmp0), ["ip", "domain"])

    if "domain" in data:
        data["domain"] = data["domain"].lower()
        existing_domain = zone_repo.first(domain=data["domain"]).results()
        if existing_domain and existing_domain.id != __tmp3:
            abort_for_input("domain", "A Zone with that domain already exists")
        zone_repo.clear()

    if __tmp0.dns_server_id is not None:
        if __tmp0.dns_server_id is 0:
            data["dns_server_id"] = None
        elif dns_server_repo.exists(id=__tmp0.dns_server_id):
            dns_server = dns_server_repo.results()
            data["dns_server"] = dns_server

    if __tmp0.http_server_id is not None:
        if __tmp0.http_server_id is 0:
            data["http_server_id"] = None
        elif http_server_repo.exists(id=__tmp0.http_server_id):
            http_server = http_server_repo.results()
            data["http_server"] = http_server

    zone = (
        zone_repo.loads(includes)
        .get_or_fail(__tmp3)
        .update(data)
        .includes(includes)
        .data()
    )
    return ZoneResponse(zone=zone)


@router.put(
    "/zone/{zone_id}/activate", name="zone.activate", response_model=ZoneResponse
)
async def __tmp1(
    __tmp3,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:update")),
):
    zone = zone_repo.get_or_fail(__tmp3).update({"is_active": True}).data()
    return ZoneResponse(zone=zone)


@router.delete("/zone/{zone_id}", name="zone.destroy", response_model=BaseResponse)
async def destroy(
    __tmp3,
    zone_repo: ZoneRepo = Depends(ZoneRepo()),
    token: TokenPayload = Depends(ScopedTo("zone:destroy")),
):
    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not zone_repo.exists(__tmp3):
        return BaseResponse(messages=messages)
    zone_repo.deactivate(__tmp3)
    return BaseResponse(messages=messages)
