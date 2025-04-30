"""Constants for Lambda WP integration."""
DOMAIN = "lambda"
DEFAULT_NAME = "EU08L"
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_HOST = "192.168.178.125"
DEFAULT_FIRMWARE = "V0.0.4-3K"
DEFAULT_ROOM_THERMOSTAT_CONTROL = False

# Konfigurationskonstanten
CONF_SLAVE_ID = "slave_id"
CONF_ROOM_TEMPERATURE_ENTITY = "room_temperature_entity_{0}"  # Formatstring für room_temperature_entity_1, _2, etc.

# Modbus Register für Raumtemperatur-Basis (wird mit HC_BASE_ADDRESS kombiniert)
ROOM_TEMPERATURE_REGISTER_OFFSET = 4  # Register-Offset für Raumtemperatur innerhalb eines HC

# Intervall für die Aktualisierung der Raumtemperatur (in Minuten)
ROOM_TEMPERATURE_UPDATE_INTERVAL = 1

# Debug configuration
DEBUG = False
DEBUG_PREFIX = "lambda_wp"

FIRMWARE_VERSION = {
    "V0.0.3-3K": "1",
    "V0.0.4-3K": "2",
    "V0.0.5-3K": "3",
    "V0.0.6-3K": "4",
    "V0.0.7-3K": "5",
}

# Logging levels
LOG_LEVELS = {
    "error": "ERROR",
    "warning": "WARNING",
    "info": "INFO",
    "debug": "DEBUG"
}

# Basisadressen für Heatpumps
HP_BASE_ADDRESS = {1: 1000, 2: 1100, 3: 1200, 4: 1300, 5: 1400}

# Basisadressen für Boiler
BOIL_BASE_ADDRESS = {1: 2000, 2: 2100, 3: 2200, 4: 2300, 5: 2400}

# Basisadressen für Heizkreise
HC_BASE_ADDRESS = {1: 5000, 2: 5100, 3: 5200, 4: 5300, 5: 5400}

# Templates für HP-Sensoren (ohne hp1_-Präfix)
HP_SENSOR_TEMPLATES = {
    "error_state": {
        "relative_address": 0,
        "name": "Error State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "error_number": {
        "relative_address": 1,
        "name": "Error Number",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "state": {
        "relative_address": 2,
        "name": "State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "operating_state": {
        "relative_address": 3,
        "name": "Operating State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "flow_line_temperature": {
        "relative_address": 4,
        "name": "Flow Line Temperature",
        "unit": "°C",
        "scale": 0.01,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "return_line_temperature": {
        "relative_address": 5,
        "name": "Return Line Temperature",
        "unit": "°C",
        "scale": 0.01,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "volume_flow_heat_sink": {
        "relative_address": 6,
        "name": "Volume Flow Heat Sink",
        "unit": "l/h",
        "scale": 1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "energy_source_inlet_temperature": {
        "relative_address": 7,
        "name": "Energy Source Inlet Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "energy_source_outlet_temperature": {
        "relative_address": 8,
        "name": "Energy Source Outlet Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "volume_flow_energy_source": {
        "relative_address": 9,
        "name": "Volume Flow Energy Source",
        "unit": "l/min",
        "scale": 0.01,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "compressor_unit_rating": {
        "relative_address": 10,
        "name": "Compressor Unit Rating",
        "unit": "%",
        "scale": 0.01,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "actual_heating_capacity": {
        "relative_address": 11,
        "name": "Actual Heating Capacity",
        "unit": "kW",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "inverter_power_consumption": {
        "relative_address": 12,
        "name": "Inverter Power Consumption",
        "unit": "W",
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "cop": {
        "relative_address": 13,
        "name": "COP",
        "unit": None,
        "scale": 0.01,
        "precision": 2,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "request_type": {
        "relative_address": 15,
        "name": "Request-Type",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "requested_flow_line_temperature": {
        "relative_address": 16,
        "name": "Requested Flow Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "requested_return_line_temperature": {
        "relative_address": 17,
        "name": "Requested Return Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "requested_flow_to_return_line_temperature_difference": {
        "relative_address": 18,
        "name": "Requested Flow to Return Line Temperature Difference",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "relais_state_2nd_heating_stage": {
        "relative_address": 19,
        "name": "Relais State 2nd Heating Stage",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "compressor_power_consumption_accumulated": {
        "relative_address": 20,
        "name": "Compressor Power Consumption Accumulated",
        "unit": "Wh",
        "scale": 1,
        "precision": 0,
        "data_type": "int32",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
    "compressor_thermal_energy_output_accumulated": {
        "relative_address": 22,
        "name": "Compressor Thermal Energy Output Accumulated",
        "unit": "Wh",
        "scale": 1,
        "precision": 0,
        "data_type": "int32",
        "firmware_version": 1,
        "device_type": "heat_pump",
    },
}

# Templates für Boiler-Sensoren (ohne boil1_-Präfix)
BOIL_SENSOR_TEMPLATES = {
    "error_number": {
        "relative_address": 0,
        "name": "Boiler Error Number",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "boiler",
    },
    "operating_state": {
        "relative_address": 1,
        "name": "Boiler Operating State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
        "device_type": "boiler",
    },
    "actual_high_temperature": {
        "relative_address": 2,
        "name": "Boiler Actual High Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "boiler",
    },
    "actual_low_temperature": {
        "relative_address": 3,
        "name": "Boiler Actual Low Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "boiler",
    },
    "target_high_temperature": {
        "relative_address": 50,
        "name": "Boiler Target High Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "boiler",
    },
}

# Templates für HC-Sensoren (ohne hc1_-Präfix)
HC_SENSOR_TEMPLATES = {
    "error_number": {
        "relative_address": 0,
        "name": "Heating Circuit Error Number",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "operating_state": {
        "relative_address": 1,
        "name": "Heating Circuit Operating State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "flow_line_temperature": {
        "relative_address": 2,
        "name": "Flow Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "return_line_temperature": {
        "relative_address": 3,
        "name": "Return Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "room_device_temperature": {
        "relative_address": 4,
        "name": "Room Device Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "set_flow_line_temperature": {
        "relative_address": 5,
        "name": "Set Flow Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "operating_mode": {
        "relative_address": 6,
        "name": "Operating Mode",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "set_flow_line_offset_temperature": {
        "relative_address": 50,
        "name": "Set Flow Line Offset Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "target_room_temperature": {
        "relative_address": 51,
        "name": "Target Room Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
    "set_cooling_mode_room_temperature": {
        "relative_address": 52,
        "name": "Set Cooling Mode Room Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "heating_circuit",
    },
}

SENSOR_TYPES = {
    # General Ambient
    "aaaadummy": {
        "address": 0,
        "name": "Dummy für FW Selction",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 2,
        "device_type": "main",
    },    
    "ambient_error_number": {
        "address": 0,
        "name": "Ambient Error Number",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "main",
    },
    "ambient_operating_state": {
        "address": 1,
        "name": "Ambient Operating State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
        "device_type": "main",
    },
    "ambient_temperature": {
        "address": 2,
        "name": "Ambient Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "main",
    },
    "ambient_temperature_1h": {
        "address": 3,
        "name": "Ambient Temperature 1h",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "main",
    },
    "ambient_temperature_calculated": {
        "address": 4,
        "name": "Ambient Temperature Calculated",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
        "device_type": "main",
    },
}

# Text templates for the state sensors
AMBIENT_OPERATING_STATE = {
    0: "Off",
    1: "Automatik",
    2: "Manual",
    3: "Error"
}

EMGR_OPERATING_STATE = {
    0: "Off",
    1: "Automatik",
    2: "Manual",
    3: "Error",
    4: "Offline"
}

HP_ERROR_STATE = {
    0: "OK",
    1: "Message",
    2: "Warning",
    3: "Alarm",
    4: "Fault"
}

HP_STATE = {
    0: "Init",
    1: "Reference",
    2: "Restart-Block",
    3: "Ready",
    4: "Start Pumps",
    5: "Start Compressor",
    6: "Pre-Regulation",
    7: "Regulation",
    8: "Not Used",
    9: "Cooling",
    10: "Defrosting",
    31: "Fault-Lock",
    32: "Alarm-Block",
    41: "Error-Reset"
}

HP_OPERATING_STATE = {
    0: "Standby",
    1: "Heizung",
    2: "WW-Bereitung",
    3: "Cold Climate",
    4: "Circulation",
    5: "Defrost",
    6: "Off",
    7: "Frost",
    8: "Standby-Frost",
    9: "Not used",
    10: "Sommer",
    11: "Ferienbetrieb",
    12: "Error",
    13: "Warning",
    14: "Info-Message",
    15: "Time-Block",
    16: "Release-Block",
    17: "Mintemp-Block",
    18: "Firmware-Download"
}

HP_REQUEST_TYPE = {
    0: "No Request",
    1: "Flow Pump Circulation",
    2: "Central Heating",
    3: "Central Cooling",
    4: "Domestic Hot Water"
}

BOIL_OPERATING_STATE = {
    0: "Standby",
    1: "Domestic Hot Water",
    2: "Legio",
    3: "Summer",
    4: "Frost",
    5: "Holiday",
    6: "Prio-Stop",
    7: "Error",
    8: "Off",
    9: "Prompt-DHW",
    10: "Trailing-Stop",
    11: "Temp-Lock",
    12: "Standby-Frost"
}

HC_OPERATING_STATE = {
    0: "Heating",
    1: "Eco",
    2: "Cooling",
    3: "Floor-dry",
    4: "Frost",
    5: "Max-Temp",
    6: "Error",
    7: "Service",
    8: "Holiday",
    9: "Central Heating Summer",
    10: "Central Cooling Winter",
    11: "Prio-Stop",
    12: "Off",
    13: "Release-Off",
    14: "Time-Off",
    15: "Standby",
    16: "Standby-Heating",
    17: "Standby-Eco",
    18: "Standby-Cooling",
    19: "Standby-Frost",
    20: "Standby-Floor-dry"
}

HC_OPERATING_MODE = {
    0: "Off",
    1: "Manual",
    2: "Automatik",
    3: "Auto-Heating",
    4: "Auto-Cooling",
    5: "Frost",
    6: "Summer",
    7: "Floor-dry"
}

