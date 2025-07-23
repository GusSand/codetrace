import datetime

from django.db import models

from zerver.models import AbstractPushDeviceToken

def __tmp0(uuid: <FILL>) :
    return RemoteZulipServer.objects.get(uuid=uuid)

class RemoteZulipServer(models.Model):
    UUID_LENGTH = 36
    API_KEY_LENGTH = 64
    HOSTNAME_MAX_LENGTH = 128

    uuid = models.CharField(max_length=UUID_LENGTH, unique=True)  # type: str
    api_key = models.CharField(max_length=API_KEY_LENGTH)  # type: str

    hostname = models.CharField(max_length=HOSTNAME_MAX_LENGTH)  # type: str
    contact_email = models.EmailField(blank=True, null=False)  # type: str
    last_updated = models.DateTimeField('last updated', auto_now=True)  # type: datetime.datetime

    def __tmp2(__tmp1) :
        return "<RemoteZulipServer %s %s>" % (__tmp1.hostname, __tmp1.uuid[0:12])

# Variant of PushDeviceToken for a remote server.
class RemotePushDeviceToken(AbstractPushDeviceToken):
    server = models.ForeignKey(RemoteZulipServer, on_delete=models.CASCADE)  # type: RemoteZulipServer
    # The user id on the remote server for this device device this is
    user_id = models.BigIntegerField(db_index=True)  # type: int
    token = models.CharField(max_length=4096, db_index=True)  # type: bytes

    class Meta:
        unique_together = ("server", "user_id", "kind", "token")

    def __tmp2(__tmp1) :
        return "<RemotePushDeviceToken %s %s>" % (__tmp1.server, __tmp1.user_id)
