# Lambda Heat Pump Integration - Documentation

## Structure of the Integration

The integration consists of the following main files:

- **manifest.json**: Contains metadata such as name, version, dependencies (`pymodbus`), minimum Home Assistant version (`2025.3.0`), and configuration details (`config_flow: true`, `iot_class: local_polling`).
- **const.py**: Defines constants used throughout the integration, including the domain name (`DOMAIN`), default values for host/port/slave ID, available firmware versions (`FIRMWARE_VERSION`), and especially the templates for dynamic Modbus sensors (`HP_SENSOR_TEMPLATES`, `BOIL_SENSOR_TEMPLATES`, `HC_SENSOR_TEMPLATES`) and their base addresses. The number of instances (heat pumps, boilers, heating circuits) is configured via `num_hps`, `num_boil`, `num_hc`.
- **__init__.py**: Initializes the integration, sets up the central `LambdaDataUpdateCoordinator`, loads the sensor and climate platforms, and registers a listener for configuration changes to reload the integration if needed.
- **config_flow.py**: Implements the configuration flow for setting up the integration via the Home Assistant UI (`LambdaConfigFlow`) and the options flow for adjusting settings after setup (`LambdaOptionsFlow`). The number of instances for HP, Boiler, and HC can be selected during setup.
- **sensor.py**: Defines the sensor platform. The `async_setup_entry` function dynamically creates sensor entities for each configured instance (HP, Boiler, HC) and each template. Firmware compatibility is checked. The `LambdaSensor` class represents a single sensor and fetches its data from the coordinator.
- **climate.py**: Defines the climate platform. For each Boiler and HC instance, a separate climate entity is dynamically created, referencing the appropriate dynamic sensors. The target temperature can be set via the climate entity.
- **coordinator.py**: Contains the `LambdaDataUpdateCoordinator` class, which cyclically reads all configured and compatible sensors (HP, Boiler, HC) and provides the values for the entities.

## Dynamic Sensor and Climate Generation

- The number of heat pumps (`num_hps`), boilers (`num_boil`), and heating circuits (`num_hc`) is set during setup.
- For each instance and each template, sensors are dynamically created (e.g., `hp1_flow_line_temperature`, `boil2_actual_high_temperature`, `hc1_room_device_temperature`).
- Climate entities for hot water and heating circuit are also dynamically created per instance (e.g., `climate.hot_water_1`, `climate.heating_circuit_2`).
- The firmware version is considered: sensors/entities are only created if they are compatible with the selected firmware.
- If the number of boilers or heating circuits is set to 0, no corresponding entities are created.

## Workflow

1. **Setup (`async_setup_entry` in `__init__.py`)**:
    * When the integration is added via the UI, `async_setup_entry` is called.
    * A `LambdaDataUpdateCoordinator` is created.
    * The coordinator attempts the first data update (`async_refresh()`).
    * The coordinator's data is stored in the `hass.data` dictionary.
    * The sensor and climate platforms (`sensor.py`, `climate.py`) are loaded (`async_forward_entry_setups`).
    * An update listener (`async_reload_entry`) is registered to react to configuration changes.

2. **Platform Setup (`async_setup_entry` in `sensor.py` & `climate.py`)**:
    * Each platform gets the coordinator from `hass.data`.
    * The configured firmware version and instance counts are read from `entry.data`.
    * For each instance and template, sensors and climate entities are dynamically created if compatible with the firmware.
    * All created entities are added to Home Assistant via `async_add_entities`.

3. **Data Update (`_async_update_data` in `LambdaDataUpdateCoordinator`)**:
    * This method is called periodically (according to `SCAN_INTERVAL`).
    * Connects to the Modbus device if not already connected.
    * Reads Modbus registers for each configured instance (HP, Boiler, HC) and each template.
    * Processes raw data based on data type (`int16`, `int32`) and scaling (`scale`).
    * Stores the processed values in a dictionary.
    * Returns the data dictionary. Home Assistant then notifies all dependent entities of the new data.

4. **Configuration Flow (`config_flow.py`)**:
    * **`LambdaConfigFlow`**: Called when the integration is added.
        * `async_step_user`: Shows the initial form (name, host, port, slave ID, debug mode, firmware version, number of HP/Boiler/HC). Firmware options are generated from `FIRMWARE_VERSION`. After input, data is validated and a config entry is created (`async_create_entry`).
    * **`LambdaOptionsFlow`**: Called when the user edits integration options.
        * `async_step_init`: Shows the options form (temperature ranges, update interval, firmware version). The number of instances cannot be changed afterwards.

5. **Reload on Configuration Change (`async_reload_entry` in `__init__.py`)**:
    * The listener registered in `async_setup_entry` calls this function when config entry data changes (e.g., via the options flow).
    * Unloads the platforms (`async_unload_platforms`).
    * Closes the Modbus connection.
    * Calls `async_setup_entry` again to reinitialize the integration with the new settings.

## Classes and Methods

* **LambdaDataUpdateCoordinator (`coordinator.py`)**
    * `__init__(hass, entry)`: Initializes the coordinator, stores the config entry, and sets the Modbus client to `None`. Passes `config_entry` to the superclass.
    * `_async_update_data()`: Main data-fetching method. Connects, reads all relevant Modbus registers for all configured instances and templates, processes the data, and returns it. Implements error handling for Modbus communication.

* **LambdaConfigFlow (`config_flow.py`)**
    * `async_step_user(user_input)`: Handles the initial setup step. Shows the form and creates the config entry.

* **LambdaOptionsFlow (`config_flow.py`)**
    * `async_step_init(user_input)`: Handles the options flow. Shows the form. Updates the main data (`config_entry.data`) if the firmware version changes and saves the remaining options.

* **LambdaSensor (`sensor.py`)**
    * `__init__(coordinator, entry, sensor_id, sensor_config)`: Initializes the sensor entity. Stores configuration, sets attributes like name, `unique_id`, unit, `device_class`, `state_class`, and precision based on the template.
    * `native_value`: Property that fetches the current value from the coordinator. Scaling is already applied in the coordinator.

* **LambdaClimateEntity (`climate.py`)**
    * `__init__(coordinator, entry, climate_type, translation_key, current_temp_sensor, target_temp_sensor, min_temp, max_temp, temp_step)`: Initializes the climate entity. Stores type, names of required temperature sensors, and temperature limits. Sets attributes like name, `unique_id`, temperature unit, supported features, and HVAC modes.
    * `current_temperature`: Property that fetches the value of `current_temp_sensor` from the coordinator.
    * `target_temperature`: Property that fetches the value of `target_temp_sensor` from the coordinator.
    * `async_set_temperature(**kwargs)`: Method to set the target temperature. Gets the sensor definition from the appropriate template, calculates the raw value for Modbus, writes the value via the coordinator's Modbus client, and updates the local coordinator cache and HA state.

---

This documentation describes the current, dynamic architecture of the integration (as of April 2025).
