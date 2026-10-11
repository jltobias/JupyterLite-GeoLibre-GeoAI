"""Protect source-image integrity, visible attribution and beginner navigation."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from extract_platform_graphics import ASSETS, FIGURES, check, png_dimensions


class PlatformChapters(unittest.TestCase):
    def test_presentation_images_match_provenance(self):
        manifest = check()
        self.assertEqual(len(manifest["figures"]), 7)
        self.assertEqual(sum(f["bytes"] for f in manifest["figures"]), 4431332)

    def test_navigation_images_and_relative_links(self):
        toc = (ROOT / "book/_toc.yml").read_text(encoding="utf-8")
        for chapter, count in (("jupyterlite", 3), ("geolibre", 4)):
            with self.subTest(chapter=chapter):
                self.assertIn("file: platforms/" + chapter, toc)
                path = ROOT / "book/platforms" / (chapter + ".md")
                source = path.read_text(encoding="utf-8")
                images = []
                for bang, label, target in re.findall(r"(!?)\[([^\]]*)\]\(([^)]+)\)", source):
                    if target.startswith(("https://", "http://", "#")):
                        continue
                    resolved = (path.parent / target.split("#")[0]).resolve()
                    self.assertTrue(resolved.is_relative_to(ROOT / "book"), target)
                    self.assertTrue(resolved.is_file(), target)
                    if bang:
                        self.assertGreater(len(label), 70)
                        self.assertEqual(resolved.parent, ASSETS)
                        images.append(resolved.name)
                self.assertEqual(len(images), count)
                self.assertEqual(set(images), {f[0] for f in FIGURES if f[3] == chapter})
                self.assertEqual(source.count("**Read the picture:**"), count)
                self.assertEqual(source.count("[Open full-size graphic]"), count)
                self.assertIn("provenance.json", source)
                for filename, slide, _, which, _, url in FIGURES:
                    if which != chapter:
                        continue
                    self.assertIn(f"Presentation slide {slide}.", source)
                    if url:
                        self.assertIn(url, source)

    def test_citation_and_runtime_boundaries_are_visible(self):
        geo = (ROOT / "book/platforms/geolibre.md").read_text(encoding="utf-8")
        lite = (ROOT / "book/platforms/jupyterlite.md").read_text(encoding="utf-8")
        for required in ("Qiusheng Wu", "10.5281/zenodo.20785400", "OpenStreetMap",
                         "GEOLIBRE-LICENSE.txt", "geolibre_lite.LiteMap", "geolibre==3.0.0",
                         "concept DOI", "spatialthoughts", "giswqs"):
            self.assertIn(required, geo)
        for required in ("JupyterLite Contributors", "Pyodide", "JUPYTERLITE-LICENSE.txt",
                         "Saving in JupyterLite does not commit or push to GitHub",
                         "Compiled packages are possible", "not automatic guarantees"):
            self.assertIn(required, lite)
        self.assertIn("Copyright (c) 2026 Qiusheng Wu", (ASSETS / "GEOLIBRE-LICENSE.txt").read_text())
        self.assertIn("JupyterLite Contributors", (ASSETS / "JUPYTERLITE-LICENSE.txt").read_text())

    def test_invalid_image_header_is_rejected(self):
        for raw in (b"not a PNG", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"):
            with self.subTest(header=raw), self.assertRaises(ValueError):
                png_dimensions(raw)


if __name__ == "__main__":
    unittest.main()
