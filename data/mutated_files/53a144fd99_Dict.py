from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""handles the mailing operations across the app."""

import traceback
from typing import Dict

import requests
from requests.models import Response

from exceptions import FailedToSendMail


class __typ1:
    """Send a mail through the Mailgun API."""

    auth = None
    api_url = None
    sender = None

    def __tmp5(__tmp0, __tmp4, api_key, __tmp1) :
        """
        Initialize the Mailer class.

        :param domain: Domain name of the sender
        :type domain: str
        :param api_key: API key of the Mailgun API
        :type api_key: str
        :param sender_name: name of the person sending the email
        :type sender_name: str
        """
        __tmp0.auth = ("api", api_key)
        __tmp0.api_url = f"https://api.mailgun.net/v3/{__tmp4}"
        __tmp0.sender = f"{__tmp1} <noreply@{__tmp4}>"

    def __tmp3(__tmp0, __tmp2: <FILL>) :
        """
        Send a message.

        :param data: A dict consisting of the data for email
        :type data: dict
        :return: A Response object
        :rtype: requests.Response
        """
        __tmp2['from'] = __tmp0.sender
        try:
            return requests.post(f"{__tmp0.api_url}/messages", auth=__tmp0.auth, __tmp2=__tmp2)
        except (requests.HTTPError, requests.ConnectionError):
            traceback.print_exc()
            raise FailedToSendMail
