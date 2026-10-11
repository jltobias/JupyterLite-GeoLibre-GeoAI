"""Validate every notebook; optionally execute synthetic and bundled-data labs.

python scripts/validate_notebooks.py --execute
Add --save-outputs when intentionally refreshing the book's static figures.
"""
import argparse
import ast
import json
from pathlib import Path
import shutil
import tempfile

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "book" / "notebooks"
BUNDLED_LABS = {"16_sea_level_rise_sat_scan_geoai.ipynb", "17_rewiring_global_health_six_hats.ipynb",
                "18_ollama_geolibre_setup.ipynb", "19_ollama_chat_to_map.ipynb", "20_ollama_evidence_review.ipynb"}


def executable_offline(path, nb):
    """Explicit allowlist: a report derivative is not synthetic training data."""
    return nb.metadata.get("cognition", {}).get("synthetic", False) or path.name in BUNDLED_LABS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--save-outputs", action="store_true")
    args = parser.parse_args()
    if args.save_outputs and not args.execute:
        parser.error("--save-outputs requires --execute")
    paths = sorted(NOTEBOOKS.glob("*.ipynb"))
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                compile(cell.source, f"{path.name}:cell-{i}", "exec",
                        flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        print("Valid:", path.name, flush=True)
    if not args.execute:
        return
    from nbclient import NotebookClient
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        if not executable_offline(path, nb):
            continue
        # Use a temporary notebook directory so exported fixture files never
        # pollute the distributed contents or overwrite a user's exports.
        with tempfile.TemporaryDirectory(prefix="geolibre-lab-") as temp:
            for helper in NOTEBOOKS.glob("*.py"):
                Path(temp, helper.name).write_bytes(helper.read_bytes())
            if path.name in BUNDLED_LABS:
                shutil.copytree(NOTEBOOKS / "data", Path(temp, "data"))
            if path.name.startswith("16_"):
                nb.cells.append(nbformat.v4.new_code_cell("""
assert len(risk) == 10 and len(long) == 30
assert [frame.name for frame in fig.frames] == ['A', 'B', 'C']
assert all(set(frame.data[0].ids) == set(risk.city_label) for frame in fig.frames)
assert len({frame.data[0].marker.sizeref for frame in fig.frames}) == 1
assert fig.layout.coloraxis.cmin == 0
assert fig.layout.coloraxis.cmax == float(long.scenario_indicator.max())
np.testing.assert_allclose(fig3d.data[0].z, risk.relative_risk)
np.testing.assert_allclose(scenario_table['C'], risk.flood_c_mean)
"""))
            client = NotebookClient(nb, timeout=180, kernel_name="python3",
                                    resources={"metadata": {"path": temp}})
            client.execute()
            if path.name.startswith("16_"):
                nb.cells.pop()  # test-only consumer assertions are not teaching cells
            artifacts = sorted(Path(temp, "exports").glob("*.json"))
            for artifact in artifacts:
                json.loads(artifact.read_text(encoding="utf-8"),
                           parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
            print(f"Executed: {path.name}; {len(artifacts)} JSON exports", flush=True)
        if args.save_outputs:
            # Saved static plots and HTML work in the book; live widgets need
            # a kernel and should be constructed by running the notebook.
            nb.metadata.pop("widgets", None)
            for cell in nb.cells:
                if cell.cell_type == "code":
                    cell.outputs = [o for o in cell.outputs if
                        "application/vnd.jupyter.widget-view+json" not in o.get("data", {})]
            nbformat.write(nb, path)


if __name__ == "__main__":
    main()
