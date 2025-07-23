import typing

import dependency


def test_injection():
    """
    Test the Injector class.
    """
    class __typ0(dict):
        pass

    class Method(str):
        pass

    class __typ1(dict):
        pass

    def __tmp8(__tmp3) :
        return Method(__tmp3['METHOD'])

    def __tmp4(__tmp3) :
        headers = {}
        for key, value in __tmp3.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                headers[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                headers[key] = value
        return __typ1(headers)

    injector = dependency.Injector(
        providers={
            Method: __tmp8,
            __typ1: __tmp4
        },
        required_state={
            'environ': __typ0
        }
    )

    def __tmp7(__tmp5, headers):
        return {'method': __tmp5, 'headers': headers}

    func = injector.inject(__tmp7)
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

    class Method(str):
        pass

    class __typ1(dict):
        pass

    @dependency.add_provider
    def __tmp8(__tmp3) :
        return Method(__tmp3['METHOD'])

    @dependency.add_provider
    def __tmp4(__tmp3) :
        headers = {}
        for key, value in __tmp3.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                headers[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                headers[key] = value
        return __typ1(headers)

    dependency.set_required_state({
        'environ': __typ0
    })

    @dependency.inject
    def __tmp7(__tmp5: <FILL>, headers):
        return {'method': __tmp5, 'headers': headers}

    state = {
        'environ': {
            'METHOD': 'GET',
            'CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '127.0.0.1'
        }
    }
    result = __tmp7(state=state)

    assert result == {
        'method': 'GET',
        'headers': {'content-type': 'application/json', 'host': '127.0.0.1'}
    }
    assert repr(__tmp7) == '\n'.join([
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

        def __init__(__tmp1):
            pass

        def __tmp2(__tmp1):
            __tmp1.events.append('__enter__')

        def __exit__(__tmp1, *args, **kwargs):
            __tmp1.events.append('__exit__')

    injector = dependency.Injector(providers={
        Session: Session,
    })

    def do_something(session):
        pass

    func = injector.inject(do_something)
    func()

    assert Session.events == ['__enter__', '__exit__']
    assert repr(func) == '\n'.join([
        'with Session() as session:',
        '    return do_something(session=session)'
    ])


def __tmp6():
    """
    The ParamName class can be used to provide the parameter name
    that was used for the dependency injection.
    """
    Lookups = typing.NewType('Lookups', typing.Dict[str, int])
    Lookup = typing.NewType('Lookup', int)

    def get_lookup(name, lookups):
        return lookups[name]

    injector = dependency.Injector(
        providers={
            Lookup: get_lookup,
        },
        required_state={
            'lookups': Lookups
        }
    )

    def make_lookups(__tmp0, b):
        return 'a: %s, b: %s' % (__tmp0, b)

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
