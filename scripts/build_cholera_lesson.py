"""Build the five-minute lesson, genuine fitted snapshots and local presentation.

No network access. Historical source CSVs are never modified. Saved outputs from
unchanged notebook cells are retained. The presentation switches fitted snapshots;
only the runnable notebook fits Python models in the visitor's browser.
"""
import argparse
import json
from pathlib import Path
import sys
import textwrap

from build_learning_media import ROOT, NOTEBOOKS, transform, write_or_check, svg, text, rect, path

sys.path.insert(0, str(NOTEBOOKS))
from cholera_demo import load_records, cluster_locations, summary, local_xy, color_for, geolibre_map, RADII

ASSETS = NOTEBOOKS / 'assets/cholera'
STEM = '21_cholera_geoai_first_steps'
AUTHORED = [
('markdown', '''# 21 — From John Snow’s map to GeoAI

**Can a model find nearby groups before we reveal the pumps?**

Use the [five-minute presentation walkthrough](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/presentations/cholera-five-minutes.html) first. It has saved views for a talk; this notebook performs the actual Python calculations. Run cells from top to bottom with **Shift+Enter**. No AI account, API key, Ollama or live outbreak-data service is needed.

**JupyterLite** runs the Python workbench in your browser. **DBSCAN** supplies a small machine-learning method. **GeoLibre** provides an optional interactive map. The tile-free analytical views work even when the external map viewer is unavailable, after the notebook and packages have loaded.

Historical teaching data, not a contemporary surveillance dataset. Do not replace it with patient addresses in this public site.'''),
('code', '''
import sys
if sys.platform == "emscripten":
    from pyodide_js import loadPackage
    await loadPackage(["numpy", "pandas", "matplotlib", "scikit-learn", "micropip"])
    import micropip
    await micropip.install("ipywidgets")
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from sklearn.cluster import DBSCAN
from IPython.display import display, clear_output
from cholera_demo import (load_records, cluster_locations, summary,
                          plot_locations, geolibre_map, EARTH_RADIUS_M)
print("Tools ready. No model has been fitted yet.")
'''),
('markdown', '''## 1. Map the evidence

**Say:** “These dots show where deaths were recorded. What do you notice?” One dot represents a location, not a person. These files contain 250 locations, 489 recorded deaths and eight pumps; those are not claims about the complete outbreak. The location map deliberately has no street basemap and does not yet show pumps.'''),
('code', '''
deaths, pumps = load_records()
print(f"{len(deaths)} locations | {int(deaths.DEATHS.sum())} recorded deaths | {len(pumps)} pumps")
display(deaths.head())
baseline_figure = plot_locations(deaths)
plt.show()
'''),
('markdown', '''## 2. Add one machine-learning step

**Say:** “Now let a model group nearby locations. We have not told it where the pumps are.”

DBSCAN is unsupervised learning: no correct-group labels are supplied. A core neighborhood needs at least **five locations, including itself**, within the chosen distance. Connected neighborhoods can form a group much wider than that distance. Sparse observations may be unassigned (`-1`); this does not mean they are errors or unimportant.

The inputs are coordinates only. `DEATHS` is **not** a training weight. A building with one recorded death and a building with several each contribute one location. We are exploring recorded-location density, **not population-adjusted risk**. The pump table is not passed to the model.'''),
('code', '''
radius_m = 50  # Chosen teaching setting, not an estimated disease-transmission distance.
coordinates_radians = np.radians(deaths[["LAT", "LON"]].to_numpy())
labels = DBSCAN(eps=radius_m / EARTH_RADIUS_M, min_samples=5,
                metric="haversine", algorithm="brute").fit_predict(coordinates_radians)
display(summary(deaths, labels))  # DEATHS is summed only after fitting.
group_figure = plot_locations(deaths, labels, radius_m=radius_m)
plt.show()
'''),
('markdown', '''## 3. Reveal the pumps, then ask a better question

**Say:** “Which places would you investigate, and what other evidence would you need?” This cell reuses the existing labels; it does not refit or rank pumps. P1 is the source table's Broadwick Street record, associated with the historical Broad Street setting. Source names are preserved rather than supplied to the model as an answer.'''),
('code', '''
reveal_figure = plot_locations(deaths, labels, pumps=pumps, radius_m=radius_m)
plt.show()
display(pumps.assign(map_label=[f"P{i}" for i in range(1, len(pumps)+1)])[["map_label", "Street"]])
'''),
('markdown', '''## 4. Change one setting and watch the result

Try **50 → 25 → 100 meters**. The gray points are unassigned at that setting. Colors and group numbers are arbitrary identifiers, not severity categories or stable identities across settings. A model that puts almost everything into one group may be a poor investigation aid.

This slider runs **real DBSCAN fits in Python**. Unlike the Book's saved-results presentation, it recalculates when you change the distance. The checkbox only changes whether pumps appear.'''),
('code', '''
radius_control = widgets.SelectionSlider(options=[25, 50, 100], value=50,
    description="Meters:", continuous_update=False)
pump_control = widgets.Checkbox(value=False, description="Reveal pumps (context only)")
live_output = widgets.Output()
cached_radius = None
current_labels = None
def redraw(change=None):
    global cached_radius, current_labels
    if cached_radius != radius_control.value:
        current_labels = cluster_locations(deaths, radius_control.value)
        cached_radius = radius_control.value
    with live_output:
        clear_output(wait=True)
        groups = len(set(current_labels) - {-1})
        unassigned = int((current_labels == -1).sum())
        print(f"{radius_control.value} m | {groups} group(s) | {unassigned} unassigned locations")
        figure = plot_locations(deaths, current_labels,
            pumps=pumps if pump_control.value else None, radius_m=radius_control.value)
        display(figure)
        plt.close(figure)
radius_control.observe(redraw, names="value")
pump_control.observe(redraw, names="value")
display(widgets.VBox([radius_control, pump_control, live_output]))
redraw()
'''),
('markdown', '''## 5. Explore the same result in GeoLibre (optional)

**Say:** “GeoLibre helps us explore the result; the clustering was performed by Python.” Set `SHOW_GEOLIBRE=True` and run the next cell when internet access is available. It uses the current distance and pump-checkbox settings. **Rerun this cell after changing those controls**; this separate map is not automatically synchronized.

The hosted GeoLibre viewer and its basemap use the network and receive this public historical layer. The optional package installation can take time; rehearse beforehand. A local `.geolibre.json` file is not published until you download/share it. You can also [open the bundled 50-meter project with pumps in full GeoLibre](https://web.geolibre.app/?url=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-GeoLibre-GeoAI%2Flite%2Ffiles%2Fdata%2Fcholera-demo.geolibre.json). That link is a fixed saved project, not your current slider state.'''),
('code', '''
SHOW_GEOLIBRE = False  # Optional hosted map; the analytical lesson above needs no map service.
cholera_map = None
if SHOW_GEOLIBRE:
    if sys.platform == "emscripten":
        import micropip
        await micropip.install(["geolibre==3.0.0", "anywidget"])
    map_labels = cluster_locations(deaths, radius_control.value)
    cholera_map = geolibre_map(deaths, pumps, map_labels,
        radius_m=radius_control.value, reveal_pumps=pump_control.value)
    display(cholera_map)
    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)
    (export_dir / "cholera.geolibre.json").write_text(
        json.dumps(cholera_map.to_project(), indent=2, allow_nan=False), encoding="utf-8")
    print("Map recipe saved locally. Keep the data credits and license when sharing.")
else:
    print("Optional GeoLibre viewer not opened. Set SHOW_GEOLIBRE=True to explore it.")
'''),
('markdown', '''## Close with the evidence boundary

**Mapping displays observations. Spatial statistics summarize them. GeoAI can fit spatial patterns. People investigate their meaning.**

GeoAI is an application of AI, not its opposite. This ordinary machine-learning algorithm becomes geographic through its coordinate inputs, meter-based neighborhoods and spatial interpretation. Neither a colored map nor the original case study's death-weighted center is, by itself, machine learning. This lesson does not use the separate `geoai-py` deep-learning package.

**Do not conclude:** a cluster identifies a contaminated pump, an unassigned location is safe, or removing a marker simulates an intervention. There are no population denominators, individual water-consumption observations, control households, temporal records or causal labels in these CSVs. We compute no disease rates, statistical significance, forecasts or intervention effects. Building density, omitted observations, geocoding and chosen parameters can affect the pattern. Choosing settings to obtain a desired historical answer would be misleading.

John Snow used interviews and other investigative evidence, not machine learning. Ask what fieldwork would test a proposed explanation. This is a modern retrospective teaching exercise, not a reconstruction of his reasoning or an operational outbreak detector.

## Sources and attribution

- **Data and teaching inspiration:** PHI-Case-Studies contributors, [Jupyterlite-1854-Cholera-Basic, revision 476f6dd](https://github.com/PHI-Case-Studies/Jupyterlite-1854-Cholera-Basic/tree/476f6dd5a8430e6eb823e79614fda1d7e12a78fb). The unchanged CSVs, upstream GPL-3.0 license and checksum provenance are bundled in `data/cholera/`. Original digitization and completeness are not independently verified. This is a new extension; no upstream notebook code, images or videos were copied.
- **Method:** [scikit-learn DBSCAN documentation](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html). Haversine uses latitude/longitude in radians; GeoJSON instead uses longitude/latitude in degrees. This distinction is why we cannot feed raw degree coordinates to a meter-distance model.
- **Historical interpretation:** CDC (2004), [150th Anniversary of John Snow and the Pump Handle](https://www.cdc.gov/Mmwr/preview/mmwrhtml/mm5334a1.htm). Interviews and water-use evidence extended beyond a spatial pattern.
- **GeoLibre:** Qiusheng Wu and contributors; [official citation](https://geolibre.app/citation/), [Zenodo DOI 10.5281/zenodo.20785400](https://doi.org/10.5281/zenodo.20785400). The point maps without streets are newly computed analytical views, not screenshots of Snow's original map. Preserve any basemap credits in the hosted viewer.

Sources reviewed 11 October 2026. Next: compare this example with [What is GeoAI?](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/geoai/primer.html) and [outbreak-response applications](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/geoai/outbreaks.html).'''),
]


def build_notebook(check):
    target = NOTEBOOKS / (STEM+'.ipynb')
    previous = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
    old = {cell.get('id'): cell for cell in previous.get('cells', [])}
    cells = []
    for index, (kind, content) in enumerate(AUTHORED):
        source = textwrap.dedent(content).strip()+'\n'
        identifier = f'cholera-21-{index:02d}'
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
            'cholera_lesson': {'historical_data': True, 'offline_data': True, 'synthetic': False}}}
    notebook = transform(notebook, '21', target.name)
    write_or_check(target, json.dumps(notebook, ensure_ascii=False, indent=1)+'\n', check)


def map_svg(deaths, pumps, labels=None, radius_m=50, reveal=False):
    heading = 'Map the recorded locations' if labels is None else ('Reveal the pumps' if reveal else 'Find geographic groups')
    title = f'{heading}'+('' if labels is None else f' — {radius_m} m neighborhoods')
    body = rect(0, 0, 1200, 830, '#f8fafc', radius=0)
    body += text(30, 48, title, 31, '#14283f', 700)
    body += text(30, 87, 'Historical teaching data • one dot = one recorded location • not a disease-risk map', 22, '#45576c')
    body += rect(30, 115, 700, 620, 'white', '#cddbe9')
    def screen(x, y):
        return 108 + (float(x)+330)*.8, 144 + (350-float(y))*.8
    for x in range(-300, 351, 100):
        px, _ = screen(x, 0)
        body += path(f'M{px:.2f} 144 V708', '#e4e9ef', 1)
    for y in range(-300, 351, 100):
        _, py = screen(0, y)
        body += path(f'M108 {py:.2f} H652', '#e4e9ef', 1)
    x, y = local_xy(deaths)
    for index, (xi, yi) in enumerate(zip(x, y)):
        px, py = screen(xi, yi)
        color = '#374151' if labels is None else color_for(int(labels[index]))
        body += f'<circle cx="{px:.2f}" cy="{py:.2f}" r="4" fill="{color}" stroke="white" stroke-width=".4"/>'
    if reveal:
        px, py = local_xy(pumps)
        for index, (xi, yi) in enumerate(zip(px, py), 1):
            sx, sy = screen(xi, yi)
            body += path(f'M{sx:.2f} {sy-8:.2f} L{sx+8:.2f} {sy:.2f} L{sx:.2f} {sy+8:.2f} L{sx-8:.2f} {sy:.2f} Z', 'white', 1, '#b45309')
            body += text(sx+11, sy-8, f'P{index}', 18, '#92400e', 700)
    body += path('M65 180 V140 M59 148 L65 140 L71 148', '#45576c', 2)
    body += text(55, 130, 'N', 17, '#45576c', 700)
    body += path('M70 690 H150 M70 685 V695 M150 685 V695', '#45576c', 3)
    body += text(70, 715, '100 m', 17, '#45576c')
    body += text(765, 155, 'What is being shown?', 26, '#14283f', 700)
    if labels is None:
        lines = [('250', 'recorded locations'), ('489', 'recorded deaths'), ('8', 'pumps, not shown yet')]
        for index, (count, label) in enumerate(lines):
            body += text(765, 218+index*85, count, 35, '#2459b8', 700)
            body += text(765, 249+index*85, label, 22, '#45576c')
        body += text(765, 530, 'No model has been fitted in this view.', 24, width=28)
    else:
        counts = summary(deaths, labels)
        groups = sum(counts.group != -1)
        body += text(765, 195, f'{groups} group(s) • minimum 5 locations', 21, '#45576c')
        for index, row in enumerate(counts.itertuples()):
            label = 'Unassigned' if row.group == -1 else f'Group {row.group}'
            body += rect(765, 217+index*28, 16, 16, color_for(row.group), radius=2)
            body += text(790, 231+index*28, f'{label}: {row.locations} locations', 19)
        body += text(765, 641, 'Pumps were not model inputs.', 22, '#92400e', 700)
        body += text(765, 676, 'Colors are groups, not severity.', 22, '#45576c')
    body += text(30, 775, 'Geographic point map, no street basemap. Display uses approximate local meters; fitting uses haversine.', 19, '#45576c')
    body += text(30, 811, 'Data: PHI-Case-Studies contributors. Source revision and GPL-3.0 notice: data/cholera/.', 18, '#45576c')
    desc = title+'. 250 recorded locations represent 489 deaths in this teaching dataset. '
    desc += ('Eight pump locations are shown as diamonds P1 to P8. ' if reveal else 'Pump locations are hidden. ')
    desc += 'No population-adjusted risk, causal inference or forecast is shown.'
    return svg(body, title, desc, 1200, 830)


def snapshot_data(deaths):
    scenarios = {}
    for radius in RADII:
        labels = cluster_locations(deaths, radius)
        scenarios[str(radius)] = {'labels': list(map(int, labels)),
            'groups': len(set(map(int, labels)) - {-1}), 'unassigned': int((labels == -1).sum()),
            'summary': summary(deaths, labels).to_dict(orient='records')}
    return {'source_revision': '476f6dd5a8430e6eb823e79614fda1d7e12a78fb',
            'method': 'sklearn DBSCAN, haversine, min_samples=5, unweighted locations',
            'location_ids': list(map(int, deaths.FID)), 'scenarios': scenarios}


def presentation_html(snapshots):
    template = (ROOT/'scripts/cholera_presentation.html').read_text(encoding='utf-8')
    return template.replace('/* SNAPSHOT_DATA */', json.dumps(snapshots, ensure_ascii=True, separators=(',', ':')))


def public_project(deaths, pumps):
    project = geolibre_map(deaths, pumps, cluster_locations(deaths, 50)).to_project()
    project['name'] = 'Historical cholera: 50 m location groups, not disease risk'
    for index, layer in enumerate(project['layers']):
        layer['id'] = f'cholera-layer-{index}'
    project['metadata'] = {'source': 'PHI-Case-Studies/Jupyterlite-1854-Cholera-Basic',
        'revision': '476f6dd5a8430e6eb823e79614fda1d7e12a78fb',
        'license_notice': 'GPL-3.0; retain data/cholera/LICENSE and provenance',
        'model': 'DBSCAN; haversine; 50 m neighbors; min_samples=5; locations unweighted',
        'limits': 'Exploratory recorded-location groups, not causal evidence or disease-risk estimates'}
    return project


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    deaths, pumps = load_records()
    build_notebook(args.check)
    write_or_check(ASSETS/'map.svg', map_svg(deaths, pumps), args.check)
    for radius in RADII:
        labels = cluster_locations(deaths, radius)
        for reveal, name in ((False, 'groups'), (True, 'pumps')):
            write_or_check(ASSETS/f'{name}-{radius}.svg', map_svg(deaths, pumps, labels, radius, reveal), args.check)
    snapshots = snapshot_data(deaths)
    write_or_check(ASSETS/'results.json', json.dumps(snapshots, indent=2)+'\n', args.check)
    write_or_check(ASSETS/'presentation.html', presentation_html(snapshots), args.check)
    write_or_check(NOTEBOOKS/'data/cholera-demo.geolibre.json', json.dumps(public_project(deaths, pumps), indent=2)+'\n', args.check)
    print('Verified' if args.check else 'Built', 'cholera notebook, seven analytical maps, saved-results presentation and GeoLibre project')


if __name__ == '__main__':
    main()
