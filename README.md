# VTTRPGE (Virtual Tabletop RPG Engine)

Eine leichtgewichtige, webbasierte Engine für Pen & Paper Rollenspiele, entwickelt mit Python (Flask) und Flask-SocketIO.

Sie ermöglicht es dir, Kampagnen zu erstellen, Karten (Maps) hochzuladen, Tokens (Spielfiguren, NPCs, Gegenstände) zu platzieren und in Echtzeit mit deinen Spielern zu interagieren. Mit Funktionen wie Nebel des Krieges (Fog of War), einer Zeichenfunktion (Paint) und mobiler Unterstützung bietet sie alles, was du für dein digitales Abenteuer benötigst.

Für eine vollständige und detaillierte Anleitung zur Nutzung (für Spielleiter und Spieler) sowie technische Details (Installation, Konfiguration, Backup) siehe bitte das **[BENUTZERHANDBUCH](BENUTZERHANDBUCH.md)**.

## Features & Technische Details im Überblick

### Hauptfunktionen
- **Kampagnen & Bibliotheken:** Verwalte Kampagnen, Abenteuer, Szenen und teile Token-Templates (Spieler, NPCs, Gegenstände) kampagnenübergreifend.
- **GM Engine (Spielleiter):**
  - Grid-System mit konfigurierbarer Größe, Offset, Farbe und Dicke sowie Grid-Snapping.
  - Upload und Verwaltung von Hintergrundbildern.
  - Drag & Drop von Templates.
  - Radierbarer "Nebel des Krieges" (Fog of War) und eine integrierte Paint-Funktion (Zeichnen-Ebene).
  - Übersichtliches Dashboard mit einklappbaren Menüs (Sidebar), deren Status über Sessions hinweg erhalten bleibt.
  - Drag & Drop zum Neuordnen von Kampagnen, Abenteuern und Szenen.
- **Spieler-Ansicht:** Spieler loggen sich mit ihrem Namen ein und können *nur* ihre eigenen Tokens bewegen (Namensabgleich zwischen Spieler- und Token-Name). Sie sehen den Nebel des Krieges komplett schwarz, bis der GM ihn aufdeckt.
- **Second Screen (`/display`):** Eine reine Viewer-Ansicht für einen zweiten Monitor oder Beamer (z.B. für einen Spieltisch vor Ort).
- **Warteraum-System:** Ist keine Szene durch den GM aktiv geschaltet, landen Spieler automatisch in einem Warteraum.
- **Mobile Support:** Touch-Steuerung für das Bewegen von Tokens auf Tablets und Smartphones.
- **Echtzeit-Synchronisation:** Alle Bewegungen, Grid-Änderungen, Zeichenebenen und Nebel-Aktualisierungen passieren in Echtzeit über WebSockets (Global Broadcast pro Szene).

### Technische Basis
- **Backend:** Python, Flask, Flask-SocketIO (WebSockets), Flask-SQLAlchemy.
- **Datenbank:** Lokale SQLite-Datenbank (`instance/ttrpg.db`).
- **Frontend / UI:** Tailwind CSS (Dark Theme), natives HTML5 (z.B. `<details>`/`<summary>`), SortableJS für Drag & Drop Listen, Cropper.js für das Zuschneiden von hochgeladenen Tokens.
- **Map / Renderer:** Eigenentwickelte HTML5 Canvas-Engine mit separaten Ebenen (`bgLayer`, `paintLayer`, `gridLayer`, `tokenLayer`, `fowLayer`, `uiLayer`) für sauberes Zoomen und Pannen.

---
**Hinweis:** Die Installationsanleitung, Konfiguration, Backup-Erstellung sowie ausführliche Erklärungen aller Funktionen findest du nun im **[BENUTZERHANDBUCH](BENUTZERHANDBUCH.md)**.
