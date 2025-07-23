from typing import TypeAlias
__typ0 : TypeAlias = "HomeAssistantType"
"""
Helper to handle a set of topics to subscribe to.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/mqtt/
"""
import logging
from typing import Any, Callable, Dict, Optional

import attr

from homeassistant.components import mqtt
from homeassistant.components.mqtt import DEFAULT_QOS, MessageCallbackType
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.loader import bind_hass

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class EntitySubscription:
    """Class to hold data about an active entity topic subscription."""

    topic = attr.ib(type=str)
    message_callback = attr.ib(type=MessageCallbackType)
    unsubscribe_callback = attr.ib(type=Optional[Callable[[], None]])
    qos = attr.ib(type=int, default=0)
    encoding = attr.ib(type=str, default='utf-8')

    async def resubscribe_if_necessary(__tmp0, hass, __tmp3):
        """Re-subscribe to the new topic if necessary."""
        if not __tmp0._should_resubscribe(__tmp3):
            return

        if __tmp3 is not None and __tmp3.unsubscribe_callback is not None:
            __tmp3.unsubscribe_callback()

        if __tmp0.topic is None:
            # We were asked to remove the subscription or not to create it
            return

        __tmp0.unsubscribe_callback = await mqtt.async_subscribe(
            hass, __tmp0.topic, __tmp0.message_callback,
            __tmp0.qos, __tmp0.encoding
        )

    def _should_resubscribe(__tmp0, __tmp3):
        """Check if we should re-subscribe to the topic using the old state."""
        if __tmp3 is None:
            return True

        return (__tmp0.topic, __tmp0.qos, __tmp0.encoding) != \
            (__tmp3.topic, __tmp3.qos, __tmp3.encoding)


@bind_hass
async def __tmp4(hass: __typ0,
                                 __tmp2: Optional[Dict[str,
                                                          EntitySubscription]],
                                 __tmp6: Dict[str, Any]):
    """(Re)Subscribe to a set of MQTT topics.

    State is kept in sub_state and a dictionary mapping from the subscription
    key to the subscription state.

    Please note that the sub state must not be shared between multiple
    sets of topics. Every call to async_subscribe_topics must always
    contain _all_ the topics the subscription state should manage.
    """
    current_subscriptions = __tmp2 if __tmp2 is not None else {}
    __tmp2 = {}
    for key, value in __tmp6.items():
        # Extract the new requested subscription
        requested = EntitySubscription(
            topic=value.get('topic', None),
            message_callback=value.get('msg_callback', None),
            unsubscribe_callback=None,
            qos=value.get('qos', DEFAULT_QOS),
            encoding=value.get('encoding', 'utf-8'),
        )
        # Get the current subscription state
        current = current_subscriptions.pop(key, None)
        await requested.resubscribe_if_necessary(hass, current)
        __tmp2[key] = requested

    # Go through all remaining subscriptions and unsubscribe them
    for remaining in current_subscriptions.values():
        if remaining.unsubscribe_callback is not None:
            remaining.unsubscribe_callback()

    return __tmp2


@bind_hass
async def __tmp5(hass: __typ0, __tmp1: <FILL>):
    """Unsubscribe from all MQTT topics managed by async_subscribe_topics."""
    return await __tmp4(hass, __tmp1, {})
