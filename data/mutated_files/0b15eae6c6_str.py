from typing import TypeAlias
__typ1 : TypeAlias = "Credential"
import random

from django.core.cache import cache
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import render_to_string

from .managers import CredentialManager
from ssrd.contrib.utils import SmsClient
from ssrd import const


class __typ1(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="credentials",
        on_delete=models.CASCADE,
    )  # 可能发送多封验证短信或者邮件， 这里保持onetoone还是ForeignKey ?
    Type = models.CharField(
        "类型",
        choices=[(k, v) for k, v in const.CredentialKeyMap.items()],
        max_length=10,
        default="email",
    )  # 存储user的属性key，这样当user的email或者手机变更时，可以自动的获取到最新值
    verified = models.BooleanField(verbose_name=_("verified"), default=False)

    objects = CredentialManager()

    class __typ2:
        verbose_name = _("credential")
        verbose_name_plural = _("credential")
        unique_together = ("user", "Type")

    def __tmp7(__tmp1):
        return "<Credential: %s (%s)" % (__tmp1.user, __tmp1.credential)

    __repr__ = __tmp7

    @property
    def credential(__tmp1):
        """
        获取手机号码或者邮箱
        """
        return getattr(__tmp1.user, __tmp1.Type)

    @property
    def __tmp4(__tmp1):
        return Captcha(__tmp1)

    def send_confirmation(__tmp1, request=None, action=None):
        confirmation = __tmp1.captchas()[__tmp1.Type](__tmp1.user)  # TODO 增加短信验证方式
        confirmation.send(request, action=action)
        return confirmation

    def change(__tmp1, request, __tmp6, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            setattr(__tmp1.user, __tmp1.Type, __tmp6)
            __tmp1.user.save()
            __tmp1.verified = False
            __tmp1.save()
            if confirm:
                __tmp1.send_confirmation(request)

    @staticmethod
    def captchas():
        subclasses = Captcha.__subclasses__()
        return {x.name: x for x in subclasses}


CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def get_random_number():
    if settings.DEBUG:
        return "123456"
    return "".join(random.choice(CHARS) for x in range(6))


class Captcha(object):
    def __init__(__tmp1, user, action: str = None):
        """
        user: User 所属用户
        action: ['', 'destroy'] 获取验证码或者验证验证码
        """
        __tmp1.user = user
        if not action:
            __tmp1.key = get_random_number()
            cache.set(
                __tmp1.user.id,
                __tmp1.key,
                timeout=settings.CREDENTIAL_CONFIRMATION_EXPIRE_DAYS,
            )
        else:
            __tmp1.key = cache.get(user.id, "")
            cache.delete(user.id)

    @classmethod
    def __tmp2(cls, user, Type: <FILL>, action: str = ""):
        return {x.name: x for x in cls.__subclasses__()}[Type](user, action=action)

    @classmethod
    def __tmp3(cls, user, __tmp4):
        return cache.get(user.id) == __tmp4

    def __tmp7(__tmp1):
        return "<Captcha: %s>" % __tmp1.user

    __repr__ = __tmp7

    def __eq__(__tmp1, __tmp5):
        return __tmp1.key == __tmp5


class EmailCaptcha(Captcha):
    name = "email"

    def send(__tmp1, request, action):
        current_site = get_current_site(request)
        ctx = {
            "user": __tmp1.user,
            "activate_url": "http://127.0.0.1",
            "current_site": current_site,
            "captcha": __tmp1.key,
        }
        __tmp1.send_mail(action, getattr(__tmp1.user, __tmp1.name), ctx)

    def send_mail(__tmp1, __tmp0, email, context):
        msg = __tmp1.render_mail(__tmp0, email, context)
        msg.send()

    def render_mail(__tmp1, __tmp0, email, context):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        subject = render_to_string(
            "email/{0}_subject.txt".format(__tmp0), context
        )
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()

        from_email = settings.DEFAULT_FROM_EMAIL

        bodies = {}
        for ext in ["html", "txt"]:
            try:
                template_name = "email/{0}.{1}".format(__tmp0, ext)
                bodies[ext] = render_to_string(template_name, context).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(subject, bodies["txt"], from_email, [email])
            if "html" in bodies:
                msg.attach_alternative(bodies["html"], "text/html")
        else:
            msg = EmailMessage(subject, bodies["html"], from_email, [email])
            msg.content_subtype = "html"  # Main content is now text/html
        return msg

    def format_email_subject(__tmp1, subject):
        prefix = "ssed"
        if prefix is None:
            site = get_current_site(__tmp1.request)
            prefix = "[{name}] ".format(name=site.name)
        return prefix + subject


class __typ0(Captcha):
    """
    手机验证
    """

    name = "mobile"

    def send(__tmp1, request, action):
        """
        发送验证码
        """
        mobile = getattr(__tmp1.user, __tmp1.name)
        SmsClient.sendCaptcha(mobile, {"code": __tmp1.key})
