import typing

import dependency


def test_injection():
    """
    Test the Injector class.
    """
    class __typ0(dict):
        pass

    class __typ3(str):
        pass

    class Headers(dict):
        pass

    def __tmp12(__tmp5: __typ0) -> __typ3:
        return __typ3(__tmp5['METHOD'])

    def get_headers(__tmp5) -> Headers:
        __tmp2 = {}
        for key, value in __tmp5.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                __tmp2[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                __tmp2[key] = value
        return Headers(__tmp2)

    injector = dependency.Injector(
        providers={
            __typ3: __tmp12,
            Headers: get_headers
        },
        required_state={
            'environ': __typ0
        }
    )

    def __tmp15(__tmp7: __typ3, __tmp2: Headers):
        return {'method': __tmp7, 'headers': __tmp2}

    func = injector.inject(__tmp15)
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


def __tmp8():
    """
    Test the `@dependency.add_provider` and `@depenency.inject` wrappers.
    """
    class __typ0(dict):
        pass

    class __typ3(str):
        pass

    class Headers(dict):
        pass

    @dependency.add_provider
    def __tmp12(__tmp5: __typ0) -> __typ3:
        return __typ3(__tmp5['METHOD'])

    @dependency.add_provider
    def get_headers(__tmp5: __typ0) -> Headers:
        __tmp2 = {}
        for key, value in __tmp5.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                __tmp2[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                __tmp2[key] = value
        return Headers(__tmp2)

    dependency.set_required_state({
        'environ': __typ0
    })

    @dependency.inject
    def __tmp15(__tmp7: __typ3, __tmp2: <FILL>):
        return {'method': __tmp7, 'headers': __tmp2}

    state = {
        'environ': {
            'METHOD': 'GET',
            'CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '127.0.0.1'
        }
    }
    result = __tmp15(state=state)

    assert result == {
        'method': 'GET',
        'headers': {'content-type': 'application/json', 'host': '127.0.0.1'}
    }
    assert repr(__tmp15) == '\n'.join([
        'method = get_method(environ=environ)',
        'headers = get_headers(environ=environ)',
        'return echo_method_and_headers(method=method, headers=headers)'
    ])


def __tmp0():
    """
    Context managers should handle setup and teaddown.
    """

    class __typ2():
        events = []

        def __tmp11(__tmp1):
            pass

        def __tmp4(__tmp1):
            __tmp1.events.append('__enter__')

        def __exit__(__tmp1, *args, **kwargs):
            __tmp1.events.append('__exit__')

    injector = dependency.Injector(providers={
        __typ2: __typ2,
    })

    def __tmp6(__tmp13: __typ2):
        pass

    func = injector.inject(__tmp6)
    func()

    assert __typ2.events == ['__enter__', '__exit__']
    assert repr(func) == '\n'.join([
        'with Session() as session:',
        '    return do_something(session=session)'
    ])


def test_param_name():
    """
    The ParamName class can be used to provide the parameter name
    that was used for the dependency injection.
    """
    __typ1 = typing.NewType('Lookups', typing.Dict[str, int])
    Lookup = typing.NewType('Lookup', int)

    def __tmp14(__tmp16: dependency.ParamName, __tmp10: __typ1):
        return __tmp10[__tmp16]

    injector = dependency.Injector(
        providers={
            Lookup: __tmp14,
        },
        required_state={
            'lookups': __typ1
        }
    )

    def __tmp3(a, __tmp9: Lookup):
        return 'a: %s, b: %s' % (a, __tmp9)

    func = injector.inject(__tmp3)

    state = {
        'lookups': {'a': 123, 'b': 456}
    }
    assert func(state=state) == 'a: 123, b: 456'
    assert repr(func) == '\n'.join([
        'lookup:a = get_lookup(lookups=lookups)',
        'lookup:b = get_lookup(lookups=lookups)',
        'return make_lookups(a=lookup:a, b=lookup:b)'
    ])
