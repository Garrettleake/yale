# Publishing this folder

## The lock file error

GitHub Desktop is pointed at `yale-site`, which has a broken `.git` folder left
over from an interrupted session. It contains four stale lock files:

```
.git/HEAD.lock
.git/index.lock
.git/objects/maintenance.lock
.git/refs/heads/master.lock
```

Git writes a `.lock` file before changing a ref, then deletes it when finished.
If the process dies partway through, the lock stays behind and every later
operation refuses to run — which is the error you're seeing.

**Don't fix that repo — don't use it at all.** Publish *this* folder instead
(`yale-landing-preview`), which has no `.git` in it and is already laid out
exactly the way GitHub Pages needs.

### Clearing the old one

In File Explorer, open `yale-site`, turn on **View → Hidden items**, and delete
the `.git` folder. Or in Command Prompt:

```
cd "C:\Users\bedel\Claude\Co work\yale-site"
rmdir /s /q .git
```

It only holds one commit from the failed session and has no remote, so there's
nothing to lose. Also remove `yale-site` from GitHub Desktop's repository list
(right-click → Remove) so you don't pick it by accident.

---

## Why a separate folder

For the link to work as `https://YOURNAME.github.io/REPO/`, `index.html` has to
sit at the **top level of the repository**.

`yale-site` is the project workspace — source files, generators, build scripts,
and two different builds of the site. Its `index.html` is even excluded by
`.gitignore`. Publishing it would not give you a working site.

This folder is only the finished preview: 86 files, 16 MB, all paths relative so
it works at any repo name.

---

## Publish it

1. **GitHub Desktop → File → Add local repository**
2. Choose this folder:
   `C:\Users\bedel\Claude\Co work\yale-landing-preview`
3. It will say the folder isn't a git repository — click **create a repository**.
   Leave the ignore template as None. Click **Create repository**.
4. **Publish repository** (top right).
   - Name it something readable — it becomes part of the URL. `yale-landing`
     gives you `yourname.github.io/yale-landing/`.
   - **Untick "Keep this code private."** GitHub Pages needs a paid plan for
     private repositories.
5. On github.com, open the repo → **Settings → Pages**
   - Source: **Deploy from a branch**
   - Branch: **main**, folder: **`/ (root)`**
   - Save
6. Give it a minute, then open `https://YOURNAME.github.io/REPO/`.

---

## Confirm before sending it on

- `/lease` — the brochure PDF should display inline
- `/pericos`, `/fmv-brewing` — tenant pages load with photos
- Scroll the homepage — the header logo shrinks as you go

---

## It will not show up in Google

Every page carries `noindex, nofollow, noarchive, nosnippet, noimageindex` for
Google, Bing and Yahoo. No sitemap is published, and nothing public links here.

`robots.txt` allows crawling on purpose. Blocking it would stop crawlers reading
the noindex, and a blocked URL can still be indexed from a link — which is the
opposite of what you want.

---

## Updating it later

Edit the source in `yale-site`, then from that folder:

```bash
python3 build-preview.py
```

Copy the contents of `yale-site/preview` over this folder, and GitHub Desktop
will show the changed files to commit and push.

When the real domain is confirmed, this preview is not the thing you launch —
see `DEPLOY.md` in `yale-site`, which publishes `docs/` instead.
