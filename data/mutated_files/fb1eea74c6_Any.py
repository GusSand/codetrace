from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
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

def gear_handle_match(__tmp9) :
    if relative_help_links:
        item = '[%s](%s)' % (gear_info[__tmp9][0], gear_info[__tmp9][1])
    else:
        item = '**%s**' % (gear_info[__tmp9][0],)
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

def __tmp2(__tmp9: __typ1) -> __typ1:
    if relative_help_links:
        return "1. Go to [%s](%s)." % (stream_info[__tmp9][0], stream_info[__tmp9][1])
    if __tmp9 == 'all':
        return stream_instructions_no_link + "\n\n1. Click **All streams** in the upper left."
    return stream_instructions_no_link


LINK_TYPE_HANDLERS = {
    'gear': gear_handle_match,
    'stream': __tmp2,
}

class __typ0(markdown.Extension):
    def __tmp4(__tmp1, __tmp7: markdown.Markdown, __tmp10: Dict[__typ1, Any]) :
        """ Add RelativeLinksHelpExtension to the Markdown instance. """
        __tmp7.registerExtension(__tmp1)
        __tmp7.preprocessors.add('help_relative_links', RelativeLinks(), '_begin')

relative_help_links = None  # type: Optional[bool]

def __tmp6(__tmp3) :
    global relative_help_links
    relative_help_links = __tmp3

class RelativeLinks(Preprocessor):
    def __tmp8(__tmp1, __tmp5) :
        done = False
        while not done:
            for line in __tmp5:
                loc = __tmp5.index(line)
                __tmp11 = REGEXP.search(line)

                if __tmp11:
                    text = [__tmp1.handleMatch(__tmp11)]
                    # The line that contains the directive to include the macro
                    # may be preceded or followed by text or tags, in that case
                    # we need to make sure that any preceding or following text
                    # stays the same.
                    line_split = REGEXP.split(line, maxsplit=0)
                    preceding = line_split[0]
                    following = line_split[-1]
                    text = [preceding] + text + [following]
                    __tmp5 = __tmp5[:loc] + text + __tmp5[loc+1:]
                    break
            else:
                done = True
        return __tmp5

    def handleMatch(__tmp1, __tmp11: Match[__typ1]) :
        return LINK_TYPE_HANDLERS[__tmp11.group('link_type')](__tmp11.group('key'))

def __tmp0(*args: <FILL>, **kwargs) :
    return __typ0(*args, **kwargs)
