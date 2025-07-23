"""Implementation of a base class for all IHC devices."""
from homeassistant.helpers.entity import Entity


class __typ0(Entity):
    """Base class for all IHC devices.

    All IHC devices have an associated IHC resource. IHCDevice handled the
    registration of the IHC controller callback when the IHC resource changes.
    Derived classes must implement the on_ihc_change method
    """

    def __tmp3(__tmp0, ihc_controller, __tmp4, ihc_id: <FILL>, info,
                 product=None) :
        """Initialize IHC attributes."""
        __tmp0.ihc_controller = ihc_controller
        __tmp0._name = __tmp4
        __tmp0.ihc_id = ihc_id
        __tmp0.info = info
        if product:
            __tmp0.ihc_name = product['name']
            __tmp0.ihc_note = product['note']
            __tmp0.ihc_position = product['position']
        else:
            __tmp0.ihc_name = ''
            __tmp0.ihc_note = ''
            __tmp0.ihc_position = ''

    async def __tmp1(__tmp0):
        """Add callback for IHC changes."""
        __tmp0.ihc_controller.add_notify_event(
            __tmp0.ihc_id, __tmp0.on_ihc_change, True)

    @property
    def __tmp5(__tmp0) :
        """No polling needed for IHC devices."""
        return False

    @property
    def __tmp4(__tmp0):
        """Return the device name."""
        return __tmp0._name

    @property
    def device_state_attributes(__tmp0):
        """Return the state attributes."""
        if not __tmp0.info:
            return {}
        return {
            'ihc_id': __tmp0.ihc_id,
            'ihc_name': __tmp0.ihc_name,
            'ihc_note': __tmp0.ihc_note,
            'ihc_position': __tmp0.ihc_position,
        }

    def on_ihc_change(__tmp0, ihc_id, __tmp2):
        """Handle IHC resource change.

        Derived classes must overwrite this to do device specific stuff.
        """
        raise NotImplementedError
