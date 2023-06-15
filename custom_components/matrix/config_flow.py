"""Config Flow for matrix."""
from homeassistant import config_entries
from homeassistant.const import (
    CONF_USERNAME, CONF_BASE,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.typing import ConfigType

from . import CONFIG_SCHEMA, MatrixBot
from .const import DOMAIN


class MatrixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Matrix."""

    VERSION = 1

    async def async_step_import(self, user_input: ConfigType) -> FlowResult:
        """Import a YAML config entry."""
        return await self.async_step_user(user_input=user_input)

    async def async_step_user(self, user_input: ConfigType | None = None) -> FlowResult:
        """Handle a flow initiated by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        errors = {}
        if user_input is not None:
            try:
                config = await self.validate_input(user_input)
            except ConfigEntryAuthFailed:
                errors[CONF_BASE] = "auth_failed"
            else:
                return await self.async_step_finish(config)
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA[DOMAIN],
            errors=errors,
        )

    async def async_step_finish(self, config: ConfigType) -> FlowResult:
        mx_id = config[CONF_USERNAME]
        await self.async_set_unique_id(mx_id)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=mx_id,
            data=config,
        )

    async def validate_input(self, user_input: ConfigType) -> ConfigType:
        """
        Attempt to create a MatrixBot with the given user_input.
        Catch errors and format them appropriately.
        """
        user_input = CONFIG_SCHEMA(user_input)[DOMAIN]
        matrix_bot = MatrixBot(
            self.hass,
            "",
            **user_input,
            listening_rooms=[],
            commands=[],
        )
        await matrix_bot._login()
        await matrix_bot._client.close()
        return user_input

