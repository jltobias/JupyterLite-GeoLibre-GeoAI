# JupyterLite + GeoLibre + GeoAI

Browser-native geospatial notebooks that combine **[GeoLibre](https://geolibre.app/)**, open geospatial data, and **GeoAI workflows** in **JupyterLite**.

[![Deploy Jupyter Book and JupyterLite](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/actions/workflows/pages.yml/badge.svg)](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/actions/workflows/pages.yml)
[![GeoLibre](https://img.shields.io/badge/GeoLibre-3.0-blue)](https://geolibre.app/)
[![GeoAI](https://img.shields.io/badge/GeoAI-opengeoai.org-green)](https://opengeoai.org/)

## Live sites

- **Jupyter Book:** <https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/>  
- **JupyterLite Lab:** <https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html>

> The live links below use versioned `v2_*.ipynb` paths so older browser-saved JupyterLite copies cannot shadow corrected server notebooks.

## Launch the notebooks

| Notebook | What it demonstrates | Live |
|---|---|---|
| 00 — GeoLibre quickstart | Browser-safe GeoLibre embed, GeoJSON, COG raster, browser GIS | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_00_geolibre_quickstart.ipynb) |
| 01 — WorldPop + H3 | WorldPop population streamed as H3/PMTiles + H3 geometry | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_01_worldpop_h3.ipynb) |
| 02 — Census + GeoAI | U.S. Census county geometry, derived density features, K-Means clustering | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_02_census_geoai_counties.ipynb) |
| 03 — Earth observation GeoAI | Major TOM Sentinel-2 + Copernicus DEM + ESA WorldCover, browser K-Means segmentation | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_03_earth_observation_geoai.ipynb) |
| 04 — CHIRPS climate | CHIRPS v3 daily precipitation COG + GeoLibre cloud raster visualization | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_04_chirps_climate.ipynb) |
| 05 — H3 earthquake GeoAI | Live USGS earthquakes, H3 aggregation, Isolation Forest anomaly scoring | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_05_h3_earthquake_geoai.ipynb) |
| 06 — GeoAI compatibility | JupyterLite/GeoLibre compatibility boundaries and full-CPython/GPU handoff | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_06_geoai_compatibility.ipynb) |

## Why this architecture?

### GeoLibre in JupyterLite

The upstream `geolibre.Map` widget is designed for normal Jupyter kernels. It starts a loopback HTTP server to serve GeoLibre's bundled application. A standalone JupyterLite kernel runs inside Pyodide/WebAssembly and cannot bind a TCP socket, so directly constructing `geolibre.Map()` raises an `OSError` in the browser.

The live notebooks therefore install `geolibre==3.0.0` but use **`book/notebooks/geolibre_lite.py`**. `LiteMap` is a small `anywidget` adapter that:

1. uses GeoLibre's own Python project and layer builders;
2. preserves GeoLibre project/layer schemas for GeoJSON, COG, PMTiles and graduated symbology;
3. displays the project with GeoLibre's upstream hosted viewer (`https://web.geolibre.app/?embed=1`);
4. uses the same `postMessage` project-loading protocol as GeoLibre's standalone HTML export; and
5. never opens a localhost server or OS socket.

In regular JupyterLab, VS Code, JupyterHub, Binder, or another full CPython environment where the kernel-side server/proxy is available, use upstream `geolibre.Map` directly.

### GeoAI in JupyterLite

The current `geoai-py` package includes PyTorch, TorchGeo, Transformers, rasterio, OpenCV, and other dependencies. Pyodide provides an unusually capable browser geospatial/scientific stack—including GeoPandas, rasterio, H3, scikit-learn, and scikit-image—but not the full PyTorch/TorchGeo stack. Therefore these examples implement **GeoAI-style data preparation, feature engineering, unsupervised learning, anomaly detection, and raster classification directly in JupyterLite**, then provide a clear continuation path to the full GeoAI package for GPU/deep-learning workflows.

## Build locally

```bash
python -m pip install -r requirements.txt
rm -rf site book/_build
jupyter lite build --contents book/notebooks --output-dir site/lite
jupyter-book build book
cp -a book/_build/html/. site/
touch site/.nojekyll
python -m http.server -d site 8000
```

Open <http://localhost:8000> for the book or <http://localhost:8000/lite/lab/index.html> for JupyterLite.

## Data citations and licenses

Every notebook contains a **Data & software citations** section. A consolidated, auditable source register is in **[DATA_SOURCES.md](DATA_SOURCES.md)**. The examples intentionally favor public, cloud-native, browser-readable sources.

Notable sources include WorldPop; U.S. Census Bureau TIGERweb; Copernicus Sentinel-2 and DEM through Major TOM; ESA WorldCover; CHIRPS v3 from the Climate Hazards Center/WFP mirror on Source Cooperative; USGS earthquake feeds; Uber H3; Source Cooperative; GeoLibre; and GeoAI.

### Important source note

**CHIRPS is not a NOAA product.** It is produced by the Climate Hazards Center at UC Santa Barbara. NOAA datasets such as HRRR are excellent candidates for additional notebooks, but they are cited separately rather than being conflated with CHIRPS.

## Contributing

Keep new examples browser-first:

1. Prefer COG, PMTiles, GeoParquet, STAC, GeoJSON, or small downloadable assets.
2. Verify CORS and HTTP range-request support.
3. Use `geolibre_lite.LiteMap` inside JupyterLite; reserve upstream `geolibre.Map` for full Python/Jupyter runtimes.
4. Avoid credentials when an open source exists; if credentials are unavoidable, prompt at runtime and never commit them.
5. Add an entry to `DATA_SOURCES.md` and a citation cell in the notebook.
6. Test both the rendered Jupyter Book page and the live JupyterLite notebook.
