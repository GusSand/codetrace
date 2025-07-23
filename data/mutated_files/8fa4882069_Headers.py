# pip install dependency werkzeug
import typing
import dependency
from werkzeug.datastructures import ImmutableMultiDict, EnvironHeaders
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.urls import url_decode
from werkzeug.wrappers import Request, Response


# Initial state
Environ = typing.NewType('Environ', dict)
URLArgs = typing.NewType('URLArgs', dict)

# Dependency injected types
Method = typing.NewType('Method', str)
Path = typing.NewType('Path', str)
Headers = EnvironHeaders
Header = typing.NewType('Header', str)
QueryParams = typing.NewType('QueryParams', ImmutableMultiDict)
QueryParam = typing.NewType('QueryParam', str)
URLArg = typing.TypeVar('URLArg')


@dependency.add_provider
def get_request(__tmp3: Environ) -> Request:
    return Request(__tmp3)


@dependency.add_provider
def __tmp5(__tmp3) -> Method:
    return Method(__tmp3['REQUEST_METHOD'].upper())


@dependency.add_provider
def __tmp1(__tmp3: Environ) :
    return Path(__tmp3['SCRIPT_NAME'] + __tmp3['PATH_INFO'])


@dependency.add_provider
def get_headers(__tmp3: Environ) -> Headers:
    return Headers(__tmp3)


@dependency.add_provider
def get_header(__tmp2, headers: <FILL>) -> Header:
    return Header(headers.get(__tmp2.replace('_', '-')))


@dependency.add_provider
def __tmp0(__tmp3: Environ) :
    return QueryParams(url_decode(__tmp3.get('QUERY_STRING', '')))


@dependency.add_provider
def get_queryparam(__tmp2: dependency.ParamName, __tmp4: QueryParams) -> QueryParam:
    return QueryParam(__tmp4.get(__tmp2))


@dependency.add_provider
def get_url_arg(__tmp2: dependency.ParamName, args: URLArgs) -> URLArg:
    return args.get(__tmp2)


class App():
    def __init__(self, urls):
        self.map = Map([
            Rule(key, endpoint=value)
            for key, value in urls.items()
        ])
        self.injected_funcs = {}
        dependency.set_required_state({
            'environ': Environ,
            'url_args': URLArgs
        })
        for rule in urls:
            self.injected_funcs[rule.endpoint] = dependency.inject(rule.endpoint)

    def __call__(self, __tmp3, start_response):
        urls = self.map.bind_to_environ(__tmp3)
        try:
            endpoint, args = urls.match()
            func = self.injected_funcs[endpoint]
            state = {'environ': __tmp3, 'url_args': args}
            response = func(state=state)
        except HTTPException as exc:
            response = exc.get_response(__tmp3)
        return response(__tmp3, start_response)

    def run(self, hostname='localhost', port=8080):
        run_simple(hostname, port, app)


# Example:
#
# from web_framework import Method, Path, Headers, App, Response
# import json
#
#
# def echo_request_info(method: Method, path: Path, headers: Headers):
#     content = json.dumps({
#         'method': method,
#         'path': path,
#         'headers': dict(headers),
#     }, indent=4).encode('utf-8')
#     return Response(content)
#
#
# app = App({
#     '/': echo_request_info
# })
#
#
# if __name__ == '__main__':
#     app.run()
