try:
    import ujson
except:
    import json as ujson
from sanic_session.base import BaseSessionInterface, SessionDict
import uuid

from typing import Callable


class RedisSessionInterface(BaseSessionInterface):
    def __tmp4(
            __tmp1, redis_getter: <FILL>,
            domain: str=None, expiry: int = 2592000,
            httponly: bool=True, cookie_name: str='session',
            prefix: str='session:'):
        """Initializes a session interface backed by Redis.
        Args:
            redis_getter (Callable):
                Coroutine which should return an asyncio_redis connection pool
                (suggested) or an asyncio_redis Redis connection.
            domain (str, optional):
                Optional domain which will be attached to the cookie.
            expiry (int, optional):
                Seconds until the session should expire.
            httponly (bool, optional):
                Adds the `httponly` flag to the session cookie.
            cookie_name (str, optional):
                Name used for the client cookie.
            prefix (str, optional):
                Memcache keys will take the format of `prefix+session_id`;
                specify the prefix here.
        """
        __tmp1.redis_getter = redis_getter
        __tmp1.expiry = expiry
        __tmp1.prefix = prefix
        __tmp1.cookie_name = cookie_name
        __tmp1.domain = domain
        __tmp1.httponly = httponly

    async def open(__tmp1, __tmp3):
        """Opens a session onto the request. Restores the client's session
        from Redis if one exists.The session data will be available on
        `request.session`.
        Args:
            request (sanic.request.Request):
                The request, which a sessionwill be opened onto.
        Returns:
            dict:
                the client's session data,
                attached as well to `request.session`.
        """
        sid = __tmp3.cookies.get(__tmp1.cookie_name)

        if not sid:
            sid = uuid.uuid4().hex
            session_dict = SessionDict(sid=sid)
        else:
            redis_pool = await __tmp1.redis_getter()
            async with redis_pool.get() as conn:
                val = await conn.execute('get', __tmp1.prefix + sid)
                if val is not None:
                    data = ujson.loads(val)
                    session_dict = SessionDict(data, sid=sid)
                else:
                    session_dict = SessionDict(sid=sid)

        __tmp3['session'] = session_dict
        return session_dict

    async def __tmp0(__tmp1, __tmp3, __tmp2) -> None:
        """Saves the session into Redis and returns appropriate cookies.
        Args:
            request (sanic.request.Request):
                The sanic request which has an attached session.
            response (sanic.response.Response):
                The Sanic response. Cookies with the appropriate expiration
                will be added onto this response.
        Returns:
            None
        """
        if 'session' not in __tmp3:
            return

        redis_pool = await __tmp1.redis_getter()
        key = __tmp1.prefix + __tmp3['session'].sid
        if not __tmp3['session']:
            async with redis_pool.get() as conn:
                await conn.execute('DEL', key)

            if __tmp3['session'].modified:
                __tmp1._delete_cookie(__tmp3, __tmp2)
            return

        val = ujson.dumps(dict(__tmp3['session']))
        async with redis_pool.get() as conn:
            await conn.execute("SETEX", key, __tmp1.expiry, val)

        __tmp1._set_cookie_expiration(__tmp3, __tmp2)
