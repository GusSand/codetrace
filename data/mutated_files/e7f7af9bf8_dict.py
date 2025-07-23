"""
Support for the TrackR platform.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.trackr/
"""
import logging

import voluptuous as vol

from homeassistant.components.device_tracker import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_utc_time_change
from homeassistant.util import slugify

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pytrackr==0.0.5']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_scanner(hass, config: <FILL>, see, discovery_info=None):
    """Validate the configuration and return a TrackR scanner."""
    TrackRDeviceScanner(hass, config, see)
    return True


class TrackRDeviceScanner:
    """A class representing a TrackR device."""

    def __tmp1(__tmp0, hass, config, see) :
        """Initialize the TrackR device scanner."""
        from pytrackr.api import trackrApiInterface
        __tmp0.hass = hass
        __tmp0.api = trackrApiInterface(
            config.get(CONF_USERNAME), config.get(CONF_PASSWORD))
        __tmp0.see = see
        __tmp0.devices = __tmp0.api.get_trackrs()
        __tmp0._update_info()

        track_utc_time_change(
            __tmp0.hass, __tmp0._update_info, second=range(0, 60, 30))

    def _update_info(__tmp0, now=None) :
        """Update the device info."""
        _LOGGER.debug("Updating devices %s", now)

        # Update self.devices to collect new devices added
        # to the users account.
        __tmp0.devices = __tmp0.api.get_trackrs()

        for trackr in __tmp0.devices:
            trackr.update_state()
            trackr_id = trackr.tracker_id()
            trackr_device_id = trackr.id()
            lost = trackr.lost()
            dev_id = slugify(trackr.name())
            if dev_id is None:
                dev_id = trackr_id
            location = trackr.last_known_location()
            lat = location['latitude']
            lon = location['longitude']

            attrs = {
                'last_updated': trackr.last_updated(),
                'last_seen': trackr.last_time_seen(),
                'trackr_id': trackr_id,
                'id': trackr_device_id,
                'lost': lost,
                'battery_level': trackr.battery_level()
            }

            __tmp0.see(
                dev_id=dev_id, gps=(lat, lon), attributes=attrs
            )
