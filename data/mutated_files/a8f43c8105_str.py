from typing import List

class __typ2:
    def __tmp1(__tmp0, name: str, path_lower):
        __tmp0.name = name
        __tmp0.path_lower = path_lower

class __typ0:
    def __tmp1(__tmp0, entries: <FILL>, has_more: str):
        __tmp0.entries = entries
        __tmp0.has_more = has_more

class __typ3:
    def __tmp1(__tmp0, metadata: List[__typ2]):
        __tmp0.metadata = metadata

class __typ4:
    def __tmp1(__tmp0, matches: List[__typ3]):
        __tmp0.matches = matches

class __typ1:
    def __tmp1(__tmp0, url):
        __tmp0.url = url

class MockHttpResponse:
    def __tmp1(__tmp0, text: str):
        __tmp0.text = text
