# Five minutes: from John Snow’s map to GeoAI

**A simple question:** can a model find groups of nearby recorded deaths before we reveal where the water pumps are?

Start here if your audience is new to JupyterLite, GeoLibre and GeoAI. This modern teaching extension uses the historical data in [PHI-Case-Studies’ 1854 cholera demonstration](https://github.com/PHI-Case-Studies/Jupyterlite-1854-Cholera-Basic/tree/476f6dd5a8430e6eb823e79614fda1d7e12a78fb). It does **not** suggest that John Snow used AI or that a spatial cluster proves what caused an outbreak.

[**Open the presentation controls in a full page**](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/files/assets/cholera/presentation.html) · [Read notebook 21](../notebooks/21_cholera_geoai_first_steps.ipynb) · [Run notebook 21 in JupyterLite](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html?path=21_cholera_geoai_first_steps.ipynb)

## Three tools, three different jobs

| Tool or idea | Plain-language job in this demonstration |
|---|---|
| JupyterLite | The workbench: runs the notebook’s Python in the browser. |
| GeoAI | The learning step: DBSCAN groups locations using geographic distance, without being given correct group labels. |
| GeoLibre | An optional interactive map viewer for exploring the already-computed result. It does not perform the clustering here. |

GeoAI is **an application of AI**, not an alternative to it. This example uses an ordinary machine-learning method with geographic coordinates and meter-based neighborhoods. Mapping displays observations; descriptive spatial statistics summarize them; machine learning fits patterns. A map is not automatically AI, and AI need not be a chatbot or a large neural network. See [What is GeoAI?](../geoai/primer.md).

## Present without waiting for a kernel

The controls below switch among **saved, reproducibly fitted DBSCAN results**. Python is not running in this panel. Use the notebook for a live fit; use this panel if package loading or an external map service is slow. All seven analytical maps are bundled locally and need no street-tile service.

```{raw} html
<iframe src="../lite/files/assets/cholera/presentation.html" title="Cholera GeoAI saved-results presentation: map, group and reveal pumps" width="100%" height="960" loading="lazy" style="border:1px solid #ccd8e5;border-radius:12px;"></iframe>
```

| Time | Do this | Suggested words |
|---|---|---|
| 0:00–1:00 | Select **Map locations**. | “These dots show where deaths were recorded. What pattern do you notice? A map helps us see; it has not learned a pattern.” |
| 1:00–2:00 | Select **Find groups**, initially 50 meters. | “Now a model groups nearby locations. We have not told it where any pump is.” |
| 2:00–3:00 | Try **25**, then **100 meters**. | “The same data can produce different groups. Our assumptions matter. One enormous group may not be very useful.” |
| 3:00–4:00 | Return to **50 meters**; select **Reveal pumps**. | “These are the same labels, with context added. Which places would you investigate? What other evidence would you need?” |
| 4:00–5:00 | Explain the boundary; optionally show the notebook. | “GeoAI can help us notice patterns. People must investigate, test explanations and make accountable decisions.” |

At 25 meters the bundled data produce **12 groups and 42 unassigned locations**; at 50 meters, **one group and seven unassigned**; at 100 meters, **one group and none unassigned**. These are model outputs for this data snapshot, not historical outbreak findings or estimates of disease risk. Group numbers and colors are arbitrary and can change between settings.

## What the short Python example actually does

The notebook exposes the core calculation rather than hiding it behind a chat prompt:

```python
coordinates_radians = np.radians(deaths[["LAT", "LON"]].to_numpy())
labels = DBSCAN(
    eps=50 / EARTH_RADIUS_M, min_samples=5,
    metric="haversine", algorithm="brute"
).fit_predict(coordinates_radians)
```

`LAT` and `LON` identify each location. Haversine measures distance over a sphere; the inputs must be latitude/longitude **in radians**, not raw degrees or GeoJSON’s longitude-first order. `eps` is the neighbor distance: here, 50 meters divided by Earth’s radius. A core neighborhood needs five locations, including itself. Connected neighborhoods can form a group much wider than 50 meters. `fit_predict` assigns each location a group label or `-1` for unassigned. These are the documented [DBSCAN conventions](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html).

There is **no pump table in the model inputs**. `DEATHS` is summed afterward for descriptive reporting, not used as a training weight. One building contributes one location whether it has one or several recorded deaths. The source notebooks’ mapping and death-weighted center are useful spatial analysis; this extension adds an explicit unsupervised learning step.

## Rehearse the live notebook

Open notebook 21 and run from top to bottom with **Shift+Enter**. The first cell loads packages; do this before the talk. The slider recomputes DBSCAN in Python. The checkbox reveals pumps as context. No model account, API key or Ollama is needed. The data are bundled; initial site/package loading still needs connectivity or a previously populated cache.

The optional final cell opens GeoLibre when `SHOW_GEOLIBRE=True`. Rerun that cell after changing the notebook controls. Alternatively, [open the bundled 50-meter GeoLibre project](https://web.geolibre.app/?url=https%3A%2F%2Fjltobias.github.io%2FJupyterLite-GeoLibre-GeoAI%2Flite%2Ffiles%2Fdata%2Fcholera-demo.geolibre.json). This fixed project includes pumps and does not follow the presentation controls. It uses the hosted viewer and basemap, so it needs network access. GeoLibre is created by **Qiusheng Wu and contributors**; see the [official citation](https://geolibre.app/citation/) and [Zenodo record](https://doi.org/10.5281/zenodo.20785400).

### Static presentation backup

```{figure} ../notebooks/assets/cholera/map.svg
:alt: Map of 250 recorded death locations, without machine-learned groups or pump markers.

Step 1 — Mapping: display the recorded locations. Newly generated analytical view, not Snow’s original map.
```

```{figure} ../notebooks/assets/cholera/groups-50.svg
:alt: DBSCAN at 50 meters: one group of 243 locations and seven unassigned locations, with pumps hidden.

Step 2 — GeoAI: fit geographic groups. The distance setting is a teaching choice, not an estimated transmission distance.
```

```{figure} ../notebooks/assets/cholera/pumps-50.svg
:alt: The same 50-meter groups with eight water pumps overlaid as diamonds P1 to P8.

Step 3 — Human interpretation: add context and ask what to investigate. P1 is the source’s Broadwick Street record in the historical Broad Street setting.
```

## End with a responsible global-health message

The files contain **250 locations, 489 recorded deaths and eight pumps**, not a verified complete record of the outbreak. There are no population denominators, individual water-use observations, comparison households or temporal records. Building density, missing observations, geocoding and parameter choices can all affect the groups. We compute no disease rates, statistical significance, forecasts or intervention effects. An unassigned location is not “safe”; hiding a pump does not simulate prevention.

John Snow’s investigation included interviews and water-use evidence beyond a map; see the [CDC’s historical account (2004)](https://www.cdc.gov/Mmwr/preview/mmwrhtml/mm5334a1.htm). The classroom analogy for global health is **notice → question → investigate → validate**, not “AI discovers the cause.” Contemporary applications require appropriate denominators, independent validation, local expertise and privacy safeguards; never upload patient addresses to this public teaching site. Continue to [outbreak-response applications](../geoai/outbreaks.md).

### Data and visual credits

Data and teaching inspiration: PHI-Case-Studies contributors, *Jupyterlite-1854-Cholera-Basic*, [revision 476f6dd](https://github.com/PHI-Case-Studies/Jupyterlite-1854-Cholera-Basic/tree/476f6dd5a8430e6eb823e79614fda1d7e12a78fb). CSV files are unchanged; the upstream **GPL-3.0 license** and checksum provenance accompany them in `notebooks/data/cholera/`. Original digitization and completeness were not independently verified. No upstream notebook code, images or videos were copied. The point maps and saved-results controls are new, reproducible teaching materials derived from the attributed data; they are not historical-map reproductions. Sources reviewed 11 October 2026.
