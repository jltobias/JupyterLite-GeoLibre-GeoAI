"""Generate original, locally bundled STAC discovery teaching graphics."""
import argparse
from build_learning_media import ROOT, rect, text, path, svg, write_or_check
from build_future_chapters import chapter_comic

ASSETS = ROOT / 'book/assets/discovery'


def bounding_box():
    title = 'A search box selects records; it does not cut files'
    description = ('Schematic: A is inside the purple study box, B crosses its edge, '
                   'and C is outside. Keep A and B as candidates; exclude C. '
                   'Their original footprints and raster files remain unchanged.')
    body = rect(0, 0, 1280, 690, '#f5f7fa', radius=0)
    body += text(30, 50, title, 33, '#14283f', 700)
    body += text(30, 92, 'Filter by overlap, then inspect the metadata and actual coverage.', 24, '#45576c')
    body += rect(30, 125, 690, 460, 'white', '#cddbe9')
    for x in range(70, 710, 40):
        body += path(f'M{x} 145 V565', '#e1e8ef', 1)
    for y in range(145, 575, 40):
        body += path(f'M50 {y} H700', '#e1e8ef', 1)
    for x, y, w, h, label, color in (
        (75, 175, 105, 85, 'C', '#64748b'),
        (265, 290, 105, 85, 'A', '#2459b8'),
        (445, 395, 220, 120, 'B', '#2459b8'),
    ):
        body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-width="3"/>'
        body += text(x+15, y+35, label, 27, color, 700)
    body += '<rect x="210" y="240" width="310" height="225" fill="none" stroke="#7545b3" stroke-width="5"/>'
    body += text(210, 222, 'Your study bbox', 24, '#7545b3', 700)
    body += text(742, 180, 'A + B: keep as candidates', 27, '#2459b8', 700)
    body += text(742, 221, 'Both footprints overlap the box. B need not fit inside it.', 24, width=33)
    body += text(742, 325, 'C: outside the search area', 27, '#64748b', 700)
    body += text(742, 366, 'Exclude this footprint from this spatial search.', 24, width=33)
    body += text(742, 470, 'Still not a crop', 27, '#7545b3', 700)
    body += text(742, 511, 'A and B retain their full footprints. No pixels have been cut or read.', 24, width=33)
    body += text(30, 630, 'Coordinates: west, south, east, north — longitude / latitude in degrees.', 25, '#14283f', 700)
    body += text(30, 673, 'Original schematic, not real geography. Dates and collection choice can narrow results further.', 22, '#45576c')
    return svg(body, title, description, 1280, 690)


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
        'stac-bbox': bounding_box(),
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
    print('Verified' if args.check else 'Generated', 'three original STAC discovery visuals')
