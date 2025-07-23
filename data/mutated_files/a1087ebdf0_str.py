from typing import TypeAlias
__typ2 : TypeAlias = "Any"
import html
import json
import random
import re
from zulip_bots.lib import Any

from typing import Optional, Any, Dict, Tuple

QUESTION = 'How should we handle this?'

ANSWERS = {
    '1': 'known issue',
    '2': 'ignore',
    '3': 'in process',
    '4': 'escalate',
}

class __typ1(Exception):
    pass

class __typ0:
    def __tmp11(__tmp2) :
        return '''
            This plugin lets folks reports incidents and
            triage them.  It is intended to be sample code.
            In the real world you'd modify this code to talk
            to some kind of issue tracking system.  But the
            glue code here should be pretty portable.
            '''

    def __tmp3(__tmp2, __tmp0, __tmp4) :
        __tmp5 = __tmp0['content']
        if __tmp5.startswith('new '):
            __tmp12(__tmp5, __tmp0, __tmp4)
        elif __tmp5.startswith('answer '):
            try:
                (__tmp7, answer) = __tmp9(__tmp5)
            except __typ1:
                bot_response = 'Invalid answer format'
                __tmp4.send_reply(__tmp0, bot_response)
                return
            bot_response = 'Incident %s\n status = %s' % (__tmp7, answer)
            __tmp4.send_reply(__tmp0, bot_response)
        else:
            bot_response = 'type "new <description>" for a new incident'
            __tmp4.send_reply(__tmp0, bot_response)

def __tmp12(__tmp5, __tmp0, __tmp4) :
    # Here is where we would enter the incident in some sort of backend
    # system.  We just simulate everything by having an incident id that
    # we generate here.

    __tmp8 = __tmp5[len('new '):]

    __tmp7 = __tmp6(__tmp4.storage)
    bot_response = format_incident_for_markdown(__tmp7, __tmp8)
    widget_content = __tmp1(__tmp7, __tmp8)

    __tmp4.send_reply(__tmp0, bot_response, widget_content)

def __tmp9(__tmp5) :
    m = re.match('answer\s+(TICKET....)\s+(.)', __tmp5)
    if not m:
        raise __typ1()

    __tmp7 = m.group(1)

    # In a real world system, we'd validate the ticket_id against
    # a backend system.  (You could use Zulip itself to store incident
    # data, if you want something really lite, but there are plenty
    # of systems that specialize in incident management.)

    answer = m.group(2).upper()
    if answer not in '1234':
        raise __typ1()

    return (__tmp7, ANSWERS[answer])

def __tmp6(storage) :
    try:
        incident_num = storage.get('ticket_id')
    except (KeyError):
        incident_num = 0
    incident_num += 1
    incident_num = incident_num % (1000)
    storage.put('ticket_id', incident_num)
    __tmp7 = 'TICKET%04d' % (incident_num,)
    return __tmp7

def __tmp1(__tmp7, __tmp8) :
    widget_type = 'zform'

    heading = __tmp7 + ': ' + __tmp8

    def get_choice(__tmp10) :
        answer = ANSWERS[__tmp10]
        reply = 'answer ' + __tmp7 + ' ' + __tmp10

        return dict(
            type='multiple_choice',
            short_name=__tmp10,
            long_name=answer,
            reply=reply,
        )

    choices = [get_choice(__tmp10) for __tmp10 in '1234']

    extra_data = dict(
        type='choices',
        heading=heading,
        choices=choices,
    )

    widget_content = dict(
        widget_type=widget_type,
        extra_data=extra_data,
    )
    payload = json.dumps(widget_content)
    return payload

def format_incident_for_markdown(__tmp7: <FILL>, __tmp8) :
    answer_list = '\n'.join([
        '* **{code}** {answer}'.format(
            __tmp10=__tmp10,
            answer=ANSWERS[__tmp10],
        )
        for __tmp10 in '1234'
    ])
    how_to_respond = '''**reply**: answer {ticket_id} <code>'''.format(__tmp7=__tmp7)

    content = '''
Incident: {incident}
Q: {question}

{answer_list}
{how_to_respond}'''.format(
        question=QUESTION,
        answer_list=answer_list,
        how_to_respond=how_to_respond,
        __tmp8=__tmp8,
    )
    return content

handler_class = __typ0
