"""Optional browser QA for teaching graphics and the built video companions.

python scripts/check_learning_browser.py --base-url http://127.0.0.1:8765
Requires requirements-media.txt and a Chromium installation. Serve site/ first.
Screenshots are written to a caller-supplied directory, never to notebook assets.
"""
import argparse
from pathlib import Path

from build_learning_media import ASSETS, PROFILES, slide


def main():
    from playwright.sync_api import sync_playwright
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url",required=True)
    parser.add_argument("--screenshots",type=Path)
    parser.add_argument("--keys", nargs="*", help="Check only these lab IDs; CI checks all by default")
    args=parser.parse_args()
    if args.keys and set(args.keys)-set(PROFILES):
        parser.error("Unknown lab ID in --keys")
    if args.screenshots:
        args.screenshots.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as pw:
        browser=pw.chromium.launch()
        tab=browser.new_page(viewport={"width":1360,"height":1000})
        for key,p in PROFILES.items():
            if args.keys and key not in args.keys:
                continue
            graphics=[("infographic",(ASSETS/key/"infographic.svg").read_text(encoding="utf-8")),
                      ("cartoon",(ASSETS/key/"cartoon.svg").read_text(encoding="utf-8"))]
            graphics.extend((f"slide-{i}",slide(key,p,i)) for i in range(4))
            for kind,markup in graphics:
                tab.set_content('<html><body style="margin:0">'+markup+'</body></html>')
                # Validate every rendered text line, including card boundaries.
                overflow=tab.evaluate("""kind => {
                    const bounds=document.querySelector('svg').getBoundingClientRect();
                    return [...document.querySelectorAll('text')].filter(t=>{
                        const b=t.getBoundingClientRect();
                        if (b.left < bounds.left-1 || b.right > bounds.right+1 || b.bottom > bounds.bottom+1) return true;
                        const x=+t.getAttribute('x'), y=+t.getAttribute('y');
                        if(kind==='infographic' && y>=270 && y<=430 && t.textContent!=='→') {
                            const col=Math.floor((x-28)/313);
                            return b.right > bounds.left+28+col*313+294-10;
                        }
                        if(kind==='cartoon' && y>=84 && y<=238) {
                            const col=Math.floor((x-26)/420);
                            return b.right > bounds.left+26+col*420+398-18;
                        }
                        return false;
                    }).map(t=>t.textContent);
                }""",kind)
                if overflow:
                    raise AssertionError(f"{key}/{kind} clipped text: {overflow}")
                if args.screenshots and key in {"02","13","16","18","19","20"} and kind in {"infographic","cartoon"}:
                    tab.locator("svg").screenshot(path=str(args.screenshots/f"{key}-{kind}.png"))
            tab.goto(args.base_url.rstrip('/')+f"/lite/files/assets/learning/{key}/watch.html")
            tab.locator("video").evaluate("v => {v.preload='auto'; if(!v.readyState) v.load();}")
            tab.wait_for_function("document.querySelector('video').readyState >= 4")
            details=tab.locator("video").evaluate("""v=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,
                captions:v.textTracks.length,autoplay:v.autoplay})""")
            assert 31.9 <= details["duration"] <= 32.1, details
            assert (details["width"],details["height"])==(960,540), details
            assert details["captions"]==1 and not details["autoplay"], details
            tab.locator("video").evaluate("v => new Promise(resolve => {v.addEventListener('seeked',resolve,{once:true}); v.currentTime=17;})")
            tab.locator("video").evaluate("v => v.play()")
            tab.wait_for_function("document.querySelector('video').currentTime > 17.1")
            tab.locator("video").evaluate("v=>v.pause()")
            tab.wait_for_function("document.querySelector('video').textTracks[0].cues.length===4")
            if args.screenshots and key in {"02","16"}:
                tab.screenshot(path=str(args.screenshots/f"{key}-player-desktop.png"),full_page=True)
            tab.set_viewport_size({"width":390,"height":844})
            assert tab.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"{key}: mobile overflow"
            if args.screenshots and key=="02":
                tab.screenshot(path=str(args.screenshots/"02-player-mobile.png"),full_page=True)
            tab.set_viewport_size({"width":1360,"height":1000})
            print(f"Browser verified {key}: 6 graphics, playable video, 4 captions, mobile layout",flush=True)
        browser.close()


if __name__=="__main__":
    main()
