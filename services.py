"""Services for Lambda WP integration."""
from __future__ import annotations
import logging
from typing import Any
from datetime import timedelta

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.const import (
    ATTR_ENTITY_ID,
)
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.components.sensor import SensorStateClass

from .const import (
    DOMAIN,
    CONF_ROOM_TEMPERATURE_ENTITY,
    ROOM_TEMPERATURE_REGISTER_OFFSET,
    ROOM_TEMPERATURE_UPDATE_INTERVAL,
    HC_BASE_ADDRESS,
)

# Konstanten für Zustandsarten definieren
STATE_UNAVAILABLE = "unavailable"
STATE_UNKNOWN = "unknown"

_LOGGER = logging.getLogger(__name__)

# Service Schema
UPDATE_ROOM_TEMPERATURE_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_ENTITY_ID): cv.string,
    }
)

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up Lambda WP services."""
    
    # Speichere die Unsubscribe-Funktionen pro Entry, um sie später entfernen zu können
    unsub_update_callbacks = {}
    
    async def async_update_room_temperature(call: ServiceCall) -> None:
        """Update room temperature from the selected sensor to Modbus register."""
        # Hole alle Lambda-Integrationen
        lambda_entries = hass.data.get(DOMAIN, {})
        
        if not lambda_entries:
            _LOGGER.error("No Lambda WP integrations found")
            return
        
        # Optional spezifisches Entity_ID zur Einschränkung
        target_entity_id = call.data.get(ATTR_ENTITY_ID)
        
        for entry_id, entry_data in lambda_entries.items():
            config_entry = hass.config_entries.async_get_entry(entry_id)
            if not config_entry or not config_entry.options:
                _LOGGER.debug("No config entry or options for entry_id %s", entry_id)
                continue
                
            # Prüfe, ob Raumthermostat aktiviert ist
            if not config_entry.options.get("room_thermostat_control", False):
                _LOGGER.debug("Room thermostat control not enabled for entry_id %s", entry_id)
                continue
                
            # Anzahl Heizkreise ermitteln
            num_hc = config_entry.data.get("num_hc", 1)
            
            # Wenn eine spezifische Entity-ID angegeben wurde und nicht übereinstimmt, überspringe
            if target_entity_id and target_entity_id != entry_id:
                continue
                
            # Hole Coordinator für gemeinsame Nutzung
            coordinator = entry_data.get("coordinator")
            if not coordinator or not coordinator.client:
                _LOGGER.error("Coordinator or Modbus client not available for entry_id %s", entry_id)
                continue
                
            # Für jeden Heizkreis prüfen und aktualisieren
            for hc_idx in range(1, num_hc + 1):
                entity_key = CONF_ROOM_TEMPERATURE_ENTITY.format(hc_idx)
                
                # Prüfen, ob für diesen Heizkreis ein Temperatursensor konfiguriert ist
                room_temp_entity_id = config_entry.options.get(entity_key)
                if not room_temp_entity_id:
                    _LOGGER.debug("No room temperature entity selected for heating circuit %s in entry_id %s", 
                                 hc_idx, entry_id)
                    continue
                
                # Holen der Temperatur vom Sensor
                state = hass.states.get(room_temp_entity_id)
                if state is None or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN, ""):
                    _LOGGER.warning(
                        "Room temperature entity %s is not available for heating circuit %s",
                        room_temp_entity_id,
                        hc_idx
                    )
                    continue
                    
                try:
                    temperature = float(state.state)
                    
                    # Berechne Rohwert (Temperatur * 10)
                    raw_value = int(temperature * 10)
                    
                    # Berechne die korrekte Modbus-Register-Adresse für diesen Heizkreis
                    register_address = HC_BASE_ADDRESS[hc_idx] + ROOM_TEMPERATURE_REGISTER_OFFSET
                    
                    # Debug-Eintrag anstatt tatsächlich ins Modbus-Register zu schreiben
                    _LOGGER.info(
                        "Simuliere Modbus write auf Register %s mit Wert %s (Temperatur: %s°C) für Heizkreis %s, entry_id %s",
                        register_address,
                        raw_value,
                        temperature,
                        hc_idx,
                        entry_id
                    )
                    
                    # Kein tatsächlicher Modbus-Schreibvorgang!
                    # result = await hass.async_add_executor_job(
                    #     coordinator.client.write_registers,
                    #     register_address,
                    #     [raw_value],
                    #     config_entry.data.get("slave_id", 1)
                    # )
                    # 
                    # if result.isError():
                    #     _LOGGER.error("Failed to write room temperature: %s", result)
                        
                except (ValueError, TypeError) as ex:
                    _LOGGER.error(
                        "Unable to convert temperature from %s for heating circuit %s: %s",
                        room_temp_entity_id,
                        hc_idx,
                        ex
                    )
                except Exception as ex:
                    _LOGGER.error("Error updating room temperature for heating circuit %s: %s", 
                                 hc_idx, ex)
    
    # Setup regelmäßige Aktualisierungen für alle Entries
    @callback
    def setup_scheduled_updates() -> None:
        """Set up scheduled updates for all entries."""
        # Bestehende Unsubscriber entfernen
        for unsub in unsub_update_callbacks.values():
            unsub()
        unsub_update_callbacks.clear()
        
        # Für jede Konfiguration einen Timer einrichten, wenn Raumthermostat aktiviert ist
        for entry_id in hass.data.get(DOMAIN, {}):
            config_entry = hass.config_entries.async_get_entry(entry_id)
            if not config_entry or not config_entry.options:
                continue
                
            # Prüfe, ob Raumthermostat aktiviert ist
            if not config_entry.options.get("room_thermostat_control", False):
                continue
                
            # Prüfe, ob mindestens ein Heizkreis einen Sensor hat
            num_hc = config_entry.data.get("num_hc", 1)
            has_sensor = False
            
            for hc_idx in range(1, num_hc + 1):
                entity_key = CONF_ROOM_TEMPERATURE_ENTITY.format(hc_idx)
                if config_entry.options.get(entity_key):
                    has_sensor = True
                    break
            
            if not has_sensor:
                _LOGGER.debug("No room temperature sensors configured for entry_id %s", entry_id)
                continue
                
            # Update-Intervall aus der Konstante
            update_interval = timedelta(minutes=ROOM_TEMPERATURE_UPDATE_INTERVAL)
            
            # Timer einrichten
            _LOGGER.debug(
                "Setting up scheduled room temperature updates for entry_id %s every %s",
                entry_id,
                update_interval
            )
            
            # Erstelle ServiceCall-Daten für den spezifischen Entry
            service_data = {ATTR_ENTITY_ID: entry_id}
            
            # Timer starten mit periodischem Aufruf des Services
            unsub = async_track_time_interval(
                hass,
                lambda _: async_update_room_temperature(ServiceCall(DOMAIN, "update_room_temperature", service_data)),
                update_interval
            )
            
            # Speichere Unsubscribe-Funktion
            unsub_update_callbacks[entry_id] = unsub
    
    # Bei Änderungen in der Konfiguration die Timers neu einrichten
    @callback
    def config_entry_updated(hass, updated_entry) -> None:
        """Reagiere auf Konfigurationsänderungen."""
        _LOGGER.debug("Config entry updated, resetting scheduled updates")
        setup_scheduled_updates()
    
    # Registriere Listener für Konfigurationsänderungen
    hass.bus.async_listen("config_entry_updated", config_entry_updated)
    
    # Initialen Setup durchführen
    setup_scheduled_updates()
    
    # Registriere Services
    hass.services.async_register(
        DOMAIN,
        "update_room_temperature",
        async_update_room_temperature,
        schema=UPDATE_ROOM_TEMPERATURE_SCHEMA
    )
    
    # Unregister-Callback für das Entfernen aller Unsubscriber
    @callback
    def async_unload_services_callback() -> None:
        """Unload services callback."""
        for unsub in unsub_update_callbacks.values():
            unsub()
        unsub_update_callbacks.clear()
        
    # Speichere Unsubscribe-Funktion in hass.data
    hass.data.setdefault(f"{DOMAIN}_services", {})["unsub_callbacks"] = async_unload_services_callback

async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Lambda WP services."""
    if hass.services.has_service(DOMAIN, "update_room_temperature"):
        hass.services.async_remove(DOMAIN, "update_room_temperature")
        
    # Unsubscribe von allen Timern
    if f"{DOMAIN}_services" in hass.data and "unsub_callbacks" in hass.data[f"{DOMAIN}_services"]:
        hass.data[f"{DOMAIN}_services"]["unsub_callbacks"]()
        del hass.data[f"{DOMAIN}_services"] 