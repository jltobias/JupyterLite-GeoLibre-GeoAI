"""Keep the field guide reproducible, linked and accessible without live services."""
from pathlib import Path
import hashlib
import json
import re
import struct
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from build_geoai_primer import ASSETS, render_all


class GeoAIPrimer(unittest.TestCase):
    def test_all_authored_diagrams_are_current_and_accessible(self):
        figures=render_all()
        self.assertEqual(len(figures),24)
        self.assertEqual({p.stem for p in ASSETS.glob("*.svg")},set(figures))
        for name,expected in figures.items():
            with self.subTest(diagram=name):
                self.assertEqual((ASSETS/(name+".svg")).read_text(encoding="utf-8"),expected)
                svg=ET.fromstring(expected)
                ns={"s":"http://www.w3.org/2000/svg"}
                self.assertEqual(svg.attrib["role"],"img")
                self.assertEqual(svg.attrib["aria-labelledby"],"title desc")
                self.assertTrue(svg.find("s:title",ns).text)
                self.assertGreater(len(svg.find("s:desc",ns).text),100)
                self.assertIsNone(svg.find("s:script",ns))
                self.assertIsNone(svg.find("s:image",ns))  # no hidden remote assets

    def test_chapters_navigation_local_links_and_image_alternatives(self):
        chapters=sorted((ROOT/"book/geoai").glob("*.md"))
        self.assertEqual(len(chapters),7)
        toc=(ROOT/"book/_toc.yml").read_text(encoding="utf-8")
        images=set()
        for chapter in chapters:
            with self.subTest(chapter=chapter.name):
                self.assertIn("file: geoai/"+chapter.stem,toc)
                source=chapter.read_text(encoding="utf-8")
                self.assertIn("**Read the picture:**",source)
                for bang,label,target in re.findall(r"(!?)\[([^\]]*)\]\(([^)]+)\)",source):
                    if bang: self.assertGreater(len(label),30)
                    if target.startswith(("https://","http://","#")): continue
                    path=(chapter.parent/target.split("#")[0]).resolve()
                    self.assertTrue(path.is_relative_to(ROOT/"book"),target)
                    self.assertTrue(path.is_file(),target)
                    if path.parent==ASSETS: images.add(path.stem)
        self.assertEqual(images,set(render_all()))

    def test_atlas_accounts_for_every_notebook(self):
        atlas=(ROOT/"book/geoai/notebook-atlas.md").read_text(encoding="utf-8")
        notebooks=sorted((ROOT/"book/notebooks").glob("*.ipynb"))
        self.assertEqual(len(notebooks),22)
        for notebook in notebooks:
            self.assertIn(f"../notebooks/{notebook.name}",atlas)

    def test_esri_attribution_and_teaching_boundaries(self):
        url="https://www.esri.com/en-us/capabilities/geoai/overview"
        primer=(ROOT/"book/geoai/primer.md").read_text(encoding="utf-8")
        references=(ROOT/"book/references.md").read_text(encoding="utf-8")
        register=(ROOT/"DATA_SOURCES.md").read_text(encoding="utf-8")
        for source in (primer,references,register):
            self.assertIn(url,source)
        section=primer.split("## What Esri's overview adds\n",1)[1].split("\n## ",1)[0]
        self.assertIn("this book's teaching interpretation",section)
        self.assertIn("not affiliated with or endorsed by Esri",section)
        self.assertIn("No Esri videos or text passages are reproduced",section)
        self.assertIn("<esri-geoai-diagrams>",section)
        self.assertIn("not validated forecasts",section)
        self.assertIn("11 October 2026",section)
        self.assertIn("Esri. (n.d.).",references)
        # The overview discussion is a paraphrase; separately credited images come from the docs.
        self.assertNotIn("![",section)
        self.assertNotIn("<iframe",section)

    def test_esri_diagrams_have_unchanged_assets_and_figure_level_sources(self):
        assets=ROOT/"book/assets/esri"
        metadata=json.loads((assets/"provenance.json").read_text(encoding="utf-8"))
        primer=(ROOT/"book/geoai/primer.md").read_text(encoding="utf-8")
        references=(ROOT/"book/references.md").read_text(encoding="utf-8")
        register=(ROOT/"DATA_SOURCES.md").read_text(encoding="utf-8")
        self.assertEqual(metadata["creator"],"Esri")
        self.assertEqual(len(metadata["images"]),2)
        self.assertEqual({p.name for p in assets.glob("*.png")},
                         {item["file"] for item in metadata["images"]})
        section=primer.split("## Start with Esri's two diagrams\n",1)[1].split("\n## ",1)[0]
        self.assertEqual(section.count("**Image credit: Esri.**"),2)
        for item in metadata["images"]:
            with self.subTest(image=item["file"]):
                data=(assets/item["file"]).read_bytes()
                self.assertEqual(data[:8],b"\x89PNG\r\n\x1a\n")
                self.assertEqual(hashlib.sha256(data).hexdigest(),item["sha256"])
                self.assertEqual(struct.unpack(">II",data[16:24]),(item["width"],item["height"]))
                self.assertIn(f'](../assets/esri/{item["file"]})',section)
                self.assertIn(f'href="../_images/{item["file"]}" target="_blank" rel="noopener"',section)
                self.assertIn(item["source_url"],section)
                self.assertIn(item["source_url"],references)
        for source in (primer,references,register):
            self.assertIn(metadata["source_page"],source)
            self.assertIn(metadata["related_overview"],source)
            self.assertNotIn("No Esri graphics, videos or text passages are reproduced",source)
            self.assertNotIn("No Esri media or text passages are reproduced",source)
        self.assertIn("not deep learning",section)
        self.assertIn("spatial analysis without a fitted AI model",section)
        self.assertIn("not an Esri evaluation",section)
        self.assertIn("12 October 2026",section)
        self.assertIn("(esri-geoai-diagram-reference)=",references)
        self.assertIn("<esri-geoai-diagram-reference>",section)
        self.assertLess(primer.index("(esri-geoai-diagrams)="),primer.index("## Is GeoAI different"))

    def test_aws_attribution_and_browser_teaching_boundaries(self):
        url="https://aws.amazon.com/what-is/geospatial-artificial-intelligence/"
        primer=(ROOT/"book/geoai/primer.md").read_text(encoding="utf-8")
        references=(ROOT/"book/references.md").read_text(encoding="utf-8")
        register=(ROOT/"DATA_SOURCES.md").read_text(encoding="utf-8")
        for source in (primer,references,register):
            self.assertIn(url,source)
        self.assertIn("(aws-geoai-perspective)=",primer)
        section=primer.split("## What AWS's overview adds\n",1)[1].split("\n## ",1)[0]
        for boundary in ("this book's teaching interpretation", "not affiliated with or endorsed by AWS",
                         "No AWS graphics, videos or text passages are reproduced",
                         "GeoAI does not require AWS or cloud execution",
                         "no AWS account, SDK or service dependency is added",
                         "not a result reported by AWS", "12 October 2026"):
            self.assertIn(boundary,section)
        for notebook in ("21_cholera_geoai_first_steps", "03_earth_observation_geoai", "15_astra_network_accessibility"):
            self.assertIn(f"../notebooks/{notebook}.ipynb",section)
        self.assertIn("Amazon Web Services. (n.d.).",references)
        self.assertIn("{ref}`AWS perspective in the primer <aws-geoai-perspective>`",references)
        self.assertNotIn("![",section)
        self.assertNotIn("<iframe",section)

    def test_spatial_intelligence_definition_and_notebook_boundaries(self):
        url="https://hai.stanford.edu/ai-definitions/what-is-spatial-intelligence"
        primer=(ROOT/"book/geoai/primer.md").read_text(encoding="utf-8")
        references=(ROOT/"book/references.md").read_text(encoding="utf-8")
        register=(ROOT/"DATA_SOURCES.md").read_text(encoding="utf-8")
        for source in (primer,references,register):
            self.assertIn(url,source)
        self.assertIn("(spatial-intelligence)=",primer)
        section=primer.split("## What is spatial intelligence?\n",1)[1].split("\n## ",1)[0]
        for boundary in ("this book's teaching interpretation", "not synonyms",
                         "a 3D map is not by itself spatial intelligence",
                         "12 October 2026", "No Stanford artwork or text passage is reproduced"):
            self.assertIn(boundary,section)
        for notebook in ("21_cholera_geoai_first_steps", "14_astra_terrain_3d", "15_astra_network_accessibility"):
            self.assertIn(f"../notebooks/{notebook}.ipynb",section)
        self.assertIn("{ref}`spatial-intelligence introduction <spatial-intelligence>`",references)

    def test_thinking_and_connection_book_references(self):
        primer=(ROOT/"book/geoai/primer.md").read_text(encoding="utf-8")
        references=(ROOT/"book/references.md").read_text(encoding="utf-8")
        register=(ROOT/"DATA_SOURCES.md").read_text(encoding="utf-8")
        for url in ("https://www.goodreads.com/en/book/show/97030.Six_Thinking_Hats",
                    "https://www.goodreads.com/en/book/show/16233761-rewire",
                    "https://ethanzuckerman.com/books/rewire/"):
            for source in (primer,references,register):
                self.assertIn(url,source)
        for label in ("six-thinking-hats-reference", "rewire-reference"):
            self.assertIn(f"({label})=",references)
            self.assertIn(f"<{label}>`",primer)
        for entry in ("de Bono, E. (2000)", "Zuckerman, E. (2013)",
                      "9780140296662", "9780393082838", "Penguin Books", "W. W. Norton"):
            self.assertIn(entry,references)
        self.assertIn("not an original seventh",primer)
        self.assertIn("not fixed personality types",primer)
        self.assertIn("not been verified as a verbatim quotation",primer)
        self.assertIn("not a mathematical equation or proof of improved health outcomes",primer)

    def test_supplied_infographics_preserve_provenance_and_enlargement_links(self):
        primer=(ROOT/"book/geoai/primer.md").read_text(encoding="utf-8")
        assets=ROOT/"book/assets/rewiring"
        metadata=json.loads((assets/"provenance.json").read_text(encoding="utf-8"))
        data=(assets/metadata["asset"]).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(),metadata["sha256"])
        self.assertEqual(data[:8],b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II",data[16:24]),(metadata["width"],metadata["height"]))
        self.assertIn(metadata["source_revision"],primer)
        references=(ROOT/"book/references.md").read_text(encoding="utf-8")
        self.assertIn("**Artwork source project:**",primer)
        self.assertIn(f'[**JupyterLite-Rewiring-Global-Health**]({metadata["source_repository"]})',primer)
        self.assertIn("{ref}`full repository reference <rewiring-repository-reference>`",primer)
        self.assertIn("(rewiring-repository-reference)=",references)
        self.assertIn(f'[JupyterLite-Rewiring-Global-Health]({metadata["source_repository"]})',references)
        hats=ROOT/"book/notebooks/assets/six-thinking-hats-global-health.png"
        self.assertEqual(hashlib.sha256(hats.read_bytes()).hexdigest(),
                         "979853bfd774236a6a807d00a826e0cc6fccfc982e21f9fc3b8aa6c2a09a33bf")
        for target in ("../notebooks/assets/six-thinking-hats-global-health.png",
                       "../assets/rewiring/rewiring-global-health.png"):
            self.assertEqual(primer.count(f"]({target})"),1)
            # HTML links open Sphinx's image asset; Markdown file links force a download.
            self.assertIn(f'href="../_images/{Path(target).name}" target="_blank" rel="noopener"',primer)
        self.assertIn("Its pictured buttons are part of a static image",primer)
        self.assertIn("interpretation",metadata)
        self.assertIn("rights",metadata)

    def test_explanatory_arithmetic(self):
        # Protect the explicitly invented cohort illustration from misleading ratios.
        self.assertEqual(6000/8000,0.75)
        self.assertEqual(6000/10000,0.60)
        self.assertEqual(5400/6000,0.90)
        self.assertEqual(5400/10000,0.54)
        chart=render_all()["denominators"]
        self.assertIn("75%",chart)
        self.assertIn("60%",chart)
        self.assertIn("Entirely invented",chart)


if __name__=="__main__":
    unittest.main()
