from typing import TypeAlias
__typ0 : TypeAlias = "str"
import re
import os
import sys
import logging
import configparser

import requests

from typing import Dict, Any, Tuple, Union

class GithubHandler(object):
    '''
    This bot provides details on github issues and pull requests when they're
    referenced in the chat.
    '''

    GITHUB_ISSUE_URL_TEMPLATE = 'https://api.github.com/repos/{owner}/{repo}/issues/{id}'
    HANDLE_MESSAGE_REGEX = re.compile("(?:([\w-]+)\/)?([\w-]+)?#(\d+)")

    def initialize(__tmp0, bot_handler: <FILL>) -> None:
        __tmp0.config_info = bot_handler.get_config_info('github_detail', optional=True)
        __tmp0.owner = __tmp0.config_info.get("owner", False)
        __tmp0.repo = __tmp0.config_info.get("repo", False)

    def usage(__tmp0) -> __typ0:
        return ("This plugin displays details on github issues and pull requests. "
                "To reference an issue or pull request usename mention the bot then "
                "anytime in the message type its id, for example:\n"
                "@**Github detail** #3212 zulip#3212 zulip/zulip#3212\n"
                "The default owner is {} and the default repo is {}.".format(__tmp0.owner, __tmp0.repo))

    def format_message(__tmp0, details: Dict[__typ0, Any]) -> __typ0:
        number = details['number']
        title = details['title']
        link = details['html_url']
        author = details['user']['login']
        owner = details['owner']
        repo = details['repo']

        description = details['body']
        status = details['state'].title()

        message_string = ('**[{owner}/{repo}#{id}]'.format(owner=owner, repo=repo, id=number),
                          '({link}) - {title}**\n'.format(title=title, link=link),
                          'Created by **[{author}](https://github.com/{author})**\n'.format(author=author),
                          'Status - **{status}**\n```quote\n{description}\n```'.format(status=status, description=description))
        return ''.join(message_string)

    def get_details_from_github(__tmp0, owner, repo: __typ0, number: __typ0) -> Union[None, Dict[__typ0, Union[__typ0, int, bool]]]:
        # Gets the details of an issues or pull request
        try:
            r = requests.get(
                __tmp0.GITHUB_ISSUE_URL_TEMPLATE.format(owner=owner, repo=repo, id=number))
        except requests.exceptions.RequestException as e:
            logging.exception(__typ0(e))
            return None
        if r.status_code != requests.codes.ok:
            return None
        return r.json()

    def get_owner_and_repo(__tmp0, __tmp1: Any) :
        owner = __tmp1.group(1)
        repo = __tmp1.group(2)
        if owner is None:
            owner = __tmp0.owner
            if repo is None:
                repo = __tmp0.repo
        return (owner, repo)

    def handle_message(__tmp0, message: Dict[__typ0, __typ0], bot_handler) -> None:
        # Send help message
        if message['content'] == 'help':
            bot_handler.send_reply(message, __tmp0.usage())
            return

        # Capture owner, repo, id
        issue_prs = list(re.finditer(
            __tmp0.HANDLE_MESSAGE_REGEX, message['content']))
        bot_messages = []
        if len(issue_prs) > 5:
            # We limit to 5 requests to prevent denial-of-service
            bot_message = 'Please ask for <=5 links in any one request'
            bot_handler.send_reply(message, bot_message)
            return

        for __tmp1 in issue_prs:
            owner, repo = __tmp0.get_owner_and_repo(__tmp1)
            if owner and repo:
                details = __tmp0.get_details_from_github(owner, repo, __tmp1.group(3))
                if details is not None:
                    details['owner'] = owner
                    details['repo'] = repo
                    bot_messages.append(__tmp0.format_message(details))
                else:
                    bot_messages.append("Failed to find issue/pr: {owner}/{repo}#{id}"
                                        .format(owner=owner, repo=repo, id=__tmp1.group(3)))
            else:
                bot_messages.append("Failed to detect owner and repository name.")
        if len(bot_messages) == 0:
            bot_messages.append("Failed to find any issue or PR.")
        bot_message = '\n'.join(bot_messages)
        bot_handler.send_reply(message, bot_message)

handler_class = GithubHandler
