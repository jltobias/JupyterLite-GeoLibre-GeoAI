# Data and software source register

Last reviewed: **2026-09-16**.

This file is the consolidated citation and provenance register for the JupyterLite/GeoLibre/GeoAI examples. Each notebook also contains a concise citation section.

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

### Source Cooperative
- Platform: https://source.coop/
- Operator: Radiant Earth.
- Role: cloud-native hosting/mirroring for several example assets.
- License follows each individual product; Source Cooperative hosting does not replace source-product attribution.

## Additional high-value sources considered for future labs

### Copernicus C3S / Interactive Climate Atlas
- Atlas: https://atlas.climate.copernicus.eu/
- Excellent source for climate projections and indicators.
- A future notebook should use a stable, documented public API/download endpoint and preserve the dataset-specific citation and scenario metadata rather than scraping the interactive UI.

### NOAA
- NOAA open datasets (for example HRRR/GFS) are strong candidates for weather-focused labs, including cloud-native mirrors on Source Cooperative.
- They are intentionally listed separately from CHIRPS to preserve correct provenance.
