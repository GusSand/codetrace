from typing import TypeAlias
__typ2 : TypeAlias = "HomeAssistant"
__typ1 : TypeAlias = "SetupFlow"
__typ0 : TypeAlias = "str"
__typ3 : TypeAlias = "bool"
"""Example auth module."""
import logging
from typing import Any, Dict

import voluptuous as vol

from homeassistant.core import HomeAssistant

from . import MultiFactorAuthModule, MULTI_FACTOR_AUTH_MODULES, \
    MULTI_FACTOR_AUTH_MODULE_SCHEMA, SetupFlow

CONFIG_SCHEMA = MULTI_FACTOR_AUTH_MODULE_SCHEMA.extend({
    vol.Required('data'): [vol.Schema({
        vol.Required('user_id'): __typ0,
        vol.Required('pin'): __typ0,
    })]
}, extra=vol.PREVENT_EXTRA)

_LOGGER = logging.getLogger(__name__)


@MULTI_FACTOR_AUTH_MODULES.register('insecure_example')
class InsecureExampleModule(MultiFactorAuthModule):
    """Example auth module validate pin."""

    DEFAULT_TITLE = 'Insecure Personal Identify Number'

    def __init__(__tmp1, __tmp8, __tmp7: Dict[__typ0, Any]) :
        """Initialize the user data store."""
        super().__init__(__tmp8, __tmp7)
        __tmp1._data = __tmp7['data']

    @property
    def __tmp6(__tmp1) -> vol.Schema:
        """Validate login flow input data."""
        return vol.Schema({'pin': __typ0})

    @property
    def setup_schema(__tmp1) :
        """Validate async_setup_user input data."""
        return vol.Schema({'pin': __typ0})

    async def __tmp11(__tmp1, __tmp9: __typ0) -> __typ1:
        """Return a data entry flow handler for setup module.

        Mfa module should extend SetupFlow
        """
        return __typ1(__tmp1, __tmp1.setup_schema, __tmp9)

    async def __tmp5(__tmp1, __tmp9: __typ0, __tmp3: <FILL>) -> Any:
        """Set up user to use mfa module."""
        # data shall has been validate in caller
        pin = __tmp3['pin']

        for data in __tmp1._data:
            if data['user_id'] == __tmp9:
                # already setup, override
                data['pin'] = pin
                return

        __tmp1._data.append({'user_id': __tmp9, 'pin': pin})

    async def __tmp0(__tmp1, __tmp9: __typ0) :
        """Remove user from mfa module."""
        found = None
        for data in __tmp1._data:
            if data['user_id'] == __tmp9:
                found = data
                break
        if found:
            __tmp1._data.remove(found)

    async def __tmp2(__tmp1, __tmp9) :
        """Return whether user is setup."""
        for data in __tmp1._data:
            if data['user_id'] == __tmp9:
                return True
        return False

    async def __tmp4(
            __tmp1, __tmp9: __typ0, __tmp10) :
        """Return True if validation passed."""
        for data in __tmp1._data:
            if data['user_id'] == __tmp9:
                # user_input has been validate in caller
                if data['pin'] == __tmp10['pin']:
                    return True

        return False
