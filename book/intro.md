# GeoLibre + GeoAI in JupyterLite

This book is a set of **live, browser-native geospatial labs**. Each chapter can be read as documentation or launched into a writable JupyterLite session with no local Python installation.

**Launch the lab:** [https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html)

## Notebook gallery

| Lab | Focus | Launch |
|---|---|---|
| GeoLibre quickstart | GeoLibre map, GeoJSON, COG | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=00_geolibre_quickstart.ipynb) |
| WorldPop + H3 | Population, PMTiles, hex indexing | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=01_worldpop_h3.ipynb) |
| Census + GeoAI | Census polygons + browser clustering | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=02_census_geoai_counties.ipynb) |
| Earth observation GeoAI | Sentinel-2, DEM, WorldCover, raster ML | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=03_earth_observation_geoai.ipynb) |
| CHIRPS climate | Daily rainfall COG | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=04_chirps_climate.ipynb) |
| H3 earthquake GeoAI | USGS feed + anomaly detection | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=05_h3_earthquake_geoai.ipynb) |
| GeoAI compatibility | Browser/full-stack boundary | [Open live](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=06_geoai_compatibility.ipynb) |

## A practical interpretation of “GeoAI in JupyterLite”

The full `geoai-py` package is designed for advanced workflows including deep-learning segmentation, detection, classification, change detection, and model training. Its dependency graph includes PyTorch and TorchGeo. JupyterLite runs CPython compiled to WebAssembly through Pyodide, so not every native/GPU dependency is available.

These labs therefore use the **browser-native subset of the GeoAI workflow**: cloud data discovery, spatial feature engineering, H3 indexing, raster processing, scikit-learn modeling, anomaly detection, and interactive mapping in GeoLibre. The final chapter shows where to hand the same data and concepts to full GeoAI on a desktop, cloud VM, Binder/Hub, or GPU notebook.

## Data ethics and reproducibility

The notebooks use public data and avoid hidden credentials. All sources, licenses, fixed example dates, mirrors, and citation guidance are collected in the repository's `DATA_SOURCES.md` and repeated in the relevant lab.
