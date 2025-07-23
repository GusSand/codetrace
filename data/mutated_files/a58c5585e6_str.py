import re
import os
import sys
import json
import inspect

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from typing import Any, Dict, Optional, List
import markdown

import zerver.lib.api_test_helpers
from zerver.lib.openapi import get_openapi_fixture

MACRO_REGEXP = re.compile(r'\{generate_code_example(\(\s*(.+?)\s*\))*\|\s*(.+?)\s*\|\s*(.+?)\s*(\(\s*(.+)\s*\))?\}')
CODE_EXAMPLE_REGEX = re.compile(r'\# \{code_example\|\s*(.+?)\s*\}')

PYTHON_CLIENT_CONFIG = """
#!/usr/bin/env python3

import zulip

# Pass the path to your zuliprc file here.
client = zulip.Client(config_file="~/zuliprc")

"""

PYTHON_CLIENT_ADMIN_CONFIG = """
#!/usr/bin/env python

import zulip

# The user for this zuliprc file must be an organization administrator
client = zulip.Client(config_file="~/zuliprc-admin")

"""

def extract_python_code_example(source, snippet) :
    start = -1
    end = -1
    for line in source:
        match = CODE_EXAMPLE_REGEX.search(line)
        if match:
            if match.group(1) == 'start':
                start = source.index(line)
            elif match.group(1) == 'end':
                end = source.index(line)
                break

    if (start == -1 and end == -1):
        return snippet

    snippet.extend(source[start + 1: end])
    snippet.append('    print(result)')
    snippet.append('\n')
    source = source[end + 1:]
    return extract_python_code_example(source, snippet)

def __tmp2(__tmp1, admin_config: Optional[bool]=False) -> List[str]:
    method = zerver.lib.api_test_helpers.TEST_FUNCTIONS[__tmp1]
    function_source_lines = inspect.getsourcelines(method)[0]

    if admin_config:
        config = PYTHON_CLIENT_ADMIN_CONFIG.splitlines()
    else:
        config = PYTHON_CLIENT_CONFIG.splitlines()

    snippet = extract_python_code_example(function_source_lines, [])

    code_example = []
    code_example.append('```python')
    code_example.extend(config)

    for line in snippet:
        # Remove one level of indentation and strip newlines
        code_example.append(line[4:].rstrip())

    code_example.append('```')

    return code_example

SUPPORTED_LANGUAGES = {
    'python': {
        'client_config': PYTHON_CLIENT_CONFIG,
        'admin_config': PYTHON_CLIENT_ADMIN_CONFIG,
        'render': __tmp2,
    }
}  # type: Dict[str, Any]

class __typ0(Extension):
    def extendMarkdown(__tmp0, md, md_globals) :
        md.preprocessors.add(
            'generate_code_example', APICodeExamplesPreprocessor(md, __tmp0.getConfigs()), '_begin'
        )


class APICodeExamplesPreprocessor(Preprocessor):
    def __init__(__tmp0, md, config) -> None:
        super(APICodeExamplesPreprocessor, __tmp0).__init__(md)

    def __tmp4(__tmp0, __tmp3: List[str]) -> List[str]:
        done = False
        while not done:
            for line in __tmp3:
                loc = __tmp3.index(line)
                match = MACRO_REGEXP.search(line)

                if match:
                    language = match.group(2)
                    __tmp1 = match.group(3)
                    key = match.group(4)
                    argument = match.group(6)

                    if key == 'fixture':
                        if argument:
                            text = __tmp0.render_fixture(__tmp1, name=argument)
                        else:
                            text = __tmp0.render_fixture(__tmp1)
                    elif key == 'example':
                        if argument == 'admin_config=True':
                            text = SUPPORTED_LANGUAGES[language]['render'](__tmp1, admin_config=True)
                        else:
                            text = SUPPORTED_LANGUAGES[language]['render'](__tmp1)

                    # The line that contains the directive to include the macro
                    # may be preceded or followed by text or tags, in that case
                    # we need to make sure that any preceding or following text
                    # stays the same.
                    line_split = MACRO_REGEXP.split(line, maxsplit=0)
                    preceding = line_split[0]
                    following = line_split[-1]
                    text = [preceding] + text + [following]
                    __tmp3 = __tmp3[:loc] + text + __tmp3[loc+1:]
                    break
            else:
                done = True
        return __tmp3

    def render_fixture(__tmp0, __tmp1: <FILL>, name: Optional[str]=None) :
        fixture = []

        # We assume that if the function we're rendering starts with a slash
        # it's a path in the endpoint and therefore it uses the new OpenAPI
        # format.
        if __tmp1.startswith('/'):
            path, method = __tmp1.rsplit(':', 1)
            fixture_dict = get_openapi_fixture(path, method, name)
        else:
            fixture_dict = zerver.lib.api_test_helpers.FIXTURES[__tmp1]

        fixture_json = json.dumps(fixture_dict, indent=4, sort_keys=True,
                                  separators=(',', ': '))

        fixture.append('```')
        fixture.extend(fixture_json.splitlines())
        fixture.append('```')

        return fixture

def makeExtension(*args: Any, **kwargs) :
    return __typ0(kwargs)
