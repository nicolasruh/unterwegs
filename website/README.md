# Statische unterWEGs-Website

Das [Webmaster-Handbuch](../HANDBUCH.md) erklärt die technische Umsetzung
und die alltägliche Pflege Schritt für Schritt, einschliesslich Einrichtung
des lokalen Galerie-Hilfsprogramms.

## Lokal ansehen

Im Projektordner starten:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory website
```

Dann <http://127.0.0.1:8000/> öffnen. Mit Strg+C beenden.
Die zentrale Mitteilung benötigt HTTP(S); direktes Öffnen per Doppelklick
reicht dafür nicht aus.

## Bearbeiten

- [Home](index.html), [Besucherinfo](besucherinfo.html),
  [Eindrücke](eindruecke.html) und [Über uns](ueber-uns.html)
  enthalten die direkt bearbeitbaren Seiteninhalte.
- In [banner.html](banner.html) nur den Inhalt innerhalb von
  `<main id="mitteilung">` bearbeiten. Die ID beibehalten.
  [banner.js](assets/banner.js) lädt diesen Inhalt auf allen vier Seiten.
  Ohne JavaScript oder bei Ladefehlern gibt es einen direkten Link zur Mitteilung.
- Das gemeinsame Aussehen steht in [style.css](assets/style.css).
- Navigation und Fusszeile stehen bewusst in jeder Seite und müssen bei
  Änderungen an allen vier Stellen angepasst werden.
  Home ist nur über das Logo erreichbar, nicht über einen eigenen Menüpunkt.
  Das Hauptmenü verwendet die lokal gespeicherte Originalschrift
  `rgaregular.woff2` ohne Unterstreichung.
- Bilder und Logo liegen lokal in `assets/`. Es gibt keine externen
  Skripte, Schriften oder automatisch geladenen Drittanbieter-Inhalte.
- Jede Seite hat ein eigenes, feststehendes Hintergrundbild, zentriert und
  mit `cover` bildschirmfüllend zugeschnitten. Die Zuordnung steht in
  [style.css](assets/style.css): Home verwendet das Standardbild,
  die anderen Seiten ihre jeweilige Klasse am `<body>`.
  Das Banner ist über die gesamte Fensterbreite halbtransparent;
  die Fusszeile ebenfalls fensterbreit und halbtransparent schwarz;
  ihre Texte bleiben am zentrierten Inhaltsbereich ausgerichtet.
  Schrift und Sprunglinks sind bewusst zurückhaltend gehalten.
- [reading.js](assets/reading.js) hinterlegt den Haupttext beim Aufruf
  und beim Scrollen mit 25 % Schwarz. Nach 500 ms ohne Scrollen blendet
  die Hinterlegung innerhalb von 2,5 Sekunden ganz aus. Die Zeiten stehen
  im Skript und in [style.css](assets/style.css). Bei bevorzugter reduzierter
  Bewegung entfällt der Übergang; ohne JavaScript bleibt die leichte
  Hinterlegung bestehen.
- Auf «Über uns» bilden die beiden `.section-pair`-Container die Paare
  Danke/Kontakt und Spenden/Impressum. Auf schmalen Bildschirmen stehen
  ihre Abschnitte untereinander.

## Stand und Quellen

Öffentliche Review-Vorschau: <https://nicolasruh.github.io/unterwegs/>.
Noch nicht auf die produktive Domain umgestellt.
Veranstaltungsangaben: Live-Website vom 4. November 2026;
Kinderwagentauglichkeit auf Wunsch zu «bedingt kinderwagentauglich» vereinheitlicht.
Übrige Texte: lokaler Weblication-Export; Absätze, Listen und interne Links
wurden für die neue Seitenstruktur angepasst. Hintergrundbilder aus dem Export:
Home verwendet `Titelbild2023.jpg`, Besucherinfo neu das Lichterkettenmotiv
`DSCF2842-Hintergrund-Startseite-2020.jpg` (1920 × 1300 Pixel),
Über uns das bisherige Kontaktmotiv `_DSC7482.jpg`. Eindrücke verwendet
neu das Wald-/Kerzenmotiv `2017_unterWEGs_35.jpg` (1920 × 1280 Pixel)
mit leichter Abdunklung; die ursprünglichen
Galerieseiten hatten einen einfarbigen Hintergrund.
Logo und Menüschrift: bestehende Live-Website.
Der Originalexport bleibt unverändert ausserhalb dieses Ordners.

Die 13 Jahresgalerien mit 314 Originalbildern sind übernommen. Ortsangaben
und vorhandene Bildnachweise stammen aus den jeweiligen Galerieseiten
des Exports. Ab 2021 lautet der Bildnachweis auf Wunsch
«Bilder: Nicolas Ruh und andere»; ältere Bildnachweise bleiben unverändert.
Die Bilddateien
des Jahresordners 2025 tragen teilweise «2026» im Namen; massgeblich für
die Zuordnung blieb die ursprüngliche Galerieseite 2025.
Das bisherige TWINT-Bild und der bestehende
Spendenlink sind übernommen; ihre Funktion ist vor Freigabe zu bestätigen.

Vor Freigabe müssen insbesondere die Aktualität der Danksagungen, der Teamangaben
und des Impressums sowie die Bildrechte bestätigt werden.
Der Lageplan von 2025 gehört zum alten Veranstaltungsort und ist bewusst
nicht als aktueller Lageplan eingebunden.

## Galerien bearbeiten

- Bilder liegen in `assets/bilder/JJJJ/`, ohne CMS-Verwaltungsdateien.
  Die Originaldateien sind unverändert kopiert. Pro Jahr gibt es ein
  verkleinertes `vorschau.jpg` (maximal 640 Pixel).
- In jedem Jahresordner ist `galerie.json` die bearbeitbare Quelle für
  Ort (`place`), Bildnachweis (`credit`) und optional das Vorschaufoto
  (`preview`, exakter Dateiname eines Originals).
- Neue Fotos oder Jahre ergänzen und danach vom Projektordner aus
  `.venv/bin/python scripts/galerien_aktualisieren.py` ausführen.
  Einrichtung: siehe [Handbuch](../HANDBUCH.md).
- Das Skript erzeugt die Vorschaubilder und
  [galerien.json](assets/bilder/galerien.json) mit natürlich sortierten
  Bildnamen sowie die Jahreslinks und Karten in
  [eindruecke.html](eindruecke.html). Generierte Bereiche sind durch
  `GALERIE-JAHRE:START/ENDE` und `GALERIE-VORSCHAUEN:START/ENDE` markiert.
  Diese Bereiche und die zentrale JSON-Datei nicht von Hand bearbeiten.
  Die restliche HTML-Datei bleibt manuell bearbeitbar.
- Ohne `preview` wird das erste Foto verwendet. `vorschau.jpg` wird nicht
  als Original aufgelistet. Leere Jahresordner, fehlende Metadaten oder
  ungültige Vorschaufotos führen vor dem Schreiben zu einer Fehlermeldung.
  Das Skript benötigt lokal Python/Pillow, die veröffentlichte Website nicht.
- [gallery.js](assets/gallery.js) und [gallery.css](assets/gallery.css)
  steuern das bildschirmfüllende Dialog-Overlay. Die Übersicht lädt nur
  Vorschaubilder, die Originale erst beim Öffnen/Blättern.
  Der Bedienhinweis steht unter den Jahresvorschauen. Die Steuerungsleiste
  ist zentriert, der Galerietitel abgetönt. Bildnachweise liegen als
  transparente Wasserzeichen unten rechts im sichtbaren Bildbereich,
  auch bei Hochformatbildern und nach einer Grössenänderung.
- Pfeile in der unteren Navigationszeile und Pfeiltasten blättern mit Umlauf.
  Pro Bild gibt es einen anklickbaren Punkt; der aktuelle ist halbtransparent
  gefüllt. Auf kleinen Bildschirmen ist die Punktreihe horizontal scrollbar
  und folgt dem aktuellen Bild. Die Bildnummer bleibt für Screenreader verfügbar.
  Escape oder das dezente X schliesst und setzt den Fokus auf die Jahresvorschau zurück.
  Der Dialog hält den Tastaturfokus innerhalb der Galerie.
- Autoplay startet nur auf Wunsch. Der Start/Pause-Knopf aktiviert einen
  Wechsel alle fünf Sekunden nach dem Laden des Bilds. Das Symbol wechselt
  zwischen Start und Pause; Tooltip und zugängliche Beschriftung passen sich an.
  Manuelles Blättern oder Auswählen eines Punkts,
  Schliessen oder ein Wechsel in einen anderen Tab stoppt die Diashow.
  Ladefehler werden angezeigt und stoppen ebenfalls die Diashow.
- Der Vollbildknopf in derselben Zeile schaltet bei Browserunterstützung
  echtes Vollbild ein und aus. Schliessen beendet auch das Galerie-Vollbild.
  Escape verlässt im Vollbild je nach Browser zunächst den Vollbildmodus.
  Bei fehlender Unterstützung bleibt der Knopf verborgen; das
  bildschirmfüllende Overlay funktioniert weiterhin.
- Ohne JavaScript führt jede Jahresvorschau direkt zum ersten Originalbild.

## Galerie-Skript testen

Im Projektordner:

```sh
.venv/bin/python -m unittest discover -s scripts -p 'test_*.py'
```

Die Tests verwenden temporäre Testgalerien und ändern keine echten Fotos.
`--site-dir PFAD` erlaubt dem Hilfsprogramm alternativ einen anderen
Website-Ordner; ohne Angabe verwendet es immer den Projektordner `website`,
unabhängig vom aktuellen Arbeitsverzeichnis.

## Veröffentlichen

Nur den Inhalt dieses Ordners bereitstellen, niemals den gesamten
CMS-Export mit Verwaltungsdateien, Versionen und Protokollen.
Der Workflow [Publish GitHub Pages](../.github/workflows/pages.yml)
veröffentlicht bei jedem Push auf `main` diesen Ordner als Website-Artefakt.
Repository: <https://github.com/nicolasruh/unterwegs>.
Die Schritte für Commit und Push stehen im [Handbuch](../HANDBUCH.md).
Alle internen Pfade sind relativ,
damit auch eine Projektadresse mit Unterpfad funktioniert.

Für den Produktivstart Vorschauhinweis entfernen und die
`noindex`-Metatags in allen fünf HTML-Dateien prüfen bzw.
entfernen. Zuvor Backup, Weiterleitungen alter URLs und Prüfung auf dem
Zielhost vorsehen. Der bestehende Host und die produktive Domain bleiben
unverändert.
