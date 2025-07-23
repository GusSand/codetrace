from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def __tmp0(__tmp2, create: <FILL>, __tmp1: Sequence[Any], **kwargs):
        __tmp0 = Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(
            extra_kwargs={}
        )
        __tmp2.set_password(__tmp0)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
