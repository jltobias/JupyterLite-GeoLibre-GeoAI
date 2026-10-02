# References and data-source register

The canonical data-source register for this project is [`DATA_SOURCES.md`](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/blob/main/DATA_SOURCES.md).

## Software

- **GeoLibre** — open-source, browser/desktop/Jupyter GIS: https://geolibre.app/ and https://github.com/opengeos/GeoLibre
- **GeoAI** — Wu, Q. (2026). *GeoAI: A Python package for integrating artificial intelligence with geospatial data analysis and visualization.* Journal of Open Source Software, 11(118), 9605. https://doi.org/10.21105/joss.09605
- **JupyterLite** — https://jupyterlite.readthedocs.io/
- **H3** — https://h3geo.org/
- **GPT-6 Astra** — [model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra), [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [image inputs](https://developers.openai.com/api/docs/guides/images-vision), [function calling](https://developers.openai.com/api/docs/guides/function-calling). Examples checked 2026-10-02; API access is optional.
- **Matplotlib / Plotly** — https://matplotlib.org/stable/ and https://plotly.com/python/. Static charts and interactive 3D surfaces complement native GeoLibre maps.

## Data

See the per-notebook citation cells and `DATA_SOURCES.md` for WorldPop, Census/TIGERweb, Major TOM, Sentinel-2, Copernicus DEM, ESA WorldCover, CHIRPS, USGS earthquake feeds, Source Cooperative, and OpenStreetMap attribution.

Labs 12–15 use synthetic teaching fixtures authored in the repository. The additional rainfall series in lab 04 is also synthetic and is not extracted CHIRPS data. Model plans and tool arguments shown in the default runs are hand-authored examples, not captured Astra responses. Real-data transfer exercises specify the metadata and validation needed before substituting observations.
