from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
import datetime

from django.http import HttpRequest
from django.utils import timezone

from .models import HttpAccessLogModel


def __tmp1(__tmp0: <FILL>) :
    return __tmp0.META.get('HTTP_X_FORWARDED_FOR') or __tmp0.META.get('REMOTE_ADDR')


def __tmp2(__tmp0: HttpRequest, path, query_string: __typ0 = None, hours: __typ1 = 24, method='GET') -> __typ1:
    '''
    Returns a value that represents the count of requests from a IP address to a given path in given range of hours.

    The default value of hours is 24, which will look for all requests in 24 hours.

    Optional, query_string can be given to narrow down the counting range

    '''
    count: __typ1 = 0
    dt_from: datetime.datetime = timezone.now() - datetime.timedelta(hours=hours)
    IPv4 = __tmp1(__tmp0)

    records = HttpAccessLogModel.objects.filter(visitor_ipv4=IPv4
                                                ).filter(time_stamp__gte=dt_from
                                                         ).filter(request_path=path
                                                                  ).filter(request_method=method
                                                                           ).filter(status_code='200')

    if query_string:
        records.filter(request_query_string=query_string)

    count = records.count()

    return count
