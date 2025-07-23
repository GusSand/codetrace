from typing import TypeAlias
__typ0 : TypeAlias = "UserEditForm"
from typing import List
from boucanpy.core import Depends
from fastapi import APIRouter, Query
from boucanpy.db.models.user import User
from boucanpy.core.security import ScopedTo, hash_password, TokenPayload, current_user
from boucanpy.core import (
    PaginationQS,
    SortQS,
    BaseResponse,
    abort,
    only,
    abort_for_input,
    logger,
)
from boucanpy.core.user import (
    UserRepo,
    UsersResponse,
    UserResponse,
    UserData,
    UserCreateForm,
    UserEditForm,
)

router = APIRouter()
options = {"prefix": ""}


@router.get("/user", name="user.index", response_model=UsersResponse)
async def index(
    sort_qs: SortQS = Depends(SortQS),
    pagination: PaginationQS = Depends(PaginationQS),
    user_repo: UserRepo = Depends(UserRepo()),
    token: TokenPayload = Depends(ScopedTo("user:list")),
):
    pg, items = user_repo.sort(sort_qs).paginate(pagination).data()
    return UsersResponse(pagination=pg, users=items)


@router.post("/user", name="user.store", response_model=UserResponse)
async def store(
    form: UserCreateForm,
    user_repo: UserRepo = Depends(UserRepo()),
    token: TokenPayload = Depends(ScopedTo("user:create", "super", satisfy="one")),
):

    if user_repo.exists(email=form.email):
        abort_for_input("email", "Email has already been taken.")

    user_repo.clear()

    # TODO: data validation against current db & perm checks
    data = {
        "email": form.email,
        "hashed_password": hash_password(form.password),
        "is_active": getattr(form, "is_superuser", True),
        "is_superuser": getattr(form, "is_superuser", False),
    }
    item = user_repo.create(data).data()
    return UserResponse(user=item)


@router.get("/user/{user_id}", name="user.show", response_model=UserResponse)
async def show(
    __tmp0: int,
    user_repo: UserRepo = Depends(UserRepo()),
    token: TokenPayload = Depends(ScopedTo("user:show", "super")),
    includes: List[str] = Query(None),
):
    includes = only(includes, [], values=True)

    item = user_repo.loads(includes).get_or_fail(__tmp0).includes(includes).data()
    return UserResponse(user=item)


@router.put("/user/{user_id}", name="user.update", response_model=UserResponse)
async def update(
    __tmp0: int,
    form,
    user_repo: UserRepo = Depends(UserRepo()),
    token: TokenPayload = Depends(ScopedTo("user:update", "super", satisfy="one")),
):

    email = getattr(form, "email", None)
    if email:
        for u in user_repo.new().all().results():
            print("USER:", u.id, u.email, u)
        existing = user_repo.new().first(email=email).results()
        if existing and existing.id != __tmp0:
            abort_for_input(msg="Invalid Email Address", code=422, field="email")

    data = only(form, ["email", "is_active", "is_superuser"])

    if getattr(form, "password", None):
        data["hashed_password"] = hash_password(form.password)

    item = user_repo.new().get_or_fail(__tmp0).update(data).data()
    return UserResponse(user=item)


@router.put(
    "/user/{user_id}/activate", name="user.activate", response_model=UserResponse
)
async def activate(
    __tmp0: <FILL>,
    user_repo: UserRepo = Depends(UserRepo()),
    token: TokenPayload = Depends(ScopedTo("user:create", "super")),
):

    user = user_repo.get_or_fail(__tmp0).update({"is_active": True}).data()
    return UserResponse(user=user)


@router.delete("/user/{user_id}", response_model=BaseResponse)
async def destroy(
    __tmp0,
    user_repo: UserRepo = Depends(UserRepo()),
    token: TokenPayload = Depends(ScopedTo("user:create", "super", satisfy="one")),
    user: User = Depends(current_user),
):
    if __tmp0 == user.id:
        abort(403, msg="Cannot deactivate self")

    remaining_supers = len(
        user_repo.filter(
            user_repo.label("is_superuser") == True,
            user_repo.label("is_active") == True,
            user_repo.label("id") != __tmp0,
        )
        .all()
        .results()
    )

    if remaining_supers < 1:
        abort(403, msg="Cannot deactivate user. No other active super users available.")

    user_repo.clear()

    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not user_repo.exists(id=__tmp0):
        return BaseResponse(messages=messages)

    user_repo.deactivate(__tmp0)
    return BaseResponse(messages=messages)
