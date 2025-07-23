from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "Any"
import re
import markdown
from typing import Any, Dict, List, Optional, Union
from typing.re import Match
from markdown.preprocessors import Preprocessor

# There is a lot of duplicated code between this file and
# help_settings_links.py. So if you're making a change here consider making
# it there as well.

REGEXP = re.compile(r'\{relative\|(?P<link_type>.*?)\|(?P<key>.*?)\}')

gear_info = {
    # The pattern is key: [name, link]
    # key is from REGEXP: `{relative|gear|key}`
    # name is what the item is called in the gear menu: `Select **name**.`
    # link is used for relative links: `Select [name](link).`
    'manage-streams': ['Manage streams', '/#streams/subscribed'],
    'settings': ['Settings', '/#settings/your-account'],
    'manage-organization': ['Manage organization', '/#organization/organization-profile'],
    'integrations': ['Integrations', '/integrations'],
    'stats': ['Statistics', '/stats'],
    'plans': ['Plans and pricing', '/plans'],
    'billing': ['Billing', '/billing'],
    'invite': ['Invite users', '/#invite'],
}

gear_instructions = """
1. From your desktop, click on the **gear**
   (<i class="fa fa-cog"></i>) in the upper right corner.

1. Select %(item)s.
"""

def __tmp4(__tmp6) :
    if relative_help_links:
        item = '[%s](%s)' % (gear_info[__tmp6][0], gear_info[__tmp6][1])
    else:
        item = '**%s**' % (gear_info[__tmp6][0],)
    return gear_instructions % {'item': item}


stream_info = {
    'all': ['All streams', '/#streams/all'],
    'subscribed': ['Your streams', '/#streams/subscribed'],
}

stream_instructions_no_link = """
1. From your desktop, click on the **gear**
   (<i class="fa fa-cog"></i>) in the upper right corner.

1. Click **Manage streams**.
"""

def stream_handle_match(__tmp6: __typ2) -> __typ2:
    if relative_help_links:
        return "1. Go to [%s](%s)." % (stream_info[__tmp6][0], stream_info[__tmp6][1])
    if __tmp6 == 'all':
        return stream_instructions_no_link + "\n\n1. Click **All streams** in the upper left."
    return stream_instructions_no_link


LINK_TYPE_HANDLERS = {
    'gear': __tmp4,
    'stream': stream_handle_match,
}

class __typ0(markdown.Extension):
    def __tmp3(__tmp1, md, __tmp7) :
        """ Add RelativeLinksHelpExtension to the Markdown instance. """
        md.registerExtension(__tmp1)
        md.preprocessors.add('help_relative_links', __typ1(), '_begin')

relative_help_links = None  # type: Optional[bool]

def __tmp5(__tmp2: <FILL>) :
    global relative_help_links
    relative_help_links = __tmp2

class __typ1(Preprocessor):
    def run(__tmp1, lines) :
        done = False
        while not done:
            for line in lines:
                loc = lines.index(line)
                __tmp8 = REGEXP.search(line)

                if __tmp8:
                    text = [__tmp1.handleMatch(__tmp8)]
                    # The line that contains the directive to include the macro
                    # may be preceded or followed by text or tags, in that case
                    # we need to make sure that any preceding or following text
                    # stays the same.
                    line_split = REGEXP.split(line, maxsplit=0)
                    preceding = line_split[0]
                    following = line_split[-1]
                    text = [preceding] + text + [following]
                    lines = lines[:loc] + text + lines[loc+1:]
                    break
            else:
                done = True
        return lines

    def handleMatch(__tmp1, __tmp8) :
        return LINK_TYPE_HANDLERS[__tmp8.group('link_type')](__tmp8.group('key'))

def __tmp0(*args, **kwargs) :
    return __typ0(*args, **kwargs)
