from typing import TypeAlias
__typ0 : TypeAlias = "str"

from typing import Any, Callable, Dict, List, Set

from django.db import connection

from zerver.lib.management import ZulipBaseCommand

def __tmp1(index_name: __typ0, table_name,
                              column_string: __typ0, where_clause: __typ0) -> None:
    #
    #  This function is somewhat similar to
    #  zerver.lib.migrate.create_index_if_not_exist.
    #
    #  The other function gets used as part of Django migrations; this function
    #  uses SQL that is not supported by Django migrations.
    #
    #  Creating concurrent indexes is kind of a pain with current versions
    #  of Django/postgres, because you will get this error with seemingly
    #  reasonable code:
    #
    #    CREATE INDEX CONCURRENTLY cannot be executed from a function or multi-command string
    #
    # For a lot more detail on this process, refer to the commit message
    # that added this file to the repo.

    with connection.cursor() as cursor:
        sql = '''
            SELECT 1
            FROM pg_class
            where relname = %s
            '''
        cursor.execute(sql, [index_name])
        rows = cursor.fetchall()
        if len(rows) > 0:
            print('Index %s already exists.' % (index_name,))
            return

        print("Creating index %s." % (index_name,))
        sql = '''
            CREATE INDEX CONCURRENTLY
            %s
            ON %s (%s)
            %s;
            ''' % (index_name, table_name, column_string, where_clause)
        cursor.execute(sql)
        print('Finished creating %s.' % (index_name,))


def __tmp0() :

    # copied from 0082
    __tmp1(
        index_name='zerver_usermessage_starred_message_id',
        table_name='zerver_usermessage',
        column_string='user_profile_id, message_id',
        where_clause='WHERE (flags & 2) != 0',
    )

    # copied from 0083
    __tmp1(
        index_name='zerver_usermessage_mentioned_message_id',
        table_name='zerver_usermessage',
        column_string='user_profile_id, message_id',
        where_clause='WHERE (flags & 8) != 0',
    )

    # copied from 0095
    __tmp1(
        index_name='zerver_usermessage_unread_message_id',
        table_name='zerver_usermessage',
        column_string='user_profile_id, message_id',
        where_clause='WHERE (flags & 1) = 0',
    )

    # copied from 0098
    __tmp1(
        index_name='zerver_usermessage_has_alert_word_message_id',
        table_name='zerver_usermessage',
        column_string='user_profile_id, message_id',
        where_clause='WHERE (flags & 512) != 0',
    )

    # copied from 0099
    __tmp1(
        index_name='zerver_usermessage_wildcard_mentioned_message_id',
        table_name='zerver_usermessage',
        column_string='user_profile_id, message_id',
        where_clause='WHERE (flags & 8) != 0 OR (flags & 16) != 0',
    )

    # copied from 0177
    __tmp1(
        index_name='zerver_usermessage_is_private_message_id',
        table_name='zerver_usermessage',
        column_string='user_profile_id, message_id',
        where_clause='WHERE (flags & 2048) != 0',
    )

    # copied from 0180
    __tmp1(
        index_name='zerver_usermessage_active_mobile_push_notification_id',
        table_name='zerver_usermessage',
        column_string='user_profile_id, message_id',
        where_clause='WHERE (flags & 4096) != 0',
    )

class Command(ZulipBaseCommand):
    help = """Create concurrent indexes for large tables."""

    def __tmp2(self, *args: <FILL>, **options: __typ0) :
        __tmp0()
