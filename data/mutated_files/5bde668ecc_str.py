import datetime
from typing import Any, Dict, Optional, Tuple, Union

from django.db import models

from zerver.lib.timestamp import floor_to_day
from zerver.models import Realm, Recipient, Stream, UserProfile

class __typ6(models.Model):
    property = models.CharField(max_length=40, unique=True)  # type: str
    end_time = models.DateTimeField()  # type: datetime.datetime

    # Valid states are {DONE, STARTED}
    DONE = 1
    STARTED = 2
    state = models.PositiveSmallIntegerField()  # type: int

    last_modified = models.DateTimeField(auto_now=True)  # type: datetime.datetime

    def __tmp1(__tmp0) :
        return "<FillState: %s %s %s>" % (__tmp0.property, __tmp0.end_time, __tmp0.state)

# The earliest/starting end_time in FillState
# We assume there is at least one realm
def installation_epoch() -> datetime.datetime:
    earliest_realm_creation = Realm.objects.aggregate(models.Min('date_created'))['date_created__min']
    return floor_to_day(earliest_realm_creation)

def __tmp2(property: <FILL>) -> Optional[datetime.datetime]:
    fillstate = __typ6.objects.filter(property=property).first()
    if fillstate is None:
        return None
    if fillstate.state == __typ6.DONE:
        return fillstate.end_time
    return fillstate.end_time - datetime.timedelta(hours=1)

# would only ever make entries here by hand
class __typ5(models.Model):
    info = models.CharField(max_length=1000)  # type: str

    def __tmp1(__tmp0) -> str:
        return "<Anomaly: %s... %s>" % (__tmp0.info, __tmp0.id)

class __typ7(models.Model):
    # Note: When inheriting from BaseCount, you may want to rearrange
    # the order of the columns in the migration to make sure they
    # match how you'd like the table to be arranged.
    property = models.CharField(max_length=32)  # type: str
    subgroup = models.CharField(max_length=16, null=True)  # type: Optional[str]
    end_time = models.DateTimeField()  # type: datetime.datetime
    value = models.BigIntegerField()  # type: int
    anomaly = models.ForeignKey(__typ5, on_delete=models.SET_NULL, null=True)  # type: Optional[Anomaly]

    class __typ4:
        abstract = True

class __typ2(__typ7):

    class __typ4:
        unique_together = ("property", "subgroup", "end_time")

    def __tmp1(__tmp0) -> str:
        return "<InstallationCount: %s %s %s>" % (__tmp0.property, __tmp0.subgroup, __tmp0.value)

class __typ3(__typ7):
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)

    class __typ4:
        unique_together = ("realm", "property", "subgroup", "end_time")
        index_together = ["property", "end_time"]

    def __tmp1(__tmp0) -> str:
        return "<RealmCount: %s %s %s %s>" % (__tmp0.realm, __tmp0.property, __tmp0.subgroup, __tmp0.value)

class __typ0(__typ7):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)

    class __typ4:
        unique_together = ("user", "property", "subgroup", "end_time")
        # This index dramatically improves the performance of
        # aggregating from users to realms
        index_together = ["property", "realm", "end_time"]

    def __tmp1(__tmp0) -> str:
        return "<UserCount: %s %s %s %s>" % (__tmp0.user, __tmp0.property, __tmp0.subgroup, __tmp0.value)

class __typ1(__typ7):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    realm = models.ForeignKey(Realm, on_delete=models.CASCADE)

    class __typ4:
        unique_together = ("stream", "property", "subgroup", "end_time")
        # This index dramatically improves the performance of
        # aggregating from streams to realms
        index_together = ["property", "realm", "end_time"]

    def __tmp1(__tmp0) -> str:
        return "<StreamCount: %s %s %s %s %s>" % (
            __tmp0.stream, __tmp0.property, __tmp0.subgroup, __tmp0.value, __tmp0.id)
