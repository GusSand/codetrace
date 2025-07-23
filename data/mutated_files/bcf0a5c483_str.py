from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "HomeAssistant"
"""Plugable auth modules for Home Assistant."""
import importlib
import logging
import types
from typing import Any, Dict, Optional

import voluptuous as vol
from voluptuous.humanize import humanize_error

from homeassistant import requirements, data_entry_flow
from homeassistant.const import CONF_ID, CONF_NAME, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util.decorator import Registry

MULTI_FACTOR_AUTH_MODULES = Registry()

MULTI_FACTOR_AUTH_MODULE_SCHEMA = vol.Schema({
    vol.Required(CONF_TYPE): str,
    vol.Optional(CONF_NAME): str,
    # Specify ID if you have two mfa auth module for same type.
    vol.Optional(CONF_ID): str,
}, extra=vol.ALLOW_EXTRA)

DATA_REQS = 'mfa_auth_module_reqs_processed'

_LOGGER = logging.getLogger(__name__)


class __typ4:
    """Multi-factor Auth Module of validation function."""

    DEFAULT_TITLE = 'Unnamed auth module'
    MAX_RETRY_TIME = 3

    def __tmp9(__tmp1, hass, config: Dict[str, __typ3]) -> None:
        """Initialize an auth module."""
        __tmp1.hass = hass
        __tmp1.config = config

    @property
    def id(__tmp1) :  # pylint: disable=invalid-name
        """Return id of the auth module.

        Default is same as type
        """
        return __tmp1.config.get(CONF_ID, __tmp1.type)

    @property
    def type(__tmp1) -> str:
        """Return type of the module."""
        return __tmp1.config[CONF_TYPE]  # type: ignore

    @property
    def name(__tmp1) -> str:
        """Return the name of the auth module."""
        return __tmp1.config.get(CONF_NAME, __tmp1.DEFAULT_TITLE)

    # Implement by extending class

    @property
    def __tmp10(__tmp1) -> vol.Schema:
        """Return a voluptuous schema to define mfa auth module's input."""
        raise NotImplementedError

    async def __tmp15(__tmp1, __tmp13) -> 'SetupFlow':
        """Return a data entry flow handler for setup module.

        Mfa module should extend SetupFlow
        """
        raise NotImplementedError

    async def async_setup_user(__tmp1, __tmp13: str, __tmp7: __typ3) -> __typ3:
        """Set up user for mfa auth module."""
        raise NotImplementedError

    async def __tmp0(__tmp1, __tmp13) -> None:
        """Remove user from mfa module."""
        raise NotImplementedError

    async def __tmp2(__tmp1, __tmp13: <FILL>) -> __typ2:
        """Return whether user is setup."""
        raise NotImplementedError

    async def __tmp5(
            __tmp1, __tmp13, __tmp14: Dict[str, __typ3]) -> __typ2:
        """Return True if validation passed."""
        raise NotImplementedError


class __typ0(data_entry_flow.FlowHandler):
    """Handler for the setup flow."""

    def __tmp9(__tmp1, __tmp4,
                 __tmp3: vol.Schema,
                 __tmp13: str) :
        """Initialize the setup flow."""
        __tmp1._auth_module = __tmp4
        __tmp1._setup_schema = __tmp3
        __tmp1._user_id = __tmp13

    async def __tmp11(
            __tmp1, __tmp14: Optional[Dict[str, str]] = None) \
            -> Dict[str, __typ3]:
        """Handle the first step of setup flow.

        Return self.async_show_form(step_id='init') if user_input is None.
        Return self.async_create_entry(data={'result': result}) if finish.
        """
        errors = {}  # type: Dict[str, str]

        if __tmp14:
            result = await __tmp1._auth_module.async_setup_user(
                __tmp1._user_id, __tmp14)
            return __tmp1.async_create_entry(
                title=__tmp1._auth_module.name,
                data={'result': result}
            )

        return __tmp1.async_show_form(
            step_id='init',
            data_schema=__tmp1._setup_schema,
            errors=errors
        )


async def __tmp6(
        hass, config: Dict[str, __typ3]) \
        :
    """Initialize an auth module from a config."""
    __tmp8 = config[CONF_TYPE]
    module = await __tmp12(hass, __tmp8)

    try:
        config = module.CONFIG_SCHEMA(config)  # type: ignore
    except vol.Invalid as err:
        _LOGGER.error('Invalid configuration for multi-factor module %s: %s',
                      __tmp8, humanize_error(config, err))
        raise

    return MULTI_FACTOR_AUTH_MODULES[__tmp8](hass, config)  # type: ignore


async def __tmp12(hass: __typ1, __tmp8) \
        :
    """Load an mfa auth module."""
    module_path = 'homeassistant.auth.mfa_modules.{}'.format(__tmp8)

    try:
        module = importlib.import_module(module_path)
    except ImportError as err:
        _LOGGER.error('Unable to load mfa module %s: %s', __tmp8, err)
        raise HomeAssistantError('Unable to load mfa module {}: {}'.format(
            __tmp8, err))

    if hass.config.skip_pip or not hasattr(module, 'REQUIREMENTS'):
        return module

    processed = hass.data.get(DATA_REQS)
    if processed and __tmp8 in processed:
        return module

    processed = hass.data[DATA_REQS] = set()

    # https://github.com/python/mypy/issues/1424
    req_success = await requirements.async_process_requirements(
        hass, module_path, module.REQUIREMENTS)    # type: ignore

    if not req_success:
        raise HomeAssistantError(
            'Unable to process requirements of mfa module {}'.format(
                __tmp8))

    processed.add(__tmp8)
    return module
