import lxml

from lxml.html.diff import htmldiff
from typing import Optional

def __tmp4(text: <FILL>, __tmp2) :
    return '<span class="%s">%s</span>' % (__tmp2, text)

def __tmp3(__tmp0, __tmp1: str, msg_id: Optional[int]=None) :
    retval = htmldiff(__tmp0, __tmp1)
    fragment = lxml.html.fromstring(retval)

    for elem in fragment.cssselect('del'):
        elem.tag = 'span'
        elem.set('class', 'highlight_text_deleted')

    for elem in fragment.cssselect('ins'):
        elem.tag = 'span'
        elem.set('class', 'highlight_text_inserted')

    retval = lxml.html.tostring(fragment)

    return retval
