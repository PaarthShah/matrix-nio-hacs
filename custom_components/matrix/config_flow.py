"""Config Flow for matrix."""
from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_USERNAME, CONF_BASE, CONF_NAME,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.typing import ConfigType

from . import CONFIG_SCHEMA, MatrixBot, ConfigCommand, CONF_COMMANDS, CONF_ROOMS
from .const import DOMAIN


class MatrixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Matrix."""

    VERSION = 1

    @staticmethod
    @callback
    async def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

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


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Matrix integration options flow."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """
        Gather information from the current config entry.
        self._options can contain:
        - CONF_ROOMS: [str]
        - CONF_COMMANDS: [dict[str, str | list[str]]
        """
        self._options: dict[str, str] = dict(config_entry.options)
        self._commands: dict[str, ConfigCommand] = {}

        """
        config_entry.options.get(CONF_COMMANDS, []) can return:
        [
            {
                CONF_WORD: str,
                CONF_EXPRESSION: str,
                CONF_NAME: str,
                CONF_ROOMS: [str],
            },
            ...
        ]
        """
        for command in config_entry.options.get(CONF_COMMANDS, []):
            self._commands[command[CONF_NAME]] = command

        # Used in self.async_step_add_remove_command to store the command name that is currently being handled.
        self.__current_command_name: str | None = None

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """
        Manage the options.
        Some possible procedures:
        - Main step -> (User: Do nothing and submit) -> End
        - Main step -> (User: Change CONF_ROOMS) -> <ROOMS_SCHEMA check passes> -> [Update CONF_ROOMS] -> [Save new options] -> End
                                                 -> <ROOMS_SCHEMA check fails>  -> Main step with error information -> ...
        - Main step -> (User: Choose an option in the list) -> Command step -> (User: Add/modify a command) -> <COMMAND_SCHEMA check passes> -> [Update self._commands] -> Main step
                                                                                                               <COMMAND_SCHEMA check fails>  -> Command step with error information -> ...
        - Main step -> (User: Change CONF_ROOMS and choose an option in the list) -> <ROOMS_SCHEMA check passes> -> Command step -> ...
                                                                                     <ROOMS_SCHEMA check fails>  -> Main step with error information -> ...
        """

        if user_input is not None:
            # CONF_ROOMS: convert str to list because voluptuous_serialize does not support List type
            user_input[CONF_ROOMS] = (
                user_input[CONF_ROOMS].split(",") if user_input[CONF_ROOMS] else []
            )

            # Check the format of CONF_ROOMS if it's not empty
            if user_input[CONF_ROOMS]:
                ROOMS_SCHEMA(user_input[CONF_ROOMS])

            # Update CONF_ROOMS
            self._options[CONF_ROOMS] = user_input[CONF_ROOMS]

            if user_input[CONF_COMMANDS] == OPTION_LIST_COMMAND:
                # Update CONF_COMMANDS
                self._options[CONF_COMMANDS] = list(self._commands.values())
                # Call async_create_entry and exit
                return self.async_create_entry(title="", data=self._options)
            elif user_input[CONF_COMMANDS] == OPTION_ADD_COMMAND:
                # Add a new command
                return await self.async_step_add_command(user_input=None)
            elif user_input[CONF_COMMANDS] in self._commands:
                # Modify/Delete an existing command
                return await self.async_step_modify_command(
                    user_input=self._commands[user_input[CONF_COMMANDS]]
                )

        return self._show_main_form()

    async def async_step_add_command(
        self, user_input: dict[str, Any] | None, is_add: bool = False
    ) -> FlowResult:
        """Add commands step."""
        return self._show_add_remove_command_form(user_input=user_input, is_add=True)

    async def async_step_modify_command(
        self, user_input: dict[str, Any] | None, is_add: bool = False
    ) -> FlowResult:
        """Modify/Delete commands step."""
        return self._show_add_remove_command_form(user_input=user_input, is_add=False)

    @callback
    def _show_main_form(self, errors: dict[str, str] | None = None) -> FlowResult:
        """Handle the main options."""

        options_schema: vol.Schema = vol.Schema(
            {
                vol.Optional(
                    CONF_ROOMS,
                    default=",".join(self._options.get(CONF_ROOMS, [])),
                ): str,  # Multiple rooms are split by commas
            }
        )

        # Add existing commands to the combobox
        option_commands: dict[str, str] = {}
        option_commands[OPTION_LIST_COMMAND] = "--Commands--"
        option_commands[OPTION_ADD_COMMAND] = "Add command..."

        # Propagate the combobox
        for command in self._commands.values():
            name: str = command[CONF_NAME]
            word_or_expression: str | None = command.get(CONF_WORD) or command.get(
                CONF_EXPRESSION
            )
            option_commands[name] = f"{name} ({word_or_expression})"

        config_schema: vol.Schema = options_schema.extend(
            {
                vol.Optional(CONF_COMMANDS, default=OPTION_LIST_COMMAND): vol.In(
                    option_commands
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=config_schema,
            errors=errors,
        )

    @callback
    def _show_add_remove_command_form(
        self, user_input: dict[str, Any] | None, is_add: bool = False
    ) -> FlowResult:
        """
        Add/remove commands step.
        user_input can contain:
        - CONF_NAME: str
        - CONF_WORD: str
        - CONF_EXPRESSION: str
        - CONF_ROOMS: list[str]
        - OPTION_DELETE_COMMAND: bool
        """

        errors: dict[str, str] = {}

        if user_input is None:
            user_input = {}
        else:
            # When entering the step from the main step, the type of user_input[CONF_ROOMS] is list.
            if isinstance(user_input[CONF_ROOMS], str):
                # CONF_ROOMS: convert str to list because voluptuous_serialize does not support List type
                user_input[CONF_ROOMS] = (
                    user_input[CONF_ROOMS].split(",") if user_input[CONF_ROOMS] else []
                )

            try:
                # Check the format of user input
                COMMAND_SCHEMA(user_input)

                if user_input[CONF_NAME] in [*self._commands]:
                    if is_add:
                        # Duplicate name when adding a new command
                        raise DuplicateNameError
                    elif self.__current_command_name is None:
                        # Raise the exception to set self.__current_command_name
                        raise CurrentCommandNameEmpty
                    else:
                        # Duplicate name when modifying the name of an existing command
                        raise DuplicateNameError

            except CurrentCommandNameEmpty:
                # Store the command name that is currently being handled
                self.__current_command_name = user_input[CONF_NAME]
                # Delete the existing command in the temporary list because we will add it back after this step is finished
                del self._commands[str(self.__current_command_name)]

            except DuplicateNameError:
                errors[CONF_NAME] = "duplicate_name"

            else:
                # Store the command in the list (the config will be updated after the user submits the form in the main step)
                if not user_input.get(OPTION_DELETE_COMMAND):
                    self._commands[user_input[CONF_NAME]] = user_input
                # Reset the command name that is currently being handled
                self.__current_command_name = None
                # Return to the main step when a command is created/modified successfully
                return self._show_main_form()

        # When the user is modifying an existing command or any error occurs in this step,
        # user_input will not be None.
        option_schema: vol.Schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=user_input.get(CONF_NAME, "")): str,
                vol.Optional(CONF_WORD, default=user_input.get(CONF_WORD, "")): str,
                vol.Optional(
                    CONF_EXPRESSION, default=user_input.get(CONF_EXPRESSION, "")
                ): str,
                vol.Optional(
                    CONF_ROOMS, default=",".join(user_input.get(CONF_ROOMS, []))
                ): str,  # Multiple rooms are split by commas
            }
        )

        if not is_add:
            # Provide an option to delete the existing command
            option_schema = option_schema.extend(
                {
                    vol.Optional(OPTION_DELETE_COMMAND, default=False): bool,
                }
            )

        return self.async_show_form(
            step_id="add_command" if is_add else "modify_command",
            data_schema=option_schema,
            errors=errors,
        )

