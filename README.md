# Yale Landing — 2500 Yale Blvd SE, Albuquerque

Website for Yale Landing, a food and drink destination near the Albuquerque International Sunport.
Static HTML and CSS. No framework, no dependencies beyond Pillow for the build script.

**Live site:** _add the URL once Pages is enabled_

## Tenants

| Business | Type | Page |
|---|---|---|
| Perico's Tacos & Burritos | Mexican / New Mexican | `pericos.html` |
| Paletería Cuauhtémoc | Paletas, ice cream, aguas frescas | `paleteria-cuauhtemoc.html` |
| FMV Brewing Co. | Brewery, taproom, coffee | `fmv-brewing.html` |
| The Suite Haus | Salon — opening soon | listed on the homepage |

## Layout

```
docs/          ← published by GitHub Pages. Generated — never edit by hand.
src/           ← the four pages. Edit these.
assets/        ← css, js, images. Edit these.
build.py       ← regenerates everything below from src/ + assets/
*.html         ← self-contained copies, for emailing a single page
yale-preview.html  ← all four pages in one file, for review
```

## Build

```bash
python3 build.py --base-url https://yourdomain.com/
```

Normalizes the images, then generates the self-contained pages, the preview file, and `docs/`.

## Editing

1. Change something in `src/` or `assets/`
2. Run the build
3. Commit and push

Full instructions in [DEPLOY.md](DEPLOY.md). Content notes, outstanding placeholders and
design decisions are in [HANDOFF.md](HANDOFF.md).

## Before launch

The site carries ten yellow editor notes flagging missing content, plus striped
"Insert Photo" tiles in empty image slots. Delete the `.todo` rule in
`assets/css/site.css` to hide the notes. Outstanding items are listed in HANDOFF.md.
