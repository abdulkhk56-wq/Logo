# SAFI symbol, round 2: black-and-white concepts

Open `index.html` for the full presentation: construction, black-and-white logo, meaning, standalone symbol, wordmark lockup and pixel test for each concept, followed by the evaluation and recommendation.

Every mark is built on a 120 × 120 artboard with a 6-unit module, from circles and straight lines only. The SVGs contain only `A` (circular arc) and `L` commands. Each arc is a circle from the construction drawing.

| Folder | Concept |
|---|---|
| `01-tandem/` | Flame split by one constant-width arc channel |
| `02-laminar/` | Flame read through three equal plates (recommended) |
| `03-gate/` | Flame as the counter of a solid block |

Each folder contains `construction.svg`, `symbol-black.svg`, `symbol-white.svg`, `lockup-black.svg`, `lockup-white.svg`, `app-icon.svg` and `pixel-test/` (true-size rasters at 16, 24, 32 and 48px).

`wordmark-provisional.svg` is the same in every lockup. Final typography, colour and the full identity come after a symbol is approved. Laminar was selected; the final colour identity is in `/public/branding/`.

Rebuild: `python3 tools/v2/build_v2.py && node tools/v2/pixel_test.js && python3 tools/v2/present.py`
