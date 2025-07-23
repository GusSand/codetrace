from typing import TypeAlias
__typ0 : TypeAlias = "Any"

from argparse import ArgumentParser
from typing import Any

from django.conf import settings
from django.contrib.auth import get_backends
from django.core.management.base import BaseCommand
from django_auth_ldap.backend import LDAPBackend, _LDAPUser

# Quick tool to test whether you're correctly authenticating to LDAP
def query_ldap(**options) :
    email = options['email']
    for backend in get_backends():
        if isinstance(backend, LDAPBackend):
            ldap_attrs = _LDAPUser(backend, backend.django_to_ldap_username(email)).attrs
            if ldap_attrs is None:
                print("No such user found")
            else:
                for django_field, ldap_field in settings.AUTH_LDAP_USER_ATTR_MAP.items():
                    print("%s: %s" % (django_field, ldap_attrs[ldap_field]))
                if settings.LDAP_EMAIL_ATTR is not None:
                    print("%s: %s" % ('email', ldap_attrs[settings.LDAP_EMAIL_ATTR]))

class Command(BaseCommand):
    def add_arguments(__tmp0, parser: <FILL>) :
        parser.add_argument('email', metavar='<email>', type=str,
                            help="email of user to query")

    def handle(__tmp0, *args, **options) :
        query_ldap(**options)
