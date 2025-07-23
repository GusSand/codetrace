from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import re

def __tmp0(__tmp1: <FILL>) -> None:
    if __tmp1 is None or len(__tmp1) == 0:
        raise ValidationError(_("Domain can't be empty."))
    if '.' not in __tmp1:
        raise ValidationError(_("Domain must have at least one dot (.)"))
    if len(__tmp1) > 255:
        raise ValidationError(_("Domain is too long"))
    if __tmp1[0] == '.' or __tmp1[-1] == '.':
        raise ValidationError(_("Domain cannot start or end with a dot (.)"))
    for subdomain in __tmp1.split('.'):
        if not subdomain:
            raise ValidationError(_("Consecutive '.' are not allowed."))
        if subdomain[0] == '-' or subdomain[-1] == '-':
            raise ValidationError(_("Subdomains cannot start or end with a '-'."))
        if not re.match('^[a-z0-9-]*$', subdomain):
            raise ValidationError(_("Domain can only have letters, numbers, '.' and '-'s."))
