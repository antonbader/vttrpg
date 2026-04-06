# VTTRPGE (Virtual Tabletop RPG Engine)

Eine leichtgewichtige, webbasierte Engine für Pen & Paper Rollenspiele, entwickelt mit Python (Flask) und Flask-SocketIO.

## Features & Technische Details

### Hauptfunktionen
- **Kampagnen & Bibliotheken:** Verwalte Kampagnen, Abenteuer, Szenen und teile Token-Templates (Spieler, NPCs, Gegenstände) kampagnenübergreifend.
- **GM Engine (Spielleiter):**
  - Grid-System mit konfigurierbarer Größe, Offset, Farbe und Dicke sowie Grid-Snapping.
  - Upload und Verwaltung von Hintergrundbildern.
  - Drag & Drop von Templates.
  - Radierbarer "Nebel des Krieges" (Fog of War) und eine integrierte Paint-Funktion (Zeichnen-Ebene).
  - Übersichtliches Dashboard mit einklappbaren Menüs (Sidebar), deren Status über Sessions hinweg erhalten bleibt.
  - Drag & Drop zum Neuordnen von Kampagnen, Abenteuern und Szenen.
- **Spieler-Ansicht:** Spieler loggen sich mit ihrem Namen ein und können *nur* ihre eigenen Token bewegen (Namensabgleich zwischen Spieler- und Token-Name). Sie sehen den Nebel des Krieges komplett schwarz, bis der GM ihn aufdeckt.
- **Second Screen (`/display`):** Eine reine Viewer-Ansicht für einen zweiten Monitor oder Beamer (z.B. für einen Spieltisch vor Ort).
- **Warteraum-System:** Ist keine Szene durch den GM aktiv geschaltet, landen Spieler automatisch in einem Warteraum.
- **Mobile Support:** Touch-Steuerung für das Bewegen von Tokens auf Tablets und Smartphones.
- **Echtzeit-Synchronisation:** Alle Bewegungen, Grid-Änderungen, Zeichenebenen und Nebel-Aktualisierungen passieren in Echtzeit über WebSockets (Global Broadcast pro Szene).

### Technische Basis
- **Backend:** Python, Flask, Flask-SocketIO (WebSockets), Flask-SQLAlchemy.
- **Datenbank:** Lokale SQLite-Datenbank (`instance/ttrpg.db`).
- **Frontend / UI:** Tailwind CSS (Dark Theme), natives HTML5 (z.B. `<details>`/`<summary>`), SortableJS für Drag & Drop Listen, Cropper.js für das Zuschneiden von hochgeladenen Tokens.
- **Map / Renderer:** Eigenentwickelte HTML5 Canvas-Engine mit separaten Ebenen (`bgLayer`, `paintLayer`, `gridLayer`, `tokenLayer`, `fowLayer`, `uiLayer`) für sauberes Zoomen und Pannen.

## Konfiguration

Wichtige Einstellungen für den Betrieb der Anwendung können in der Datei `config.py` im Stammverzeichnis vorgenommen werden:

- `GM_PASSWORD`: Das Passwort, welches der Spielleiter benötigt, um sich in das GM-Dashboard einzuloggen. (Standard: `"gm"`)
- `SERVER_PORT`: Der Port, auf dem der lokale Webserver läuft. (Standard: `5000`)
- `HOST_URL`: Der Hostname oder die lokale IP-Adresse des Servers, welche genutzt wird, um absolute Links für Spieler und die Display-Ansicht auf der GM-Login-Seite zu generieren (z.B. `"localhost"` oder `"192.168.178.50"`).

## Datenhaltung & Backups

Da die Anwendung vollständig lokal läuft, ist die Sicherung deiner Daten sehr einfach. Alle relevanten Daten werden im Projektordner gespeichert:

- **Datenbank (`instance/ttrpg.db`):** Enthält alle Kampagnen, Abenteuer, Szenen-Daten, Token-Positionen und die Base64-codierten Daten für den Nebel des Krieges sowie Zeichnungen (Paint-Layer).
- **Bilder / Uploads (`uploads/`):**
  - `uploads/maps/`: Hier werden die hochgeladenen Hintergrundbilder der Szenen gespeichert.
  - `uploads/tokens/`: Hier liegen die Bilder für deine Token-Templates (inkl. zugeschnittener Versionen).

**Backup erstellen:**
Um ein vollständiges Backup deiner VTTRPG-Instanz zu erstellen, kopiere einfach den Ordner `instance/` und den Ordner `uploads/` an einen sicheren Ort.

*Hinweis:* Wenn du Templates oder Szenen-Hintergründe im GM-Dashboard löschst, werden auch die physischen Dateien im `uploads/`-Ordner gelöscht, sofern sie nicht anderweitig verwendet werden.

## Installation & Start

1. **Abhängigkeiten installieren:**
   Stelle sicher, dass Python 3 installiert ist. Installiere die benötigten Pakete:
   ```bash
   pip install -r requirements.txt
   ```

2. **Server starten:**
   Starte die Applikation:
   ```bash
   python app.py
   ```
   Der Server läuft nun lokal unter `http://127.0.0.0:5000` (abhängig vom eingestellten Port in der `config.py`).

3. **Zugriff im lokalen Netzwerk (WLAN):**
   Damit deine Spieler über ihre Smartphones oder Laptops beitreten können:
   - Finde die lokale IP-Adresse deines Host-Rechners heraus (z.B. `192.168.178.50`).
     - Windows: `ipconfig` im CMD
     - Mac/Linux: `ifconfig` oder `ip a` im Terminal
   - Deine Spieler öffnen den Browser und rufen auf: `http://<DEINE_IP>:5000/player`
   - Für den Beamer-Bildschirm rufst du auf: `http://<DEINE_IP>:5000/display`
