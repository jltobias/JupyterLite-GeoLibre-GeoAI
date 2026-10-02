"""Build JupyterLite with its three required browser extensions explicitly.

JupyterLite's default scan only sees sys.prefix, which can omit pip --user
installs (including Windows Store Python). Resolve the actual installed
distributions rather than shipping an apparently successful site with no kernel.
"""
from importlib.metadata import distribution
import json
from pathlib import Path

REQUIRED = {
    "jupyterlite-pyodide-kernel": "@jupyterlite/pyodide-kernel-extension",
    "jupyterlab_widgets": "@jupyter-widgets/jupyterlab-manager",
    "anywidget": "anywidget",
}


def extension_paths():
    paths = []
    for package, name in REQUIRED.items():
        dist = distribution(package)
        suffix = f"/labextensions/{name}/package.json"
        matches = [dist.locate_file(f).resolve().parent for f in dist.files or []
                   if str(f).replace("\\", "/").endswith(suffix)]
        if not matches:
            raise RuntimeError(f"Browser extension missing from installed {package}")
        paths.append(str(matches[0]))
    return paths


def validate_build(output):
    config = json.loads((output / "jupyter-lite.json").read_text(encoding="utf-8"))
    bundled = {x["name"] for x in config["jupyter-config-data"].get("federated_extensions", [])}
    missing = set(REQUIRED.values()) - bundled
    if missing:
        raise RuntimeError(f"Built site is missing required browser extensions: {sorted(missing)}")
    print("Verified browser kernel and widget extensions:", ", ".join(sorted(bundled)))


def main():
    from jupyterlite_core.app import main as lite_main
    root = Path(__file__).resolve().parents[1]
    output = root / "site" / "lite"
    try:
        lite_main(argv=["build", "--lite-dir", str(root), "--contents", str(root / "book/notebooks"),
                       "--output-dir", str(output), "--ignore-sys-prefix",
                       "--LiteBuildConfig.federated_extensions=" + json.dumps(extension_paths())])
    except SystemExit as exc:
        if exc.code not in (None, 0):
            raise
    validate_build(output)


if __name__ == "__main__":
    main()
