from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "ArgumentParser"
import datetime
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand
from django.utils.timezone import now as timezone_now

from zerver.models import Message, Realm, Stream, UserProfile, get_realm

class Command(BaseCommand):
    help = "Generate statistics on user activity."

    def __tmp3(__tmp0, __tmp4: __typ0) :
        __tmp4.add_argument('realms', metavar='<realm>', type=str, nargs='*',
                            help="realm to generate statistics for")

    def messages_sent_by(__tmp0, user, __tmp2: <FILL>) :
        start = timezone_now() - datetime.timedelta(days=(__tmp2 + 1)*7)
        end = timezone_now() - datetime.timedelta(days=__tmp2*7)
        return Message.objects.filter(sender=user, pub_date__gt=start, pub_date__lte=end).count()

    def __tmp1(__tmp0, *args, **options: Any) :
        if options['realms']:
            try:
                realms = [get_realm(string_id) for string_id in options['realms']]
            except Realm.DoesNotExist as e:
                print(e)
                exit(1)
        else:
            realms = Realm.objects.all()

        for realm in realms:
            print(realm.string_id)
            user_profiles = __typ1.objects.filter(realm=realm, is_active=True)
            print("%d users" % (len(user_profiles),))
            print("%d streams" % (len(Stream.objects.filter(realm=realm)),))

            for user_profile in user_profiles:
                print("%35s" % (user_profile.email,), end=' ')
                for __tmp2 in range(10):
                    print("%5d" % (__tmp0.messages_sent_by(user_profile, __tmp2)), end=' ')
                print("")
