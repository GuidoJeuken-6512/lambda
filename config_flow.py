"""Config flow for Lambda WP integration."""
from __future__ import annotations
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig
from homeassistant.components.sensor import SensorDeviceClass

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
    DEFAULT_HOST,
    DEFAULT_FIRMWARE,
    DEFAULT_ROOM_THERMOSTAT_CONTROL,
    DEBUG,
    LOG_LEVELS,
    SENSOR_TYPES,
    CONF_SLAVE_ID,
    FIRMWARE_VERSION,
    CONF_ROOM_TEMPERATURE_ENTITY,
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
    
    def __init__(self) -> None:
        """Initialize the config flow."""
        self._data = {}
        self._options = {}

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
                            "firmware_version",
                            default=user_input.get("firmware_version", existing_data.get("firmware_version", DEFAULT_FIRMWARE)),
                        ): vol.In(firmware_options),
                    }
                ),
                errors=errors
            )

        try:
            # Ergänze fehlende Pflichtfelder aus existing_data oder Default
            if CONF_NAME not in user_input or not user_input[CONF_NAME]:
                user_input[CONF_NAME] = existing_data.get(CONF_NAME, DEFAULT_NAME)
            await validate_input(self.hass, user_input)
            if CONF_NAME not in user_input or not user_input[CONF_NAME]:
                errors["base"] = "name_required"
            else:
                # Speichere die Daten für den nächsten Schritt
                self._data = dict(user_input)
                self._options = {}
                
                # Prüfen, ob room_thermostat_control aktiviert wurde
                if user_input.get("room_thermostat_control", False):
                    # Move room_thermostat_control to options
                    self._options["room_thermostat_control"] = self._data.pop("room_thermostat_control", False)
                    # Wenn aktiviert, gehe zum Schritt für die Sensorauswahl
                    return await self.async_step_room_sensor()
                
                # Wenn nicht aktiviert, erstelle den Eintrag direkt
                # Move room_thermostat_control to options
                if "room_thermostat_control" in self._data:
                    self._options["room_thermostat_control"] = self._data.pop("room_thermostat_control", False)
                
                return self.async_create_entry(
                    title=self._data[CONF_NAME],
                    data=self._data,
                    options=self._options
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
                        "firmware_version",
                        default=user_input.get("firmware_version", existing_data.get("firmware_version", DEFAULT_FIRMWARE)),
                    ): vol.In(firmware_options),
                }
            ),
            errors=errors
        )

    async def async_step_room_sensor(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the room sensor selection step."""
        errors: dict[str, str] = {}
        
        # Anzahl der Heizkreise aus der Konfiguration holen
        num_hc = self.config_entry.data.get("num_hc", 1)
        
        if user_input is not None:
            try:
                # Speichere die ausgewählten Entitäten in den Optionen
                for hc_idx in range(1, num_hc + 1):
                    entity_key = CONF_ROOM_TEMPERATURE_ENTITY.format(hc_idx)
                    # Nur speichern, wenn eine Auswahl getroffen wurde
                    if entity_key in user_input and user_input[entity_key]:
                        self.options[entity_key] = user_input[entity_key]
                    # Wenn keine Auswahl getroffen wurde, entferne die Option falls vorhanden
                    elif entity_key in self.options:
                        del self.options[entity_key]
                
                # Erstelle den Config Entry mit den gesammelten Daten
                return self.async_create_entry(title="", data=self.options)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception in room sensor selection")
                errors["base"] = "unknown"
        
        # Finde alle Temperatur-Entitäten, die nicht zur Lambda-Domain gehören
        temp_entities = []
        for entity_id in self.hass.states.async_entity_ids():
            state = self.hass.states.get(entity_id)
            if state is None:
                continue
            
            # Prüfe, ob es eine Temperatur-Entität ist und nicht zur Lambda-Domain gehört
            domain = entity_id.split('.')[0]
            if domain != DOMAIN and state.attributes.get("device_class") == SensorDeviceClass.TEMPERATURE:
                temp_entities.append(entity_id)
        
        if not temp_entities:
            # Wenn keine Temperatur-Entitäten gefunden wurden, zeige eine Fehlermeldung
            errors["base"] = "no_temp_sensors"
            return self.async_show_form(
                step_id="room_sensor",
                errors=errors
            )
        
        # Schema für jeden Heizkreis erstellen
        schema = {}
        for hc_idx in range(1, num_hc + 1):
            entity_key = CONF_ROOM_TEMPERATURE_ENTITY.format(hc_idx)
            schema[vol.Optional(
                entity_key,
                default=self.options.get(entity_key, "")
            )] = EntitySelector(
                EntitySelectorConfig(
                    domain=["sensor", "climate", "weather"],
                    device_class=SensorDeviceClass.TEMPERATURE,
                    multiple=False,
                    include_entities=temp_entities
                )
            )
        
        # Zeige das Formular zur Auswahl eines Temperatursensors für jeden Heizkreis
        return self.async_show_form(
            step_id="room_sensor",
            data_schema=vol.Schema(schema),
            errors=errors
        )

    @staticmethod
    @config_entries.callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return LambdaOptionsFlow(config_entry)

class LambdaOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        # Do not store config_entry as an instance variable (deprecated)
        self.options = dict(config_entry.options)
        self.room_thermostat_was_enabled = False

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                _LOGGER.debug("Options Flow - Empfangener user_input: %s", user_input)
                _LOGGER.debug("Options Flow - Aktuelle Optionen: %s", self.config_entry.options)
                _LOGGER.debug("Options Flow - room_thermostat_control in user_input: %s", 
                          "room_thermostat_control" in user_input)
                _LOGGER.debug("Options Flow - room_thermostat_control Wert: %s", 
                          user_input.get("room_thermostat_control"))
                
                update_data = False
                new_data = dict(self.config_entry.data)
                # Firmware-Version
                if "firmware_version" in user_input and user_input["firmware_version"] != self.config_entry.data.get("firmware_version"):
                    new_data["firmware_version"] = user_input["firmware_version"]
                    update_data = True
                
                if update_data:
                    _LOGGER.debug("Updating config entry data: %s", new_data)
                    self.hass.config_entries.async_update_entry(
                        self.config_entry,
                        data=new_data
                    )
                
                # Entferne die Felder aus den Options, die in data gespeichert werden
                options_data = {k: v for k, v in user_input.items() if k not in ("firmware_version")}
                _LOGGER.debug("Options Flow - Nach Filterung: %s", options_data)
                
                # Prüfe, ob room_thermostat_control jetzt aktiviert wurde
                room_thermostat_control = user_input.get("room_thermostat_control", False)
                was_enabled = self.config_entry.options.get("room_thermostat_control", False)
                
                # Speichere die aktuelle Auswahl
                self.options = options_data
                
                # Wenn die Option gerade aktiviert wurde oder bereits aktiviert war, 
                # aber die Entität geändert werden soll
                if room_thermostat_control and (not was_enabled or self.room_thermostat_was_enabled):
                    return await self.async_step_room_sensor()
                
                _LOGGER.debug("Finale Options: %s", options_data)
                return self.async_create_entry(title="", data=options_data)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception in options flow")
                errors["base"] = "unknown"

        options = self.config_entry.options
        firmware_options = list(FIRMWARE_VERSION.keys())

        # Debug für room_thermostat_control
        current_rtc = options.get("room_thermostat_control", DEFAULT_ROOM_THERMOSTAT_CONTROL)
        _LOGGER.debug("Aktueller Wert von room_thermostat_control in options: %s", current_rtc)
        _LOGGER.debug("DEFAULT_ROOM_THERMOSTAT_CONTROL: %s", DEFAULT_ROOM_THERMOSTAT_CONTROL)

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
                default=options.get("room_thermostat_control", DEFAULT_ROOM_THERMOSTAT_CONTROL)
            ): bool,
            vol.Optional(
                "firmware_version",
                default=self.config_entry.data.get("firmware_version", "V0.0.4-3K"),
            ): vol.In(firmware_options),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema),
            errors=errors
        )
        
    async def async_step_room_sensor(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the room sensor selection step."""
        from homeassistant.helpers.entity_registry import async_get
        errors: dict[str, str] = {}
        num_hc = self.config_entry.data.get("num_hc", 1)

        if user_input is not None:
            try:
                for hc_idx in range(1, num_hc + 1):
                    entity_key = CONF_ROOM_TEMPERATURE_ENTITY.format(hc_idx)
                    if entity_key in user_input and user_input[entity_key]:
                        self.options[entity_key] = user_input[entity_key]
                    elif entity_key in self.options:
                        del self.options[entity_key]
                return self.async_create_entry(title="", data=self.options)
            except Exception:
                _LOGGER.exception("Unexpected exception in room sensor selection")
                errors["base"] = "unknown"

        # Hole alle Entities, die NICHT zur eigenen Integration gehören
        temp_entities = []
        registry = async_get(self.hass)
        eigene_entity_ids = {e.entity_id for e in registry.entities.values() if e.config_entry_id == self.config_entry.entry_id}
        for entity_id in self.hass.states.async_entity_ids():
            if entity_id in eigene_entity_ids:
                continue
            state = self.hass.states.get(entity_id)
            if state is None:
                continue
            if state.attributes.get("device_class") == "temperature":
                temp_entities.append(entity_id)

        if not temp_entities:
            errors["base"] = "no_temp_sensors"
            return self.async_show_form(
                step_id="room_sensor",
                errors=errors
            )

        schema = {}
        for hc_idx in range(1, num_hc + 1):
            entity_key = CONF_ROOM_TEMPERATURE_ENTITY.format(hc_idx)
            schema[vol.Optional(
                entity_key,
                default=self.options.get(entity_key, "")
            )] = EntitySelector(
                EntitySelectorConfig(
                    domain=["sensor", "climate", "weather"],
                    device_class="temperature",
                    multiple=False,
                    include_entities=temp_entities
                )
            )
        return self.async_show_form(
            step_id="room_sensor",
            data_schema=vol.Schema(schema),
            errors=errors
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