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
    def __tmp4(__tmp1) -> str:
        return '''
            This plugin lets folks reports incidents and
            triage them.  It is intended to be sample code.
            In the real world you'd modify this code to talk
            to some kind of issue tracking system.  But the
            glue code here should be pretty portable.
            '''

    def handle_message(__tmp1, __tmp0, __tmp2) -> None:
        query = __tmp0['content']
        if query.startswith('new '):
            start_new_incident(query, __tmp0, __tmp2)
        elif query.startswith('answer '):
            try:
                (ticket_id, answer) = parse_answer(query)
            except __typ1:
                bot_response = 'Invalid answer format'
                __tmp2.send_reply(__tmp0, bot_response)
                return
            bot_response = 'Incident %s\n status = %s' % (ticket_id, answer)
            __tmp2.send_reply(__tmp0, bot_response)
        else:
            bot_response = 'type "new <description>" for a new incident'
            __tmp2.send_reply(__tmp0, bot_response)

def start_new_incident(query, __tmp0: Dict[str, __typ2], __tmp2) :
    # Here is where we would enter the incident in some sort of backend
    # system.  We just simulate everything by having an incident id that
    # we generate here.

    incident = query[len('new '):]

    ticket_id = generate_ticket_id(__tmp2.storage)
    bot_response = __tmp5(ticket_id, incident)
    widget_content = format_incident_for_widget(ticket_id, incident)

    __tmp2.send_reply(__tmp0, bot_response, widget_content)

def parse_answer(query: str) :
    m = re.match('answer\s+(TICKET....)\s+(.)', query)
    if not m:
        raise __typ1()

    ticket_id = m.group(1)

    # In a real world system, we'd validate the ticket_id against
    # a backend system.  (You could use Zulip itself to store incident
    # data, if you want something really lite, but there are plenty
    # of systems that specialize in incident management.)

    answer = m.group(2).upper()
    if answer not in '1234':
        raise __typ1()

    return (ticket_id, ANSWERS[answer])

def generate_ticket_id(storage: __typ2) :
    try:
        incident_num = storage.get('ticket_id')
    except (KeyError):
        incident_num = 0
    incident_num += 1
    incident_num = incident_num % (1000)
    storage.put('ticket_id', incident_num)
    ticket_id = 'TICKET%04d' % (incident_num,)
    return ticket_id

def format_incident_for_widget(ticket_id, incident) :
    widget_type = 'zform'

    heading = ticket_id + ': ' + incident

    def __tmp3(code: <FILL>) -> Dict[str, str]:
        answer = ANSWERS[code]
        reply = 'answer ' + ticket_id + ' ' + code

        return dict(
            type='multiple_choice',
            short_name=code,
            long_name=answer,
            reply=reply,
        )

    choices = [__tmp3(code) for code in '1234']

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

def __tmp5(ticket_id: str, incident: Dict[str, __typ2]) -> str:
    answer_list = '\n'.join([
        '* **{code}** {answer}'.format(
            code=code,
            answer=ANSWERS[code],
        )
        for code in '1234'
    ])
    how_to_respond = '''**reply**: answer {ticket_id} <code>'''.format(ticket_id=ticket_id)

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

handler_class = __typ0
