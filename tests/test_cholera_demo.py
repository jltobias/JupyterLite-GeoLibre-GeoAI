"""Contracts for an attributed historical-data lesson, not an outbreak detector."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import haversine_distances

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'book/notebooks'))
sys.path.insert(0, str(ROOT/'scripts'))
import cholera_demo as demo
from build_cholera_lesson import ASSETS, AUTHORED, map_svg, snapshot_data, public_project, presentation_html


class CholeraLesson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deaths, cls.pumps = demo.load_records()

    def test_source_bytes_and_records(self):
        provenance = json.loads((demo.DATA/'provenance.json').read_text())
        for name, info in provenance['files'].items():
            self.assertEqual(hashlib.sha256((demo.DATA/name).read_bytes()).hexdigest(), info['sha256'])
        self.assertEqual((len(self.deaths), int(self.deaths.DEATHS.sum()), len(self.pumps)), (250,489,8))
        self.assertIn('GNU GENERAL PUBLIC LICENSE', (demo.DATA/'LICENSE').read_text())
        self.assertEqual(self.pumps.iloc[0].Street, 'Broadwick Street')

    def test_geographic_units_and_coordinate_order(self):
        frame = pd.DataFrame({'LAT':[0.,1.], 'LON':[0.,0.]})
        result = haversine_distances(demo.coordinates(frame))*demo.EARTH_RADIUS_M
        self.assertAlmostEqual(result[0,1],111195.0802,places=3)
        np.testing.assert_allclose(demo.coordinates(self.deaths)[0],
                                  np.radians([self.deaths.iloc[0].LAT,self.deaths.iloc[0].LON]))

    def test_three_fits_match_reported_results(self):
        for radius, expected in [(25,(12,42)),(50,(1,7)),(100,(1,0))]:
            labels = demo.cluster_locations(self.deaths, radius)
            self.assertEqual((len(set(labels)-{-1}), int((labels==-1).sum())), expected)
            table = demo.summary(self.deaths, labels)
            self.assertEqual(int(table.locations.sum()),250)
            self.assertEqual(int(table.recorded_deaths.sum()),489)
        self.assertEqual(int(demo.summary(self.deaths,demo.cluster_locations(self.deaths)).query('group == 0').locations.iloc[0]),243)

    def test_only_coordinates_are_fitted_and_source_is_unchanged(self):
        before = self.deaths.copy(deep=True)
        labels = demo.cluster_locations(before)
        altered = before.assign(DEATHS=999, FID=np.arange(1000,1250))
        np.testing.assert_array_equal(labels, demo.cluster_locations(altered))
        with patch.object(demo, 'DBSCAN', wraps=demo.DBSCAN) as constructor:
            demo.cluster_locations(before)
            self.assertEqual(constructor.call_args.kwargs['metric'], 'haversine')
            self.assertEqual(constructor.call_args.kwargs['eps'],50/demo.EARTH_RADIUS_M)
        pd.testing.assert_frame_equal(before, self.deaths)
        source = next(code for kind,code in AUTHORED if kind=='code' and 'labels = DBSCAN(' in code)
        self.assertNotIn('pumps', source)
        self.assertNotIn('sample_weight', source)

    def test_invalid_inputs_are_not_replaced_with_fixtures(self):
        for radius in (0,201,float('nan'),float('inf'),True):
            with self.subTest(radius=radius), self.assertRaises(ValueError):
                demo.cluster_locations(self.deaths, radius)
        for minimum in (1,2.5,True):
            with self.assertRaises(ValueError):
                demo.cluster_locations(self.deaths,min_locations=minimum)
        for frame in (self.deaths.iloc[:0],self.deaths.assign(LAT=91),self.deaths.assign(LON=np.nan)):
            with self.assertRaises(ValueError):
                demo.coordinates(frame)
        with self.assertRaises(ValueError):
            demo.summary(self.deaths,[0])
        with tempfile.TemporaryDirectory() as missing:
            with self.assertRaises(FileNotFoundError):
                demo.load_records(missing)

    def test_geolibre_project_uses_supported_styles_and_context_only(self):
        labels = demo.cluster_locations(self.deaths)
        with patch.object(demo, 'cluster_locations', side_effect=AssertionError('Hidden refit')):
            hidden = demo.geolibre_map(self.deaths,self.pumps,labels,reveal_pumps=False).to_project()
            revealed = demo.geolibre_map(self.deaths,self.pumps,labels).to_project()
        self.assertEqual(len(hidden['layers']),2)
        self.assertEqual(len(revealed['layers']),3)
        for first, second in zip(hidden['layers'],revealed['layers']):
            self.assertEqual(first['geojson'],second['geojson'])
            self.assertNotIn('circleColor',first['style'])
            label = first['geojson']['features'][0]['properties']['group']
            self.assertEqual(first['style']['fillColor'],demo.color_for(label))
        features = [f for layer in hidden['layers'] for f in layer['geojson']['features']]
        self.assertEqual(len(features),250)
        source = self.deaths.set_index('FID')
        for feature in features:
            row = source.loc[feature['id']]
            self.assertEqual(feature['geometry']['coordinates'],[row.LON,row.LAT])
        self.assertEqual(len(revealed['layers'][-1]['geojson']['features']),8)
        self.assertEqual(public_project(self.deaths,self.pumps),public_project(self.deaths,self.pumps))

    def test_saved_views_are_reproducible_and_labeled(self):
        snapshots = snapshot_data(self.deaths)
        self.assertEqual(snapshots,json.loads((ASSETS/'results.json').read_text()))
        self.assertEqual(presentation_html(snapshots),(ASSETS/'presentation.html').read_text(encoding='utf-8'))
        for radius in demo.RADII:
            labels = demo.cluster_locations(self.deaths,radius)
            for reveal,name in ((False,'groups'),(True,'pumps')):
                actual = map_svg(self.deaths,self.pumps,labels,radius,reveal)
                self.assertEqual(actual,(ASSETS/f'{name}-{radius}.svg').read_text(encoding='utf-8'))
                tree = ET.fromstring(actual)
                self.assertEqual(len(tree.findall('{http://www.w3.org/2000/svg}circle')),250)
                self.assertIn('not a disease-risk map', actual)
        self.assertEqual(json.loads((ROOT/'book/notebooks/data/cholera-demo.geolibre.json').read_text()),public_project(self.deaths,self.pumps))

    def test_point_display_extent_and_pump_reveal(self):
        for frame in (self.deaths,self.pumps):
            x,y = demo.local_xy(frame)
            self.assertTrue(((x > -330)&(x < 350)).all())
            self.assertTrue(((y > -355)&(y < 350)).all())
        plain = map_svg(self.deaths,self.pumps,demo.cluster_locations(self.deaths))
        reveal = map_svg(self.deaths,self.pumps,demo.cluster_locations(self.deaths),reveal=True)
        self.assertNotIn('>P1<',plain)
        for i in range(1,9):
            self.assertIn(f'>P{i}<',reveal)

    def test_notebook_is_historical_and_offline_default(self):
        notebook = json.loads((ROOT/'book/notebooks/21_cholera_geoai_first_steps.ipynb').read_text(encoding='utf-8'))
        self.assertEqual(notebook['metadata']['cholera_lesson'],{'historical_data':True,'offline_data':True,'synthetic':False})
        code = '\n'.join(''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code')
        self.assertIn('from pyodide_js import loadPackage',code)
        self.assertIn('SHOW_GEOLIBRE = False',code)
        self.assertNotIn('requests.get',code)
        self.assertEqual(sum(c['cell_type']=='code' for c in notebook['cells']),6)


if __name__=='__main__':
    unittest.main()
