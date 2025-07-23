from typing import List

class __typ0:
    def __init__(self, name, path_lower: str):
        self.name = name
        self.path_lower = path_lower

class __typ1:
    def __init__(self, entries: str, has_more: <FILL>):
        self.entries = entries
        self.has_more = has_more

class MockSearchMatch:
    def __init__(self, metadata):
        self.metadata = metadata

class __typ3:
    def __init__(self, matches: List[MockSearchMatch]):
        self.matches = matches

class MockPathLinkMetadata:
    def __init__(self, url: str):
        self.url = url

class __typ2:
    def __init__(self, text):
        self.text = text
