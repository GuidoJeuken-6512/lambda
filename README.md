# Lambda Wärmepumpe Integration für Home Assistant / Lambda Heat Pump Integration for Home Assistant


---

## Deutsch

## Branches
Im "main" Branch steht die Grundfunktionalität zur Verfügung. 
Im "subdevices" steht zudem die Möglichkeit zur Verfügung mehrer Untergeräte der Klassen HeatPump/Heating curcuit/Boiler/Buffer/Solar zu erzeugen und eine RaumThemostat Steuerung einzurichten.

Diese benutzerdefinierte Integration ermöglicht die Einbindung von Lambda Wärmepumpen in Home Assistant über das Modbus/TCP Protokoll. Sie liest Sensordaten aus und ermöglicht die Steuerung von Klima-Entitäten (z.B. Warmwasser, Heizkreis).

**Features:**
- Auslesen diverser Sensoren der Wärmepumpe (Temperaturen, Zustände, Energieverbrauch etc.)
- Steuerung der Zieltemperatur für Warmwasser und Heizkreise über `climate`-Entitäten
- Dynamische Anpassung der Sensoren und Entitäten basierend auf der Firmware-Version und der konfigurierten Anzahl von Wärmepumpen, Boilern, Heizkreisen, Pufferspeichern und Solarmodulen
- Zentrale, konsistente Filterung aller Sensoren/Entitäten nach Firmware-Version (utils.py)
- Raumthermostatsteuerung: Verwendung externer Temperatursensoren für jeden Heizkreis
- Konfigurierbarer Update-Intervall
- **Firmware-Version, Temperaturbereiche und Schritte sind jederzeit im Options-Dialog änderbar**
- **Debug-Logging beim Speichern der Konfiguration/Optionen**
- Konfiguration vollständig über die Home Assistant UI (Integrations)

**Installation:**
1. Kopieren Sie den gesamten Ordner `lambda` in Ihren `custom_components` Ordner innerhalb Ihres Home Assistant Konfigurationsverzeichnisses.
2. Starten Sie Home Assistant neu.

**Konfiguration:**
- Integration über die Home Assistant UI hinzufügen (`Einstellungen` → `Geräte & Dienste` → `Integration hinzufügen` → "Lambda WP")
- Geben Sie Name, Host, Port, Slave ID, Firmware-Version und die Anzahl der Wärmepumpen, Boiler, Heizkreise, Pufferspeicher und Solarmodule an
- Optional: Aktivieren Sie die Raumthermostatsteuerung, um externe Temperatursensoren für jeden Heizkreis zu verwenden
- Nach der Einrichtung können Temperaturbereiche, Firmware-Version und Update-Intervall **jederzeit** über die Optionen angepasst werden

**Raumthermostatsteuerung:**
- Ermöglicht die Verwendung eines externen Temperatursensors für jeden Heizkreis
- Der Sensorwert wird an die Lambda Wärmepumpe übermittelt und für die Regelung verwendet
- Aktivierung der Funktion in den Integrationseinstellungen
- Auswahl eines Temperatursensors pro Heizkreis

**Firmware- und Sensor-Handling:**
- Die Firmware-Version kann nachträglich im Options-Dialog geändert werden und triggert ein vollständiges Reload (inkl. Filterung der Sensoren)
- Sensoren und Entitäten werden **zentral** nach Firmware gefiltert (siehe `utils.py`)
- Initialwerte für Sensoren (z.B. Dummy) können in const.py gesetzt werden

**Hinweise für Home Assistant 2025.3:**
- Diese Integration ist vollständig kompatibel mit Home Assistant 2025.3
- Verwendet den neuen DataUpdateCoordinator für optimale Leistung
- Typisierung und async/await nach den neuesten Standards
- Verbesserte Fehlerbehandlung und Logging
- Moderne Konfigurations- und Options-Flows

**Debugging:**
- Beim Speichern der Konfiguration und Optionen werden die geschriebenen Werte im Home Assistant Log (DEBUG) ausgegeben

**Bekannte Probleme:**
- Die Übersetzung in andere Sprachen (außer Deutsch und Englisch)

---

## English

This custom integration allows you to connect Lambda heat pumps to Home Assistant via the Modbus/TCP protocol. It reads sensor data and enables control of climate entities (e.g., hot water, heating circuit).

## Branches
The basic functionality is available in the "main" branch. 
In the "subdevices" it is also possible to create several subdevices of the classes HeatPump/Heating circuit/Boiler/Buffer/Solar and to set up a room thermostat control.

**Features:**
- Reads various heat pump sensors (temperatures, states, energy consumption, etc.)
- Control of target temperature for hot water and heating circuits via `climate` entities
- Dynamic adaptation of sensors and entities based on firmware version and configured number of heat pumps, boilers, heating circuits, buffer tanks, and solar modules
- Central, consistent filtering of all sensors/entities by firmware version (utils.py)
- Room thermostat control: Use external temperature sensors for each heating circuit
- Configurable update interval
- **Firmware version, temperature ranges and steps can be changed at any time in the options dialog**
- **Debug logging when saving configuration/options**
- Configuration fully via the Home Assistant UI (Integrations)

**Installation:**
1. Copy the entire `lambda` folder into your `custom_components` directory inside your Home Assistant configuration folder.
2. Restart Home Assistant.

**Configuration:**
- Add the integration via the Home Assistant UI (`Settings` → `Devices & Services` → `Add Integration` → "Lambda WP")
- Enter name, host, port, slave ID, firmware version, and the number of heat pumps, boilers, heating circuits, buffer tanks, and solar modules
- Optional: Enable room thermostat control to use external temperature sensors for each heating circuit
- After setup, temperature ranges, firmware version and update interval can be **changed at any time** via the options

**Room Thermostat Control:**
- Allows using an external temperature sensor for each heating circuit
- The sensor value is sent to the Lambda heat pump and used for regulation
- Activation of this feature in the integration settings
- Selection of a temperature sensor per heating circuit

**Firmware and Sensor Handling:**
- The firmware version can be changed later in the options dialog and triggers a full reload (including filtering of sensors)
- Sensors and entities are **centrally** filtered by firmware (see `utils.py`)
- Initial values for sensors (e.g. dummy) can be set in const.py

**Notes for Home Assistant 2025.3:**
- This integration is fully compatible with Home Assistant 2025.3
- Uses the new DataUpdateCoordinator for optimal performance
- Typing and async/await according to the latest standards
- Improved error handling and logging
- Modern configuration and options flows

**Debugging:**
- When saving configuration and options, the written values are output to the Home Assistant log (DEBUG)

**Known Issues:**
- Translation to other languages (besides German and English)

---

*Diese Integration wird nicht offiziell von Lambda unterstützt. / This integration is not officially supported by Lambda.*

---

## Modbus Test-Tools (Server & Client)

Für Entwicklung und Test der Integration steht ein separates Repository mit Modbus-Testtools zur Verfügung:

**GitHub:** [https://github.com/GuidoJeuken-6512/modbus_tools](https://github.com/GuidoJeuken-6512/modbus_tools)

**Enthalten:**
- Ein einfacher Modbus TCP Server (`server.py`), der Register aus einer YAML-Datei bereitstellt (ideal zum Mocken der Wärmepumpe)
- Ein grafischer Modbus TCP Client (`modbus_client.py`) zum Testen und Debuggen von Registerzugriffen

**Kurzanleitung:**
1. Repository klonen: `git clone https://github.com/GuidoJeuken-6512/modbus_tools`
2. In das Verzeichnis wechseln: `cd modbus_tools`
3. Server starten: `python server.py` (Register werden aus `config/registers.yaml` geladen)
4. Client starten: `python modbus_client.py` (GUI zum Lesen/Schreiben von Registern)

Weitere Details und Konfigurationsmöglichkeiten finden sich im README des Repositories und in den jeweiligen Python-Dateien.

---
