## Lambda Heat Pump Integration - Dokumentation

### Aufbau der Integration

Die Integration besteht aus folgenden Hauptdateien:

-   **`manifest.json`**: Enthält Metadaten zur Integration wie Name, Version, Abhängigkeiten (`pymodbus`), Home Assistant Mindestversion (`2025.3.0`) und Konfigurationsdetails (`config_flow: true`, `iot_class: local_polling`).
-   **`const.py`**: Definiert Konstanten, die in der gesamten Integration verwendet werden. Dazu gehören der Domain-Name (`DOMAIN`), Standardwerte für Host/Port/Slave ID, verfügbare Firmware-Versionen (`FIRMWARE_VERSION`) und vor allem die Definitionen aller Modbus-Register (`SENSOR_TYPES`). Jeder Sensor ist hier mit Adresse, Name, Einheit, Skalierung, Präzision, Datentyp und minimaler Firmware-Version definiert.
-   **`__init__.py`**: Initialisiert die Integration, richtet den zentralen `LambdaDataUpdateCoordinator` ein, lädt die Sensor- und Klima-Plattformen und registriert einen Listener für Konfigurationsänderungen, um die Integration bei Bedarf neu zu laden.
-   **`config_flow.py`**: Implementiert den Konfigurationsfluss für die Einrichtung der Integration über die Home Assistant Benutzeroberfläche (`LambdaConfigFlow`) und den Optionsfluss für die Anpassung von Einstellungen nach der Einrichtung (`LambdaOptionsFlow`).
-   **`sensor.py`**: Definiert die Sensor-Plattform. Die `async_setup_entry` Funktion filtert Sensoren basierend auf der ausgewählten Firmware-Version und erstellt `LambdaSensor`-Instanzen. Die `LambdaSensor`-Klasse repräsentiert einen einzelnen Sensor und holt seine Daten vom Coordinator.
-   **`climate.py`**: Definiert die Klima-Plattform. Ähnlich wie `sensor.py` filtert die `async_setup_entry` Funktion die Klima-Entitäten basierend auf der Verfügbarkeit der benötigten Temperatursensoren für die ausgewählte Firmware-Version. Die `LambdaClimateEntity`-Klasse repräsentiert eine Klima-Entität (Heizkreis, Warmwasser) und interagiert mit dem Coordinator, um Temperaturen zu lesen und zu setzen.

### Ablauf

1.  **Einrichtung (`async_setup_entry` in `__init__.py`)**:
    *   Beim Hinzufügen der Integration über die UI wird `async_setup_entry` aufgerufen.
    *   Ein `LambdaDataUpdateCoordinator` wird erstellt.
    *   Der Coordinator versucht, die erste Datenaktualisierung (`async_refresh()`) durchzuführen.
    *   Die Daten des Coordinators werden im `hass.data` Dictionary gespeichert.
    *   Die Sensor- und Klima-Plattformen (`sensor.py`, `climate.py`) werden geladen (`async_forward_entry_setups`).
    *   Ein Update-Listener (`async_reload_entry`) wird registriert, um auf Änderungen in der Konfiguration zu reagieren.

2.  **Plattform-Setup (`async_setup_entry` in `sensor.py` & `climate.py`)**:
    *   Jede Plattform holt sich den Coordinator aus `hass.data`.
    *   Die konfigurierte Firmware-Version wird aus `entry.data` gelesen.
    *   `sensor.py`: Iteriert durch `SENSOR_TYPES` in `const.py`. Für jeden Sensor wird geprüft, ob seine `firmware_version` kleiner oder gleich der konfigurierten Version ist. Wenn ja, wird eine `LambdaSensor`-Instanz erstellt.
    *   `climate.py`: Prüft für jede Klima-Entität (Warmwasser, Heizkreis), ob die benötigten `current_temp_sensor` und `target_temp_sensor` für die konfigurierte Firmware-Version verfügbar sind (mithilfe der `is_sensor_compatible` Funktion). Wenn ja, wird eine `LambdaClimateEntity`-Instanz erstellt.
    *   Alle erstellten Entitäten werden über `async_add_entities` zu Home Assistant hinzugefügt.

3.  **Datenaktualisierung (`_async_update_data` in `LambdaDataUpdateCoordinator`)**:
    *   Der Coordinator ruft diese Methode periodisch auf (gemäß `SCAN_INTERVAL`).
    *   Stellt eine Verbindung zum Modbus-Gerät her (falls nicht bereits verbunden).
    *   Iteriert durch `SENSOR_TYPES` in `const.py`.
    *   Überspringt Sensoren, deren Schlüssel "dummy" enthält.
    *   Liest die entsprechenden Modbus-Register (`read_holding_registers`).
    *   Verarbeitet die Rohdaten basierend auf Datentyp (`int16`, `int32`) und Skalierung (`scale`).
    *   Speichert die verarbeiteten Werte in einem Dictionary.
    *   Gibt das Daten-Dictionary zurück. Home Assistant benachrichtigt daraufhin alle abhängigen Entitäten über die neuen Daten.

4.  **Konfigurationsfluss (`config_flow.py`)**:
    *   **`LambdaConfigFlow`**: Wird beim Hinzufügen der Integration aufgerufen.
        *   `async_step_user`: Zeigt das erste Formular an (Name, Host, Port, Slave ID, Debug-Modus, Firmware-Version). Die Firmware-Optionen werden dynamisch aus `FIRMWARE_VERSION` in `const.py` generiert. Nach der Eingabe werden die Daten validiert und ein Config Entry erstellt (`async_create_entry`).
    *   **`LambdaOptionsFlow`**: Wird aufgerufen, wenn der Benutzer die Integrationsoptionen bearbeitet.
        *   `async_step_init`: Zeigt das Optionsformular an (Temperaturbereiche, Update-Intervall, Firmware-Version). Der Standardwert für die Firmware-Version wird aus den Hauptdaten (`config_entry.data`) gelesen. Bei der Bestätigung:
            *   Wenn die Firmware-Version geändert wurde, werden die Hauptdaten des Config Entry aktualisiert (`async_update_entry`) und die Firmware-Version aus den `user_input`-Daten entfernt, bevor der Options-Eintrag erstellt wird (`async_create_entry`).
            *   Andere Optionsänderungen werden direkt im Options-Eintrag gespeichert.

5.  **Neuladen bei Konfigurationsänderung (`async_reload_entry` in `__init__.py`)**:
    *   Der in `async_setup_entry` registrierte Listener ruft diese Funktion auf, wenn sich die Config Entry Daten ändern (z.B. durch den Options Flow).
    *   Entlädt die Plattformen (`async_unload_platforms`).
    *   Schließt die Modbus-Verbindung.
    *   Ruft `async_setup_entry` erneut auf, um die Integration mit den neuen Einstellungen neu zu initialisieren.

### Klassen und Methoden

*   **`LambdaDataUpdateCoordinator` (`__init__.py`)**
    *   `__init__(hass, entry)`: Initialisiert den Coordinator, speichert die Config Entry (`config_entry`) und setzt den Modbus-Client auf `None`. Übergibt `config_entry` an die Superklasse.
    *   `_async_update_data()`: Hauptmethode zur Datenabfrage. Stellt Verbindung her, liest alle relevanten Modbus-Register (überspringt Dummies), verarbeitet die Daten und gibt sie zurück. Implementiert Fehlerbehandlung für Modbus-Kommunikation.

*   **`LambdaConfigFlow` (`config_flow.py`)**
    *   `async_step_user(user_input)`: Handhabt den initialen Einrichtungsschritt. Zeigt das Formular an und erstellt den Config Entry.

*   **`LambdaOptionsFlow` (`config_flow.py`)**
    *   `async_step_init(user_input)`: Handhabt den Optionsfluss. Zeigt das Formular an. Aktualisiert die Hauptdaten (`config_entry.data`), wenn die Firmware-Version geändert wird, und speichert die restlichen Optionen.

*   **`LambdaSensor` (`sensor.py`)**
    *   `__init__(coordinator, entry, sensor_id, sensor_config)`: Initialisiert die Sensor-Entität. Speichert Konfiguration, setzt Attribute wie Name, `unique_id`, Einheit, `device_class`, `state_class` und Präzision basierend auf der `sensor_config` aus `const.py`.
    *   `native_value`: Property, die den aktuellen Wert des Sensors vom Coordinator holt und zurückgibt. Wendet die Skalierung aus der Konfiguration an.

*   **`LambdaClimateEntity` (`climate.py`)**
    *   `__init__(coordinator, entry, climate_type, name, current_temp_sensor, target_temp_sensor, min_temp, max_temp, temp_step)`: Initialisiert die Klima-Entität. Speichert Typ, Namen der benötigten Temperatursensoren und Temperatur-Grenzwerte. Setzt Attribute wie Name, `unique_id`, Temperatureinheit, unterstützte Features und HVAC-Modi.
    *   `current_temperature`: Property, die den Wert des `current_temp_sensor` vom Coordinator holt.
    *   `target_temperature`: Property, die den Wert des `target_temp_sensor` vom Coordinator holt.
    *   `async_set_temperature(**kwargs)`: Methode zum Setzen der Zieltemperatur. Holt die Sensor-Definition aus `SENSOR_TYPES`, berechnet den Rohwert für Modbus, schreibt den Wert über den Modbus-Client des Coordinators und aktualisiert den lokalen Coordinator-Cache sowie den HA-State.

Diese Dokumentation sollte einen guten Überblick über die Funktionsweise der Integration geben.
