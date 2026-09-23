# Case studies · Lukasz Rodzen

Static site, no build step for visitors. Three pages: `index.html` (landing), `the-system.html`, `how-i-ship.html`.

Edit `src/content.py` for content and `src/theme.py` for shared styling. Rebuild with `PYTHONDONTWRITEBYTECODE=1 ./build.sh`; the generated HTML is served directly.

The system overview player lives in `src/overview.py`, with its media paths configured in `src/content.py`. Its MP4, poster and English captions are in `assets/video/`. Keep those three files together when publishing. The player loads the video on demand and includes native controls and a readable transcript. Local video seeking requires a static server that supports HTTP byte ranges.

Hosting: GitHub Pages, branch `main`, folder `/ (root)`. `.nojekyll` keeps Pages from processing the files. Publish only after review and explicit commit/push approval.
