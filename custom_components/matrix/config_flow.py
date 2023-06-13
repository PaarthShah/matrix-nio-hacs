"""Config Flow for matrix."""
from homeassistant import config_entries
from homeassistant.const import (
    CONF_USERNAME,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.typing import ConfigType

from . import CONFIG_SCHEMA
from .const import DOMAIN


class MatrixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Matrix."""

    VERSION = 1

    async def async_step_import(self, user_input: ConfigType) -> FlowResult:
        """Import a YAML config entry."""
        return await self.async_step_user(user_input=user_input)

    async def async_step_user(self, user_input: ConfigType | None = None) -> FlowResult:
        """User Interaction Step."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        if user_input is not None:
            assert CONFIG_SCHEMA(user_input)[DOMAIN]
            return self.async_create_entry(
                title=user_input[DOMAIN][CONF_USERNAME],
                data=user_input[DOMAIN],
            )
