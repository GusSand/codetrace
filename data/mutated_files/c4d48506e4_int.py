from typing import TypeAlias
__typ0 : TypeAlias = "Request"
from fastapi import APIRouter, Depends, Query
from typing import List
from starlette.responses import RedirectResponse
from starlette.requests import Request
from boucanpy.core import only, logger
from boucanpy.core.security import ScopedTo, TokenPayload

from boucanpy.core.dns_record import (
    DnsRecordsResponse,
    DnsRecordResponse,
    DnsRecordRepo,
    DnsRecordForZoneCreateForm,
)

from boucanpy.core import SortQS, PaginationQS, BaseResponse

router = APIRouter()
options = {"prefix": ""}


@router.get("/dns-record", name="dns_record.index", response_model=DnsRecordsResponse)
async def __tmp4(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:list")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["zone"], values=True)

    pg, items = (
        dns_record_repo.loads("zone")
        .sort(sort_qs)
        .paginate(pagination)
        .includes(includes)
        .data()
    )

    return DnsRecordsResponse(pagination=pg, dns_records=items)


@router.post("/dns-record", name="dns_record.store")
async def store(request, form: DnsRecordForZoneCreateForm = Depends()):
    return RedirectResponse(
        url=request.url_for("zone.dns_record.store", zone_id=form.zone_id),
        status_code=307,
    )


@router.get(
    "/dns-record/{dns_record_id}",
    name="dns_record.show",
    response_model=DnsRecordResponse,
)
async def __tmp3(
    __tmp2: int,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:show")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["zone"], values=True)

    item = (
        dns_record_repo.loads("zone")
        .first_or_fail(id=__tmp2)
        .includes(includes)
        .data()
    )

    return DnsRecordResponse(dns_record=item)


# TODO: create update form for dns record
@router.put("/dns-record/{dns_record_id}", name="dns_record.update")
async def __tmp1(
    __tmp2: <FILL>, request, form: DnsRecordForZoneCreateForm = Depends()
):
    return RedirectResponse(
        url=request.url_for(
            "zone.dns_record.update", zone_id=form.zone_id, __tmp2=__tmp2
        ),
        status_code=307,
    )


@router.delete(
    "/dns-record/{dns_record_id}",
    name="dns_record.destroy",
    response_model=BaseResponse,
)
async def __tmp0(
    __tmp2,
    dns_record_repo: DnsRecordRepo = Depends(DnsRecordRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-record:destroy")),
):

    dns_record_repo.first_or_fail(id=__tmp2).delete()
    messages = [{"text": "Delete Succesful", "type": "success"}]
    return BaseResponse(messages=messages)
