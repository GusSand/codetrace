from typing import TypeAlias
__typ0 : TypeAlias = "PostDataProvider"
from buslane.events import EventBus
from dataclasses import dataclass

from meerkat.domain.post.data_providers import PostDataProvider
from meerkat.domain.post.events import PostPublished
from meerkat.domain.post.value_objects import Id


@dataclass(frozen=True)
class PublishPostCommand:
    id: Id


class __typ1:
    def __init__(__tmp0, data_provider, event_bus: <FILL>):
        __tmp0.data_provider = data_provider
        __tmp0.event_bus = event_bus

    def exec(__tmp0, command: PublishPostCommand) -> None:
        post = __tmp0.data_provider.get(command.id)
        post.publish()
        __tmp0.data_provider.save(post)
        __tmp0.event_bus.publish(PostPublished(post))
