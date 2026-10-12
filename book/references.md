# References and data-source register

## JupyterLite and GeoLibre platform introductions

The illustrated [JupyterLite](platforms/jupyterlite.md) and [GeoLibre](platforms/geolibre.md) chapters contain figure-level credits and official documentation links, checked **11 October 2026**. Their seven PNGs were extracted unchanged from **Tobias, J. L. (2026, July 10). *JupyterLite: Geospatial Data Science and Global Health* [Presentation]**, supplied as PPTX and PDF. Slides 11, 17 and 19 support the JupyterLite chapter; slides 38, 39, 41 and 42 support GeoLibre. The original presentation date is distinct from this book's update date.

The [asset provenance manifest](assets/platforms/provenance.json) records slide numbers, original PPTX members, hashes and source credits. The full presentation is not redistributed. The ecosystem graphic's separate creator/license is unspecified; it is identified as supplied artwork, not an original illustration made for this repository. Software licenses do not relicense the presentation, logos or third-party datasets.

- **JupyterLite:** JupyterLite Contributors; [documentation](https://jupyterlite.readthedocs.io/en/stable/) and [BSD 3-Clause notice](assets/platforms/JUPYTERLITE-LICENSE.txt).
- **Python runtime:** Pyodide contributors; [Pyodide documentation](https://pyodide.org/en/stable/).
- **GeoLibre:** Qiusheng Wu and contributors; [recommended citation and DOI guidance](platforms/geolibre.md), [upstream citation page](https://geolibre.app/citation/) and [MIT notice](assets/platforms/GEOLIBRE-LICENSE.txt).
- **Dependencies and map data:** [GeoLibre acknowledgements](https://geolibre.app/acknowledgements/); preserve the pictured OpenFreeMap, OpenMapTiles and OpenStreetMap credits, and each gallery project's authorship and data terms.

## Illustrated GeoAI and global-health guide

The seven [visual field-guide chapters](geoai/primer.md) cite sources next to the claims they support. Initial sources were consulted on **11 October 2026**; additions carry their own access dates below. Dates within historical reports remain their original dates. Potential health applications are the book's teaching proposals, not claims that these organizations have validated the notebooks.

- **GeoAI definition and research:** [USGS GeoAI for topographic mapping](https://www.usgs.gov/publications/geoai-us-geological-survey-topographic-mapping).
- **Industry perspective:** Esri. (n.d.). *[What is GeoAI?](https://www.esri.com/en-us/capabilities/geoai/overview)* Accessed 11 October 2026. The primer paraphrases selected ideas; its notebook comparisons and proposed evaluation question are this book's interpretation, not Esri findings or endorsement. No Esri media or text passages are reproduced.
- **Additional industry perspective:** Amazon Web Services. (n.d.). *[What Is Geospatial Artificial Intelligence?](https://aws.amazon.com/what-is/geospatial-artificial-intelligence/)* Accessed 12 October 2026. The {ref}`AWS perspective in the primer <aws-geoai-perspective>` is a brief attributed paraphrase. Notebook mappings, the browser comparison and the proposed health-program question are this book's interpretation, not AWS findings or endorsement. No AWS media or text passages are reproduced.
- **Spatial-intelligence definition:** Stanford Institute for Human-Centered Artificial Intelligence (Stanford HAI). (n.d.). *[What is Spatial Intelligence?](https://hai.stanford.edu/ai-definitions/what-is-spatial-intelligence)* Accessed 12 October 2026. The {ref}`spatial-intelligence introduction <spatial-intelligence>` paraphrases the glossary; its comparison with GIS, GeoAI and geospatial intelligence and its notebook examples are this book's interpretation. This is a separate source from the Zhang et al. policy brief below, and does not validate these notebooks as physical-world reasoning systems.
- **Health geography and governance:** [WHO GIS Centre](https://www.who.int/data/gis); [WHO ethics and governance of AI for health](https://www.who.int/publications/i/item/9789240029200).
- **Validation:** [scikit-learn cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html); [spatial cross-validation research](https://arxiv.org/abs/2303.07334).
- **HIV and TB evidence:** [CDC PEPFAR analysis, 2004–2022](https://www.cdc.gov/mmwr/volumes/72/wr/mm7212e1.htm); [UNAIDS data repository](https://adr.unaids.org/); [WHO TB data](https://www.who.int/teams/global-tuberculosis-programme/data).
- **Disease and response planning:** [GPEI microplanning](https://polioeradication.org/news/the-microplanning-puzzle-planning-for-an-effective-vaccination-campaign/); [WHO malaria subnational tailoring](https://www.who.int/publications/b/81075); [WHO Ebola contact tracing](https://www.who.int/publications/i/item/WHO-EVD-Guidance-Contact-15.1); [WHO HeRAMS](https://www.who.int/initiatives/herams).
- **Climate and environmental evidence:** [WHO climate and health](https://www.who.int/health-topics/climate-change); [WHO heat and health](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health); [NASA surface temperature](https://science.nasa.gov/earth/earth-observatory/global-maps/land-surface-temperature/); [NOAA coastal viewer](https://coast.noaa.gov/digitalcoast/tools/slr.html); [FEWS NET guidance](https://fews.net/products/guidance-documents); [NASA surface PM2.5 training announcement](https://forum.earthdata.nasa.gov/viewtopic.php?t=7992); [WHO drinking-water safety](https://www.who.int/teams/environment-climate-change-and-health/water-sanitation-and-health/water-safety-and-quality).
- **Vector and social pathways:** [WHO vector-borne diseases](https://www.who.int/en/news-room/fact-sheets/detail/vector-borne-diseases); [IPCC AR6 WGII Chapter 7](https://www.ipcc.ch/report/ar6/wg2/chapter/chapter-7/).

The 24 SVGs in `book/assets/geoai/` are original conceptual illustrations authored for this repository and generated by `scripts/build_geoai_primer.py`. They are not copied agency graphics, measured health estimates or model outputs. Each includes an embedded title and text description; each chapter provides explanatory text. The invented HIV cohort and score ranges must not be cited as program evidence. The supplied Six Thinking Hats artwork remains unchanged and is separately identified in the [decision chapter](geoai/climate-society.md) and lab 17.

The canonical data-source register for this project is [`DATA_SOURCES.md`](https://github.com/jltobias/JupyterLite-GeoLibre-GeoAI/blob/main/DATA_SOURCES.md).

(thinking-and-connection-books)=
## Books on thinking and human connection

These books provide conceptual context for human review and collaboration. They are not GeoAI software manuals or evidence that these notebooks improve health outcomes. Online descriptions and catalogue records were checked **12 October 2026**; no book passages or cover artwork are reproduced.

(six-thinking-hats-reference)=
### Edward de Bono — Six Thinking Hats

**de Bono, E. (2000). *Six Thinking Hats* (revised and updated edition). Penguin Books.** ISBN 9780140296662. [Requested Goodreads listing](https://www.goodreads.com/en/book/show/97030.Six_Thinking_Hats); [library catalogue record](https://search.worldcat.org/title/44652811); [official de Bono book overview](https://www.debono.com/book-six-thinking-hats). The date identifies the cited edition, not the origin of the method; Goodreads lists this paperback as published 31 October 2000.

The book is the conceptual reference for the {ref}`Six Thinking Hats infographic discussion <six-thinking-hats-infographic>`, the [decision workshop](geoai/climate-society.md) and lab 17. The [official summary](https://www.debono.com/_files/ugd/acf405_0ec0d7f959d7424fad5a9f9e9ec581e7.pdf) supports the explanation of shared thinking modes and blue process management. **Purple orchestration is an extension in the supplied artwork, not an original seventh de Bono hat.** The supplied image is not represented as an illustration from the book or as endorsed de Bono training material.

(rewire-reference)=
### Ethan Zuckerman — Rewire

**Zuckerman, E. (2013). *Rewire: Digital Cosmopolitans in the Age of Connection*. W. W. Norton & Company.** ISBN 9780393082838. [Requested Goodreads listing](https://www.goodreads.com/en/book/show/16233761-rewire); [author's book page](https://ethanzuckerman.com/books/rewire/); [publisher's record](https://wwnorton.co.uk/books/9780393082838-rewire). Publication details and the brief paraphrase were checked against the author and publisher; Goodreads restricted automated access during review.

The {ref}`Rewiring Global Health infographic discussion <rewiring-global-health-infographic>` connects the book's themes to questions about whose knowledge enters a GeoAI workflow. That application is our interpretation, not a method or result reported by Zuckerman. The wording attributed to him inside the supplied artwork **has not been verified as a verbatim quotation**; readers should use the attributed paraphrase and bibliographic reference instead.

**Rewiring infographic provenance:** James L. Tobias supplied the composite project artwork. It is copied unchanged from the [companion repository at revision 84bf945](https://github.com/jltobias/JupyterLite-Rewiring-Global-Health/blob/84bf945de91ad5ae3c8b2f67e9bd3e4781cf88b9/assets/rewiring-global-health.png); the [asset record](assets/rewiring/provenance.json) records its hash and rights caveats. It is not analytical data or evidence of measured health outcomes. Third-party elements retain their respective rights; neither the repository's software license nor this citation establishes a blanket media license.

## Presentation-informed future directions

- **Digital twins presentation:** *Digital Twins: Botswana Kopanyo TB Study (2012-2016) for Gaborone TB simulation*, 27 August 2026, supplied PDF, 22 pages. Cover credits James L. Tobias, Herman Tolentino and Tadesse Wuhib; also names Patrick Moonan and John Oeltmann (CDC Global TB Branch). The [chapter](futures/digital-twins.md) gives page-level context and distinguishes the separate notebook series from this repository.
- **Map encryption presentation:** *Map Encryption Democratized with JupyterLite*, cover date 21 September 2026, supplied PDF, 36 pages; export metadata dated 4 October 2026. Cover credits Herman Tolentino, James L. Tobias, Tadesse Wuhib and Vinit Mishra. The [chapter](futures/map-encryption.md) distinguishes encryption, masking, aggregation and access control.
- **Public technical/research context:** [NIST digital twins](https://www.nist.gov/digital-twins); [Starsim project](https://starsim.org/); Baker et al. (2023), [*Use of High-Resolution Geospatial and Genomic Data to Characterize Recent Tuberculosis Transmission, Botswana*, doi:10.3201/eid2905.220796](https://wwwnc.cdc.gov/eid/article/29/5/22-0796_article); [NIST SP 800-38D](https://csrc.nist.gov/pubs/sp/800/38/d/final); [W3C Web Cryptography security considerations](https://www.w3.org/TR/webcrypto/#security-considerations). Accessed 11 October 2026.

The [source register](assets/futures/provenance.json) identifies the exact supplied PDFs by SHA-256 and records PDF-versus-slide numbering. Four new SVGs in `assets/futures/` are original teaching illustrations generated by `scripts/build_future_chapters.py`. No source PDF, internal repository screenshot, patient-level data or cryptographic key is republished. Presentation concepts do not certify an implementation or imply endorsement.

## Local AI assistance and geospatial intelligence

- **GeoLibre native assistant:** Qiusheng Wu and contributors, [AI Assistant guide](https://geolibre.app/user-guide/ai-assistant/), [embedding guide](https://geolibre.app/user-guide/embedding/), and source revision [734c7963b57f508500c5745361a4afc52763671c](https://github.com/opengeos/GeoLibre/tree/734c7963b57f508500c5745361a4afc52763671c). The [advanced chapter](advanced/ollama-assistant.md) links the specific provider, field-definition and tool implementations used to check integration details. Software citation: Wu, Q. (2026), *GeoLibre*, [doi:10.5281/zenodo.20785400](https://doi.org/10.5281/zenodo.20785400).
- **Ollama:** [server configuration](https://docs.ollama.com/faq), [list-model API](https://docs.ollama.com/api/tags), [chat API](https://docs.ollama.com/api/chat), [structured outputs](https://docs.ollama.com/capabilities/structured-outputs) and [tool calling](https://docs.ollama.com/capabilities/tool-calling). **Qwen:** [qwen3:4b model card and Apache 2.0 license](https://ollama.com/library/qwen3:4b). Model weights are not redistributed by this repository.
- **Global Nature Watch / Land & Carbon Lab:** [Horizon experimental interface and overview](https://horizon.globalnaturewatch.org/). Credited as interaction inspiration only; no code, screenshots, agents or dataset outputs are copied.
- **Chrome Developers:** Thompson, C. (2025), [*New permission prompt for Local Network Access*](https://developer.chrome.com/blog/local-network-access). Browser permission and Ollama's allowed origins are separate checks.
- **Stanford HAI:** Zhang, D., Wald, R., Adeli, E., Cryst, E., Ho, D. E., Meinhardt, C., Wu, J., Zegart, A., & Li, F. (2026, July 27). [*The World Model and Spatial Intelligence Era: Governing AI Beyond Language*](https://hai.stanford.edu/policy/the-world-model-and-spatial-intelligence-era-governing-ai-beyond-language). Paraphrased in the GeoAI primer; the GIS → GeoAI → accountable geospatial intelligence diagram is this book's synthesis, not the authors' diagram or an endorsement.

Sources accessed 11 October 2026. Three SVGs in `assets/assistant/` and the lab 18–20 storyboards are original teaching schematics. The supplied Six-Thinking-Hats-GPT graphic is reused unchanged with the existing provenance caveat: its original designer/generation process has not been independently verified, and purple orchestration is the artwork's extension. The authored review card does not instantiate multiple AI agents.

## Software

The [STAC discovery chapter](platforms/stac-discovery.md) connects the [JupyterLite STAC Browser companion](https://github.com/jltobias/JupyterLite-STAC-Browser), credited to its contributors in [CITATION.cff](https://github.com/jltobias/JupyterLite-STAC-Browser/blob/563ed599a42188a4b476cfec44173e97fa06e3cc/CITATION.cff), with [STAC](https://stacspec.org/en/about/stac-spec/), [Item Search](https://github.com/radiantearth/stac-api-spec/blob/main/item-search/README.md) and the separate [upstream STAC Browser](https://github.com/radiantearth/stac-browser). Companion revision reviewed: `563ed599a42188a4b476cfec44173e97fa06e3cc`, 11 October 2026. Two original diagrams/cartoons live in `assets/discovery/`; no companion client code or provider imagery is copied.

- **GeoLibre** — open-source, browser/desktop/Jupyter GIS: https://geolibre.app/ and https://github.com/opengeos/GeoLibre
- **GeoAI** — Wu, Q. (2026). *GeoAI: A Python package for integrating artificial intelligence with geospatial data analysis and visualization.* Journal of Open Source Software, 11(118), 9605. https://doi.org/10.21105/joss.09605
- **JupyterLite** — https://jupyterlite.readthedocs.io/
- **H3** — https://h3geo.org/
- **GPT-6 Astra** — [model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra), [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [image inputs](https://developers.openai.com/api/docs/guides/images-vision), [function calling](https://developers.openai.com/api/docs/guides/function-calling). Examples checked 2026-10-02; API access is optional.
- **Matplotlib / Plotly** — https://matplotlib.org/stable/ and https://plotly.com/python/. Static charts and interactive 3D surfaces complement native GeoLibre maps.

## Data

**Historical cholera demonstration:** PHI-Case-Studies contributors, [*Jupyterlite-1854-Cholera-Basic*, revision 476f6dd](https://github.com/PHI-Case-Studies/Jupyterlite-1854-Cholera-Basic/tree/476f6dd5a8430e6eb823e79614fda1d7e12a78fb). Unchanged CSVs, upstream GPL-3.0 notice and checksum manifest accompany notebook 21. The [five-minute walkthrough](presentations/cholera-five-minutes.md) is a new extension, not a reproduction of upstream notebook code or of Snow's reasoning. Method: [scikit-learn DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html). Historical context: CDC (2004), [*150th Anniversary of John Snow and the Pump Handle*](https://www.cdc.gov/Mmwr/preview/mmwrhtml/mm5334a1.htm). Sources accessed 11 October 2026. Newly generated maps show exploratory recorded-location groups, not disease risk or causal attribution.

See the per-notebook citation cells and `DATA_SOURCES.md` for WorldPop, Census/TIGERweb, Major TOM, Sentinel-2, Copernicus DEM, ESA WorldCover, CHIRPS, USGS earthquake feeds, Source Cooperative, and OpenStreetMap attribution.

Labs 12–15 use synthetic teaching fixtures authored in the repository. The additional rainfall series in lab 04 is also synthetic and is not extracted CHIRPS data. Model plans and tool arguments shown in the default runs are hand-authored examples, not captured Astra responses. Real-data transfer exercises specify the metadata and validation needed before substituting observations.
