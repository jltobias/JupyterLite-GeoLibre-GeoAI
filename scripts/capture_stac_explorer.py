"""Capture the public companion Explorer, with live metadata and no asset downloads.

Run explicitly, not in CI: this makes one bounded WorldPop search. The screenshot
is an unaltered browser viewport; do not replace failed responses with fixtures.
"""
import argparse
from pathlib import Path


def main():
    from playwright.sync_api import sync_playwright, expect
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1560, 'height': 1320},
                                device_scale_factor=1)
        page.goto('https://jltobias.github.io/JupyterLite-STAC-Browser/explorer/')
        expect(page.locator('#search')).to_be_enabled(timeout=45000)
        page.locator('#collection').select_option('UGA')
        page.locator('#start').fill('')
        page.locator('#end').fill('')
        page.locator('#bbox').fill('31.4,0.1,32.9,0.8')
        page.locator('#bbox').press('Tab')
        page.locator('#limit').select_option('10')
        page.locator('#search').click()
        expect(page.locator('.result-card').first).to_be_visible(timeout=45000)
        page.locator('.result-card').filter(
            has_text='Uganda, Spatial Distribution of Population in 2030 at 100m').click()
        expect(page.locator('#metadata h3').first).to_be_visible()
        page.wait_for_function("[...document.querySelectorAll('.leaflet-tile')].every(i => i.complete && i.naturalWidth)")
        page.evaluate('document.fonts.ready')
        page.evaluate('window.scrollTo(0, 0)')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(args.output), animations='disabled')
        print('Saved:', args.output)
        print('Status:', page.locator('#status').inner_text())
        print('Selected:', page.locator('#metadata').inner_text())
        print('Attribution:', page.locator('.leaflet-control-attribution').inner_text())
        browser.close()


if __name__ == '__main__':
    main()
