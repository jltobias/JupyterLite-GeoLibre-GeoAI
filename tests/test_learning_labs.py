"""Tests for measurement, validation and API boundaries, with no network calls."""
import copy
import json
from pathlib import Path
import sys
import unittest
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "book/notebooks"), str(ROOT / "scripts")]
import numpy as np
from astra_lab import (ACCESS_TOOL, apply_plan, dispatch_tool, make_request,
                       response_text)
from cognition import grid_features, teaching_city
from geolibre_lite import LiteMap
from run_astra import run_request
from build_lite import REQUIRED, extension_paths, validate_build


class LearningLabs(unittest.TestCase):
    def setUp(self):
        self.table, self.city = teaching_city()
        self.plan = {"field": "temperature_c", "operator": ">=", "threshold": 30,
                     "reason": "Known teaching threshold"}
        self.evidence = {"routes": [
            {"baseline": 0, "bridge_closed": 0},
            {"baseline": 10, "bridge_closed": 20},
            {"baseline": 12, "bridge_closed": None},
        ]}

    def test_grid_has_closed_lon_lat_rings_and_south_to_north_values(self):
        fc = grid_features([[1, 2], [3, 4]], cell_m=200)
        rings = [f["geometry"]["coordinates"][0] for f in fc["features"]]
        self.assertTrue(all(r[0] == r[-1] for r in rings))
        self.assertEqual([f["properties"]["value"] for f in fc["features"]], [1, 2, 3, 4])
        self.assertGreater(rings[1][0][0], rings[0][0][0])
        self.assertGreater(rings[2][0][1], rings[0][0][1])
        self.assertTrue(all(-180 <= p[0] <= 180 and -90 <= p[1] <= 90 for r in rings for p in r))
        with self.assertRaises(ValueError):
            grid_features([[np.nan]])

    def test_plan_has_correct_boundary_and_rejects_unsafe_values(self):
        import pandas as pd
        values = pd.DataFrame({"temperature_c": [29, 30, 31]})
        self.assertEqual(apply_plan(values, self.plan).index.tolist(), [1, 2])
        for patch in ({"field": "__import__('os')"}, {"operator": "eval"},
                      {"threshold": float("nan")}, {"threshold": True},
                      {"threshold": 900}, {"command": "unexpected"}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                apply_plan(self.table, {**self.plan, **patch})

    def test_unreachable_nodes_are_not_counted_as_accessible(self):
        result = dispatch_tool("summarize_accessibility",
                               {"scenario": "bridge_closed", "threshold_minutes": 12}, self.evidence)
        self.assertEqual(result["reachable_nodes"], 1)
        self.assertEqual(result["fraction"], 1/3)
        baseline = dispatch_tool("summarize_accessibility",
                                 {"scenario": "baseline", "threshold_minutes": 12}, self.evidence)
        self.assertEqual(baseline["fraction"], 1)
        with self.assertRaises(ValueError):
            dispatch_tool("run_shell", {}, self.evidence)
        with self.assertRaises(ValueError):
            dispatch_tool("summarize_accessibility",
                          {"scenario": "baseline", "threshold_minutes": -1}, self.evidence)

    def test_camera_sync_and_native_extrusions(self):
        m = LiteMap()
        original = m.project
        m.set_view(pitch=60, bearing=-25)
        self.assertIsNot(m.project, original)
        self.assertEqual(m.project["mapView"]["bearing"], 335)
        m.add_geojson(self.city, extrusionEnabled=True, extrusionHeightProperty="temperature_c")
        self.assertTrue(m.to_project()["layers"][0]["style"]["extrusionEnabled"])
        with self.assertRaises(ValueError):
            m.set_view(pitch=100)

    def test_incomplete_and_refused_responses_are_not_results(self):
        for response in ({"status": "incomplete"}, {"status": "completed", "output": []},
                         {"status": "completed", "output": [{"content": [{"type": "refusal"}]}]}):
            with self.assertRaises(ValueError):
                response_text(response)

    def test_bounded_tool_roundtrip_preserves_reasoning_and_request(self):
        request = make_request("Compare accessibility", {})
        request["tools"] = [ACCESS_TOOL]
        original = copy.deepcopy(request)
        sent = []
        first = {"status": "completed", "output": [
            {"type": "reasoning", "id": "rs_test", "summary": []},
            {"type": "function_call", "call_id": "test", "name": "summarize_accessibility",
             "arguments": json.dumps({"scenario": "bridge_closed", "threshold_minutes": 12})}]}
        final = {"status": "completed", "output": [{"type": "message", "content": [
            {"type": "output_text", "text": '{"observations":[],"limitations":[],"next_checks":[]}'}]}]}
        responses = iter([first, final])
        def send(body):
            sent.append(copy.deepcopy(body))
            return next(responses)
        result = run_request(request, self.evidence, send)
        self.assertEqual(result, final)
        self.assertEqual(request, original)
        self.assertEqual(sent[1]["input"][1]["type"], "reasoning")
        output = sent[1]["input"][-1]
        self.assertEqual(output["type"], "function_call_output")
        self.assertEqual(json.loads(output["output"])["reachable_nodes"], 1)

    def test_runaway_tool_calls_stop(self):
        request = make_request("Compare", {})
        request["tools"] = [ACCESS_TOOL]
        calls = []
        def send(body):
            calls.append(1)
            return {"status": "completed", "output": [{"type": "function_call", "call_id": "loop",
                "name": "summarize_accessibility", "arguments": '{"scenario":"baseline","threshold_minutes":12}'}]}
        with self.assertRaisesRegex(ValueError, "round limit"):
            run_request(request, self.evidence, send)
        self.assertEqual(len(calls), 4)

    def test_browser_extensions_resolve_to_installed_packages(self):
        paths = extension_paths()
        names = {json.loads((Path(p) / "package.json").read_text(encoding="utf-8"))["name"]
                 for p in paths}
        self.assertEqual(names, set(REQUIRED.values()))

    def test_build_without_a_browser_kernel_fails_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            (output / "jupyter-lite.json").write_text('{"jupyter-config-data":{}}')
            with self.assertRaisesRegex(RuntimeError, "missing required browser extensions"):
                validate_build(output)


if __name__ == "__main__":
    unittest.main()
