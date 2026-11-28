# SAFI | صافي brand assets

Open `brand-guide.html` for the full guidelines.

## Idea
In Arabic, «صافي» means pure, clear, filtered: what SAFI does to a control room's alarm flood. The symbol is the letter «ص», the name's first letter, reversed out of a navy tile. The name is always shown in both scripts, set from one family (Readex Pro, SIL OFL), outlined so no font is needed.

## Files
| File | Use |
|---|---|
| `safi-logo-primary.svg` / `-primary-dark.svg` | Bilingual logo (default), light / navy grounds |
| `safi-logo-latin(-dark).svg` | English-only logo |
| `safi-logo-arabic(-dark).svg` | Arabic-only logo |
| `safi-logo-stacked(-dark).svg` | Centred and square formats |
| `safi-logo-mono-black.svg`, `-mono-white.svg` | One-colour logo (the letter is cut out of the tile) |
| `safi-symbol.svg`, `-dark`, `-gold`, `-mono-*` | Symbol tile |
| `safi-symbol-letter.svg` | The letter alone |
| `safi-wordmark(-arabic)(-white/-black).svg` | Wordmarks alone |
| `safi-app-icon(-ios/-maskable).svg`, `safi-favicon.svg`, `png/` | Icons and PNG exports |
| `site.webmanifest`, `safi-colors.css`, `safi-tokens.json` | Manifest and tokens |

## Colour
| Name | Hex | Use |
|---|---|---|
| SAFI Navy | `#0B2A3C` | Tile, wordmarks, text |
| Gold | `#C49A4A` | Divider rules, small highlights only |
| White | `#FFFFFF` | Ground |
| Deep Navy | `#071C29` | Dark interface ground |
| Steel | `#5E6E7A` | Secondary text |
| Mist | `#E9EDF0` | Panels |

## Usage
Clear space: half the tile width on every side. Minimum size: bilingual logo 140px / 35mm wide; single-script logo 90px; symbol 16px.

## HTML head
```html
<link rel="icon" href="/branding/safi-favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/branding/png/apple-touch-icon-180.png">
<link rel="manifest" href="/branding/site.webmanifest">
<meta name="theme-color" content="#0B2A3C">
```

## Rebuild
`pip install fonttools uharfbuzz && python3 tools/build.py && node tools/export_png.js && python3 tools/guide.py`
