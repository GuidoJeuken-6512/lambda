"""Data update coordinator for Lambda."""
from __future__ import annotations
from datetime import timedelta
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

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
        self.client = None

    async def _async_update_data(self):
        """Fetch data from Lambda device."""
        from pymodbus.client import ModbusTcpClient
        from pymodbus.exceptions import ModbusException
        
        if not self.client:
            self.client = ModbusTcpClient(self.host, port=self.port)
            if not await self.hass.async_add_executor_job(self.client.connect):
                raise ConnectionError("Could not connect to Modbus TCP")

        try:
            # Hier Ihre Modbus-Abfragelogik implementieren
            data = {}
            # Beispiel:
            result = await self.hass.async_add_executor_job(
                self.client.read_holding_registers,
                1004,  # Beispiel-Adresse
                1,
                self.slave_id
            )
            if result.isError():
                raise ModbusException("Modbus error")
                
            data["flow_temp"] = result.registers[0] * 0.1  # Beispiel-Skalierung
            
            return data
            
        except ModbusException as ex:
            _LOGGER.error("Modbus error: %s", ex)
            if self.client:
                await self.hass.async_add_executor_job(self.client.close)
                self.client = None
            raise