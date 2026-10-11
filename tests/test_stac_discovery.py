"""Check the discovery chapter, original graphics and copyable Python example."""
import contextlib
import io
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_stac_discovery import ASSETS, render_all

CHAPTER = ROOT/'book/platforms/stac-discovery.md'


class StacDiscovery(unittest.TestCase):
    def test_diagrams_are_reproducible_and_accessible(self):
        graphics = render_all()
        self.assertEqual(len(graphics), 2)
        for name, content in graphics.items():
            self.assertEqual((ASSETS/(name+'.svg')).read_text(encoding='utf-8'), content)
            root = ET.fromstring(content)
            ns = {'s':'http://www.w3.org/2000/svg'}
            self.assertTrue(root.find('s:title', ns).text)
            self.assertTrue(root.find('s:desc', ns).text)
            self.assertIsNone(root.find('.//s:script', ns))
            self.assertIsNone(root.find('.//s:image', ns))

    def test_navigation_and_attribution(self):
        chapter = CHAPTER.read_text(encoding='utf-8')
        self.assertIn('file: platforms/stac-discovery', (ROOT/'book/_toc.yml').read_text())
        for file in ('README.md', 'book/intro.md', 'book/visual-library.md', 'book/references.md'):
            self.assertIn('platforms/stac-discovery.', (ROOT/file).read_text(encoding='utf-8'))
        for path in (ROOT/'book/notebooks').glob('0[78]_*.ipynb'):
            self.assertIn('platforms/stac-discovery.html', path.read_text(encoding='utf-8'))
        for credit in ('JupyterLite-STAC-Browser contributors', 'Qiusheng Wu',
                       'radiantearth/stac-browser', '563ed599a42188a4b476cfec44173e97fa06e3cc'):
            self.assertIn(credit, chapter)
        for bang, label, target in re.findall(r'(!?)\[([^\]]*)\]\(([^)]+)\)', chapter):
            if bang:
                self.assertGreater(len(label), 40)
            if not target.startswith(('https://', '#')):
                self.assertTrue((CHAPTER.parent/target.split('#')[0]).is_file(), target)

    def run_example(self, item):
        code = re.findall(r'```python\n(.*?)\n```', CHAPTER.read_text(encoding='utf-8'), re.S)
        self.assertEqual(len(code), 1)
        output = io.StringIO()
        with patch.object(Path, 'read_text', return_value=json.dumps(item)) as reader:
            with contextlib.redirect_stdout(output):
                exec(compile(code[0], str(CHAPTER), 'exec'), {})
            reader.assert_called_once_with(encoding='utf-8')
        return output.getvalue()

    def test_python_example_inspects_assets_without_fetching_them(self):
        result = self.run_example({
            'type':'Feature', 'stac_version':'1.1.0', 'id':'invented-record',
            'collection':'teaching-only', 'geometry':None, 'links':[],
            'properties':{'datetime':'2020-01-01T00:00:00Z', 'year':2019},
            'assets':{'data':{'href':'https://example.invalid/unreachable.tif',
                              'type':'image/tiff', 'roles':['data']},
                      'preview':{'href':'https://example.invalid/preview.png',
                                 'type':'image/png', 'roles':['thumbnail']}}
        })
        self.assertIn('2019', result)
        self.assertIn('data | image/tiff | roles: data', result)
        self.assertIn('preview | image/png | roles: thumbnail', result)
        self.assertNotIn('https://', result)

    def test_python_example_handles_missing_metadata_and_rejects_wrong_exports(self):
        result = self.run_example({'type':'Feature', 'stac_version':'1.1.0',
            'id':'interval-example', 'properties':{'datetime':None,
                'start_datetime':'2020-01-01T00:00:00Z', 'end_datetime':'2020-12-31T23:59:59Z'},
            'assets':{}})
        self.assertIn('2020-12-31', result)
        self.assertIn('unknown', result)
        self.assertIn('No assets advertised', result)
        for document in ({'type':'FeatureCollection','features':[]}, {'query':{}}, []):
            with self.assertRaisesRegex(ValueError, 'one exported STAC Item'):
                self.run_example(document)


if __name__ == '__main__':
    unittest.main()
