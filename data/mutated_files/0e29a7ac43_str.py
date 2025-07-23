from typing import TypeAlias
__typ2 : TypeAlias = "Any"
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


class MultiFactorAuthModule:
    """Multi-factor Auth Module of validation function."""

    DEFAULT_TITLE = 'Unnamed auth module'
    MAX_RETRY_TIME = 3

    def __init__(__tmp0, hass: __typ1, config: Dict[str, __typ2]) -> None:
        """Initialize an auth module."""
        __tmp0.hass = hass
        __tmp0.config = config

    @property
    def id(__tmp0) :  # pylint: disable=invalid-name
        """Return id of the auth module.

        Default is same as type
        """
        return __tmp0.config.get(CONF_ID, __tmp0.type)

    @property
    def type(__tmp0) -> str:
        """Return type of the module."""
        return __tmp0.config[CONF_TYPE]  # type: ignore

    @property
    def name(__tmp0) :
        """Return the name of the auth module."""
        return __tmp0.config.get(CONF_NAME, __tmp0.DEFAULT_TITLE)

    # Implement by extending class

    @property
    def input_schema(__tmp0) :
        """Return a voluptuous schema to define mfa auth module's input."""
        raise NotImplementedError

    async def async_setup_flow(__tmp0, user_id: <FILL>) :
        """Return a data entry flow handler for setup module.

        Mfa module should extend SetupFlow
        """
        raise NotImplementedError

    async def async_setup_user(__tmp0, user_id: str, setup_data: __typ2) -> __typ2:
        """Set up user for mfa auth module."""
        raise NotImplementedError

    async def async_depose_user(__tmp0, user_id) -> None:
        """Remove user from mfa module."""
        raise NotImplementedError

    async def __tmp1(__tmp0, user_id) -> bool:
        """Return whether user is setup."""
        raise NotImplementedError

    async def async_validate(
            __tmp0, user_id: str, user_input: Dict[str, __typ2]) -> bool:
        """Return True if validation passed."""
        raise NotImplementedError


class __typ0(data_entry_flow.FlowHandler):
    """Handler for the setup flow."""

    def __init__(__tmp0, __tmp4: MultiFactorAuthModule,
                 setup_schema: vol.Schema,
                 user_id) :
        """Initialize the setup flow."""
        __tmp0._auth_module = __tmp4
        __tmp0._setup_schema = setup_schema
        __tmp0._user_id = user_id

    async def __tmp3(
            __tmp0, user_input: Optional[Dict[str, str]] = None) \
            :
        """Handle the first step of setup flow.

        Return self.async_show_form(step_id='init') if user_input is None.
        Return self.async_create_entry(data={'result': result}) if finish.
        """
        errors = {}  # type: Dict[str, str]

        if user_input:
            result = await __tmp0._auth_module.async_setup_user(
                __tmp0._user_id, user_input)
            return __tmp0.async_create_entry(
                title=__tmp0._auth_module.name,
                data={'result': result}
            )

        return __tmp0.async_show_form(
            step_id='init',
            data_schema=__tmp0._setup_schema,
            errors=errors
        )


async def __tmp2(
        hass: __typ1, config: Dict[str, __typ2]) \
        -> MultiFactorAuthModule:
    """Initialize an auth module from a config."""
    module_name = config[CONF_TYPE]
    module = await _load_mfa_module(hass, module_name)

    try:
        config = module.CONFIG_SCHEMA(config)  # type: ignore
    except vol.Invalid as err:
        _LOGGER.error('Invalid configuration for multi-factor module %s: %s',
                      module_name, humanize_error(config, err))
        raise

    return MULTI_FACTOR_AUTH_MODULES[module_name](hass, config)  # type: ignore


async def _load_mfa_module(hass: __typ1, module_name) \
        -> types.ModuleType:
    """Load an mfa auth module."""
    module_path = 'homeassistant.auth.mfa_modules.{}'.format(module_name)

    try:
        module = importlib.import_module(module_path)
    except ImportError as err:
        _LOGGER.error('Unable to load mfa module %s: %s', module_name, err)
        raise HomeAssistantError('Unable to load mfa module {}: {}'.format(
            module_name, err))

    if hass.config.skip_pip or not hasattr(module, 'REQUIREMENTS'):
        return module

    processed = hass.data.get(DATA_REQS)
    if processed and module_name in processed:
        return module

    processed = hass.data[DATA_REQS] = set()

    # https://github.com/python/mypy/issues/1424
    req_success = await requirements.async_process_requirements(
        hass, module_path, module.REQUIREMENTS)    # type: ignore

    if not req_success:
        raise HomeAssistantError(
            'Unable to process requirements of mfa module {}'.format(
                module_name))

    processed.add(module_name)
    return module
