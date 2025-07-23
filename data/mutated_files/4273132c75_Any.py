from typing import TypeAlias
__typ2 : TypeAlias = "ArgumentParser"
__typ1 : TypeAlias = "Command"
__typ0 : TypeAlias = "str"

import sys
from argparse import ArgumentParser
from typing import Any

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from zerver.lib.domains import validate_domain
from zerver.lib.management import ZulipBaseCommand
from zerver.models import RealmDomain, get_realm_domains

class __typ1(ZulipBaseCommand):
    help = """Manage domains for the specified realm"""

    def add_arguments(__tmp0, parser) :
        parser.add_argument('--op',
                            dest='op',
                            type=__typ0,
                            default="show",
                            help='What operation to do (add, show, remove).')
        parser.add_argument('--allow-subdomains',
                            dest='allow_subdomains',
                            action="store_true",
                            default=False,
                            help='Whether subdomains are allowed or not.')
        parser.add_argument('domain', metavar='<domain>', type=__typ0, nargs='?',
                            help="domain to add or remove")
        __tmp0.add_realm_args(parser, True)

    def __tmp1(__tmp0, *args: <FILL>, **options) :
        realm = __tmp0.get_realm(options)
        assert realm is not None  # Should be ensured by parser
        if options["op"] == "show":
            print("Domains for %s:" % (realm.string_id,))
            for realm_domain in get_realm_domains(realm):
                if realm_domain["allow_subdomains"]:
                    print(realm_domain["domain"] + " (subdomains allowed)")
                else:
                    print(realm_domain["domain"] + " (subdomains not allowed)")
            sys.exit(0)

        domain = options['domain'].strip().lower()
        try:
            validate_domain(domain)
        except ValidationError as e:
            print(e.messages[0])
            sys.exit(1)
        if options["op"] == "add":
            try:
                RealmDomain.objects.create(realm=realm, domain=domain,
                                           allow_subdomains=options["allow_subdomains"])
                sys.exit(0)
            except IntegrityError:
                print("The domain %(domain)s is already a part of your organization." % {'domain': domain})
                sys.exit(1)
        elif options["op"] == "remove":
            try:
                RealmDomain.objects.get(realm=realm, domain=domain).delete()
                sys.exit(0)
            except RealmDomain.DoesNotExist:
                print("No such entry found!")
                sys.exit(1)
        else:
            __tmp0.print_help("./manage.py", "realm_domain")
            sys.exit(1)
