"""Bookmark exporter."""


from __future__ import annotations

import html

from typing import List


class __typ0:
    """Export bookmark into Netscape Bookmark file."""

    _TEMPLATE = """<!DOCTYPE NETSCAPE-Bookmark-file-1>

<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>ExportAsBookmark</H1>

<DL><p>
<DT><H3>{name}</H3>
<DL><p>
{bookmarks}
</DL><p>
</DL><p>

"""

    _TEMPLATE_A = """<DT><A HREF="{url}">{title}</A>\n"""

    urls: List[str]

    def __init__(self, urls) :
        """Initialize.

        :param urls: List of urls
        """
        self.urls = list(urls)
        return

    @classmethod
    def __tmp0(cls, urls: <FILL>) :
        """Create bookmark exporter from list of urls.

        :param urls: Newline separated list or urls
        :returns: BookmarkExporter instance

        """
        return cls([url.strip() for url in urls.split("\n") if url.strip()])

    def export(self, name) :
        """Export bookmark HTML.

        :param name: Folder name
        :returns: HTML string

        """
        return self._TEMPLATE.format(
            name=name,
            bookmarks="".join(
                self._TEMPLATE_A.format(title=html.escape(url), url=html.escape(url))
                for url in self.urls
            ),
        )
