from typing import List
from fastapi import APIRouter, Depends, Query
from boucanpy.core import logger, only, abort, abort_for_input
from boucanpy.core.security import ScopedTo, TokenPayload
from boucanpy.core import PaginationQS, SortQS
from boucanpy.core.dns_server import (
    DnsServerRepo,
    DnsServersResponse,
    DnsServerResponse,
    DnsServerCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/dns-server", name="dns_server.index", response_model=DnsServersResponse)
async def __tmp1(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-server:list")),
    search: str = Query(None),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["zones"], values=True)

    pg, items = (
        dns_server_repo.loads(includes)
        .includes(includes)
        .search(search, searchable=["name", "id"])
        .paginate(pagination)
        .data()
    )
    return DnsServersResponse(pagination=pg, dns_servers=items)


@router.post("/dns-server", name="dns_server.store", response_model=DnsServerResponse)
async def store(
    __tmp0,
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-server:create")),
):
    if dns_server_repo.exists(name=__tmp0.name.lower()):
        abort_for_input("name", "Server name already taken")

    data = only(dict(__tmp0), ["name"])

    data["name"] = data["name"].lower()

    item = dns_server_repo.create(data).data()
    return DnsServerResponse(dns_server=item)


@router.get(
    "/dns-server/{dns_server}", name="dns_server.show", response_model=DnsServerResponse
)
async def show(
    dns_server: <FILL>,
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-server:show")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["zones"], values=True)

    dns_server_id_label = dns_server_repo.label("id")

    try:
        dns_server = int(dns_server)
        label = dns_server_id_label
    except ValueError:
        label = dns_server_repo.label("name")

    # TODO: is this vulnerable to sql injection?
    item = (
        dns_server_repo.loads(includes)
        .filter(label == dns_server)
        .first_or_fail()
        .includes(includes)
        .data()
    )

    return DnsServerResponse(dns_server=item)


# TODO: make specifi update form for dns server
@router.put(
    "/dns-server/{dns_server}",
    name="dns_server.update",
    response_model=DnsServerResponse,
)
async def update(
    dns_server: str,
    __tmp0,
    dns_server_repo: DnsServerRepo = Depends(DnsServerRepo()),
    token: TokenPayload = Depends(ScopedTo("dns-server:update")),
):

    data = only(dict(__tmp0), ["name"])
    data["name"] = data["name"].lower()

    dns_server_id_label = dns_server_repo.label("id")

    try:
        dns_server = int(dns_server)
        label = dns_server_id_label
    except ValueError:
        label = dns_server_repo.label("name")

    # TODO: is this vulnerable to sql injection?
    item = (
        dns_server_repo.filter(label == dns_server).first_or_fail().update(data).data()
    )

    return DnsServerResponse(dns_server=item)
