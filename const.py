"""Constants for Lambda WP integration."""
DOMAIN = "lambda"
DEFAULT_NAME = "EU08L"
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_HOST = "192.168.178.125"
DEFAULT_FIRMWARE = "V0.0.4-3K"

# Konfigurationskonstanten
CONF_SLAVE_ID = "slave_id"

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
    },
    "error_number": {
        "relative_address": 1,
        "name": "Error Number",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "state": {
        "relative_address": 2,
        "name": "State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
    },
    "operating_state": {
        "relative_address": 3,
        "name": "Operating State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
    },
    "flow_line_temperature": {
        "relative_address": 4,
        "name": "Flow Line Temperature",
        "unit": "°C",
        "scale": 0.01,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "return_line_temperature": {
        "relative_address": 5,
        "name": "Return Line Temperature",
        "unit": "°C",
        "scale": 0.01,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "volume_flow_heat_sink": {
        "relative_address": 6,
        "name": "Volume Flow Heat Sink",
        "unit": "l/h",
        "scale": 1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "energy_source_inlet_temperature": {
        "relative_address": 7,
        "name": "Energy Source Inlet Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "energy_source_outlet_temperature": {
        "relative_address": 8,
        "name": "Energy Source Outlet Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "volume_flow_energy_source": {
        "relative_address": 9,
        "name": "Volume Flow Energy Source",
        "unit": "l/min",
        "scale": 0.01,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "compressor_unit_rating": {
        "relative_address": 10,
        "name": "Compressor Unit Rating",
        "unit": "%",
        "scale": 0.01,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
    },
    "actual_heating_capacity": {
        "relative_address": 11,
        "name": "Actual Heating Capacity",
        "unit": "kW",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "inverter_power_consumption": {
        "relative_address": 12,
        "name": "Inverter Power Consumption",
        "unit": "W",
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "cop": {
        "relative_address": 13,
        "name": "COP",
        "unit": None,
        "scale": 0.01,
        "precision": 2,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "request_type": {
        "relative_address": 15,
        "name": "Request-Type",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "requested_flow_line_temperature": {
        "relative_address": 16,
        "name": "Requested Flow Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "requested_return_line_temperature": {
        "relative_address": 17,
        "name": "Requested Return Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "requested_flow_to_return_line_temperature_difference": {
        "relative_address": 18,
        "name": "Requested Flow to Return Line Temperature Difference",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "relais_state_2nd_heating_stage": {
        "relative_address": 19,
        "name": "Relais State 2nd Heating Stage",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "compressor_power_consumption_accumulated": {
        "relative_address": 20,
        "name": "Compressor Power Consumption Accumulated",
        "unit": "Wh",
        "scale": 1,
        "precision": 0,
        "data_type": "int32",
        "firmware_version": 1,
    },
    "compressor_thermal_energy_output_accumulated": {
        "relative_address": 22,
        "name": "Compressor Thermal Energy Output Accumulated",
        "unit": "Wh",
        "scale": 1,
        "precision": 0,
        "data_type": "int32",
        "firmware_version": 1,
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
    },
    "operating_state": {
        "relative_address": 1,
        "name": "Boiler Operating State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
    },
    "actual_high_temperature": {
        "relative_address": 2,
        "name": "Boiler Actual High Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "actual_low_temperature": {
        "relative_address": 3,
        "name": "Boiler Actual Low Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "target_high_temperature": {
        "relative_address": 50,
        "name": "Boiler Target High Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
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
    },    
    "ambient_error_number": {
        "address": 0,
        "name": "Ambient Error Number",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "ambient_operating_state": {
        "address": 1,
        "name": "Ambient Operating State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
        "firmware_version": 1,
    },
    "ambient_temperature": {
        "address": 2,
        "name": "Ambient Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "ambient_temperature_1h": {
        "address": 3,
        "name": "Ambient Temperature 1h",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    "ambient_temperature_calculated": {
        "address": 4,
        "name": "Ambient Temperature Calculated",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
        "firmware_version": 1,
    },
    # Heating Circuit
    "hc1_error_number": {
        "address": 5000,
        "name": "Heating Circuit Error Number",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
    },
    "hc1_operating_state": {
        "address": 5001,
        "name": "Heating Circuit Operating State",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "uint16",
    },
    "hc1_flow_line_temperature": {
        "address": 5002,
        "name": "Flow Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
    },
    "hc1_return_line_temperature": {
        "address": 5003,
        "name": "Return Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
    },
    "hc1_room_device_temperature": {
        "address": 5004,
        "name": "Room Device Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
    },
    "hc1_set_flow_line_temperature": {
        "address": 5005,
        "name": "Set Flow Line Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
    },
    "hc1_operating_mode": {
        "address": 5006,
        "name": "Operating Mode",
        "unit": None,
        "scale": 1,
        "precision": 0,
        "data_type": "int16",
    },
    "hc1_set_flow_line_offset_temperature": {
        "address": 5050,
        "name": "Set Flow Line Offset Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
    },
    "hc1_target_room_temperature": {
        "address": 5051,
        "name": "Target Room Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
    },
    "hc1_set_cooling_mode_room_temperature": {
        "address": 5052,
        "name": "Set Cooling Mode Room Temperature",
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "data_type": "int16",
    },
}