from typing import TypeAlias
__typ1 : TypeAlias = "ConfigType"
__typ3 : TypeAlias = "bool"
"""
Support for ISY994 locks.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/lock.isy994/
"""
import logging
from typing import Callable  # noqa

from homeassistant.components.lock import LockDevice, DOMAIN
import homeassistant.components.isy994 as isy
from homeassistant.const import STATE_LOCKED, STATE_UNLOCKED, STATE_UNKNOWN
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

VALUE_TO_STATE = {
    0: STATE_UNLOCKED,
    100: STATE_LOCKED
}

UOM = ['11']
STATES = [STATE_LOCKED, STATE_UNLOCKED]


# pylint: disable=unused-argument
def setup_platform(__tmp0, config,
                   add_devices, discovery_info=None):
    """Set up the ISY994 lock platform."""
    if isy.ISY is None or not isy.ISY.connected:
        _LOGGER.error("A connection has not been made to the ISY controller")
        return False

    devices = []

    for node in isy.filter_nodes(isy.NODES, units=UOM,
                                 states=STATES):
        devices.append(__typ2(node))

    for program in isy.PROGRAMS.get(DOMAIN, []):
        try:
            status = program[isy.KEY_STATUS]
            actions = program[isy.KEY_ACTIONS]
            assert actions.dtype == 'program', 'Not a program'
        except (KeyError, AssertionError):
            pass
        else:
            devices.append(__typ0(program.name, status, actions))

    add_devices(devices)


class __typ2(isy.ISYDevice, LockDevice):
    """Representation of an ISY994 lock device."""

    def __init__(__tmp1, node) :
        """Initialize the ISY994 lock device."""
        isy.ISYDevice.__init__(__tmp1, node)
        __tmp1._conn = node.parent.parent.conn

    @property
    def is_locked(__tmp1) -> __typ3:
        """Get whether the lock is in locked state."""
        return __tmp1.state == STATE_LOCKED

    @property
    def state(__tmp1) :
        """Get the state of the lock."""
        if __tmp1.is_unknown():
            return None
        else:
            return VALUE_TO_STATE.get(__tmp1.value, STATE_UNKNOWN)

    def lock(__tmp1, **kwargs) -> None:
        """Send the lock command to the ISY994 device."""
        # Hack until PyISY is updated
        req_url = __tmp1._conn.compileURL(['nodes', __tmp1.unique_id, 'cmd',
                                         'SECMD', '1'])
        response = __tmp1._conn.request(req_url)

        if response is None:
            _LOGGER.error('Unable to lock device')

        __tmp1._node.update(0.5)

    def unlock(__tmp1, **kwargs) :
        """Send the unlock command to the ISY994 device."""
        # Hack until PyISY is updated
        req_url = __tmp1._conn.compileURL(['nodes', __tmp1.unique_id, 'cmd',
                                         'SECMD', '0'])
        response = __tmp1._conn.request(req_url)

        if response is None:
            _LOGGER.error('Unable to lock device')

        __tmp1._node.update(0.5)


class __typ0(__typ2):
    """Representation of a ISY lock program."""

    def __init__(__tmp1, name: <FILL>, node, actions) :
        """Initialize the lock."""
        __typ2.__init__(__tmp1, node)
        __tmp1._name = name
        __tmp1._actions = actions

    @property
    def is_locked(__tmp1) :
        """Return true if the device is locked."""
        return __typ3(__tmp1.value)

    @property
    def state(__tmp1) :
        """Return the state of the lock."""
        return STATE_LOCKED if __tmp1.is_locked else STATE_UNLOCKED

    def lock(__tmp1, **kwargs) :
        """Lock the device."""
        if not __tmp1._actions.runThen():
            _LOGGER.error("Unable to lock device")

    def unlock(__tmp1, **kwargs) :
        """Unlock the device."""
        if not __tmp1._actions.runElse():
            _LOGGER.error("Unable to unlock device")
