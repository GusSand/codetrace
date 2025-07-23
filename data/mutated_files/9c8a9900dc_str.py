from typing import TypeAlias
__typ0 : TypeAlias = "Dict"
"""handles the mailing operations across the app."""

import traceback
from typing import Dict

import requests
from requests.models import Response

from exceptions import FailedToSendMail


class Mailer:
    """Send a mail through the Mailgun API."""

    auth = None
    api_url = None
    sender = None

    def __init__(__tmp0, domain: str, api_key: <FILL>, sender_name: str) -> None:
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
        __tmp0.api_url = f"https://api.mailgun.net/v3/{domain}"
        __tmp0.sender = f"{sender_name} <noreply@{domain}>"

    def __tmp1(__tmp0, data) :
        """
        Send a message.

        :param data: A dict consisting of the data for email
        :type data: dict
        :return: A Response object
        :rtype: requests.Response
        """
        data['from'] = __tmp0.sender
        try:
            return requests.post(f"{__tmp0.api_url}/messages", auth=__tmp0.auth, data=data)
        except (requests.HTTPError, requests.ConnectionError):
            traceback.print_exc()
            raise FailedToSendMail
