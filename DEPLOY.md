# Getting Yale Landing online with GitHub Pages

Free, no server to manage, and it works with a custom domain later. Roughly ten minutes.

---

## Step 1 — Create the repository

On [github.com](https://github.com), click **New repository**.

- **Name:** `yale` (or anything — it becomes part of the URL)
- **Visibility:** Public. *GitHub Pages needs a paid plan for private repos.*
- **Do not** tick "Add a README" — the folder already has one

Copy the URL it shows you. It looks like `https://github.com/YOURNAME/yale.git`.

---

## Step 2 — Set the real URL and rebuild

Your site's address will be:

```
https://YOURNAME.github.io/yale/
```

Substitute your username and repo name, then run this from inside the `yale-site` folder:

```bash
python3 build.py --base-url https://YOURNAME.github.io/yale/
```

This matters. The canonical tags, social preview tags and sitemap currently point at a
placeholder domain. If you skip it, you're telling Google the real site lives somewhere
that doesn't exist.

*(Already own a domain? Use it here instead — `--base-url https://yourdomain.com/` — and see
Step 5.)*

---

## Step 3 — Push

> **Delete the `.git` folder first.** I tried to initialize the repo for you and the sandbox
> couldn't finish — it can't delete files in your synced folder, so it left a half-made repo
> with stale lock files behind. It's hidden; in File Explorer tick **View → Hidden items**,
> or from Command Prompt inside `yale-site`:
>
> ```
> rmdir /s /q .git
> ```
>
> Skip this and git will refuse to run with "another git process seems to be running."

Then, from inside the `yale-site` folder:

```bash
git init
git add .
git commit -m "Yale Landing — initial site"
git branch -M main
git remote add origin https://github.com/YOURNAME/yale.git
git push -u origin main
```

If it asks for a password, GitHub wants a **personal access token**, not your account
password — Settings → Developer settings → Personal access tokens → Tokens (classic) →
Generate new token, tick `repo`. Or install [GitHub Desktop](https://desktop.github.com)
and drag the folder in, which avoids the whole thing.

---

## Step 4 — Turn on Pages

In the repo: **Settings → Pages**

- **Source:** Deploy from a branch
- **Branch:** `main`, folder **`/docs`**
- Save

Give it a minute or two. `https://YOURNAME.github.io/yale/` goes live.

> The `/docs` folder is the published site. Everything else in the repo — `src/`, `assets/`,
> the preview file — comes along for version history but isn't served.

---

## Step 5 — Custom domain (optional, do it whenever)

1. Buy the domain (Namecheap, Cloudflare, Google Domains — all fine).
2. At your registrar, add these DNS records:

   | Type | Name | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | YOURNAME.github.io |

3. In **Settings → Pages → Custom domain**, enter the domain and save. Tick
   **Enforce HTTPS** once it becomes available (can take an hour).
4. Rebuild with the real domain and push again:

   ```bash
   python3 build.py --base-url https://yourdomain.com/
   git add . && git commit -m "Point canonical URLs at the live domain" && git push
   ```

---

## Making changes later

```bash
# edit files in src/ or assets/
python3 build.py --base-url https://YOURNAME.github.io/yale/
git add .
git commit -m "what changed"
git push
```

Live in under a minute. Never edit anything in `docs/` directly — it gets wiped and
rebuilt every time.

---

## Once it's live

- **Submit the sitemap.** [Google Search Console](https://search.google.com/search-console) →
  add the property → Sitemaps → submit `sitemap.xml`. This is what gets the restaurant pages
  indexed.
- **Link it from the Google Business Profiles.** Each tenant's profile should point at its page
  on the site. Higher impact for "food near ABQ airport" than anything on the site itself.
- **Delete the editor notes first** if you don't want them public — the ten yellow `.todo`
  blocks. Removing the `.todo` rule from `assets/css/site.css` hides all of them at once.

---

## Alternative: skip GitHub entirely

If this feels like a lot, [Netlify Drop](https://app.netlify.com/drop) will host the site
in about thirty seconds — drag the `docs` folder onto the page and you get a live URL. No
account needed to start, and you can attach a custom domain later. The tradeoff is no version
history, and you re-drag the folder for every update.
