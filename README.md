# Case studies · Lukasz Rodzen

Static site, no build step for visitors. Three pages: `index.html` (landing), `the-system.html`, `how-i-ship.html`.

Edit `src/content.py` for content and `src/theme.py` for shared styling. Rebuild with `PYTHONDONTWRITEBYTECODE=1 ./build.sh`; the generated HTML is served directly.

The system video player lives in `src/overview.py`, with media paths configured in `src/content.py`. It defaults to the 50-second Overview; the Full walkthrough tab opens the 8:31 recording. Switching pauses the previous video and preserves each video’s position during the page visit. Each video loads on demand and has its own MP4, poster, English captions, and readable transcript. The full transcript and 32 chapter links live in `src/walkthrough.py`. Keep each media set together when publishing. Keyboard tabs and native no-JavaScript playback are supported. Local seeking requires a static server with HTTP byte ranges.

Hosting: GitHub Pages, branch `main`, folder `/ (root)`. `.nojekyll` keeps Pages from processing the files. Publish only after review and explicit commit/push approval.
