# SAFI brand assets

Open `brand-guide.html` for the full guidelines: concept, exploration, logo suite, app icons, colour and usage rules.

## The mark: Tandem Flame

A two-tongued flame split by one constant-width S-channel into an outer blade (the process) and an inner blade (the operator), standing on a flat, level base. It combines energy (the flame), filtration (the channel that takes the noise out), control and stability (the level base and the containment), and the letter S.

## Files

| File | Use |
|---|---|
| `safi-logo-primary.svg` | Primary logo (symbol + wordmark), light backgrounds |
| `safi-logo-primary-dark.svg` | Primary logo, dark backgrounds |
| `safi-logo-stacked.svg`, `safi-logo-stacked-dark.svg` | Stacked lockup for square formats and splash screens |
| `safi-logo-mono-black.svg`, `safi-logo-mono-white.svg` | Single-colour lockups |
| `safi-symbol.svg` | Secondary logo: symbol only (Flare). Also `-ivory`, `-graphite`, `-mono-black`, `-mono-white` |
| `safi-wordmark.svg` | Wordmark only (Graphite). Also `-ivory`, `-mono-black`, `-mono-white` |
| `safi-app-icon.svg` | App icon, rounded square, 1024 grid. Also `-light`, `-mono` |
| `safi-app-icon-ios.svg`, `safi-app-icon-maskable.svg` | Full-bleed squares for OS-applied masks (iOS, Android adaptive, PWA maskable) |
| `safi-favicon.svg` | Browser favicon |
| `png/` | Raster exports for platforms that require them |
| `site.webmanifest` | PWA manifest wired to the icons |
| `safi-colors.css`, `safi-tokens.json` | Colour tokens |
| `exploration/` | The four explored concepts |

All logo SVGs are outlined vector paths with transparent backgrounds (app icons excepted). They contain no fonts, images, masks or gradients.

## Colour

| Token | Hex | Role |
|---|---|---|
| Graphite | `#16191D` | Primary dark: wordmark, UI chrome, icon field |
| Flare | `#E0782A` | Signature accent: the symbol and brand moments |
| Ivory | `#F4EFE6` | Light surface; wordmark on dark |
| Petroleum | `#14403D` | Secondary: stable / in-limits states |
| Steel | `#8A9199` | Neutral |
| Ember | `#A34C16` | Flare at text size (5.1:1 on Ivory) |

In operator HMI screens (ISA-101 style), amber often carries alarm meaning. Keep Flare to the logo and splash screens there, and use Graphite, Steel and Petroleum as interface accents.

## Usage

- Clear space: one quarter of the symbol height on every side.
- Minimum size: lockup 96px wide; symbol 16px.
- Don't stretch, rotate, recolour, add effects, or retype the wordmark in a font.

## HTML head snippet

```html
<link rel="icon" href="/branding/safi-favicon.svg" type="image/svg+xml">
<link rel="icon" href="/branding/png/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/branding/png/apple-touch-icon-180.png">
<link rel="manifest" href="/branding/site.webmanifest">
<meta name="theme-color" content="#16191D">
```

## Rebuilding

The marks are generated from the construction scripts in `/tools`:

```sh
pip install shapely numpy
python3 tools/build.py          # SVG assets, tokens, concepts
node tools/export-png.js        # PNG exports (Playwright)
python3 tools/guide.py          # brand-guide.html
```
