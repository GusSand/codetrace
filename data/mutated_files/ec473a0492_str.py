# See readme.md for instructions on running this code.
import logging
from urllib import parse

import requests

from bs4 import BeautifulSoup

from typing import Dict, Any, Union, List

def __tmp4(__tmp6: str) :
    query = {'q': __tmp6}
    # Gets the page
    page = requests.get('http://www.google.com/search', params=query)
    # Parses the page into BeautifulSoup
    soup = BeautifulSoup(page.text, "lxml")

    # Gets all search URLs
    anchors = soup.find(id='search').findAll('a')
    results = []

    for a in anchors:
        try:
            # Tries to get the href property of the URL
            link = a['href']
        except KeyError:
            continue
        # Link must start with '/url?', as these are the search result links
        if not link.startswith('/url?'):
            continue
        # Makes sure a hidden 'cached' result isn't displayed
        if a.text.strip() == 'Cached' and 'webcache.googleusercontent.com' in a['href']:
            continue
        # a.text: The name of the page
        result = {'url': "https://www.google.com{}".format(link),
                  'name': a.text}
        results.append(result)
    return results

def get_google_result(__tmp5: <FILL>) -> str:
    help_message = "To use this bot, start messages with @mentioned-bot, \
                    followed by what you want to search for. If \
                    found, Zulip will return the first search result \
                    on Google.\
                    \
                    An example message that could be sent is:\
                    '@mentioned-bot zulip' or \
                    '@mentioned-bot how to create a chatbot'."

    __tmp5 = __tmp5.strip()

    if __tmp5 == 'help':
        return help_message
    elif __tmp5 == '' or __tmp5 is None:
        return help_message
    else:
        try:
            results = __tmp4(__tmp5)
            if (len(results) == 0):
                return "Found no results."
            return "Found Result: [{}]({})".format(results[0]['name'], results[0]['url'])
        except Exception as e:
            logging.exception(str(e))
            return 'Error: Search failed. {}.'.format(e)

class GoogleSearchHandler(object):
    '''
    This plugin allows users to enter a search
    term in Zulip and get the top URL sent back
    to the context (stream or private) in which
    it was called. It looks for messages starting
    with @mentioned-bot.
    '''

    def __tmp7(__tmp1) -> str:
        return '''
            This plugin will allow users to search
            for a given search term on Google from
            Zulip. Use '@mentioned-bot help' to get
            more information on the bot usage. Users
            should preface messages with
            @mentioned-bot.
            '''

    def __tmp2(__tmp1, __tmp0: Dict[str, str], __tmp3) -> None:
        original_content = __tmp0['content']
        result = get_google_result(original_content)
        __tmp3.send_reply(__tmp0, result)

handler_class = GoogleSearchHandler
