#!/usr/bin/env python3
"""
Build self-contained pages for Yale Landing.

Takes the linked source pages in src/ (which reference assets/css, assets/js and
assets/img) and produces single-file HTML in the site root, with the stylesheet,
script and images all inlined. That way a page renders correctly no matter where
it's opened from — email attachment, preview pane, a folder without assets/.

Run:  python3 build.py
"""

import argparse, base64, io, os, re, shutil, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DOCS = os.path.join(ROOT, "docs")
IMG = os.path.join(ROOT, "assets", "img")
PAGES = ["index.html", "pericos.html", "paleteria-cuauhtemoc.html", "fmv-brewing.html"]

# The placeholder baked into the source pages. build_docs() swaps this for the
# real base URL so canonical tags, Open Graph tags and the sitemap all match
# wherever the site actually lives.
PLACEHOLDER_BASE = "https://yaleabq.com/"

JPEG_QUALITY = 78
MAX_EDGE = 1200


def normalize_images():
    """Bake in EXIF rotation and strip metadata, so orientation is never guessed."""
    for name in sorted(os.listdir(IMG)):
        if not name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        path = os.path.join(IMG, name)
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        if max(im.size) > MAX_EDGE:
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
        im.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        print(f"  image  {name:34} {im.size[0]}x{im.size[1]}  {os.path.getsize(path)/1024:.0f}KB")


def data_uri(rel_path):
    path = os.path.join(ROOT, rel_path)
    mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode("ascii")


def build():
    css = open(os.path.join(ROOT, "assets/css/site.css"), encoding="utf-8").read()
    js = open(os.path.join(ROOT, "assets/js/site.js"), encoding="utf-8").read()

    for page in PAGES:
        html = open(os.path.join(SRC, page), encoding="utf-8").read()

        html = html.replace(
            '<link rel="stylesheet" href="assets/css/site.css">',
            "<style>\n" + css + "\n</style>",
        )
        html = html.replace(
            '<script src="assets/js/site.js"></script>',
            "<script>\n" + js + "\n</script>",
        )

        # Inline every local image reference
        cache = {}

        def repl(m):
            rel = m.group(1)
            if rel not in cache:
                cache[rel] = data_uri(rel)
            return f'src="{cache[rel]}"'

        html = re.sub(r'src="(assets/img/[^"]+)"', repl, html)

        out = os.path.join(ROOT, page)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"  page   {page:34} {os.path.getsize(out)/1024:.0f}KB  ({len(cache)} images inlined)")


# ---------------------------------------------------------------------------
# Single-file preview
#
# Some viewers render an HTML file in isolation, with no folder around it. In
# that context a link to a sibling page (pericos.html) has nothing to resolve
# against and errors out. yale-preview.html sidesteps that entirely: all four
# pages live in one document and navigation is handled in JavaScript, so it
# works anywhere. Review artefact only — deploy the real pages from src/.
# ---------------------------------------------------------------------------

PAGE_IDS = {
    "index.html": "home",
    "pericos.html": "pericos",
    "paleteria-cuauhtemoc.html": "paleteria",
    "fmv-brewing.html": "fmv",
}

PREVIEW_CSS = """
.pv-bar{background:#231F20;color:rgba(255,255,255,.72);font-family:"Jost",sans-serif;
  font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;text-align:center;
  padding:.55rem 1rem;line-height:1.5}
.pv-bar b{color:#FCE5C8;font-weight:500}
.pv-page[hidden]{display:none}
"""

PREVIEW_JS = """
(function(){
  var pages = {};
  document.querySelectorAll('.pv-page').forEach(function(p){ pages[p.dataset.pv] = p; });

  function show(id, anchor){
    if(!pages[id]) id = 'home';
    Object.keys(pages).forEach(function(k){ pages[k].hidden = (k !== id); });

    document.querySelectorAll('[data-nav]').forEach(function(a){
      if(a.dataset.nav === id && !a.dataset.anchor) a.setAttribute('aria-current','page');
      else a.removeAttribute('aria-current');
    });

    if(anchor){
      var t = pages[id].querySelector('#' + anchor) || document.getElementById(anchor);
      if(t){ t.scrollIntoView({behavior:'smooth', block:'start'}); return; }
    }
    window.scrollTo({top:0, behavior:'smooth'});
  }

  document.addEventListener('click', function(e){
    var a = e.target.closest('[data-nav]');
    if(!a) return;
    e.preventDefault();
    show(a.dataset.nav, a.dataset.anchor || '');
    var nav = document.getElementById('site-nav');
    if(nav){ nav.classList.remove('is-open'); }
  });

  show('home','');
})();
"""


def namespace_ids(body, pid):
    """
    Four pages sharing one document means duplicate ids — every tenant page has an
    `id="hours"` sidecard, for instance. Suffix each id with its page so they stay
    unique, and repoint that page's own anchors at the new names.
    Returns the rewritten body and the map of old id -> new id.
    """
    ids = re.findall(r'\sid="([^"]+)"', body)
    mapping = {i: f"{i}__{pid}" for i in ids}

    def fix_id(m):
        return f' id="{mapping.get(m.group(1), m.group(1))}"'
    body = re.sub(r'\sid="([^"]+)"', fix_id, body)

    def fix_href(m):
        target = m.group(1)
        return f'href="#{mapping[target]}"' if target in mapping else m.group(0)
    body = re.sub(r'href="#([^"]+)"', fix_href, body)

    return body, mapping


def rewrite_links(html, anchor_maps):
    """Turn cross-page hrefs into in-document navigation triggers."""
    def repl(m):
        href = m.group(1)
        file, _, anchor = href.partition("#")
        if file in PAGE_IDS:
            pid = PAGE_IDS[file]
            anchor = anchor_maps.get(pid, {}).get(anchor, anchor)
            return f'href="#" data-nav="{pid}" data-anchor="{anchor}"'
        return m.group(0)
    return re.sub(r'href="([^"]+)"', repl, html)


def rewrite_bare_anchors(html, home_map):
    """
    The shared header and footer link to homepage sections with plain anchors
    (#visit, #lease). From a tenant page those sections are hidden, so the click
    does nothing. Convert them into navigation triggers that switch to the
    homepage first, then scroll.
    """
    def repl(m):
        target = m.group(1)
        if target in home_map:
            return f'href="#" data-nav="home" data-anchor="{home_map[target]}"'
        return m.group(0)
    return re.sub(r'href="#([^"]+)"', repl, html)


def build_preview():
    css = open(os.path.join(ROOT, "assets/css/site.css"), encoding="utf-8").read()
    js = open(os.path.join(ROOT, "assets/js/site.js"), encoding="utf-8").read()

    index_src = open(os.path.join(SRC, "index.html"), encoding="utf-8").read()
    header = re.search(r'<header class="site-header">.*?</header>', index_src, re.S).group(0)
    footer = re.search(r'<footer class="site-footer">.*?</footer>', index_src, re.S).group(0)

    sections = []
    anchor_maps = {}
    for page, pid in PAGE_IDS.items():
        src = open(os.path.join(SRC, page), encoding="utf-8").read()
        body = re.search(r'<main id="main">(.*?)</main>', src, re.S).group(1)
        # Anything between </main> and <footer> (e.g. the FMV note) belongs to the page too
        tail = re.search(r'</main>(.*?)<footer class="site-footer">', src, re.S)
        extra = tail.group(1).strip() if tail else ""
        body, mapping = namespace_ids(body + "\n" + extra, pid)
        anchor_maps[pid] = mapping
        sections.append(f'<div class="pv-page" data-pv="{pid}" hidden>\n{body}\n</div>')

    home_map = anchor_maps["home"]
    header = rewrite_bare_anchors(header, home_map)
    footer = rewrite_bare_anchors(footer, home_map)

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Yale Landing — Full Site Preview (all pages in one file)</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
{css}
{PREVIEW_CSS}
</style>
</head>
<body>
<div class="pv-bar">Preview build — all four pages in one file so the menu works anywhere. <b>Deploy the separate pages in src/.</b></div>
{rewrite_links(header, anchor_maps)}
<main id="main">
{rewrite_links(chr(10).join(sections), anchor_maps)}
</main>
{rewrite_links(footer, anchor_maps)}
<script>
{js}
{PREVIEW_JS}
</script>
</body>
</html>
"""

    cache = {}

    def repl(m):
        rel = m.group(1)
        if rel not in cache:
            cache[rel] = data_uri(rel)
        return f'src="{cache[rel]}"'

    doc = re.sub(r'src="(assets/img/[^"]+)"', repl, doc)

    out = os.path.join(ROOT, "yale-preview.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"  page   {'yale-preview.html':34} {os.path.getsize(out)/1024:.0f}KB  ({len(cache)} images inlined)")


# ---------------------------------------------------------------------------
# docs/ — the folder GitHub Pages actually serves
#
# The linked pages in src/ reference assets/ as a sibling, so src/ can't be
# published on its own. docs/ puts the pages and assets/ side by side, which is
# the layout GitHub Pages expects, and rewrites the placeholder domain to
# whatever base URL the site is really hosted at.
# ---------------------------------------------------------------------------

def build_docs(base_url):
    if not base_url.endswith("/"):
        base_url += "/"

    # Overwrite in place rather than deleting the tree first. Some synced folders
    # (OneDrive, Dropbox, network shares) refuse unlink, which would crash a rmtree.
    os.makedirs(DOCS, exist_ok=True)

    stripped = 0
    for page in PAGES:
        html = open(os.path.join(SRC, page), encoding="utf-8").read()
        html = html.replace(PLACEHOLDER_BASE, base_url)

        # Remove the editor notes outright rather than hiding them with CSS —
        # hidden text is still in the source, and some of it discusses things
        # that shouldn't be published at all.
        html, n = re.subn(r'[ \t]*<div class="todo"[^>]*>.*?</div>\s*\n?', '', html, flags=re.S)
        stripped += n
        # And the empty wrappers a few of them were sitting in
        html = re.sub(r'<div class="wrap">\s*</div>\s*\n?', '', html)

        # Empty photo slots: swap the internal "Insert Photo — <shot description>"
        # for something a visitor should see.
        html = re.sub(
            r'<div class="ph([^"]*)">\s*<strong>.*?</strong>\s*<span>.*?</span>\s*</div>',
            r'<div class="ph\1"><span>Photo coming soon</span></div>',
            html, flags=re.S)

        with open(os.path.join(DOCS, page), "w", encoding="utf-8") as fh:
            fh.write(html)
    print(f"  stripped {stripped} editor notes from the public build")

    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DOCS, "assets"),
                    dirs_exist_ok=True)

    # Public build: hide the editor notes, and soften the empty photo tiles so an
    # unfinished slot reads as "coming soon" rather than an internal to-do list.
    # src/ keeps both intact, so the preview file still shows you what's missing.
    css_path = os.path.join(DOCS, "assets", "css", "site.css")
    with open(css_path, "a", encoding="utf-8") as fh:
        fh.write("""

/* ===== public build overrides (generated by build.py — edit src, not this) ===== */
.ph span {
  font-size: .66rem; letter-spacing: .19em; text-transform: uppercase;
  color: var(--gray); max-width: none;
}
.ph--dark span { color: rgba(255,255,255,.55); }
""")

    for extra in ("sitemap.xml", "robots.txt"):
        text = open(os.path.join(ROOT, extra), encoding="utf-8").read()
        text = text.replace(PLACEHOLDER_BASE, base_url)
        with open(os.path.join(DOCS, extra), "w", encoding="utf-8") as fh:
            fh.write(text)

    # Stops GitHub running the pages through Jekyll
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    total = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, _, fs in os.walk(DOCS) for f in fs
    )
    n = sum(len(fs) for _, _, fs in os.walk(DOCS))
    print(f"  docs/  {n} files, {total/1024:.0f}KB total — base URL {base_url}")

    leftover = [p for p in PAGES
                if PLACEHOLDER_BASE.rstrip('/') in open(os.path.join(DOCS, p), encoding="utf-8").read()]
    if leftover:
        print("  WARNING placeholder domain still present in:", leftover)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the Yale Landing site.")
    ap.add_argument("--base-url", default=PLACEHOLDER_BASE,
                    help="Public URL the site will be served from, e.g. "
                         "https://username.github.io/yale/ or https://yaleabq.com/")
    args = ap.parse_args()

    if not os.path.isdir(SRC):
        sys.exit("src/ not found — the linked source pages should live there.")

    print("Normalizing images…")
    normalize_images()
    print("Building self-contained pages…")
    build()
    print("Building single-file preview…")
    build_preview()
    print("Building docs/ for GitHub Pages…")
    build_docs(args.base_url)
    print("Done.")
