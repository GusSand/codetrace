from typing import TypeAlias
__typ1 : TypeAlias = "Post"
__typ0 : TypeAlias = "PostDataProvider"
import uuid
from buslane.events import EventBus
from dataclasses import dataclass

from meerkat.domain.post.data_providers import PostDataProvider
from meerkat.domain.post.entities import Post
from meerkat.domain.post.events import PostCreated
from meerkat.domain.post.value_objects import Title, Body, Id


@dataclass(frozen=True)
class AddNewPostCommand:
    title: str
    body: str


class AddNewPostUseCase:
    def __init__(__tmp0, data_provider, event_bus: <FILL>):
        __tmp0.data_provider = data_provider
        __tmp0.event_bus = event_bus

    def exec(__tmp0, command: AddNewPostCommand) :
        post = __typ1.create(Id(uuid.uuid4()), Title(command.title), Body(command.body))
        __tmp0.data_provider.save(post)
        __tmp0.event_bus.publish(PostCreated(post))
        return post
