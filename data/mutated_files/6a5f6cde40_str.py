from typing import TypeAlias
__typ1 : TypeAlias = "Any"
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


class WebsocketClient:
    def __init__(__tmp2, host_url: str, sockjs_url: str, __tmp0: str,
                 run_on_start: Callable[..., None], validate_ssl: bool=True,
                 **run_kwargs) :
        # NOTE: Callable should take a WebsocketClient & kwargs, but this is not standardised
        __tmp2.validate_ssl = validate_ssl
        __tmp2.auth_email = __tmp0
        __tmp2.user_profile = get_system_bot(__tmp0)
        __tmp2.request_id_number = 0
        __tmp2.parsed_host_url = urlparse(host_url)
        __tmp2.sockjs_url = sockjs_url
        __tmp2.cookie_dict = __tmp2._login()
        __tmp2.cookie_str = __tmp2._get_cookie_header(__tmp2.cookie_dict)
        __tmp2.events_data = __tmp2._get_queue_events(__tmp2.cookie_str)
        __tmp2.ioloop_instance = IOLoop.instance()
        __tmp2.run_on_start = run_on_start
        __tmp2.run_kwargs = run_kwargs
        __tmp2.scheme_dict = {'http': 'ws', 'https': 'wss'}
        __tmp2.ws = None  # type: Optional[WebSocketClientConnection]

    def _login(__tmp2) :

        # Ideally, we'd migrate this to use API auth instead of
        # stealing cookies, but this works for now.
        auth_backend = settings.AUTHENTICATION_BACKENDS[0]
        session_auth_hash = __tmp2.user_profile.get_session_auth_hash()
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore()  # type: ignore # import_module
        session[SESSION_KEY] = __tmp2.user_profile._meta.pk.value_to_string(__tmp2.user_profile)
        session[BACKEND_SESSION_KEY] = auth_backend
        session[HASH_SESSION_KEY] = session_auth_hash
        session.save()
        return {
            settings.SESSION_COOKIE_NAME: session.session_key,
            settings.CSRF_COOKIE_NAME: _get_new_csrf_token()}

    def _get_cookie_header(__tmp2, cookies) :
        return ';'.join(
            ["{}={}".format(name, value) for name, value in cookies.items()])

    @gen.coroutine
    def _websocket_auth(__tmp2, queue_events_data,
                        cookies) :
        message = {
            "req_id": __tmp2._get_request_id(),
            "type": "auth",
            "request": {
                "csrf_token": cookies.get(settings.CSRF_COOKIE_NAME),
                "queue_id": queue_events_data['queue_id'],
                "status_inquiries": []
            }
        }
        auth_frame_str = ujson.dumps(message)
        __tmp2.ws.write_message(ujson.dumps([auth_frame_str]))
        response_ack = yield __tmp2.ws.read_message()
        response_message = yield __tmp2.ws.read_message()
        raise gen.Return([response_ack, response_message])

    def _get_queue_events(__tmp2, cookies_header) -> Dict[str, str]:
        url = urljoin(__tmp2.parsed_host_url.geturl(), '/json/events?dont_block=true')
        response = requests.get(url, headers={'Cookie': cookies_header}, verify=__tmp2.validate_ssl)
        return response.json()

    @gen.engine
    def connect(__tmp2) -> Generator[str, WebSocketClientConnection, None]:
        try:
            request = HTTPRequest(url=__tmp2._get_websocket_url(), validate_cert=__tmp2.validate_ssl)
            request.headers.add('Cookie', __tmp2.cookie_str)
            __tmp2.ws = yield websocket_connect(request)
            yield __tmp2.ws.read_message()
            yield __tmp2._websocket_auth(__tmp2.events_data, __tmp2.cookie_dict)
            __tmp2.run_on_start(__tmp2, **__tmp2.run_kwargs)
        except Exception as e:
            logging.exception(str(e))
            IOLoop.instance().stop()
        IOLoop.instance().stop()

    @gen.coroutine
    def send_message(__tmp2, client: <FILL>, type, subject: str, stream: str,
                     __tmp1,
                     content: str="") -> Generator[str, WebSocketClientConnection, None]:
        user_message = {
            "req_id": __tmp2._get_request_id(),
            "type": "request",
            "request": {
                "client": client,
                "type": type,
                "subject": subject,
                "stream": stream,
                "private_message_recipient": __tmp1,
                "content": content,
                "sender_id": __tmp2.user_profile.id,
                "queue_id": __tmp2.events_data['queue_id'],
                "to": ujson.dumps([__tmp1]),
                "reply_to": __tmp2.user_profile.email,
                "local_id": -1
            }
        }
        __tmp2.ws.write_message(ujson.dumps([ujson.dumps(user_message)]))
        response_ack = yield __tmp2.ws.read_message()
        response_message = yield __tmp2.ws.read_message()
        raise gen.Return([response_ack, response_message])

    def run(__tmp2) :
        __tmp2.ioloop_instance.add_callback(__tmp2.connect)
        __tmp2.ioloop_instance.start()

    def _get_websocket_url(__tmp2) -> str:
        return '{}://{}{}'.format(__tmp2.scheme_dict[__tmp2.parsed_host_url.scheme],
                                  __tmp2.parsed_host_url.netloc, __tmp2.sockjs_url)

    def _get_request_id(__tmp2) -> Iterable[str]:
        __tmp2.request_id_number += 1
        return ':'.join((__tmp2.events_data['queue_id'], str(__tmp2.request_id_number)))
