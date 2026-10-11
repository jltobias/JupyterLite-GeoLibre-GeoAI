"""Browser regression checks for the resource directory, charts and map protocol.

--offline-js serves the installed Plotly bundle instead of the CDN in CI.
The widget protocol uses a controlled viewer; it does not certify upstream
GeoLibre availability or execute all live-data notebooks in Pyodide.
"""
import argparse
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "book/notebooks"))
from geolibre_lite import _ESM


def main():
    from playwright.sync_api import sync_playwright
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--offline-js', action='store_true')
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width':1280,'height':900})
        from build_future_chapters import render_all
        from build_stac_discovery import render_all as render_discovery
        from build_assistant_visuals import render_all as render_assistant
        for name, markup in {**render_all(), **render_discovery(), **render_assistant()}.items():
            page.set_content('<html><body style="margin:0">'+markup+'</body></html>')
            clipped = page.evaluate("""() => {
                const bounds=document.querySelector('svg').getBoundingClientRect();
                return [...document.querySelectorAll('text')].filter(t=>{
                    const b=t.getBoundingClientRect();
                    return b.left<bounds.left || b.right>bounds.right || b.bottom>bounds.bottom;
                }).map(t=>t.textContent);
            }""")
            assert not clipped, (name,clipped)
            if args.screenshots:
                page.locator('svg').screenshot(path=str(args.screenshots/(name+'.png')))
        if args.offline_js:
            from plotly.offline import get_plotlyjs
            bundle = get_plotlyjs()
            page.route('https://cdn.plot.ly/*.js', lambda route: route.fulfill(content_type='application/javascript',body=bundle))
        base = args.base_url.rstrip('/')
        for chapter in ('futures/digital-twins','futures/map-encryption','platforms/stac-discovery','advanced/ollama-assistant'):
            page.goto(base + '/' + chapter + '.html')
            page.wait_for_function("[...document.querySelectorAll('article img')].every(i=>i.complete)")
            assert page.locator('article img').count() == 2
            assert page.evaluate("[...document.querySelectorAll('article img')].every(i=>i.naturalWidth && i.alt)")
            for width in (1280,390):
                page.set_viewport_size({'width':width,'height':900})
                if width == 390:
                    page.wait_for_function("document.querySelector('article').getBoundingClientRect().width >= innerWidth-32")
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2'), chapter
                if args.screenshots:
                    page.screenshot(path=str(args.screenshots/f'{chapter.split("/")[-1]}-{width}.png'),full_page=True,animations='disabled')
            page.set_viewport_size({'width':1280,'height':900})
        page.goto(base + '/visual-library.html')
        notebook_count = len(list((ROOT/'book/notebooks').glob('*.ipynb')))
        assert page.locator('article a',has_text='Watch').count() == notebook_count
        assert page.locator('article a',has_text='Cartoon').count() == notebook_count
        for width in (1280,390):
            page.set_viewport_size({'width':width,'height':900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
            if args.screenshots:
                page.screenshot(path=str(args.screenshots/f'visual-library-{width}.png'),full_page=True)
        page.set_viewport_size({'width':1280,'height':900})
        for number, filename, expected in (
            ('14','14_astra_terrain_3d',1),('16','16_sea_level_rise_sat_scan_geoai',3)):
            page.goto(base + '/notebooks/' + filename + '.html')
            page.locator('article iframe[srcdoc]').first.wait_for()
            frames = [f for f in page.frames if f.url == 'about:srcdoc']
            assert len(frames) == expected, (filename,len(frames))
            for frame in frames:
                frame.wait_for_function("document.querySelector('.js-plotly-plot')?._fullLayout !== undefined",timeout=45000)
            if number == '16':
                animation = frames[1]
                assert animation.locator('.slider-container').count() == 1
                rail = animation.locator('.slider-rail-touch-rect')
                bounds = rail.bounding_box()
                rail.click(position={'x':bounds['width']-2,'y':bounds['height']/2})
                with (ROOT/'book/notebooks/data/pbix_top10_sat_scan.csv').open(encoding='utf-8') as source:
                    expected_values = [float(row['flood_c_mean']) for row in csv.DictReader(source)]
                animation.wait_for_function("""expected => {
                    const plot=document.querySelector('.js-plotly-plot');
                    return plot._fullLayout.sliders[0].active === 2 &&
                        Array.from(plot._fullData[0].marker.color).length === expected.length &&
                        Array.from(plot._fullData[0].marker.color).every((v,i)=>Math.abs(v-expected[i])<1e-8);
                }""",arg=expected_values)
                assert page.locator('article table').count() >= 3
                assert page.locator('article img').count() >= 6
            scene = frames[-1]
            scene.evaluate("""() => {Plotly.relayout(document.querySelector('.js-plotly-plot'),
                {'scene.camera.eye':{x:1.8,y:-1.5,z:1.2}});} """)
            scene.wait_for_function("document.querySelector('.js-plotly-plot')._fullLayout.scene.camera.eye.x === 1.8")
            assert scene.evaluate("document.querySelector('.js-plotly-plot')._fullLayout.scene.camera.eye.x") == 1.8
            if args.screenshots:
                page.screenshot(path=str(args.screenshots/f'lab-{number}.png'),full_page=True)
            page.set_viewport_size({'width':390,'height':844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2'), filename
            page.set_viewport_size({'width':1280,'height':900})
            print(f'Chart rendering and interaction verified: lab {number}',flush=True)
        # Test the actual widget frontend, not just Python project dictionaries.
        page.route('https://viewer.test/**', lambda route: route.fulfill(content_type='text/html',body='''
            <!doctype html><title>Controlled GeoLibre viewer</title><script>
            window.received=[];
            addEventListener('message', e => {if(e.data.type==='geolibre:load-project') received.push(e.data)});
            parent.postMessage({type:'geolibre:ready'}, '*');
            </script>'''))
        page.goto(base + '/visual-library.html')
        awaitable = """async esm => {
            const module = await import(URL.createObjectURL(new Blob([esm],{type:'text/javascript'})));
            const values={project:{name:'first',layers:[]},height:'500px',app_url:'https://viewer.test/'};
            const listeners={};
            const model={get:k=>values[k], on:(k,f)=>listeners[k]=f, off:k=>delete listeners[k]};
            window.updateMap=(key,value)=>{values[key]=value;listeners['change:'+key]?.()};
            const el=document.createElement('div'); document.body.append(el);
            window.disposeMap=module.default.render({model,el});
        }"""
        page.evaluate(awaitable,_ESM)
        page.wait_for_function("document.querySelector('iframe') !== null")
        frame = next(f for f in page.frames if f != page.main_frame)
        frame.wait_for_function('received.length === 1')
        assert page.locator('iframe').get_attribute('title')
        page.evaluate("updateMap('project',{name:'updated',mapView:{pitch:60},layers:[{id:'test'}]})")
        frame.wait_for_function('received.length === 2')
        assert frame.evaluate('received[1].project.mapView.pitch') == 60
        page.evaluate("""() => {
            window.dispatchEvent(new MessageEvent('message',{source:document.querySelector('iframe').contentWindow,
                origin:'https://untrusted.test',data:{type:'geolibre:ready'}}));
            window.dispatchEvent(new MessageEvent('message',{source:window,
                origin:'https://viewer.test',data:{type:'geolibre:ready'}}));
        }""")
        assert frame.evaluate('received.length') == 2
        page.evaluate("disposeMap();updateMap('project',{name:'after-dispose'})")
        assert frame.evaluate('received.length') == 2
        browser.close()
    print(f'Browser verified: {notebook_count} resource routes, rendered Plotly views, scenario selection, 3D camera, mobile layout and guarded map-message delivery')


if __name__ == '__main__':
    main()
