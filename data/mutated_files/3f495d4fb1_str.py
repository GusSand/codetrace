"""Test cases for generating node-level dependencies (for fine-grained incremental checking)"""

import os
from typing import List, Tuple, Dict, Optional, Set
MYPY = False
if MYPY:
    from typing import DefaultDict
from collections import defaultdict

from mypy import build, defaults
from mypy.build import BuildSource
from mypy.errors import CompileError
from mypy.nodes import MypyFile, Expression
from mypy.options import Options
from mypy.server.deps import get_dependencies
from mypy.test.config import test_temp_dir
from mypy.test.data import DataDrivenTestCase, DataSuite
from mypy.test.helpers import assert_string_arrays_equal
from mypy.types import Type


# Only dependencies in these modules are dumped
dumped_modules = ['__main__', 'pkg', 'pkg.mod']


class __typ0(DataSuite):
    files = [
        'deps.test',
        'deps-types.test',
        'deps-generics.test',
        'deps-expressions.test',
        'deps-statements.test',
        'deps-classes.test',
    ]
    base_path = test_temp_dir
    optional_out = True

    def __tmp1(self, __tmp2) :
        src = '\n'.join(__tmp2.input)
        dump_all = '# __dump_all__' in src
        if __tmp2.name.endswith('python2'):
            python_version = defaults.PYTHON2_VERSION
        else:
            python_version = defaults.PYTHON3_VERSION
        messages, files, type_map = self.build(src, python_version)
        a = messages
        if files is None or type_map is None:
            if not a:
                a = ['Unknown compile error (likely syntax error in test case or fixture)']
        else:
            deps = defaultdict(set)  # type: DefaultDict[str, Set[str]]
            for module in files:
                if module in dumped_modules or dump_all and module not in ('abc',
                                                                           'typing',
                                                                           'mypy_extensions',
                                                                           'enum'):
                    new_deps = get_dependencies(files[module], type_map, python_version)
                    for __tmp0 in new_deps:
                        deps[__tmp0].update(new_deps[__tmp0])

            for __tmp0, targets in sorted(deps.items()):
                if __tmp0.startswith('<enum.'):
                    # Remove noise.
                    continue
                line = '%s -> %s' % (__tmp0, ', '.join(sorted(targets)))
                # Clean up output a bit
                line = line.replace('__main__', 'm')
                a.append(line)

        assert_string_arrays_equal(
            __tmp2.output, a,
            'Invalid output ({}, line {})'.format(__tmp2.file,
                                                  __tmp2.line))

    def build(self,
              __tmp0: <FILL>,
              python_version: Tuple[int, int]) -> Tuple[List[str],
                                                        Optional[Dict[str, MypyFile]],
                                                        Optional[Dict[Expression, Type]]]:
        options = Options()
        options.use_builtins_fixtures = True
        options.show_traceback = True
        options.cache_dir = os.devnull
        options.python_version = python_version
        try:
            result = build.build(sources=[BuildSource('main', None, __tmp0)],
                                 options=options,
                                 alt_lib_path=test_temp_dir)
        except CompileError as e:
            # TODO: Should perhaps not return None here.
            return e.messages, None, None
        return result.errors, result.files, result.types
