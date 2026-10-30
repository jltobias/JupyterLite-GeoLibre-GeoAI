"""Build the reproducible RustGIS bridge lesson and public synthetic snapshot."""
import argparse
import json
import sys
import textwrap
from build_learning_media import ROOT, NOTEBOOKS, transform, write_or_check

sys.path.insert(0, str(NOTEBOOKS))
from rustgis_bridge import sample_sites, fit_groups

STEM = '22_rustgis_geoai_bridge'
AUTHORED = [
('markdown', '''# 22 — One GeoAI result, GeoLibre and RustGIS

**Question:** can we fit a simple geographic pattern in the browser, then inspect the same result in two mapping tools?

[Read What is RustGIS?](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/platforms/rustgis.html) for the illustrated introduction and credits. Run with **Shift+Enter**, from top to bottom. The data are **20 invented points**, not real facilities or patient locations. No account, API key, Ollama, native Rust or RustGIS installation is required.

![Python fits groups in JupyterLite; GeoJSON carries the result to separate GeoLibre and RustGIS browser apps.](assets/rustgis/bridge.svg)

JupyterLite runs Python through Pyodide. RustGIS Web runs a separate Rust/WebAssembly GIS. The native Python `rustgis` package needs ordinary CPython; **do not install it with micropip here**. GeoJSON is our portable data format, not a shared project or automatic synchronization protocol.'''),
('code', '''
import sys
if sys.platform == "emscripten":
    from pyodide_js import loadPackage
    await loadPackage(["numpy", "matplotlib", "scikit-learn", "ipython"])
import json
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, FileLink
from rustgis_bridge import (sample_sites, validate_sites, fit_groups, group_counts,
                            plot_sites, export_groups, public_view_url)
print("Tools ready. The data will be invented locally; no model has run yet.")
'''),
('markdown', '''## 1. Start with a map, not an answer

These points form two small grids and two isolated locations near London. They are deliberately invented so we can understand an algorithm without exposing anyone's location. A dot's position is a **measurement input in the example**, not evidence that a clinic exists there. The tile-free plot is a coordinate view, not a road or travel-time map.'''),
('code', '''
sites = sample_sites()
validate_sites(sites)
print(f"{len(sites['features'])} invented points")
print(json.dumps(sites['features'][0], indent=2))
plot_sites(sites, "Invented points: mapping before machine learning")
plt.show()
'''),
('markdown', '''## 2. Add one GeoAI step

**DBSCAN** is an unsupervised learning method: it computes groups from the locations without being given correct labels. The helper calls scikit-learn's `DBSCAN(eps=radius_m / EARTH_RADIUS_M, min_samples=3, metric="haversine", algorithm="brute").fit_predict(...)`. It first reverses GeoJSON longitude/latitude into latitude/longitude and converts degrees to radians.

The 350-meter setting is a chosen neighborhood distance, **not** a learned disease-transmission distance. Connected neighborhoods can make a group wider than 350 meters. A label of `-1` means unassigned at this setting; it does not mean an error or a low-risk place. No disease, population, roads, capacity or service-use data enter this model.'''),
('code', '''
radius_m = 350
grouped = fit_groups(sites, radius_m=radius_m)
print("Group label -> number of points:", group_counts(grouped))
plot_sites(grouped, f"DBSCAN location groups: {radius_m} m neighbors")
plt.show()
'''),
('markdown', '''## 3. Ask how much the assumption matters

Try a smaller neighborhood. This cell prints comparison fits while keeping `grouped` unchanged for export. To export a new setting, change `radius_m` above and rerun that cell and the export cell. Group colors and numbers are identifiers, not severity ranks.

**Health-program transfer:** an analyst might explore candidate geographic groupings of public service locations. That still requires verified facilities, demand, roads, travel time, staffing and community review before making a service-placement decision. These invented groups establish none of those facts.'''),
('code', '''
for trial_radius in (150, 350):
    trial = fit_groups(sites, radius_m=trial_radius)
    print(f"{trial_radius} m:", group_counts(trial))
'''),
('markdown', '''## 4. Export your result, including its limits

Run the cell, then **download both files**. In JupyterLite, use the links or right-click each file in the `exports` folder and select Download. Files inside the browser's notebook filesystem are not automatically visible to another tab.

Open [RustGIS Web](https://web.rustgis.app/?blank), use **Add Data** (or drag the downloaded `.geojson` onto the map), and inspect a feature's `id`, `group`, `neighbor_radius_m` and `synthetic` fields. Style categories by `group` if desired. Keep the provenance JSON alongside the data; it is a method card, not a layer. RustGIS may save its own `.rgis` project; do not treat that as a GeoLibre project.'''),
('code', '''
data_path, provenance_path = export_groups(grouped)
print("Notebook files saved; download them before importing into another app.")
if sys.platform == "emscripten":
    display(FileLink(str(data_path)), FileLink(str(provenance_path)))
else:
    # Static Book outputs must not link to files created in a temporary test kernel.
    print(data_path, provenance_path)
'''),
('markdown', '''## 5. Open a ready-made 2D or globe example

These links load the **published 350-meter snapshot** directly from GitHub Pages, which must be reachable and allow cross-origin requests. They do **not** upload or show your edits. To inspect changed results, use the file transfer above. A globe changes the view; there are no measured heights or 3D risk estimates in this dataset. If a hosted app or URL fails, use the saved plots and downloaded GeoJSON.'''),
('code', '''
display(Markdown(
    f"[Open the published example in RustGIS (2D)]({public_view_url()}) · "
    f"[Open the same example on a globe]({public_view_url(globe=True)})"
))
'''),
('markdown', '''## 6. Optional: inspect the same current result in GeoLibre

Change the flag only when you want the hosted interactive viewer. This uses the repository's browser adapter, with the same GeoJSON already computed in `grouped`. It does not refit a model. Re-run after changing the earlier result. Compare feature values across apps; styling and camera settings belong to each app.'''),
('code', '''
SHOW_GEOLIBRE = False
comparison_map = None
if SHOW_GEOLIBRE:
    if sys.platform == "emscripten":
        await loadPackage("micropip")
        import micropip
        await micropip.install(["geolibre==3.0.0", "anywidget"])
    from geolibre_lite import LiteMap
    comparison_map = LiteMap(center=(-0.11, 51.505), zoom=11)
    comparison_map.add_geojson(grouped, name="Invented DBSCAN groups")
    display(comparison_map)
else:
    print("Optional GeoLibre view is off. Plots, GeoJSON and RustGIS links remain available.")
'''),
('markdown', '''## What did we learn?

| Operation | What changed? | Model fitting? |
|---|---|---|
| Plot the input points | A view of the supplied coordinates | No |
| Fit DBSCAN | Group membership derived from geographic neighbors | Yes, unsupervised learning |
| Change the radius and refit | The grouping assumption and possibly the labels | Yes |
| Open 2D, globe or GeoLibre | How an existing result is displayed | No |
| Export GeoJSON | Where data can be read | No |

For a separate **native CPython 3.12+** environment, the [RustGIS Python documentation](https://github.com/opengeos/RustGIS/blob/8b322b290448e468c8972df9b1f601d3a72f7d53/docs/python.md) describes `pip install rustgis`, `rustgis.Session()`, `session.add_geojson(...)` and `session.save("example.rgis")`. That route is not executed in this browser lesson.

## Sources and attribution

- **RustGIS:** Wu, Q., Rincón Albarracín, J. G., Filho, E., Hofbauer, D., Fitzgerald, M., & Strebel, D. (2026). *RustGIS: A fast, free and open-source GIS in pure Rust for mapping, analyzing and sharing geospatial data.* [Zenodo, doi:10.5281/zenodo.23633281](https://doi.org/10.5281/zenodo.23633281). Apache-2.0; [source and contributors](https://github.com/opengeos/RustGIS). Web launch parameters: [installation documentation, reviewed revision](https://github.com/opengeos/RustGIS/blob/8b322b290448e468c8972df9b1f601d3a72f7d53/docs/installation.md).
- **Companion teaching context:** James L. Tobias, [JupyterLite-RustGIS](https://github.com/jltobias/JupyterLite-RustGIS), reviewed 2026-10-30. Its notebooks and maps are linked, not copied into this lesson.
- **DBSCAN implementation:** [scikit-learn DBSCAN reference](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html). Geographic distance is interpreted in meters after conversion to angular distance.
- **GeoLibre:** Qiusheng Wu and contributors; [software, citation and data credits](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/platforms/geolibre.html).

The synthetic dataset, runtime illustration and lesson are authored for this repository. No external source dataset, health record, RustGIS screenshot or companion artwork is reproduced. Replacing a basemap or viewer does not change data attribution.'''),
]


def build_notebook(check):
    target = NOTEBOOKS / (STEM + '.ipynb')
    previous = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
    old = {cell.get('id'): cell for cell in previous.get('cells', [])}
    cells = []
    for index, (kind, content) in enumerate(AUTHORED):
        source = textwrap.dedent(content).strip() + '\n'
        identifier = f'rustgis-22-{index:02d}'
        prior = old.get(identifier)
        if prior and prior['cell_type'] == kind and ''.join(prior['source']) == source:
            cells.append(prior)
        else:
            cell = {'cell_type': kind, 'id': identifier, 'metadata': {}, 'source': source.splitlines(True)}
            if kind == 'code':
                cell.update(execution_count=None, outputs=[])
            cells.append(cell)
    notebook = {'nbformat': 4, 'nbformat_minor': 5, 'cells': cells,
        'metadata': {**previous.get('metadata', {}),
            'kernelspec': {'display_name': 'Python 3 (ipykernel)', 'language': 'python', 'name': 'python3'},
            'cognition': {'synthetic': True}}}
    write_or_check(target, json.dumps(transform(notebook, '22', target.name), ensure_ascii=False, indent=1) + '\n', check)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    build_notebook(args.check)
    snapshot = fit_groups(sample_sites(), radius_m=350)
    write_or_check(NOTEBOOKS/'data/rustgis-groups.geojson', json.dumps(snapshot, indent=2, allow_nan=False)+'\n', args.check)
    print('Verified' if args.check else 'Built', 'RustGIS notebook and synthetic public snapshot')


if __name__ == '__main__':
    main()
