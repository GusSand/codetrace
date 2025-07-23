from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"

from typing import Any, Callable, Dict, List, Set

from django.db import connection

from zerver.lib.management import ZulipBaseCommand

def __tmp3(__tmp1: str, table_name: <FILL>,
                              __tmp2: str, __tmp5: str) -> None:
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
        cursor.execute(sql, [__tmp1])
        rows = cursor.fetchall()
        if len(rows) > 0:
            print('Index %s already exists.' % (__tmp1,))
            return

        print("Creating index %s." % (__tmp1,))
        sql = '''
            CREATE INDEX CONCURRENTLY
            %s
            ON %s (%s)
            %s;
            ''' % (__tmp1, table_name, __tmp2, __tmp5)
        cursor.execute(sql)
        print('Finished creating %s.' % (__tmp1,))


def __tmp4() -> None:

    # copied from 0082
    __tmp3(
        __tmp1='zerver_usermessage_starred_message_id',
        table_name='zerver_usermessage',
        __tmp2='user_profile_id, message_id',
        __tmp5='WHERE (flags & 2) != 0',
    )

    # copied from 0083
    __tmp3(
        __tmp1='zerver_usermessage_mentioned_message_id',
        table_name='zerver_usermessage',
        __tmp2='user_profile_id, message_id',
        __tmp5='WHERE (flags & 8) != 0',
    )

    # copied from 0095
    __tmp3(
        __tmp1='zerver_usermessage_unread_message_id',
        table_name='zerver_usermessage',
        __tmp2='user_profile_id, message_id',
        __tmp5='WHERE (flags & 1) = 0',
    )

    # copied from 0098
    __tmp3(
        __tmp1='zerver_usermessage_has_alert_word_message_id',
        table_name='zerver_usermessage',
        __tmp2='user_profile_id, message_id',
        __tmp5='WHERE (flags & 512) != 0',
    )

    # copied from 0099
    __tmp3(
        __tmp1='zerver_usermessage_wildcard_mentioned_message_id',
        table_name='zerver_usermessage',
        __tmp2='user_profile_id, message_id',
        __tmp5='WHERE (flags & 8) != 0 OR (flags & 16) != 0',
    )

    # copied from 0177
    __tmp3(
        __tmp1='zerver_usermessage_is_private_message_id',
        table_name='zerver_usermessage',
        __tmp2='user_profile_id, message_id',
        __tmp5='WHERE (flags & 2048) != 0',
    )

    # copied from 0180
    __tmp3(
        __tmp1='zerver_usermessage_active_mobile_push_notification_id',
        table_name='zerver_usermessage',
        __tmp2='user_profile_id, message_id',
        __tmp5='WHERE (flags & 4096) != 0',
    )

class __typ0(ZulipBaseCommand):
    help = """Create concurrent indexes for large tables."""

    def __tmp0(self, *args: __typ1, **options: str) -> None:
        __tmp4()
