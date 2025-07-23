from typing import TypeAlias
__typ0 : TypeAlias = "dict"
__typ2 : TypeAlias = "User"
__typ1 : TypeAlias = "TokenPayload"
from datetime import timedelta, datetime
from typing import List
import jwt
from starlette.requests import Request
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from boucanpy.core import logger, abort
from boucanpy.core.token import TokenPayload
from boucanpy.core.user import UserRepo
from boucanpy.core.black_listed_token import BlackListedTokenRepo

from boucanpy.db.models.user import User

DEFAULT_TOKEN_URL = "/api/v1/auth/token"

oauth2 = OAuth2PasswordBearer(tokenUrl=DEFAULT_TOKEN_URL)

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return context.verify(plain_password, hashed_password)


def hash_password(password: <FILL>):
    return context.hash(password)


def create_bearer_token(
    *, data: __typ0, expires_delta: timedelta = None, expire: datetime = None
):
    from boucanpy.api import config  # environment must be loaded

    if not expires_delta:
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if not expire:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.API_SECRET_KEY, algorithm=config.JWT_ALGORITHM
    )

    return str(encoded_jwt.decode())


def __tmp0(token, bl_token_repo=None, leeway=0) :
    from boucanpy.api import config  # environment must be loaded

    if bl_token_repo:
        if bl_token_repo.exists(token=token):
            raise HTTPException(status_code=403, detail="Forbidden")
    else:
        logger.warning("verifying token without checking the blacklist. dangerous!")
    try:
        payload = jwt.decode(
            token, config.API_SECRET_KEY, algorithms=config.JWT_ALGORITHM, leeway=leeway
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Forbidden")

    return __typ1(
        payload=payload,
        scopes=payload.get("scopes", "").split(" "),
        token=token,
        sub=payload.get("sub", ""),
        exp=payload.get("exp", ""),
    )


def token_has_required_scopes(token_payload, scopes):
    token_scopes = token_payload.scopes
    required_scopes = scopes or []
    for required_scope in required_scopes:
        satisfied = False
        for token_scope in token_scopes:
            if token_scope == required_scope:
                satisfied = True
            # probably bad / too generous
            # a:b in a:b:c
            elif token_scope in required_scope:
                satisfied = True
        if not satisfied:
            logger.critical(f"auth token missing scope: {required_scope}")

            return False
    return True


def token_has_one_required_scopes(token_payload, scopes):
    token_scopes = token_payload.scopes
    required_scopes = scopes or []
    for required_scope in required_scopes:
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    logger.critical(f"auth token missing at least one scope: {required_scope}")
    return False


class ScopedTo:
    def __init__(self, *scopes, leeway=0, satisfy="all") :
        self._scopes = scopes
        self._leeway = leeway
        self._satisfy = satisfy

    async def __call__(
        self,
        request,
        bl_token_repo: BlackListedTokenRepo = Depends(BlackListedTokenRepo()),
        token: str = Security(oauth2),
    ) :

        token = __tmp0(
            token, bl_token_repo, self._leeway
        )  # proper validation goes here
        if self._satisfy not in ["all", "one"]:
            logger.warning(f"Invalid satisfy value: {self._satisfy}")

        if self._satisfy == "one":
            if not token_has_one_required_scopes(token, self._scopes):
                vmsg = f"Token does not have one of the required scopes: {str(self._scopes)}"
                logger.error(vmsg)
                abort(code=403, msg="Forbidden", debug=vmsg)
        else:
            if not token_has_required_scopes(token, self._scopes):
                vmsg = f"Token does not have all required scopes: {str(self._scopes)}"
                logger.error(vmsg)
                abort(code=403, msg="Forbidden", debug=vmsg)
        return token


async def current_user(
    token: __typ1 = Depends(ScopedTo()), user_repo: UserRepo = Depends(UserRepo())
) :
    user = user_repo.get_by_sub(token.sub)
    if not user:
        raise HTTPException(404, detail="Not Found")
    return user
