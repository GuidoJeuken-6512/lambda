"""Config flow for Lambda WP integration."""
from __future__ import annotations
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
    DEFAULT_HOST,
    DEBUG,
    LOG_LEVELS
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host", default=DEFAULT_HOST): str,
        vol.Required("port", default=DEFAULT_PORT): int,
        vol.Required("slave_id", default=DEFAULT_SLAVE_ID): int,
        vol.Optional("name", default=DEFAULT_NAME): str,
        vol.Optional("debug", default=False): bool,
    }
)

class LambdaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lambda WP."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            # Validate the connection
            await self._test_connection(user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

        if not errors:
            # Set debug logging if enabled
            if user_input.get("debug", False):
                logging.getLogger(DOMAIN).setLevel(logging.DEBUG)
                _LOGGER.info("Debug logging enabled for Lambda WP integration")

            return self.async_create_entry(
                title=user_input["name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def _test_connection(self, user_input: dict[str, Any]) -> None:
        """Test the connection to the Lambda device."""
        from pymodbus.client import ModbusTcpClient
        from pymodbus.exceptions import ModbusException

        client = ModbusTcpClient(user_input["host"], port=user_input["port"])
        try:
            if not await self.hass.async_add_executor_job(client.connect):
                raise CannotConnect
            # Test read a register
            result = await self.hass.async_add_executor_job(
                client.read_holding_registers,
                1004,  # Example register
                1,
                user_input["slave_id"],
            )
            if result.isError():
                raise CannotConnect
        except ModbusException as ex:
            _LOGGER.error("Modbus connection test failed: %s", ex)
            raise CannotConnect from ex
        finally:
            await self.hass.async_add_executor_job(client.close)

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""