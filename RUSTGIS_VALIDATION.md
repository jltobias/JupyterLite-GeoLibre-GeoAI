# RustGIS browser bridge validation — 2026-10-30

Scope: the RustGIS introduction, notebook 22, its reproducible synthetic GeoJSON,
seven code guides, original runtime diagram, infographic, cartoon and captioned
video. The Book, README, notebook atlas, visual library and references include the
same lesson. Existing notebooks 00–21 are unchanged.

Verified locally:

- 75 unit tests pass, including geographic coordinate-order/distance semantics,
  distance sensitivity, input validation, export round trips and launch URLs.
- All 23 notebook schemas/code cells validate. Notebook 22 executes in CPython;
  its saved analytical plots are included for Book readers.
- All seven default cells execute in real Pyodide v314.0.4, including exports.
  Results match the committed snapshot: at 350 m, two groups of nine points and
  two unassigned; at 150 m, all 20 points unassigned. No native `rustgis` import.
- Strict Jupyter Book build and JupyterLite build pass. The alignment guard
  compares all 23 notebook downloads and 228 Lite content files with sources.
- New chapter/notebook layouts pass at 1280 and 390 pixels. The runtime SVG and
  all six generated lesson graphics fit their bounds. The 32-second MP4 plays
  with four caption cues. The updated notebook-atlas visual also passes checks.
- RustGIS Web and the companion Book, Lab, 2D map, extruded map and scene return
  HTTP 200. Reachability is not an interactive rendering test.

Not verified here: the external RustGIS import/globe interface (the connected
browser host was unavailable), the optional hosted GeoLibre comparison view, or
the separate native RustGIS Python recipe. These remain clearly identified
routes, not claims of an embedded RustGIS kernel or automatic app synchronization.
The published links open the fixed 350 m example; notebook edits require export
and manual import. All points are invented, and no health-risk claim is made.

Reproduce: `python -m unittest discover -s tests -q`,
`python scripts/build_rustgis_lesson.py --check`, and, after building/serving
`site/`, `python scripts/check_rustgis_browser.py --base-url http://127.0.0.1:8765 --pyodide`
and `python scripts/check_learning_browser.py --base-url http://127.0.0.1:8765 --keys 22`.
The deployment workflow also runs these runtime and alignment checks.
