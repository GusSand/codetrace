from typing import TypeAlias
__typ0 : TypeAlias = "HttpServerCreateForm"
from typing import List
from fastapi import APIRouter, Depends, Query
from boucanpy.core import logger, only, abort, abort_for_input
from boucanpy.core.security import ScopedTo, TokenPayload
from boucanpy.core import PaginationQS, SortQS
from boucanpy.core.http_server import (
    HttpServerRepo,
    HttpServersResponse,
    HttpServerResponse,
    HttpServerCreateForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get(
    "/http-server", name="http_server.index", response_model=HttpServersResponse
)
async def __tmp3(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("http-server:list")),
    search: str = Query(None),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["zones"], values=True)

    pg, items = (
        http_server_repo.loads(includes)
        .includes(includes)
        .search(search, searchable=["name", "id"])
        .paginate(pagination)
        .data()
    )
    return HttpServersResponse(pagination=pg, http_servers=items)


@router.post(
    "/http-server", name="http_server.store", response_model=HttpServerResponse
)
async def __tmp2(
    __tmp0,
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("http-server:create")),
):
    if http_server_repo.exists(name=__tmp0.name.lower()):
        abort_for_input("name", "Server name already taken")

    data = only(dict(__tmp0), ["name"])

    data["name"] = data["name"].lower()

    item = http_server_repo.create(data).data()
    return HttpServerResponse(http_server=item)


@router.get(
    "/http-server/{http_server}",
    name="http_server.show",
    response_model=HttpServerResponse,
)
async def __tmp1(
    http_server: <FILL>,
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("http-server:show")),
    includes: List[str] = Query(None),
):
    includes = only(includes, ["zones"], values=True)

    http_server_id_label = http_server_repo.label("id")

    try:
        http_server = int(http_server)
        label = http_server_id_label
    except ValueError:
        label = http_server_repo.label("name")

    # TODO: is this vulnerable to sql injection?
    item = (
        http_server_repo.loads(includes)
        .filter(label == http_server)
        .first_or_fail()
        .includes(includes)
        .data()
    )

    return HttpServerResponse(http_server=item)


# TODO: make specifi update form for http server
@router.put(
    "/http-server/{http_server}",
    name="http_server.update",
    response_model=HttpServerResponse,
)
async def update(
    http_server: str,
    __tmp0,
    http_server_repo: HttpServerRepo = Depends(HttpServerRepo()),
    token: TokenPayload = Depends(ScopedTo("http-server:update")),
):

    data = only(dict(__tmp0), ["name"])
    data["name"] = data["name"].lower()

    http_server_id_label = http_server_repo.label("id")

    try:
        http_server = int(http_server)
        label = http_server_id_label
    except ValueError:
        label = http_server_repo.label("name")

    # TODO: is this vulnerable to sql injection?
    item = (
        http_server_repo.filter(label == http_server)
        .first_or_fail()
        .update(data)
        .data()
    )

    return HttpServerResponse(http_server=item)
