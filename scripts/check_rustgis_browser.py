"""Inspect the RustGIS lesson and run its default cells in real browser Pyodide.

Does not install native RustGIS or claim to test its external web application.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT/'book/notebooks'
STEM = '22_rustgis_geoai_bridge'


def main():
    from playwright.sync_api import sync_playwright
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--pyodide', action='store_true')
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    base = args.base_url.rstrip('/')
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width':1280, 'height':1000})
        page.goto(base+'/lite/files/assets/rustgis/bridge.svg')
        clipped = page.evaluate('''() => {
            const b=document.querySelector('svg').getBoundingClientRect();
            return [...document.querySelectorAll('text')].filter(t=>{
                const r=t.getBoundingClientRect();
                return r.left<b.left || r.right>b.right || r.bottom>b.bottom;
            }).map(t=>t.textContent);
        }''')
        assert not clipped, clipped
        if args.screenshots:
            page.locator('svg').screenshot(path=str(args.screenshots/'rustgis-bridge.png'))
        for slug in ('platforms/rustgis', 'notebooks/'+STEM):
            for width in (1280, 390):
                page.set_viewport_size({'width':width, 'height':1000})
                response = page.goto(base+'/'+slug+'.html')
                assert response.ok, slug
                assert page.locator('article').get_by_role('link', name='RustGIS', exact=False).count()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (slug,width)
                assert page.locator('article img').count()
                if args.screenshots:
                    page.screenshot(path=str(args.screenshots/(slug.split('/')[-1]+f'-{width}.png')),full_page=True)
        print('RustGIS chapter, notebook and runtime diagram: desktop/mobile checks passed', flush=True)
        if args.pyodide:
            schema = json.loads((ROOT/'site/lite/extensions/@jupyterlite/pyodide-kernel-extension/static/schema/kernel.v0.schema.json').read_text())
            url = schema['properties']['pyodideUrl']['default']
            page.goto(base+'/intro.html')
            if url.endswith('.mjs'):
                page.evaluate('''async url => {const {loadPyodide}=await import(url);
                    window.runtime=await loadPyodide();}''', url)
            else:
                page.add_script_tag(url=url)
                page.evaluate('async () => {window.runtime=await loadPyodide();}')
            page.evaluate('''source => {
                runtime.FS.writeFile('/home/pyodide/rustgis_bridge.py',source);
                runtime.runPython("import os; os.environ['MPLBACKEND']='agg'");
            }''', (NOTEBOOKS/'rustgis_bridge.py').read_text(encoding='utf-8'))
            nb = json.loads((NOTEBOOKS/(STEM+'.ipynb')).read_text(encoding='utf-8'))
            cells = [''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code']
            for i, source in enumerate(cells, 1):
                page.evaluate('async code => {await runtime.runPythonAsync(code);}', source)
                print(f'Real Pyodide: RustGIS lesson cell {i}/{len(cells)} passed', flush=True)
            result = page.evaluate('''async () => await runtime.runPythonAsync(`
assert sys.platform == 'emscripten'
assert comparison_map is None
assert 'rustgis' not in sys.modules
assert group_counts(grouped) == {-1:2, 0:9, 1:9}
assert group_counts(fit_groups(sites, 150)) == {-1:20}
assert json.loads(data_path.read_text()) == grouped
assert json.loads(provenance_path.read_text())['neighbor_radius_m'] == 350
json.dumps(grouped)
`)''')
            expected = json.loads((NOTEBOOKS/'data/rustgis-groups.geojson').read_text())
            assert json.loads(result) == expected
            print('Real Pyodide result and exports match the public snapshot; native RustGIS was not imported', flush=True)
        browser.close()


if __name__ == '__main__':
    main()
