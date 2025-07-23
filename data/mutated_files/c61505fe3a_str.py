import re
import os
import sys
import logging
import configparser

import requests

from typing import Dict, Any, Tuple, Union

class __typ0(object):
    '''
    This bot provides details on github issues and pull requests when they're
    referenced in the chat.
    '''

    GITHUB_ISSUE_URL_TEMPLATE = 'https://api.github.com/repos/{owner}/{repo}/issues/{id}'
    HANDLE_MESSAGE_REGEX = re.compile("(?:([\w-]+)\/)?([\w-]+)?#(\d+)")

    def __tmp5(__tmp1, __tmp3: Any) -> None:
        __tmp1.config_info = __tmp3.get_config_info('github_detail', optional=True)
        __tmp1.owner = __tmp1.config_info.get("owner", False)
        __tmp1.repo = __tmp1.config_info.get("repo", False)

    def usage(__tmp1) -> str:
        return ("This plugin displays details on github issues and pull requests. "
                "To reference an issue or pull request usename mention the bot then "
                "anytime in the message type its id, for example:\n"
                "@**Github detail** #3212 zulip#3212 zulip/zulip#3212\n"
                "The default owner is {} and the default repo is {}.".format(__tmp1.owner, __tmp1.repo))

    def format_message(__tmp1, __tmp4) -> str:
        __tmp7 = __tmp4['number']
        title = __tmp4['title']
        link = __tmp4['html_url']
        author = __tmp4['user']['login']
        owner = __tmp4['owner']
        repo = __tmp4['repo']

        description = __tmp4['body']
        status = __tmp4['state'].title()

        message_string = ('**[{owner}/{repo}#{id}]'.format(owner=owner, repo=repo, id=__tmp7),
                          '({link}) - {title}**\n'.format(title=title, link=link),
                          'Created by **[{author}](https://github.com/{author})**\n'.format(author=author),
                          'Status - **{status}**\n```quote\n{description}\n```'.format(status=status, description=description))
        return ''.join(message_string)

    def get_details_from_github(__tmp1, owner, repo: <FILL>, __tmp7) -> Union[None, Dict[str, Union[str, int, bool]]]:
        # Gets the details of an issues or pull request
        try:
            r = requests.get(
                __tmp1.GITHUB_ISSUE_URL_TEMPLATE.format(owner=owner, repo=repo, id=__tmp7))
        except requests.exceptions.RequestException as e:
            logging.exception(str(e))
            return None
        if r.status_code != requests.codes.ok:
            return None
        return r.json()

    def get_owner_and_repo(__tmp1, __tmp6: Any) -> Tuple[str, str]:
        owner = __tmp6.group(1)
        repo = __tmp6.group(2)
        if owner is None:
            owner = __tmp1.owner
            if repo is None:
                repo = __tmp1.repo
        return (owner, repo)

    def __tmp2(__tmp1, __tmp0, __tmp3) -> None:
        # Send help message
        if __tmp0['content'] == 'help':
            __tmp3.send_reply(__tmp0, __tmp1.usage())
            return

        # Capture owner, repo, id
        issue_prs = list(re.finditer(
            __tmp1.HANDLE_MESSAGE_REGEX, __tmp0['content']))
        bot_messages = []
        if len(issue_prs) > 5:
            # We limit to 5 requests to prevent denial-of-service
            bot_message = 'Please ask for <=5 links in any one request'
            __tmp3.send_reply(__tmp0, bot_message)
            return

        for __tmp6 in issue_prs:
            owner, repo = __tmp1.get_owner_and_repo(__tmp6)
            if owner and repo:
                __tmp4 = __tmp1.get_details_from_github(owner, repo, __tmp6.group(3))
                if __tmp4 is not None:
                    __tmp4['owner'] = owner
                    __tmp4['repo'] = repo
                    bot_messages.append(__tmp1.format_message(__tmp4))
                else:
                    bot_messages.append("Failed to find issue/pr: {owner}/{repo}#{id}"
                                        .format(owner=owner, repo=repo, id=__tmp6.group(3)))
            else:
                bot_messages.append("Failed to detect owner and repository name.")
        if len(bot_messages) == 0:
            bot_messages.append("Failed to find any issue or PR.")
        bot_message = '\n'.join(bot_messages)
        __tmp3.send_reply(__tmp0, bot_message)

handler_class = __typ0
