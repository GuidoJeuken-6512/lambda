"""Sensor platform for Lambda."""
from __future__ import annotations
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN, SENSOR_TYPES

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Lambda sensors from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    entities = []
    for sensor_type, sensor_config in SENSOR_TYPES.items():
        entities.append(
            LambdaSensor(
                coordinator,
                entry,
                sensor_type,
                sensor_config
            )
        )

    async_add_entities(entities)

class LambdaSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lambda sensor."""

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        sensor_type: str,
        sensor_config: dict[str, Any]
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._config = sensor_config
        self._entry = entry

        self._attr_name = f"{entry.data.get(CONF_NAME, 'Lambda')} {sensor_config['name']}"
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_native_unit_of_measurement = sensor_config.get("unit")
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_type)