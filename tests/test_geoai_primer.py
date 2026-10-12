"""Keep the field guide reproducible, linked and accessible without live services."""
from pathlib import Path
import re
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
        self.assertIn("No Esri graphics, videos or text passages are reproduced",section)
        self.assertIn("not validated forecasts",section)
        self.assertIn("11 October 2026",section)
        self.assertIn("Esri. (n.d.).",references)
        # Refer readers to the original source; don't silently embed its assets.
        self.assertNotIn("![",section)
        self.assertNotIn("<iframe",section)

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
