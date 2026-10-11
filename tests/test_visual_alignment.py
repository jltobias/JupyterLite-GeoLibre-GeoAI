"""Regression guards for reviewed map geometry, styles and publication routes."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "book/notebooks")]
import h3
import nbformat
from cognition import grid_features, plotly_view
from geolibre_lite import LiteMap
from spatial_geometry import horizontal_bbox, split_antimeridian_ring
from build_resource_index import replace_index, resource_table
from check_site_alignment import same_file
from validate_notebooks import executable_offline


class VisualAlignment(unittest.TestCase):
    def test_horizontal_bbox_handles_elevation_and_date_line(self):
        self.assertEqual(horizontal_bbox([-123, 37, 10, -121, 39, 90]), [-123, 37, -121, 39])
        self.assertEqual(horizontal_bbox([179, -20, -178, -16]), [179, -20, -178, -16])
        self.assertEqual(horizontal_bbox(None), [None] * 4)
        for bbox in ([1, 2, 3], [0, 30, 1, 20], [0, 0, float('nan'), 1]):
            with self.assertRaises(ValueError):
                horizontal_bbox(bbox)

    def test_date_line_cells_are_small_closed_parts_not_world_spanning_bands(self):
        boundary = h3.cell_to_boundary(h3.latlng_to_cell(52, 179.9, 3))
        result = split_antimeridian_ring([[lon, lat] for lat, lon in boundary])
        self.assertEqual(result['type'], 'MultiPolygon')
        for polygon in result['coordinates']:
            ring = polygon[0]
            self.assertEqual(ring[0], ring[-1])
            self.assertTrue(all(-180 <= lon <= 180 for lon, _ in ring))
            self.assertTrue(all(abs(a[0]-b[0]) < 5 for a,b in zip(ring, ring[1:])))
        ordinary = split_antimeridian_ring([[0,0],[1,0],[1,1],[0,1],[0,0]])
        self.assertEqual(ordinary['type'], 'Polygon')
        with self.assertRaisesRegex(ValueError, 'Pole-enclosing'):
            split_antimeridian_ring([[lon, lat] for lat, lon in h3.cell_to_boundary(h3.latlng_to_cell(90, 0, 3))])

    def test_date_line_clipping_preserves_area_and_orientation(self):
        geometry = split_antimeridian_ring([[179,0],[-179,0],[-179,2],[179,2]])
        area = 0
        for polygon in geometry['coordinates']:
            ring = polygon[0]
            signed = sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring, ring[1:]))/2
            self.assertGreater(signed, 0)
            area += signed
        self.assertAlmostEqual(area, 4)

    def test_styles_and_null_properties_reach_geolibre_builders(self):
        m = LiteMap()
        fc = {'type':'FeatureCollection', 'features':[
            {'type':'Feature', 'geometry':{'type':'Point','coordinates':[0,0]}, 'properties':{'value':1}},
            {'type':'Feature', 'geometry':{'type':'Point','coordinates':[1,1]}, 'properties':None}]}
        m.add_geojson(fc, fillColor='#ef4444', circleRadius=10, fillOpacity=0.8)
        style = m.to_project()['layers'][0]['style']
        self.assertEqual((style['fillColor'],style['circleRadius'],style['fillOpacity']), ('#ef4444',10,0.8))
        m.add_choropleth(fc, column='value')
        source = (ROOT / 'book/notebooks/10_sister_cities_graph_geoai.ipynb').read_text(encoding='utf-8')
        self.assertNotIn('pointColor=',source)
        self.assertNotIn('pointRadius=',source)

    def test_nonfinite_grid_size_rejected(self):
        for size in (float('nan'),float('inf'),-1,0):
            with self.assertRaises(ValueError):
                grid_features([[1]],cell_m=size)

    def test_resource_directory_has_every_read_run_and_companion(self):
        paths = sorted((ROOT / 'book/notebooks').glob('*.ipynb'))
        table = resource_table(paths)
        for path in paths:
            self.assertIn(f'/notebooks/{path.stem}.html',table)
            self.assertIn(f'path={path.name}',table)
            self.assertIn(f'/learning/{path.name[:2]}/watch.html',table)
        for page in ('README.md','book/visual-library.md'):
            text = (ROOT/page).read_text(encoding='utf-8')
            self.assertEqual(text,replace_index(text))
        with self.assertRaises(ValueError):
            replace_index('Missing markers')

    def test_missing_and_stale_published_copies_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp,'source'),Path(tmp,'target')
            source.write_text('canonical',encoding='utf-8')
            with self.assertRaises(ValueError):
                same_file(source,target)
            target.write_text('old',encoding='utf-8')
            with self.assertRaises(ValueError):
                same_file(source,target)
            target.write_bytes(source.read_bytes())
            same_file(source,target)

    def test_bundled_labs_execute_without_claiming_synthetic_data(self):
        for number in ('16','17'):
            path = next((ROOT/'book/notebooks').glob(number+'_*.ipynb'))
            nb = nbformat.read(path,as_version=4)
            self.assertTrue(executable_offline(path,nb))
            self.assertFalse(nb.metadata.get('cognition',{}).get('synthetic',False))
            self.assertTrue(any(c.get('outputs') for c in nb.cells if c.cell_type=='code'))

    def test_static_analytical_alternatives_exist(self):
        for number in ('12','13','14','15','16'):
            path = next((ROOT/'book/notebooks').glob(number+'_*.ipynb'))
            nb = nbformat.read(path,as_version=4)
            pngs = [o for c in nb.cells if c.cell_type=='code' for o in c.outputs if 'image/png' in o.get('data',{})]
            self.assertTrue(pngs,number)

    def test_iframe_title_is_escaped(self):
        import plotly.graph_objects as go
        value = plotly_view(go.Figure(),title='Scenario "A" < B').data
        self.assertIn('title="Scenario &quot;A&quot; &lt; B"',value)


if __name__ == '__main__':
    unittest.main()
