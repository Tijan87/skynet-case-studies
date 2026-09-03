# Publish on GitHub Pages (one-time, about 3 minutes)

1. On github.com, create a new **public** repository named `skynet-case-studies` (no README, no .gitignore).
2. In this folder run:
   ```
   git remote add origin https://github.com/Tijan87/skynet-case-studies.git
   git add -A && git commit -m "Case studies site" && git push -u origin main
   ```
3. In the repository: Settings → Pages → Build and deployment → Source: "Deploy from a branch" → Branch: `main`, folder `/ (root)` → Save.
4. After about a minute the site is live at **https://tijan87.github.io/skynet-case-studies/** (landing), plus `/the-system.html` and `/how-i-ship.html`.

Later changes: edit `src/content.py` (copy and numbers) or `src/theme.py` (design), run `./build.sh`, commit, push. Pages redeploys automatically.

Optional custom domain: Settings → Pages → Custom domain (e.g. `cv.yourdomain.com`), add the CNAME record at your DNS provider, tick "Enforce HTTPS".

Notes: `robots.txt` and `<meta name="robots" content="noindex">` keep the pages out of search engines; only people with the link find them. Remove both if you want it indexed.
