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

class InvalidAnswerException(Exception):
    pass

class IncidentHandler:
    def __tmp6(__tmp3) -> __typ0:
        return '''
            This plugin lets folks reports incidents and
            triage them.  It is intended to be sample code.
            In the real world you'd modify this code to talk
            to some kind of issue tracking system.  But the
            glue code here should be pretty portable.
            '''

    def __tmp2(__tmp3, __tmp0, __tmp4: Any) -> None:
        __tmp5 = __tmp0['content']
        if __tmp5.startswith('new '):
            start_new_incident(__tmp5, __tmp0, __tmp4)
        elif __tmp5.startswith('answer '):
            try:
                (__tmp8, answer) = __tmp11(__tmp5)
            except InvalidAnswerException:
                bot_response = 'Invalid answer format'
                __tmp4.send_reply(__tmp0, bot_response)
                return
            bot_response = 'Incident %s\n status = %s' % (__tmp8, answer)
            __tmp4.send_reply(__tmp0, bot_response)
        else:
            bot_response = 'type "new <description>" for a new incident'
            __tmp4.send_reply(__tmp0, bot_response)

def start_new_incident(__tmp5: __typ0, __tmp0: Dict[__typ0, Any], __tmp4: Any) -> None:
    # Here is where we would enter the incident in some sort of backend
    # system.  We just simulate everything by having an incident id that
    # we generate here.

    __tmp10 = __tmp5[len('new '):]

    __tmp8 = __tmp9(__tmp4.storage)
    bot_response = __tmp13(__tmp8, __tmp10)
    widget_content = __tmp1(__tmp8, __tmp10)

    __tmp4.send_reply(__tmp0, bot_response, widget_content)

def __tmp11(__tmp5: __typ0) -> Tuple[__typ0, __typ0]:
    m = re.match('answer\s+(TICKET....)\s+(.)', __tmp5)
    if not m:
        raise InvalidAnswerException()

    __tmp8 = m.group(1)

    # In a real world system, we'd validate the ticket_id against
    # a backend system.  (You could use Zulip itself to store incident
    # data, if you want something really lite, but there are plenty
    # of systems that specialize in incident management.)

    answer = m.group(2).upper()
    if answer not in '1234':
        raise InvalidAnswerException()

    return (__tmp8, ANSWERS[answer])

def __tmp9(storage: <FILL>) -> __typ0:
    try:
        incident_num = storage.get('ticket_id')
    except (KeyError):
        incident_num = 0
    incident_num += 1
    incident_num = incident_num % (1000)
    storage.put('ticket_id', incident_num)
    __tmp8 = 'TICKET%04d' % (incident_num,)
    return __tmp8

def __tmp1(__tmp8: __typ0, __tmp10: Dict[__typ0, Any]) -> __typ0:
    widget_type = 'zform'

    heading = __tmp8 + ': ' + __tmp10

    def __tmp7(__tmp12: __typ0) -> Dict[__typ0, __typ0]:
        answer = ANSWERS[__tmp12]
        reply = 'answer ' + __tmp8 + ' ' + __tmp12

        return dict(
            type='multiple_choice',
            short_name=__tmp12,
            long_name=answer,
            reply=reply,
        )

    choices = [__tmp7(__tmp12) for __tmp12 in '1234']

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

def __tmp13(__tmp8: __typ0, __tmp10: Dict[__typ0, Any]) -> __typ0:
    answer_list = '\n'.join([
        '* **{code}** {answer}'.format(
            __tmp12=__tmp12,
            answer=ANSWERS[__tmp12],
        )
        for __tmp12 in '1234'
    ])
    how_to_respond = '''**reply**: answer {ticket_id} <code>'''.format(__tmp8=__tmp8)

    content = '''
Incident: {incident}
Q: {question}

{answer_list}
{how_to_respond}'''.format(
        question=QUESTION,
        answer_list=answer_list,
        how_to_respond=how_to_respond,
        __tmp10=__tmp10,
    )
    return content

handler_class = IncidentHandler
