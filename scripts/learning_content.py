"""Authored teaching copy, keyed to the code cells in each notebook.

The build checks each anchor against the corresponding cell before inserting
Markdown. Keep explanations here so videos, transcripts and notebooks agree.
"""


def step(title, anchor, explanation, result, experiment):
    return dict(title=title, anchor=anchor, explanation=explanation,
                result=result, experiment=experiment)


SETUP = step(
    "Prepare the browser toolbox", "import sys",
    "`import` makes a package available to Python. `sys.platform` identifies the runtime; "
    "the indented `if` block runs only in Pyodide. `await` waits for package loading. "
    "`LiteMap as Map` gives the browser-compatible map class a shorter name. Installing a "
    "package and importing its functions are separate steps.",
    "Imports complete before you run the next cell. The first run can take longer while packages download.",
    "Find the alias `Map`. If a later cell says a name is undefined, rerun this setup cell first.")
PLOTS = step(
    "Load the plotting tools", "loadPackage",
    "`from IPython.display import display` lets a cell show objects explicitly. In Pyodide, "
    "`await loadPackage('matplotlib')` loads a compiled plotting package. The `if` block "
    "is skipped in ordinary Python, where the package must already be installed.",
    "This preparation cell may show no figure; the next cell creates it.",
    "Keep this cell before the chart cell when you rerun the notebook after a kernel restart.")
RESPONSE = step(
    "Inspect an optional model response", "RESPONSE_PATH",
    "`None` means no response file was supplied. Only a real path enters the `if` branch; "
    "`json.loads` converts saved JSON text into Python objects. The `else` branch keeps the "
    "default lesson usable without an API call. Follow the preceding export/import instructions for live use.",
    "The default run prints an offline message. An imported answer is evidence to inspect, not a new measurement.",
    "Write your own explanation first, then check any imported response against the computed values and units.")


LESSONS = {
"00": [
    SETUP,
    step("Build a map from two kinds of data", "m.add_cog",
         "`m = Map(...)` stores a map object. `center=(-98, 39)` is (longitude, latitude); `zoom` controls the view. "
         "`add_geojson` adds discrete places and `add_cog` adds a raster grid of elevations. A URL is an address, not the data itself. "
         "The last line `m` asks Jupyter to display the map.",
         "A layer panel with places and a DEM, subject to the remote services loading.",
         "Change only `zoom` from 3 to 4. Did any elevation values change, or only your view?"),
    step("Keep the map recipe", "m.to_project()",
         "`to_project()` collects layer definitions and camera settings into a dictionary. `project.keys()` lists its top-level field names. "
         "This recipe can point to remote assets without copying their pixels into the notebook.",
         "A list of project keys, not a saved file; this cell does not call a file-writing function.",
         "Compare the idea of saving a map recipe with saving a screenshot. Which can be restyled later?"),
    PLOTS,
    step("Decode longitude and latitude", "points =",
         "The dictionary gives names to coordinate pairs. The `for` loop unpacks each pair into `x` and `y`, plots a dot, "
         "and labels it. A second loop places the same points on GeoLibre. `plt.show()` displays the chart; `display(...)` displays the map.",
         "B is east of A, and C is north of A. Both views should agree.",
         "Change B's longitude to -122.32 and predict which side of A it will appear on before running.")],
"01": [
    SETUP,
    step("Open a population tile archive", "WORLDPOP_H3",
         "An uppercase variable stores the PMTiles URL. `add_pmtiles` lets the viewer request tiles for the current view. "
         "Python has not loaded a table of population totals here; it has configured a map layer.",
         "A WorldPop H3 layer over Cambodia when the remote archive loads.",
         "Zoom into Phnom Penh and inspect the legend or feature attributes before interpreting a color as a count."),
    step("Turn one location into a hexagon", "latlng_to_cell",
         "`h3.latlng_to_cell(lat, lon, 7)` assigns a spatial index at resolution 7. H3 accepts latitude first, "
         "whereas GeoJSON needs longitude first. The list comprehension swaps each boundary pair, then repeats the first point to close the polygon.",
         "An H3 identifier in `cell` and a GeoJSON polygon in `feature`; neither contains a population count.",
         "Change resolution 7 to 8. Predict whether the cell grows or shrinks."),
    step("Overlay the hexagon and its reference point", "m.add_marker",
         "A FeatureCollection wraps a list of features. `fillOpacity=0.25` leaves the population tiles visible underneath. "
         "`add_marker(lon, lat)` places the reference point using map coordinate order.",
         "A highlighted cell around the Phnom Penh marker.",
         "Switch the WorldPop layer off. What information remains, and what information disappears?"),
    PLOTS,
    step("Measure the effect of spatial resolution", "h3.grid_disk",
         "`grid_disk(cell, 2)` returns nearby H3 indexes; each becomes a polygon patch. The list comprehension calculates "
         "cell area in square kilometres for resolutions 3 through 9. `semilogy` uses a logarithmic vertical axis so very different areas fit together.",
         "A neighborhood sketch and a falling cell-area curve. These are geometry measurements.",
         "Try radius 3 and compare the number of cells. Explain why more cells alone does not mean more people.")],
"02": [
    SETUP,
    step("Import table, geometry and learning tools", "StandardScaler",
         "`pd`, `np`, and `gpd` are aliases for pandas, NumPy and GeoPandas. `pyodide_http.patch_all()` adapts requests to browser networking. "
         "`StandardScaler` rescales numeric features; `KMeans` learns groups from them.",
         "Tools are ready; no model has been fitted yet.",
         "Locate the two learning imports and the one networking adapter."),
    step("Fetch Illinois county records", "STATE='17'",
         "`params` is a dictionary of query options. The STATE filter limits the download, `outFields` selects columns, "
         "and `outSR=4326` requests longitude/latitude geometry. `raise_for_status()` stops on HTTP errors; `from_features` creates a spatial table.",
         "`gdf.head()` previews five rows, although `gdf` holds all returned counties.",
         "Compare a row's population count with its land area. Why might ranking by count alone favor large counties?"),
    step("Learn groups from comparable features", "KMeans(n_clusters=5",
         "`to_crs(5070)` projects geometry before measuring area. Division by one million converts m² to km². "
         "`log1p` compresses large values, and `fit_transform` standardizes the features. `fit_predict` fits five groups and returns a group ID per county. "
         "The zero fill for an undefined people-per-housing-unit ratio is a modeling choice to revisit if such records occur.",
         "Three density/ratio features plus arbitrary cluster IDs. `random_state=42` makes this fitting reproducible for the same inputs.",
         "Try four clusters and rerun the map and charts. Record which counties move without calling any group better or worse."),
    step("Compare population and learned patterns", "m.add_choropleth",
         "A choropleth colors polygons by a column. The first layer uses density; the second uses the learned cluster ID. "
         "Quantiles group a numeric distribution into classes. Cluster numbers label categories and do not have a low-to-high meaning.",
         "Two switchable county layers answering different questions.",
         "Inspect a county in both layers and describe its actual features rather than only its cluster color."),
    PLOTS,
    step("Check what the model actually grouped", "corr = X.corr()",
         "The loop plots one cluster at a time. `symlog` makes a wide numeric range readable while allowing zero. "
         "`X.corr()` compares the log-transformed features; the nested loops print each correlation value on the heatmap.",
         "A scatter plot and a correlation matrix that reveal whether population and housing repeat a similar signal.",
         "If two predictors are strongly correlated, how might including both affect the clustering?")],
"03": [
    SETUP,
    step("Stream three complementary Earth layers", "major_tom.add_cog",
         "The f-strings reuse a base address to form three COG URLs. `bands=[4, 3, 2]` chooses the displayed Sentinel-2 channels; "
         "`rescale` controls their appearance. Elevation and land cover provide different context for the same example chip.",
         "A GeoLibre project with imagery, terrain and land-cover layers; these layers are separate from the following NASA image experiment.",
         "Toggle each layer and state what its values represent before comparing their colors."),
    step("Request a small georeferenced image", "source_image =",
         "`BBOX` records west, south, east, north. The WMS request fixes an image date and size. "
         "`response.content` is a sequence of bytes; `BytesIO` lets Pillow open it like a file, then `.convert('RGB')` creates three color channels.",
         "A 512 by 512 NASA GIBS image, with the selected date printed beside its size.",
         "Keep the same bounding box if you compare dates. Why would a changed extent confuse a change analysis?"),
    step("Convert pixels into a learning table", "pixels = rgb.reshape",
         "Resizing makes the problem small enough for a browser. Dividing by 255 puts colors on a 0–1 scale. "
         "`reshape(-1, 3)` makes one row per pixel and three feature columns. MiniBatch K-Means assigns six color groups; the last reshape restores image rows and columns.",
         "A 128 by 128 label grid and counts for each cluster ID.",
         "Explain why the model can group similar colors without knowing the words forest, water or cloud."),
    step("Put the model labels back on Earth", "from_bounds",
         "`from_bounds` connects array rows and columns to the original bounding box. `shapes` traces same-label regions into polygons. "
         "`dissolve` groups polygons with the same cluster ID; `simplify(0.01)` reduces boundary detail in degrees.",
         "One row per cluster with spatial geometry; simplified boundaries may lose small details.",
         "Why should a detailed measurement use the original pixels or validated geometry instead of this simplified display?"),
    step("Display the geographic prediction", "ml_map.add_choropleth",
         "The cluster column selects the polygon color and `fillOpacity` keeps the basemap visible. "
         "The f-string places the acquisition date into the layer name so the map carries temporal context.",
         "A map of RGB appearance groups over the requested region.",
         "Find a bright image region and inspect its cluster; name two possible causes for that brightness."),
    PLOTS,
    step("Read image, label and count together", "np.bincount",
         "`extent` uses west/east/south/north for plotting; `origin='upper'` places the first row at the north. "
         "A categorical palette links the label image to its bars. `bincount` counts label IDs, then division turns counts into percentages.",
         "Three linked panels: appearance, clusters, and pixel share. Pixel share is not an equal-area land-cover statistic.",
         "Change the number of clusters only if you also update the palette, boundaries and count length consistently.")],
"04": [
    SETUP,
    step("Display one day of rainfall", "rescale=[0, 75]",
         "Python joins the two adjacent strings into a COG URL. `add_cog` adds the raster to the viewer. "
         "The display range of 0–75 controls color; it does not change rainfall values or calculate an anomaly.",
         "A map layer for 2024-01-15, subject to remote access.",
         "Try a display maximum of 50. Which changed: the rainfall evidence or its visual emphasis?"),
    PLOTS,
    step("Turn daily rain into a trailing total", "np.convolve",
         "`rain` is an explicitly invented 30-day series. `np.ones(7)` creates seven weights of one. "
         "Convolution with `mode='valid'` sums only complete seven-day windows, giving 24 totals. `days[6:]` aligns the first total to day 7.",
         "Daily bars, trailing totals, and an invented monthly total. No rainfall values are extracted from the COG here.",
         "Set one wet day to zero and identify which seven-day windows change. A climate anomaly would also need a comparable baseline.")],
"05": [
    SETUP,
    step("Prepare aggregation and anomaly tools", "IsolationForest",
         "pandas stores the event table, H3 assigns spatial cells, and Isolation Forest learns unusual feature combinations. "
         "The HTTP patch adapts network calls to Pyodide without bypassing provider access rules.",
         "Imported functions, with no feed downloaded or model trained yet.",
         "Find the package responsible for geometry indexing and the one responsible for learning."),
    step("Read events and give each a spatial index", "eq[\"h3\"]",
         "The loop separates coordinates from properties in each GeoJSON feature. Missing magnitudes become `np.nan`, "
         "not zero. `zip(eq.lat, eq.lon)` pairs each latitude with its longitude before assigning H3 resolution 3.",
         "An event table and its record count. The monthly feed changes over time.",
         "Inspect an event's depth unit and record the feed date before comparing it with a future run."),
    step("Learn which cell profiles are unusual", "agg =",
         "`groupby('h3')` combines events in the same cell. Named aggregations calculate count, maximum, mean and depth. "
         "Missing predictors are imputed only in `X`; source measurements stay missing. Negating `score_samples` makes larger scores mean more unusual.",
         "One anomaly score per occupied H3 cell, relative to this feed and these features.",
         "Compare a high-score cell with its count and depth. Unusual does not mean a future earthquake is more likely."),
    step("Attach scores to map geometry", "ring.append(ring[0])",
         "`itertuples` visits the aggregate rows. The H3 boundary is reordered into GeoJSON coordinates, closed, and split at the date line when necessary. "
         "Explicit `float` and `int` conversions make values serializable; `None` preserves missing properties as JSON null.",
         "A FeatureCollection with one Polygon or MultiPolygon and a set of model attributes per cell. Pole-enclosing cells fail with an explicit GIS-conversion message.",
         "Identify the line that preserves a missing magnitude instead of inventing a measurement."),
    step("Separate event density from anomaly score", "m.add_heatmap",
         "The choropleth colors modeled cell scores. The heatmap uses each event with equal weight because `weight_field` is empty. "
         "Its radius is a visual smoothing choice, separate from the H3 aggregation scale.",
         "Two layers: where events are concentrated and where cell feature profiles are unusual.",
         "Toggle layers and find a place where the two signals disagree."),
    PLOTS,
    step("Check the time window and feature relationships", "pd.to_datetime(eq.time",
         "USGS timestamps are milliseconds since the Unix epoch. `utc=True` and `floor('D')` define daily bins consistently. "
         "The scatter pairs count with anomaly score and uses color for mean depth; the logarithmic x axis compresses count differences.",
         "Daily event counts, cell scores, feed generation time and a missing-magnitude count.",
         "Explain why the first and last day's bars may represent partial days.")],
"06": [
    step("Ask the runtime what is available", "find_spec",
         "`find_spec` checks whether Python can find a package; it does not test every feature or allocate a GPU. "
         "The dictionary comprehension repeats the check for each package name, returning True or False.",
         "A platform string and availability table specific to your current environment.",
         "Why is finding `rasterio` different from proving every TIFF compression codec works?"),
    SETUP,
    step("Inspect a remote land-cover raster", "nlcd_2021",
         "`add_cog` passes a cloud raster source to the hosted GeoLibre viewer. "
         "Displaying its pixels does not imply that Pyodide can train the model that created those land-cover classes.",
         "An NLCD example layer when the remote viewer and raster are reachable.",
         "Separate the data producer, the map renderer and the Python analysis in your own words."),
    PLOTS,
    step("Choose the right place to run each task", "matrix = np.array",
         "The hand-authored matrix encodes this repository's architecture: 1 means used here and 0 means a handoff. "
         "Nested loops put text in every square, so color is not the only way to read the diagram.",
         "A runtime decision matrix, not a speed test or universal compatibility guarantee.",
         "Trace how a browser-created GeoJSON file could go to a GPU workflow and return as mapped predictions.")],
"07": [
    SETUP,
    step("Keep provider addresses separate from requests", "CATALOGS =",
         "Each catalog has a human-facing browser URL and a machine-facing API URL. `get_json` wraps request, HTTP checking and JSON parsing. "
         "The loop deliberately skips direct probes in JupyterLite; in full Python it records successes or exceptions per provider so one failure does not stop the table.",
         "Four status rows. A skipped browser query is a policy choice in this notebook, not proof the provider is currently down.",
         "Locate `continue` and explain why no API request happens after it in the browser branch."),
    step("Make readable links from a dictionary", "display(Markdown",
         "An f-string fills each provider's name and URL into Markdown link syntax. "
         "The generator visits all providers and `'\\n'.join(...)` combines their lines. `Markdown` tells Jupyter how to render the resulting text.",
         "Clickable links to four STAC browsers alongside their API roots.",
         "Open one browser and identify a collection title and its license."),
    step("Follow the catalog's advertised relationships", "root.get('links'",
         "`dict.get` supplies a default if a field is absent. A set removes duplicate relationship names, "
         "and `sorted` makes the result readable. Subtracting the available-root names from all catalog names finds those that were not inspected.",
         "Relationship names in full Python when queries succeeded; a skipped list is expected in JupyterLite.",
         "Treat the final 'blocked' message as 'not inspected' for a deliberately skipped query; it is not a measured CORS diagnosis."),
    step("Use a context map without inventing coverage", "m.add_marker",
         "Each marker includes a provider link in its properties. These hand-placed points are illustrative context markers; "
         "they are neither provider headquarters nor the boundaries of catalog coverage.",
         "Four clickable context markers. No imagery search or download occurs in this cell.",
         "Explain why a point at 0,0 cannot describe the geographic extent of UN Biodiversity Lab."),
    PLOTS,
    step("Read STAC as a graph of links", "nodes =",
         "`nodes` gives diagram labels plot coordinates, not Earth coordinates. `edges` lists the arrows. "
         "The first loop draws relationships and the second draws labeled boxes. `axis('off')` hides meaningless spatial axes.",
         "A schematic catalog → collection → item → asset graph.",
         "Trace a path to a thumbnail and a different path to a COG; say which one contains analysis pixels.")],
"08": [
    SETUP,
    step("Search a small catalog sample", "QUERIES =",
         "Each query pairs an API address with a bounding box and item limit. `requests.post(..., json=payload)` sends a JSON body. "
         "The nested loop tags returned items with their source; `try/except` reports a provider failure and continues. Limits apply per query, not to the whole catalog.",
         "A possibly empty list of STAC Items. Browser access rules can prevent any response.",
         "Use a linked STAC browser from lab 07 if all requests fail; do not interpret zero returned items as zero available Earth data."),
    step("Normalize varied metadata into one table", "rows = []",
         "The loop uses `.get` to read optional fields and default values. It preserves geometry separately from the bounding box. "
         "Supplying column names to `DataFrame` keeps a predictable table even when there are no rows.",
         "One row per returned item with source, date, cloud cover and footprint information.",
         "Find a missing cloud value. Why is unknown cloud cover different from 0% cloud cover?"),
    step("Cluster metadata with missingness visible", "cloud_missing",
         "`to_numeric(..., errors='coerce')` turns invalid numeric text into missing values. A binary flag remembers missing cloud metadata. "
         "The model uses box width, height, cloud cover and that flag after standardization; the distinct-row count bounds the cluster count. "
         "With fewer than three items, cluster 0 is a placeholder and no model is fitted.",
         "Exploratory metadata groups. Degree widths are not equal ground distances across latitudes.",
         "Compare group membership with provider and missingness before claiming that it reflects landscape differences."),
    step("Map only items with geometry", "geo_items =",
         "The boolean filter keeps rows with nonmissing geometry. The loop turns table rows back into GeoJSON. "
         "Missing cloud values become null, preserving their meaning in map popups. The `else` branch handles an empty result explicitly.",
         "A footprint map or a clear no-footprints message.",
         "Explain why a footprint tells you where an item covers, but not what its pixels contain."),
    PLOTS,
    step("Inspect the sample before trusting groups", "if items.empty:",
         "The empty-table guard prevents plotting a nonexistent sample. `groupby(...).size()` counts only returned rows. "
         "The histogram drops missing cloud values and reports their number separately; bins span 0–100%.",
         "Provider sample counts and a cloud histogram when data arrived.",
         "Would doubling a query limit prove that a provider has twice as much data? Explain the sampling issue.")],
"09": [
    step("Create a small, inspectable search collection", "DEMOS =",
         "The list of tuples is a reviewed manifest of demo descriptions. `DataFrame` assigns names to its columns. "
         "Adding strings builds web and project-JSON URLs for every row; no full gallery is scraped.",
         "Eighteen demo titles and their tags, ready to become text features.",
         "Pick a demo and identify the words you expect a wildfire query to match."),
    step("Learn themes from word weights", "TfidfVectorizer",
         "The corpus joins title, tags and description. TF–IDF weights distinctive words and word pairs; `fit_transform` makes a sparse feature matrix. "
         "K-Means groups those vectors, and `argsort` finds prominent terms in each cluster center.",
         "Six vocabulary groups with example titles and distinctive terms.",
         "Explain why shared wording can group demos even if their underlying datasets are very different."),
    step("Sketch similarity in two dimensions", "TruncatedSVD(n_components=2",
         "SVD compresses many text features into two coordinates for plotting. `zip` pairs each demo row with its projected point. "
         "These axes are latent text dimensions, not longitude and latitude, and compression loses information.",
         "An annotated similarity scatter plot.",
         "Find two nearby labels and compare their descriptions; do not infer a geographic relationship from this plot."),
    step("Rank demos for your question", "QUERY =",
         "`transform` expresses the new query using the already learned vocabulary. Cosine similarity compares its direction with each demo vector. "
         "`nlargest(5, 'similarity')` selects five scores and the loop renders links. Scores measure word-based similarity, not answer correctness.",
         "Five suggested demos. A query with no known terms can produce all-zero scores and arbitrary ties.",
         "Try 'rainfall health population' and inspect whether the recommended descriptions actually support your task.")],
"10": [
    SETUP,
    step("Inspect the source map", "IFrame(DEMO",
         "`IFrame` places another web page inside the notebook. The embed flag requests its map view. "
         "This display is a reference example; analytical tables are created by later cells.",
         "The authored Sister Cities map if the remote page is available.",
         "Choose one city and predict whether its many links will translate into a high graph degree."),
    step("Read the map's portable data recipe", "links_fc = next",
         "The project URL returns JSON with layers. Generator expressions look for layer names containing 'links' and 'cities'; "
         "`next` selects the first matching layer. If the upstream structure changes, this selection needs inspection rather than guessed data.",
         "Two FeatureCollections and the source project's reported description and feature counts.",
         "Locate one point and one relationship feature in the source recipe."),
    step("Turn partnerships into a spatial graph", "G = nx.Graph()",
         "The location dictionary links city names to coordinates. `add_edge` connects city nodes with kilometre weights. "
         "Degree counts neighbors; sampled weighted betweenness measures how often a city lies on the graph's shortest paths. "
         "A simple Graph merges repeated edges between the same pair.",
         "A table of degree, approximate betweenness and relationship distances for graph nodes.",
         "Why might a city with few links still lie between otherwise weakly connected parts of this graph?"),
    step("Compare network roles and outliers", "network_role",
         "The four graph features are log-transformed and standardized before fitting. K-Means assigns four roles; "
         "Isolation Forest flags unusual combinations. `contamination=0.06` sets the approximate outlier fraction rather than measuring an objective bad-city rate.",
         "Median features by role and a ranked anomaly table.",
         "Describe an unusual city's feature profile without equating it with real-world influence or quality."),
    step("Reconnect learned roles with geography", "def point_collection",
         "Rows missing coordinates remain in analysis but are excluded from mapping. The helper function builds GeoJSON properties from each row. "
         "A loop adds one layer per role, then a final layer highlights unusual profiles.",
         "Categorical role layers plus a larger outlier overlay.",
         "Compare the number analyzed with the number mapped; explain what missing coordinates hide from the map.")],
"11": [
    SETUP,
    step("See the perimeter source", "IFrame(DEMO",
         "The iframe displays the authored 2025 wildfire project. `PROJECT_JSON` points to the machine-readable recipe that the next cell reads.",
         "A source map, before this notebook adds derived features or selects satellite scenes.",
         "Distinguish a historical perimeter snapshot from a live incident feed."),
    step("Measure shape in projected coordinates", "compactness",
         "GeoPandas attaches properties to geometries; `to_datetime` parses discovery dates. "
         "The projected copy supplies area in m² and perimeter in metres. Compactness uses 4π × area / perimeter², with a circle as the reference shape.",
         "Fire records with discovery day, projected area, perimeter and a shape descriptor.",
         "Explain why degrees of longitude are unsuitable units for directly calculating a fire perimeter in kilometres."),
    step("Select a case for investigation", "model_columns",
         "Log transforms reduce extreme acreage and perimeter differences; standardization balances feature scales. "
         "Isolation Forest flags unusual profiles. Among flagged records, the code sorts first by acreage and then anomaly score before choosing the target.",
         "A named investigation target; the selection is not a prediction of the next dangerous fire.",
         "Read the sorting order carefully: does the target necessarily have the highest anomaly score?"),
    step("Search satellite metadata near the target", "payload =",
         "Geometry bounds and a small degree padding define the search box. Timedeltas create a ±30-day window around discovery. "
         "The JSON query limits cloud cover and returned fields, keeping the first page small. A limit of 60 is not an exhaustive search.",
         "Candidate Sentinel-2 Items or a clear no-match error asking you to adjust the search.",
         "Why might two scenes with low whole-scene cloud cover still differ in cloud over the actual fire?"),
    step("Rank candidates with a visible scoring rule", "triage_score",
         "The loop collects dates, cloud percentages and visual-asset links. A weighted sum gives 65% weight to cloud cover and 35% to time distance. "
         "Missing cloud cover receives a conservative 100% proxy. This hand-set ranking is separate from K-Means acquisition groups.",
         "A sorted candidate table and its first row in `best_scene`.",
         "Swap the weights to 35% cloud and 65% time, then explain why the preferred scene might change."),
    step("Inspect the selection against the source geography", "best_scene['visual_cog']",
         "If a visual asset exists, the viewer streams it as an RGB COG. The map then adds scored perimeters, a highlighted target and candidate footprints. "
         "Dates are converted to strings so the spatial table can be serialized as JSON.",
         "A layered investigation map linking the chosen fire to candidate satellite coverage.",
         "Inspect the selected scene over the fire before proceeding to burn-severity analysis; this notebook does not calculate burn severity.")],
"12": [
    SETUP,
    step("Start with a known synthetic city", "teaching_city()",
         "The helper returns two aligned representations: a table of invented attributes and a GeoJSON grid. "
         "`head()` previews rows; `unique()` confirms the source label. Keeping stable cell IDs lets later views select the same places.",
         "64 teaching cells, each with invented temperature, canopy and population fields.",
         "Locate one cell ID and explain how it will connect the table to a map polygon."),
    step("Execute a bounded plan and test sensitivity", "apply_plan(table, plan)",
         "The dictionary states a field, comparison and threshold. `apply_plan` validates that allowed operation and filters rows. "
         "A set stores selected IDs. The panels compare the temperature grid, canopy scatter and percentage selected as the threshold changes.",
         "A repeatable selection from a hand-authored plan; the default code has not asked a language model to choose it.",
         "Increase the threshold from 30 to 32. Predict the direction of the selected-count change."),
    step("Map and export the selected cells", "selected_fc =",
         "The list comprehension keeps polygons whose IDs are in the selected set. The conditional avoids drawing an empty overlay. "
         "`save_json` writes a GeoJSON subset and map recipe to the notebook filesystem for download.",
         "A temperature map with selected outlines and two export files.",
         "Check a boundary cell's value against the >= comparison rather than guessing from its color."),
    step("Connect one slider to two views", "def update_threshold",
         "The callback runs when the slider changes. It updates the threshold, recomputes IDs, resets a deep copy of the base project and draws a histogram. "
         "`continuous_update=False` waits until you release the slider, reducing redraw work.",
         "A linked selection overlay and histogram with a moving threshold line.",
         "Drag to 34 and back to 30. Why would failing to reset the project accumulate old layers?"),
    step("Package evidence for an optional copilot", "request = make_request",
         "The evidence dictionary includes units, grid size, source and records. `make_request` builds a structured request with an allowed output schema. "
         "Saving that JSON prepares a handoff; it does not make an API call.",
         "A request file that can be inspected before using the separate full-Python runner.",
         "Find the source and units fields that prevent a model from mistaking this fixture for measured city temperatures."),
    RESPONSE],
"13": [
    SETUP,
    step("Create a scene with known change", "predicted =",
         "A fixed random seed makes the noise repeatable. Boolean arrays identify the invented changed rectangle and cloud. "
         "`np.linalg.norm(..., axis=2)` measures RGB difference per pixel; a threshold and validity mask define detected change. "
         "True/false positive/negative counts compare detection with known synthetic truth; IoU measures overlap.",
         "A change mask and overlap score for an easy controlled example with an oracle cloud mask.",
         "Predict what happens to false positives if you stop excluding cloud pixels."),
    step("Explain success and mistakes visually", "matrix = np.array",
         "The four image panels reuse one extent and orientation. Histograms compare known changed and unchanged pixels. "
         "The confusion matrix puts truth on rows and prediction on columns, with text counts so it remains readable without color.",
         "Before/after images, difference, detection, distributions and error counts.",
         "Point to the false-positive square and explain the kind of mistake it counts."),
    step("Convert detected pixels into mapped area", "area_m2 =",
         "`grid_features` turns the boolean result into synthetic 20 m grid cells. A list comprehension keeps only value 1. "
         "Multiplying the detected-cell count by 20² calculates the area in the local teaching grid.",
         "Mapped change polygons, an area value in m² and a GeoJSON export.",
         "Why must you multiply by pixel area instead of by pixel width?"),
    step("Give the optional model measured evidence", "images=[image_evidence]",
         "The evidence includes counts, units, mask size, threshold and source. The request combines these values with a labeled PNG. "
         "The prompt asks for observations and missing checks; numerical measurements still come from the code.",
         "A saved multimodal request containing one figure; no live answer is generated by this cell.",
         "Which parts of an explanation could the image support, and which require dates, calibration or local knowledge?"),
    RESPONSE],
"14": [
    SETUP,
    step("Distinguish elevation, slope and profile", "np.gradient",
         "`meshgrid` creates east/north coordinates. Two smooth bumps define an invented elevation surface. "
         "`gradient(z,100,100)` uses metre spacing to estimate derivatives; arctangent converts their combined rise/run into a slope angle. "
         "The selected array row defines a fixed northing for the profile.",
         "Contour, slope and cross-section views of exactly the same synthetic terrain.",
         "Find a high flat area and a lower steep area. Why are elevation and slope different questions?"),
    step("Rotate the terrain and inspect exaggeration", "go.Surface",
         "Plotly's Surface uses the same x, y and z arrays. The aspect ratio compares elevation range to horizontal extent. "
         "The menu changes vertical display scale without modifying elevations. A static Matplotlib surface supports reading outside the interactive viewer.",
         "An interactive surface with 1×, 2× and 4× vertical-scale options, plus a static 3D view.",
         "Toggle 4× and explain why the computed slope values do not change."),
    step("Put sampled heights into a GeoLibre scene", "extrusionHeightProperty",
         "The slices sample every fourth grid point to keep the layer small. `grid_features` makes display cells; "
         "the extrusion reads height from `elevation_m`. `set_view` tilts and rotates the camera. Columns represent sampled synthetic terrain.",
         "A tilted map of elevation columns and a saved project recipe.",
         "Describe the columns as a sampled representation rather than measured buildings or a continuous surveyed surface."),
    step("Prepare an evidence-based terrain question", "terrain_metrics",
         "`min`, `max` and profile selection calculate numbers directly from arrays. Converting NumPy values to Python floats makes them JSON-safe. "
         "The request supplies these measurements and the 2D figure to support a later explanation.",
         "A saved request with exact synthetic terrain statistics and units.",
         "Explain which extra information a real drainage or route decision would need beyond this surface."),
    RESPONSE],
"15": [
    SETUP,
    step("Follow a shortest-path algorithm", "def shortest_times",
         "The grid creates nodes and two-minute edges, with only two crossings of the river. "
         "The function builds neighbor lists, starts node 0 at time zero and uses a priority queue to visit the cheapest known route next. "
         "A shorter candidate replaces the stored time. Skipping one bridge changes connectivity; assertions check hand-traced examples.",
         "Baseline and closed-bridge times, including 8 versus 20 minutes at node 9.",
         "Trace node 9's detour on the diagram and explain why straight-line distance misses it."),
    step("Compare route maps with coverage curves", "plt.subplot_mosaic",
         "Both maps share a color scale, so the same color means the same number of minutes. "
         "For each threshold, `.le(t).mean()` computes the fraction of nodes reachable within that time. The step chart reflects discrete nodes.",
         "Before/after network maps and two accessibility curves, with node 0 marked as the destination.",
         "At 12 minutes, count covered nodes. Explain why this is not yet a percentage of residents."),
    step("Map the network with explicit attributes", "network_fc=",
         "Each edge becomes a LineString and each node becomes a marker. `local_lonlat` approximately anchors the invented grid on a basemap. "
         "Marker radius adds a fixed minimum to half the delay, keeping zero-delay nodes visible.",
         "A synthetic street map whose point properties contain baseline, closure and delay minutes.",
         "Compare a large marker's attributes with the table to decode its size."),
    step("Test the speed assumption", "fast=np.array",
         "Multiplying travel times by 0.8 and 1.2 creates faster/slower scenarios. Each is evaluated at the same thresholds. "
         "`fill_between` shades their envelope; these two assumed scenarios do not estimate a statistical confidence interval.",
         "Coverage curves with bands showing sensitivity to a ±20% travel-time change.",
         "Which matters more at your chosen cutoff: the bridge closure or the assumed speed?"),
    step("Expose a bounded calculation as a tool", "dispatch_tool",
         "The replay passes a named scenario and threshold to a permitted local function, which calculates from the route evidence. "
         "The request advertises that tool for optional model use. Separate files retain the full evidence and map recipe for inspection.",
         "A computed replay result and exported files; these arguments were hand-authored, not chosen by a live model.",
         "Compare the replay fraction with your own count at 12 minutes."),
    RESPONSE],
"16": [
    step("Read the small report derivative", "pd.read_csv",
         "The browser setup installs the plotting and map tools. `read_csv` loads the bundled ten-row summary. "
         "Adding city and country strings creates a readable label without changing the original rank or risk fields.",
         "Ten reported cluster summaries from the supplied PBIX, with supporting city-level aggregates.",
         "Compare `all_facilities` and `n_sites`: these come from different table summaries and must not be treated as the same denominator."),
    step("Compare rank, relative risk and location", "risk.sort_values",
         "Sorting the bar chart by relative risk changes display order, not the report's cluster rank. "
         "`itertuples` makes one representative city point per row, with properties for inspection. These points are not cluster boundaries.",
         "Relative-risk bars colored by facility count and a 2D map of the ten reported clusters' representative city locations.",
         "Identify the highest relative-risk bar. Is it also cluster rank 1 in the original report?"),
    step("Reshape columns for a scenario animation", "risk.melt",
         "`melt` turns the A/B/C columns into thirty rows: one city-scenario combination per row. "
         "A dictionary maps field names to scenario labels. `animation_frame` changes the displayed scenario while size and color encode the indicator.",
         "A scenario-comparison animation. A/B/C labels represent alternatives, not a measured time sequence or rising water surface.",
         "Check a changing bubble against the table. Why cannot its indicator value be read as metres of floodwater?"),
    step("Read the three-dimensional axes literally", "go.Scatter3d",
         "Longitude, latitude and relative risk become x, y and z. `np.clip` bounds marker sizes for legibility, "
         "so size is only a display cue. Color uses the all-scenario mean from the supporting sites table.",
         "A rotatable 3D statistical scatter; the vertical axis is relative risk, not terrain elevation or water depth.",
         "Compare the 3D view with the bars before drawing a conclusion; the camera can obscure points.")],
"17": [
    step("Turn perspectives into a readable table", "hats = pd.DataFrame",
         "`read_csv` opens the previous lesson's ten-row report derivative. Each tuple supplies one hat, mode and question; "
         "the column list names those fields. This is an authored reflection framework, with purple added for synthesis.",
         "Seven rows of questions: six de Bono perspectives plus the project's purple extension.",
         "Pick the white-hat question and identify a PBIX field you would need to verify."),
    step("Build workshop prompts with Python strings", "r.hat",
         "`itertuples` visits the perspectives. An f-string inserts each hat's labels into Markdown, and `join` assembles the list. "
         "`len(risk)` counts the report rows. Python formats an agenda here; it does not run seven autonomous agents or generate a model consensus.",
         "A workshop question list and a case snapshot referencing ten reported clusters.",
         "Write one competing interpretation, then assign who will check it and what evidence would change your mind.")],
}


def profile(title, question, role, browser, value, stages, dialogue, challenge, answer, visual):
    return dict(title=title, question=question, role=role, browser=browser, value=value,
                stages=stages, dialogue=dialogue, challenge=challenge, answer=answer, visual=visual)


PROFILES = {
"00": profile("A map is a data recipe", "How do coordinates and layers become an explorable map?",
    "Spatial foundation: this notebook does not fit a learning model.",
    "Python constructs a map recipe; GeoLibre's hosted viewer renders it in your browser. Remote assets and basemaps need network access.",
    "You can inspect and share the geographic context that later models need, using a few visible lines of Python.",
    [("Locate", "center=(-98, 39)", "A coordinate pair tells the map where to look: longitude first, latitude second."),
     ("Layer", "m.add_geojson(...)", "Vector places and raster elevations answer different questions about the same map."),
     ("Inspect", "m", "Display the map and compare a point with the raster beneath it."),
     ("Preserve", "m.to_project()", "Keep the recipe so the source addresses and styling remain inspectable.")],
    ["Can a colorful map explain a place?", "First connect each mark to a coordinate and a source.", "Then we can check what a later model claims!"],
    "What changes if you change zoom, and what changes if you change longitude?",
    "Zoom changes the view. Changing a feature's longitude changes its position. Neither alone trains a model.", "map"),
"01": profile("The hexagon is a container", "How does changing spatial scale change what we can compare?",
    "Spatial indexing foundation: H3 assigns cells; it does not estimate their populations.",
    "H3 geometry and area calculations run in Pyodide. The population PMTiles layer is streamed by the map viewer.",
    "A common spatial index can connect population with later model features while keeping scale choices visible.",
    [("Locate", "latlng_to_cell(lat, lon, 7)", "Assign one location to a resolution-7 H3 cell."),
     ("Outline", "cell_to_boundary(cell)", "Convert the cell boundary to longitude-first GeoJSON."),
     ("Compare", "h3.cell_area(...)", "Finer resolution covers a smaller area; geometry is independent of population."),
     ("Join later", "m.add_pmtiles(...)", "Use population attributes as a separate source before calculating exposure or density.")],
    ["More hexagons means more people?", "No: these are containers. Counts come from WorldPop.", "I will check area and population separately."],
    "If the same population is redistributed across finer cells, must the total grow?",
    "No. Spatial resolution changes the allocation units; a correctly conserved sum can stay the same.", "hex"),
"02": profile("From county rows to patterns", "Which counties have similar density and housing profiles?",
    "Browser machine learning: K-Means learns groups from engineered county features.",
    "Feature engineering, scaling and K-Means run in Pyodide after the Census service returns records.",
    "A small browser model helps explore many counties consistently, then returns group membership to the map for inspection.",
    [("Measure", "gdf.to_crs(5070)", "Use projected area to turn population counts into comparable densities."),
     ("Scale", "StandardScaler()", "Log transforms and standardization reduce domination by feature units and large values."),
     ("Learn", "KMeans(n_clusters=5)", "Group similar feature vectors; cluster numbers are category IDs."),
     ("Check", "X.corr()", "Compare maps, scatter and correlations before assigning meaning to groups.")],
    ["Is cluster 4 better than cluster 1?", "The numbers name groups; they do not rank counties.", "I will describe density and housing instead."],
    "Why compare the feature scatter with the geographic map?",
    "The scatter shows what the model grouped; the map shows where those records are. Both are needed to interpret the result.", "clusters"),
"03": profile("Pixels become model features", "Can a browser learn patterns from a small satellite image?",
    "Browser machine learning: MiniBatch K-Means groups RGB appearance; no labeled land-cover model is trained.",
    "A small NASA JPEG is decoded and clustered in Pyodide. The separate Major TOM COG layers render in GeoLibre.",
    "You can follow an entire image-to-feature-to-model-to-map pipeline without hiding the relationship between pixels and predictions.",
    [("Fetch", "source_image.resize((128, 128))", "A fixed date and bounding box anchor a compact image sample."),
     ("Reshape", "rgb.reshape(-1, 3)", "Each pixel becomes a row with red, green and blue feature values."),
     ("Learn", "model.fit_predict(pixels)", "Six clusters describe color similarity, with arbitrary IDs."),
     ("Map", "from_bounds(*BBOX, w, h)", "Restore geographic position, then compare original image and grouped regions.")],
    ["Blue pixels must all be water!", "The model learned colors, not the meaning of water.", "I need independent labels to test that claim."],
    "Can cloud and built surfaces land in the same bright cluster?",
    "Yes. RGB similarity can combine different surface types; semantic labels require additional evidence.", "pixels"),
"04": profile("A day is not a climate trend", "What does accumulated rain reveal that a daily map cannot?",
    "Feature preparation: streaming and rolling sums support a later GeoAI workflow; no anomaly model is fitted here.",
    "GeoLibre streams a real CHIRPS COG. A separate, clearly invented series is summed and plotted in Pyodide.",
    "Browser experiments make temporal feature engineering understandable before you train on real climate records.",
    [("View", "m.add_cog(CHIRPS, ...)", "Inspect one actual daily rainfall layer and its source date."),
     ("Practice", "rain = np.array(...)", "Use invented daily values to make the arithmetic easy to follow."),
     ("Accumulate", "np.convolve(rain, np.ones(7), ...)", "A trailing total combines seven consecutive days of rainfall."),
     ("Interpret", "days[6:]", "Align each total with its final day; a climate anomaly still needs a baseline.")],
    ["It stopped raining. Why is the curve still high?", "The seven-day window still contains earlier rain.", "I will read the time window before naming a trend."],
    "Why are there 24 complete seven-day windows in a 30-day series?",
    "The first ends on day 7 and the last on day 30: 30 − 7 + 1 = 24.", "rain"),
"05": profile("Unusual is a question to investigate", "Which spatial event summaries differ from the rest of this feed?",
    "Browser machine learning: Isolation Forest scores unusual H3 feature profiles.",
    "USGS events are downloaded; aggregation, H3 indexing and model fitting run locally in Pyodide.",
    "A model can help focus exploration of a large event table, while the map and charts expose why a profile might be unusual.",
    [("Collect", "response.json()", "Read event coordinates, magnitudes and depths from a changing monthly feed."),
     ("Aggregate", "eq.groupby('h3')", "Represent each occupied cell with event count, magnitude and depth summaries."),
     ("Score", "-iso.score_samples(X)", "Assign higher values to unusual feature combinations in this sample."),
     ("Challenge", "agg.sort_values(...)", "Inspect time window, missingness and depth before interpreting a high score.")],
    ["A red cell predicts an earthquake?", "It is unusual in this past-event sample.", "I will inspect the features, not forecast from the color."],
    "Can a low-count cell have a high anomaly score?",
    "Yes. Depth or magnitude combinations can differ from the rest even when few events occur.", "anomaly"),
"06": profile("Follow the runtime handoff", "Which parts of a GeoAI workflow belong in this browser?",
    "Architecture lesson: it checks packages and explains where computation takes place.",
    "Small arrays and supported learning packages run in Pyodide; remote data and the GeoLibre viewer still need services. Full GPU workflows use another runtime.",
    "A clear handoff lets people inspect features and predictions in a browser while using another environment for heavier computation.",
    [("Inspect", "sys.platform", "Identify the current Python runtime before choosing tools."),
     ("Check", "importlib.util.find_spec(name)", "Discover packages, then test the particular capability you need."),
     ("Exchange", "GeoJSON / JSON / PNG", "Export geometry, evidence and figures through understandable formats."),
     ("Return", "m.add_cog(...)", "Bring computed results back to a browser map for inspection.")],
    ["If I can see it here, was it trained here?", "Rendering a result and training a model are different jobs.", "I will label each computation's runtime."],
    "Does no local Python installation imply no network dependencies?",
    "No. First-time package loading, basemaps, remote assets and hosted viewers can all require the network.", "handoff"),
"07": profile("Read the catalog before the pixels", "How do we find an Earth dataset and understand its access path?",
    "Discovery foundation: STAC organizes metadata; this notebook does not train a model.",
    "The notebook offers browser links and a schematic graph. Direct API probing is intentionally skipped in JupyterLite to avoid unreliable provider requests.",
    "Reliable discovery records location, time, links and licensing before a GeoAI workflow spends resources on image assets.",
    [("Browse", "CATALOGS", "Keep human-facing browser links beside machine-facing API addresses."),
     ("Follow", "root.get('links', [])", "Catalog and collection links lead toward item metadata."),
     ("Inspect", "Item → assets", "An item describes geometry and time and links to data or thumbnails."),
     ("Check access", "browser_runtime", "A working catalog page does not prove every data asset accepts browser requests.")],
    ["I found a thumbnail. Do I have all the data?", "Check the item, asset type, license and access rules.", "Discovery comes before downloading and learning."],
    "Why does a skipped request differ from an empty catalog?",
    "A skipped request collected no evidence about contents. An empty response only describes that particular query.", "catalog"),
"08": profile("A footprint is not its contents", "Can we compare catalog items before downloading large imagery?",
    "Browser machine learning when enough items arrive: K-Means groups metadata, not image pixels.",
    "Browser HTTP searches may fail under provider access rules. Returned metadata is normalized, scaled and clustered locally.",
    "Small metadata samples can reveal coverage and missingness and help choose what to inspect next.",
    [("Search", "requests.post(..., json=payload)", "Bound the geographic question and the maximum returned sample."),
     ("Normalize", "pd.DataFrame(rows, ...)", "Put different providers' metadata into a common set of columns."),
     ("Learn", "items['cloud_missing']", "Preserve unknown cloud values as missingness information before clustering."),
     ("Inspect", "geo_items = items[...]", "Map valid footprints and compare groups with provider counts and cloud metadata.")],
    ["These footprints share a color. Same land cover?", "Only their selected metadata looked similar.", "I will inspect the actual assets before naming a surface."],
    "Is an imputed cloud value an observed measurement?",
    "No. It is a model input substitute; the missingness flag and original metadata preserve the distinction.", "footprints"),
"09": profile("A transparent discovery assistant", "Which existing map demos resemble the workflow I want to try?",
    "Browser text learning: TF–IDF features, K-Means themes, SVD visualization and cosine retrieval.",
    "The bundled eighteen-description manifest is processed in Pyodide. Opening recommended live projects needs network access.",
    "A visible text baseline can help find reusable geospatial examples and explain the words behind its suggestions.",
    [("Describe", "corpus = ...", "Combine each demo's title, tags and description into one document."),
     ("Encode", "vectorizer.fit_transform(corpus)", "Turn distinctive words and pairs into numeric features."),
     ("Compare", "cosine_similarity(query_vector, X)", "Compare a question with every description using the same vocabulary."),
     ("Inspect", "nlargest(5, 'similarity')", "Read the suggested projects; a similarity score is not a correctness probability.")],
    ["The first suggestion must be the right answer!", "It matched words. Read its data and workflow.", "I can change my query and compare the evidence."],
    "What happens if none of your query words is in the learned vocabulary?",
    "The query vector can be all zero, producing tied zero scores rather than meaningful recommendations.", "retrieval"),
"10": profile("Geography plus relationships", "Which cities play similar roles in a partnership network?",
    "Browser machine learning: graph features feed K-Means and Isolation Forest.",
    "The source project is remote. NetworkX graph measurements and scikit-learn fitting run locally in Pyodide.",
    "Adding connections to locations lets you explore patterns that a point map alone cannot reveal.",
    [("Connect", "G.add_edge(..., km=...)", "Represent partnerships as graph edges with distance weights."),
     ("Measure", "nx.betweenness_centrality(...)", "Summarize each node's degree, bridging role and connection distances."),
     ("Learn", "KMeans(n_clusters=4)", "Group similar graph profiles and identify unusual combinations."),
     ("Map", "point_collection(mapped)", "Return scores to cities with known coordinates, keeping missing records visible in the table.")],
    ["Many links means this city is most important?", "Only in this extracted partnership graph.", "I will check coverage and the meaning of each metric."],
    "Why can analysis include a city that the output map omits?",
    "Graph edges can identify the city while its coordinates are missing. Mapping requires that extra location match.", "network"),
"11": profile("From a fire shape to a scene shortlist", "Which satellite acquisitions should we inspect around a selected fire?",
    "Mixed workflow: learned fire outliers and acquisition groups, plus a hand-set scene ranking rule.",
    "Features, model fitting and ranking run in Pyodide; perimeters, STAC metadata and COG imagery come from remote services.",
    "The workflow connects a large-data discovery task to an inspectable case, reducing the scenes a person needs to examine first.",
    [("Measure", "fires.to_crs(5070)", "Describe historical fire area, perimeter, date and compactness."),
     ("Select", "IsolationForest(...)", "Flag unusual profiles, then choose a case using the explicit sorting rule."),
     ("Discover", "payload['bbox']", "Search Sentinel-2 near the case in a bounded date window."),
     ("Rank", "0.65 * cloud + 0.35 * time", "Use an understandable preference rule and inspect the candidate over the fire.")],
    ["Lowest cloud score means perfect fire imagery?", "The whole scene can be clear while the fire is cloudy.", "I will inspect the target before analyzing change."],
    "Which part is a learned model and which part is a chosen preference?",
    "Isolation Forest learns unusual profiles; the 65/35 cloud/time weights are human-set ranking preferences.", "triage"),
"12": profile("A question becomes a checked operation", "How can a copilot propose a spatial selection we can verify?",
    "Bounded AI handoff: the default plan is hand-authored; optional model requests run through a separate full-Python runner.",
    "Synthetic data, plan validation, filtering, linked charts and exports run in Pyodide. The default run sends no model request.",
    "Keeping the operation explicit makes a proposed answer testable against table values and mapped geometry.",
    [("Ask", "temperature >= 30", "Start with a question that names a field, unit and threshold."),
     ("Validate", "apply_plan(table, plan)", "Allow only defined fields and comparisons rather than executing generated Python."),
     ("Inspect", "selection_ids = set(selected.id)", "Link the same selected records to map outlines and charts."),
     ("Challenge", "update_threshold(threshold)", "Move a threshold and observe how sensitive the selection is to the question.")],
    ["The copilot says these cells are hot.", "Show the field, units, comparison and threshold.", "Now I can reproduce and challenge the selection."],
    "What would convince you that a live plan matches the hand-authored baseline?",
    "Validate the operation, recompute it and compare selected cell IDs, not just the wording of the answer.", "threshold"),
"13": profile("Measure change before explaining it", "How can an image explanation stay tied to reproducible evidence?",
    "Image-analysis foundation with optional vision-model interpretation; the default RGB threshold is a deterministic rule.",
    "Synthetic images, masks, area and error counts run in Pyodide. A separate optional runner can send the exported image and metrics to a model.",
    "Known synthetic truth makes mistakes visible before the method is transferred to real Earth imagery.",
    [("Compare", "distance = norm(after-before)", "Calculate a per-pixel RGB difference between aligned invented scenes."),
     ("Mask", "predicted = (distance > threshold) & valid", "Exclude the known synthetic cloud and apply an explicit threshold."),
     ("Evaluate", "iou = tp / (tp + fp + fn)", "Compare prediction with known change using error counts and overlap."),
     ("Explain", "evidence['detected_area_m2']", "Use computed area and a labeled figure to support, then check, an explanation.")],
    ["All bright changes must be new buildings!", "The cloud also changed appearance. Check the mask.", "I will measure errors before explaining causes."],
    "Why does excellent accuracy here not validate a real satellite model?",
    "The scene and cloud truth are deliberately easy and known. Real imagery adds misalignment, seasonality, sensor and labeling uncertainty.", "change"),
"14": profile("One surface, three useful views", "How do contours, profiles and 3D help us understand terrain?",
    "Spatial analysis with optional model interpretation: derivatives measure shape; no terrain-learning model is fitted here.",
    "The invented surface, slope and views are computed locally. Plotly and GeoLibre displays use their web rendering resources.",
    "A browser can make geometry and camera choices tangible, helping people question a terrain explanation before acting on it.",
    [("Construct", "x, y = np.meshgrid(axis_m, axis_m)", "Use local metre coordinates to define a known teaching surface."),
     ("Differentiate", "np.gradient(z, 100, 100)", "Calculate how elevation changes over distance, then express slope in degrees."),
     ("Link views", "z[profile_row]", "Trace a fixed cross-section through the same surface shown in contours and 3D."),
     ("Question", "scene.aspectratio.z", "Change vertical exaggeration and see why camera appearance is not a new measurement.")],
    ["The 4x mountain looks much more dangerous!", "Only the display scale changed; the slopes did not.", "I will read units and compare the profile."],
    "Can the highest cell have a gentler slope than a cell on the hillside?",
    "Yes. Elevation describes height; slope describes local change in height over distance.", "terrain"),
"15": profile("A bridge changes the reachable world", "How does one closure change access to a destination?",
    "Graph analysis plus optional bounded model tools; shortest paths are computed by an explicit algorithm.",
    "Network construction, shortest paths, coverage and tool replay run in Pyodide. Live model calls use the optional external runner.",
    "A small controlled network reveals how connectivity and assumptions affect an apparently simple access percentage.",
    [("Connect", "edges.append((a, b, 2.0))", "Represent travel possibilities as nodes, edges and minute costs."),
     ("Reroute", "shortest_times(closed=True)", "Remove one bridge and recompute routes to the same destination."),
     ("Compare", "routes['delay']", "Show who gains travel time and how a threshold changes covered-node counts."),
     ("Test", "routes[column] * 1.2", "Vary speed assumptions before asking an optional model to interpret computed evidence.")],
    ["The clinic is nearby, so everyone can reach it.", "A river and a closed bridge can force a long detour.", "I will measure network travel time, then consider people."],
    "Does 80% node coverage mean 80% population coverage?",
    "No. Node coverage treats nodes equally. Population coverage needs validated population allocation and a defined denominator.", "bridge"),
"16": profile("Keep the risk axes honest", "How can we explore the report's top ten clusters without mixing metrics?",
    "Evidence interpretation supporting GeoAI: this notebook visualizes existing SaTScan results and fits no new model.",
    "The small bundled PBIX derivative is read locally; Plotly shows bars, scenario bubbles and 3D points. GeoLibre maps representative city coordinates.",
    "Linked views help compare statistical risk, reported facilities and scenario indicators while exposing what additional evidence a decision needs.",
    [("Read", "pd.read_csv(...)", "Start with ten cluster-ranked report rows and documented city aggregates."),
     ("Compare", "sort_values('relative_risk')", "Display relative risk separately from original rank and facility counts."),
     ("Animate", "risk.melt(...)", "Compare A/B/C indicators as alternative scenarios, not as a forecast movie."),
     ("Interpret", "z=risk.relative_risk", "Read 3D height as relative risk; it is not terrain or floodwater depth.")],
    ["A taller point means deeper flooding?", "Here the z axis is a statistical relative risk.", "I will read the axes and check the source denominators."],
    "Why should the two facility/site counts not be interchanged?",
    "ALLMODELS cluster counts and supporting city-site aggregates use different selections; their denominators need separate interpretation.", "risk"),
"17": profile("More perspectives, accountable decisions", "How can people question a GeoAI result from several useful angles?",
    "Human interpretation and governance: Python formats prompts; it does not run autonomous hat agents.",
    "The bundled CSV and authored perspective table are processed locally with pandas and Markdown rendering.",
    "A repeatable question set helps connect computational results to evidence, lived experience, alternatives and a responsible next action.",
    [("Ground", "risk = pd.read_csv(...)", "Name the case and trace what the report actually contributes."),
     ("Question", "hats = pd.DataFrame(...)", "Use six perspectives plus the project's purple synthesis extension."),
     ("Discuss", "for r in hats.itertuples()", "Turn the table into a workshop agenda that invites disagreement."),
     ("Act", "display(Markdown(...))", "Assign who will verify a claim and what evidence would change the decision.")],
    ["Seven hats means seven AI experts agreed?", "These are authored questions for people to examine.", "We will preserve disagreement and choose a checked next step."],
    "What should purple synthesis do with a serious unresolved disagreement?",
    "Record the disagreement, its evidence and an owner for follow-up; synthesis should not erase it or invent consensus.", "hats"),
}

from ollama_learning_content import extend as _extend_ollama
_extend_ollama(LESSONS, PROFILES, step, profile, SETUP)
