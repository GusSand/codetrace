from typing import TypeAlias
__typ0 : TypeAlias = "bool"

from typing import Optional, Set

import re

# Match multi-word string between @** ** or match any one-word
# sequences after @
find_mentions = r'(?<![^\s\'\"\(,:<])@(\*\*[^\*]+\*\*|all|everyone|stream)'
user_group_mentions = r'(?<![^\s\'\"\(,:<])@(\*[^\*]+\*)'

wildcards = ['all', 'everyone', 'stream']

def __tmp2(mention: str) -> __typ0:
    return mention in wildcards

def __tmp3(__tmp0) -> Optional[str]:
    if __tmp0.startswith("**") and __tmp0.endswith("**"):
        text = __tmp0[2:-2]
        if text in wildcards:
            return None
        return text

    # We don't care about @all, @everyone or @stream
    return None

def possible_mentions(content: <FILL>) :
    matches = re.findall(find_mentions, content)
    # mention texts can either be names, or an extended name|id syntax.
    texts_with_none = (__tmp3(match) for match in matches)
    texts = {text for text in texts_with_none if text}
    return texts

def __tmp4(__tmp1: str) -> str:
    return __tmp1[1:-1]

def possible_user_group_mentions(content) -> Set[str]:
    matches = re.findall(user_group_mentions, content)
    return {__tmp4(match) for match in matches}
