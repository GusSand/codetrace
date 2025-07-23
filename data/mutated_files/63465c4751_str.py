import re
import os
import ujson

from django.utils.html import escape as escape_html
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from zerver.lib.openapi import get_openapi_parameters
from typing import Any, Dict, Optional, List
import markdown

REGEXP = re.compile(r'\{generate_api_arguments_table\|\s*(.+?)\s*\|\s*(.+)\s*\}')


class MarkdownArgumentsTableGenerator(Extension):
    def __init__(__tmp0, configs: Optional[Dict[str, Any]]=None) -> None:
        if configs is None:
            configs = {}
        __tmp0.config = {
            'base_path': ['.', 'Default location from which to evaluate relative paths for the JSON files.'],
        }
        for key, value in configs.items():
            __tmp0.setConfig(key, value)

    def extendMarkdown(__tmp0, __tmp3: markdown.Markdown, __tmp4: Dict[str, Any]) -> None:
        __tmp3.preprocessors.add(
            'generate_api_arguments', APIArgumentsTablePreprocessor(__tmp3, __tmp0.getConfigs()), '_begin'
        )


class APIArgumentsTablePreprocessor(Preprocessor):
    def __init__(__tmp0, __tmp3, config: Dict[str, Any]) :
        super(APIArgumentsTablePreprocessor, __tmp0).__init__(__tmp3)
        __tmp0.base_path = config['base_path']

    def run(__tmp0, __tmp2: List[str]) -> List[str]:
        done = False
        while not done:
            for line in __tmp2:
                loc = __tmp2.index(line)
                match = REGEXP.search(line)

                if not match:
                    continue

                filename = match.group(1)
                doc_name = match.group(2)
                filename = os.path.expanduser(filename)

                is_openapi_format = filename.endswith('.yaml')

                if not os.path.isabs(filename):
                    parent_dir = __tmp0.base_path
                    filename = os.path.normpath(os.path.join(parent_dir, filename))

                if is_openapi_format:
                    endpoint, method = doc_name.rsplit(':', 1)
                    __tmp1 = []  # type: List[Dict[str, Any]]

                    try:
                        __tmp1 = get_openapi_parameters(endpoint, method)
                    except KeyError as e:
                        # Don't raise an exception if the "parameters"
                        # field is missing; we assume that's because the
                        # endpoint doesn't accept any parameters
                        if e.args != ('parameters',):
                            raise e
                else:
                    with open(filename, 'r') as fp:
                        json_obj = ujson.load(fp)
                        __tmp1 = json_obj[doc_name]

                if __tmp1:
                    text = __tmp0.render_table(__tmp1)
                else:
                    text = ['This endpoint does not consume any arguments.']
                # The line that contains the directive to include the macro
                # may be preceded or followed by text or tags, in that case
                # we need to make sure that any preceding or following text
                # stays the same.
                line_split = REGEXP.split(line, maxsplit=0)
                preceding = line_split[0]
                following = line_split[-1]
                text = [preceding] + text + [following]
                __tmp2 = __tmp2[:loc] + text + __tmp2[loc+1:]
                break
            else:
                done = True
        return __tmp2

    def render_table(__tmp0, __tmp1: List[Dict[str, Any]]) -> List[str]:
        table = []
        beginning = """
<table class="table">
  <thead>
    <tr>
      <th>Argument</th>
      <th>Example</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
<tbody>
"""
        tr = """
<tr>
  <td><code>{argument}</code></td>
  <td><code>{example}</code></td>
  <td>{required}</td>
  <td>{description}</td>
</tr>
"""

        table.append(beginning)

        md_engine = markdown.Markdown(extensions=[])

        for argument in __tmp1:
            description = argument['description']

            oneof = ['`' + item + '`'
                     for item in argument.get('schema', {}).get('enum', [])]
            if oneof:
                description += '\nMust be one of: {}.'.format(', '.join(oneof))

            default = argument.get('schema', {}).get('default')
            if default is not None:
                description += '\nDefaults to `{}`.'.format(ujson.dumps(default))

            # TODO: Swagger allows indicating where the argument goes
            # (path, querystring, form data...). A column in the table should
            # be added for this.
            table.append(tr.format(
                argument=argument.get('argument') or argument.get('name'),
                # Show this as JSON to avoid changing the quoting style, which
                # may cause problems with JSON encoding.
                example=escape_html(ujson.dumps(argument['example'])),
                required='Yes' if argument.get('required') else 'No',
                description=md_engine.convert(description),
            ))

        table.append("</tbody>")
        table.append("</table>")

        return table

def makeExtension(*args: Any, **kwargs: <FILL>) :
    return MarkdownArgumentsTableGenerator(kwargs)
