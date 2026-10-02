# JupyterLite + GeoLibre + GeoAI

Browser-native geospatial notebooks that combine **[GeoLibre](https://geolibre.app/)**, open geospatial data, and **GeoAI workflows** in **JupyterLite**.

[![Deploy Jupyter Book and JupyterLite](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/actions/workflows/pages.yml/badge.svg)](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/actions/workflows/pages.yml)
[![GeoLibre](https://img.shields.io/badge/GeoLibre-3.0-blue)](https://geolibre.app/)
[![GeoAI](https://img.shields.io/badge/GeoAI-opengeoai.org-green)](https://opengeoai.org/)

**GeoLibre citation:** Wu, Q. (2026). *GeoLibre: A lightweight, cloud-native GIS platform for visualizing, exploring, and analyzing geospatial data.* Zenodo. [https://doi.org/10.5281/zenodo.20785400](https://doi.org/10.5281/zenodo.20785400)

**GeoAI citation:** Wu, Q. (2026). *GeoAI: A Python package for integrating artificial intelligence with geospatial data analysis and visualization.* *Journal of Open Source Software*, 11(118), 9605. [https://doi.org/10.21105/joss.09605](https://doi.org/10.21105/joss.09605).

## Live sites

- **Jupyter Book:** <https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/>  
- **JupyterLite Lab:** <https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html>

## Launch the notebooks

| Notebook | What it demonstrates | Live |
|---|---|---|
| 00 — GeoLibre quickstart | Browser-safe GeoLibre embed, GeoJSON, COG raster, browser GIS | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=00_geolibre_quickstart.ipynb) |
| 01 — WorldPop + H3 | WorldPop population streamed as H3/PMTiles + H3 geometry | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=01_worldpop_h3.ipynb) |
| 02 — Census + GeoAI | U.S. Census county geometry, derived density features, K-Means clustering | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=02_census_geoai_counties.ipynb) |
| 03 — Earth observation GeoAI | Major TOM layers + browser-safe NASA GIBS K-Means workflow | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=03_earth_observation_geoai.ipynb) |
| 04 — CHIRPS climate | CHIRPS v3 daily precipitation COG + GeoLibre cloud raster visualization | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=04_chirps_climate.ipynb) |
| 05 — H3 earthquake GeoAI | Live USGS earthquakes, H3 aggregation, Isolation Forest anomaly scoring | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=05_h3_earthquake_geoai.ipynb) |
| 06 — GeoAI compatibility | JupyterLite/GeoLibre compatibility boundaries and full-CPython/GPU handoff | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=06_geoai_compatibility.ipynb) |
| 07 — STAC Browser catalogs | Discover UN Biodiversity Lab, Copernicus, USGS, and WorldPop STAC APIs | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=07_stac_browser_catalogs.ipynb) |
| 08 — STAC + GeoAI footprints | Search public STAC APIs, cluster metadata, and map item footprints in GeoLibre | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=08_stac_geoai_footprints.ipynb) |
| 09 — GeoLibre demo recommender | Cluster official demo descriptions and rank projects for a natural-language workflow | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=09_geolibre_demo_recommender.ipynb) |
| 10 — Sister Cities graph GeoAI | Extract a live GeoLibre project, model its city network, and map unusual graph profiles | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=10_sister_cities_graph_geoai.ipynb) |
| 11 — Wildfire + STAC triage | Score NIFC fire perimeters, search Sentinel-2 STAC, and stream a ranked COG to GeoLibre | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=11_wildfire_stac_triage.ipynb) |

## New Astra learning labs

| Notebook | Visual investigation | Live |
|---|---|---|
| 12 — Astra spatial copilot | Structured plans, map/scatter views, threshold sensitivity | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=12_astra_spatial_copilot.ipynb) |
| 13 — Astra vision + change | Before/after imagery, masks, confusion matrix, image-grounded interpretation | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=13_astra_vision_change.ipynb) |
| 14 — Astra + 3D terrain | Contours, slopes, profiles, rotatable surface, GeoLibre elevation extrusions | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=14_astra_terrain_3d.ipynb) |
| 15 — Astra accessibility tools | Network graphs, bridge closure, travel-time sensitivity, function calling | [Launch](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=15_astra_network_accessibility.ipynb) |

Labs 00–08 and 12–15 include a concept map and a visual investigation with a **predict → run → compare → explain** exercise. Maps answer *where*, charts explain *how much*, network graphs expose *connections*, and 3D/profile views show *shape*. Bundled SVG concept diagrams remain visible without a kernel or diagram CDN.

Start with **00 → 01 → 02** for spatial representations, **03 → 13** for imagery, **14** for terrain, or **12 → 15** for Astra-assisted analysis. Labs 12–15 have saved static figure outputs and deterministic synthetic datasets. Their analytical exercises do not depend on changing data APIs. Synthetic values are explicitly labeled; they are not measurements of the displayed real-world locations. GeoLibre's hosted viewer, basemaps, initial package installation, and interactive Plotly scripts still need internet access. Native map widgets appear when the notebook runs.

## Using GPT-6 Astra

The new labs use Astra's documented image inputs, structured outputs, and function calling to propose bounded operations and interpret supplied evidence. They do not claim a dedicated GIS engine or geospatial accuracy benchmark. Python computes the measurements, GeoLibre displays the geometry, and a full GeoAI runtime can supply heavier inference. See the [Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra) and [Responses function-calling documentation](https://developers.openai.com/api/docs/guides/function-calling).

The default **Run All makes no model calls**. Offline plans/tool arguments are hand-authored teaching examples, not claimed model outputs. Each new lab exports a Responses API request to `exports/`. To try Astra:

1. Download a request JSON from JupyterLite. For lab 15 also download `accessibility_evidence.json`.
2. Set `OPENAI_API_KEY` in a full CPython terminal outside JupyterLite. Never embed the key in browser code, a notebook, or a deployed static site.
3. Preview or send the request from the repo root:

   ```bash
   python scripts/run_astra.py spatial_plan_request.json
   python scripts/run_astra.py spatial_plan_request.json --send --output astra_response.json
   python scripts/run_astra.py accessibility_request.json --evidence accessibility_evidence.json --send --output astra_response.json
   ```

4. Upload the response JSON into the notebook folder, set `RESPONSE_PATH`, and rerun the import cell. Review the answer against the computed evidence.

Sending uses your API project's access and billing. The runner reports token usage, rejects incomplete/refused responses, and bounds the accessibility tool loop. No API SDK, API key, or server is required for the default teaching run. Live API access is separate from access to Astra in a chat application.

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
python scripts/build_lite.py
jupyter-book build book
cp -a book/_build/html/. site/
touch site/.nojekyll
python -m http.server -d site 8000
```

Open <http://localhost:8000> for the book or <http://localhost:8000/lite/lab/index.html> for JupyterLite.

`scripts/build_lite.py` explicitly includes the Pyodide kernel, Jupyter widget manager and anywidget extensions, including when Python packages were installed with `pip --user`. It verifies those extensions in the built site. Saved figures are generated in CPython; running the notebooks in JupyterLite creates fresh browser results.

## Verify the learning labs

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
python scripts/validate_notebooks.py --execute
```

Validation checks all notebook schemas and Python syntax, then executes labs 12–15 in isolated temporary directories without data-service or model calls. Use `--execute --save-outputs` to refresh their saved figures. Older notebooks still query their documented public data services; CORS, availability and changing feeds must be checked in the browser. The book build intentionally does not execute those live queries.

## Citations, attribution, and licenses

Every notebook contains a **Data & software citations** section. The table below makes the repository-level attributions self-contained; **[DATA_SOURCES.md](DATA_SOURCES.md)** remains the detailed provenance register with fixed asset URLs, roles, caveats, and product-specific notes.

When publishing results derived from these notebooks, cite the original data producer—not only this repository, GeoLibre, a catalog, or a hosting mirror. A catalog or mirror does not replace the source product's terms. Recheck the linked collection metadata before redistribution because upstream terms and versions can change.

### Core software

- **GeoLibre:** Wu, Q. (2026). *GeoLibre: A lightweight, cloud-native GIS platform for visualizing, exploring, and analyzing geospatial data.* Zenodo. https://doi.org/10.5281/zenodo.20785400. Source: https://github.com/opengeos/GeoLibre. License: MIT.
- **GeoAI:** Wu, Q. (2026). “GeoAI: A Python package for integrating artificial intelligence with geospatial data analysis and visualization.” *Journal of Open Source Software*, 11(118), 9605. https://doi.org/10.21105/joss.09605. Source: https://github.com/opengeos/geoai. License: MIT.
- **JupyterLite / Pyodide:** https://jupyterlite.readthedocs.io/ and https://pyodide.org/. Retain the licenses and notices of the individual packages loaded into Pyodide.
- **Uber H3:** https://h3geo.org/ and https://github.com/uber/h3-py. License: Apache-2.0.
- **scikit-learn:** Pedregosa et al. (2011), “Scikit-learn: Machine Learning in Python,” *Journal of Machine Learning Research*, 12, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html. License: BSD-3-Clause.
- **NetworkX:** Hagberg, A., Swart, P., & Schult, D. (2008). *Exploring network structure, dynamics, and function using NetworkX.* https://networkx.org/. License: BSD-3-Clause.

### Data and service attribution by lab

| Labs | Data/service | Required attribution and terms |
|---|---|---|
| 00 | GeoLibre sample places and public DEM | GeoLibre sample: `https://assets.geolibre.app/data/places.geojson`. DEM hosted in the `giswqs/opengeos` collection on [Source Cooperative](https://source.coop/giswqs/opengeos). Verify the asset-level terms before redistribution. |
| 01 | WorldPop 2020 population counts | Bondarenko, M., Kerr, D., Sorichetta, A., & Tatem, A.J. (2020). *Census/projection-disaggregated gridded population datasets for 189 countries in 2020 using BSGM outputs.* WorldPop, University of Southampton. https://doi.org/10.5258/SOTON/WP00684. The cited product family is CC BY 4.0; verify substituted layers independently. |
| 02 | U.S. Census Bureau Census 2020 / TIGERweb | Source: U.S. Census Bureau, [TIGERweb State and County service](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer). U.S. Census Bureau data are used with source identification; consult Census terms for a substituted service or product. |
| 03 | Major TOM, Copernicus Sentinel-2, Copernicus DEM GLO-30, ESA WorldCover | [Major TOM Core](https://source.coop/major-tom/core) supplies aligned cloud assets. Attribute the underlying Copernicus Sentinel-2, Copernicus DEM, and ESA WorldCover products and follow each source's terms listed by the collection. Major TOM/Source Cooperative hosting does not replace those terms. |
| 03 | NASA GIBS imagery | Imagery served by [NASA Global Imagery Browse Services](https://www.earthdata.nasa.gov/data/tools/gibs). Attribute NASA and the specific instrument/product shown by the notebook; consult the product metadata for science use. |
| 04 | CHIRPS v3 daily precipitation | Climate Hazards Center CHIRPS3 Data Repository (2025), https://doi.org/10.15780/G2JQ0P. WFP/VAM [CHIRPS v3 RNL daily mirror](https://source.coop/wfp/chirps-rnl-daily), CC BY 4.0. **CHIRPS is produced by the Climate Hazards Center at UC Santa Barbara, not NOAA.** |
| 05 | USGS Earthquake Hazards Program | Source: U.S. Geological Survey, [Earthquake Hazards Program GeoJSON feeds](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php). Record the retrieval time because the monthly feed is live. Do not interpret the anomaly model as earthquake prediction or official hazard guidance. |
| 06 | National Land Cover Database | Source: U.S. Geological Survey, [Annual National Land Cover Database](https://www.usgs.gov/centers/eros/science/annual-national-land-cover-database). The example COG is hosted on Source Cooperative; attribute USGS and the specific NLCD product/year. |
| 07–08 | STAC specification and public catalogs | Cite the [STAC specification](https://stacspec.org/) and the data collection actually used. Catalogs demonstrated: [UN Biodiversity Lab](https://stac.unbiodiversitylab.org/?.language=en), [Copernicus Data Space](https://browser.stac.dataspace.copernicus.eu/), [USGS LandsatLook](https://landsatlook.usgs.gov/stac-browser/?.language=en), and [WorldPop](https://stac.worldpop.org/?.language=en). STAC metadata discovery does not grant rights to its assets; inspect each Item/Collection license. |
| 09 | GeoLibre Official Demos descriptions | Source: [GeoLibre Gallery](https://geolibre.app/gallery/) and [Official Demos collection](https://share.geolibre.app/giswqs/collections/official-demos), reviewed 2026-09-29. The notebook models a compact manifest of titles, tags, and descriptions. Each linked project identifies its own underlying sources and terms, which must be checked before using its data. |
| 10 | Sister Cities demo / Wikidata | Source project: [Sister Cities of Major World Cities](https://share.geolibre.app/giswqs/sister-cities-of-major-world-cities). Its structured relationship data are from Wikidata's “twinned administrative body” property. [Wikidata structured data are CC0](https://www.wikidata.org/wiki/Wikidata:Data_access). Clearly identify Wikidata and the GeoLibre transformation when publishing derived graph results. |
| 11 | NIFC WFIGS fire perimeters | Source project: [US Wildfire Perimeters 2025](https://share.geolibre.app/giswqs/us-wildfire-perimeters-2025), which identifies [NIFC Wildland Fire Interagency Geospatial Services (WFIGS) Interagency Perimeters](https://data-nifc.opendata.arcgis.com/pages/d6ef1367fadc4405b5f09c98e52ed972) / National Interagency Fire Center as its source. Preserve that source identification. This educational snapshot is not operational incident information. |
| 11 | Element 84 Earth Search / Copernicus Sentinel-2 | [Earth Search](https://github.com/Element84/earth-search) provides the `sentinel-2-c1-l2a` STAC Collection and public COG assets. Attribute the Copernicus Sentinel-2 mission and follow the current Collection metadata and [Copernicus data terms](https://dataspace.copernicus.eu/terms-and-conditions). Attribute Element 84 for the Earth Search service and derived COG distribution. |

### Shared basemap and hosting attribution

- GeoLibre maps may display OpenStreetMap-derived basemaps. Preserve on-map attribution: **© OpenStreetMap contributors**, https://www.openstreetmap.org/copyright.
- [Source Cooperative](https://source.coop/) is a cloud-native hosting platform used by several examples. Cite the original data producer and product license in addition to identifying the mirror.
- GeoLibre `.geolibre.json` projects can combine sources under different terms. Inspect each project's metadata, attribution, and linked provider before reuse.

## Contributing

Keep new examples browser-first:

1. Prefer COG, PMTiles, GeoParquet, STAC, GeoJSON, or small downloadable assets.
2. Verify CORS and HTTP range-request support.
3. Use `geolibre_lite.LiteMap` inside JupyterLite; reserve upstream `geolibre.Map` for full Python/Jupyter runtimes.
4. Avoid credentials when an open source exists; if credentials are unavoidable, prompt at runtime and never commit them.
5. Add an entry to `DATA_SOURCES.md` and a citation cell in the notebook.
6. Test both the rendered Jupyter Book page and the live JupyterLite notebook.
