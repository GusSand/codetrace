import typing

import dependency


def test_injection():
    """
    Test the Injector class.
    """
    class __typ0(dict):
        pass

    class __typ2(str):
        pass

    class Headers(dict):
        pass

    def __tmp17(__tmp6) :
        return __typ2(__tmp6['METHOD'])

    def __tmp7(__tmp6) :
        headers = {}
        for key, value in __tmp6.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                headers[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                headers[key] = value
        return Headers(headers)

    injector = dependency.Injector(
        providers={
            __typ2: __tmp17,
            Headers: __tmp7
        },
        required_state={
            'environ': __typ0
        }
    )

    def __tmp16(__tmp8, headers: <FILL>):
        return {'method': __tmp8, 'headers': headers}

    func = injector.inject(__tmp16)
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


def __tmp9():
    """
    Test the `@dependency.add_provider` and `@depenency.inject` wrappers.
    """
    class __typ0(dict):
        pass

    class __typ2(str):
        pass

    class Headers(dict):
        pass

    @dependency.add_provider
    def __tmp17(__tmp6) :
        return __typ2(__tmp6['METHOD'])

    @dependency.add_provider
    def __tmp7(__tmp6) :
        headers = {}
        for key, value in __tmp6.items():
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
    def __tmp16(__tmp8, headers: Headers):
        return {'method': __tmp8, 'headers': headers}

    state = {
        'environ': {
            'METHOD': 'GET',
            'CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '127.0.0.1'
        }
    }
    result = __tmp16(state=state)

    assert result == {
        'method': 'GET',
        'headers': {'content-type': 'application/json', 'host': '127.0.0.1'}
    }
    assert repr(__tmp16) == '\n'.join([
        'method = get_method(environ=environ)',
        'headers = get_headers(environ=environ)',
        'return echo_method_and_headers(method=method, headers=headers)'
    ])


def __tmp0():
    """
    Context managers should handle setup and teaddown.
    """

    class __typ1():
        events = []

        def __tmp13(__tmp2):
            pass

        def __tmp5(__tmp2):
            __tmp2.events.append('__enter__')

        def __exit__(__tmp2, *args, **kwargs):
            __tmp2.events.append('__exit__')

    injector = dependency.Injector(providers={
        __typ1: __typ1,
    })

    def do_something(__tmp14):
        pass

    func = injector.inject(do_something)
    func()

    assert __typ1.events == ['__enter__', '__exit__']
    assert repr(func) == '\n'.join([
        'with Session() as session:',
        '    return do_something(session=session)'
    ])


def __tmp12():
    """
    The ParamName class can be used to provide the parameter name
    that was used for the dependency injection.
    """
    Lookups = typing.NewType('Lookups', typing.Dict[str, int])
    __typ3 = typing.NewType('Lookup', int)

    def __tmp15(__tmp3, __tmp11):
        return __tmp11[__tmp3]

    injector = dependency.Injector(
        providers={
            __typ3: __tmp15,
        },
        required_state={
            'lookups': Lookups
        }
    )

    def __tmp4(__tmp1, __tmp10: __typ3):
        return 'a: %s, b: %s' % (__tmp1, __tmp10)

    func = injector.inject(__tmp4)

    state = {
        'lookups': {'a': 123, 'b': 456}
    }
    assert func(state=state) == 'a: 123, b: 456'
    assert repr(func) == '\n'.join([
        'lookup:a = get_lookup(lookups=lookups)',
        'lookup:b = get_lookup(lookups=lookups)',
        'return make_lookups(a=lookup:a, b=lookup:b)'
    ])
