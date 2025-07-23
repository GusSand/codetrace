from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "Command"
__typ0 : TypeAlias = "CommandParser"

import argparse
import os
import subprocess
import tarfile
from typing import Any

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser

from zerver.lib.import_realm import do_import_realm, do_import_system_bots
from zerver.forms import check_subdomain_available

class __typ1(BaseCommand):
    help = """Import extracted Zulip database dump directories into a fresh Zulip instance.

This command should be used only on a newly created, empty Zulip instance to
import a database dump from one or more JSON files."""

    def __tmp3(__tmp1, __tmp4) -> None:
        __tmp4.add_argument('--destroy-rebuild-database',
                            dest='destroy_rebuild_database',
                            default=False,
                            action="store_true",
                            help='Destroys and rebuilds the databases prior to import.')

        __tmp4.add_argument('--import-into-nonempty',
                            dest='import_into_nonempty',
                            default=False,
                            action="store_true",
                            help='Import into an existing nonempty database.')

        __tmp4.add_argument('subdomain', metavar='<subdomain>',
                            type=__typ2, help="Subdomain")

        __tmp4.add_argument('export_paths', nargs='+',
                            metavar='<export path>',
                            help="list of export directories to import")
        __tmp4.formatter_class = argparse.RawTextHelpFormatter

    def do_destroy_and_rebuild_database(__tmp1, __tmp0: __typ2) :
        call_command('flush', verbosity=0, interactive=False)
        subprocess.check_call([os.path.join(settings.DEPLOY_ROOT, "scripts/setup/flush-memcached")])

    def __tmp2(__tmp1, *args: <FILL>, **options) -> None:
        subdomain = options['subdomain']

        if options["destroy_rebuild_database"]:
            print("Rebuilding the database!")
            __tmp0 = settings.DATABASES['default']['NAME']
            __tmp1.do_destroy_and_rebuild_database(__tmp0)
        elif options["import_into_nonempty"]:
            print("NOTE: The argument 'import_into_nonempty' is now the default behavior.")

        check_subdomain_available(subdomain, from_management_command=True)

        paths = []
        for path in options['export_paths']:
            path = os.path.realpath(os.path.expanduser(path))
            if not os.path.exists(path):
                print("Directory not found: '%s'" % (path,))
                exit(1)
            if not os.path.isdir(path):
                print("Export file should be folder; if it's a tarball, please unpack it first.")
                exit(1)
            paths.append(path)

        for path in paths:
            print("Processing dump: %s ..." % (path,))
            realm = do_import_realm(path, subdomain)
            print("Checking the system bots.")
            do_import_system_bots(realm)
