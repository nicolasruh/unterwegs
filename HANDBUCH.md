# unterWEGs – Technik und Webmaster-Handbuch

## 1. Überblick: Was gehört wohin?

Die neue Website liegt im Ordner [website](website/). Nur dessen Inhalt
wird später veröffentlicht. Die Ordner `lichterweg` und `lichterweg-wAssets`
sind der bisherige CMS-Export und werden nicht mit hochgeladen.

| Datei oder Ordner | Aufgabe |
|---|---|
| [website/index.html](website/index.html) | Home, erreichbar über das Logo |
| [website/besucherinfo.html](website/besucherinfo.html) | Hinweise für Besuchende |
| [website/eindruecke.html](website/eindruecke.html) | Jahresübersicht und Galerie |
| [website/ueber-uns.html](website/ueber-uns.html) | Team, Danke, Kontakt, Spenden, Impressum |
| [website/banner.html](website/banner.html) | Gemeinsame aktuelle Mitteilung auf allen Seiten |
| [website/assets/style.css](website/assets/style.css) | Gemeinsame Gestaltung |
| [website/assets/gallery.css](website/assets/gallery.css) | Gestaltung der Galerien |
| [website/assets/bilder](website/assets/bilder/) | Fotos und Jahresordner |
| [scripts/galerien_aktualisieren.py](scripts/galerien_aktualisieren.py) | Lokales Hilfsprogramm für die Galeriepflege |

### Technische Eckpunkte

- Reines HTML, CSS und lokales JavaScript; kein CMS, keine Datenbank,
  kein JavaScript-Framework und kein Serverprogramm für die veröffentlichte Website.
- Vier eigenständige Seiten, ergänzt um eine Bannerdatei. Navigation und
  Footer stehen bewusst in jeder Seite und müssen bei Änderungen überall
  angepasst werden.
- Alle internen Pfade sind relativ. Die Website funktioniert daher auch
  unter einer GitHub-Pages-Projektadresse mit Unterpfad.
- Bilder, Logo und Menüschrift liegen lokal. Es werden keine externen
  Skripte oder Schriften eingebunden. Spenden- und andere externe Links
  führen erst beim Anklicken zu den jeweiligen Diensten.
- Jede Seite hat ein zentriertes, feststehendes Hintergrundbild, das
  bildschirmfüllend zugeschnitten wird. Layout und Spalten passen sich
  der Bildschirmbreite an.
- `banner.js` lädt den Inhalt von `banner.html` mit der ID `mitteilung`.
  Bei einem Fehler oder ohne JavaScript gibt es einen direkten Link dorthin.
  Für die Vorschau ist deshalb ein lokaler Webserver nötig, nicht nur
  ein Doppelklick auf eine HTML-Datei.
- `reading.js` hinterlegt den Haupttext beim Aufruf und beim Scrollen
  leicht schwarz. Nach einer halben Sekunde Ruhe blendet die Hinterlegung
  innerhalb von 2,5 Sekunden aus.
- Die Galerie öffnet einen modalen Dialog. Bildpunkte, Pfeile, Pfeiltasten,
  Schliessen-X, optionale Diashow und bei Browserunterstützung echtes Vollbild
  werden durch `gallery.js` gesteuert. Fotos werden erst beim Blättern geladen.
  Credits sind nur eine visuelle Einblendung, nicht fest in die Fotos eingebrannt.
- Der Browser kann auf statischem Hosting keine Jahresordner auflisten.
  Das lokale Python-Skript erzeugt deshalb vorher die Dateiliste und die
  Jahresübersicht. Die fertige Website braucht kein Python.
- Das Skript verarbeitet nur direkt enthaltene Fotos in vierstelligen
  Jahresordnern: JPG, JPEG, PNG und WebP. Es sortiert Jahre absteigend und
  Bilder nach Dateinamen mit natürlicher Zahlenfolge: `2.jpg` vor `10.jpg`.
  Originalfotos werden nicht verändert.

## 2. Vorbereitungen am eigenen Computer

Die folgenden Anleitungen beziehen sich auf macOS und das Projekt in VS Code.
Die Galerieerzeugung selbst ist mit Python und Pillow auch unter Windows/Linux
nutzbar; dort unterscheidet sich gegebenenfalls der Pfad zum Python-Programm.

### Terminal am richtigen Ort öffnen

1. Öffne diesen Projektordner in VS Code.
2. Wähle im Menü **Terminal → Neues Terminal**.
3. Die Befehle unten jeweils vollständig kopieren, ins Terminal einfügen
   und mit der Eingabetaste ausführen. Die Terminalposition soll der
   Projektordner sein, in dem dieses Handbuch liegt.

### Einmalig das Galerie-Hilfsprogramm vorbereiten

Voraussetzung ist Python 3. Prüfen lässt sich das mit `python3 --version`.
Falls Python fehlt, muss es einmal installiert werden.

Führe diese beiden Befehle nacheinander aus:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
```

Damit wird die Bildbibliothek Pillow nur für dieses Projekt installiert.
Der versteckte Ordner `.venv` enthält Hilfsprogramme, keine Website-Inhalte.
Er wird nicht hochgeladen. Die Vorbereitung ist nur beim ersten Einrichten
oder nach einem Computerwechsel nötig.

### Lokale Vorschau starten

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory website
```

Öffne danach <http://127.0.0.1:8000/> im Browser.
Lass das Terminal während der Vorschau offen. Mit **Ctrl+C** kannst du
den Vorschau-Server beenden. Andere Befehle kannst du in einem zweiten
Terminal ausführen.

## 3. Häufige Arbeiten – Schritt für Schritt

### Vor jeder Änderung

Erstelle eine Sicherung der betroffenen Datei oder des Website-Ordners
ausserhalb von `website`. Falls das Projekt bereits mit Git verwaltet wird,
kannst du stattdessen einen gesicherten Versionsstand verwenden.

Speichere Änderungen in VS Code mit **Cmd+S**. Prüfe danach die lokale
Vorschau, bevor du etwas veröffentlichst.

### Bannertext ändern

1. Öffne [website/banner.html](website/banner.html) im Editor.
2. Suche die Zeile mit `<main class="banner" id="mitteilung">`.
3. Ändere darunter die Überschrift zwischen `<h2>` und `</h2>` und die
   Texte zwischen `<p>` und `</p>`.
4. Lass die umgebenden Zeichen und besonders `id="mitteilung"` unverändert.
5. Speichere und lade die Vorschau im Browser neu.
6. Prüfe den Banner auf mehreren Seiten. Er wird überall aus dieser einen
   Datei geladen. Ein Galerie-Aktualisierungslauf ist dafür nicht nötig.

Beispiel:

```html
<h2>UnterWEGs 2026</h2>
<p>Hier steht die aktuelle Mitteilung.</p>
<p><strong>Wichtig:</strong> Hier steht ein hervorgehobener Hinweis.</p>
```

Für einen zusätzlichen Absatz kannst du eine vollständige `<p>…</p>`-Zeile
kopieren. Für eine neue Zeile innerhalb eines Absatzes verwende `<br>`.
Ein sichtbares `&` schreibst du im HTML als `&amp;`.

### Sonstigen Text ändern

1. Wähle die passende HTML-Datei aus der Tabelle oben.
2. Suche mit **Cmd+F** einen Teil des bisherigen Textes.
3. Ersetze nur die Wörter zwischen den HTML-Markierungen:
   beispielsweise `<p>Text</p>` für Absätze oder `<li>Text</li>` für Listen.
4. Lass Angaben wie `id="kontakt"`, Dateinamen und Verlinkungen stehen,
   sofern du sie nicht bewusst ändern möchtest.
5. Speichere und prüfe die Seite auch mit einem schmalen Browserfenster.

Die automatisch erzeugten Jahreslinks und Vorschaubereiche in
`eindruecke.html` sind eine Ausnahme: Inhalte zwischen den Kommentaren
`GALERIE-JAHRE:START/ENDE` und `GALERIE-VORSCHAUEN:START/ENDE` nicht von
Hand ändern. Beim nächsten Galerie-Lauf werden diese Bereiche ersetzt.
Andere Texte auf dieser Seite bleiben erhalten.

**E-Mail-Adresse ändern:** In `ueber-uns.html` stehen sichtbare Adresse und
`mailto:`-Adresse. Beide ändern, auch im Impressum. Bei Änderungen an
Navigation oder Footer dieselbe Anpassung in allen vier Seiten vornehmen.

### Neue Galerie anlegen, zum Beispiel 2026

1. Öffne [website/assets/bilder](website/assets/bilder/) und erstelle
   darin einen Ordner namens **2026**. Nur die vier Ziffern verwenden.
2. Kopiere die Fotos direkt hinein, nicht in weitere Unterordner.
   Verwende nach Möglichkeit einfache Namen wie `001.jpg`, `002.jpg`.
   Ihre alphabetisch-numerische Reihenfolge bestimmt die Bildabfolge.
3. Kopiere die Datei `galerie.json` aus einem bestehenden Jahresordner
   in den neuen Ordner. **Nicht** die zentrale Datei `galerien.json` kopieren.
4. Öffne die kopierte `galerie.json` und passe sie an, zum Beispiel:

```json
{
  "place": "Alpenzeiger Aarau",
  "credit": "Bilder: Nicolas Ruh und andere",
  "preview": "001.jpg"
}
```

`place` ist der Ort hinter der Jahreszahl. `credit` ist der Bildnachweis.
`preview` ist der genaue Name eines Fotos in diesem Jahresordner; daraus
wird die verkleinerte Vorschau erstellt. Gross-/Kleinschreibung und Endung
müssen stimmen. Ist der Ort oder Bildnachweis unbekannt, darf der Wert
`""` sein. Ohne die ganze `preview`-Zeile wird das erste Foto verwendet;
dabei auch das Komma nach der `credit`-Zeile entfernen.

Lass die geraden Anführungszeichen, Kommas und geschweiften Klammern
wie im Beispiel stehen. Nach der letzten Zeile steht kein Komma.

5. Speichere die Datei und führe im Terminal aus:

```sh
.venv/bin/python scripts/galerien_aktualisieren.py
```

6. Warte auf die Meldung **„Fertig: … Jahresgalerien …“**.
   Das Programm erstellt automatisch:
   - das verkleinerte `vorschau.jpg` pro Jahr;
   - die zentrale Bildliste `assets/bilder/galerien.json`;
   - die Jahreslinks und Vorschaukarten in `eindruecke.html`.
7. Lade die lokale Vorschau neu und öffne **Eindrücke**. Das neue Jahr
   erscheint oben. Prüfe Ort, Vorschau, Bildreihenfolge und Credits.
8. Für die spätere Veröffentlichung müssen der neue Jahresordner,
   die aktualisierten Vorschaubilder, `galerien.json` und `eindruecke.html`
   zusammen hochgeladen werden. Am einfachsten den ganzen geprüften
   Inhalt von `website` übertragen.

**Nur den Jahresordner hochladen reicht nicht.** Das Hilfsprogramm muss
vorher lokal laufen. Du musst weder HTML-Karten kopieren noch Bildnamen
in eine zentrale Liste von Hand eintragen.

### Bilder oder Angaben in einer bestehenden Galerie ändern

- **Foto hinzufügen:** In den Jahresordner kopieren, Aktualisierungsbefehl
  ausführen, prüfen.
- **Foto entfernen:** Aus dem Jahresordner herausnehmen, Befehl ausführen.
  War es das ausgewählte Vorschaubild, vorher `preview` anpassen.
- **Ort, Credits oder Vorschau ändern:** Die `galerie.json` des betreffenden
  Jahres bearbeiten und Befehl ausführen.
- **Reihenfolge ändern:** Bilddateien passend umbenennen, etwa mit
  `001-`, `002-` am Anfang; gegebenenfalls `preview` anpassen.
  Danach Befehl ausführen.
- **Jahr entfernen:** Den ganzen Jahresordner ausserhalb von
  `assets/bilder` sichern/verschieben, danach Befehl ausführen. Beim
  produktiven Upload auch den alten Ordner auf dem Host entfernen, wenn
  die Bilder dort nicht mehr erreichbar sein sollen. Das Skript löscht
  keine entfernten Dateien auf dem Host.

`vorschau.jpg` ist eine erzeugte Datei. Keine Originalaufnahme so nennen.
Die zentrale `galerien.json` nicht manuell bearbeiten; Änderungen darin
würden beim nächsten Lauf überschrieben. Leere Jahresordner führen zu
einer Fehlermeldung. Neue Jahre deshalb erst mit Fotos anlegen.

### Wenn etwas nicht funktioniert

| Problem | Was tun? |
|---|---|
| Banner lädt beim Doppelklick nicht | Vorschau-Server starten und die HTTP-Adresse oben verwenden. |
| `.venv/bin/python` fehlt | Die einmalige Vorbereitung aus Abschnitt 2 ausführen. |
| `No module named PIL` | Pillow mit dem Installationsbefehl aus Abschnitt 2 nachinstallieren. |
| „ungültiges JSON, Zeile …“ | `galerie.json` des genannten Jahres öffnen; Anführungszeichen und Kommas mit dem Beispiel vergleichen. |
| „Vorschaubild … nicht gefunden“ | Exakten Bildnamen bei `preview` prüfen. |
| „HTML-Markierungen fehlen …“ | Die genannten Kommentare in `eindruecke.html` aus einer Sicherung wiederherstellen. |
| Neue Bilder erscheinen nicht | Aktualisierungsbefehl ausführen und alle erzeugten Dateien mit übertragen. |
| Browser zeigt den alten Stand | Vollständig neu laden, auf dem Mac mit **Cmd+Shift+R**. |

Bei einer Fehlermeldung nicht veröffentlichen. Die Eingaben werden vor
dem Schreiben geprüft; bei Eingabefehlern bleiben die bisherigen Ausgaben
erhalten. Falls der Computer während des Schreibens ausfällt, den Befehl
nach Behebung erneut ausführen und die Vorschau prüfen.

## 4. Prüfen und veröffentlichen

Der geplante Weg bleibt: **lokal → GitHub-Pages-Review → bisheriger Host**.
Die öffentliche GitHub-Pages-Vorschau liegt unter
<https://nicolasruh.github.io/unterwegs/>.
Das Repository ist <https://github.com/nicolasruh/unterwegs>.
Die produktive Domain und der bisherige Host bleiben unverändert.
Ein Galerie-Aktualisierungslauf lädt nichts ins Internet hoch.

### Änderungen auf GitHub Pages veröffentlichen

Nach der lokalen Prüfung im Projektordner ausführen:

```sh
git add website scripts HANDBUCH.md .gitignore .github
git diff --cached --stat
git commit -m "Website aktualisieren"
git push origin main
```

Vor dem Commit die angezeigte Dateiliste kontrollieren. Jeder Push auf
`main` startet den Workflow **Publish GitHub Pages**. Er veröffentlicht
ausschliesslich den Ordner `website`. Den Fortschritt und eventuelle Fehler
zeigt <https://github.com/nicolasruh/unterwegs/actions>.
Erst nach einem erfolgreichen Lauf die Vorschau neu laden und prüfen.
Die CMS-Exporte und `.venv` werden durch `.gitignore` ausgeschlossen.

Vor jedem Upload:

- Alle vier Seiten öffnen; Banner und E-Mail-Link prüfen.
- Geänderte Galerien öffnen, blättern und wieder schliessen.
- Kleines Browserfenster beziehungsweise Smartphone prüfen.
- Rechte zur Veröffentlichung der Fotos und richtige Bildnachweise bestätigen.
- Den bisher veröffentlichten Stand für einen Rückwechsel sichern.

Die Vorschau enthält `noindex`-Metatags und einen sichtbaren Vorschauhinweis.
Beides vor dem Produktivstart bewusst entfernen. `noindex` ist kein
Zugriffsschutz: Eine GitHub-Pages-Vorschau ist in der Regel öffentlich.
Beim Wechsel auf den bisherigen Host sind zudem die Weiterleitungen alter
URLs einzurichten und zu prüfen.

Nur den **Inhalt von `website`** bereitstellen, nicht den CMS-Export,
`scripts`, `.venv` oder dieses Handbuch. Auch die erzeugten Dateien können
ohne laufendes Hilfsprogramm auf beiden Hosts verwendet werden.
