from typing import TypeAlias
__typ0 : TypeAlias = "bool"

from typing import Optional, Set

import re

# Match multi-word string between @** ** or match any one-word
# sequences after @
find_mentions = r'(?<![^\s\'\"\(,:<])@(\*\*[^\*]+\*\*|all|everyone|stream)'
user_group_mentions = r'(?<![^\s\'\"\(,:<])@(\*[^\*]+\*)'

wildcards = ['all', 'everyone', 'stream']

def user_mention_matches_wildcard(mention) :
    return mention in wildcards

def extract_mention_text(__tmp0) -> Optional[str]:
    if __tmp0.startswith("**") and __tmp0.endswith("**"):
        text = __tmp0[2:-2]
        if text in wildcards:
            return None
        return text

    # We don't care about @all, @everyone or @stream
    return None

def __tmp2(__tmp1: str) -> Set[str]:
    matches = re.findall(find_mentions, __tmp1)
    # mention texts can either be names, or an extended name|id syntax.
    texts_with_none = (extract_mention_text(match) for match in matches)
    texts = {text for text in texts_with_none if text}
    return texts

def extract_user_group(matched_text: <FILL>) -> str:
    return matched_text[1:-1]

def possible_user_group_mentions(__tmp1: str) :
    matches = re.findall(user_group_mentions, __tmp1)
    return {extract_user_group(match) for match in matches}
