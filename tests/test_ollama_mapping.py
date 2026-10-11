"""Offline contracts; no local service, model, secret or download required in CI."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import AsyncMock, patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "book/notebooks"))
sys.path.insert(0, str(ROOT / "scripts"))
import ollama_mapping as om
from build_assistant_visuals import ASSETS, render_all


class Plans(unittest.TestCase):
    def test_known_selection_and_followup(self):
        original = deepcopy(om.FIXTURE_PLAN)
        before = om.preview_plan(original)
        after = om.preview_plan({**original, "minimum_heat": 41, "pitch": 0})
        self.assertEqual(len(om.synthetic_cells()["features"]), 12)
        self.assertEqual(len(before["features"]), 7)
        self.assertEqual(len(after["features"]), 4)
        self.assertLess({f["id"] for f in after["features"]}, {f["id"] for f in before["features"]})
        self.assertEqual(original, om.FIXTURE_PLAN)

    def test_reject_unknown_and_malformed_values(self):
        invalid = [None, [], {}, {**om.FIXTURE_PLAN, "url": "https://example.com"}]
        for key, values in {"minimum_heat": [True, None, "39", float("nan"), float("inf"), 29, 46],
                            "pitch": [False, 45.0, 90, -1],
                            "color": [None, [], "red", "<script>"],
                            "layer": [None, [], "unverified_data"]}.items():
            invalid.extend({**om.FIXTURE_PLAN, key: value} for value in values)
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                om.validate_plan(value)

    def test_approval_must_be_explicit(self):
        for value in [False, None, 1, "yes"]:
            with self.assertRaises(PermissionError):
                om.apply_plan(om.FIXTURE_PLAN, approved=value)
        self.assertEqual(len(om.apply_plan(om.FIXTURE_PLAN, approved=True)["features"]), 7)

    def test_no_ambiguous_json(self):
        for value in ['{"x":NaN}', '{"x":Infinity}', '{"x":1,"x":2}', '```json\n{}\n```']:
            with self.assertRaises(ValueError):
                om.strict_json(value)

    def test_network_scope(self):
        for value in ["http://127.0.0.1:11434", "http://localhost:11434/", "http://[::1]:11434"]:
            self.assertEqual(om.local_base_url(value), value.rstrip("/"))
        for value in ["https://example.com", "http://localhost:11434.evil.invalid", "http://127.0.0.1:8080",
                      "http://user:secret@localhost:11434", "http://localhost:11434/v1",
                      "http://localhost:11434/?x=1", "http://localhost:11434/#x", None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                om.local_base_url(value)
        with self.assertRaises(ValueError):
            asyncio.run(om.local_json("/api/pull"))

    def test_project_matches_fixture_without_credentials(self):
        project = om.demo_map().to_project()
        expected = json.loads((ROOT / "book/notebooks/data/ollama-demo.geolibre.json").read_text(encoding="utf-8"))
        self.assertEqual(project["layers"][0]["geojson"], expected["layers"][0]["geojson"])
        self.assertEqual(expected["preferences"]["environmentVariables"], [])
        filtered = om.demo_map(om.FIXTURE_PLAN).to_project()
        self.assertEqual(filtered["mapView"]["pitch"], 45)
        self.assertEqual(filtered["layers"][0]["style"]["fillColor"], om.COLORS["orange"])
        self.assertEqual(len(filtered["layers"][0]["geojson"]["features"]), 7)


class Inference(unittest.IsolatedAsyncioTestCase):
    def responses(self, **overrides):
        final = {"done": True, "done_reason": "stop", "model": om.MODEL,
                 "message": {"content": json.dumps(om.FIXTURE_PLAN)}, **overrides}
        return [{"models": [{"name": om.MODEL}]}, {"capabilities": ["completion", "thinking", "tools"]}, final]

    async def test_schema_and_local_request_contract(self):
        with patch.object(om, "local_json", AsyncMock(side_effect=self.responses())) as request:
            result = await om.propose_map("Select >=39 in orange at 45 degrees", current_plan=om.FIXTURE_PLAN)
            self.assertEqual(result["plan"], om.FIXTURE_PLAN)
            self.assertEqual(result["source"], "live local Ollama")
            path, body = request.call_args.args
            self.assertEqual(path, "/api/chat")
            self.assertEqual(body["format"], om.PLAN_SCHEMA)
            self.assertIs(body["stream"], False)
            self.assertIs(body["think"], False)
            self.assertNotIn("tools", body)
            self.assertEqual(body["options"]["num_predict"], 256)

    async def test_failures_do_not_turn_into_fixtures(self):
        failures = [{"done": False}, {"done_reason": "length"},
                    {"message": {"content": "not json"}},
                    {"message": {"content": "{}", "tool_calls": [{"name": "exec"}]}}]
        for override in failures:
            with self.subTest(override=override), patch.object(om, "local_json", AsyncMock(side_effect=self.responses(**override))):
                with self.assertRaises(ValueError):
                    await om.propose_map("Show my layer")
        with patch.object(om, "local_json", AsyncMock(side_effect=TimeoutError)):
            with self.assertRaises(TimeoutError):
                await om.propose_map("Show my layer")
            diagnostic = await om.diagnose()
            self.assertFalse(diagnostic["reachable"])
            self.assertNotIn("models", diagnostic)

    async def test_missing_or_cloud_model_never_reaches_chat(self):
        for entries in [[], [{"name": "another-model"}]]:
            with patch.object(om, "local_json", AsyncMock(return_value={"models": entries})) as request:
                with self.assertRaises(ValueError):
                    await om.propose_map("Show my layer")
                self.assertEqual(request.call_count, 1)
        with patch.object(om, "local_json", AsyncMock(side_effect=[{"models": [{"name": om.MODEL}]},
                                      {"remote_host": "https://example.com", "capabilities": ["completion"]}])) as request:
            with self.assertRaises(ValueError):
                await om.propose_map("Show my layer")
            self.assertEqual(request.call_count, 2)
        with self.assertRaises(ValueError):
            await om.propose_map("Show my layer", model="example:cloud")


class Teaching(unittest.TestCase):
    def test_original_accessible_diagrams(self):
        for name, expected in render_all().items():
            self.assertEqual((ASSETS / (name+".svg")).read_text(encoding="utf-8"), expected)
            root = ET.fromstring(expected)
            ns = {"s": "http://www.w3.org/2000/svg"}
            self.assertTrue(root.find("s:title", ns).text)
            self.assertGreater(len(root.find("s:desc", ns).text), 100)

    def test_credit_and_intelligence_boundaries(self):
        chapter = (ROOT / "book/advanced/ollama-assistant.md").read_text(encoding="utf-8")
        primer = (ROOT / "book/geoai/primer.md").read_text(encoding="utf-8")
        for term in ["Qiusheng Wu", "Global Nature Watch", "not a sandbox", "LIVE_MODEL=True"]:
            self.assertIn(term, chapter)
        for term in ["Stanford HAI", "not a learned world model", "Purple", "user-supplied"]:
            self.assertIn(term.lower(), primer.lower())


if __name__ == "__main__":
    unittest.main()
