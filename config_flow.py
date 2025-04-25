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
    DEFAULT_FIRMWARE,
    DEBUG,
    LOG_LEVELS,
    SENSOR_TYPES,
    CONF_SLAVE_ID,
    FIRMWARE_VERSION,
)

_LOGGER = logging.getLogger(__name__)

def get_sensor_options() -> dict[str, Any]:
    """Get sensor options from SENSOR_TYPES."""
    options = {}
    for sensor_key, sensor_info in SENSOR_TYPES.items():
        if "temperature" in sensor_key.lower():
            options[sensor_key] = f"{sensor_info['name']} (Register {sensor_info['address']})"
    return options

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Validate the user input allows us to connect."""
    # Hier können wir später eine Validierung hinzufügen
    pass

class LambdaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lambda WP."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is None:
            user_input = {}
        # Default-Werte aus bestehendem Eintrag holen, falls vorhanden
        current_entries = self._async_current_entries()
        existing_data = current_entries[0].data if current_entries else {}

        # Pflichtfelder prüfen
        required_fields = [CONF_NAME, CONF_HOST, CONF_PORT, CONF_SLAVE_ID]
        if not all(k in user_input and user_input[k] for k in required_fields):
            # Formular anzeigen, wenn Eingaben fehlen
            firmware_options = list(FIRMWARE_VERSION.keys())
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_NAME, default=user_input.get(CONF_NAME, existing_data.get(CONF_NAME, DEFAULT_NAME))): str,
                        vol.Required(CONF_HOST, default=user_input.get(CONF_HOST, existing_data.get(CONF_HOST, DEFAULT_HOST))): str,
                        vol.Required(CONF_PORT, default=user_input.get(CONF_PORT, existing_data.get(CONF_PORT, DEFAULT_PORT))): int,
                        vol.Required(CONF_SLAVE_ID, default=user_input.get(CONF_SLAVE_ID, existing_data.get(CONF_SLAVE_ID, DEFAULT_SLAVE_ID))): int,
                        vol.Required(
                            "num_hps",
                            default=user_input.get("num_hps", existing_data.get("num_hps", 1)),
                            description={"suggested_value": 1},
                        ): int,
                        vol.Required(
                            "num_boil",
                            default=user_input.get("num_boil", existing_data.get("num_boil", 1)),
                            description={"suggested_value": 1},
                        ): int,
                        vol.Required(
                            "num_hc",
                            default=user_input.get("num_hc", existing_data.get("num_hc", 1)),
                            description={"suggested_value": 1},
                        ): int,
                        vol.Optional(
                            "room_thermostat_control",
                            default=user_input.get("room_thermostat_control", existing_data.get("room_thermostat_control", False)),
                            description={
                                "suggested_value": False,
                                "description": "{room_thermostat_control_tooltip}"
                            }
                        ): bool,
                        vol.Optional(
                            "firmware_version",
                            default=user_input.get("firmware_version", existing_data.get("firmware_version", DEFAULT_FIRMWARE)),
                        ): vol.In(firmware_options),
                    }
                ),
                errors=errors,
                description_placeholders={
                    "room_thermostat_control_tooltip": "room_thermostat_control_tooltip"
                }
            )

        try:
            # Ergänze fehlende Pflichtfelder aus existing_data oder Default
            if CONF_NAME not in user_input or not user_input[CONF_NAME]:
                user_input[CONF_NAME] = existing_data.get(CONF_NAME, DEFAULT_NAME)
            await validate_input(self.hass, user_input)
            if CONF_NAME not in user_input or not user_input[CONF_NAME]:
                errors["base"] = "name_required"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

        firmware_options = list(FIRMWARE_VERSION.keys())

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=user_input.get(CONF_NAME, existing_data.get(CONF_NAME, DEFAULT_NAME))): str,
                    vol.Required(CONF_HOST, default=user_input.get(CONF_HOST, existing_data.get(CONF_HOST, DEFAULT_HOST))): str,
                    vol.Required(CONF_PORT, default=user_input.get(CONF_PORT, existing_data.get(CONF_PORT, DEFAULT_PORT))): int,
                    vol.Required(CONF_SLAVE_ID, default=user_input.get(CONF_SLAVE_ID, existing_data.get(CONF_SLAVE_ID, DEFAULT_SLAVE_ID))): int,
                    vol.Required(
                        "num_hps",
                        default=user_input.get("num_hps", existing_data.get("num_hps", 1)),
                        description={"suggested_value": 1},
                    ): int,
                    vol.Required(
                        "num_boil",
                        default=user_input.get("num_boil", existing_data.get("num_boil", 1)),
                        description={"suggested_value": 1},
                    ): int,
                    vol.Required(
                        "num_hc",
                        default=user_input.get("num_hc", existing_data.get("num_hc", 1)),
                        description={"suggested_value": 1},
                    ): int,
                    vol.Optional(
                        "room_thermostat_control",
                        default=user_input.get("room_thermostat_control", existing_data.get("room_thermostat_control", False)),
                        description={
                            "suggested_value": False,
                            "description": "{room_thermostat_control_tooltip}"
                        }
                    ): bool,
                    vol.Optional(
                        "firmware_version",
                        default=user_input.get("firmware_version", existing_data.get("firmware_version", DEFAULT_FIRMWARE)),
                    ): vol.In(firmware_options),
                }
            ),
            errors=errors,
            description_placeholders={
                "room_thermostat_control_tooltip": "room_thermostat_control_tooltip"
            }
        )

    @staticmethod
    @config_entries.callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return LambdaOptionsFlow()

class LambdaOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                update_data = False
                new_data = dict(self.config_entry.data)
                # Firmware-Version
                if "firmware_version" in user_input and user_input["firmware_version"] != self.config_entry.data.get("firmware_version"):
                    new_data["firmware_version"] = user_input["firmware_version"]
                    update_data = True
                # Room Thermostat Control
                if "room_thermostat_control" in user_input and user_input["room_thermostat_control"] != self.config_entry.data.get("room_thermostat_control", False):
                    new_data["room_thermostat_control"] = user_input["room_thermostat_control"]
                    update_data = True
                if update_data:
                    self.hass.config_entries.async_update_entry(
                        self.config_entry,
                        data=new_data
                    )
                # Entferne die Felder aus den Options, die in data gespeichert werden
                user_input = {k: v for k, v in user_input.items() if k not in ("firmware_version", "room_thermostat_control")}
                return self.async_create_entry(title="", data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception in options flow")
                errors["base"] = "unknown"

        options = self.config_entry.options
        firmware_options = list(FIRMWARE_VERSION.keys())

        schema = {
            vol.Optional(
                "hot_water_min_temp",
                default=options.get("hot_water_min_temp", 40),
            ): vol.All(vol.Coerce(float), vol.Range(min=20, max=80)),
            vol.Optional(
                "hot_water_max_temp",
                default=options.get("hot_water_max_temp", 60),
            ): vol.All(vol.Coerce(float), vol.Range(min=20, max=80)),
            vol.Optional(
                "heating_circuit_min_temp",
                default=options.get("heating_circuit_min_temp", 15),
            ): vol.All(vol.Coerce(float), vol.Range(min=5, max=35)),
            vol.Optional(
                "heating_circuit_max_temp",
                default=options.get("heating_circuit_max_temp", 35),
            ): vol.All(vol.Coerce(float), vol.Range(min=5, max=35)),
            vol.Optional(
                "update_interval",
                default=options.get("update_interval", 10),
            ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
            vol.Optional(
                "room_thermostat_control",
                default=options.get("room_thermostat_control", False),
                description={
                    "suggested_value": False,
                    "description": "{room_thermostat_control_tooltip}"
                }
            ): bool,
            vol.Optional(
                "firmware_version",
                default=self.config_entry.data.get("firmware_version", "V0.0.4-3K"),
            ): vol.In(firmware_options),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema),
            errors=errors,
            description_placeholders={
                "room_thermostat_control_tooltip": "room_thermostat_control_tooltip"
            },
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