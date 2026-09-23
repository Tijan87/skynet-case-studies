"""The case-study overview player, with native playback as its no-JS fallback."""
from html import escape

TRANSCRIPT = [
    "Here's Skynet. Research, strategy, sizing, and execution, connected in one workspace.",
    "Start with a source. See how its strategies behave in bull, bear, and sideways markets.",
    "Now change the sizing. This preset excludes smaller tokens and increases selected position sizes. The historical replay turns positive. These are simulated results before trading costs.",
    "Move into the terminal to check balances, approve a Phantom swap, or follow automated strategies and open positions.",
    "Then open a recorded trade. The engine work took eighty-one milliseconds. The displayed end-to-end time was two point four seconds. You can inspect the stages behind those numbers.",
    "That's Skynet. From the signal to the evidence.",
]

def player(config):
    src, poster, captions = (escape(config[k], quote=True) for k in ('src', 'poster', 'captions'))
    transcript = ''.join('<p>' + escape(p) + '</p>' for p in TRANSCRIPT)
    return f'''<figure class="overview rv" id="overview" aria-labelledby="overview-title">
<div class="overview-heading"><div><div class="kicker">A recorded walkthrough</div><h2 id="overview-title">From signal to evidence.</h2></div><span class="overview-duration">01:00 <span>/ overview</span></span></div>
<div class="overview-screen">
<video id="system-overview" src="{src}" controls playsinline preload="none" width="1920" height="1080" poster="{poster}" aria-label="SKYNET system overview" aria-describedby="overview-caption">
<track kind="captions" src="{captions}" srclang="en" label="English">
Your browser cannot play this video. <a href="{src}">Open the 60-second overview</a> or read the transcript below.
</video>
<button class="overview-play" type="button" aria-label="Play the 60-second system overview" aria-controls="system-overview" hidden><span class="overview-play-inner"><svg viewBox="0 0 32 32" width="32" height="32" aria-hidden="true"><path d="M11 6.5 26 16 11 25.5Z" fill="currentColor"/></svg><span class="overview-play-label">Play overview</span></span></button>
</div>
<figcaption id="overview-caption" class="overview-caption"><span>Research. Sizing. Execution. The record behind the trade.</span><a href="{src}">Open video <span aria-hidden="true">↗</span></a></figcaption>
<p class="overview-error" role="status" hidden>The video could not load. Try Play again, or use the Open video link.</p>
<details class="overview-transcript"><summary>Read the transcript</summary><div>{transcript}</div></details>
</figure>'''

CSS = r'''
/* The complete viewport stays visible; the player's only motion follows user input. */
.overview{margin:0;scroll-margin-top:80px}
.overview-heading{display:flex;align-items:flex-end;justify-content:space-between;gap:1.5rem;margin-bottom:1.25rem}
.overview-heading h2{margin-top:.65rem;max-inline-size:none;font-size:clamp(1.65rem,2.3vw,2.5rem)}
.overview-duration{flex-shrink:0;font:500 .875rem/1.5 var(--mono);color:var(--ink);font-variant-numeric:tabular-nums;padding-bottom:.1rem}
.overview-duration span{color:var(--ink-3)}
.overview-screen{position:relative;isolation:isolate;aspect-ratio:16/9;border:1px solid var(--line-2);border-radius:var(--r);overflow:hidden;background:var(--bg);box-shadow:0 24px 70px -40px rgba(0,0,0,.8)}
.overview-screen video{display:block;width:100%;height:100%;object-fit:contain;background:var(--bg)}
.overview-screen video:focus-visible{outline:2px solid var(--accent);outline-offset:-4px}
.overview-play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;width:100%;border:0;padding:0;cursor:pointer;color:var(--ink);background:linear-gradient(180deg,transparent 30%,rgba(5,8,15,.12) 100%);font:500 .9rem/1 var(--body)}
.overview-play[hidden],.overview-error[hidden]{display:none}
.overview-play-inner{display:flex;align-items:center;gap:10px;min-height:60px;padding:14px 22px 14px 16px;border:1px solid rgba(49,217,255,.5);border-radius:999px;background:rgba(5,8,15,.93);box-shadow:0 8px 40px rgba(0,0,0,.45);transition:border-color .18s ease,background .18s ease,transform .18s ease}
.overview-play svg{color:var(--accent);flex-shrink:0}
.overview-play:hover .overview-play-inner{background:#101d2b;border-color:var(--accent);transform:translateY(-2px)}
.overview-play:focus-visible{outline:3px solid var(--accent);outline-offset:-5px;border-radius:var(--r)}
.overview-caption{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;margin-top:.9rem;font-size:var(--fs-cap);line-height:1.5;color:var(--ink-2)}
.overview-caption a{flex-shrink:0;display:inline-flex;align-items:center;gap:8px;min-height:44px;color:var(--ink);text-decoration:underline;text-underline-offset:4px;text-decoration-color:var(--line-2)}
.overview-caption a:hover{color:var(--accent);text-decoration-color:var(--accent)}
.overview-error{margin-top:.75rem;color:var(--ink-2);font-size:var(--fs-cap)}
.overview-transcript{margin-top:.7rem;border-top:1px solid var(--line);color:var(--ink-2)}
.overview-transcript summary{width:fit-content;min-height:44px;padding:.85rem 0;cursor:pointer;font-size:var(--fs-cap);color:var(--ink-2)}
.overview-transcript summary:hover{color:var(--ink)}
.overview-transcript>div{max-width:var(--w-prose);padding:.3rem 0 1rem}
.overview-transcript p+p{margin-top:1rem}
@media(max-width:640px){.overview-heading{align-items:flex-start;gap:.75rem}.overview-duration{font-size:.75rem;padding-top:.1rem}.overview-duration span{display:none}.overview-heading .kicker{font-size:.75rem}.overview-caption{display:block}.overview-caption a{display:flex;width:fit-content;margin-top:.25rem}.overview-play-inner{min-height:50px;padding:9px 16px 9px 11px}.overview-play svg{width:26px;height:26px}}
@media(prefers-reduced-motion:reduce){.overview-play-inner{transition:none}.overview-play:hover .overview-play-inner{transform:none}}
@media print{.overview-play{display:none}.overview-screen{box-shadow:none}.overview-transcript>div{display:block}}
'''

JS = r'''
(function(){
  const video = document.getElementById('system-overview');
  if (!video || typeof video.play !== 'function') return;
  const figure = video.closest('.overview');
  const button = figure.querySelector('.overview-play');
  const label = button.querySelector('.overview-play-label');
  const error = figure.querySelector('.overview-error');
  button.hidden = false;
  video.controls = false;
  button.addEventListener('click', async function(){
    if (button.disabled) return;
    error.hidden = true;
    button.disabled = true;
    label.textContent = 'Loading…';
    if (video.ended) video.currentTime = 0;
    if (video.error) video.load();
    try {
      await video.play();
      video.controls = true;
      button.hidden = true;
      video.focus({preventScroll:true});
    } catch (_) {
      video.controls = true;
      button.hidden = false;
      label.textContent = 'Try again';
      button.setAttribute('aria-label','Try playing the system overview again');
      error.hidden = false;
    } finally { button.disabled = false; }
  });
  video.addEventListener('play', function(){ button.hidden = true; video.controls = true; error.hidden = true; });
  video.addEventListener('ended', function(){
    button.hidden = false;
    label.textContent = 'Replay overview';
    button.setAttribute('aria-label','Replay the 60-second system overview');
  });
  video.addEventListener('error', function(){
    video.controls = true;
    button.hidden = false;
    button.disabled = false;
    label.textContent = 'Try again';
    error.hidden = false;
  });
})();
'''
