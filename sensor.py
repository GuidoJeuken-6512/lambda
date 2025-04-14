"""Platform for Lambda WP sensor integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEFAULT_NAME, SENSOR_TYPES, FIRMWARE_VERSION

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Lambda sensor entries."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    # Hole die konfigurierte Firmware-Version
    configured_fw = entry.data.get("firmware_version", "V0.0.4-3K")
    fw_version = int(FIRMWARE_VERSION.get(configured_fw, "1"))
    
    _LOGGER.debug(
        "Firmware-Version Setup - Configured: %s, Numeric Version: %s, Raw Entry Data: %s, Available Versions: %s",
        configured_fw,
        fw_version,
        entry.data,
        FIRMWARE_VERSION
    )
    
    # Erstelle eine Liste von Sensoren basierend auf der Firmware-Version
    entities = []
    
    for sensor_id, sensor_config in SENSOR_TYPES.items():
        # Prüfe ob der Sensor für diese Firmware-Version verfügbar ist
        sensor_fw = sensor_config.get("firmware_version", 1)
        is_compatible = sensor_fw <= fw_version
        
        _LOGGER.debug(
            "Sensor Compatibility Check - Sensor: %s, Required FW: %s, Current FW: %s, Compatible: %s, Raw Sensor Config: %s",
            sensor_id,
            sensor_fw,
            fw_version,
            is_compatible,
            sensor_config
        )
        
        if is_compatible:
            entities.append(
                LambdaSensor(
                    coordinator=coordinator,
                    entry=entry,
                    sensor_id=sensor_id,
                    sensor_config=sensor_config,
                )
            )
    
    _LOGGER.debug("Total number of compatible entities: %s", len(entities))
    async_add_entities(entities)

class LambdaSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lambda sensor."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        sensor_id: str,
        sensor_config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._sensor_id = sensor_id
        self._config = sensor_config
        self._attr_name = sensor_config["name"]
        self._attr_unique_id = f"{entry.entry_id}_{sensor_id}"
        self._attr_native_unit_of_measurement = sensor_config["unit"]
        
        # Setze die Genauigkeit
        if "precision" in sensor_config:
            self._attr_suggested_display_precision = sensor_config["precision"]

        # Bestimme die Device-Klasse basierend auf der Einheit
        if sensor_config["unit"] == "°C":
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
        elif sensor_config["unit"] == "W":
            self._attr_device_class = SensorDeviceClass.POWER
        elif sensor_config["unit"] == "Wh":
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
            
        value = self.coordinator.data.get(self._sensor_id)
        if value is None:
            return None
            
        # Skaliere den Wert entsprechend der Konfiguration
        return value * self._config["scale"]