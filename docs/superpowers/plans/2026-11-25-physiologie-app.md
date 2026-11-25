# Physiologie-App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Passwortgeschützte Lern-App (eine HTML-Datei) mit Lernseiten und Fragen samt Antworten aus den Unterlagen der Nutzerin.

**Architecture:** Inhalte als Python-Daten in `src/inhalt/`, `src/build.py` prüft sie und bettet sie als JSON in eine HTML-Hülle (`src/app/`) ein. Für GitHub wird das Ergebnis mit `protect.mjs` verschlüsselt. Die Quellen kommen als verschlüsseltes Archiv `quelle.enc` ins Repository, `src/` selbst nie im Klartext.

**Tech Stack:** Python 3.13 (Build, pytest), Vanilla JS/CSS, Node 22 (WebCrypto), Playwright (Smoke-Tests), pdftotext/pdftoppm (Unterlagen lesen).

**Spec:** `docs/superpowers/specs/2026-11-25-physiologie-app-design.md`

## Global Constraints
- Nichts hochladen/pushen ohne ausdrückliches OK der Nutzerin; zuerst Vorschau (`build/Physiologie - Vorschau.html`) im Chat.
- Passwort nie speichern (nur `MA_PW` als Umgebungsvariable beim Aufruf).
- `src/` und `build/` stehen in `.gitignore`; im Repo nur verschlüsselte Inhalte.
- Gleiche Domain wie Muskelatlas (leonyx23.github.io): localStorage-Schlüssel nur mit Präfix `physiologie.`, Cache-Namen nur mit Präfix `physiologie-`, Service Worker löscht nur eigene Caches.
- Lernformat: keine Fließtexte; Abschnittsschlüssel `h, li, tb, tc, fl, br, ly, m`; `**…**` = fett, sonst alles als Text (kein HTML aus Daten).
- Jede Antwort hat mindestens eine Quelle `(Kürzel, Seite)`; Seite muss in der PDF existieren.
- Bedienbar ab 360 px, hell/dunkel, keine Konsolenfehler.
- Nach jedem Task lokal committen (`git add` nur Repo-Dateien, nie `src/`).

## Review Focus
- Sehr lange Antworten/Tabellen auf 360 px: kein waagerechtes Scrollen der Seite (Tabellen scrollen in sich) → smoke prüft `scrollWidth <= innerWidth`.
- Suche mit Umlauten/Groß-Klein/„ß“ und Sonderzeichen wie `(`: findet „Glykolyse“ bei „glykolyse“, wirft nie → smoke sucht `Säure`, `atp`, `(`.
- Abfragen ohne Fragen in der Auswahl oder nach dem letzten Kärtchen: klare Meldung statt Leere → smoke.
- localStorage nicht verfügbar (privates Fenster): App läuft trotzdem → Zugriffe in try/catch, smoke mit kaputtem localStorage.
- Direkter Aufruf eines alten/ungültigen Hash-Links (`#/lernen/gibtsnicht`): zurück zur Übersicht statt Fehler → smoke.

---

### Task 1: Inhaltsformat, Prüfung und Build
**Files:** Create `src/build.py`, `src/inhalt/quellen.py`, `src/inhalt/neu.py`, `src/inhalt/t_beispiel.py` (nur Test-Fixture unter `src/tests/fixtures/`), `src/tests/test_build.py`, `.gitignore`.

**Interfaces – Produces:**
- Themen-Datei `src/inhalt/thema_<id>.py` mit `THEMA = dict(id, titel, bereich, razzia:int, lern=[Abschnitt])`.
- Fragen-Datei `src/inhalt/fragen_<id>.py` mit `FRAGEN = dict(id, titel, razzia:int, fragen=[dict(id, thema, f, a=[Abschnitt], q=[(kürzel, seite)], korr=[str]?)])`.
- `QUELLEN = {kürzel: dict(t=Titel, datei=Pfad relativ zum Unterlagen-Ordner, seiten=int)}`; `NEU = [dict(id, datum, titel, punkte=[str])]` (neueste zuerst).
- `load(src_dir) -> dict(themen, fragensets, quellen, neu)`; `validate(data) -> list[str]`; `build(src_dir, out_dir) -> Path` schreibt `vorschau.html` und `pwa_plain.html`.

- [ ] Test: `test_validate_ok` (Fixture ohne Fehler), `test_unknown_key` (`dict(h='x', zz=1)` → Fehler nennt `zz`), `test_bad_source` (Kürzel fehlt / Seite > seiten), `test_dup_id`, `test_table_width` (Zeile kürzer als Kopf), `test_frage_without_source`, `test_build_embeds_json` (`</script>` im Text wird zu `</script>`).
- [ ] Fehlschlag prüfen: `cd src && python3 -m pytest tests -q` → FAIL.
- [ ] `build.py` schreiben (Module per `importlib` laden; Daten-JSON in `<script id="data" type="application/json">`; App-Dateien `app/shell.html` mit Platzhaltern `/*CSS*/`, `/*JS*/`, `__DATA__`).
- [ ] Tests grün. Commit `.gitignore` + Plan.

### Task 2: App-Oberfläche
**Files:** Create `src/app/shell.html`, `src/app/style.css`, `src/app/app.js`, `src/tests/smoke.py`.
**Interfaces – Consumes:** Daten-JSON aus Task 1. **Produces:** Hash-Routen `#/lernen`, `#/lernen/<thema>`, `#/fragen`, `#/fragen/<set>`, `#/abfragen`, `#/suche?q=`, `#/neu`; localStorage `physiologie.stand` (`{frageId:{ok:int,nochmal:int,t:int}}`), `physiologie.neu` (zuletzt gesehene NEU-id).
- [ ] smoke.py (Playwright, Fixture-Build): je 360/430/1100 px hell+dunkel: alle Reiter, jede Lernseite, jede Frage aufdecken, „Alle aufdecken“, Abfragen 3 Kärtchen (gewusst/nochmal) bis Ende, Suche `atp`/`Säure`/`(`, ungültiger Hash, localStorage kaputt; keine Konsolenfehler; `scrollWidth <= innerWidth`.
- [ ] Renderer für `h, li (Unterpunkte), tb (breit → Karten ≤ 560 px), tc, fl (Pfeilkette, loop), br (Balken, Wert/Anzeige), ly (Schichten), m (Merke)`; Quellenzeile „Quelle: Titel, S. n“; Korrektur-Kasten „✎ Korrigiert“.
- [ ] Fragen: verdeckt bis Antippen, „Alle aufdecken/verdecken“; Lernseite verlinkt ihre Fragen, Frage verlinkt ihr Thema.
- [ ] Abfragen: Auswahl Razzia/Thema, Reihenfolge gemischt, „Nochmal“ kommt am Ende wieder, Zusammenfassung, Fortschritt je Frage.
- [ ] Suche (normalisiert: klein, ä→a usw., ß→ss) über Titel, Lernseiten, Fragen und Antworten; Treffer mit Ausschnitt.
- [ ] Neu-Reiter mit rotem Punkt. smoke grün, Commit.

### Task 3: Fragen „Razzia 2“
**Files:** Create `src/inhalt/quellen.py` (echte Unterlagen), `src/inhalt/fragen_razzia2.py`.
- [ ] Razzia 2.pdf vollständig lesen; jede Frage übernehmen, Antwort im Lernformat aus den Unterlagen prüfen/ergänzen, Quellen mit Seitenzahlen, Fehler korrigieren und in `korr` begründen.
- [ ] `pytest` + smoke grün, Vorschau bauen, Commit (nur Repo-Dateien).

### Task 4: Lernseiten 2. Razzia
**Files:** `src/inhalt/thema_*.py` für Energiestoffwechsel/Leistungsphysiologie, Lungenphysiologie, Muskel und Training.
- [ ] Unterlagen (Text + Bildseiten per `pdftoppm` ansehen) durcharbeiten, Lernseiten mit Schaubildern, Quellen je Abschnitt.
- [ ] Tests grün, Vorschau → **Pause, Vorschau an Nutzerin**.

### Task 5: Lernseiten MK
**Files:** `src/inhalt/thema_*.py` Herz-Kreislauf-Physiologie, Exkurs 5.
- [ ] wie Task 4. Vorschau → Pause.

### Task 6: Verpacken und Hochladen (erst nach OK)
**Files:** Create `src/gate.html`, `src/protect.mjs` (aus Muskelatlas-Doc, Speicher `physiologie.zugang`, Titel „Physiologie“), `src/seal.mjs` (`enc|dec` für `quelle.enc`), `src/publish.sh`, `src/icons.py`; Repo: `index.html`, `sw.js` (Cache `physiologie-v1`, Netz zuerst für Navigation), `manifest.webmanifest`, `icon-180/192/512.png`, `quelle.enc`, `README.md`.
- [ ] Passwort erfragen; protect; Klartext-grep (z. B. „Glykolyse“ darf nicht in index.html/quelle.enc stehen); Login per Playwright; `seal.mjs dec` ergibt identisches Archiv.
- [ ] Nach OK: push, GitHub Pages einschalten (`gh api` oder Nutzerin), Live-Seite prüfen, Projekt-Doc aktualisieren.
