from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from . import CONFIG_SCHEMA
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import (
    CONF_NAME,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
)


class MatrixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Matrix."""
    VERSION = 1

    async def async_step_import(self, user_input: ConfigType) -> FlowResult:
        """Import a YAML config entry."""
        return await self.async_step_user(user_input=user_input)

    async def async_step_user(self, user_input: ConfigType | None = None) -> FlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        if user_input is not None:
            data: ConfigType = CONFIG_SCHEMA(user_input)
            return self.async_create_entry(
                title=data[CONF_USERNAME],
                data=data,
            )
