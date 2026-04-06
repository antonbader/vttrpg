# Benutzerhandbuch: VTTRPGE

Willkommen zum Virtual Tabletop RPG Engine (VTTRPGE) Benutzerhandbuch! Dieses Handbuch erklärt dir Schritt für Schritt, wie du das System als Spielleiter (GM) konfigurierst und bedienst, wie deine Spieler daran teilnehmen können, wie du ein separates Betrachtungsfenster (z.B. für einen Beamer) nutzt und wie die technische Einrichtung funktioniert.

---

## Inhaltsverzeichnis
1. [Spielleiter-Handbuch (GM Engine)](#1-spielleiter-handbuch-gm-engine)
2. [Spieler-Handbuch](#2-spieler-handbuch)
3. [Das Betrachtungsfenster (Display)](#3-das-betrachtungsfenster-display)
4. [Technischer Teil: Installation & Betrieb](#4-technischer-teil-installation--betrieb)

---

## 1. Spielleiter-Handbuch (GM Engine)

Als Spielleiter (Game Master / GM) hast du die volle Kontrolle über die Kampagnen, Abenteuer, Szenen und Tokens.

### 1.1 Login und Dashboard

**Der Login:**
1. Öffne den Browser und navigiere zu der dir bekannten Adresse (Standard lokal: `http://127.0.0.1:5000/gm/login`).
2. Du siehst eine Login-Seite. Gib das in der `config.py` festgelegte **GM Passwort** ein (Standard ist `gm`).
3. Klicke auf den Button **"Login"**.
4. Unter dem Login-Bereich findest du die direkten Links für deine Spieler (`/player`) und für das Display (`/display`), die du kopieren und teilen kannst.

**Das Dashboard:**
Nach dem Login befindest du dich auf der Hauptseite. Hier organisierst du deine Spielwelt hierarchisch:
- **Kampagnen:** Die oberste Ebene (z.B. "Fluch des Strahd").
- **Abenteuer:** Unterkapitel einer Kampagne (z.B. "Das Dorf Barovia").
- **Szenen:** Die eigentlichen Karten/Maps, auf denen gespielt wird (z.B. "Taverne zum blutigen Pfirsich").

### 1.2 Kampagnen, Abenteuer und Szenen verwalten

**Eine Kampagne erstellen:**
1. Im Dashboard siehst du ein Feld "Neue Kampagne".
2. Trage den **Namen** (und optional eine kurze Beschreibung) ein.
3. Klicke auf **"Erstellen"**. Die Kampagne erscheint in der Liste.

**Ein Abenteuer erstellen:**
1. Klappe die gewünschte Kampagne aus, indem du auf ihren Namen klickst.
2. Trage bei "Neues Abenteuer" einen Namen ein.
3. Klicke auf **"Hinzufügen"**. Das Abenteuer ist nun der Kampagne untergeordnet.

**Eine Szene erstellen:**
1. Klappe das entsprechende Abenteuer aus.
2. Trage bei "Neue Szene" einen Namen ein.
3. Klicke auf **"Hinzufügen"**. Die Szene wird erstellt.

**Verwalten & Sortieren:**
- Du kannst Kampagnen, Abenteuer und Szenen mit der Maus **per Drag & Drop** (anfassen und verschieben) neu anordnen.
- Jedes Element hat einen **Stift-Button** zum Umbenennen und einen **Mülleimer-Button** zum Löschen. *Achtung: Das Löschen einer Kampagne löscht auch alle enthaltenen Abenteuer und Szenen!*

### 1.3 Die Template-Bibliothek

Damit du nicht für jede Szene neue Tokens hochladen musst, gibt es die Template-Bibliothek pro Kampagne.
1. Klicke im Dashboard bei deiner Kampagne auf den Button **"Bibliothek öffnen"**.
2. **Neues Template anlegen:**
   - Gib einen **Namen** für das Token ein (z.B. "Ork Wache" oder "Spielername").
   - Wähle den **Typ** ("player", "npc" oder "item").
   - Wähle ein **Bild** von deiner Festplatte aus.
   - Klicke auf **"Erstellen"**.
3. **Zuschneiden (Cropping):** Bevor das Bild hochgeladen wird, öffnet sich oft ein Editor. Wähle den gewünschten quadratischen oder runden Ausschnitt aus, um perfekte Token-Bilder zu generieren.
4. Du kannst Templates auch über den Button **"Importieren"** aus anderen deiner Kampagnen kopieren.

### 1.4 Die Szenen-Ansicht (Die Map)

Wenn du bei einer Szene im Dashboard auf **"Als GM beitreten"** klickst, öffnet sich die Map-Ansicht. Diese ist dein wichtigstes Werkzeug während des Spiels.

**Aktivieren der Szene:**
Oben rechts in der Navigation findest du den Button **"Szene für Spieler aktivieren / deaktivieren"**.
- Nur eine einzige Szene kann im gesamten System aktiv sein.
- Spieler und das Display sehen immer nur die *aktive* Szene.
- Klickst du darauf, werden alle verbundenen Spieler sofort in diese Szene gezogen.

**Die Menüleiste (Sidebar links):**
Hier findest du alle Werkzeuge für die Szene. Die Menüs sind einklappbar.

#### Bereich: Karte & Hintergrund
1. Klicke auf **"Durchsuchen"**, um eine Map-Grafik (z.B. ein JPG oder PNG) hochzuladen.
2. Klicke auf **"Hintergrund hochladen"**. Das Bild erscheint auf der Arbeitsfläche.
3. Mit dem Button **"Hintergrund löschen"** entfernst du die Karte wieder (Tokens und Nebel werden dabei zurückgesetzt!).

#### Bereich: Grid Einstellungen (Das Raster)
Hier steuerst du das Gitternetz, über das sich die Tokens bewegen.
- **Größe:** Regelt die Größe der Kästchen in Pixeln.
- **Offset X / Y:** Verschiebt das Gitter nach links/rechts bzw. oben/unten, um es perfekt über das hochgeladene Hintergrundbild zu legen.
- **Farbe & Dicke:** Wähle eine Farbe (z.B. rot, schwarz, halb-transparent) und die Liniendicke.
- **An Raster ausrichten (Snap to Grid):** Ist das Häkchen gesetzt, springen Tokens beim Loslassen automatisch in die Mitte des nächsten Feldes. Ist es deaktiviert, kannst du sie völlig frei platzieren.
*Jede Änderung hier wird sofort (in Echtzeit) für alle Spieler sichtbar.*

#### Bereich: Tokens platzieren
Dieser Bereich zeigt alle Templates der Kampagne.
- **Am PC:** Klicke auf ein Template (z.B. einen Ork) und ziehe es mit gedrückter Maustaste auf die Karte (Drag & Drop).
- **Mobile Placement Mode (für Touch-Geräte):** Da Drag & Drop auf dem Tablet schwierig ist, klicke auf das **Handy-Icon** oben rechts (Mobile Placement Mode). Klicke nun im Menü einmal kurz auf das gewünschte Token-Template und danach einfach auf die gewünschte Stelle auf der Karte. Das Token erscheint dort.

#### Bereich: Tokens verwalten
Hier siehst du eine Liste aller Tokens, die sich aktuell auf der Karte befinden.
- Ein Klick auf den **Mülleimer** neben einem Token in der Liste löscht es von der Karte.

#### Bereich: Fog of War (Nebel des Krieges)
Hiermit verdeckst du die Karte für deine Spieler.
- Standardmäßig ist die Karte für Spieler komplett schwarz (verdeckt). Als GM siehst du die Karte leicht abgedunkelt.
- **Pinselgröße:** Stelle die Größe deines Werkzeugs ein.
- **"Nebel zeichnen" (Standard):** Klicke auf der Karte und ziehe die Maus, um Bereiche für die Spieler *sichtbar* zu machen (du radierst den Nebel weg).
- **"Nebel wiederherstellen" (Häkchen setzen):** Wenn du hier einen Haken setzt, malst du den Nebel wieder über aufgedeckte Bereiche (du verdeckst sie wieder).
- **Reset:** Der Button "Nebel komplett zurücksetzen" macht die Karte für Spieler wieder zu 100% schwarz.

#### Bereich: Paint (Zeichnen)
Ermöglicht es dir, frei auf der Karte zu malen (z.B. um Zonen, Pfeile oder Effekte zu markieren).
- Wähle eine **Farbe** und eine **Pinselgröße**.
- Setze das Häkchen bei **"Radiergummi"**, um Gezeichnetes wieder zu entfernen.
- Klicke auf **"Zeichnung löschen"**, um alles komplett wegzuwischen.
*Achtung: Während das Paint-Menü geöffnet ist (und du aktiv malst), können Tokens unter Umständen nicht bewegt werden.*

### 1.5 Navigation auf der Karte
- **Zoomen:** Nutze das Mausrad zum rein- und rauszoomen.
- **Bewegen (Pannen):** Halte die rechte Maustaste (oder das Mausrad) gedrückt und ziehe die Maus, um die Ansicht zu verschieben.
- **Auf Touch-Geräten:** Nutze zwei Finger zum Zoomen (Pinch-to-zoom) und zwei Finger zum Verschieben der Karte.

---

## 2. Spieler-Handbuch

Für Spieler ist das System sehr einfach und intuitiv gehalten.

### 2.1 Beitritt zum Spiel
1. Öffne den Link, den dir dein Spielleiter gegeben hat (z.B. `http://192.168.178.50:5000/player`).
2. Du siehst eine Startseite. Trage bei **"Dein Charaktername"** deinen Namen ein.
   *WICHTIG:* Dieser Name muss exakt mit dem Namen deines Tokens (welches der GM angelegt hat) übereinstimmen! Wenn der GM ein Token namens "Gimli" anlegt, musst du dich zwingend mit "Gimli" einloggen, sonst kannst du deine Spielfigur später nicht bewegen.
3. Klicke auf **"Beitreten"**.

### 2.2 Der Warteraum
Wenn der Spielleiter aktuell keine aktive Szene ausgewählt hat, landest du auf einem schwarzen Bildschirm mit der Meldung "Keine Szene aktiviert. Bitte warten...".
Du musst nichts weiter tun. Sobald der GM eine Szene aktiviert, lädt deine Ansicht automatisch und du siehst die Karte.

### 2.3 Spielen auf der Karte
Sobald du in der Szene bist, siehst du die Karte (oder nur schwarz, wenn der GM den Nebel des Krieges noch nicht aufgedeckt hat).
- **Sicht:** Du siehst nur das, was der GM für dich aufdeckt. Außerhalb dieses Bereichs ist alles schwarz.
- **Bewegen:** Klicke mit der linken Maustaste (oder dem Finger auf dem Tablet) auf **dein** Token, halte die Taste gedrückt und ziehe es an die gewünschte Position.
- **Einschränkung:** Du kannst die Tokens anderer Spieler oder von NPCs (Gegnern) nicht bewegen. Du kannst sie nicht einmal anklicken.
- **Sichtbeschränkung für Bewegung:** Du kannst dein Token nicht in den schwarzen "Nebel des Krieges" ziehen. Wenn du es versuchst, wird die Bewegung blockiert.
- **Kameraführung:** Mit dem Mausrad kannst du zoomen. Mit gehaltener rechter Maustaste kannst du den Kartenausschnitt verschieben.

---

## 3. Das Betrachtungsfenster (Display)

Das Display-Fenster ist eine spezielle Ansicht, die für einen zweiten Monitor, einen Fernseher am Spieltisch oder einen Beamer gedacht ist.

### 3.1 Aufruf
- Der Link zum Display lautet `/display` (z.B. `http://192.168.178.50:5000/display`).
- Du findest den genauen Link als GM auf der Login-Seite (`/gm/login`).

### 3.2 Funktion
- Das Display zeigt exakt das, was die Spieler sehen (inklusive des Nebels des Krieges).
- **Unterschied zu Spielern:** Das Display hat *keine* Berechtigung, irgendwelche Tokens zu bewegen.
- Es verhält sich passiv. Wenn der GM eine Szene aktiviert, wechselt das Display automatisch dorthin. Ist keine aktiv, zeigt das Display das Warteraum-Bild.

---

## 4. Technischer Teil: Installation & Betrieb

Dieser Teil richtet sich an die Person, die das System hostet (in der Regel der Spielleiter).

### 4.1 Systemanforderungen
- **Python:** Du benötigst Python (Version 3.8 oder höher).
- **Git:** (Optional) um den Code herunterzuladen.
- Einen modernen Webbrowser (Chrome, Firefox, Edge, Safari).

### 4.2 Installation
1. Lade den Code herunter oder klone das Repository.
2. Öffne ein Terminal (Kommandozeile / PowerShell) und navigiere in den Ordner des Projekts.
3. Installiere die benötigten Abhängigkeiten mit dem Befehl:
   ```bash
   pip install -r requirements.txt
   ```
   *(Tipp: Es empfiehlt sich, ein sogenanntes "Virtual Environment" für Python zu nutzen).*

### 4.3 Konfiguration (`config.py`)
Bevor du startest, kannst du die Datei `config.py` in einem Texteditor öffnen. Hier findest du drei wichtige Einstellungen:
- `APP_TITLE = "VTTRPGE"`: Der Name, der im Browser-Tab angezeigt wird.
- `GM_PASSWORD = "gm"`: Das Passwort für den Spielleiter-Login. Ändere dies für mehr Sicherheit.
- `SERVER_PORT = 5000`: Der Port, auf dem der Server läuft.
- `HOST_URL = "localhost"`: **Wichtig für das lokale Netzwerk.** Wenn deine Spieler über ihre Handys in deinem WLAN mitspielen sollen, trage hier die lokale IP-Adresse deines PCs ein (z.B. `"192.168.178.50"`). Dies sorgt dafür, dass die Links auf der Login-Seite korrekt generiert werden.

### 4.4 Starten des Servers
1. Öffne das Terminal im Projektordner.
2. Führe den folgenden Befehl aus:
   ```bash
   python app.py
   ```
3. Der Server startet. Du siehst in der Konsole Meldungen, dass der Server auf bestimmten Ports horcht (meist `http://127.0.0.1:5000`).
4. Lasse das Terminal-Fenster im Hintergrund offen! Solange es offen ist, läuft der Server.

### 4.5 Beenden des Servers
Um den Server zu stoppen und das Spiel zu beenden:
1. Gehe in das Terminal-Fenster, in dem `python app.py` läuft.
2. Drücke gleichzeitig **`Strg` + `C`** (auf dem Mac `Control` + `C`).
3. Der Server fährt herunter und das Terminal ist wieder freigegeben.

### 4.6 Datenhaltung & Backups
Alle deine Daten (Kampagnen, Szenen, Tokens, hochgeladene Bilder) bleiben lokal auf deinem Rechner.

- **Die Datenbank:** Alle Text- und Einstelldaten (inkl. Nebel und Zeichnungen) liegen in der Datei `instance/ttrpg.db`.
- **Die Bilder:** Hochgeladene Karten und Tokens liegen im Ordner `uploads/`.

**Wie mache ich ein Backup?**
Kopiere einfach den Ordner `instance/` und den Ordner `uploads/` an einen sicheren Ort (z.B. auf einen USB-Stick oder in eine Cloud). Wenn du das System auf einem anderen PC nutzen willst, kopierst du diese Ordner einfach in dein neues Projektverzeichnis.
