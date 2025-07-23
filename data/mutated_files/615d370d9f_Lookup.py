import typing

import dependency


def __tmp2():
    """
    Test the Injector class.
    """
    class __typ0(dict):
        pass

    class __typ1(str):
        pass

    class Headers(dict):
        pass

    def get_method(environ) :
        return __typ1(environ['METHOD'])

    def get_headers(environ) -> Headers:
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                headers[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                headers[key] = value
        return Headers(headers)

    injector = dependency.Injector(
        providers={
            __typ1: get_method,
            Headers: get_headers
        },
        required_state={
            'environ': __typ0
        }
    )

    def echo_method_and_headers(__tmp3, headers: Headers):
        return {'method': __tmp3, 'headers': headers}

    func = injector.inject(echo_method_and_headers)
    state = {
        'environ': {
            'METHOD': 'GET',
            'CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '127.0.0.1'
        }
    }
    result = func(state=state)

    assert result == {
        'method': 'GET',
        'headers': {'content-type': 'application/json', 'host': '127.0.0.1'}
    }
    assert repr(func) == '\n'.join([
        'method = get_method(environ=environ)',
        'headers = get_headers(environ=environ)',
        'return echo_method_and_headers(method=method, headers=headers)'
    ])


def test_wrappers():
    """
    Test the `@dependency.add_provider` and `@depenency.inject` wrappers.
    """
    class __typ0(dict):
        pass

    class __typ1(str):
        pass

    class Headers(dict):
        pass

    @dependency.add_provider
    def get_method(environ: __typ0) :
        return __typ1(environ['METHOD'])

    @dependency.add_provider
    def get_headers(environ) -> Headers:
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                headers[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                headers[key] = value
        return Headers(headers)

    dependency.set_required_state({
        'environ': __typ0
    })

    @dependency.inject
    def echo_method_and_headers(__tmp3, headers: Headers):
        return {'method': __tmp3, 'headers': headers}

    state = {
        'environ': {
            'METHOD': 'GET',
            'CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '127.0.0.1'
        }
    }
    result = echo_method_and_headers(state=state)

    assert result == {
        'method': 'GET',
        'headers': {'content-type': 'application/json', 'host': '127.0.0.1'}
    }
    assert repr(echo_method_and_headers) == '\n'.join([
        'method = get_method(environ=environ)',
        'headers = get_headers(environ=environ)',
        'return echo_method_and_headers(method=method, headers=headers)'
    ])


def test_context_manager():
    """
    Context managers should handle setup and teaddown.
    """

    class Session():
        events = []

        def __init__(self):
            pass

        def __enter__(self):
            self.events.append('__enter__')

        def __exit__(self, *args, **kwargs):
            self.events.append('__exit__')

    injector = dependency.Injector(providers={
        Session: Session,
    })

    def __tmp1(session):
        pass

    func = injector.inject(__tmp1)
    func()

    assert Session.events == ['__enter__', '__exit__']
    assert repr(func) == '\n'.join([
        'with Session() as session:',
        '    return do_something(session=session)'
    ])


def test_param_name():
    """
    The ParamName class can be used to provide the parameter name
    that was used for the dependency injection.
    """
    Lookups = typing.NewType('Lookups', typing.Dict[str, int])
    Lookup = typing.NewType('Lookup', int)

    def get_lookup(name, lookups: Lookups):
        return lookups[name]

    injector = dependency.Injector(
        providers={
            Lookup: get_lookup,
        },
        required_state={
            'lookups': Lookups
        }
    )

    def make_lookups(a: <FILL>, __tmp0: Lookup):
        return 'a: %s, b: %s' % (a, __tmp0)

    func = injector.inject(make_lookups)

    state = {
        'lookups': {'a': 123, 'b': 456}
    }
    assert func(state=state) == 'a: 123, b: 456'
    assert repr(func) == '\n'.join([
        'lookup:a = get_lookup(lookups=lookups)',
        'lookup:b = get_lookup(lookups=lookups)',
        'return make_lookups(a=lookup:a, b=lookup:b)'
    ])
