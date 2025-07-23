from typing import TypeAlias
__typ3 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
# See readme.md for instructions on running this code.

import copy
import importlib
from math import log10, floor

import re
from zulip_bots.bots.converter import utils

from typing import Any, Dict, List

def is_float(__tmp2: <FILL>) :
    try:
        float(__tmp2)
        return True
    except ValueError:
        return False

# Rounds the number 'x' to 'digits' significant digits.
# A normal 'round()' would round the number to an absolute amount of
# fractional decimals, e.g. 0.00045 would become 0.0.
# 'round_to()' rounds only the digits that are not 0.
# 0.00045 would then become 0.0005.

def round_to(x, digits: __typ1) :
    return round(x, digits-__typ1(floor(log10(abs(x)))))

class __typ2(object):
    '''
    This plugin allows users to make conversions between various units,
    e.g. Celsius to Fahrenheit, or kilobytes to gigabytes.
    It looks for messages of the format
    '@mention-bot <number> <unit_from> <unit_to>'
    The message '@mention-bot help' posts a short description of how to use
    the plugin, along with a list of all supported units.
    '''

    def __tmp4(__tmp1) -> __typ0:
        return '''
               This plugin allows users to make conversions between
               various units, e.g. Celsius to Fahrenheit,
               or kilobytes to gigabytes. It looks for messages of
               the format '@mention-bot <number> <unit_from> <unit_to>'
               The message '@mention-bot help' posts a short description of
               how to use the plugin, along with a list of
               all supported units.
               '''

    def handle_message(__tmp1, __tmp0, bot_handler: Any) :
        bot_response = __tmp3(__tmp0, bot_handler)
        bot_handler.send_reply(__tmp0, bot_response)

def __tmp3(__tmp0, bot_handler) :
    content = __tmp0['content']

    words = content.lower().split()
    convert_indexes = [i for i, word in enumerate(words) if word == "@convert"]
    convert_indexes = [-1] + convert_indexes
    results = []

    for convert_index in convert_indexes:
        if (convert_index + 1) < len(words) and words[convert_index + 1] == 'help':
            results.append(utils.HELP_MESSAGE)
            continue
        if (convert_index + 3) < len(words):
            number = words[convert_index + 1]
            unit_from = utils.ALIASES.get(words[convert_index + 2], words[convert_index + 2])
            unit_to = utils.ALIASES.get(words[convert_index + 3], words[convert_index + 3])
            exponent = 0

            if not is_float(number):
                results.append('`' + number + '` is not a valid number. ' + utils.QUICK_HELP)
                continue

            # cannot reassign "number" as a float after using as string, so changed name
            convert_num = float(number)
            number_res = copy.copy(convert_num)

            for key, exp in utils.PREFIXES.items():
                if unit_from.startswith(key):
                    exponent += exp
                    unit_from = unit_from[len(key):]
                if unit_to.startswith(key):
                    exponent -= exp
                    unit_to = unit_to[len(key):]

            uf_to_std = utils.UNITS.get(unit_from, [])  # type: List[Any]
            ut_to_std = utils.UNITS.get(unit_to, [])  # type: List[Any]

            if not uf_to_std:
                results.append('`' + unit_from + '` is not a valid unit. ' + utils.QUICK_HELP)
            if not ut_to_std:
                results.append('`' + unit_to + '` is not a valid unit.' + utils.QUICK_HELP)
            if not uf_to_std or not ut_to_std:
                continue

            base_unit = uf_to_std[2]
            if uf_to_std[2] != ut_to_std[2]:
                unit_from = unit_from.capitalize() if uf_to_std[2] == 'kelvin' else unit_from
                results.append('`' + unit_to.capitalize() + '` and `' + unit_from + '`' +
                               ' are not from the same category. ' + utils.QUICK_HELP)
                continue

            # perform the conversion between the units
            number_res *= uf_to_std[1]
            number_res += uf_to_std[0]
            number_res -= ut_to_std[0]
            number_res /= ut_to_std[1]

            if base_unit == 'bit':
                number_res *= 1024 ** (exponent // 3)
            else:
                number_res *= 10 ** exponent
            number_res = round_to(number_res, 7)

            results.append('{} {} = {} {}'.format(number,
                                                  words[convert_index + 2],
                                                  number_res,
                                                  words[convert_index + 3]))

        else:
            results.append('Too few arguments given. ' + utils.QUICK_HELP)

    new_content = ''
    for idx, result in enumerate(results, 1):
        new_content += ((__typ0(idx) + '. conversion: ') if len(results) > 1 else '') + result + '\n'

    return new_content

handler_class = __typ2
