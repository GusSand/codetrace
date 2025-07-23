from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
import datetime

from django.http import HttpRequest
from django.utils import timezone

from .models import HttpAccessLogModel


def __tmp2(__tmp1) :
    return __tmp1.META.get('HTTP_X_FORWARDED_FOR') or __tmp1.META.get('REMOTE_ADDR')


def __tmp3(__tmp1, __tmp0: <FILL>, query_string: str = None, hours: int = 24, method='GET') :
    '''
    Returns a value that represents the count of requests from a IP address to a given path in given range of hours.

    The default value of hours is 24, which will look for all requests in 24 hours.

    Optional, query_string can be given to narrow down the counting range

    '''
    count: int = 0
    dt_from: datetime.datetime = timezone.now() - datetime.timedelta(hours=hours)
    IPv4 = __tmp2(__tmp1)

    records = HttpAccessLogModel.objects.filter(visitor_ipv4=IPv4
                                                ).filter(time_stamp__gte=dt_from
                                                         ).filter(request_path=__tmp0
                                                                  ).filter(request_method=method
                                                                           ).filter(status_code='200')

    if query_string:
        records.filter(request_query_string=query_string)

    count = records.count()

    return count
