# What is GeoAI?

Looking for the tools rather than the methods? [What is JupyterLite?](../platforms/jupyterlite.md) introduces the browser workbench; [What is GeoLibre?](../platforms/geolibre.md) introduces the mapping workspace. GeoAI is the analytical idea, not another name for either application.

**GeoAI uses artificial-intelligence methods with geographic data and reasoning.** It asks not only “what pattern is present?” but also “where, when, at what scale, and connected to what?” Geography changes the inputs, interpretation and testing of a model. This introduction follows the broad definition used in [USGS GeoAI research](https://www.usgs.gov/publications/geoai-us-geological-survey-topographic-mapping).

This visual field guide answers the questions behind the code. Start here without installing Python or running a notebook. All 24 new diagrams are original teaching schematics, not measured health outcomes; the surrounding text provides their reading guide. Open any diagram in a new tab to enlarge it.

## Is GeoAI different from “traditional AI”?

![GeoAI sits within AI and combines geographic context with GIS and health-domain knowledge.](../assets/geoai/what-is-geoai.svg)

**Read the picture:** the inner box is not a rival to the outer box. GeoAI can use familiar AI methods, including machine learning, computer vision and language models. The geographic context makes the application spatial: neighboring observations may resemble one another, roads connect some places but not others, and the same pattern can mean different things at different scales. GIS contributes spatial operations; health professionals and communities supply knowledge that is not contained in coordinates.

| Ordinary example | Geographic version | What geography adds |
|---|---|---|
| Group records with similar numeric values | Group districts by selected environmental or service indicators | Boundaries, rates, spatial scale and regional interpretation |
| Classify an image | Identify features in georeferenced satellite imagery | Pixel size, acquisition date, cloud masks and positional accuracy |
| Flag an unusual record | Flag an unusual place–time service pattern | Local baseline, reporting completeness and spatial/time validation |
| Summarize text | Explain verified evidence linked to places | Traceable geographic sources and limits on unsupported spatial claims |

“Traditional AI” is a broad phrase, not a precise opposing category. A standard K-Means algorithm can be part of GeoAI when applied to geospatial features. A chatbot mentioning a city is not automatically doing spatial analysis. The **field of GeoAI** is also broader than the particular **`geoai-py` software package**: these browser lessons teach selected methods, not the entire package's deep-learning stack.

## Why does place matter?

![Two invented communities have the same straight-line distance to a clinic, but a closed bridge forces a longer route.](../assets/geoai/spatial-context.svg)

**Read the picture:** home area H and clinic C did not move. Closing the bridge changes the route, not their coordinates. A model using only straight-line distance might miss a barrier to care. [Lab 15](../notebooks/15_astra_network_accessibility.ipynb) lets you change a bridge in an invented network and compare travel times. That calculation is a spatial algorithm, not learned AI; it could become an input to a larger GeoAI workflow.

Three other geographic traps deserve names:

- **Spatial dependence:** nearby places may share conditions. Testing on near-neighbors of training data can exaggerate performance elsewhere.
- **Scale and boundaries:** an average for a large district can hide a small underserved area; regrouping observations can change a pattern.
- **Ecological fallacy:** an area-level association does not establish an individual's status, behavior or risk.

## Which parts of these notebooks are actually AI?

![Four method families distinguish spatial algorithms, machine learning, text or optional model assistance, and evidence interpretation.](../assets/geoai/methods.svg)

**Read the picture:** a project can benefit from all four families. Only some steps learn from data. For example, `fit_predict(...)` in a clustering lab learns group assignments from features; a threshold such as `temperature >= 30` applies a rule chosen by its author. A map renders the result of either operation but does not turn a rule into a trained model.

The [18-notebook atlas](notebook-atlas.md) identifies exactly what each lesson does. In particular, labs 12–15 run deterministic, synthetic exercises by default; optional external-model requests are separate. Lab 16 visualizes pre-existing SaTScan report results. Lab 17 structures human discussion. Neither performs a new AI analysis of disease burden.

## Why demonstrate this in a browser?

![A three-part runtime diagram separates local browser computation, external data and map services, and optional server or GPU work.](../assets/geoai/browser-boundary.svg)

**Read the picture:** JupyterLite makes small, inspectable experiments available without a local Python installation. A novice can alter a feature, threshold or route and see the consequence. GeoLibre provides interactive geographic views through the browser adapter. Large model training is a different environment; browser memory, package compatibility, service availability and cross-origin access still constrain these lessons.

This is useful for teaching, prototyping and explaining assumptions to program colleagues. It is **not evidence that a prototype is ready for sensitive operational data**. External map services can receive requests and supplied layer content; an exported notebook can retain outputs. Use public or synthetic examples in this public site, never patient addresses, line lists, HIV status or credentials.

## A two-minute teach-back

Explain this sentence to a colleague: “We clustered geographic feature profiles, then mapped them.” What learned from data? What did the map add? What claim would go too far?

One reasonable answer: the clustering method learned similarity groups; the map showed their locations; the groups do not, by themselves, prove disease risk or the cause of a pattern.

**Next:** [How GeoAI works](how-it-works.md), then choose a program in [HIV and TB](hiv-tb.md), [outbreak response](outbreaks.md), or [climate and health](climate-health.md).
