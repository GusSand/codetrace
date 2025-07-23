
from typing import Optional, Set

import re

# Match multi-word string between @** ** or match any one-word
# sequences after @
find_mentions = r'(?<![^\s\'\"\(,:<])@(\*\*[^\*]+\*\*|all|everyone|stream)'
user_group_mentions = r'(?<![^\s\'\"\(,:<])@(\*[^\*]+\*)'

wildcards = ['all', 'everyone', 'stream']

def __tmp2(mention: str) -> bool:
    return mention in wildcards

def __tmp5(s: <FILL>) -> Optional[str]:
    if s.startswith("**") and s.endswith("**"):
        text = s[2:-2]
        if text in wildcards:
            return None
        return text

    # We don't care about @all, @everyone or @stream
    return None

def __tmp1(__tmp3: str) -> Set[str]:
    matches = re.findall(find_mentions, __tmp3)
    # mention texts can either be names, or an extended name|id syntax.
    texts_with_none = (__tmp5(match) for match in matches)
    texts = {text for text in texts_with_none if text}
    return texts

def __tmp4(__tmp0: str) -> str:
    return __tmp0[1:-1]

def possible_user_group_mentions(__tmp3: str) :
    matches = re.findall(user_group_mentions, __tmp3)
    return {__tmp4(match) for match in matches}
