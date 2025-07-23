from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    @post_generation
    def __tmp1(__tmp2, __tmp3: <FILL>, __tmp0, **kwargs):
        __tmp1 = Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(
            extra_kwargs={}
        )
        __tmp2.set_password(__tmp1)

    class __typ0:
        model = get_user_model()
        django_get_or_create = ["username"]
