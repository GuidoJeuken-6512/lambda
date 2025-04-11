"""The Lambda integration."""
from __future__ import annotations
from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, DEBUG, DEBUG_PREFIX, LOG_LEVELS, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)

def setup_debug_logging(hass: HomeAssistant, config: ConfigType) -> None:
    """Set up debug logging for the integration."""
    if config.get("debug", False):
        logging.getLogger(DEBUG_PREFIX).setLevel(logging.DEBUG)
        _LOGGER.info("Debug logging enabled for %s", DEBUG_PREFIX)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Lambda integration."""
    setup_debug_logging(hass, config)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lambda from a config entry."""
    _LOGGER.debug("Setting up Lambda integration with config: %s", entry.data)
    
    try:
        coordinator = LambdaDataUpdateCoordinator(hass, entry)
        await coordinator.async_config_entry_first_refresh()
    except Exception as ex:
        _LOGGER.error("Failed to initialize Lambda integration: %s", ex)
        return False

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator
    }

    # Set up all platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "climate"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Lambda integration")
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, ["sensor", "climate"]):
        if entry.entry_id in hass.data[DOMAIN]:
            coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
            if coordinator.client:
                await hass.async_add_executor_job(coordinator.client.close)
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class LambdaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Lambda data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name="Lambda Coordinator",
            update_interval=SCAN_INTERVAL
        )
        self.entry = entry
        self.client = None
        _LOGGER.debug("Initialized LambdaDataUpdateCoordinator")

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Lambda device."""
        from pymodbus.client import ModbusTcpClient
        from pymodbus.exceptions import ModbusException

        if self.client is None:
            _LOGGER.debug("Creating new Modbus TCP client")
            self.client = ModbusTcpClient(
                self.entry.data["host"],
                port=self.entry.data["port"]
            )
            if not await self.hass.async_add_executor_job(self.client.connect):
                _LOGGER.error("Could not connect to Modbus TCP at %s:%s", 
                            self.entry.data["host"], 
                            self.entry.data["port"])
                self.client = None
                raise UpdateFailed("Could not connect to Modbus TCP")

        try:
            data = {}
            _LOGGER.debug("Reading Modbus registers")
            
            # Read all sensor registers defined in SENSOR_TYPES
            for sensor_key, sensor_info in SENSOR_TYPES.items():
                try:
                    # Determine number of registers to read based on data type
                    count = 2 if sensor_info["data_type"] == "int32" else 1
                    
                    result = await self.hass.async_add_executor_job(
                        self.client.read_holding_registers,
                        sensor_info["address"],
                        count,  # Number of registers to read
                        self.entry.data.get("slave_id", 1)
                    )
                    
                    if result.isError():
                        _LOGGER.error("Modbus read error for sensor %s: %s", sensor_key, result)
                        continue
                        
                    # Process the value based on data type
                    if sensor_info["data_type"] == "int32":
                        # Combine two 16-bit registers into one 32-bit value
                        raw_value = (result.registers[0] << 16) | result.registers[1]
                    else:
                        raw_value = result.registers[0]
                        
                    # Apply scaling and store the value
                    scaled_value = raw_value * sensor_info["scale"]
                    data[sensor_key] = scaled_value
                    
                    _LOGGER.debug("Successfully read %s: %s (raw: %s)", 
                                sensor_key, 
                                scaled_value,
                                raw_value)
                    
                except ModbusException as ex:
                    _LOGGER.error("Error reading sensor %s: %s", sensor_key, ex)
                    continue
                    
            if not data:
                _LOGGER.error("No sensor data could be read")
                raise UpdateFailed("No sensor data available")
                
            return data

        except ModbusException as ex:
            _LOGGER.error("Modbus communication error: %s", ex)
            if self.client:
                await self.hass.async_add_executor_job(self.client.close)
            self.client = None
            raise UpdateFailed(f"Modbus communication error: {ex}")
        except Exception as ex:
            _LOGGER.error("Unexpected error: %s", ex)
            if self.client:
                await self.hass.async_add_executor_job(self.client.close)
            self.client = None
            raise UpdateFailed(f"Unexpected error: {ex}")