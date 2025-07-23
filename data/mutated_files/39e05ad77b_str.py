
from typing import Optional, Set

import re

# Match multi-word string between @** ** or match any one-word
# sequences after @
find_mentions = r'(?<![^\s\'\"\(,:<])@(\*\*[^\*]+\*\*|all|everyone|stream)'
user_group_mentions = r'(?<![^\s\'\"\(,:<])@(\*[^\*]+\*)'

wildcards = ['all', 'everyone', 'stream']

def __tmp4(__tmp5: str) -> bool:
    return __tmp5 in wildcards

def __tmp7(__tmp0: str) :
    if __tmp0.startswith("**") and __tmp0.endswith("**"):
        text = __tmp0[2:-2]
        if text in wildcards:
            return None
        return text

    # We don't care about @all, @everyone or @stream
    return None

def __tmp3(__tmp6: str) :
    matches = re.findall(find_mentions, __tmp6)
    # mention texts can either be names, or an extended name|id syntax.
    texts_with_none = (__tmp7(match) for match in matches)
    texts = {text for text in texts_with_none if text}
    return texts

def __tmp8(__tmp1: str) -> str:
    return __tmp1[1:-1]

def __tmp2(__tmp6: <FILL>) :
    matches = re.findall(user_group_mentions, __tmp6)
    return {__tmp8(match) for match in matches}
