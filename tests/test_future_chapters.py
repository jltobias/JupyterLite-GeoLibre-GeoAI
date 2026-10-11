"""Guard presentation attribution, diagram reproducibility and capability scope."""
import json
from pathlib import Path
import re
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_future_chapters import ASSETS,render_all


class FutureChapters(unittest.TestCase):
    def test_four_original_graphics_are_current_and_accessible(self):
        graphics=render_all()
        self.assertEqual(len(graphics),4)
        for name,value in graphics.items():
            self.assertEqual((ASSETS/(name+'.svg')).read_text(encoding='utf-8'),value)
            root=ET.fromstring(value)
            ns={'s':'http://www.w3.org/2000/svg'}
            self.assertTrue(root.find('s:title',ns).text)
            self.assertTrue(root.find('s:desc',ns).text)
            self.assertIsNone(root.find('s:image',ns))
            self.assertIsNone(root.find('s:script',ns))

    def test_local_links_and_toc_match_chapters(self):
        toc=(ROOT/'book/_toc.yml').read_text(encoding='utf-8')
        for chapter in sorted((ROOT/'book/futures').glob('*.md')):
            self.assertIn('file: futures/'+chapter.stem,toc)
            source=chapter.read_text(encoding='utf-8')
            self.assertIn('**Read the picture:**',source)
            self.assertIn('Sources and attribution',source)
            for bang,label,target in re.findall(r'(!?)\[([^\]]*)\]\(([^)]+)\)',source):
                if bang:
                    self.assertGreater(len(label),40)
                if target.startswith(('http://','https://','#')):
                    continue
                path=(chapter.parent/target.split('#')[0]).resolve()
                self.assertTrue(path.is_relative_to(ROOT/'book'))
                self.assertTrue(path.is_file(),target)

    def test_provenance_and_implementation_limits(self):
        manifest=json.loads((ASSETS/'provenance.json').read_text(encoding='utf-8'))
        self.assertEqual([s['pdf_pages'] for s in manifest['sources']],[22,36])
        for source in manifest['sources']:
            self.assertRegex(source['sha256'],r'^[a-f0-9]{64}$')
            chapter=(ROOT/'book'/source['chapter']).read_text(encoding='utf-8')
            for name in source['cover_credits']:
                self.assertIn(name,chapter)
            self.assertIn(source['filename'],chapter)
        twin=(ROOT/'book/futures/digital-twins.md').read_text(encoding='utf-8')
        security=(ROOT/'book/futures/map-encryption.md').read_text(encoding='utf-8')
        self.assertIn('not established Starsim/CHSP compatibility',twin)
        self.assertIn('No Gaborone disease model or patient-level data',twin)
        self.assertIn('not an implemented encryption service',security)
        self.assertIn('No security mechanism or cryptographic dependency is added',security)


if __name__=='__main__':
    unittest.main()
