from typing import TypeAlias
__typ0 : TypeAlias = "Command"
# -*- coding: utf-8 -*-
import argparse
import os
from typing import Any

from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS

from scripts.lib.zulip_tools import get_dev_uuid_var_path
from zerver.lib.test_fixtures import get_migration_status

class __typ0(BaseCommand):
    help = "Get status of migrations."

    def __tmp0(__tmp1, __tmp2) -> None:
        __tmp2.add_argument('app_label', nargs='?',
                            help='App label of an application to synchronize the state.')

        __tmp2.add_argument('--database', action='store', dest='database',
                            default=DEFAULT_DB_ALIAS, help='Nominates a database to synchronize. '
                            'Defaults to the "default" database.')

        __tmp2.add_argument('--output', action='store',
                            help='Path to store the status to (default to stdout).')

    def __tmp3(__tmp1, *args: Any, **options: <FILL>) -> None:
        result = get_migration_status(**options)
        if options['output'] is not None:
            uuid_var_path = get_dev_uuid_var_path()
            path = os.path.join(uuid_var_path, options['output'])
            with open(path, 'w') as f:
                f.write(result)
        else:
            __tmp1.stdout.write(result)
