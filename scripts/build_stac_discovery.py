"""Generate original, locally bundled STAC discovery teaching graphics."""
import argparse
from build_learning_media import ROOT, rect, text, svg, write_or_check
from build_future_chapters import chapter_comic

ASSETS = ROOT / 'book/assets/discovery'


def render_all():
    title = 'Follow the record to the right file'
    subtitle = 'A common STAC route: context first, then the asset you actually need.'
    entries = [
        ('Catalog', 'Find entry points and related catalogs.', '#2459b8'),
        ('Collection', 'Read product context, coverage and license.', '#087f78'),
        ('Item', 'Inspect one record: identifier, footprint and time.', '#7545b3'),
        ('Assets', 'Choose data, a preview or metadata. Check the role.', '#a96112'),
    ]
    body = rect(0, 0, 1280, 600, '#f5f7fa', radius=0)
    body += text(30, 48, title, 34, '#14283f', 700)
    body += text(30, 90, subtitle, 23, '#45576c')
    for index, (heading, explanation, color) in enumerate(entries):
        x = 30 + index * 312
        body += rect(x, 145, 280, 285, 'white', '#cddbe9')
        body += rect(x, 145, 280, 8, color, radius=0)
        body += text(x+18, 201, heading, 28, color, 700)
        body += text(x+18, 266, explanation, 24, width=19, line=1.35)
        if index < 3:
            body += text(x+285, 305, '→', 24, '#45576c', 700)
    body += text(30, 490, 'A footprint describes coverage. It does not contain the raster pixels.', 26, '#14283f', 700)
    body += text(30, 537, 'Catalogs may nest; one Item may have several assets. Follow the advertised links.', 23, '#45576c')
    body += text(30, 579, 'Original teaching schematic, not a live catalog response.', 19, '#45576c')
    description = subtitle+' '+'. '.join(h+': '+v for h, v, _ in entries)
    return {
        'stac-route': svg(body, title, description, 1280, 600),
        'stac-cartoon': chapter_comic('A footprint is not a flood measurement', [
            'This footprint covers my city. Is it a flood map?',
            'It shows coverage. Inspect the asset and its meaning.',
            'I will check units, dates and access before modeling.',
        ]),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, content in render_all().items():
        write_or_check(ASSETS/(name+'.svg'), content, args.check)
    print('Verified' if args.check else 'Generated', 'two original STAC discovery visuals')
