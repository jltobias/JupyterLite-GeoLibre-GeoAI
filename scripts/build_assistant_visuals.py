"""Original diagrams: local inference, approval and geospatial intelligence."""
import argparse
from build_learning_media import ROOT, rect, text, svg, write_or_check

ASSETS = ROOT / "book/assets/assistant"


def four_cards(title, subtitle, cards, footer):
    body = rect(0, 0, 1280, 600, "#f5f7fa", radius=0)
    body += text(30, 50, title, 34, "#14283f", 700)
    body += text(30, 94, subtitle, 23, "#45576c")
    for i, (heading, description) in enumerate(cards):
        x = 30 + i * 313
        color = ["#2459b8", "#087f78", "#7545b3", "#a96112"][i]
        body += rect(x, 140, 280, 290, "white", "#cddbe9")
        body += text(x+18, 184, heading, 26, color, 700)
        body += text(x+18, 235, description, 23, width=20, line=1.4)
        if i < 3:
            body += text(x+285, 300, "→", 24, "#45576c", 700)
    body += text(30, 495, footer, 25, "#14283f", 700, width=87)
    body += text(30, 579, "Original teaching schematic. Arrows are a reasoning sequence, not a historical timeline.", 18, "#45576c")
    return svg(body, title, subtitle + " " + "; ".join(h+": "+d for h,d in cards)+" "+footer, 1280, 600)


def render_all():
    title = "Two interfaces. One local inference service."
    body = rect(0, 0, 1280, 660, "#f5f7fa", radius=0)
    body += text(30, 50, title, 34, "#14283f", 700)
    body += text(30, 95, "Separate map state; separate permissions; shared responsibility to check results.", 23, "#45576c")
    rows = [
        ("NATIVE GEOLIBRE", "GeoLibre chat", "Local Ollama", "GeoLibre tools", "Inspect transcript and map; decline code fallback in this exercise."),
        ("NOTEBOOK LESSON", "JupyterLite prompt", "Local Ollama", "Validated plan", "Preview in Python → human approval → create a GeoLibre map."),
    ]
    for i, (label, left, center, right, caption) in enumerate(rows):
        y = 138 + i*220
        color = ["#2459b8", "#087f78"][i]
        body += text(30, y+15, label, 19, color, 700)
        for j, heading in enumerate([left, center, right]):
            x = 30+j*414
            body += rect(x, y+38, 370, 96, "white", color)
            body += text(x+20, y+79, heading, 27, color, 700)
            body += text(x+20, y+112, "On your desktop" if j==1 else "In your browser", 19, "#45576c")
            if j<2: body += text(x+377, y+99, "↔", 26, "#45576c")
        body += text(30, y+180, caption, 24, "#14283f")
    body += text(30, 622, "Local model ≠ fully offline app. Basemaps and remote data still use external services.", 23, "#a96112", 700)
    return {
        "two-routes": svg(body, title, "The native route sends a GeoLibre conversation to a local model and uses GeoLibre tools. The separate notebook route validates a bounded plan and requires human approval. Both render in the browser; neither runs the language model inside Pyodide.", 1280, 660),
        "approval-gate": four_cards("A proposal is not an instruction to execute", "Inspect meaning as well as format before a map changes.", [
            ("1 · Propose", "Local model returns four JSON settings for one invented layer."),
            ("2 · Validate", "Python rejects unknown fields, layers and invalid numbers."),
            ("3 · Preview", "Compute feature IDs and counts from the actual fixture."),
            ("4 · Approve", "A person checks the request, then chooses whether to apply."),
        ], "Valid JSON can still be wrong. A selected cell is not a predicted health outcome."),
        "geospatial-intelligence": four_cards("From geographic context to accountable action", "This book's synthesis: complementary capabilities, not a replacement ladder.", [
            ("GIS", "Locate, connect, measure and document geographic evidence."),
            ("GeoAI", "Learn patterns or assist operations while retaining spatial context."),
            ("Human judgment", "Question evidence, harms, benefits, alternatives and uncertainty."),
            ("Intelligence", "Use checked knowledge for a decision; evaluate what happened."),
        ], "World models are a further research direction. A chatbot plus a map is not one."),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for name, content in render_all().items():
        write_or_check(ASSETS / (name+".svg"), content, args.check)
    print("Verified" if args.check else "Generated", "three assistant/intelligence diagrams")
