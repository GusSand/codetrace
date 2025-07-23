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

class __typ1(markdown.Extension):
    def extendMarkdown(self, md: markdown.Markdown, __tmp1: Dict[str, Any]) -> None:
        """ Add SettingHelpExtension to the Markdown instance. """
        md.registerExtension(self)
        md.preprocessors.add('emoticon_translations', __typ0(), '_end')


class __typ0(Preprocessor):
    def run(self, __tmp0: List[str]) -> List[str]:
        for loc, line in enumerate(__tmp0):
            __tmp2 = REGEXP.search(line)
            if __tmp2:
                text = self.handleMatch(__tmp2)
                __tmp0 = __tmp0[:loc] + text + __tmp0[loc+1:]
                break
        return __tmp0

    def handleMatch(self, __tmp2) -> List[str]:
        rows = [
            ROW_HTML.format(emoticon=emoticon,
                            name=name.strip(':'),
                            codepoint=name_to_codepoint[name.strip(':')])
            for emoticon, name in EMOTICON_CONVERSIONS.items()
        ]
        body = '\n'.join(rows).strip()
        return TABLE_HTML.format(body=body).strip().splitlines()

def makeExtension(*args, **kwargs: <FILL>) -> __typ1:
    return __typ1(*args, **kwargs)
