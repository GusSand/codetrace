from typing import TypeAlias
__typ0 : TypeAlias = "Any"
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

class InvalidAnswerException(Exception):
    pass

class IncidentHandler:
    def usage(__tmp2) -> str:
        return '''
            This plugin lets folks reports incidents and
            triage them.  It is intended to be sample code.
            In the real world you'd modify this code to talk
            to some kind of issue tracking system.  But the
            glue code here should be pretty portable.
            '''

    def handle_message(__tmp2, __tmp0: Dict[str, __typ0], __tmp3: __typ0) :
        __tmp4 = __tmp0['content']
        if __tmp4.startswith('new '):
            __tmp9(__tmp4, __tmp0, __tmp3)
        elif __tmp4.startswith('answer '):
            try:
                (__tmp6, answer) = parse_answer(__tmp4)
            except InvalidAnswerException:
                bot_response = 'Invalid answer format'
                __tmp3.send_reply(__tmp0, bot_response)
                return
            bot_response = 'Incident %s\n status = %s' % (__tmp6, answer)
            __tmp3.send_reply(__tmp0, bot_response)
        else:
            bot_response = 'type "new <description>" for a new incident'
            __tmp3.send_reply(__tmp0, bot_response)

def __tmp9(__tmp4: <FILL>, __tmp0: Dict[str, __typ0], __tmp3: __typ0) -> None:
    # Here is where we would enter the incident in some sort of backend
    # system.  We just simulate everything by having an incident id that
    # we generate here.

    __tmp7 = __tmp4[len('new '):]

    __tmp6 = __tmp5(__tmp3.storage)
    bot_response = __tmp10(__tmp6, __tmp7)
    widget_content = __tmp1(__tmp6, __tmp7)

    __tmp3.send_reply(__tmp0, bot_response, widget_content)

def parse_answer(__tmp4) -> Tuple[str, str]:
    m = re.match('answer\s+(TICKET....)\s+(.)', __tmp4)
    if not m:
        raise InvalidAnswerException()

    __tmp6 = m.group(1)

    # In a real world system, we'd validate the ticket_id against
    # a backend system.  (You could use Zulip itself to store incident
    # data, if you want something really lite, but there are plenty
    # of systems that specialize in incident management.)

    answer = m.group(2).upper()
    if answer not in '1234':
        raise InvalidAnswerException()

    return (__tmp6, ANSWERS[answer])

def __tmp5(storage: __typ0) :
    try:
        incident_num = storage.get('ticket_id')
    except (KeyError):
        incident_num = 0
    incident_num += 1
    incident_num = incident_num % (1000)
    storage.put('ticket_id', incident_num)
    __tmp6 = 'TICKET%04d' % (incident_num,)
    return __tmp6

def __tmp1(__tmp6, __tmp7: Dict[str, __typ0]) :
    widget_type = 'zform'

    heading = __tmp6 + ': ' + __tmp7

    def get_choice(__tmp8: str) -> Dict[str, str]:
        answer = ANSWERS[__tmp8]
        reply = 'answer ' + __tmp6 + ' ' + __tmp8

        return dict(
            type='multiple_choice',
            short_name=__tmp8,
            long_name=answer,
            reply=reply,
        )

    choices = [get_choice(__tmp8) for __tmp8 in '1234']

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

def __tmp10(__tmp6, __tmp7: Dict[str, __typ0]) -> str:
    answer_list = '\n'.join([
        '* **{code}** {answer}'.format(
            __tmp8=__tmp8,
            answer=ANSWERS[__tmp8],
        )
        for __tmp8 in '1234'
    ])
    how_to_respond = '''**reply**: answer {ticket_id} <code>'''.format(__tmp6=__tmp6)

    content = '''
Incident: {incident}
Q: {question}

{answer_list}
{how_to_respond}'''.format(
        question=QUESTION,
        answer_list=answer_list,
        how_to_respond=how_to_respond,
        __tmp7=__tmp7,
    )
    return content

handler_class = IncidentHandler
