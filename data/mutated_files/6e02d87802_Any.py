import re
import markdown
from typing import Any, Dict, List, Optional, Union
from typing.re import Match
from markdown.preprocessors import Preprocessor

from zerver.lib.emoji import EMOTICON_CONVERSIONS, name_to_codepoint

REGEXP = re.compile(r'\{emoticon_translations\}')

TABLE_HTML = """
<table>
    <thead>
        <tr>
            <th align="center">Emoticon</th>
            <th align="center">Emoji</th>
        </tr>
    </thead>
    <tbody>
        {body}
    </tbody>
</table>
"""

ROW_HTML = """
<tr>
    <td align="center"><code>{emoticon}</code></td>
    <td align="center">
        <img
            src="/static/generated/emoji/images-google-64/{codepoint}.png"
            alt="{name}"
            class="emoji-big">
    </td>
</tr>
"""

class __typ0(markdown.Extension):
    def __tmp0(self, md: markdown.Markdown, md_globals: Dict[str, Any]) -> None:
        """ Add SettingHelpExtension to the Markdown instance. """
        md.registerExtension(self)
        md.preprocessors.add('emoticon_translations', __typ1(), '_end')


class __typ1(Preprocessor):
    def run(self, lines: List[str]) :
        for loc, line in enumerate(lines):
            match = REGEXP.search(line)
            if match:
                text = self.handleMatch(match)
                lines = lines[:loc] + text + lines[loc+1:]
                break
        return lines

    def handleMatch(self, match) -> List[str]:
        rows = [
            ROW_HTML.format(emoticon=emoticon,
                            name=name.strip(':'),
                            codepoint=name_to_codepoint[name.strip(':')])
            for emoticon, name in EMOTICON_CONVERSIONS.items()
        ]
        body = '\n'.join(rows).strip()
        return TABLE_HTML.format(body=body).strip().splitlines()

def makeExtension(*args: <FILL>, **kwargs: Any) -> __typ0:
    return __typ0(*args, **kwargs)
