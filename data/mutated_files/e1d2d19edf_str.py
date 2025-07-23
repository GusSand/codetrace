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

    def __tmp3(__tmp0, urls: List[str]) -> None:
        """Initialize.

        :param urls: List of urls
        """
        __tmp0.urls = list(urls)
        return

    @classmethod
    def __tmp1(__tmp2, urls) :
        """Create bookmark exporter from list of urls.

        :param urls: Newline separated list or urls
        :returns: BookmarkExporter instance

        """
        return __tmp2([url.strip() for url in urls.split("\n") if url.strip()])

    def __tmp4(__tmp0, name: <FILL>) -> str:
        """Export bookmark HTML.

        :param name: Folder name
        :returns: HTML string

        """
        return __tmp0._TEMPLATE.format(
            name=name,
            bookmarks="".join(
                __tmp0._TEMPLATE_A.format(title=html.escape(url), url=html.escape(url))
                for url in __tmp0.urls
            ),
        )
