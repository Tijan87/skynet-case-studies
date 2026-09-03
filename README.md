# Case studies · Lukasz Rodzen

Static site, no build step. Three pages: `index.html` (landing), `the-system.html`, `how-i-ship.html`.
Generated from `scratch/build_site.py` + `content.py`; edit those, run `python3 build_site.py --out .`, commit.

Hosting: GitHub Pages, branch `main`, folder `/ (root)`. `.nojekyll` keeps Pages from processing the files.
