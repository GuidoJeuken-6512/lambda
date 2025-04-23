"""Data update coordinator for Lambda."""
from __future__ import annotations
from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import SENSOR_TYPES, HP_SENSOR_TEMPLATES, HP_BASE_ADDRESS

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)

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
        self.host = entry.data["host"]
        self.port = entry.data["port"]
        self.slave_id = entry.data.get("slave_id", 1)
        self.debug_mode = entry.data.get("debug_mode", False)
        if self.debug_mode:
            _LOGGER.setLevel(logging.DEBUG)
        self.client = None
        self.config_entry_id = entry.entry_id

    async def _async_update_data(self):
        """Fetch data from Lambda device."""
        from pymodbus.client import ModbusTcpClient
        from pymodbus.exceptions import ModbusException
        
        if not self.client:
            self.client = ModbusTcpClient(self.host, port=self.port)
            if not await self.hass.async_add_executor_job(self.client.connect):
                raise ConnectionError("Could not connect to Modbus TCP")
            _LOGGER.debug("Modbus client initialized for host %s on port %s", self.host, self.port)

        try:
            data = {}
            # 1. Statische Sensoren abfragen
            _LOGGER.debug("Starting static sensor block...")
            static_sensor_count = len(SENSOR_TYPES)
            _LOGGER.debug("Reading %d static sensors", static_sensor_count)
            try:
                for sensor_id, sensor_config in SENSOR_TYPES.items():
                    _LOGGER.debug("Reading static sensor: %s with address: %d", sensor_id, sensor_config["address"])
                    count = 2 if sensor_config["data_type"] == "int32" else 1
                    result = await self.hass.async_add_executor_job(
                        self.client.read_holding_registers,
                        sensor_config["address"],
                        count,
                        self.slave_id
                    )
                    if result.isError():
                        _LOGGER.warning(f"Modbus error for {sensor_id}")
                        continue
                    if sensor_config["data_type"] == "int32":
                        raw_value = (result.registers[0] << 16) | result.registers[1]
                    else:
                        raw_value = result.registers[0]
                    scaled_value = raw_value * sensor_config["scale"]
                    data[sensor_id] = scaled_value
            except Exception as ex:
                _LOGGER.error("Exception in static sensor block: %s", ex)
            _LOGGER.debug("Static sensor block finished, entering HP sensor block...")
            # 2. Dynamische HP-Sensoren abfragen
            num_hps = self.hass.config_entries.async_get_entry(self.config_entry_id).data.get("num_hps", 1)
            _LOGGER.debug("Reading  %d heat pumps",  num_hps)
            dynamic_sensor_count = num_hps * len(HP_SENSOR_TEMPLATES)
            _LOGGER.debug("Reading %d dynamic sensors for %d heat pumps", dynamic_sensor_count, num_hps)
            _LOGGER.debug("Preparing to read HP sensors: num_hps=%s, HP_SENSOR_TEMPLATES keys: %s, HP_BASE_ADDRESS keys: %s", num_hps, list(HP_SENSOR_TEMPLATES.keys()), list(HP_BASE_ADDRESS.keys()))
            if not HP_SENSOR_TEMPLATES:
                _LOGGER.error("HP_SENSOR_TEMPLATES is empty!")
            for hp_idx in range(1, num_hps + 1):
                _LOGGER.debug("Reading sensors for HP %s", hp_idx)
                for template_key in HP_SENSOR_TEMPLATES:
                    _LOGGER.debug("HP %s, template_key: %s", hp_idx, template_key)
                    sensor_id = f"hp{hp_idx}_{template_key}"
                    address = HP_BASE_ADDRESS.get(hp_idx)
                    if address is None:
                        _LOGGER.warning("No base address for HP %s", hp_idx)
                        continue
                    address += HP_SENSOR_TEMPLATES[template_key]["relative_address"]
                    count = 2 if HP_SENSOR_TEMPLATES[template_key]["data_type"] == "int32" else 1
                    try:
                        _LOGGER.debug("Attempting to read Modbus register for sensor %s at address %d with count %d", sensor_id, address, count)
                        result = await self.hass.async_add_executor_job(
                            self.client.read_holding_registers,
                            address,
                            count,
                            self.slave_id
                        )
                        if result.isError():
                            _LOGGER.warning(f"Modbus error for {sensor_id}")
                            continue
                        if HP_SENSOR_TEMPLATES[template_key]["data_type"] == "int32":
                            raw_value = (result.registers[0] << 16) | result.registers[1]
                        else:
                            raw_value = result.registers[0]
                        scaled_value = raw_value * HP_SENSOR_TEMPLATES[template_key]["scale"]
                        _LOGGER.debug(
                            "Successfully read %s: %s (raw: %s)",
                            sensor_id, scaled_value, raw_value
                        )
                        data[sensor_id] = scaled_value
                    except Exception as ex:
                        _LOGGER.error("Exception reading HP sensor %s at address %s: %s", sensor_id, address, ex)
            _LOGGER.debug("Final data structure: %s", data)
            return data
        except ModbusException as ex:
            _LOGGER.error("Modbus error: %s", ex)
            if self.client:
                await self.hass.async_add_executor_job(self.client.close)
                self.client = None
            raise
        except Exception as ex:
            _LOGGER.error("Exception in _async_update_data: %s", ex)
            raise
        finally:
            _LOGGER.debug("End of _async_update_data reached (after HP sensor block)")