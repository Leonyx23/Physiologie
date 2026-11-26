# Physiologie

Lern-App für Physiologie (Physiotherapie-Ausbildung): Lernseiten nach Abteilungen und die Razzia-Fragen mit
geprüften Antworten, Quellenangaben und Korrekturhinweisen. Läuft im Browser und lässt sich aufs Handy oder Tablet
legen („Zum Home-Bildschirm“); funktioniert nach dem ersten Öffnen auch offline.

**App:** https://leonyx23.github.io/Physiologie/

## Aufbau
- `inhalt/` – alle Inhalte als Python-Daten (Abteilungen, Lernseiten `thema_*.py`, Fragen `fragen_*.py`, Quellen, Neuigkeiten)
- `app/` – Oberfläche (HTML-Hülle, CSS, JavaScript)
- `tools/build.py` – prüft die Inhalte und baut `build/vorschau.html` und `build/pwa_plain.html`
- `tools/publish.py` – baut und legt das Ergebnis als `index.html` ab; `tools/icons.py` erzeugt die Icons
- `sw.js`, `manifest.webmanifest`, `icon-*.png` – Web-App (Cache-Präfix `physiologie-`, Speicher-Präfix `physiologie.`)
- `tests/` – `python3 -m pytest tests -q` (Build-Prüfung, Browser-Tests mit Playwright)
- `docs/superpowers/` – Entwurf und Bauplan

## Neue Version
1. Inhalte in `inhalt/` ändern, Eintrag in `inhalt/neu.py` ergänzen (neue `id` → roter Punkt bei „Neu“).
2. `python3 tools/publish.py` und `python3 -m pytest tests -q`.
3. Erst Vorschau zeigen, nach OK committen und pushen – GitHub Pages veröffentlicht automatisch.
