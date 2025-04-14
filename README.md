# Lambda Wärmepumpe Integration für Home Assistant

Diese benutzerdefinierte Integration ermöglicht die Einbindung von Lambda Wärmepumpen in Home Assistant über das Modbus/TCP Protokoll. Sie liest Sensordaten aus und ermöglicht die Steuerung von Klima-Entitäten (z.B. Warmwasser, Heizkreis).

## Features

*   Auslesen diverser Sensoren der Wärmepumpe (Temperaturen, Zustände, Energieverbrauch etc.).
*   Steuerung der Zieltemperatur für Warmwasser und Heizkreise über `climate`-Entitäten.
*   Dynamische Anpassung der Sensoren basierend auf der Firmware-Version.
*   Konfigurierbarer Update-Intervall.
*   Konfiguration über die Home Assistant UI (Integrations).

## Installation

1.  **Kopieren der Dateien:**
    *   Kopieren Sie den gesamten Ordner `lambda` (mit allen enthaltenen Dateien wie `__init__.py`, `sensor.py`, `manifest.json` etc.) in Ihren `custom_components` Ordner innerhalb Ihres Home Assistant Konfigurationsverzeichnisses.
    *   Pfad: `<HA-Konfigurationsordner>/custom_components/lambda/`
    *   Falls der `custom_components` Ordner nicht existiert, erstellen Sie ihn bitte.

2.  **Neustart von Home Assistant:**
    *   Starten Sie Home Assistant neu, damit die neue Integration erkannt wird.

## Konfiguration

1.  **Integration hinzufügen:**
    *   Gehen Sie in Home Assistant zu `Einstellungen` -> `Geräte & Dienste`.
    *   Klicken Sie unten rechts auf `Integration hinzufügen`.
    *   Suchen Sie nach "Lambda WP" und wählen Sie die Integration aus.

2.  **Verbindungsdaten eingeben:**
    *   **Name:** Ein beliebiger Name für Ihre Wärmepumpe (z.B. "Lambda Wärmepumpe").
    *   **Host:** Die IP-Adresse Ihrer Lambda Wärmepumpe im Netzwerk (z.B. `192.168.1.100`).
    *   **Port:** Der Modbus/TCP Port (Standard ist `502`).
    *   **Slave ID:** Die Modbus Slave ID Ihrer Wärmepumpe (Standard ist `1`).
    *   **Firmware Version:** Wählen Sie die passende Firmware-Version Ihrer Wärmepumpe aus. Dies beeinflusst, welche Sensoren verfügbar sind.

3.  **Abschließen:**
    *   Klicken Sie auf `Senden`. Die Integration wird nun eingerichtet und die entsprechenden Entitäten (Sensoren, Klima) sollten in Home Assistant erscheinen.

## Optionen

Nach der Einrichtung können Sie einige Optionen über `Einstellungen` -> `Geräte & Dienste` -> `Lambda WP` -> `Konfigurieren` anpassen:

*   **Temperaturbereiche:** Minimale und maximale Zieltemperaturen für Warmwasser und Heizkreis.
*   **Update-Intervall:** Wie oft die Daten von der Wärmepumpe abgefragt werden (in Sekunden).
*   **Firmware Version:** Ändern der Firmware-Version (erfordert einen Neustart der Integration).

## Bekannte Probleme / TODO

*   Die dynamische Handhabung mehrerer Wärmepumpen, Heizkreise, Pufferspeicher ist noch in Arbeit (siehe `docs/todo.txt`).

---

*Diese Integration wird nicht offiziell von Lambda unterstützt.* 
