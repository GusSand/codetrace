import lxml

from lxml.html.diff import htmldiff
from typing import Optional

def highlight_with_class(__tmp0: str, __tmp1: str) -> str:
    return '<span class="%s">%s</span>' % (__tmp1, __tmp0)

def highlight_html_differences(s1: <FILL>, s2: str, msg_id: Optional[int]=None) -> str:
    retval = htmldiff(s1, s2)
    fragment = lxml.html.fromstring(retval)

    for elem in fragment.cssselect('del'):
        elem.tag = 'span'
        elem.set('class', 'highlight_text_deleted')

    for elem in fragment.cssselect('ins'):
        elem.tag = 'span'
        elem.set('class', 'highlight_text_inserted')

    retval = lxml.html.tostring(fragment)

    return retval
