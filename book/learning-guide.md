# First steps: read the code, see the idea

New to the tools themselves? Read [What is JupyterLite?](platforms/jupyterlite.md) for the notebook interface and saving your work, and [What is GeoLibre?](platforms/geolibre.md) for map layers and the browser integration. Both use attributed graphics from the supplied July 2026 presentation.

For the bigger picture, begin with [What is GeoAI?](geoai/primer.md), the [21-notebook method atlas](geoai/notebook-atlas.md), and the illustrated applications for [HIV/TB](geoai/hiv-tb.md), [outbreaks](geoai/outbreaks.md) and [climate–health](geoai/climate-health.md). They explain why the code matters before introducing Python syntax.

You can learn from these notebooks before writing Python from scratch. Start with the question, read the visual field guide, then run one code cell at a time. Each of the 21 notebooks has a captioned mini-video, an infographic, a teaching cartoon and a reading guide before every code cell.

[Open the visual learning library](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/files/assets/learning/index.html) or [launch JupyterLite](https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI/lite/lab/index.html). Videos are 32-second silent storyboards with pause/seek controls, English captions and full text transcripts. They explain the method rather than replaying a live model run. The illustrations are original schematics; analytical plots in the notebooks use the sources identified in their citation cells.

## Your first five minutes

1. Open notebook **00** in JupyterLite. The published book is a readable version; the live notebook is where code runs.
2. Read the opening question and infographic. Predict what the first map should contain.
3. Select the first code cell and press **Shift+Enter**. Wait for its running indicator to finish; the first package downloads may take time.
4. Continue downward. A cell can use names created by earlier cells, so skipping setup often causes a `NameError`.
5. Change one number, predict its effect, then rerun that cell and the cells that depend on it. Compare the result with the prediction.

Use **Kernel → Restart Kernel** followed by **Run → Run All Cells** when you want a fresh, ordered run. Some live-data notebooks require reachable public services, so a network failure may stop that run. Their explanations and illustrations remain readable.

Your browser session is not a Git commit. Download notebooks or exports you want to keep using the file browser's download action. If a deployed update seems absent, an older editable copy may still be saved in browser storage. Preserve your work, then download the latest notebook from the repository and open it under a new name. See [JupyterLite's content documentation](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html).

## Read a cell as input → operation → output

In a typical cell, `table` holds records, an operation computes a new column, and a display makes the result visible. The name on the left side of `=` remembers the value on the right. It does not assert mathematical equality.

| Python you will see | Plain-language reading | Why it matters here |
|---|---|---|
| `import pandas as pd` | Load a package and give it a short alias | Later `pd.DataFrame(...)` calls belong to pandas |
| `await micropip.install(...)` | Wait for a package installation | Loading must finish before its functions can be used |
| `m = Map(...)` | Build a map object and remember it as `m` | Later cells add layers to that same object |
| `{'name': 'A', 'value': 3}` | A dictionary of named values | GeoJSON, STAC and model requests use nested records |
| `[a, b, c]` / `(lon, lat)` | A list / an ordered pair | Order carries meaning for geometry and function arguments |
| `table['population']` | Select the column called population | Each row remains tied to its location or identifier |
| `table[table.value >= 30]` | Keep rows whose value meets a condition | A transparent rule makes a geographic selection |
| `for row in table.itertuples():` | Repeat for each row | One table record can become one map feature |
| `[f for f in features if ...]` | Build a list while filtering | A compact loop selects matching polygons |
| `def transform(value):` | Define reusable instructions | A function separates a method from repeated calls |
| `.groupby('h3').agg(...)` | Summarize records sharing the same cell | Event-level data becomes a spatial feature table |
| `.fit_transform(X)` | Learn a transformation and apply it | Scaling and text encoding prepare model inputs |
| `.fit_predict(X)` | Fit a model and return labels | A learned group can be joined back to geometry |
| `f'City: {name}'` | Insert a value into a string | Labels and provenance can travel with an output |
| `display(result)` / `plt.show()` | Render an object / plot | A successful calculation may otherwise show no output |

Indentation groups the statements controlled by `if`, `for` or `def`. A line beginning with `#` is a comment for people. `None` represents absence; `NaN` usually indicates a missing numeric value. Neither should automatically be interpreted as an observed zero.

## What makes the examples GeoAI?

GeoAI combines geographic information with learning or AI-assisted reasoning. These notebooks also teach the spatial, statistical and interpretive steps that make those systems useful. A map, index, threshold or visualization does not become a trained model simply because it appears in a GeoAI lesson.

| Lessons | What actually happens | What to learn from it |
|---|---|---|
| 00–01, 04, 06–07 | Maps, H3, rolling sums, runtime inspection and STAC discovery | Prepare and inspect evidence before learning |
| 02–03, 05, 08–10 | K-Means, image/text features, anomaly models and graph features | Learn modest, inspectable patterns in the browser |
| 11 | Learned anomaly/cluster outputs plus an explicit scene-ranking formula | Separate learning from human-chosen preferences |
| 12–15 | Deterministic synthetic calculations and optional model handoffs | Compare an AI explanation or proposed operation with computed evidence |
| 16 | Existing SaTScan report results, scenario comparison and linked views | Interpret statistical outputs without fitting another model |
| 17 | Authored questions for a human workshop | Connect interpretation to accountable decisions |

K-Means group numbers are arbitrary labels. The model groups the features you supply; it does not discover a moral ranking, a cause or a guaranteed real-world category. See the [scikit-learn clustering guide](https://scikit-learn.org/stable/modules/clustering.html#k-means).

## Where the computation happens

The browser runs a Pyodide Python kernel for supported local calculations. The notebook's `LiteMap` adapter creates a map recipe and displays it through GeoLibre's hosted viewer. Data APIs, raster assets, basemaps and some rendering resources still require network access. Optional model calls in labs 12–15 use the separate full-Python runner described in those lessons; the default lessons do not send them.

| Boundary | What crosses it | A useful check |
|---|---|---|
| Provider → browser | Metadata, small tables, imagery or visible tile ranges | Record source, time, license and units |
| Python → map viewer | Layer definitions, geographic features and styling | Check coordinate order and what each color encodes |
| Browser → optional full-Python workflow | Downloaded evidence, images or request JSON | Read what is exported before sending it |
| External result → notebook | An imported response or predictions | Recompute measurements and inspect supporting evidence |

The full `geoai-py` deep-learning environment is a continuation path, not a dependency installed by these lessons. Package availability and browser capabilities vary; [Pyodide's FAQ](https://pyodide.org/en/stable/usage/faq.html) explains runtime detection and browser limitations.

## Learn to read the visuals

**Map:** start with source and date, then the legend, unit and spatial scale. GeoJSON positions are longitude first. H3's `latlng_to_cell` accepts latitude first. A footprint describes coverage; a STAC asset contains or links to the data. See the [STAC specification overview](https://stacspec.org/en/about/stac-spec/).

**Chart:** name the axes and denominator. A count of cells, share of pixels and share of people answer different questions. Equal colors across two charts only support comparison if their color scales are also equal.

**Animation:** read each frame label. A sequence of A/B/C scenarios can compare alternatives without being a measured time series or a forecast. In lab 16, bubble changes do not animate a physical flood surface.

**3D:** read the vertical axis and display scaling before interpreting height. In lab 14, height is synthetic elevation in metres. In lab 16, height is relative risk. Rotating the camera changes visibility; it does not change the values.

**Cartoon or infographic:** use it to understand the reasoning, then find the notebook evidence that supports the claim. The illustrative dots, pixels and graphs are deliberately schematic.

## When something goes wrong

| Symptom | What it can mean | First action |
|---|---|---|
| `NameError: ... is not defined` | A prerequisite cell did not run or the kernel restarted | Start at setup and run in order |
| Package import fails | Loading failed or that package is unavailable in this runtime | Read the setup output and runtime note |
| `NetworkError` or failed request | Provider availability, CORS, authentication or connectivity | Check the source link; the error alone does not identify one cause |
| STAC query returns no items | This particular request returned nothing | Inspect extent, date, collection and access status |
| A map frame is blank | A viewer, source or web resource may not have loaded | Read table/chart evidence while checking the layer URLs |
| A result changed on a fresh run | Live data, a parameter or execution order may differ | Compare retrieval time and settings |

Do not attempt to fix CORS by disabling browser security. For the intentionally skipped catalog probes in lab 07, follow the human-facing STAC browser links. A browser accepting a page does not imply that its APIs allow cross-origin reads.

## Choose your learning path

| Your goal | Suggested order | Explain this at the end |
|---|---|---|
| Understand maps and browser learning | 00 → 01 → 02 → 06 | How a feature table becomes a learned group on a map |
| Learn imagery and data discovery | 07 → 08 → 03 → 13 | Why metadata, pixels and validated meaning differ |
| Explore climate and hazards | 04 → 05 → 11 → 16 | Which values are observations, scores or scenarios |
| Explore AI-assisted spatial reasoning | 12 → 14 → 15 → 17 | How a proposed explanation is checked against calculations |

After each lesson, finish these sentences: **I used…**, **the code computed…**, **the visual shows…**, and **I still need to check…**. A useful explanation should let another person reproduce the calculation and question its interpretation.
