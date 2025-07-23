from typing import TypeAlias
__typ0 : TypeAlias = "SimpleCookie"
import logging
import requests
import ujson

from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.middleware.csrf import _get_new_csrf_token
from importlib import import_module
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.httpclient import HTTPRequest
from tornado.websocket import websocket_connect, WebSocketClientConnection
from urllib.parse import urlparse, urlunparse, urljoin
from http.cookies import SimpleCookie

from zerver.models import get_system_bot

from typing import Any, Callable, Dict, Generator, Iterable, Optional


class __typ1:
    def __tmp4(__tmp0, __tmp2: str, sockjs_url, __tmp1: str,
                 run_on_start, validate_ssl: bool=True,
                 **run_kwargs: Any) -> None:
        # NOTE: Callable should take a WebsocketClient & kwargs, but this is not standardised
        __tmp0.validate_ssl = validate_ssl
        __tmp0.auth_email = __tmp1
        __tmp0.user_profile = get_system_bot(__tmp1)
        __tmp0.request_id_number = 0
        __tmp0.parsed_host_url = urlparse(__tmp2)
        __tmp0.sockjs_url = sockjs_url
        __tmp0.cookie_dict = __tmp0._login()
        __tmp0.cookie_str = __tmp0._get_cookie_header(__tmp0.cookie_dict)
        __tmp0.events_data = __tmp0._get_queue_events(__tmp0.cookie_str)
        __tmp0.ioloop_instance = IOLoop.instance()
        __tmp0.run_on_start = run_on_start
        __tmp0.run_kwargs = run_kwargs
        __tmp0.scheme_dict = {'http': 'ws', 'https': 'wss'}
        __tmp0.ws = None  # type: Optional[WebSocketClientConnection]

    def _login(__tmp0) -> Dict[str, str]:

        # Ideally, we'd migrate this to use API auth instead of
        # stealing cookies, but this works for now.
        auth_backend = settings.AUTHENTICATION_BACKENDS[0]
        session_auth_hash = __tmp0.user_profile.get_session_auth_hash()
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore()  # type: ignore # import_module
        session[SESSION_KEY] = __tmp0.user_profile._meta.pk.value_to_string(__tmp0.user_profile)
        session[BACKEND_SESSION_KEY] = auth_backend
        session[HASH_SESSION_KEY] = session_auth_hash
        session.save()
        return {
            settings.SESSION_COOKIE_NAME: session.session_key,
            settings.CSRF_COOKIE_NAME: _get_new_csrf_token()}

    def _get_cookie_header(__tmp0, cookies) :
        return ';'.join(
            ["{}={}".format(name, value) for name, value in cookies.items()])

    @gen.coroutine
    def _websocket_auth(__tmp0, queue_events_data,
                        cookies) -> Generator[str, str, None]:
        message = {
            "req_id": __tmp0._get_request_id(),
            "type": "auth",
            "request": {
                "csrf_token": cookies.get(settings.CSRF_COOKIE_NAME),
                "queue_id": queue_events_data['queue_id'],
                "status_inquiries": []
            }
        }
        auth_frame_str = ujson.dumps(message)
        __tmp0.ws.write_message(ujson.dumps([auth_frame_str]))
        response_ack = yield __tmp0.ws.read_message()
        response_message = yield __tmp0.ws.read_message()
        raise gen.Return([response_ack, response_message])

    def _get_queue_events(__tmp0, __tmp6: str) -> Dict[str, str]:
        url = urljoin(__tmp0.parsed_host_url.geturl(), '/json/events?dont_block=true')
        response = requests.get(url, headers={'Cookie': __tmp6}, verify=__tmp0.validate_ssl)
        return response.json()

    @gen.engine
    def connect(__tmp0) -> Generator[str, WebSocketClientConnection, None]:
        try:
            request = HTTPRequest(url=__tmp0._get_websocket_url(), validate_cert=__tmp0.validate_ssl)
            request.headers.add('Cookie', __tmp0.cookie_str)
            __tmp0.ws = yield websocket_connect(request)
            yield __tmp0.ws.read_message()
            yield __tmp0._websocket_auth(__tmp0.events_data, __tmp0.cookie_dict)
            __tmp0.run_on_start(__tmp0, **__tmp0.run_kwargs)
        except Exception as e:
            logging.exception(str(e))
            IOLoop.instance().stop()
        IOLoop.instance().stop()

    @gen.coroutine
    def __tmp7(__tmp0, client: str, type: <FILL>, subject: str, __tmp3: str,
                     private_message_recepient: str,
                     content: str="") :
        user_message = {
            "req_id": __tmp0._get_request_id(),
            "type": "request",
            "request": {
                "client": client,
                "type": type,
                "subject": subject,
                "stream": __tmp3,
                "private_message_recipient": private_message_recepient,
                "content": content,
                "sender_id": __tmp0.user_profile.id,
                "queue_id": __tmp0.events_data['queue_id'],
                "to": ujson.dumps([private_message_recepient]),
                "reply_to": __tmp0.user_profile.email,
                "local_id": -1
            }
        }
        __tmp0.ws.write_message(ujson.dumps([ujson.dumps(user_message)]))
        response_ack = yield __tmp0.ws.read_message()
        response_message = yield __tmp0.ws.read_message()
        raise gen.Return([response_ack, response_message])

    def __tmp5(__tmp0) -> None:
        __tmp0.ioloop_instance.add_callback(__tmp0.connect)
        __tmp0.ioloop_instance.start()

    def _get_websocket_url(__tmp0) -> str:
        return '{}://{}{}'.format(__tmp0.scheme_dict[__tmp0.parsed_host_url.scheme],
                                  __tmp0.parsed_host_url.netloc, __tmp0.sockjs_url)

    def _get_request_id(__tmp0) -> Iterable[str]:
        __tmp0.request_id_number += 1
        return ':'.join((__tmp0.events_data['queue_id'], str(__tmp0.request_id_number)))
