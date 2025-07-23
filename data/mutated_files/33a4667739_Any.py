from typing import TypeAlias
__typ0 : TypeAlias = "str"
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

class __typ2:
    def usage(__tmp1) -> __typ0:
        return '''
            This plugin lets folks reports incidents and
            triage them.  It is intended to be sample code.
            In the real world you'd modify this code to talk
            to some kind of issue tracking system.  But the
            glue code here should be pretty portable.
            '''

    def __tmp2(__tmp1, __tmp0, bot_handler: <FILL>) -> None:
        __tmp3 = __tmp0['content']
        if __tmp3.startswith('new '):
            start_new_incident(__tmp3, __tmp0, bot_handler)
        elif __tmp3.startswith('answer '):
            try:
                (__tmp5, answer) = parse_answer(__tmp3)
            except __typ1:
                bot_response = 'Invalid answer format'
                bot_handler.send_reply(__tmp0, bot_response)
                return
            bot_response = 'Incident %s\n status = %s' % (__tmp5, answer)
            bot_handler.send_reply(__tmp0, bot_response)
        else:
            bot_response = 'type "new <description>" for a new incident'
            bot_handler.send_reply(__tmp0, bot_response)

def start_new_incident(__tmp3: __typ0, __tmp0: Dict[__typ0, Any], bot_handler: Any) -> None:
    # Here is where we would enter the incident in some sort of backend
    # system.  We just simulate everything by having an incident id that
    # we generate here.

    incident = __tmp3[len('new '):]

    __tmp5 = generate_ticket_id(bot_handler.storage)
    bot_response = format_incident_for_markdown(__tmp5, incident)
    widget_content = format_incident_for_widget(__tmp5, incident)

    bot_handler.send_reply(__tmp0, bot_response, widget_content)

def parse_answer(__tmp3: __typ0) -> Tuple[__typ0, __typ0]:
    m = re.match('answer\s+(TICKET....)\s+(.)', __tmp3)
    if not m:
        raise __typ1()

    __tmp5 = m.group(1)

    # In a real world system, we'd validate the ticket_id against
    # a backend system.  (You could use Zulip itself to store incident
    # data, if you want something really lite, but there are plenty
    # of systems that specialize in incident management.)

    answer = m.group(2).upper()
    if answer not in '1234':
        raise __typ1()

    return (__tmp5, ANSWERS[answer])

def generate_ticket_id(storage: Any) -> __typ0:
    try:
        incident_num = storage.get('ticket_id')
    except (KeyError):
        incident_num = 0
    incident_num += 1
    incident_num = incident_num % (1000)
    storage.put('ticket_id', incident_num)
    __tmp5 = 'TICKET%04d' % (incident_num,)
    return __tmp5

def format_incident_for_widget(__tmp5, incident) :
    widget_type = 'zform'

    heading = __tmp5 + ': ' + incident

    def __tmp4(__tmp6) -> Dict[__typ0, __typ0]:
        answer = ANSWERS[__tmp6]
        reply = 'answer ' + __tmp5 + ' ' + __tmp6

        return dict(
            type='multiple_choice',
            short_name=__tmp6,
            long_name=answer,
            reply=reply,
        )

    choices = [__tmp4(__tmp6) for __tmp6 in '1234']

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

def format_incident_for_markdown(__tmp5: __typ0, incident: Dict[__typ0, Any]) -> __typ0:
    answer_list = '\n'.join([
        '* **{code}** {answer}'.format(
            __tmp6=__tmp6,
            answer=ANSWERS[__tmp6],
        )
        for __tmp6 in '1234'
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
        incident=incident,
    )
    return content

handler_class = __typ2
