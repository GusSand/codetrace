import pytest

from apfelschuss.users.models import User

pytestmark = pytest.mark.django_db


def __tmp0(user: <FILL>):
    assert user.get_absolute_url() == f"/users/{user.username}/"
