# Yale Landing — client preview

Preview build for review only.

**Not searchable.** Every page carries
`noindex, nofollow, noarchive, nosnippet, noimageindex` for Google, Bing
and Yahoo, and no sitemap is published.

robots.txt deliberately *allows* crawling. That looks backwards, but a
blanket `Disallow: /` would stop crawlers fetching the pages at all, so
they would never read the noindex — and Google can still index a blocked
URL from inbound links alone. Allowing the crawl is what makes the
noindex bite.

Paths are relative, so this works at any `github.io/REPO/` address.

Rebuild with `python3 build-preview.py` from the parent folder.
The production build for the real domain lives in `docs/`.
