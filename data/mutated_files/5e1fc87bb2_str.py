# -*- coding: utf-8 -*-
import operator

from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils.lru_cache import lru_cache

from itertools import zip_longest
from typing import Any, List, Dict, Optional

import os
import ujson

def with_language(string: str, __tmp3: str) -> str:
    """
    This is an expensive function. If you are using it in a loop, it will
    make your code slow.
    """
    old_language = translation.get_language()
    translation.activate(__tmp3)
    result = _(string)
    translation.activate(old_language)
    return result

@lru_cache()
def __tmp0() :
    path = os.path.join(settings.STATIC_ROOT, 'locale', 'language_name_map.json')
    with open(path, 'r') as reader:
        languages = ujson.load(reader)
        return languages['name_map']

def get_language_list_for_templates(__tmp4: str) :
    language_list = [l for l in __tmp0()
                     if 'percent_translated' not in l or
                        l['percent_translated'] >= 5.]

    formatted_list = []
    lang_len = len(language_list)
    firsts_end = (lang_len // 2) + operator.mod(lang_len, 2)
    firsts = list(range(0, firsts_end))
    seconds = list(range(firsts_end, lang_len))
    assert len(firsts) + len(seconds) == lang_len
    for row in zip_longest(firsts, seconds):
        item = {}
        for position, ind in zip(['first', 'second'], row):
            if ind is None:
                continue

            lang = language_list[ind]
            percent = name = lang['name']
            if 'percent_translated' in lang:
                percent = "{} ({}%)".format(name, lang['percent_translated'])

            selected = False
            if __tmp4 in (lang['code'], lang['locale']):
                selected = True

            item[position] = {
                'name': name,
                'code': lang['code'],
                'percent': percent,
                'selected': selected
            }

        formatted_list.append(item)

    return formatted_list

def get_language_name(code: <FILL>) -> Optional[str]:
    for lang in __tmp0():
        if code in (lang['code'], lang['locale']):
            return lang['name']
    return None

def __tmp1() :
    language_list = __tmp0()
    codes = [__tmp3['code'] for __tmp3 in language_list]
    return codes

def __tmp2(__tmp3) -> Dict[str, str]:
    if __tmp3 == 'zh-hans':
        __tmp3 = 'zh_Hans'
    elif __tmp3 == 'zh-hant':
        __tmp3 = 'zh_Hant'
    elif __tmp3 == 'id-id':
        __tmp3 = 'id_ID'
    path = os.path.join(settings.STATIC_ROOT, 'locale', __tmp3, 'translations.json')
    try:
        with open(path, 'r') as reader:
            return ujson.load(reader)
    except FileNotFoundError:
        print('Translation for {} not found at {}'.format(__tmp3, path))
        return {}
