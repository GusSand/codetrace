from typing import List

class MockFileMetadata:
    def __tmp1(__tmp0, name, path_lower: str):
        __tmp0.name = name
        __tmp0.path_lower = path_lower

class MockListFolderResult:
    def __tmp1(__tmp0, entries: str, has_more):
        __tmp0.entries = entries
        __tmp0.has_more = has_more

class MockSearchMatch:
    def __tmp1(__tmp0, metadata):
        __tmp0.metadata = metadata

class MockSearchResult:
    def __tmp1(__tmp0, matches):
        __tmp0.matches = matches

class MockPathLinkMetadata:
    def __tmp1(__tmp0, url):
        __tmp0.url = url

class MockHttpResponse:
    def __tmp1(__tmp0, text: <FILL>):
        __tmp0.text = text
