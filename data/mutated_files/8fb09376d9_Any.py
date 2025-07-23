from typing import TypeAlias
__typ0 : TypeAlias = "str"
import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from typing import Any, Dict, Optional, List, Tuple
import markdown

START_TABBED_SECTION_REGEX = re.compile(r'^\{start_tabs\}$')
END_TABBED_SECTION_REGEX = re.compile(r'^\{end_tabs\}$')
TAB_CONTENT_REGEX = re.compile(r'^\{tab\|\s*(.+?)\s*\}$')

CODE_SECTION_TEMPLATE = """
<div class="code-section" markdown="1">
{nav_bar}
<div class="blocks">
{blocks}
</div>
</div>
""".strip()

NAV_BAR_TEMPLATE = """
<ul class="nav">
{tabs}
</ul>
""".strip()

NAV_LIST_ITEM_TEMPLATE = """
<li data-language="{data_language}">{name}</li>
""".strip()

DIV_TAB_CONTENT_TEMPLATE = """
<div data-language="{data_language}" markdown="1">
{content}
</div>
""".strip()

# If adding new entries here, also check if you need to update
# tabbed-instructions.js
TAB_DISPLAY_NAMES = {
    'desktop-web': 'Desktop/Web',
    'ios': 'iOS',
    'android': 'Android',
    'mac': 'macOS',
    'windows': 'Windows',
    'linux': 'Linux',
    'python': 'Python',
    'js': 'JavaScript',
    'curl': 'curl',
    'zulip-send': 'zulip-send',

    'cloud': 'HipChat Cloud',
    'server': 'HipChat Server or Data Center',
}

class TabbedSectionsGenerator(Extension):
    def extendMarkdown(__tmp1, __tmp4: markdown.Markdown, md_globals: Dict[__typ0, Any]) -> None:
        __tmp4.preprocessors.add(
            'tabbed_sections', TabbedSectionsPreprocessor(__tmp4, __tmp1.getConfigs()), '_end')

class TabbedSectionsPreprocessor(Preprocessor):
    def __init__(__tmp1, __tmp4: markdown.Markdown, config) :
        super(TabbedSectionsPreprocessor, __tmp1).__init__(__tmp4)

    def __tmp5(__tmp1, __tmp3: List[__typ0]) -> List[__typ0]:
        __tmp2 = __tmp1.parse_tabs(__tmp3)
        while __tmp2:
            nav_bar = __tmp1.generate_nav_bar(__tmp2)
            content_blocks = __tmp1.generate_content_blocks(__tmp2, __tmp3)
            rendered_tabs = CODE_SECTION_TEMPLATE.format(
                nav_bar=nav_bar, blocks=content_blocks)

            start = __tmp2['start_tabs_index']
            end = __tmp2['end_tabs_index'] + 1
            __tmp3 = __tmp3[:start] + [rendered_tabs] + __tmp3[end:]
            __tmp2 = __tmp1.parse_tabs(__tmp3)
        return __tmp3

    def generate_content_blocks(__tmp1, __tmp2: Dict[__typ0, Any], __tmp3: List[__typ0]) -> __typ0:
        tab_content_blocks = []
        for index, tab in enumerate(__tmp2['tabs']):
            start_index = tab['start'] + 1
            try:
                # If there are more tabs, we can use the starting index
                # of the next tab as the ending index of the previous one
                end_index = __tmp2['tabs'][index + 1]['start']
            except IndexError:
                # Otherwise, just use the end of the entire section
                end_index = __tmp2['end_tabs_index']

            content = '\n'.join(__tmp3[start_index:end_index]).strip()
            tab_content_block = DIV_TAB_CONTENT_TEMPLATE.format(
                data_language=tab['tab_name'],
                # Wrapping the content in two newlines is necessary here.
                # If we don't do this, the inner Markdown does not get
                # rendered properly.
                content='\n{}\n'.format(content))
            tab_content_blocks.append(tab_content_block)
        return '\n'.join(tab_content_blocks)

    def generate_nav_bar(__tmp1, __tmp2) -> __typ0:
        li_elements = []
        for tab in __tmp2['tabs']:
            li = NAV_LIST_ITEM_TEMPLATE.format(
                data_language=tab.get('tab_name'),
                name=TAB_DISPLAY_NAMES.get(tab.get('tab_name')))
            li_elements.append(li)
        return NAV_BAR_TEMPLATE.format(tabs='\n'.join(li_elements))

    def parse_tabs(__tmp1, __tmp3: List[__typ0]) :
        block = {}  # type: Dict[str, Any]
        for index, line in enumerate(__tmp3):
            start_match = START_TABBED_SECTION_REGEX.search(line)
            if start_match:
                block['start_tabs_index'] = index

            tab_content_match = TAB_CONTENT_REGEX.search(line)
            if tab_content_match:
                block.setdefault('tabs', [])
                tab = {'start': index,
                       'tab_name': tab_content_match.group(1)}
                block['tabs'].append(tab)

            end_match = END_TABBED_SECTION_REGEX.search(line)
            if end_match:
                block['end_tabs_index'] = index
                break
        return block

def __tmp0(*args: <FILL>, **kwargs: __typ0) :
    return TabbedSectionsGenerator(kwargs)
