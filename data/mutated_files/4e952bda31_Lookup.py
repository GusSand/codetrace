import typing

import dependency


def __tmp16():
    """
    Test the Injector class.
    """
    class __typ0(dict):
        pass

    class __typ1(str):
        pass

    class __typ3(dict):
        pass

    def __tmp11(__tmp12) :
        return __typ1(__tmp12['METHOD'])

    def __tmp13(__tmp12) :
        __tmp5 = {}
        for key, value in __tmp12.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                __tmp5[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                __tmp5[key] = value
        return __typ3(__tmp5)

    injector = dependency.Injector(
        providers={
            __typ1: __tmp11,
            __typ3: __tmp13
        },
        required_state={
            'environ': __typ0
        }
    )

    def __tmp10(__tmp14: __typ1, __tmp5: __typ3):
        return {'method': __tmp14, 'headers': __tmp5}

    func = injector.inject(__tmp10)
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


def __tmp3():
    """
    Test the `@dependency.add_provider` and `@depenency.inject` wrappers.
    """
    class __typ0(dict):
        pass

    class __typ1(str):
        pass

    class __typ3(dict):
        pass

    @dependency.add_provider
    def __tmp11(__tmp12: __typ0) -> __typ1:
        return __typ1(__tmp12['METHOD'])

    @dependency.add_provider
    def __tmp13(__tmp12: __typ0) :
        __tmp5 = {}
        for key, value in __tmp12.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                __tmp5[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                __tmp5[key] = value
        return __typ3(__tmp5)

    dependency.set_required_state({
        'environ': __typ0
    })

    @dependency.inject
    def __tmp10(__tmp14, __tmp5):
        return {'method': __tmp14, 'headers': __tmp5}

    state = {
        'environ': {
            'METHOD': 'GET',
            'CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '127.0.0.1'
        }
    }
    result = __tmp10(state=state)

    assert result == {
        'method': 'GET',
        'headers': {'content-type': 'application/json', 'host': '127.0.0.1'}
    }
    assert repr(__tmp10) == '\n'.join([
        'method = get_method(environ=environ)',
        'headers = get_headers(environ=environ)',
        'return echo_method_and_headers(method=method, headers=headers)'
    ])


def test_context_manager():
    """
    Context managers should handle setup and teaddown.
    """

    class __typ2():
        events = []

        def __tmp15(__tmp1):
            pass

        def __tmp17(__tmp1):
            __tmp1.events.append('__enter__')

        def __tmp18(__tmp1, *args, **kwargs):
            __tmp1.events.append('__exit__')

    injector = dependency.Injector(providers={
        __typ2: __typ2,
    })

    def do_something(session: __typ2):
        pass

    func = injector.inject(do_something)
    func()

    assert __typ2.events == ['__enter__', '__exit__']
    assert repr(func) == '\n'.join([
        'with Session() as session:',
        '    return do_something(session=session)'
    ])


def __tmp7():
    """
    The ParamName class can be used to provide the parameter name
    that was used for the dependency injection.
    """
    Lookups = typing.NewType('Lookups', typing.Dict[str, int])
    Lookup = typing.NewType('Lookup', int)

    def __tmp8(__tmp4: dependency.ParamName, __tmp6):
        return __tmp6[__tmp4]

    injector = dependency.Injector(
        providers={
            Lookup: __tmp8,
        },
        required_state={
            'lookups': Lookups
        }
    )

    def __tmp2(__tmp0, __tmp9: <FILL>):
        return 'a: %s, b: %s' % (__tmp0, __tmp9)

    func = injector.inject(__tmp2)

    state = {
        'lookups': {'a': 123, 'b': 456}
    }
    assert func(state=state) == 'a: 123, b: 456'
    assert repr(func) == '\n'.join([
        'lookup:a = get_lookup(lookups=lookups)',
        'lookup:b = get_lookup(lookups=lookups)',
        'return make_lookups(a=lookup:a, b=lookup:b)'
    ])
