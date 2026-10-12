"""Protect teaching/code alignment and distributable media references."""
import copy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_learning_media import ASSETS, LESSONS, PROFILES, transform, media_digest


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self,tag,attrs):
        self.urls.extend(v for k,v in attrs if k in {"src","href","poster"} and v)


class LearningContent(unittest.TestCase):
    def test_each_code_cell_has_current_guidance_and_rebuild_is_idempotent(self):
        paths = sorted((ROOT / "book/notebooks").glob("*.ipynb"))
        self.assertEqual({p.name[:2] for p in paths}, set(PROFILES))
        for path in paths:
            nb = json.loads(path.read_text(encoding="utf-8"))
            key = path.name[:2]
            with self.subTest(notebook=path.name):
                rebuilt = transform(copy.deepcopy(nb),key,path.name)
                self.assertEqual(rebuilt,nb)
                for index,cell in enumerate(nb["cells"]):
                    if cell["cell_type"]=="code":
                        guide=nb["cells"][index-1]
                        self.assertTrue(guide["metadata"].get("learning_guide"))
                        self.assertEqual(guide["metadata"]["code_sha256"],
                                         hashlib.sha256("".join(cell["source"]).encode()).hexdigest())

    def test_changed_code_order_is_rejected_instead_of_misexplained(self):
        path = next((ROOT / "book/notebooks").glob("00_*.ipynb"))
        nb = json.loads(path.read_text(encoding="utf-8"))
        cell = next(c for c in nb["cells"] if c["cell_type"]=="code")
        cell["source"] = ["print('replacement cell with a different purpose')"]
        with self.assertRaisesRegex(ValueError,"anchor absent"):
            transform(nb,"00",path.name)

    def test_original_code_and_saved_outputs_survive_rebuild(self):
        path = next((ROOT / "book/notebooks").glob("16_*.ipynb"))
        nb = json.loads(path.read_text(encoding="utf-8"))
        cell = next(c for c in nb["cells"] if c["cell_type"]=="code")
        cell["execution_count"] = 81
        cell["outputs"] = [{"output_type":"stream","name":"stdout","text":["Keep my result\n"]}]
        cell["metadata"]["user_note"] = "keep this too"
        expected=copy.deepcopy(cell)
        rebuilt=transform(nb,"16",path.name)
        self.assertEqual(next(c for c in rebuilt["cells"] if c["cell_type"]=="code"),expected)

    def test_markdown_preamble_is_preserved_before_generated_intro(self):
        path = ROOT / "book/notebooks/00_geolibre_quickstart.ipynb"
        nb = json.loads(path.read_text(encoding="utf-8"))
        nb["cells"][1]["metadata"]["user_note"] = "Keep this introduction"
        expected = copy.deepcopy(nb["cells"][:7])
        rebuilt = transform(nb,"00",path.name)
        self.assertEqual(rebuilt["cells"][:7],expected)
        self.assertEqual(rebuilt["cells"][7]["id"],"learn-00-intro")
        self.assertEqual(transform(copy.deepcopy(rebuilt),"00",path.name),rebuilt)

    def test_preamble_rejects_code_and_misplaced_cells(self):
        path = ROOT / "book/notebooks/00_geolibre_quickstart.ipynb"
        nb = json.loads(path.read_text(encoding="utf-8"))
        invalid = copy.deepcopy(nb)
        invalid["cells"][1]["cell_type"] = "code"
        with self.assertRaisesRegex(ValueError,"must be Markdown"):
            transform(invalid,"00",path.name)
        invalid = copy.deepcopy(nb)
        invalid["cells"][1]["metadata"].pop("learning_preamble")
        with self.assertRaisesRegex(ValueError,"must immediately follow the title"):
            transform(invalid,"00",path.name)

    def test_accessible_media_and_local_links_exist_for_every_lesson(self):
        for key,p in PROFILES.items():
            directory=ASSETS/key
            with self.subTest(lesson=key):
                for name in ("infographic.svg","cartoon.svg"):
                    root=ET.parse(directory/name).getroot()
                    self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"))
                    self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}desc"))
                movie=(directory/"walkthrough.mp4").read_bytes()
                self.assertEqual(movie[4:8],b"ftyp")
                self.assertLess(movie.find(b"moov"),movie.find(b"mdat"))  # progressive playback
                self.assertTrue((directory/"poster.png").read_bytes().startswith(b"\x89PNG"))
                self.assertEqual((directory/"media-source.sha256").read_text().strip(),media_digest(key,p))
                captions=(directory/"captions.vtt").read_text(encoding="utf-8")
                self.assertEqual(captions.count(" --> "),4)
                self.assertIn("00:00:32.000",captions)
                player=(directory/"watch.html").read_text(encoding="utf-8")
                self.assertIn("<video controls playsinline preload=\"none\"",player)
                self.assertNotIn("autoplay",player)
                self.assertIn("Transcript and code landmarks",player)
                parser=References(); parser.feed(player)
                for url in parser.urls:
                    parsed=urlsplit(url)
                    if parsed.scheme or parsed.path.endswith("lab/index.html"):
                        continue
                    target=(directory/parsed.path).resolve()
                    self.assertTrue(target.is_relative_to(ASSETS),url)
                    self.assertTrue(target.is_file(),url)


if __name__=="__main__":
    unittest.main()
