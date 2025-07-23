from typing import TypeAlias
__typ0 : TypeAlias = "DataDrivenTestCase"
"""Test cases for AST diff (used for fine-grained incremental checking)"""

import os
from typing import List, Tuple, Dict, Optional

from mypy import build
from mypy.build import BuildSource
from mypy.defaults import PYTHON3_VERSION
from mypy.errors import CompileError
from mypy.nodes import MypyFile
from mypy.options import Options
from mypy.server.astdiff import snapshot_symbol_table, compare_symbol_table_snapshots
from mypy.test.config import test_temp_dir
from mypy.test.data import DataDrivenTestCase, DataSuite
from mypy.test.helpers import assert_string_arrays_equal


class __typ1(DataSuite):
    files = ['diff.test']
    base_path = test_temp_dir
    optional_out = True

    def run_case(__tmp1, __tmp0) :
        first_src = '\n'.join(__tmp0.input)
        files_dict = dict(__tmp0.files)
        second_src = files_dict['tmp/next.py']

        messages1, files1 = __tmp1.build(first_src)
        messages2, files2 = __tmp1.build(second_src)

        a = []
        if messages1:
            a.extend(messages1)
        if messages2:
            a.append('== next ==')
            a.extend(messages2)

        assert files1 is not None and files2 is not None, ('cases where CompileError'
                                                           ' occurred should not be run')
        prefix = '__main__'
        snapshot1 = snapshot_symbol_table(prefix, files1['__main__'].names)
        snapshot2 = snapshot_symbol_table(prefix, files2['__main__'].names)
        diff = compare_symbol_table_snapshots(prefix, snapshot1, snapshot2)
        for trigger in sorted(diff):
            a.append(trigger)

        assert_string_arrays_equal(
            __tmp0.output, a,
            'Invalid output ({}, line {})'.format(__tmp0.file,
                                                  __tmp0.line))

    def build(__tmp1, source: <FILL>) :
        options = Options()
        options.use_builtins_fixtures = True
        options.show_traceback = True
        options.cache_dir = os.devnull
        options.python_version = PYTHON3_VERSION
        try:
            result = build.build(sources=[BuildSource('main', None, source)],
                                 options=options,
                                 alt_lib_path=test_temp_dir)
        except CompileError as e:
            # TODO: Is it okay to return None?
            return e.messages, None
        return result.errors, result.files
