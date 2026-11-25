# SAFI brand assets

Open `brand-guide.html` for the full guidelines.

## Symbol: Laminar

A flame constructed with compass and straight-edge, then read through three equal vertical plates. Only the outline that survives the plates is kept. The plates stand for filtration and control, and the centre plate in Flare is the energy at the core. The development round and construction drawings are in `concepts/`.

Geometry: 120-unit artboard, 6-unit module, plates 24, gaps 12, six construction circles. Every SVG path is circular arcs and straight lines only.

## Files

| File | Use |
|---|---|
| `safi-logo-primary.svg` | Primary logo, light grounds |
| `safi-logo-primary-dark.svg` | Primary logo, navy / dark grounds |
| `safi-logo-stacked.svg`, `-stacked-dark.svg` | Centred and square formats |
| `safi-logo-mono-black.svg`, `-mono-white.svg`, `-mono-navy.svg` | One-colour reproduction |
| `safi-symbol.svg`, `-dark`, `-mono-black`, `-mono-white` | Symbol alone |
| `safi-symbol-small.svg` | Small-size cut (gaps opened to 16), for 24px and below |
| `safi-wordmark.svg`, `-white`, `-black` | Wordmark alone (custom-drawn; never retype it) |
| `safi-app-icon.svg`, `-light`, `-ios`, `-maskable` | App icons, 1024 grid |
| `safi-favicon.svg`, `png/` | Favicon and raster exports |
| `site.webmanifest` | PWA manifest |
| `safi-colors.css`, `safi-tokens.json` | Tokens |

## Colour

| Name | Hex | Role |
|---|---|---|
| SAFI Navy | `#0F2A3D` | Primary: plates, wordmark, brand surfaces |
| Flare | `#DD5A1E` | The centre plate; at most one highlight per layout |
| White | `#FFFFFF` | Primary ground |
| Deep Navy | `#0A1E2C` | Dark interface ground |
| Steel | `#5B6B78` | Secondary text, rules |
| Mist | `#E8ECEF` | Panels, fills |

On control-room screens (ISA-101), orange often signals an alarm. Use Flare there only inside the logo.

## Typography

Barlow (SIL OFL) for headlines and text, Barlow Semi Condensed for data and labels.

## Usage

- Clear space: one plate width (24 of the symbol's 96 units) on every side.
- Minimum size: lockup 100px / 25mm wide; symbol 16px / 5mm tall. Use `safi-symbol-small.svg` at 24px and below.
- Don't stretch, recolour plates, move the Flare, add effects, or place the colour logo on Flare or busy grounds.

## HTML head

```html
<link rel="icon" href="/branding/safi-favicon.svg" type="image/svg+xml">
<link rel="icon" href="/branding/png/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/branding/png/apple-touch-icon-180.png">
<link rel="manifest" href="/branding/site.webmanifest">
<meta name="theme-color" content="#0F2A3D">
```

## Rebuild

```sh
pip install shapely numpy
python3 tools/v2/identity.py && node tools/v2/export_png.js && python3 tools/v2/guide_final.py
```
