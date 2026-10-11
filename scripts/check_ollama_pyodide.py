"""Automated runtime test: real Pyodide, mocked Ollama HTTP responses.

Tests our helper in a browser engine without controlling an external app UI,
calling a user's service, granting permissions, or disabling browser security.
It does NOT verify native GeoLibre or production-origin connectivity.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    from playwright.sync_api import sync_playwright
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="Locally served built site")
    args = parser.parse_args()
    schema = json.loads((ROOT / "site/lite/extensions/@jupyterlite/pyodide-kernel-extension/static/schema/kernel.v0.schema.json").read_text())
    runtime_url = schema["properties"]["pyodideUrl"]["default"]
    source = (ROOT / "book/notebooks/ollama_mapping.py").read_text(encoding="utf-8")
    calls = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        def mocked(route):
            request = route.request
            path = request.url.split(":11434", 1)[1]
            headers = {"Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                       "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                       "Access-Control-Allow-Headers": "content-type"}
            if request.method == "OPTIONS":
                route.fulfill(status=204, headers=headers)
                return
            calls.append(path)
            replies = {"/api/tags": {"models": [{"name": "qwen3:4b"}]},
                       "/api/version": {"version": "mock-server-not-a-live-result"},
                       "/api/show": {"capabilities": ["completion", "thinking", "tools"]}}
            if path == "/api/chat":
                body = request.post_data_json
                assert body["stream"] is False and body["think"] is False
                plan = {"layer": "synthetic_cells", "minimum_heat": 39, "color": "orange", "pitch": 45}
                payload = {"model": "qwen3:4b", "done": True, "done_reason": "stop",
                           "message": {"content": json.dumps(plan)}}
            else:
                payload = replies[path]
            route.fulfill(status=200, headers=headers, content_type="application/json", body=json.dumps(payload))
        page.route("http://127.0.0.1:11434/**", mocked)
        page.goto(args.base_url.rstrip("/") + "/intro.html")
        page.add_script_tag(url=runtime_url)
        page.evaluate("async () => { window.runtime = await loadPyodide(); }")
        page.evaluate("source => runtime.FS.writeFile('/home/pyodide/ollama_mapping.py',source)", source)
        result = page.evaluate("""async () => await runtime.runPythonAsync(`
import json, sys
from ollama_mapping import diagnose, propose_map, preview_plan, local_json
assert sys.platform == 'emscripten'
status = await diagnose()
assert status['reachable'] and status['models'] == ['qwen3:4b']
answer = await propose_map('Select >=39 in orange at 45 degrees')
assert len(preview_plan(answer['plan'])['features']) == 7
json.dumps({'runtime': sys.version.split()[0], 'mocked_plan': answer['plan'], 'selected_count': 7})
`)""")
        assert calls == ["/api/version", "/api/tags", "/api/tags", "/api/show", "/api/chat"], calls
        # A real Fetch rejection exercises the diagnostic path, not an invented success.
        page.unroute("http://127.0.0.1:11434/**", mocked)
        page.route("http://127.0.0.1:11434/**", lambda route: route.abort("failed"))
        failure = page.evaluate("""async () => await runtime.runPythonAsync(`
failure = await diagnose()
assert not failure['reachable'] and 'models' not in failure
json.dumps(failure)
`)""")
        print("Real Pyodide / mocked service:", result)
        print("Fetch failure handled:", failure)
        browser.close()


if __name__ == "__main__":
    main()
