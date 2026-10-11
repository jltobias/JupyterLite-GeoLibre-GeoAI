# Ollama learning extension: verification scope

Checked 11 October 2026. These results concern teaching software, not a clinical, climate or security validation.

## Reproducible checks

- 51 unit tests cover existing lessons plus plan types/ranges, strict JSON, local-only URLs, missing/remote models, no silent fixture fallback, approval, deterministic feature counts, map project structure, attribution, graphics and Book links that also work from Lite.
- All 21 notebooks pass schema/syntax validation. Offline labs 12–20 execute in ordinary Python; labs 18–20 save static figures and labeled fixture outputs without contacting Ollama. The earlier labs' committed outputs are preserved.
- Every notebook has matching Book/Lite sources and code guides. Labs 18–20 add 14 guides, three original infographics, three cartoons and three 32-second captioned storyboards. These videos are not recordings of a live assistant session.
- `scripts/build_ollama_lessons.py --check` verifies authored lessons and the public twelve-cell project; `scripts/build_assistant_visuals.py --check` verifies three original chapter diagrams.
- `scripts/check_ollama_pyodide.py` ran the real browser/Pyodide HTTP branch with intercepted **mock** Ollama responses and an aborted Fetch request. It verified the seven-cell selection and a truthful failed-connection diagnostic under Python **3.12.7 and 3.14.2** (Pyodide 0.27.6 and 314.0.6). The test supports both classic `.js` and modern `.mjs` loaders; the latter corrected a CI-only loader mismatch. This validates the helper's browser runtime path, not access to the user's model from the published origin. No browser protections are disabled by this test.

## Live local inference

With the user's approval, `qwen3:4b` was installed from Ollama's official registry. A local API smoke test on Ollama **0.40.2** used model digest `359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7`.

| Request | Returned settings | Independently computed count |
|---|---|---|
| Select synthetic heat proxy >=39, orange, 45° | Requested layer, cutoff 39, orange, pitch 45 | 7 |
| Keep layer/color, raise cutoff to 41, flatten | Same layer/color, cutoff 41, pitch 0 | 4 |

Both exact-plan checks passed at 21:25 UTC. The counts come from Python, not model assertions. This is two controlled examples, not an accuracy benchmark or a guarantee for other prompts/models. Reproduce deliberately with `python scripts/check_ollama_local.py --live`; it does not download models, change settings or restart services.

## Browser/native limits at this checkpoint

The saved Windows origin setting was present, but the running server had not reloaded it: requests with either published origin returned HTTP 403. The local listener remained `127.0.0.1:11434`. This does not invalidate the direct local inference result; it prevents claiming that the published pages can yet reach that service.

No connected interactive browser was available to complete GeoLibre's **native** assistant UI test. The native workflow is grounded in the upstream guide and source at revision `734c7963b57f508500c5745361a4afc52763671c`, and lab 18 supplies explicit manual acceptance checks. A native conversation, tool transcript, map change and Undo must still be observed on the intended browser/model before calling that path end-to-end verified.

A working terminal API, mocked viewer protocol or offline notebook execution does not establish native GeoLibre interoperability, browser permissions, full offline operation or suitability for sensitive data. No security protections were disabled, wildcard origins added, network binding broadened or hosted-model credentials configured.

## Build and publishing

The strict Book build and Lite build passed. `check_site_alignment.py` matched **21 Book notebook sources and 190 Lite content files**. `check_visual_browser.py` passed the 21 resource routes, new chapter diagrams, desktop/mobile layout, existing analytical chart interactions and guarded map-message delivery. Those map-message tests use a controlled viewer, not native GeoLibre.

`check_learning_browser.py` checks graphic text bounds, video playback/seeking, captions and mobile layout. GitHub Actions repeats offline execution and media/layout/runtime checks; it cannot access a learner's desktop Ollama. Model-dependent tests remain opt-in and are not substituted for deterministic CI.
