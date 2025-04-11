"""Climate platform for Lambda integration."""
from __future__ import annotations
from typing import Any
import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEFAULT_NAME, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Lambda climate entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    # Finde die Register-Adressen für die Klima-Entitäten
    hot_water_current_temp_register = None
    hot_water_target_temp_register = None
    heating_circuit_current_temp_register = None
    heating_circuit_target_temp_register = None
    
    for sensor_key, sensor_info in SENSOR_TYPES.items():
        if sensor_key == "boil1_actual_high_temperature":
            hot_water_current_temp_register = sensor_info["address"]
        elif sensor_key == "boil1_target_high_temperature":
            hot_water_target_temp_register = sensor_info["address"]
        elif sensor_key == "hc1_room_device_temperature":
            heating_circuit_current_temp_register = sensor_info["address"]
        elif sensor_key == "hc1_target_room_temperature":  # Korrekter Sensor-Schlüssel
            heating_circuit_target_temp_register = sensor_info["address"]
    
    entities = [
        LambdaClimateEntity(
            coordinator=coordinator,
            entry=entry,
            climate_type="hot_water",
            name="Hot Water",
            current_temp_register=hot_water_current_temp_register,
            target_temp_register=hot_water_target_temp_register,
            min_temp=40,
            max_temp=60,
            temp_step=1
        ),
        LambdaClimateEntity(
            coordinator=coordinator,
            entry=entry,
            climate_type="heating_circuit",
            name="Heating Circuit",
            current_temp_register=heating_circuit_current_temp_register,
            target_temp_register=heating_circuit_target_temp_register,
            min_temp=15,
            max_temp=35,
            temp_step=0.5
        )
    ]
    
    async_add_entities(entities)

class LambdaClimateEntity(CoordinatorEntity, ClimateEntity):
    """Representation of a Lambda climate entity."""

    _attr_temperature_unit = "°C"
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_hvac_modes = [HVACMode.HEAT]  # Nur HEAT-Modus
    _attr_hvac_mode = HVACMode.HEAT     # Immer im HEAT-Modus

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        climate_type: str,
        name: str,
        current_temp_register: int,
        target_temp_register: int,
        min_temp: float,
        max_temp: float,
        temp_step: float
    ) -> None:
        """Initialize the climate entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._climate_type = climate_type
        self._current_temp_register = current_temp_register
        self._target_temp_register = target_temp_register
        
        self._attr_name = f"{entry.data.get(CONF_NAME, DEFAULT_NAME)} {name}"
        self._attr_unique_id = f"{entry.entry_id}_{climate_type}"
        self._attr_min_temp = min_temp
        self._attr_max_temp = max_temp
        self._attr_target_temperature_step = temp_step

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if not self.coordinator.data:
            return None
        # Suche den Sensor mit der passenden Register-Adresse
        for sensor_key, sensor_info in SENSOR_TYPES.items():
            if sensor_info["address"] == self._current_temp_register:
                return self.coordinator.data.get(sensor_key)
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        if not self.coordinator.data:
            return None
        # Suche den Sensor mit der passenden Register-Adresse
        for sensor_key, sensor_info in SENSOR_TYPES.items():
            if sensor_info["address"] == self._target_temp_register:
                return self.coordinator.data.get(sensor_key)
        return None

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return

        try:
            # Suche die Sensor-Definition mit der passenden Register-Adresse
            sensor_info = None
            for info in SENSOR_TYPES.values():
                if info["address"] == self._target_temp_register:
                    sensor_info = info
                    break
            
            if not sensor_info:
                _LOGGER.error("No sensor definition found for register %s", self._target_temp_register)
                return
            
            # Berechne den Rohwert für das Register mit der korrekten Skalierung
            raw_value = int(temperature / sensor_info["scale"])
            
            # Schreibe den Wert in das Modbus-Register
            result = await self.hass.async_add_executor_job(
                self.coordinator.client.write_registers,
                self._target_temp_register,
                [raw_value],
                self._entry.data.get("slave_id", 1)
            )
            
            if result.isError():
                _LOGGER.error("Failed to write target temperature: %s", result)
                return
                
            # Aktualisiere den Coordinator-Cache
            for sensor_key, info in SENSOR_TYPES.items():
                if info["address"] == self._target_temp_register:
                    self.coordinator.data[sensor_key] = temperature
                    break
                    
            self.async_write_ha_state()
            _LOGGER.debug("Successfully set target temperature to %s°C", temperature)
            
        except Exception as ex:
            _LOGGER.error("Error setting target temperature: %s", ex)