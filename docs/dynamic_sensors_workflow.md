# Ablauf der Dynamischen Sensoren

## Initialisierung der Dynamischen Sensoren

1. **`async_setup_entry` in `__init__.py`**:
   - Diese Funktion wird aufgerufen, wenn die Integration in Home Assistant eingerichtet wird.
   - Sie initialisiert den `LambdaDataUpdateCoordinator`, der für das Abrufen der Daten verantwortlich ist.
   - Die Funktion ruft `async_refresh` auf, um die Daten sofort zu aktualisieren.

2. **`LambdaDataUpdateCoordinator` in `coordinator.py`**:
   - Diese Klasse erbt von `DataUpdateCoordinator` und verwaltet das Abrufen der Daten von den Modbus-Registrierungen.
   - Die Methode `_async_update_data` wird verwendet, um die Daten von den Sensoren abzurufen.

3. **`async_setup_entry` in `sensor.py`**:
   - Diese Funktion wird aufgerufen, um die Sensor-Entitäten in Home Assistant zu erstellen.
   - Sie erstellt Instanzen der `LambdaSensor`-Klasse für jeden dynamischen Sensor basierend auf der Konfiguration.

4. **`LambdaSensor` in `sensor.py`**:
   - Diese Klasse repräsentiert einen einzelnen Sensor in Home Assistant.
   - Sie erbt von `CoordinatorEntity` und `SensorEntity`, um die Sensor-Daten in der Benutzeroberfläche anzuzeigen.

## Update der Dynamischen Sensoren

1. **`_async_update_data` in `LambdaDataUpdateCoordinator`**:
   - Diese Methode wird regelmäßig aufgerufen, um die Daten von den Modbus-Registrierungen abzurufen.
   - Sie liest die Register für die dynamischen Sensoren basierend auf den in `HP_SENSOR_TEMPLATES` definierten Adressen.

2. **Modbus-Abfragen**:
   - Innerhalb von `_async_update_data` werden die Modbus-Register für jeden dynamischen Sensor abgefragt.
   - Die Ergebnisse werden skaliert und in einem Datenwörterbuch gespeichert, das von den Sensor-Entitäten verwendet wird.

3. **Sensor-Entitäten**:
   - Die `LambdaSensor`-Entitäten verwenden die aktualisierten Daten aus dem Koordinator, um ihre Zustände in der Home Assistant-Benutzeroberfläche zu aktualisieren. 