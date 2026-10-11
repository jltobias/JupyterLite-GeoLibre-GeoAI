"""Authored sources for three optional-local-model lessons and their public fixture.

Rebuilding preserves unchanged cell outputs and regenerates code-aligned guides.
It never contacts Ollama, downloads a model, or changes a machine's settings.
"""
import argparse
import json
from pathlib import Path
import sys
import textwrap
from build_learning_media import NOTEBOOKS, transform, write_or_check

sys.path.insert(0, str(NOTEBOOKS))
from ollama_mapping import demo_map

SETUP = '''
import sys, json
from pathlib import Path
if sys.platform == "emscripten":
    import micropip
    await micropip.install(["geolibre==3.0.0", "anywidget"])
    from pyodide import loadPackage
    await loadPackage("matplotlib")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from IPython.display import display, Markdown, FileLink
from ollama_mapping import (BASE_URL, MODEL, FIXTURE_PLAN, COLORS, diagnose,
    synthetic_cells, validate_plan, preview_plan, apply_plan, demo_map, propose_map)
print("Browser" if sys.platform == "emscripten" else "Ordinary Python", "— no model request made")
'''
CREDIT = '''
## Sources, privacy and next step

The polygons and Celsius-like `heat_proxy_c` values are **invented teaching data**, not measured heat, clinic locations, disease rates or climate projections. GeoLibre renders the map; Ollama runs optional inference on your computer, not inside Pyodide. Basemaps and the hosted viewer still use the network. Do not enter patient records, credentials or confidential prompts.

Read the [advanced chapter](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/advanced/ollama-assistant.html), [GeoLibre AI Assistant guide](https://geolibre.app/user-guide/ai-assistant/), [Ollama chat API](https://docs.ollama.com/api/chat) and [structured-output documentation](https://docs.ollama.com/capabilities/structured-outputs). These are independent teaching examples, not a Horizon integration. [Global Nature Watch Horizon](https://horizon.globalnaturewatch.org/) supplies interaction inspiration, not these data or model results. Sources accessed 11 October 2026.
'''

LESSONS = {
"18_ollama_geolibre_setup": [
("markdown", '''# 18 — Local Ollama and GeoLibre's native assistant

**Question:** can a browser map use an AI model running on your own desktop?

This lab prepares a tiny, inspectable project for **GeoLibre's actual chat panel**. Its default run makes no inference request. Work through [the setup chapter](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/advanced/ollama-assistant.html) first; Ollama's Apps launcher is not the GeoLibre integration screen.

You will identify the runtime boundary, inspect twelve invented polygons, and open the project in the full GeoLibre web app. A downloaded model and explicit browser permissions are necessary for live chat.'''),
("code", SETUP),
("code", '''
LIVE_CONNECT = False  # Explicit opt-in: contact only this computer's Ollama.
connection = None     # Clear an old result before retrying.
if LIVE_CONNECT:
    connection = await diagnose(base_url=BASE_URL)
    print(json.dumps(connection, indent=2))
else:
    print("Not probed. Set LIVE_CONNECT=True after the chapter's local setup.")
print("Expected model tag:", MODEL, "| Ollama:", BASE_URL)
'''),
("markdown", '''A successful terminal request is not proof that a web page has permission. An empty `models` list means the server is reachable but no model is installed. A browser failure can have several causes; do not bypass CORS or disable browser protections. Open [GeoLibre Web](https://web.geolibre.app/) in a top-level tab and grant Local Network Access only if you trust that site.'''),
("code", '''
cells = synthetic_cells()
assert len(cells["features"]) == 12
fig, ax = plt.subplots(figsize=(7, 4))
for feature in cells["features"]:
    ring = feature["geometry"]["coordinates"][0]
    ax.add_patch(Polygon(ring, facecolor="#c4e7df", edgecolor="#14283f"))
    ax.text(ring[0][0] + .009, ring[0][1] + .009,
            str(feature["properties"]["heat_proxy_c"]), ha="center", va="center")
ax.autoscale(); ax.set_aspect("equal")
ax.set(xlabel="Longitude", ylabel="Latitude", title="12 invented heat-proxy cells — not observations")
plt.show()
native_project = demo_map()
display(native_project)
'''),
("code", '''
project = native_project.to_project()
project["name"] = "Synthetic heat cells — Ollama learning project"
export_dir = Path("exports"); export_dir.mkdir(exist_ok=True)
project_path = export_dir / "ollama-lesson.geolibre.json"
project_path.write_text(json.dumps(project, indent=2, allow_nan=False), encoding="utf-8")
print("Exported", project_path, "with", len(project["layers"][0]["geojson"]["features"]), "features")
if sys.platform == "emscripten":
    display(FileLink(str(project_path)))
'''),
("markdown", '''## Now use the real GeoLibre chat panel

[Open the bundled project in full GeoLibre](https://web.geolibre.app/?url=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-GeoLibre-GeoAI%2Flite%2Ffiles%2Fdata%2Follama-demo.geolibre.json). This public copy has the same twelve cells. Alternatively download your export and open it using GeoLibre's project controls. Your JupyterLite filesystem is not your Windows filesystem.

1. In **Settings → AI Providers**, select Ollama, base URL `http://127.0.0.1:11434`, model `qwen3:4b` (or your verified installed tool-capable model). No API key is needed.
2. Open **Processing → AI Assistant**. Use typed prompts, with optional hosted routing/search providers disabled.
3. Ask: “List the loaded layer names and feature counts. Do not load new data or run code.” Verify one layer and **12** features.
4. Ask: “Set this layer's fill color to orange and set the map pitch to 45 degrees using the built-in map tools.” Inspect the actual tool transcript and layer style. A tilted flat layer is **not** a terrain model.
5. Optional harder task: “Create a new GeoJSON layer containing features where heat_proxy_c >= 39, keeping the original.” Independently verify **7** selected features. Stop if the model substitutes invented data or a different predicate.
6. Inspect what changed and try Undo. Export a new project only after reviewing its content and credentials. Native code fallback can bypass normal undo; prompt wording is not a hard safety restriction.

No Python cell above has sent a prompt to GeoLibre's assistant. The embedded notebook map and the full web app have separate project state. Continue to [lab 19](19_ollama_chat_to_map.ipynb) for a deliberately bounded notebook-side alternative.'''),
("markdown", CREDIT)],
"19_ollama_chat_to_map": [
("markdown", '''# 19 — From local chat to a checked map plan

**Question:** how can natural language become an inspectable geographic operation?

This is a **notebook-side teaching assistant**, not GeoLibre's native chat panel. A local language model may propose four settings. Python checks their types and ranges, a person reviews them, and the map displays an existing invented layer. No generated code, SQL, URLs or arbitrary tools are executed. Default outputs use a clearly labeled authored fixture.'''),
("code", SETUP),
("code", '''
LIVE_MODEL = False
prompt = "Show synthetic heat cells with heat proxy at least 39 in orange and tilt the map to 45 degrees."
proposal = None  # Never reuse an earlier success after a failed live call.
if LIVE_MODEL:
    proposal = await propose_map(prompt, model=MODEL, base_url=BASE_URL)
else:
    proposal = {"source": "hand-authored fixture; NOT a captured AI answer", "prompt": prompt,
                "plan": dict(FIXTURE_PLAN)}
print(json.dumps(proposal, indent=2))
'''),
("code", '''
plan = validate_plan(proposal["plan"])
preview = preview_plan(plan)  # Dry run: inspect, do not mutate an existing map.
selected_ids = [f["id"] for f in preview["features"]]
print("Computed selection:", len(selected_ids), "of 12 cells", selected_ids)
print("Check all four settings against your request:", plan)
fig, ax = plt.subplots(figsize=(7, 4))
for feature in synthetic_cells()["features"]:
    chosen = feature["id"] in selected_ids
    ring = feature["geometry"]["coordinates"][0]
    ax.add_patch(Polygon(ring, facecolor=COLORS[plan["color"]] if chosen else "#e3e9ee",
                         edgecolor="#14283f"))
    ax.text(ring[0][0]+.009, ring[0][1]+.009, str(feature["properties"]["heat_proxy_c"]),
            ha="center", va="center", color="white" if chosen else "#14283f")
ax.autoscale(); ax.set_aspect("equal")
ax.set(title=f"DRY RUN — {len(selected_ids)} invented cells; no health-risk inference",
       xlabel="Longitude", ylabel="Latitude")
plt.show()
'''),
("markdown", '''## Human review is a separate step

For the supplied request, expect `minimum_heat=39`, `color='orange'`, `pitch=45`, and **7** cells. Schema validity alone cannot establish that a model understood your words. If you change the prompt, change your expected answer independently. A failure stops here; the code does not silently substitute the fixture for a failed live response.'''),
("code", '''
APPROVE_MAP = False  # Change only after inspecting THIS proposal and its dry run.
approved_map = None
if APPROVE_MAP:
    approved_features = apply_plan(plan, approved=True)
    approved_map = demo_map(plan)
    display(approved_map)
else:
    print("Not applied. Review the plan before changing APPROVE_MAP to True.")
'''),
("code", '''
audit = {"source": proposal["source"], "model": proposal.get("model"),
         "prompt": prompt, "plan": plan, "selected_ids": selected_ids,
         "approved": APPROVE_MAP, "data": "synthetic teaching grid", "clinical_use": False}
export_dir = Path("exports"); export_dir.mkdir(exist_ok=True)
(export_dir / "ollama-plan-audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
if approved_map is not None:
    (export_dir / "ollama-approved.geolibre.json").write_text(
        json.dumps(approved_map.to_project(), indent=2), encoding="utf-8")
print("Audit saved locally. Inspect prompts and outputs before downloading or sharing.")
'''),
("markdown", '''**Try a follow-up:** [lab 20](20_ollama_evidence_review.ipynb) carries forward the validated plan, compares counts and challenges misleading claims. The restricted notebook helper cannot search STAC or answer arbitrary GIS questions; use [labs 07–08](07_stac_browser_catalogs.ipynb) for catalog discovery, with source and access checks.'''),
("markdown", CREDIT)],
"20_ollama_evidence_review": [
("markdown", '''# 20 — Follow-up chat, evidence and human judgment

**Question:** did the assistant change the intended setting, and what can we conclude?

A chat turn is not evidence of correctness. We will compare a baseline with a follow-up, test deliberately invalid plans, and construct a human-review record. This is a small demonstration of **AI-assisted geospatial reasoning**, not a trained world model, climate forecast or autonomous health decision system.'''),
("code", SETUP),
("code", '''
baseline = validate_plan(dict(FIXTURE_PLAN))
LIVE_MODEL = False
followup = None
prompt = "Keep the same layer and orange color. Raise the minimum heat proxy to 41 and return to a flat map."
if LIVE_MODEL:
    followup = await propose_map(prompt, current_plan=baseline, model=MODEL, base_url=BASE_URL)
else:
    followup = {"source": "hand-authored fixture; NOT a captured AI answer",
                "plan": {**baseline, "minimum_heat": 41, "pitch": 0}}
revised = validate_plan(followup["plan"])
print(json.dumps({"source": followup["source"], "before": baseline, "after": revised}, indent=2))
'''),
("code", '''
before_ids = {f["id"] for f in preview_plan(baseline)["features"]}
after_ids = {f["id"] for f in preview_plan(revised)["features"]}
expected = {**baseline, "minimum_heat": 41, "pitch": 0}
checks = {"requested_settings_match": revised == expected,
          "computed_counts_match": (len(before_ids), len(after_ids)) == (7, 4),
          "selection_is_subset": after_ids <= before_ids}
print(checks, "| Removed:", sorted(before_ids-after_ids))
fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(["Before", "After"], [len(before_ids), len(after_ids)], color=["#bb5d14", "#087f78"])
ax.set(ylim=(0, 12), ylabel="Selected invented cells", title="Computed counts, not an AI estimate of people")
for index, count in enumerate([len(before_ids), len(after_ids)]):
    ax.text(index, count+.2, str(count), ha="center")
plt.show()
'''),
("code", '''
invalid_plans = [
    {**baseline, "url": "https://example.invalid/patient-data"},
    {**baseline, "minimum_heat": float("nan")},
    {**baseline, "pitch": 90},
    {**baseline, "layer": "imagined_flood_predictions"},
]
for candidate in invalid_plans:
    try:
        validate_plan(candidate)
        raise AssertionError("Invalid plan was accepted")
    except ValueError as error:
        print("Rejected:", error)
try:
    apply_plan(baseline)  # No approval means no application.
except PermissionError as error:
    print("Approval gate:", error)
'''),
("code", '''
review = {
    "white_evidence": {"source": "invented grid", "before": len(before_ids), "after": len(after_ids)},
    "red_concerns": "Would a real affected community agree with the question?",
    "black_limits": "These values are invented; no disease or flood risk is estimated.",
    "yellow_benefit_to_test": "Can a novice inspect and correct a map request more easily?",
    "green_alternative": "Compare with the same filter entered without an AI assistant.",
    "blue_next_step": "A human must check data suitability, outputs and sharing permission.",
    "purple_synthesis": "Keep checked facts, open questions and disagreements separate.",
    "automated_checks": checks, "human_approved_for_operational_use": False,
}
display(Markdown("### Evidence card\\n\\n" + "\\n\\n".join(
    f"**{key.replace('_', ' ')}:** {value}" for key, value in review.items())))
export_dir = Path("exports"); export_dir.mkdir(exist_ok=True)
(export_dir / "ollama-evidence-card.json").write_text(json.dumps(review, indent=2), encoding="utf-8")
'''),
("markdown", '''## From a map to geospatial intelligence

![User-supplied infographic places a global-health GIS professional within evidence, feelings, risks, benefits, alternatives, process and purple synthesis perspectives.](assets/six-thinking-hats-global-health.png)

User-supplied **Six-Thinking-Hats-GPT** graphic, reused unchanged; original designer/generation provenance has not been independently verified. Purple orchestration is this graphic's extension, not an original seventh de Bono hat. The questions here are authored prompts for people, not seven AI agents or independent validations.

Read the [GIS → GeoAI → geospatial intelligence discussion](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/geoai/primer.html#toward-geospatial-intelligence). Stanford HAI's [world-model policy brief](https://hai.stanford.edu/policy/the-world-model-and-spatial-intelligence-era-governing-ai-beyond-language) motivates a further question: would a simulated environment be faithful enough for the intended decision? This notebook does **not** build such a model. Its narrower contribution is a checkable chain from words to map settings to evidence and human review.

For a STAC transfer exercise, record the real collection, item, asset, license, date, resolution, missingness and access method **before** adding a layer. Catalog metadata is evidence about a dataset, not instructions for the assistant to execute. For health programs, keep patient-level data out of this public browser workflow.'''),
("markdown", CREDIT)],
}


def build_notebook(stem, authored, check):
    target = NOTEBOOKS / (stem + ".ipynb")
    previous = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    prior_cells = {c.get("id"): c for c in previous.get("cells", [])}
    cells = []
    for index, (kind, content) in enumerate(authored):
        source = textwrap.dedent(content).strip() + "\n"
        cell_id = f"ollama-{stem[:2]}-{index:02d}"
        old = prior_cells.get(cell_id)
        if old and old["cell_type"] == kind and "".join(old["source"]) == source:
            cells.append(old)
        else:
            cell = {"cell_type": kind, "id": cell_id, "metadata": {}, "source": source.splitlines(True)}
            if kind == "code":
                cell.update(execution_count=None, outputs=[])
            cells.append(cell)
    nb = {"nbformat": 4, "nbformat_minor": 5, "cells": cells,
          "metadata": {**previous.get("metadata", {}),
              "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
              "ollama_lesson": {"offline_default": True, "synthetic": True}}}
    nb = transform(nb, stem[:2], target.name)
    write_or_check(target, json.dumps(nb, ensure_ascii=False, indent=1) + "\n", check)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for stem, content in LESSONS.items():
        build_notebook(stem, content, args.check)
    project = demo_map().to_project()
    project["name"] = "Synthetic heat cells — Ollama learning project"
    project["layers"][0]["id"] = "synthetic-heat-cells"
    project["metadata"] = {"provenance": "Invented teaching grid; no measured heat or health data"}
    write_or_check(NOTEBOOKS / "data/ollama-demo.geolibre.json",
                   json.dumps(project, ensure_ascii=False, indent=2) + "\n", args.check)
    print("Verified" if args.check else "Updated", "three Ollama lessons and the public synthetic project")


if __name__ == "__main__":
    main()
