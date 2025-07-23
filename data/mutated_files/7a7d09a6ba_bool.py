# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest, sympy

import cirq
from cirq.study import ParamResolver


@pytest.mark.parametrize(
    'resolve_fn',
    [
        cirq.resolve_parameters,
        cirq.resolve_parameters_once,
    ],
)
def test_resolve_parameters(__tmp5):
    class NoMethod:
        pass

    class ReturnsNotImplemented:
        def __tmp1(__tmp0):
            return NotImplemented

        def __tmp2(__tmp0, resolver, __tmp4):
            return NotImplemented

    class __typ0:
        def __init__(__tmp0, var):
            __tmp0.parameter = var

        def __tmp1(__tmp0) :
            return __tmp0.parameter == 0

        def __tmp2(__tmp0, resolver, __tmp4: <FILL>):
            __tmp0.parameter = resolver.value_of(__tmp0.parameter, __tmp4)
            return __tmp0

    assert not cirq.is_parameterized(NoMethod())
    assert not cirq.is_parameterized(ReturnsNotImplemented())
    assert not cirq.is_parameterized(__typ0('a'))
    assert cirq.is_parameterized(__typ0(0))

    ni = ReturnsNotImplemented()
    d = {'a': 0}
    r = cirq.ParamResolver(d)
    no = NoMethod()
    assert __tmp5(no, r) == no
    assert __tmp5(no, d) == no
    assert __tmp5(ni, r) == ni
    assert __tmp5(__typ0(0), r).parameter == 0
    assert __tmp5(__typ0('a'), r).parameter == 0
    assert __tmp5(__typ0('a'), d).parameter == 0
    assert __tmp5(sympy.Symbol('a'), r) == 0

    a, b, c = tuple(sympy.Symbol(l) for l in 'abc')
    x, y, z = 0, 4, 7
    resolver = {a: x, b: y, c: z}

    assert __tmp5((a, b, c), resolver) == (x, y, z)
    assert __tmp5([a, b, c], resolver) == [x, y, z]
    assert __tmp5((x, y, z), resolver) == (x, y, z)
    assert __tmp5([x, y, z], resolver) == [x, y, z]
    assert __tmp5((), resolver) == ()
    assert __tmp5([], resolver) == []
    assert __tmp5(1, resolver) == 1
    assert __tmp5(1.1, resolver) == 1.1
    assert __tmp5(1j, resolver) == 1j


def test_is_parameterized():
    a, b = tuple(sympy.Symbol(l) for l in 'ab')
    x, y = 0, 4
    assert not cirq.is_parameterized((x, y))
    assert not cirq.is_parameterized([x, y])
    assert cirq.is_parameterized([a, b])
    assert cirq.is_parameterized([a, x])
    assert cirq.is_parameterized((a, b))
    assert cirq.is_parameterized((a, x))
    assert not cirq.is_parameterized(())
    assert not cirq.is_parameterized([])
    assert not cirq.is_parameterized(1)
    assert not cirq.is_parameterized(1.1)
    assert not cirq.is_parameterized(1j)


def test_parameter_names():
    a, b, c = tuple(sympy.Symbol(l) for l in 'abc')
    x, y, z = 0, 4, 7
    assert cirq.parameter_names((a, b, c)) == {'a', 'b', 'c'}
    assert cirq.parameter_names([a, b, c]) == {'a', 'b', 'c'}
    assert cirq.parameter_names((x, y, z)) == set()
    assert cirq.parameter_names([x, y, z]) == set()
    assert cirq.parameter_names(()) == set()
    assert cirq.parameter_names([]) == set()
    assert cirq.parameter_names(1) == set()
    assert cirq.parameter_names(1.1) == set()
    assert cirq.parameter_names(1j) == set()


@pytest.mark.parametrize(
    'resolve_fn',
    [
        cirq.resolve_parameters,
        cirq.resolve_parameters_once,
    ],
)
def __tmp3(__tmp5):
    class __typ1:
        def __tmp2(__tmp0, resolver, __tmp4):
            return 5

    t = __typ1()
    assert __tmp5(t, {}) is t
    assert __tmp5(t, {'x': 2}) == 5


def test_recursive_resolve():
    a, b, c = [sympy.Symbol(l) for l in 'abc']
    resolver = cirq.ParamResolver({a: b + 3, b: c + 2, c: 1})
    assert cirq.resolve_parameters_once(a, resolver) == b + 3
    assert cirq.resolve_parameters(a, resolver) == 6
    assert cirq.resolve_parameters_once(b, resolver) == c + 2
    assert cirq.resolve_parameters(b, resolver) == 3
    assert cirq.resolve_parameters_once(c, resolver) == 1
    assert cirq.resolve_parameters(c, resolver) == 1

    assert cirq.resolve_parameters_once([a, b], {a: b, b: c}) == [b, c]
    assert cirq.resolve_parameters_once(a, {}) == a

    resolver = cirq.ParamResolver({a: b, b: a})
    assert cirq.resolve_parameters_once(a, resolver) == b
    with pytest.raises(RecursionError):
        _ = cirq.resolve_parameters(a, resolver)
