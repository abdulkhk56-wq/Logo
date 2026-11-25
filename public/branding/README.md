# SAFI brand assets

Open `brand-guide.html` for the full guidelines.

## Logo
- **Symbol:** a gas flame with a tall main tongue and a shorter second tongue, drawn in three flat layers (outer flame, body, core). There are no gradients. In one colour, the core is cut out of the outer flame.
- **Wordmark:** Archivo SemiExpanded (SIL OFL, width 112, weight 640), outlined and letterspaced. Never retype it.

## Files
| File | Use |
|---|---|
| `safi-logo-primary.svg` / `-primary-dark.svg` | Primary logo, light / navy grounds |
| `safi-logo-stacked.svg` / `-stacked-dark.svg` | Centred and square formats |
| `safi-logo-mono-black/white/navy.svg` | One-colour logo |
| `safi-symbol.svg`, `safi-symbol-mono-*.svg` | Symbol alone |
| `safi-wordmark(-white/-black).svg` | Wordmark alone |
| `safi-app-icon(-light/-ios/-maskable).svg` | App icons (1024 grid) |
| `safi-favicon.svg`, `png/` | Favicon and PNG exports |
| `site.webmanifest`, `safi-colors.css`, `safi-tokens.json` | Manifest and tokens |

## Colour
| Name | Hex | Use |
|---|---|---|
| SAFI Navy | `#0E2236` | Wordmark, text, brand surfaces |
| Flame Red | `#D63A1A` | Outer flame |
| Flame Orange | `#EE7420` | Flame body; the one accent colour in layouts |
| Flame Yellow | `#F8B320` | Flame core (symbol only) |
| Steel | `#5B6B78` | Secondary text |
| Mist | `#E8ECEF` | Panels |

On control-room screens, flame colours appear only inside the logo, because orange often signals an alarm.

## Usage
Clear space: half the flame width on every side. Minimum size: lockup 96px / 25mm wide; symbol 16px.

## HTML head
```html
<link rel="icon" href="/branding/safi-favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/branding/png/apple-touch-icon-180.png">
<link rel="manifest" href="/branding/site.webmanifest">
<meta name="theme-color" content="#0E2236">
```

## Rebuild
`pip install fonttools && python3 tools/build.py && node tools/export_png.js && python3 tools/guide.py`
