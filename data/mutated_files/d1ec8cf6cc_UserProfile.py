from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "HttpRequest"
__typ0 : TypeAlias = "str"
# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpRequest
import re
from typing import Optional

from zerver.models import get_realm, Realm, UserProfile

def __tmp5(__tmp2) -> __typ0:

    # The HTTP spec allows, but doesn't require, a client to omit the
    # port in the `Host` header if it's "the default port for the
    # service requested", i.e. typically either 443 or 80; and
    # whatever Django gets there, or from proxies reporting that via
    # X-Forwarded-Host, it passes right through the same way.  So our
    # logic is a bit complicated to allow for that variation.
    #
    # For both EXTERNAL_HOST and REALM_HOSTS, we take a missing port
    # to mean that any port should be accepted in Host.  It's not
    # totally clear that's the right behavior, but it keeps
    # compatibility with older versions of Zulip, so that's a start.

    host = __tmp2.get_host().lower()

    m = re.search(r'\.%s(:\d+)?$' % (settings.EXTERNAL_HOST,),
                  host)
    if m:
        subdomain = host[:m.start()]
        if subdomain in settings.ROOT_SUBDOMAIN_ALIASES:
            return Realm.SUBDOMAIN_FOR_ROOT_DOMAIN
        return subdomain

    for subdomain, realm_host in settings.REALM_HOSTS.items():
        if re.search(r'^%s(:\d+)?$' % (realm_host,),
                     host):
            return subdomain

    return Realm.SUBDOMAIN_FOR_ROOT_DOMAIN

def __tmp1(__tmp2) :
    return __tmp5(__tmp2) == Realm.SUBDOMAIN_FOR_ROOT_DOMAIN

def __tmp3(__tmp6, __tmp0: <FILL>) :
    if __tmp6 is None:
        return True  # nocoverage # This state may no longer be possible.
    return __tmp0.realm.subdomain == __tmp6

def __tmp4() :
    if settings.ROOT_DOMAIN_LANDING_PAGE:
        return False
    return get_realm(Realm.SUBDOMAIN_FOR_ROOT_DOMAIN) is None
