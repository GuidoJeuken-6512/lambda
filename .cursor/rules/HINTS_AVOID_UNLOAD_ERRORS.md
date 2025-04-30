# Hinweise: Fehler beim Entladen von Home Assistant Integrationen vermeiden

**Best Practices für async_unload_entry in custom_components:**

- Vor dem Entfernen eines Eintrags aus `hass.data[DOMAIN]` immer prüfen, ob der Key existiert:
  ```python
  if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
      hass.data[DOMAIN].pop(entry.entry_id)
  else:
      _LOGGER.debug("Entry %s not in hass.data[%s], nothing to remove.", entry.entry_id, DOMAIN)
  ```

- ValueError beim Entladen von Plattformen (z.B. sensor, climate) abfangen:
  ```python
  try:
      unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "climate"])
  except ValueError as ex:
      _LOGGER.debug("Platform was not loaded or already unloaded: %s", ex)
      unload_ok = True
  ```

- Fehler beim Unload immer sauber loggen, nicht crashen lassen.

**Hintergrund:**
Diese Fehler entstehen, wenn Home Assistant versucht, einen Config Entry zu entladen, der nie vollständig geladen wurde oder schon entfernt ist. Die oben genannten Maßnahmen machen das Entladen robust und verhindern störende Fehler im Log.
