import typing

import dependency


def test_injection():
    """
    Test the Injector class.
    """
    class __typ3(dict):
        pass

    class Method(str):
        pass

    class __typ1(dict):
        pass

    def __tmp14(__tmp6) :
        return Method(__tmp6['METHOD'])

    def get_headers(__tmp6) :
        __tmp4 = {}
        for key, value in __tmp6.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                __tmp4[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                __tmp4[key] = value
        return __typ1(__tmp4)

    injector = dependency.Injector(
        providers={
            Method: __tmp14,
            __typ1: get_headers
        },
        required_state={
            'environ': __typ3
        }
    )

    def __tmp13(__tmp7: <FILL>, __tmp4: __typ1):
        return {'method': __tmp7, 'headers': __tmp4}

    func = injector.inject(__tmp13)
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
    class __typ3(dict):
        pass

    class Method(str):
        pass

    class __typ1(dict):
        pass

    @dependency.add_provider
    def __tmp14(__tmp6) :
        return Method(__tmp6['METHOD'])

    @dependency.add_provider
    def get_headers(__tmp6) :
        __tmp4 = {}
        for key, value in __tmp6.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                __tmp4[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                __tmp4[key] = value
        return __typ1(__tmp4)

    dependency.set_required_state({
        'environ': __typ3
    })

    @dependency.inject
    def __tmp13(__tmp7: Method, __tmp4):
        return {'method': __tmp7, 'headers': __tmp4}

    state = {
        'environ': {
            'METHOD': 'GET',
            'CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '127.0.0.1'
        }
    }
    result = __tmp13(state=state)

    assert result == {
        'method': 'GET',
        'headers': {'content-type': 'application/json', 'host': '127.0.0.1'}
    }
    assert repr(__tmp13) == '\n'.join([
        'method = get_method(environ=environ)',
        'headers = get_headers(environ=environ)',
        'return echo_method_and_headers(method=method, headers=headers)'
    ])


def __tmp0():
    """
    Context managers should handle setup and teaddown.
    """

    class __typ4():
        events = []

        def __init__(__tmp2):
            pass

        def __tmp5(__tmp2):
            __tmp2.events.append('__enter__')

        def __exit__(__tmp2, *args, **kwargs):
            __tmp2.events.append('__exit__')

    injector = dependency.Injector(providers={
        __typ4: __typ4,
    })

    def __tmp8(session):
        pass

    func = injector.inject(__tmp8)
    func()

    assert __typ4.events == ['__enter__', '__exit__']
    assert repr(func) == '\n'.join([
        'with Session() as session:',
        '    return do_something(session=session)'
    ])


def __tmp11():
    """
    The ParamName class can be used to provide the parameter name
    that was used for the dependency injection.
    """
    __typ0 = typing.NewType('Lookups', typing.Dict[str, int])
    __typ2 = typing.NewType('Lookup', int)

    def __tmp12(__tmp3: dependency.ParamName, __tmp10):
        return __tmp10[__tmp3]

    injector = dependency.Injector(
        providers={
            __typ2: __tmp12,
        },
        required_state={
            'lookups': __typ0
        }
    )

    def make_lookups(__tmp1, __tmp9):
        return 'a: %s, b: %s' % (__tmp1, __tmp9)

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
