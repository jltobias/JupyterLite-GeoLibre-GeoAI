"""Small, inspectable local-model lesson. No generated Python/SQL is executed.

This notebook-side planner is NOT GeoLibre's native AI Assistant. It supports
one invented layer and a deliberately tiny vocabulary; see the advanced chapter.
"""
import asyncio
from copy import deepcopy
import json
import math
import sys
from urllib.parse import urlsplit

BASE_URL = "http://127.0.0.1:11434"
MODEL = "qwen3:4b"
COLORS = {"orange": "#bb5d14", "teal": "#087f78", "purple": "#7545b3"}
MAX_BYTES = 512_000
PLAN_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["layer", "minimum_heat", "color", "pitch"],
    "properties": {
        "layer": {"type": "string", "enum": ["synthetic_cells"]},
        "minimum_heat": {"type": "number", "minimum": 30, "maximum": 45},
        "color": {"type": "string", "enum": list(COLORS)},
        "pitch": {"type": "integer", "enum": [0, 45]},
    },
}
# Authored example, deliberately NOT attributed to a live model.
FIXTURE_PLAN = {"layer": "synthetic_cells", "minimum_heat": 39, "color": "orange", "pitch": 45}


def strict_json(value):
    def reject_constant(value):
        raise ValueError("Non-finite JSON value: " + value)
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(value, parse_constant=reject_constant, object_pairs_hook=unique_pairs)


def local_base_url(value):
    """Only the default loopback service; no credentials, paths or redirects."""
    if not isinstance(value, str):
        raise ValueError("Use a loopback Ollama URL")
    parsed = urlsplit(value)
    if (parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
            or parsed.port != 11434 or parsed.username is not None or parsed.password is not None
            or parsed.path not in {"", "/"} or parsed.query or parsed.fragment):
        raise ValueError("This lesson only calls http://127.0.0.1:11434 (or localhost / [::1])")
    return value.rstrip("/")


async def local_json(path, body=None, *, base_url=BASE_URL, timeout=15):
    """Async Fetch in Pyodide; a bounded, no-redirect request in ordinary Python."""
    base = local_base_url(base_url)
    if path not in {"/api/tags", "/api/version", "/api/show", "/api/chat"}:
        raise ValueError("Endpoint is not allowed by this lesson")
    if not isinstance(timeout, (int, float)) or not 0 < timeout <= 180:
        raise ValueError("Timeout must be between 0 and 180 seconds")
    encoded = None if body is None else json.dumps(body, allow_nan=False).encode("utf-8")
    if encoded is not None and len(encoded) > 32_000:
        raise ValueError("Request is too large for this lesson")
    if sys.platform == "emscripten":
        from js import AbortController
        from pyodide.http import pyfetch
        controller = AbortController.new()
        try:
            async with asyncio.timeout(timeout):
                response = await pyfetch(base + path, method="GET" if body is None else "POST",
                    headers={} if body is None else {"Content-Type": "application/json"},
                    body=None if encoded is None else encoded.decode("utf-8"),
                    signal=controller.signal, redirect="error", credentials="omit")
                if not response.ok:
                    raise RuntimeError(f"Ollama returned HTTP {response.status}")
                raw = await response.bytes()
        finally:
            controller.abort()
    else:
        from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler
        class NoRedirect(HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                raise RuntimeError("Redirects are not allowed")
        def fetch():
            # A localhost lesson never needs a corporate/public HTTP proxy.
            opener = build_opener(ProxyHandler({}), NoRedirect())
            request = Request(base + path, data=encoded,
                headers={} if encoded is None else {"Content-Type": "application/json"})
            with opener.open(request, timeout=timeout) as response:
                return response.read(MAX_BYTES + 1)
        raw = await asyncio.wait_for(asyncio.to_thread(fetch), timeout=timeout)
    if len(raw) > MAX_BYTES:
        raise ValueError("Response exceeds the lesson's size limit")
    result = strict_json(raw)
    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object from Ollama")
    return result


async def diagnose(*, base_url=BASE_URL):
    """Report failure without substituting fake server/model results."""
    try:
        version = await local_json("/api/version", base_url=base_url)
        tags = await local_json("/api/tags", base_url=base_url)
        entries = tags.get("models", [])
        if not isinstance(entries, list):
            raise ValueError("Malformed model list")
        names = [entry["name"] for entry in entries
                 if isinstance(entry, dict) and isinstance(entry.get("name"), str)]
        return {"reachable": True, "version": version.get("version"), "models": names}
    except Exception as error:
        return {"reachable": False, "error": type(error).__name__,
                "next_step": "Check Ollama, exact OLLAMA_ORIGINS, and browser Local Network Access permission. "
                "A browser network failure alone does not prove CORS is the cause. No cloud fallback was used."}


def validate_plan(plan):
    """Schema hints are not enforcement: validate independently after inference."""
    if not isinstance(plan, dict) or set(plan) != set(PLAN_SCHEMA["required"]):
        raise ValueError("Plan must contain exactly layer, minimum_heat, color and pitch")
    if (plan["layer"] != "synthetic_cells" or not isinstance(plan["color"], str)
            or plan["color"] not in COLORS):
        raise ValueError("Unknown layer or color")
    number = plan["minimum_heat"]
    if type(number) not in (int, float) or not math.isfinite(number) or not 30 <= number <= 45:
        raise ValueError("minimum_heat must be a finite number between 30 and 45")
    if type(plan["pitch"]) is not int or plan["pitch"] not in (0, 45):
        raise ValueError("pitch must be 0 or 45")
    return deepcopy(plan)


def synthetic_cells():
    """Invented grid near Gaborone; NO measured temperature or health records."""
    features = []
    for row in range(3):
        for col in range(4):
            west, south = 25.86 + col * .02, -24.70 + row * .02
            ring = [[west, south], [west + .018, south], [west + .018, south + .018],
                    [west, south + .018], [west, south]]
            features.append({"type": "Feature", "id": f"cell-{row}-{col}",
                "properties": {"cell_id": f"cell-{row}-{col}", "heat_proxy_c": 35 + 2 * col + row,
                               "provenance": "invented teaching data; not observed heat or health risk"},
                "geometry": {"type": "Polygon", "coordinates": [ring]}})
    return {"type": "FeatureCollection", "features": features}


def preview_plan(plan):
    validated = validate_plan(plan)
    selected = [f for f in synthetic_cells()["features"]
                if f["properties"]["heat_proxy_c"] >= validated["minimum_heat"]]
    return {"type": "FeatureCollection", "features": selected}


def apply_plan(plan, *, approved=False):
    """Explicit human gate for this helper only; not a GeoLibre security policy."""
    if approved is not True:
        raise PermissionError("Review the plan and explicitly approve it before applying")
    return preview_plan(plan)


def demo_map(plan=None):
    """Caller chooses whether to apply; default is all 12 synthetic polygons."""
    from geolibre_lite import Map
    selected = synthetic_cells() if plan is None else preview_plan(plan)
    result = Map(center=(25.90, -24.665), zoom=12, height="530px")
    color = "#087f78" if plan is None else COLORS[plan["color"]]
    result.add_geojson(selected, name="Synthetic heat cells — not observations",
                       fillColor=color, strokeColor="#14283f", fillOpacity=.65)
    result.set_view(pitch=0 if plan is None else plan["pitch"])
    return result


async def propose_map(prompt, *, current_plan=None, model=MODEL, base_url=BASE_URL):
    """One explicit live call; failures propagate, never replaced with a fixture."""
    if not isinstance(prompt, str) or not 1 <= len(prompt.strip()) <= 1000:
        raise ValueError("Use a prompt of 1–1000 characters")
    if not isinstance(model, str) or not model or len(model) > 100 or "cloud" in model.lower():
        raise ValueError("Select an installed local model, not a cloud model")
    tags = await local_json("/api/tags", base_url=base_url)
    if model not in [m.get("name") for m in tags.get("models", []) if isinstance(m, dict)]:
        raise ValueError("Model is not installed. Pull it yourself in a terminal; no automatic download occurs.")
    details = await local_json("/api/show", {"model": model}, base_url=base_url)
    if details.get("remote_host") or details.get("remote_model"):
        raise ValueError("Remote-backed models are not allowed in this local-only lesson")
    if "completion" not in details.get("capabilities", []):
        raise ValueError("This model does not advertise text completion")
    previous = None if current_plan is None else validate_plan(current_plan)
    instruction = ("Return only a JSON map plan matching the supplied schema. The ONLY layer is synthetic_cells, "
        "12 invented polygons near Gaborone with heat_proxy_c (invented Celsius-like values, NOT observations). "
        "minimum_heat is an inclusive >= cutoff, from 30 to 45. Colors: orange, teal, purple. "
        "pitch 0 means flat; 45 means tilted, NOT flood depth or a world model. "
        "Do not create URLs, code, SQL, patient data, health claims, counts or additional fields. "
        "For follow-ups change only the requested settings from the previous plan. "
        "Default settings are minimum_heat 30, color teal, pitch 0. "
        "Previous validated plan: " + json.dumps(previous))
    body = {"model": model, "messages": [{"role": "system", "content": instruction},
                                         {"role": "user", "content": prompt}],
            "format": PLAN_SCHEMA, "stream": False,
            "options": {"temperature": 0, "num_predict": 256, "num_ctx": 4096}, "keep_alive": "2m"}
    if "thinking" in details.get("capabilities", []):
        body["think"] = False
    response = await local_json("/api/chat", body, base_url=base_url, timeout=180)
    if response.get("done") is not True or response.get("done_reason") == "length":
        raise ValueError("Incomplete response; no plan applied")
    message = response.get("message", {})
    if not isinstance(message, dict) or message.get("tool_calls"):
        raise ValueError("This planner accepts JSON content, not executable tool calls")
    plan = validate_plan(strict_json(message.get("content", "")))
    return {"source": "live local Ollama", "model": response.get("model", model),
            "prompt": prompt, "previous_plan": previous, "plan": plan,
            "evaluation_note": "A valid schema does not prove the prompt was understood. Review every value."}
