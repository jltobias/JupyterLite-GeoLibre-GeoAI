# Data and software source register

Original source register reviewed: **2026-09-29**. Visual learning labs and Astra references added: **2026-10-02**.

This file is the consolidated citation and provenance register for the JupyterLite/GeoLibre/GeoAI examples. Each notebook also contains a concise citation section.

## Visual learning edition (2026-10-09)

- All 18 notebooks include newly authored teaching copy, a vector infographic, a vector cartoon, a PNG preview, and a silent 32-second MP4 storyboard with WebVTT captions and an HTML transcript. Sources: `scripts/learning_content.py` and `scripts/build_learning_media.py`; outputs: `book/notebooks/assets/learning/`.
- These are original schematic illustrations of methods, not observed geographic datasets, measured hazard maps, screenshots of live results or captured model conversations. The diagrams and fictional dialogue must be read with the notebook's source-specific analytical outputs.
- No stock artwork or third-party videos are redistributed. The user-supplied Six Thinking Hats artwork remains separate with its existing attribution below. The new generic cartoon figures do not depict real people.
- Videos and posters are rendered from the same authored SVG/storyboard content. Transcripts also appear in notebook Markdown; static SVG alternatives remain available without video playback or a Python kernel.
- Runtime, code and STAC explanations refer to the [Pyodide FAQ](https://pyodide.org/en/stable/usage/faq.html), [JupyterLite content documentation](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html), [scikit-learn clustering guide](https://scikit-learn.org/stable/modules/clustering.html#k-means), and [STAC specification overview](https://stacspec.org/en/about/stac-spec/), checked 2026-10-09.

## Presentation graphics for the platform introductions (2026-10-11)

- Source: **Tobias, J. L. (2026, July 10). *JupyterLite: Geospatial Data Science and Global Health* [Presentation]**. User-supplied originals: `Jim-Tobias-Peraton-JupyterLite-Geospatial-Data-Science-and-Global-Health-7102026.pptx` and the matching `.pdf`. The 47-slide originals remain outside the repository.
- Seven original embedded PNGs are retained byte-for-byte in `book/assets/platforms/`. [Provenance manifest](book/assets/platforms/provenance.json): source-file SHA-256 hashes, slide numbers, PPTX member names, per-image hashes/dimensions, source URLs and credits. Extractor: `scripts/extract_platform_graphics.py`; offline verification: `python scripts/extract_platform_graphics.py --check`.
- **Slides 11 and 17:** JupyterLite interface and deployment documentation, JupyterLite Contributors. [Documentation](https://jupyterlite.readthedocs.io/en/stable/) and [deployment guide](https://jupyterlite.readthedocs.io/en/stable/quickstart/deploy.html). BSD 3-Clause software notice retained in `JUPYTERLITE-LICENSE.txt`; GitHub UI and the incidental screenshot advertisement retain their respective ownership and do not imply endorsement.
- **Slide 19:** ecosystem infographic supplied in the presentation. Separate illustrator/license not specified. It is not relabeled as original repository artwork or assigned a new open license. The JupyterLite chapter clarifies its packaging simplifications and conditional offline/security claims; project names/logos retain their respective credits.
- **Slides 38, 39, 41 and 42:** GeoLibre Web, notebook integration docs, Python docs and sharing gallery. **Qiusheng Wu and contributors**; [official citation](https://geolibre.app/citation/), concept DOI [10.5281/zenodo.20785400](https://doi.org/10.5281/zenodo.20785400). Copyright (c) 2026 Qiusheng Wu; MIT software notice retained in `GEOLIBRE-LICENSE.txt`. These slides' presentation-level Wu citations are repeated in the new chapter text rather than lost when extracting embedded PNGs.
- **Basemap and gallery credits:** retain OpenFreeMap, OpenMapTiles and [OpenStreetMap contributors](https://www.openstreetmap.org/copyright) visible on slide 38. Gallery projects on slide 42 include authors **spatialthoughts** and **giswqs**; their underlying sources retain their own terms. The Python screenshot shows a historical v1.10.0; the repository's Python builders remain pinned to 3.0.0 and the hosted viewer evolves independently.
- Figure captions and reading guides are in [What is JupyterLite?](book/platforms/jupyterlite.md) and [What is GeoLibre?](book/platforms/geolibre.md). None of these source graphics is an analytical output or health-program finding. Software licenses do not grant blanket rights to the full presentation, third-party imagery, logos, or data.

## Software

### GeoLibre
- Project: https://geolibre.app/
- Source: https://github.com/opengeos/GeoLibre
- Python package used in live notebooks: `geolibre==3.0.0`
- License: MIT (see upstream repository).
- Role: interactive GIS, COG/PMTiles/GeoJSON rendering, notebook map widget.

### GeoAI
- Project/docs: https://opengeoai.org/
- Source: https://github.com/opengeos/geoai
- Citation: Wu, Q. (2026). “GeoAI: A Python package for integrating artificial intelligence with geospatial data analysis and visualization.” *Journal of Open Source Software*, 11(118), 9605. https://doi.org/10.21105/joss.09605
- License: MIT.
- Role: design reference and full-stack continuation for AI workflows. The full package is not installed in JupyterLite because its current dependency graph includes PyTorch/TorchGeo/Transformers. Browser notebooks use Pyodide-provided GeoPandas, rasterio, H3, scikit-learn and scikit-image to implement compatible workflow patterns.

### Uber H3
- Project: https://h3geo.org/
- Python bindings: https://github.com/uber/h3-py
- License: Apache-2.0.
- Role: hierarchical hexagonal spatial indexing.

### JupyterLite / Pyodide
- JupyterLite: https://jupyterlite.readthedocs.io/
- Pyodide packages: https://pyodide.org/en/stable/usage/packages-in-pyodide.html
- Role: in-browser Python/WebAssembly runtime.

## Data

### Synthetic visual learning fixtures (labs 12–15 and rainfall exercise in 04)
- Origin: deterministic functions and fixed-seed arrays authored in this repository, including `book/notebooks/cognition.py` and the notebook cells.
- Fixtures: 8 × 8 invented temperature/canopy/population grid; paired 64 × 64 RGB scenes with a known change/cloud mask; analytic metric terrain; a 6 × 6 street network with two bridges; a fixed 30-day rainfall teaching series.
- These are **not observed environmental, population, satellite, road, or service-access data**. The longitude/latitude anchor only demonstrates mapping and does not describe the real location beneath the basemap.
- Cell areas and terrain derivatives are computed in local metric coordinates. The small-patch longitude/latitude conversion is a teaching approximation, not a surveyed projection or production georeferencing method.
- No downloaded imagery is transmitted to Astra by default. Optional vision requests contain PNGs generated from the synthetic arrays and their numerical evidence.
- Reproduction: run the cells in order. Lab 13 uses NumPy seed 42; other fixtures use fixed formulas or explicit values. Exports retain source labels.

### Astra, plotting and concept diagrams
- Model: `gpt-6-astra`, accessed optionally through the Responses API from full CPython, not locally installed in Pyodide.
- Official sources checked 2026-10-02: [model](https://developers.openai.com/api/docs/models/gpt-6-astra), [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [image inputs](https://developers.openai.com/api/docs/guides/images-vision), [function calling](https://developers.openai.com/api/docs/guides/function-calling).
- The examples demonstrate general reasoning, image interpretation and tool use applied to geospatial evidence. No dedicated geospatial performance guarantee is asserted. Offline plans and tool calls are hand-authored fixtures, not model-generated responses.
- [Matplotlib](https://matplotlib.org/stable/) provides static charts. [Plotly](https://plotly.com/python/) (`plotly==6.5.0`) provides a rotatable surface, loading its matching JavaScript bundle from the Plotly CDN.
- The SVG concept maps under `book/notebooks/assets/` are authored diagrams, include text alternatives, and use no external diagram renderer.
- GeoLibre 3.0 native extrusion properties render the synthetic elevation columns. [Terrain controls](https://geolibre.app/user-guide/map-controls/) provide separate terrain context; loaded COGs do not automatically become that elevation source.

### GeoLibre hosted sample data
- Hosted sample used by quickstart: `https://assets.geolibre.app/data/places.geojson`
- Public DEM sample used by quickstart: `https://data.source.coop/giswqs/opengeos/dem.tif`
- Product landing page: https://source.coop/giswqs/opengeos
- Role: small, CORS-friendly demonstration assets.

### WorldPop
- Product family: WorldPop population counts, University of Southampton.
- Example WorldPop-on-H3 PMTiles mirror: `https://data.source.coop/smartmaps/h3ys-worldpop/khm.pmtiles`
- Mirror landing page: https://source.coop/smartmaps/h3ys-worldpop/khm.pmtiles
- Recommended citation for 2020 population-count products: Bondarenko, M., Kerr, D., Sorichetta, A., & Tatem, A.J. (2020). *Census/projection-disaggregated gridded population datasets for 189 countries in 2020 using Built-Settlement Growth Model (BSGM) outputs.* WorldPop, University of Southampton. https://doi.org/10.5258/SOTON/WP00684
- WorldPop license: CC BY 4.0 for the cited product family; verify license metadata for any substituted WorldPop layer.
- Role: population surface and H3 aggregation example.

### U.S. Census Bureau — Census 2020 / TIGERweb
- Service: https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer
- Example layer: Counties from the Census 2020 group, queried as GeoJSON.
- Provider/copyright: U.S. Census Bureau.
- Role: county polygons and 2020 population/housing attributes for feature engineering and clustering.
- Note: the notebook intentionally uses TIGERweb attributes that do not require an API key. Current Census Data API endpoints may require an API key.

### Major TOM Core multimodal chips
- Landing page: https://source.coop/major-tom/core
- Example tile prefix: `https://data.source.coop/major-tom/core/DATA/42/`
- Modalities used: Sentinel-2 (`s2/data.tif`), Copernicus DEM (`dem/data.tif`), ESA WorldCover (`wc/data.tif`).
- Major TOM is an AI-ready multimodal collection. Follow the landing page's per-source licensing and attribution requirements.
- Role: aligned EO inputs for browser raster visualization and unsupervised classification.

### Copernicus Sentinel-2
- Data programme: Copernicus / European Union.
- Source in these notebooks: Major TOM mirror on Source Cooperative.
- Data terms: use the applicable Copernicus Sentinel data terms and attribution described by the source collection.
- Role: multispectral Earth observation imagery.

### Copernicus DEM GLO-30
- Source in these notebooks: Major TOM mirror on Source Cooperative.
- Native product: Copernicus DEM GLO-30.
- Role: terrain/elevation context aligned to EO imagery.
- Follow the Copernicus DEM licensing/attribution stated by the source collection.

### ESA WorldCover
- Source in these notebooks: Major TOM mirror on Source Cooperative.
- Product: ESA WorldCover.
- Role: land-cover reference layer aligned to the EO chip.
- Follow ESA WorldCover citation/license requirements stated by the source collection.

### CHIRPS v3
- Producer: Climate Hazards Center (CHC), UC Santa Barbara.
- Mirror/processor: WFP Food Security and Nutrition Analysis Service (VAM), hosted by Source Cooperative.
- Landing page: https://source.coop/wfp/chirps-rnl-daily
- Fixed example COG: `https://data.source.coop/wfp/chirps-rnl-daily/v3.0/2024/01/15/chirps-v3.0.rnl.2024.01.15.tif`
- Citation: Climate Hazards Center CHIRPS3 Data Repository (2025), https://doi.org/10.15780/G2JQ0P
- Peer-reviewed reference listed by the mirror: Funk et al., *Scientific Data* (2026), https://doi.org/10.1038/s41597-026-07096-4
- License on the mirror: CC BY 4.0.
- Important: **CHIRPS is not produced by NOAA.** It is a Climate Hazards Center product. NOAA weather/climate datasets such as HRRR should be cited separately.

### USGS Earthquake Hazards Program
- GeoJSON feed documentation: https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
- Live monthly feed used: `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson`
- Provider: U.S. Geological Survey.
- Role: live point events for H3 aggregation and anomaly detection.
- Because the feed is live, results change over time; notebook output should record its run timestamp when used in research.

### OpenStreetMap
- GeoLibre basemaps may include OpenStreetMap-derived tiles.
- Attribution: © OpenStreetMap contributors, https://www.openstreetmap.org/copyright
- Role: contextual basemap.

### STAC catalogs and browsers
- STAC specification: https://stacspec.org/; STAC API specification: https://github.com/radiantearth/stac-api-spec.
- UN Biodiversity Lab Browser: https://stac.unbiodiversitylab.org/?.language=en; public API root: `https://unbl-prod-stac.azurewebsites.net/`. Asset access may require a UNBL workspace/token.
- Copernicus Data Space Browser: https://browser.stac.dataspace.copernicus.eu/; public API root: `https://stac.dataspace.copernicus.eu/v1/`.
- USGS LandsatLook Browser: https://landsatlook.usgs.gov/stac-browser/?.language=en; public API root: `https://landsatlook.usgs.gov/stac-server/`.
- WorldPop Browser: https://stac.worldpop.org/?.language=en; public API root: `https://api.stac.worldpop.org`.
- Role: standards-based discovery of collections, items, footprints, temporal metadata, assets, and licensing information for the STAC notebooks.

### GeoLibre Official Demos
- Gallery: https://geolibre.app/gallery/
- Collection: https://share.geolibre.app/giswqs/collections/official-demos
- Portable project convention: `https://share.geolibre.app/giswqs/{slug}.geolibre.json`
- Role: authored, portable examples that expose layer configuration, source attribution, inline GeoJSON, raster tile URLs, and visualization settings. Notebook 09 uses a compact, reviewed manifest of selected gallery descriptions; notebooks 10 and 11 read live project JSON directly.
- Licensing: GeoLibre software is MIT licensed, but every demo can incorporate data under different terms. Read the project description and original-provider terms before reuse.

### Sister Cities / Wikidata
- GeoLibre project: https://share.geolibre.app/giswqs/sister-cities-of-major-world-cities
- Project JSON: https://share.geolibre.app/giswqs/sister-cities-of-major-world-cities.geolibre.json
- Original structured-data source identified by the demo: Wikidata, “twinned administrative body.”
- Wikidata data access and CC0 statement: https://www.wikidata.org/wiki/Wikidata:Data_access
- Role: 367 mapped cities and 1,108 sister-city relationships for graph feature engineering, clustering, and anomaly exploration.

### NIFC WFIGS wildfire perimeters
- GeoLibre project: https://share.geolibre.app/giswqs/us-wildfire-perimeters-2025
- Project JSON: https://share.geolibre.app/giswqs/us-wildfire-perimeters-2025.geolibre.json
- Source identified by the demo: NIFC WFIGS Interagency Fire Perimeters, National Interagency Fire Center.
- Role: 2025 U.S. fire perimeters and attributes for spatial feature engineering and exploratory anomaly scoring.
- Operational caveat: the notebook snapshot is educational and must not be used for emergency decisions.

### User-supplied Power BI report / SaTScan teaching derivative
- Source report: `Prototype-July-8-2024.pbix`, supplied by the repository author.
- Committed derivative: `book/notebooks/data/pbix_top10_sat_scan.csv` contains the top ten rows from the report's `ALLMODELS` table plus city coordinate, elevation, and scenario summaries aggregated from `Climate-Sites-w-coords`.
- Role: reproducible teaching snapshot for notebook 16; it is not the complete report model and is not an independent reanalysis or operational hazard forecast.
- Interpretation: preserve the report's original source citations, terms, scenario definitions, and limitations when reusing these values.

### Rewiring Global Health / Six Thinking Hats
- Conceptual reference: https://github.com/jltobias/JupyterLite-Rewiring-Global-Health
- User-supplied artwork: `book/notebooks/assets/six-thinking-hats-global-health.png`, copied unchanged at the user's request.
- Role: structured reflection and sense-making prompts for responsible GeoAI learning. Six Thinking Hats concepts are associated with Edward de Bono; third-party names, concepts, and quotations retain their respective rights.

### Element 84 Earth Search / Sentinel-2
- STAC API: https://earth-search.aws.element84.com/v1
- Source/documentation: https://github.com/Element84/earth-search
- Collection used: `sentinel-2-c1-l2a` (Copernicus Sentinel-2 Collection 1 Level-2A, exposed as cloud-optimized GeoTIFF assets).
- Role: bbox/time/cloud-filtered scene discovery around a selected fire perimeter, metadata triage, footprint mapping, and direct streaming of the visual COG into GeoLibre.
- Licensing: inspect the Earth Search STAC Collection and Copernicus terms for current attribution and reuse requirements.

### Source Cooperative
- Platform: https://source.coop/
- Operator: Radiant Earth.
- Role: cloud-native hosting/mirroring for several example assets.
- License follows each individual product; Source Cooperative hosting does not replace source-product attribution.

## GeoAI and global-health visual field guide

- Seven authored chapters: `book/geoai/`. Their inline citations and `book/references.md` identify primary sources consulted on 2026-10-11 for definitions, public-health context, environmental measurement and governance.
- Twenty-four original conceptual SVGs: `book/assets/geoai/`, reproducibly generated by `scripts/build_geoai_primer.py`. These are explanatory schematics, not third-party agency artwork, model results or measured health estimates. Titles, complete embedded text descriptions and chapter reading guides accompany the visuals.
- The HIV cohort values (10,000; 8,000; 6,000; 5,400), score ranges, network sketches and coastal cross-section are explicitly invented illustrations. They are not additional data extracted from the PBIX report or a real program.
- The program applications are proposed transfers of notebook methods. They do not claim that WHO, CDC, UNAIDS, GPEI, NASA, NOAA, FEWS NET or IPCC endorses or has validated these notebooks.
- The supplied Six Thinking Hats artwork is unchanged. The purple-synthesis discussion and evidence-to-decision framing connect to the companion Rewiring Global Health repository; no new individual-level health data or external model calls were introduced.

## Additional high-value sources considered for future labs

### Copernicus C3S / Interactive Climate Atlas
- Atlas: https://atlas.climate.copernicus.eu/
- Excellent source for climate projections and indicators.
- A future notebook should use a stable, documented public API/download endpoint and preserve the dataset-specific citation and scenario metadata rather than scraping the interactive UI.

### NOAA
- NOAA open datasets (for example HRRR/GFS) are strong candidates for weather-focused labs, including cloud-native mirrors on Source Cooperative.
- They are intentionally listed separately from CHIRPS to preserve correct provenance.
