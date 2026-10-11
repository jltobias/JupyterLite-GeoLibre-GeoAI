"""Opt-in smoke test on this computer. Never used by public CI.

python scripts/check_ollama_local.py --live [--output /path/to/report.json]
Does not download models, restart services, change permissions or operate GeoLibre.
"""
import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.request import Request, build_opener, ProxyHandler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "book/notebooks"))
from ollama_mapping import BASE_URL, MODEL, local_json, propose_map, preview_plan


async def check():
    version = await local_json("/api/version")
    tags = await local_json("/api/tags")
    model = next(m for m in tags["models"] if m["name"] == MODEL)
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "ollama_version": version["version"], "model": MODEL, "model_digest": model["digest"],
              "scope": "CPython local API smoke test, NOT native GeoLibre UI or browser end-to-end",
              "origins": {}, "turns": []}
    opener = build_opener(ProxyHandler({}))
    for origin in ("https://web.geolibre.app", "https://jltobias.github.io"):
        try:
            with opener.open(Request(BASE_URL+"/api/tags", headers={"Origin": origin}), timeout=10) as response:
                report["origins"][origin] = {"http_status": response.status,
                    "allow_origin": response.headers.get("Access-Control-Allow-Origin")}
        except HTTPError as error:
            report["origins"][origin] = {"http_status": error.code, "allow_origin": None}
    plan = None
    cases = [("Show synthetic heat cells with heat proxy at least 39 in orange and tilt the map to 45 degrees.",
              {"layer": "synthetic_cells", "minimum_heat": 39, "color": "orange", "pitch": 45}, 7),
             ("Keep the same layer and orange color. Raise the minimum heat proxy to 41 and return to a flat map.",
              {"layer": "synthetic_cells", "minimum_heat": 41, "color": "orange", "pitch": 0}, 4)]
    for prompt, expected, count in cases:
        result = await propose_map(prompt, current_plan=plan)
        plan = result["plan"]
        result["computed_count"] = len(preview_plan(plan)["features"])
        result["expected_plan"] = expected
        result["pass"] = plan == expected and result["computed_count"] == count
        report["turns"].append(result)
        print(json.dumps(result, indent=2), flush=True)
    report["all_plan_checks_pass"] = all(t["pass"] for t in report["turns"])
    report["browser_origins_accepted"] = all(v["http_status"] == 200 and v["allow_origin"] == k
                                             for k,v in report["origins"].items())
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Explicitly permit two synthetic prompts to local Ollama")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.live:
        parser.error("This optional test contacts Ollama; supply --live deliberately")
    result = asyncio.run(check())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "turns"}, indent=2))
    raise SystemExit(0 if result["all_plan_checks_pass"] else 1)
