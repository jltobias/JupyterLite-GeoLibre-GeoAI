# Repository visual-content and alignment review

Reviewed 11 October 2026 against baseline `4cbcb9628f282e5171c02529be3be60f4714cd00`. Scope: all 18 canonical notebooks, helpers, Book chapters, README, visual assets, generation scripts, tests and deployment. Independent adversarial, edge-case, verification-gap and structure passes were followed by a dependent prose pass. This is a bounded repository review, not a certification of every external service or health/scientific claim.

Before edits, all 18 deployed Book notebook downloads and all 18 Lite notebooks were byte-identical to their repository sources. The gaps were navigation, saved analytical outputs, rendering safeguards and validation—not divergent notebook copies. All 18 existing 32-second videos passed real playback, seeking, caption and mobile-layout checks. The editorial pass examined 14,841 baseline words across 12 documents; no length target was imposed.

The [machine-readable findings](REPO_REVIEW.json) preserve all 35 findings/recommendations. Overlaps between independent lenses are retained as corroborating signals, not removed. Locations below refer to the baseline; line numbers may have moved. Dispositions describe this update.

## Remaining work and evidence boundaries

- The PBIX derivative still needs an exact extraction recipe and verified A/B/C definitions, source dates, joins and denominators. Charts reproduce the committed CSV, not a newly verified extraction. Do not treat the subset as a worldwide top-ten risk ranking.
- A true observed time-series map, modeled 2D/3D inundation and a coordinated standalone story-map application need additional work and appropriate evidence. Current scenario frames are not dates or water depths.
- Labs 08–11 still need execution for their analytical results. Lab 09 could receive a deterministic saved-result path in a subsequent change.
- Media and notebook cross-site links target production; forks/local previews need configurable deployment routing.
- Tests now cover the widget message contract, but that controlled harness does not certify the hosted GeoLibre service, every CORS endpoint or all notebooks in Pyodide. Saved-output presence is checked; full semantic freshness checking of every saved result remains open.

## Verification for this update

See the deployment workflow and scripts for reproducible checks: unit tests; all notebook schemas/syntax; isolated execution of labs 12–17; generated media/navigation and presentation provenance; strict Book build; Book/Lite byte alignment; browser video/caption checks; scenario selection and 3D chart interaction; map-message origin/source guards. The deployment must complete successfully before treating the new live links as published.

The follow-up request also adds two presentation-informed chapters on digital twins and map encryption, with four original diagrams/cartoons, cover-author credits, page references and source hashes. These are educational discussions, not implementations of the separate projects. Their mobile layouts and image alternatives are checked. The combined local suite passes 35 tests; all 18 videos pass playback, seeking and caption checks. Browser checks exercise scenario A/B/C selection and 3D camera movement using both the CDN and the installed Plotly bundle.

## adversarial

### book/notebooks/10_sister_cities_graph_geoai.ipynb:340

- Trigger: Point styles use unsupported pointColor/pointRadius/pointOpacity names.
- Guard: Use fillColor/circleRadius/fillOpacity; test project styles.
- Consequence: Groups and outliers lose their intended distinctions.
- Disposition: Fixed in lab 10; lab 16 radius also corrected.

### book/notebooks/05_h3_earthquake_geoai.ipynb:443

- Trigger: H3 cells crossing ±180 are emitted as unsplit polygons.
- Guard: Cut small non-polar rings at the antimeridian; preserve feature properties.
- Consequence: Small cells can draw as world-spanning bands.
- Disposition: Fixed with tested geometry helper; pole-enclosing rings fail explicitly.

### book/_config.yml:6; notebooks 08–11, 16–17

- Trigger: Book execution is off and these chapters have no saved analytical outputs.
- Guard: Save representative results and distinguish live-only views.
- Consequence: Readable chapters omit their computed results.
- Disposition: Partly fixed: 16–17 now have saved results; 08–11 remain run-required.

### scripts/validate_notebooks.py:39

- Trigger: Execution gate excludes nonsynthetic bundled-data lessons.
- Guard: Allowlist bundled labs and copy their data into temporary execution directories.
- Consequence: Report calculations/rendering regress without detection.
- Disposition: Fixed for 16–17; deterministic lab 09 execution remains a follow-up.

### DATA_SOURCES.md:167

- Trigger: PBIX derivative lacks extraction recipe, join keys, scenario definitions and transformation provenance.
- Guard: Obtain and document the exact derivation and field dictionary.
- Consequence: CSV charts reproduce but the derivative and scenario interpretation cannot be independently reconstructed.
- Disposition: Open evidence requirement; definitions are now visibly marked unverified.

### README.md — notebook galleries

- Trigger: Only Launch links are provided per notebook.
- Guard: Provide Read/Run/Watch/Infographic/Cartoon links and visual-type guidance.
- Consequence: Existing visual resources are hard to discover.
- Disposition: Fixed with generated directory and visual preview.

### Notebook citation cells

- Trigger: Most standalone notebooks omit the creator and GeoLibre DOI.
- Guard: Include Qiusheng Wu, DOI, license/source and pinned builder version in every downloadable notebook.
- Consequence: Downloaded lessons lose the site's attribution.
- Disposition: Fixed in all 18 notebooks.

### scripts/build_learning_media.py:278

- Trigger: Generated links hardcode the production hostname.
- Guard: Support a configurable base and same-deployment routing.
- Consequence: Local builds and forks can open a different deployment/revision.
- Disposition: Open portability improvement; current production links are intentional and checked.

### book/notebooks/13_astra_vision_change.ipynb:266

- Trigger: Confusion counts are only rendered inside an image.
- Guard: Provide the counts as an HTML/plain-text table and improve analytical image alternatives.
- Consequence: Screen-reader users cannot recover the numerical evidence.
- Disposition: Partly fixed: accessible confusion table added; richer figure alternatives remain useful.

### book/notebooks/geolibre_lite.py:32

- Trigger: Map iframe has no accessible name.
- Guard: Set a descriptive iframe title.
- Consequence: Assistive technology cannot identify the map frame.
- Disposition: Fixed.

### README.md:49; notebook 17 linked-view discussion

- Trigger: Independent views are described as a story map or linked-view experience.
- Guard: Describe a narrative notebook or implement shared selection/story navigation.
- Consequence: Learners expect coordinated interactions or an exported story application.
- Disposition: Fixed labels; coordinated standalone story-map app remains future work.

## edge-case-hunter

### book/notebooks/10_sister_cities_graph_geoai.ipynb:340–343

- Trigger: Role and anomaly rendering uses ignored style keys.
- Guard: Use fillColor, circleRadius and fillOpacity.
- Consequence: Categorical colors and emphasis disappear.
- Disposition: Fixed; overlaps adversarial style finding.

### book/_config.yml:6; scripts/validate_notebooks.py:39

- Trigger: Read-only chapters have empty outputs.
- Guard: Preserve results and assert required saved figures/tables.
- Consequence: Book omits the promised analytical views.
- Disposition: Partly fixed for 16–17; saved-output presence guards added for 12–17.

### scripts/build_learning_media.py:278–290

- Trigger: Opening a local build or fork follows production links.
- Guard: Make the deployment base configurable.
- Consequence: Reader leaves the current revision.
- Disposition: Open; overlaps adversarial portability finding.

### book/notebooks/08_stac_geoai_footprints.ipynb:188

- Trigger: A STAC bbox has six coordinates including elevation.
- Guard: Use horizontal_bbox to select horizontal axes and validate bounds.
- Consequence: Elevation contaminates width/height clustering features.
- Disposition: Fixed with 2D/3D/date-line regression fixtures.

### book/notebooks/11_wildfire_stac_triage.ipynb:333–337

- Trigger: Discovery timestamps have UTC offsets while acquisitions are made naive.
- Guard: Normalize both dates to UTC before subtraction.
- Consequence: TypeError stops scene ranking.
- Disposition: Fixed.

### book/notebooks/05_h3_earthquake_geoai.ipynb:217

- Trigger: Earthquake feed has no records.
- Guard: Stop with an explicit empty-feed message before constructing columns.
- Consequence: AttributeError hides the actual empty-data condition.
- Disposition: Fixed.

### book/notebooks/geolibre_lite.py:235

- Trigger: GeoJSON feature has properties:null.
- Guard: Use (feature.get('properties') or {}).get(column).
- Consequence: One empty property object prevents the choropleth.
- Disposition: Fixed with builder regression test.

### book/notebooks/cognition.py:40

- Trigger: cell_m is NaN or infinity.
- Guard: Require a finite positive grid size.
- Consequence: Invalid geometry reaches JSON export or display.
- Disposition: Fixed with regression tests.

### book/notebooks/geolibre_lite.py:32

- Trigger: Screen reader enters unnamed iframe.
- Guard: Give the map frame a descriptive title.
- Consequence: Map purpose is unavailable.
- Disposition: Fixed; overlaps adversarial accessibility finding.

### DATA_SOURCES.md:167–171

- Trigger: Attempting to reconstruct or interpret PBIX aggregates.
- Guard: Record exact transformation, keys, denominators and scenario definitions.
- Consequence: Derivative provenance cannot be verified.
- Disposition: Open evidence requirement; overlaps adversarial provenance finding.

## verification-gap

### book/notebooks/geolibre_lite.py:55

- Trigger: Project message delivery breaks while Python dictionaries still pass tests.
- Guard: Test frontend ready/load/update handling, origin/source guards and disposal.
- Consequence: Maps and elevation scenes can stop displaying data.
- Verification evidence: Replacing geolibre:load-project with an invalid name passed the baseline Python camera test; existing browser scripts did not exercise the widget.
- Consumer / gap: Lab 14 terrain_map display; regression-gap.
- Disposition: Fixed protocol harness; upstream service and full Pyodide E2E remain separate checks.

### scripts/validate_notebooks.py:39

- Trigger: Bundled CSV schema changes outside the synthetic execution gate.
- Guard: Execute 16–17 with their CSV and inspect frame/city identities and 3D risk values.
- Consequence: Report animation or discussion notebook breaks despite schema-only validation.
- Verification evidence: Removing flood_c_mean caused a KeyError; baseline execution copied only Python helpers and skipped both labs.
- Consumer / gap: Lab 16 risk.melt and lab 17 CSV read; broken-verification-gap.
- Disposition: Fixed.

### scripts/validate_notebooks.py:54

- Trigger: Committed outputs are missing or stale while new test outputs are discarded.
- Guard: Guard saved results and test the rendered analytical views.
- Consequence: Readable Book omits results available after execution.
- Verification evidence: Clearing lab 14 outputs still passed baseline schema/guide checks; lab 16 had no outputs.
- Consumer / gap: Book with execute_notebooks off; regression-gap.
- Disposition: Partly fixed: presence and browser checks; full deterministic output freshness hashing remains open.

### tests/test_learning_content.py:70

- Trigger: MP4 container markers survive a truncated, undecodable video.
- Guard: Run real playback, seeking and caption checks in deployment.
- Consequence: Unplayable media can publish.
- Verification evidence: Truncating the lab 16 MP4 preserved the baseline ftyp/moov assertions but decoding failed.
- Consumer / gap: Generated watch.html video players; broken-verification-gap.
- Disposition: Fixed: all-18 browser media check added to CI.

## structure

| Pass | Original text / location | Revised text | Changes |
|---|---|---|---|
| structure | README galleries: Two launch-only galleries | One generated Read/Run/Watch/Infographic/Cartoon directory | Applied; adds direct visual discovery. |
| structure | README / Book intro: Labs 12–17 grouped as Astra/synthetic | 12–15 synthetic optional-model labs; 16 report interpretation; 17 discussion | Applied; scope clarified. |
| structure | Book lab 16: No saved analytical results | Saved tables and static counterparts beside interactive results | Applied; results readable without a kernel. |
| structure | book/geoai/primer.md: Esri section before foundational geographic concepts | Move Esri comparison after place and method explanations | Applied; 0 words cut from attributed section. |
| structure | GeoLibre attribution / learning guide: Creator and figure credits; repeated interpretation guidance | Preserve contextual repetitions | Preserved; 376 words identified for retention. |

## prose

| Pass | Original text / location | Revised text | Changes |
|---|---|---|---|
| prose | book/intro.md:3: Each chapter can be launched | Each notebook chapter can be launched | Applied; conceptual chapters are not runnable notebooks. |
| prose | README.md external-model instructions: Run All makes no model calls | Run All makes no external model API calls | Applied; scoped to labs 12–15. |
| prose | README / book/geoai/climate-health.md: Story map and 3D columns | Narrative notebook and 3D points encoding reported relative risk | Applied; matches actual outputs. |
| prose | book/intro.md:60: Question → validated plan → mapped selection | Question → plan checked for allowed operations → mapped selection | Original gallery removed; no unsupported validation claim retained there. |
| prose | book/geoai/notebook-atlas.md:15: Learn seasonality and aggregation | Learn daily variability and rolling totals | Applied; 30 invented daily values are not seasonal evidence. |
