# VTTRPG (Virtual Tabletop RPG Engine)

Eine leichtgewichtige, webbasierte Engine für Pen & Paper Rollenspiele, entwickelt mit Python (Flask) und Flask-SocketIO.

## Features
- **Kampagnen & Bibliotheken:** Verwalte Kampagnen, Abenteuer, Szenen und teile Token-Templates (Spieler, NPCs, Gegenstände) zwischen ihnen.
- **GM Engine (Spielleiter):** Grid-System mit Snapping, Drag & Drop von Templates, Hintergrundbildern und einem radiierbaren "Nebel des Krieges" (Fog of War).
- **Spieler-Ansicht:** Spieler loggen sich mit ihrem Namen ein, können *nur* ihre eigenen Token bewegen (Name = Token-Name) und sehen den Nebel des Krieges komplett schwarz, bis der GM ihn aufdeckt.
- **Second Screen (`/display`):** Eine reine Viewer-Ansicht für einen zweiten Monitor oder Beamer (z.B. für einen Spieltisch).
- **Mobile Support:** Touch-Steuerung für das Bewegen von Tokens auf Tablets und Smartphones.
- **Echtzeit-Synchronisation:** Alle Bewegungen, Grid-Änderungen und Nebel-Aktualisierungen passieren in Echtzeit über WebSockets.

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
   Der Server läuft nun lokal unter `http://0.0.0.0:5000`.

3. **Zugriff im lokalen Netzwerk (WLAN):**
   Damit deine Spieler über ihre Smartphones oder Laptops beitreten können:
   - Finde die lokale IP-Adresse deines Host-Rechners heraus (z.B. `192.168.178.50`).
     - Windows: `ipconfig` im CMD
     - Mac/Linux: `ifconfig` oder `ip a` im Terminal
   - Deine Spieler öffnen den Browser und rufen auf: `http://<DEINE_IP>:5000/player`
   - Für den Beamer-Bildschirm rufst du auf: `http://<DEINE_IP>:5000/display`