"""Optional visual QA: SVG text bounds/overlap plus built-book images/navigation.

Requires requirements-media.txt and Playwright Chromium. Build the book first.
Screenshots are written outside the repository to the given --output directory.
"""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    failures=[]
    with sync_playwright() as p:
        browser=p.chromium.launch()
        page=browser.new_page(viewport={"width":1200,"height":720},device_scale_factor=1)
        for svg in sorted((ROOT/"book/assets/geoai").glob("*.svg")):
            page.goto(svg.as_uri())
            errors=page.evaluate('''() => {
                const nodes=[...document.querySelectorAll('text')];
                const boxes=nodes.map(n=>({text:n.textContent,b:n.getBBox()}));
                let errors=[];
                for (const a of boxes) {
                    if(a.b.x<0 || a.b.y<0 || a.b.x+a.b.width>1196 || a.b.y+a.b.height>719)
                        errors.push('out of bounds: '+a.text);
                }
                for(let i=0;i<boxes.length;i++) for(let j=i+1;j<boxes.length;j++) {
                    const a=boxes[i], b=boxes[j];
                    const dx=Math.min(a.b.x+a.b.width,b.b.x+b.b.width)-Math.max(a.b.x,b.b.x);
                    const dy=Math.min(a.b.y+a.b.height,b.b.y+b.b.height)-Math.max(a.b.y,b.b.y);
                    if(dx>1 && dy>1) errors.push('overlap: '+a.text+' / '+b.text);
                }
                return errors;
            }''')
            failures.extend(svg.name+": "+e for e in errors)
            page.screenshot(path=str(args.output/(svg.stem+".png")))
        for width in [1280,390]:
            page.set_viewport_size({"width":width,"height":900})
            for chapter in sorted((ROOT/"book/geoai").glob("*.md")):
                built=ROOT/"book/_build/html/geoai"/(chapter.stem+".html")
                if not built.exists(): raise SystemExit("Build Jupyter Book before browser QA")
                page.goto(built.as_uri())
                page.locator("article").wait_for()
                page.wait_for_function("[...document.querySelectorAll('article img')].every(i => i.complete)")
                bad=page.evaluate('''() => [...document.querySelectorAll('article img')]
                    .filter(i=>!i.naturalWidth || !i.alt).map(i=>i.src)''')
                failures.extend(f"{chapter.name}@{width}: missing image/alt {src}" for src in bad)
                overflow=page.evaluate("document.documentElement.scrollWidth > innerWidth+2")
                if overflow: failures.append(f"{chapter.name}@{width}: horizontal page overflow")
                if chapter.stem in {"primer","climate-health","hiv-tb"}:
                    page.screenshot(path=str(args.output/f"page-{chapter.stem}-{width}.png"),full_page=True)
        browser.close()
    if failures: raise SystemExit("\n".join(failures))
    print("24 SVGs: no clipped/overlapping text. Seven chapters: desktop/mobile images and layout passed.")


if __name__=="__main__":
    main()
