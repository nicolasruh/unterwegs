#!/usr/bin/env python3
"""Erzeugt die statischen Galeriedaten, Jahresvorschauen und HTML-Jahresblöcke."""

import argparse
from html import escape
from io import BytesIO
import json
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import quote

from PIL import Image, ImageOps


SITE_DIR = Path(__file__).resolve().parents[1] / "website"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
PREVIEW_NAME = "vorschau.jpg"
LINKS_START = "<!-- GALERIE-JAHRE:START -->"
LINKS_END = "<!-- GALERIE-JAHRE:ENDE -->"
CARDS_START = "<!-- GALERIE-VORSCHAUEN:START -->"
CARDS_END = "<!-- GALERIE-VORSCHAUEN:ENDE -->"


def natural_key(name):
    return re.sub(r"\d+", lambda match: match.group().zfill(12), name.casefold()), name


def replace_block(text, start, end, content):
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"HTML-Markierungen fehlen oder sind mehrfach vorhanden: {start}, {end}")
    before, remainder = text.split(start)
    _, after = remainder.split(end)
    return before + start + "\n" + content + "\n      " + end + after


def load_metadata(folder):
    path = folder / "galerie.json"
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"{path}: galerie.json fehlt oder ist eine Verknüpfung.")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path}: ungültiges JSON, Zeile {error.lineno}: {error.msg}") from error
    if not isinstance(data, dict):
        raise ValueError(f"{path}: erwartet wird ein JSON-Objekt mit place und credit.")
    for field in ("place", "credit"):
        if not isinstance(data.get(field), str):
            raise ValueError(f'{path}: "{field}" muss als Text in Anführungszeichen vorhanden sein.')
    if "preview" in data and not isinstance(data["preview"], str):
        raise ValueError(f'{path}: "preview" muss ein Bilddateiname in Anführungszeichen sein.')
    unknown = set(data) - {"place", "credit", "preview"}
    if unknown:
        raise ValueError(f"{path}: unbekannte Felder: {', '.join(sorted(unknown))}")
    return data


def create_preview(path):
    with Image.open(path) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")
        image.thumbnail((640, 640), Image.Resampling.LANCZOS)
        output = BytesIO()
        image.save(output, format="JPEG", quality=85, optimize=True)
        return output.getvalue(), image.size


def atomic_write(path, content):
    if path.is_symlink():
        raise ValueError(f"{path}: Ausgabedatei darf keine Verknüpfung sein.")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        temporary.chmod(0o644)
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def update_galleries(site_dir=SITE_DIR):
    site_dir = Path(site_dir)
    images_dir = site_dir / "assets" / "bilder"
    html_path = site_dir / "eindruecke.html"
    html = html_path.read_text(encoding="utf-8")
    folders = sorted(
        (path for path in images_dir.iterdir()
         if path.is_dir() and re.fullmatch(r"[0-9]{4}", path.name)),
        key=lambda path: path.name, reverse=True,
    )
    if not folders:
        raise ValueError(f"{images_dir}: keine vierstelligen Jahresordner gefunden.")

    galleries = {}
    previews = []
    cards = []
    links = []
    for folder in folders:
        if folder.is_symlink():
            raise ValueError(f"{folder}: Jahresordner darf keine Verknüpfung sein.")
        year = folder.name
        metadata = load_metadata(folder)
        photos = sorted(
            (path for path in folder.iterdir()
             if path.suffix.lower() in EXTENSIONS
             and path.name.casefold() != PREVIEW_NAME
             and not path.name.startswith(".")),
            key=lambda path: natural_key(path.name),
        )
        if not photos:
            raise ValueError(f"{folder}: keine Bilder gefunden. Leere Jahresordner nicht veröffentlichen.")
        for photo in photos:
            if not photo.is_file() or photo.is_symlink() or "\\" in photo.name:
                raise ValueError(f"{photo}: erwartet wird eine normale Bilddatei ohne Verknüpfung.")
        filenames = [photo.name for photo in photos]
        if len({name.casefold() for name in filenames}) != len(filenames):
            raise ValueError(f"{folder}: Bildnamen unterscheiden sich nur in der Gross-/Kleinschreibung.")
        preview = metadata.get("preview", filenames[0])
        if preview not in filenames:
            raise ValueError(f'{folder / "galerie.json"}: Vorschaubild "{preview}" nicht gefunden.')
        try:
            preview_bytes, (width, height) = create_preview(folder / preview)
        except (OSError, ValueError, Image.DecompressionBombError) as error:
            raise ValueError(f"{folder / preview}: Vorschaubild nicht lesbar: {error}") from error
        previews.append((folder / PREVIEW_NAME, preview_bytes))
        galleries[year] = {
            "place": metadata["place"],
            "credit": metadata["credit"],
            "images": filenames,
        }
        place = f' <span>({escape(metadata["place"])})</span>' if metadata["place"] else ""
        first_url = escape(f"assets/bilder/{year}/{quote(filenames[0], safe='')}", quote=True)
        links.append(f'        <a href="#jahr-{year}">{year}</a>')
        cards.append(
            f'        <section id="jahr-{year}">\n'
            f'          <a class="gallery-open" data-year="{year}" href="{first_url}">\n'
            f'            <img src="assets/bilder/{year}/vorschau.jpg" '
            f'alt="Lichterweg {year} – Galerie öffnen" width="{width}" height="{height}" loading="lazy">\n'
            f'            <h2>{year}{place}</h2>\n'
            f'          </a>\n'
            f'        </section>'
        )

    html = replace_block(html, LINKS_START, LINKS_END, "\n".join(links))
    html = replace_block(html, CARDS_START, CARDS_END, "\n".join(cards))
    manifest = json.dumps(galleries, ensure_ascii=False, indent=2) + "\n"
    outputs = previews + [
        (images_dir / "galerien.json", manifest.encode("utf-8")),
        (html_path, html.encode("utf-8")),
    ]
    # Erst alle Eingaben prüfen, bevor bestehende Website-Dateien ersetzt werden.
    for path, _ in outputs:
        if path.is_symlink():
            raise ValueError(f"{path}: Ausgabedatei darf keine Verknüpfung sein.")
    for path, content in outputs:
        atomic_write(path, content)
    return len(galleries), sum(len(gallery["images"]) for gallery in galleries.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=SITE_DIR, help="Website-Ordner (Standard: website)")
    args = parser.parse_args()
    try:
        years, pictures = update_galleries(args.site_dir)
    except (OSError, ValueError) as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 1
    print(f"Fertig: {years} Jahresgalerien mit {pictures} Bildern aktualisiert.")
    print("Vorschaubilder, galerien.json und Jahresübersicht wurden erzeugt. Bitte lokal prüfen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
