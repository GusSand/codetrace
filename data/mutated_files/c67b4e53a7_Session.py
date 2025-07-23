import typing

import dependency


def __tmp3():
    """
    Test the Injector class.
    """
    class __typ4(dict):
        pass

    class __typ0(str):
        pass

    class __typ2(dict):
        pass

    def get_method(__tmp7: __typ4) -> __typ0:
        return __typ0(__tmp7['METHOD'])

    def __tmp9(__tmp7: __typ4) -> __typ2:
        __tmp4 = {}
        for key, value in __tmp7.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                __tmp4[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                __tmp4[key] = value
        return __typ2(__tmp4)

    injector = dependency.Injector(
        providers={
            __typ0: get_method,
            __typ2: __tmp9
        },
        required_state={
            'environ': __typ4
        }
    )

    def __tmp14(__tmp10: __typ0, __tmp4):
        return {'method': __tmp10, 'headers': __tmp4}

    func = injector.inject(__tmp14)
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
    class __typ4(dict):
        pass

    class __typ0(str):
        pass

    class __typ2(dict):
        pass

    @dependency.add_provider
    def get_method(__tmp7: __typ4) -> __typ0:
        return __typ0(__tmp7['METHOD'])

    @dependency.add_provider
    def __tmp9(__tmp7) -> __typ2:
        __tmp4 = {}
        for key, value in __tmp7.items():
            if key.startswith('HTTP_'):
                key = key[5:].replace('_', '-').lower()
                __tmp4[key] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = key.replace('_', '-').lower()
                __tmp4[key] = value
        return __typ2(__tmp4)

    dependency.set_required_state({
        'environ': __typ4
    })

    @dependency.inject
    def __tmp14(__tmp10: __typ0, __tmp4: __typ2):
        return {'method': __tmp10, 'headers': __tmp4}

    state = {
        'environ': {
            'METHOD': 'GET',
            'CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '127.0.0.1'
        }
    }
    result = __tmp14(state=state)

    assert result == {
        'method': 'GET',
        'headers': {'content-type': 'application/json', 'host': '127.0.0.1'}
    }
    assert repr(__tmp14) == '\n'.join([
        'method = get_method(environ=environ)',
        'headers = get_headers(environ=environ)',
        'return echo_method_and_headers(method=method, headers=headers)'
    ])


def __tmp0():
    """
    Context managers should handle setup and teaddown.
    """

    class Session():
        events = []

        def __tmp12(__tmp2):
            pass

        def __tmp5(__tmp2):
            __tmp2.events.append('__enter__')

        def __tmp8(__tmp2, *args, **kwargs):
            __tmp2.events.append('__exit__')

    injector = dependency.Injector(providers={
        Session: Session,
    })

    def __tmp11(session: <FILL>):
        pass

    func = injector.inject(__tmp11)
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
    __typ1 = typing.NewType('Lookups', typing.Dict[str, int])
    __typ3 = typing.NewType('Lookup', int)

    def __tmp13(name, lookups: __typ1):
        return lookups[name]

    injector = dependency.Injector(
        providers={
            __typ3: __tmp13,
        },
        required_state={
            'lookups': __typ1
        }
    )

    def __tmp6(__tmp1: __typ3, b: __typ3):
        return 'a: %s, b: %s' % (__tmp1, b)

    func = injector.inject(__tmp6)

    state = {
        'lookups': {'a': 123, 'b': 456}
    }
    assert func(state=state) == 'a: 123, b: 456'
    assert repr(func) == '\n'.join([
        'lookup:a = get_lookup(lookups=lookups)',
        'lookup:b = get_lookup(lookups=lookups)',
        'return make_lookups(a=lookup:a, b=lookup:b)'
    ])
