"""Validate every notebook; optionally execute the deterministic Astra labs.

python scripts/validate_notebooks.py --execute
Add --save-outputs when intentionally refreshing the book's static figures.
"""
import argparse
import ast
import json
from pathlib import Path
import tempfile

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "book" / "notebooks"


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
        if not nb.metadata.get("cognition", {}).get("synthetic", False):
            continue
        # Use a temporary notebook directory so exported fixture files never
        # pollute the distributed contents or overwrite a user's exports.
        with tempfile.TemporaryDirectory(prefix="geolibre-lab-") as temp:
            for helper in NOTEBOOKS.glob("*.py"):
                Path(temp, helper.name).write_bytes(helper.read_bytes())
            client = NotebookClient(nb, timeout=180, kernel_name="python3",
                                    resources={"metadata": {"path": temp}})
            client.execute()
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
