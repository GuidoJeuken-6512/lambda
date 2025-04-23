# Lambda Wärmepumpe Integration für Home Assistant / Lambda Heat Pump Integration for Home Assistant

---

## Deutsch

Diese benutzerdefinierte Integration ermöglicht die Einbindung von Lambda Wärmepumpen in Home Assistant über das Modbus/TCP Protokoll. Sie liest Sensordaten aus und ermöglicht die Steuerung von Klima-Entitäten (z.B. Warmwasser, Heizkreis).

**Features:**
- Auslesen diverser Sensoren der Wärmepumpe (Temperaturen, Zustände, Energieverbrauch etc.)
- Steuerung der Zieltemperatur für Warmwasser und Heizkreise über `climate`-Entitäten
- Dynamische Anpassung der Sensoren und Entitäten basierend auf der Firmware-Version und der konfigurierten Anzahl von Wärmepumpen, Boilern und Heizkreisen
- Konfigurierbarer Update-Intervall
- Konfiguration über die Home Assistant UI (Integrations)

**Installation:**
1. Kopieren Sie den gesamten Ordner `lambda` in Ihren `custom_components` Ordner innerhalb Ihres Home Assistant Konfigurationsverzeichnisses.
2. Starten Sie Home Assistant neu.

**Konfiguration:**
- Integration über die Home Assistant UI hinzufügen (`Einstellungen` → `Geräte & Dienste` → `Integration hinzufügen` → "Lambda WP")
- Geben Sie Name, Host, Port, Slave ID, Firmware-Version und die Anzahl der Wärmepumpen, Boiler und Heizkreise an
- Nach der Einrichtung können Temperaturbereiche und Update-Intervall über die Optionen angepasst werden

**Bekannte Probleme / TODO:**
- Die Übersetzung in andere Sprachen

---

## English

This custom integration allows you to connect Lambda heat pumps to Home Assistant via the Modbus/TCP protocol. It reads sensor data and enables control of climate entities (e.g., hot water, heating circuit).

**Features:**
- Reads various heat pump sensors (temperatures, states, energy consumption, etc.)
- Control of target temperature for hot water and heating circuits via `climate` entities
- Dynamic adaptation of sensors and entities based on firmware version and configured number of heat pumps, boilers, and heating circuits
- Configurable update interval
- Configuration via the Home Assistant UI (Integrations)

**Installation:**
1. Copy the entire `lambda` folder into your `custom_components` directory inside your Home Assistant configuration folder.
2. Restart Home Assistant.

**Configuration:**
- Add the integration via the Home Assistant UI (`Settings` → `Devices & Services` → `Add Integration` → "Lambda WP")
- Enter name, host, port, slave ID, firmware version, and the number of heat pumps, boilers, and heating circuits
- After setup, temperature ranges and update interval can be adjusted via the options

**Known Issues / TODO:**
- Translation to other languages

---

*Diese Integration wird nicht offiziell von Lambda unterstützt. / This integration is not officially supported by Lambda.*
