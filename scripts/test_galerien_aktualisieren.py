import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from galerien_aktualisieren import (
    CARDS_END, CARDS_START, LINKS_END, LINKS_START, update_galleries,
)


class GalleryGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.site = Path(self.temporary.name)
        self.images = self.site / "assets" / "bilder"
        self.images.mkdir(parents=True)
        self.page = self.site / "eindruecke.html"
        self.page.write_text(
            f"VORHER<nav>{LINKS_START}alte Links{LINKS_END}</nav>"
            f"<div>{CARDS_START}alte Karten{CARDS_END}</div>NACHHER",
            encoding="utf-8",
        )

    def add_year(self, year, names=("bild10.jpg", "bild2.jpg"), **metadata):
        folder = self.images / year
        folder.mkdir()
        data = {"place": "Aarau", "credit": "Bilder: Test"}
        data.update(metadata)
        (folder / "galerie.json").write_text(json.dumps(data), encoding="utf-8")
        for name in names:
            Image.new("RGB", (900, 600), "#663322").save(folder / name)
        return folder

    def test_new_year_order_preview_and_idempotence(self):
        self.add_year("2025")
        folder = self.add_year(
            "2026", names=("bild10.JPG", "bild2.jpg", "Bild & #3.jpg"),
            place='Alpenzeiger & "Wald"', preview="Bild & #3.jpg",
        )
        original = (folder / "Bild & #3.jpg").read_bytes()
        self.assertEqual(update_galleries(self.site), (2, 5))
        data = json.loads((self.images / "galerien.json").read_text())
        self.assertEqual(list(data), ["2026", "2025"])
        self.assertEqual(data["2025"]["images"], ["bild2.jpg", "bild10.jpg"])
        self.assertNotIn("vorschau.jpg", data["2026"]["images"])
        with Image.open(folder / "vorschau.jpg") as image:
            self.assertEqual(image.size, (640, 427))
        html = self.page.read_text()
        self.assertIn("Alpenzeiger &amp; &quot;Wald&quot;", html)
        self.assertIn("Bild%20%26%20%233.jpg", html)
        self.assertIn('width="640" height="427"', html)
        self.assertTrue(html.startswith("VORHER<nav>"))
        self.assertTrue(html.endswith("</div>NACHHER"))
        self.assertEqual((folder / "Bild & #3.jpg").read_bytes(), original)
        before = {path: path.read_bytes() for path in self.site.rglob("*") if path.is_file()}
        update_galleries(self.site)
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_removed_image_disappears(self):
        folder = self.add_year("2026")
        update_galleries(self.site)
        (folder / "bild10.jpg").unlink()
        update_galleries(self.site)
        data = json.loads((self.images / "galerien.json").read_text())
        self.assertEqual(data["2026"]["images"], ["bild2.jpg"])

    def test_invalid_metadata_does_not_change_outputs(self):
        self.add_year("2025")
        update_galleries(self.site)
        before = {path: path.read_bytes() for path in self.site.rglob("*") if path.is_file()}
        folder = self.add_year("2026")
        (folder / "galerie.json").write_text('{"place":', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "ungültiges JSON"):
            update_galleries(self.site)
        for path, content in before.items():
            self.assertEqual(path.read_bytes(), content)

    def test_missing_metadata(self):
        folder = self.add_year("2026")
        (folder / "galerie.json").unlink()
        with self.assertRaisesRegex(ValueError, "fehlt"):
            update_galleries(self.site)

    def test_empty_year_and_invalid_preview(self):
        folder = self.add_year("2026", names=())
        with self.assertRaisesRegex(ValueError, "keine Bilder"):
            update_galleries(self.site)
        Image.new("RGB", (30, 60)).save(folder / "bild.jpg")
        (folder / "galerie.json").write_text(
            json.dumps({"place": "", "credit": "", "preview": "../bild.jpg"}),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "nicht gefunden"):
            update_galleries(self.site)

    def test_corrupt_preview(self):
        folder = self.add_year("2026", names=())
        (folder / "bild.jpg").write_bytes(b"kein Bild")
        with self.assertRaisesRegex(ValueError, "nicht lesbar"):
            update_galleries(self.site)

    def test_markers_required_before_writing(self):
        folder = self.add_year("2026")
        self.page.write_text("Manueller Seiteninhalt", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "HTML-Markierungen"):
            update_galleries(self.site)
        self.assertFalse((folder / "vorschau.jpg").exists())
        self.assertEqual(self.page.read_text(), "Manueller Seiteninhalt")

    def test_portrait_and_empty_place(self):
        folder = self.add_year("2026", names=(), place="", credit="")
        Image.new("RGB", (800, 1200)).save(folder / "hochformat.png")
        update_galleries(self.site)
        with Image.open(folder / "vorschau.jpg") as image:
            self.assertEqual(image.size, (427, 640))
        self.assertIn("<h2>2026</h2>", self.page.read_text())


if __name__ == "__main__":
    unittest.main()
