# GeoLibre + GeoAI in JupyterLite

This book is a set of **live, browser-native geospatial labs**. Each chapter can be read as documentation or launched into a writable JupyterLite session with no local Python installation.

**Launch the lab:** [https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html)

## Notebook gallery

The live links use versioned notebook paths so previously saved browser copies cannot shadow corrected notebooks. Earth-observation lab 03 uses a `v3_` path because the earlier v2 filename may already exist in browser IndexedDB.

| Lab | Focus | Launch |
|---|---|---|
| GeoLibre quickstart | GeoLibre map, GeoJSON, COG | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_00_geolibre_quickstart.ipynb) |
| WorldPop + H3 | Population, PMTiles, hex indexing | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_01_worldpop_h3.ipynb) |
| Census + GeoAI | Census polygons + browser clustering | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_02_census_geoai_counties.ipynb) |
| Earth observation GeoAI | Major TOM layers + NASA GIBS browser ML | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v3_03_earth_observation_geoai.ipynb) |
| CHIRPS climate | Daily rainfall COG | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_04_chirps_climate.ipynb) |
| H3 earthquake GeoAI | USGS feed + anomaly detection | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_05_h3_earthquake_geoai.ipynb) |
| GeoAI compatibility | Browser/full-stack boundary | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=v2_06_geoai_compatibility.ipynb) |

## GeoLibre's JupyterLite boundary

The upstream `geolibre.Map` widget serves its bundled application from a kernel-side localhost HTTP server. That is appropriate in a normal Jupyter environment, but a Pyodide/WebAssembly kernel cannot bind the required TCP socket.

For that reason, the live labs use `geolibre_lite.LiteMap`, a small browser adapter included with the notebooks. It uses **GeoLibre's own project/layer builders** and the **GeoLibre hosted viewer's embed/postMessage protocol**, so GeoJSON, COG, PMTiles and GeoLibre symbology are still represented as GeoLibre projects without attempting to start an OS-level server.

Use upstream `geolibre.Map` directly when running the notebooks in a full CPython/Jupyter environment with a local server or supported Jupyter proxy.

## A practical interpretation of “GeoAI in JupyterLite”

The full `geoai-py` package is designed for advanced workflows including deep-learning segmentation, detection, classification, change detection, and model training. Its dependency graph includes PyTorch and TorchGeo. JupyterLite runs CPython compiled to WebAssembly through Pyodide, so not every native/GPU dependency is available.

These labs therefore use the **browser-native subset of the GeoAI workflow**: cloud data discovery, spatial feature engineering, H3 indexing, raster processing, scikit-learn modeling, anomaly detection, and interactive mapping in GeoLibre. The Earth-observation lab keeps Major TOM COGs in GeoLibre but uses NASA GIBS JPEG imagery for Python-side clustering so Pyodide does not depend on a missing GDAL ZSTD codec. The final chapter shows where to hand the same data and concepts to full GeoAI on a desktop, cloud VM, Binder/Hub, or GPU notebook.

## Data ethics and reproducibility

The notebooks use public data and avoid hidden credentials. All sources, licenses, fixed example dates, mirrors, and citation guidance are collected in the repository's `DATA_SOURCES.md` and repeated in the relevant lab.
