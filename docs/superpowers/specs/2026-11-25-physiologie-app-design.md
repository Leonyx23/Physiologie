# Physiologie-App – Entwurf (25.11.2026)

## Wozu
Lern-App für Physiologie (Physiotherapie-Ausbildung), zum Lernen für die Razzien. Die Nutzerin teilt sie mit
anderen und gibt jede Aktualisierung der Inhalte an alle weiter. Weitere Themen kommen nach und nach dazu.
Vorbild in Stil und Bedienung: ihr Muskelatlas (github.com/Leonyx23/muskelatlas).

## Ziele
- **Erklären:** je Thema eine Lernseite, geschrieben aus ihren Unterlagen, im Lernformat der Muskelatlas-Organseiten:
  Stichpunkte („Begriff: …“ fett), Unterpunkte, Tabellen, Ablaufketten, Balkenvergleiche, Schichtbilder,
  Merke-Kästen. Kein Fließtext.
- **Fragen:** ihre Fragensammlungen (zuerst „Razzia 2“) mit Antworten. Nachlesen mit „Antippen zum Aufdecken“
  und Abfragen (zufällige Reihenfolge, „gewusst / nochmal“, Fortschritt je Gerät gespeichert).
  Jede Antwort hat eine Quelle (Datei + Seite). Neue Fragen schickt sie im Chat, Claude beantwortet sie aus den
  Unterlagen und baut sie ein.
- **Korrekturen sichtbar:** Fehler in ihren Vorlagen (z. B. „anaerobe Glykolyse: 2 ADP“ → 2 ATP) werden anhand der
  Unterlagen berichtigt und in der App markiert (was geändert wurde, warum).
- **Teilen und Updates:** passwortgeschützte GitHub-Pages-Seite, als App auf Handy/Tablet installierbar. Neue
  Version kommt bei allen beim nächsten Öffnen an. Reiter „Neu“ mit rotem Punkt zeigt die Änderungen.
- **Suche** über alle Lernseiten und Fragen.

## Nicht dabei
- Keine KI-Antworten in der App (Weg 2 gewählt: feste Antworten, damit es für alle gleich funktioniert).
- Keine PDFs der Unterlagen in der App, keine aus den PDFs kopierten Abbildungen (Schaubilder werden aus Daten
  gezeichnet).
- Keine Konten, kein Abgleich des Lernfortschritts zwischen Personen.

## Was es zum Misserfolg machen würde
- Falsche Fakten oder Antworten, die sich nicht auf die Unterlagen zurückführen lassen.
- Lesbare Kursinhalte im öffentlichen Repository.
- Textwände statt Lernformat.

## Feste Regeln (von der Nutzerin)
- Jede neue Version zuerst als Vorschau zeigen. Hochladen erst nach ihrem ausdrücklichen OK.
- Passwort bei ihr erfragen, nie in Dateien, Notizen oder Commits speichern.
- In kleinen Schritten arbeiten und nach jedem Schritt speichern (Nutzungslimit).

## Wege (besprochen)
1. Claude antwortet live aus den Unterlagen (nur in der Claude-Version möglich, auf GitHub nur Stellensuche).
   Verworfen: die anderen sehen die Seite über GitHub, dort gäbe es keine Antworten.
2. **Feste Antworten, die Claude aus den Unterlagen schreibt und einbaut. Gewählt**, weil die App geteilt wird und
   für alle gleich funktionieren muss.
3. GitHub-Seite mit eigenem API-Schlüssel. Verworfen: kostet pro Frage, Schlüssel wäre für alle mit Passwort
   auslesbar.

## Umsetzung (Entscheidungen von Claude, die Nutzerin kann widersprechen)
- **Eine HTML-Datei** wie der Muskelatlas (ohne Framework), hell/dunkel, ab 360 px Breite bedienbar.
- **Inhalte als Daten:** je Thema eine Quelldatei (Lernseite + Fragen + Quellen), ein Build-Skript erzeugt daraus
  die App. Der Lader prüft Felder, Quellenangaben und Schaubild-Daten.
- **Verschlüsselung** wie beim Muskelatlas (PBKDF2-SHA256 600 000 Runden, AES-GCM, Anmeldeseite mit
  „angemeldet bleiben“). Das Repository ist öffentlich, deshalb liegen dort nur: verschlüsselte `index.html`,
  `sw.js`, Manifest, Icons, README, dieser Entwurf und die **Quellen als verschlüsseltes Archiv** (gleiches
  Passwort). So kann jede spätere Sitzung mit dem Passwort neu bauen, nichts hängt an einem Container.
- **Updates:** Service Worker lädt `index.html` zuerst aus dem Netz (offline aus dem Speicher). Neue Version →
  Hinweis „Neue Version da“ und Eintrag im Reiter „Neu“.
- **Reiter:** Lernen (Themen → Lernseite) · Fragen (nach Razzia und Thema) · Abfragen · Suche · Neu.
- **Reihenfolge:** zuerst 2. Razzia (Fragen „Razzia 2“, Lungenphysiologie, Muskel und Training) und
  MK (Herz-Kreislauf, Exkurs 5). „Stoff 1. Razzia“ folgt, sobald die Nutzerin die GoodNotes-Dateien als PDF
  schickt.

## Für später offen (fragen, wenn es so weit ist)
- Passwort: dasselbe wie beim Muskelatlas oder ein eigenes (beim ersten Hochladen fragen).
- Gibt es für die 1. Razzia auch eine Fragensammlung?
- GitHub Pages im Repository einschalten (Claude versucht es, sonst macht es die Nutzerin in den Einstellungen).
