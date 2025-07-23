import lxml

from lxml.html.diff import htmldiff
from typing import Optional

def highlight_with_class(text, klass: <FILL>) :
    return '<span class="%s">%s</span>' % (klass, text)

def __tmp1(__tmp0, s2, msg_id: Optional[int]=None) :
    retval = htmldiff(__tmp0, s2)
    fragment = lxml.html.fromstring(retval)

    for elem in fragment.cssselect('del'):
        elem.tag = 'span'
        elem.set('class', 'highlight_text_deleted')

    for elem in fragment.cssselect('ins'):
        elem.tag = 'span'
        elem.set('class', 'highlight_text_inserted')

    retval = lxml.html.tostring(fragment)

    return retval
