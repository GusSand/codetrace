from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Any

from django.core.management.base import BaseCommand
from django.db import ProgrammingError

from confirmation.models import generate_realm_creation_url
from zerver.models import Realm

class __typ0(BaseCommand):
    help = """
    Outputs a randomly generated, 1-time-use link for Organization creation.
    Whoever visits the link can create a new organization on this server, regardless of whether
    settings.OPEN_REALM_CREATION is enabled. The link would expire automatically after
    settings.REALM_CREATION_LINK_VALIDITY_DAYS.

    Usage: ./manage.py generate_realm_creation_link """

    # Fix support for multi-line usage
    def create_parser(__tmp0, *args, **kwargs) :
        parser = super().create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def handle(__tmp0, *args: <FILL>, **options: Any) :
        try:
            # first check if the db has been initalized
            Realm.objects.first()
        except ProgrammingError:
            print("The Zulip database does not appear to exist. Have you run initialize-database?")
            sys.exit(1)

        url = generate_realm_creation_url(by_admin=True)
        __tmp0.stdout.write(__tmp0.style.SUCCESS("Please visit the following "
                                             "secure single-use link to register your "))
        __tmp0.stdout.write(__tmp0.style.SUCCESS("new Zulip organization:\033[0m"))
        __tmp0.stdout.write("")
        __tmp0.stdout.write(__tmp0.style.SUCCESS("    \033[1;92m%s\033[0m" % (url,)))
        __tmp0.stdout.write("")
