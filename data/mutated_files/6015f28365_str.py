from typing import TypeAlias
__typ1 : TypeAlias = "Any"
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

class __typ0(Exception):
    pass

class IncidentHandler:
    def usage(__tmp1) :
        return '''
            This plugin lets folks reports incidents and
            triage them.  It is intended to be sample code.
            In the real world you'd modify this code to talk
            to some kind of issue tracking system.  But the
            glue code here should be pretty portable.
            '''

    def handle_message(__tmp1, __tmp0: Dict[str, __typ1], __tmp2) -> None:
        __tmp3 = __tmp0['content']
        if __tmp3.startswith('new '):
            start_new_incident(__tmp3, __tmp0, __tmp2)
        elif __tmp3.startswith('answer '):
            try:
                (__tmp5, answer) = parse_answer(__tmp3)
            except __typ0:
                bot_response = 'Invalid answer format'
                __tmp2.send_reply(__tmp0, bot_response)
                return
            bot_response = 'Incident %s\n status = %s' % (__tmp5, answer)
            __tmp2.send_reply(__tmp0, bot_response)
        else:
            bot_response = 'type "new <description>" for a new incident'
            __tmp2.send_reply(__tmp0, bot_response)

def start_new_incident(__tmp3, __tmp0, __tmp2) :
    # Here is where we would enter the incident in some sort of backend
    # system.  We just simulate everything by having an incident id that
    # we generate here.

    __tmp6 = __tmp3[len('new '):]

    __tmp5 = __tmp4(__tmp2.storage)
    bot_response = __tmp9(__tmp5, __tmp6)
    widget_content = __tmp8(__tmp5, __tmp6)

    __tmp2.send_reply(__tmp0, bot_response, widget_content)

def parse_answer(__tmp3) :
    m = re.match('answer\s+(TICKET....)\s+(.)', __tmp3)
    if not m:
        raise __typ0()

    __tmp5 = m.group(1)

    # In a real world system, we'd validate the ticket_id against
    # a backend system.  (You could use Zulip itself to store incident
    # data, if you want something really lite, but there are plenty
    # of systems that specialize in incident management.)

    answer = m.group(2).upper()
    if answer not in '1234':
        raise __typ0()

    return (__tmp5, ANSWERS[answer])

def __tmp4(storage) -> str:
    try:
        incident_num = storage.get('ticket_id')
    except (KeyError):
        incident_num = 0
    incident_num += 1
    incident_num = incident_num % (1000)
    storage.put('ticket_id', incident_num)
    __tmp5 = 'TICKET%04d' % (incident_num,)
    return __tmp5

def __tmp8(__tmp5: <FILL>, __tmp6) -> str:
    widget_type = 'zform'

    heading = __tmp5 + ': ' + __tmp6

    def get_choice(__tmp7: str) -> Dict[str, str]:
        answer = ANSWERS[__tmp7]
        reply = 'answer ' + __tmp5 + ' ' + __tmp7

        return dict(
            type='multiple_choice',
            short_name=__tmp7,
            long_name=answer,
            reply=reply,
        )

    choices = [get_choice(__tmp7) for __tmp7 in '1234']

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

def __tmp9(__tmp5, __tmp6) :
    answer_list = '\n'.join([
        '* **{code}** {answer}'.format(
            __tmp7=__tmp7,
            answer=ANSWERS[__tmp7],
        )
        for __tmp7 in '1234'
    ])
    how_to_respond = '''**reply**: answer {ticket_id} <code>'''.format(__tmp5=__tmp5)

    content = '''
Incident: {incident}
Q: {question}

{answer_list}
{how_to_respond}'''.format(
        question=QUESTION,
        answer_list=answer_list,
        how_to_respond=how_to_respond,
        __tmp6=__tmp6,
    )
    return content

handler_class = IncidentHandler
