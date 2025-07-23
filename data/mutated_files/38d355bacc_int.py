from typing import TypeAlias
__typ1 : TypeAlias = "Wechaty"
__typ0 : TypeAlias = "str"
from typing import Union
import pytest
from wechaty.wechaty import Wechaty  # noqa


@pytest.mark.asyncio
async def __tmp0(__tmp3) -> None:
    owner = await __tmp3.Room("fake_room").owner()
    await owner.ready()
    assert owner.contact_id == "wechaty_user"


@pytest.mark.asyncio
async def test_room_topic(__tmp3) :
    topic = await __tmp3.Room("fake_room").topic()
    assert topic == "fake_room"


@pytest.mark.parametrize(
    ("room_name", "res"), [("test", "test_room"), ("fake", "fake_room"), ("wechaty", None)]
)
@pytest.mark.asyncio
async def test_room_find(__tmp3, __tmp2, __tmp1) :
    room = await __tmp3.Room.find(__tmp2)
    name = room.room_id if room else None
    assert name == __tmp1


@pytest.mark.parametrize(
    ("room_name", "res"), [("test", 1), ("fake", 1), ("room", 2), ("wechaty", 0)]
)
@pytest.mark.asyncio
async def test_room_findall(__tmp3: __typ1, __tmp2: __typ0, __tmp1: <FILL>) -> None:
    room = await __tmp3.Room.find_all(__tmp2)
    assert len(room) == __tmp1
