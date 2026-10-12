"""Check the local presentation and optionally execute all six cells in real Pyodide.

Scientific packages are downloaded from official Pyodide/PyPI infrastructure.
No outbreak data API, local Ollama service or external GeoLibre UI is exercised.
The Pyodide check validates widget callbacks, not the JupyterLab widget manager.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT/'book/notebooks'


def check_runtime(page, runtime_url):
    if runtime_url.endswith('.mjs'):
        page.evaluate('''async url => {
            const {loadPyodide} = await import(url);
            window.runtime = await loadPyodide();
        }''', runtime_url)
    else:
        page.add_script_tag(url=runtime_url)
        page.evaluate('async () => {window.runtime = await loadPyodide();}')
    files = {name:(NOTEBOOKS/name).read_text(encoding='utf-8') for name in (
        'cholera_demo.py','data/cholera/cholera_deaths.csv','data/cholera/pumps.csv')}
    page.evaluate('''files => {
        runtime.FS.mkdirTree('/home/pyodide/data/cholera');
        for(const [name,contents] of Object.entries(files))
            runtime.FS.writeFile('/home/pyodide/'+name,contents);
        runtime.runPython("import os; os.environ['MPLBACKEND'] = 'agg'");
    }''',files)
    notebook = json.loads((NOTEBOOKS/'21_cholera_geoai_first_steps.ipynb').read_text(encoding='utf-8'))
    cells = [''.join(cell['source']) for cell in notebook['cells'] if cell['cell_type']=='code']
    for i, code in enumerate(cells,1):
        page.evaluate('async code => {await runtime.runPythonAsync(code);}',code)
        print(f'Real Pyodide: executed cholera cell {i}/{len(cells)}',flush=True)
    result = page.evaluate('''async () => await runtime.runPythonAsync(`
import json, sys
from unittest.mock import patch
assert sys.platform == 'emscripten'
assert len(deaths) == 250 and int(deaths.DEATHS.sum()) == 489 and len(pumps) == 8
assert cholera_map is None  # default never loads a hosted map
actual = {}
for radius in (25,50,100):
    radius_control.value = radius
    fitted = cluster_locations(deaths, radius)
    np.testing.assert_array_equal(current_labels, fitted)
    actual[str(radius)] = list(map(int,fitted))
    previous = current_labels.copy()
    with patch('cholera_demo.DBSCAN', side_effect=AssertionError('Pump toggle refitted')):
        pump_control.value = not pump_control.value
    np.testing.assert_array_equal(current_labels, previous)
assert len(plt.get_fignums()) == 3  # only the three retained baseline/group/reveal figures
json.dumps({'python':sys.version.split()[0], 'labels':actual})
`)''')
    result = json.loads(result)
    expected = json.loads((NOTEBOOKS/'assets/cholera/results.json').read_text())
    for radius, labels in result['labels'].items():
        assert labels == expected['scenarios'][radius]['labels'],radius
    print('Real Pyodide',result['python'],': all 750 labels match saved results; pump toggles do not refit',flush=True)


def main():
    from playwright.sync_api import sync_playwright
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',required=True)
    parser.add_argument('--pyodide',action='store_true')
    parser.add_argument('--runtime-url',help='Override official Pyodide entry point for cross-version testing')
    parser.add_argument('--screenshots',type=Path)
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True,exist_ok=True)
    base = args.base_url.rstrip('/')
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width':1280,'height':1000})
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        # Inspect the actual SVG text bounds, including the 12-group legend.
        for asset in sorted((NOTEBOOKS/'assets/cholera').glob('*.svg')):
            page.goto(base+'/lite/files/assets/cholera/'+asset.name)
            clipped = page.evaluate('''() => {
                const svg=document.querySelector('svg').getBoundingClientRect();
                return [...document.querySelectorAll('text')].filter(t=>{
                    const b=t.getBoundingClientRect();
                    return b.left<svg.left || b.right>svg.right || b.bottom>svg.bottom;
                }).map(t=>t.textContent);
            }''')
            assert not clipped,(asset.name,clipped)
            if args.screenshots:
                page.locator('svg').screenshot(path=str(args.screenshots/(asset.stem+'.png')))
        page.goto(base+'/lite/files/assets/cholera/presentation.html')
        assert page.locator('#radius').is_disabled()
        for stage in ('groups','pumps'):
            page.locator(f'[data-stage={stage}]').click()
            assert page.locator(f'[data-stage={stage}]').get_attribute('aria-pressed')=='true'
            for radius, groups, unassigned in ((25,12,42),(50,1,7),(100,1,0)):
                page.select_option('#radius',str(radius))
                assert page.locator('#map-image').get_attribute('src')==f'{stage}-{radius}.svg'
                assert f'{groups} group(s) · {unassigned} unassigned' in page.locator('#status').inner_text()
                page.wait_for_function("document.querySelector('#map-image').complete && document.querySelector('#map-image').naturalWidth > 0")
        page.select_option('#radius','25')
        for width in (1280,390):
            page.set_viewport_size({'width':width,'height':1000})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
            if args.screenshots:
                page.screenshot(path=str(args.screenshots/f'presentation-{width}.png'),full_page=True)
        page.locator('[data-stage=map]').click()
        assert page.locator('#radius').is_disabled()
        assert page.locator('#map-image').get_attribute('src')=='map.svg'
        assert not errors,errors  # no JavaScript errors tolerated in the new presentation
        # Book integration: real local iframe and static backup images.
        page.goto(base+'/presentations/cholera-five-minutes.html')
        frame = page.frame_locator('article iframe')
        frame.locator('[data-stage=groups]').click()
        assert '7 unassigned' in frame.locator('#status').inner_text()
        for width in (1280,390):
            page.set_viewport_size({'width':width,'height':1000})
            page.wait_for_function("[...document.querySelectorAll('article img')].every(i=>i.complete)")
            assert page.locator('article img').count()==3
            assert page.evaluate("[...document.querySelectorAll('article img')].every(i=>i.naturalWidth && i.alt)")
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
            if args.screenshots:
                page.screenshot(path=str(args.screenshots/f'book-{width}.png'),full_page=True)
        # Existing Jupyter Book 1 / sphinx-thebe output can declare this constant
        # twice. Do not mistake this unrelated, nonfatal template error for an
        # error in the new iframe; all its controls were explicitly exercised.
        known = "Identifier 'THEBE_JS_URL' has already been declared"
        assert all(error == known for error in errors),errors
        if errors:
            print('Existing Book template warning:',known,flush=True)
        print('Presentation: seven SVGs, all controls, desktop/mobile and Book integration passed',flush=True)
        if args.pyodide:
            page.goto(base+'/intro.html')
            schema=json.loads((ROOT/'site/lite/extensions/@jupyterlite/pyodide-kernel-extension/static/schema/kernel.v0.schema.json').read_text())
            check_runtime(page,args.runtime_url or schema['properties']['pyodideUrl']['default'])
        browser.close()


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        message=f'Cholera browser check: {type(error).__name__}: {error}'
        print('::error::'+message.replace('%','%25').replace('\r','%0D').replace('\n','%0A')[:2500])
        raise
