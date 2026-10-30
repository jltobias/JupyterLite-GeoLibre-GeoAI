"""Test geographic semantics and transfer boundaries, not third-party map UI."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'book/notebooks'))
from rustgis_bridge import (sample_sites, validate_sites, fit_groups, group_counts,
                            export_groups, public_view_url, PUBLIC_DATA)


class RustGISBridge(unittest.TestCase):
    def test_expected_groups_and_no_input_mutation(self):
        sites = sample_sites()
        before = deepcopy(sites)
        self.assertEqual(group_counts(fit_groups(sites, 350)), {-1: 2, 0: 9, 1: 9})
        self.assertEqual(group_counts(fit_groups(sites, 150)), {-1: 20})
        self.assertEqual(sites, before)
        self.assertEqual(len(sites['features']), 20)
        self.assertTrue(all(f['properties']['synthetic'] for f in sites['features']))

    def test_haversine_uses_latitude_first_and_meters(self):
        # At 60 N, .004 longitude is ~222 m (rather than ~445 m at the equator).
        sites = sample_sites()
        sites['features'] = sites['features'][:3]
        for f, xy in zip(sites['features'], [(0, 60), (.004, 60), (.008, 60)]):
            f['geometry']['coordinates'] = list(xy)
        self.assertEqual(group_counts(fit_groups(sites, 250)), {0: 3})
        for f in sites['features']:
            f['geometry']['coordinates'][1] = 0
        self.assertEqual(group_counts(fit_groups(sites, 250)), {-1: 3})

    def test_invalid_geometry_radius_and_ids(self):
        for xy in ([181, 0], [0, 91], [float('nan'), 0], [0, float('inf')], [True, 0], [0]):
            with self.subTest(xy=xy), self.assertRaises(ValueError):
                sites = sample_sites()
                sites['features'][0]['geometry']['coordinates'] = xy
                validate_sites(sites)
        sites = sample_sites()
        sites['features'][1]['id'] = sites['features'][0]['id']
        with self.assertRaises(ValueError):
            validate_sites(sites)
        for radius in (0, -1, True, float('nan'), float('inf')):
            with self.subTest(radius=radius), self.assertRaises(ValueError):
                fit_groups(sample_sites(), radius)

    def test_export_roundtrip_preserves_current_result(self):
        grouped = fit_groups(sample_sites(), 150)
        with tempfile.TemporaryDirectory() as directory:
            data, card = export_groups(grouped, directory)
            self.assertEqual(json.loads(data.read_text()), grouped)
            provenance = json.loads(card.read_text())
            self.assertEqual(provenance['neighbor_radius_m'], 150)
            self.assertEqual(provenance['group_counts'], {'-1': 20})
            self.assertIn('Invented', provenance['dataset'])
            self.assertIn('not risk', provenance['limits'])

    def test_links_load_public_data_not_local_exports_or_geolibre_projects(self):
        for globe in (False, True):
            url = urlsplit(public_view_url(globe))
            self.assertEqual(url.netloc, 'web.rustgis.app')
            query = parse_qs(url.query, keep_blank_values=True)
            self.assertEqual(query['data'], [PUBLIC_DATA])
            self.assertIn('blank', query)
            self.assertNotIn('project', query)
            self.assertEqual(query.get('projection'), ['globe'] if globe else None)
        expected = fit_groups(sample_sites(), 350)
        self.assertEqual(json.loads((ROOT/'book/notebooks/data/rustgis-groups.geojson').read_text()), expected)


if __name__ == '__main__':
    unittest.main()
