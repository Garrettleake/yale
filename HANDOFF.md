# Yale Landing — site handoff

Static site for **2500 Yale Blvd SE, Albuquerque, NM 87106**.

There are **three builds of the same site**. Which one you want depends on what you're doing.

```
yale-preview.html             ← LOOK AT THE SITE HERE.
                                 All four pages in one file, with the menu wired up in
                                 JavaScript. Works in any viewer, including ones that
                                 open a file in isolation. Review only — never deploy it.

index.html                    ← SEND SOMEONE A SINGLE PAGE.
pericos.html                     Each page self-contained: CSS, JS and photos baked in.
paleteria-cuauhtemoc.html        Renders correctly anywhere, but the menu only works if
fmv-brewing.html                 all four sit in the same folder.

src/                          ← DEPLOY THIS.
  index.html                     Same four pages linked to external CSS/JS/images.
  pericos.html                   ~25KB each instead of ~750KB, which matters for
  paleteria-cuauhtemoc.html      ranking. Upload src/ + assets/ + sitemap.xml +
  fmv-brewing.html               robots.txt to Netlify / Vercel / Cloudflare Pages.

assets/css/site.css           All styling
assets/js/site.js             Mobile nav + footer year
assets/img/                   Photos
build.py                      Regenerates the self-contained pages and the preview
sitemap.xml  robots.txt
```

**Why three.** Two problems turned up while reviewing, and each needed a different fix:

1. A page opened away from its folder couldn't find the stylesheet or images and rendered as
   raw text → fixed by inlining everything into each page.
2. Clicking a menu item in a viewer that renders files in isolation gave an error, because a
   link to `pericos.html` has no folder to resolve against → fixed by `yale-preview.html`,
   which holds every page in one document.

Neither fix belongs in production: inlined pages are ~30× larger, and a JavaScript-navigated
single file gives Google one URL instead of four, which throws away the per-page SEO. So
`src/` stays linked and multi-page, and the other two exist purely so you can review comfortably.

**Editing.** Change `src/` and `assets/`, then run `python3 build.py` — it regenerates the
self-contained pages *and* the preview. Or just tell me what to change and I'll rebuild all three.

---

## 1. Read this first — a name correction

The internal email lists Suite A as **"Polenta Bar."** That business is actually
**Paletería Cuauhtémoc** — a Mexican paleta and ice cream shop. Confirmed four ways:

- LoopNet's own tenant roster for the property lists "Paleteria Cuauhtemoc"
- Grubhub and Seamless both list it at *2500 Yale Blvd SE, Suite A*
- It has an active Instagram (`@paleteria_cuauh`) and TikTok
- The photo you sent, filed as *"Paleta - Ice Cream Suite A"*, shows the Paletería Cuauhtémoc sign

I built the page as Paletería Cuauhtémoc. If "Polenta Bar" is a real second business I've missed,
tell me and I'll add it.

**Brewery name — confirmed, not invented:** **FMV Brewing Co.** (Five Mountains View; the liquor
licence is filed under Five Mountains Viewpoint, LLC). Verified from LoopNet's tenant roster and
from the brewery's own site, `fivemountainsbrewing.com`, which lists 2500 Yale Blvd SE, Suite G.

---

## 2. What's confidential — and what I did about it

Nothing from the internal email is on the public site. I scanned every published file to confirm:
no per-suite rents, no Honey Hole buyout terms, no lease rates, no PSF figures, no suite letters
tied to money. The leasing section says one space is available and routes to Ted. That's it.

I also left out the *pizza* preference, as instructed — the leasing copy lists restaurant, café,
bar, retail and service uses so it stays open-ended.

Two suite letters *are* published, but only because they're already public and are customer-facing
wayfinding: Suite A (Paletería, published on delivery platforms) and Suite G (FMV, published on
their own website). The available space is described without a letter.

---

## 3. Placeholders — things I would not make up

Every one of these is marked with a yellow striped box in the page itself, so you can see them
while you scroll. **Delete the `.todo` blocks before launch** (or delete the `.todo` CSS rule to
hide them all at once).

### Hours & contact — done

All hours and phone numbers are now pulled from each business's **Google Business Profile** and are
live on the site and in the structured data.

| Business | Hours | Phone |
|---|---|---|
| Perico's (Yale Landing) | Mon–Fri 9am–8pm · Sat 10am–7pm · **Sun closed** | (505) 247-2503 |
| Paletería Cuauhtémoc | Mon–Fri 11am–9pm · Sat–Sun 12pm–9pm | (505) 527-7100 |
| FMV Brewing | Wed–Sat 12pm–9pm · Sun 12pm–8pm · **Mon–Tue closed** | (505) 226-6068 |

Two things to remember later:

- **FMV is still soft-opening**, so re-check their hours once the schedule settles. (Phone number
  confirmed good by Garrett.)
- **Perico's website** (pericosabq.com) shows the Coors Blvd store's hours, not Yale Landing's. The hours
  on our site come from the Yale Landing listing specifically, so they're right — just don't "correct" them
  against the main website later.

Also confirmed along the way: Perico's is listed at $10–20 per person with dine-in, takeout and
delivery; FMV's Google profile declares the business **veteran-owned**, which I've worked into their
page copy. Flag it if that's not something they want highlighted.

### Content still open

- **Perico's full menu** — the page now names the dishes people actually order (shredded beef tacos,
  chicharrón burrito, chile relleno burrito, sopapillas), taken from the Google listing's popular
  items and review tags. A real menu with prices would let me add `Menu` structured data.
- **Paletería flavor list** — still the biggest gap. Flavor names are the whole search play here.
- **FMV tap list** — nothing published yet. A live tap list gives people a reason to re-visit the page.
- **About Yale Landing section** (homepage) — deliberately generic. Send me a few sentences about the family,
  how long you've owned it, why Yale Blvd. This is the section most likely to earn local links.
- **Drive time to the Sunport** — I wrote "minutes" rather than invent a number. Drop in the real
  mileage and minutes from the terminal *and* the rental car center. "1.8 miles · 5 minutes" converts
  far better than "minutes away," and it's a real ranking signal.

### Photos

**Your five photos are 480 × 640 phone snapshots.** An image looks sharp when it's displayed at or
below its native size and soft when it's stretched past it, so the whole photo treatment is built
around keeping these under 480px wherever they appear:

| Treatment | Where | Why |
|---|---|---|
| **Blurred backdrop** (`.is-soft`) | Every hero | A full-bleed hero upscales a 480px photo about 3×. Blurring it turns that into deliberate depth of field, and the headline sits over it cleanly. |
| **Sharp framed inset** | Homepage hero | A 300px print floating over the blurred backdrop — well under native, so it stays crisp. Gives the hero a real focal point. |
| **White mat + hairline border** | Cards, gallery, photo row | Frames each photo as a print instead of a stretched fill, and the padding shrinks the image another ~20px. |
| **260px capped frames** | "A Look Around" | Was a full-width mosaic with one tile spanning 600px+. Now eight small framed prints, all downscaling. |
| **240px capped frames** | Tenant page galleries | Same idea. |

**To go sharp later:** delete the `is-soft` class from the hero markup. That's the only change
needed — everything else already displays below native size and will simply get sharper with
better source files. Anything 2000px or wider on the long edge.

(I've also baked the EXIF rotation into the files and recompressed them — they were relying on the
viewer honouring an orientation flag, which isn't reliable. Each dropped from ~155KB to ~50KB.)

Still needed — these render as striped "INSERT PHOTO" tiles:

1. **FMV Brewing taproom** interior (homepage card + two gallery slots)
2. **FMV patio or a pour**
3. **Salon / The Suite Haus** — build-out or finished suite
4. **Paletería product shot** — paletas or aguas frescas close-up

A note on sourcing: I couldn't pull images from Instagram or Google directly — those platforms
block automated fetching, and hotlinking their CDN breaks as soon as they rotate a URL. Either
download the tenant's own posts and drop them in `assets/img/`, or shoot them yourself. Your call
on which is faster.

Also worth adding when you have them: the building exterior wide shot and the monument sign on
Yale Blvd. Both are strong for the homepage hero.

---

## 4. Before you go live

1. **Domain.** Every canonical URL, Open Graph tag, sitemap entry and robots line uses
   `https://yaleabq.com/` as a placeholder. Find-and-replace it once you've picked the real domain.
2. **Delete the `.todo` blocks.** They're meant to be visible during review, not to customers.
3. **Google Business Profiles.** This matters more than the site for "near me" searches. Make sure
   each tenant's profile has the right address, hours, category and photos, and that the site links
   from each one. The site reinforces the profiles; it doesn't replace them.
4. **Submit the sitemap** in Google Search Console once the domain is live.
5. **Look at it on a phone.** I verified the markup, links, images, structured data and CSS
   programmatically — all clean — but I couldn't render a screenshot in this environment, so the
   visual pass is yours.

---

## 5. SEO structure as built

| Page | Primary target | Schema |
|---|---|---|
| Homepage | restaurants near Albuquerque airport / food near ABQ Sunport | `ShoppingCenter` + `containsPlace` |
| Perico's | Mexican food near the Albuquerque airport | `Restaurant` + hours, phone, price range |
| Paletería | paletas & ice cream near the Albuquerque airport | `IceCreamShop` + hours, phone |
| FMV Brewing | brewery near the Albuquerque airport | `Brewery` + hours, phone |

Each page has a unique title, meta description, single H1, canonical URL and its own JSON-LD block.
All four parse, and all three tenant pages now carry verified `openingHoursSpecification` — which is
what lets Google show an "Open · Closes 9 PM" line against your pages, not just the tenants' own
listings.

The homepage FAQ section is written for featured snippets ("Where can I get good Mexican food near
the Albuquerque airport?"). Worth adding `FAQPage` schema once the answers are final.

---

## 6. Design notes

Modeled on **Scottsdale Fashion Square** (fashionsquare.com), which is the reference you gave:

- White base with warm **tan / peach / butter** bands alternating down the page
- **Square corners and hairline borders** everywhere — no rounded cards, no drop shadows at rest
- **Outlined rectangular buttons**, uppercase and widely letterspaced — same as their
  "LEASE A QUIKSPACE" treatment
- **Wordmark centered** at the top with a small caps kicker above it ("ALBUQUERQUE / *Yale Landing*"),
  hours indicator at top left, "Lease Now" at top right, nav row centered underneath
- **Full-bleed hero** with a short all-caps headline ("EAT. DRINK. STAY AWHILE.")
- Geometric sans (**Jost**) for everything, serif (**Cormorant Garamond**) only for the wordmark
- Tenant **wordmark strip** under the hero, their "Shop Top Brands" pattern
- A **"Happening Here"** three-up card band, straight from their homepage
- Photo **mosaic** section — asymmetric grid, one large tile plus wide and standard tiles

The New Mexico read now comes from the adobe/terracotta palette rather than from ornament, which
is closer to how Fashion Square handles its own desert-Southwest setting.

One deliberate choice carried over: there's **no Zia sun symbol** anywhere. It's sacred to Zia
Pueblo and its commercial use is a live issue in New Mexico.

Leasing is present but secondary: "Lease Now" sits top-right on every page as a click-to-call
`tel:+15059489171`, and there's one leasing panel low on the homepage. Everything above it is
pointed at customers.

### Placeholder system

Two visual conventions, both meant to be removed before launch:

- **Striped tan tiles labeled "INSERT PHOTO"** sit in every image slot I couldn't fill. Eleven
  of them across the site. Each names the specific shot needed.
- **Butter-colored notes with a terracotta bar** (`.todo`) explain what's missing and why.
  Nine of them.

Delete the `.todo` rule in the CSS to hide all the notes at once. The photo tiles need real
images dropped into `assets/img/` — tell me the filenames and I'll wire them up.
