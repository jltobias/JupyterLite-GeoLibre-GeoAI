"""Explicit, server-side runner for request JSON exported by the Astra labs.

Preview: python scripts/run_astra.py request.json
Send:    python scripts/run_astra.py request.json --send --output response.json
Tools:   add --evidence accessibility_evidence.json for notebook 15.
The API key stays in this CPython process, outside the static site and browser.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "book" / "notebooks"))
from astra_lab import ACCESS_TOOL, MODEL, dispatch_tool, response_text


def run_request(request, evidence, send):
    """Bounded Responses tool loop; send is injectable for offline testing."""
    if request.get("model") != MODEL:
        raise ValueError(f"These labs target {MODEL}")
    if request.get("tools") and request["tools"] != [ACCESS_TOOL]:
        raise ValueError("Only the lab's accessibility tool is supported")
    body = {**request, "store": False}
    body["input"] = list(request["input"])
    for _ in range(4):
        response = send(body)
        if response.get("status") != "completed":
            raise ValueError("Incomplete API response; no result accepted")
        calls = [x for x in response.get("output", []) if x.get("type") == "function_call"]
        if not calls:
            json.loads(response_text(response))
            return response
        if evidence is None or len(calls) > 4:
            raise ValueError("Tool calls require local --evidence and at most four calls per round")
        # Keep reasoning items with calls when continuing a stateless Responses request.
        body["input"].extend(response["output"])
        for call in calls:
            result = dispatch_tool(call["name"], call["arguments"], evidence)
            body["input"].append({"type": "function_call_output", "call_id": call["call_id"],
                                   "output": json.dumps(result, allow_nan=False)})
    raise ValueError("Tool round limit reached; no further API calls made")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("--send", action="store_true", help="Make billable API calls")
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--output", type=Path, default=Path("astra_response.json"))
    args = parser.parse_args()
    if sys.platform == "emscripten":
        parser.error("Run this script in full CPython, outside JupyterLite")
    raw = args.request.read_bytes()
    request = json.loads(raw)
    if request.get("model") != MODEL:
        parser.error(f"Expected model {MODEL}")
    print(f"Model: {MODEL}; request: {len(raw):,} bytes; sha256: {hashlib.sha256(raw).hexdigest()}")
    if not args.send:
        print("Preview only. Use --send to call the API with OPENAI_API_KEY from your environment.")
        return
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        parser.error("Set OPENAI_API_KEY in this server-side environment")
    evidence = json.loads(args.evidence.read_text(encoding="utf-8")) if args.evidence else None

    def send(body):
        req = urllib.request.Request("https://api.openai.com/v1/responses",
            data=json.dumps(body, allow_nan=False).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as result:
                response = json.load(result)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"OpenAI HTTP {exc.code}; check access, quota, and request schema") from None
        print("API usage:", json.dumps(response.get("usage", {})))
        return response

    response = run_request(request, evidence, send)
    args.output.write_text(json.dumps(response, indent=2, allow_nan=False), encoding="utf-8")
    print("Saved response:", args.output)


if __name__ == "__main__":
    main()
