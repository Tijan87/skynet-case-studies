"""Two levels of system demonstration, with native no-JS playback."""
from html import escape
from walkthrough import TRANSCRIPT as FULL_TRANSCRIPT, CHAPTERS, DURATION

TRANSCRIPT = [
    'I built SKYNET to bring trading intelligence and execution into one platform.',
    'It tracks Telegram signals and on-chain wallet activity, with rankings that make their historical performance easier to compare.',
    'Wallet profiles reveal trading results and behavior, while market intelligence adds context about changing conditions.',
    'The strategy engine lets you replay historical signals with different exit rules and position sizes.',
    'The trading terminal brings together Phantom wallet swaps, automated copy trading through my custom Rust engine, and live position monitoring.',
    'Detailed transaction timelines show the journey from the source signal through execution to on-chain confirmation.',
    'SKYNET connects the research, the trade, and the evidence behind it.',
]


def timestamp(seconds):
    seconds = int(seconds)
    return f'{seconds // 60}:{seconds % 60:02}'


def panel(key, config, title, duration, paragraphs, caption, chapters=(), link_html=None):
    src, poster, captions = (escape(config[k], quote=True) for k in ('src', 'poster', 'captions'))
    # Optional high-quality copy hosted off-git (Cloudflare R2): offered to large screens first;
    # phones and any load failure fall through to the in-repo copy.
    hd = escape(config['src_hd'], quote=True) if config.get('src_hd') else None
    video_src = '' if hd else f' src="{src}"'
    sources = (f'<source src="{hd}" type="video/mp4" media="(min-width: 900px)">\n'
               f'<source src="{src}" type="video/mp4">\n') if hd else ''
    open_src = hd or src
    transcript = ''.join('<p>' + escape(p) + '</p>' for p in paragraphs)
    chapter_nav = ''
    if chapters:
        links = ''.join(f'<button type="button" data-seek="{c["start"]:.3f}" aria-controls="system-{key}"><span>{timestamp(c["start"])}</span>{escape(c["title"])}</button>' for c in chapters)
        chapter_nav = f'<details class="overview-chapters" hidden><summary>Jump to a chapter <span>{len(chapters)} chapters</span></summary><nav aria-label="Walkthrough chapters">{links}</nav></details>'
    return f'''<section class="overview-panel" id="video-panel-{key}" aria-labelledby="video-title-{key}" data-video="{key}" data-title="{title.lower()}">
<h3 class="overview-panel-title" id="video-title-{key}">{title} <span>{timestamp(duration)}</span></h3>
<div class="overview-screen">
<video id="system-{key}"{video_src} controls playsinline preload="none" width="1920" height="1080" poster="{poster}" aria-label="SKYNET {title.lower()}" aria-describedby="video-caption-{key}">
{sources}<track kind="captions" src="{captions}" srclang="en" label="English">
Your browser cannot play this video. <a href="{src}">Open the {title.lower()}</a> or read the transcript below.
</video>
<button class="overview-play" type="button" aria-label="Play {title.lower()}" aria-controls="system-{key}" hidden><span class="overview-play-inner"><svg viewBox="0 0 32 32" width="32" height="32" aria-hidden="true"><path d="M11 6.5 26 16 11 25.5Z" fill="currentColor"/></svg><span class="overview-play-label">Play {title.lower()}</span></span></button>
</div>
<div id="video-caption-{key}" class="overview-caption"><span>{caption}</span>{link_html or f'<a href="{open_src}">Open video <span aria-hidden="true">↗</span></a>'}</div>
<p class="overview-error" role="status" hidden>The video could not load. Try Play again, or use the Open video link.</p>
{chapter_nav}
<details class="overview-transcript"><summary>Read the transcript</summary><div>{transcript}</div></details>
</section>'''


def home(config, full_href):
    """Single overview video for the landing page, with a quiet link to the full walkthrough."""
    link = f'<a class="btn home-video-full" href="{escape(full_href, quote=True)}"><span class="home-video-verb">Watch the </span>full walkthrough · {timestamp(DURATION)} <span class="a">→</span></a>'
    video = panel('home', config, 'Overview', 50, TRANSCRIPT, 'Telegram signals. On-chain wallets. Research and execution.', link_html=link)
    return f'''<figure class="overview overview-enhanced home-video rv" id="home-overview" aria-labelledby="home-overview-title">
<div class="kicker home-video-kicker" id="home-overview-title">See it in 50 seconds</div>
{video}
</figure>'''


def player(config):
    overview = panel('overview', config, 'Overview', 50, TRANSCRIPT,
                     'Telegram signals. On-chain wallets. Research and execution.')
    walkthrough = panel('walkthrough', config['walkthrough'], 'Full walkthrough', DURATION, FULL_TRANSCRIPT,
                        'Regimes, sizing, swap engines, positions, and transaction evidence.', CHAPTERS)
    return f'''<figure class="overview rv" id="overview" aria-labelledby="overview-title">
<div class="overview-heading"><div><div class="kicker">See the system in action</div><h2 id="overview-title">Trading intelligence, connected.</h2></div></div>
<div class="overview-tabs" role="tablist" aria-label="Choose a system video" hidden>
<button type="button" id="video-tab-overview" role="tab" aria-controls="video-panel-overview" aria-selected="true" tabindex="0">Overview <span>0:50</span></button>
<button type="button" id="video-tab-walkthrough" role="tab" aria-controls="video-panel-walkthrough" aria-selected="false" tabindex="-1">Full walkthrough <span>{timestamp(DURATION)}</span></button>
</div>
{overview}
{walkthrough}
<figcaption class="overview-note">Choose the introduction or explore the complete workflow.</figcaption>
</figure>'''


CSS = r'''
.overview{margin:0;scroll-margin-top:80px}
.overview-heading{margin-bottom:1.5rem}
.overview-heading h2{margin-top:.65rem;max-inline-size:none;font-size:clamp(1.65rem,2.3vw,2.5rem)}
.overview [hidden]{display:none!important}
.overview-tabs{display:flex;gap:0;border-bottom:1px solid var(--line-2);margin:0 0 1rem}
.overview-tabs button{position:relative;display:flex;align-items:center;gap:.85rem;min-height:52px;padding:.75rem 1.35rem;border:0;background:transparent;color:var(--ink-2);font:500 1rem/1.3 var(--body);cursor:pointer;transition:color .18s ease,background .18s ease}
.overview-tabs button::after{position:absolute;inset:auto 0 -1px;height:2px;background:var(--accent);content:'';opacity:0;transition:opacity .18s ease}
.overview-tabs button[aria-selected=true]{color:var(--ink);background:linear-gradient(0deg,rgba(49,217,255,.055),transparent)}
.overview-tabs button[aria-selected=true]::after{opacity:1}
.overview-tabs button span{font:400 .75rem/1.4 var(--mono);color:var(--ink-3);font-variant-numeric:tabular-nums}
.overview-tabs button[aria-selected=true] span{color:var(--accent)}
.overview-tabs button:hover{color:var(--ink);background:var(--surface-2)}
.overview-tabs button:focus-visible,.overview-chapters button:focus-visible{outline:2px solid var(--accent);outline-offset:-3px}
.overview-panel:focus-visible{outline:2px solid var(--accent);outline-offset:5px}
.overview-panel-title{display:flex;align-items:center;gap:1rem;margin:1.5rem 0 1rem;font:500 1.1rem/1.5 var(--body)}
.overview-panel-title span{font:400 .8rem/1.5 var(--mono);color:var(--ink-3)}
.overview-enhanced .overview-panel-title{display:none}
.overview-screen{position:relative;isolation:isolate;aspect-ratio:16/9;border:1px solid var(--line-2);border-radius:var(--r);overflow:hidden;background:var(--bg);box-shadow:0 24px 70px -40px rgba(0,0,0,.8)}
.overview-screen video{display:block;width:100%;height:100%;object-fit:contain;background:var(--bg)}
.overview-screen video:focus-visible{outline:2px solid var(--accent);outline-offset:-4px}
.overview-play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;width:100%;border:0;padding:0;cursor:pointer;color:var(--ink);background:linear-gradient(180deg,transparent 30%,rgba(5,8,15,.12) 100%);font:500 .9rem/1 var(--body)}
.overview-play-inner{display:flex;align-items:center;gap:10px;min-height:60px;padding:14px 22px 14px 16px;border:1px solid rgba(49,217,255,.5);border-radius:999px;background:rgba(5,8,15,.93);box-shadow:0 8px 40px rgba(0,0,0,.45);transition:border-color .18s ease,background .18s ease,transform .18s ease}
.overview-play svg{color:var(--accent);flex-shrink:0}
.overview-play:hover .overview-play-inner{background:#101d2b;border-color:var(--accent);transform:translateY(-2px)}
.overview-play:focus-visible{outline:3px solid var(--accent);outline-offset:-5px;border-radius:var(--r)}
.overview-caption{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;margin-top:.9rem;font-size:var(--fs-cap);line-height:1.5;color:var(--ink-2)}
.overview-caption a{flex-shrink:0;display:inline-flex;align-items:center;gap:8px;min-height:44px;color:var(--ink);text-decoration:underline;text-underline-offset:4px;text-decoration-color:var(--line-2)}
.overview-caption a:hover{color:var(--accent);text-decoration-color:var(--accent)}
.overview-error{margin-top:.75rem;color:var(--ink-2);font-size:var(--fs-cap)}
.overview-transcript,.overview-chapters{margin-top:.7rem;border-top:1px solid var(--line);color:var(--ink-2)}
.overview-transcript summary,.overview-chapters summary{width:fit-content;min-height:44px;padding:.85rem 0;cursor:pointer;font-size:var(--fs-cap);color:var(--ink-2)}
.overview-transcript summary:hover,.overview-chapters summary:hover{color:var(--ink)}
.overview-transcript>div{max-width:var(--w-prose);padding:.3rem 0 1rem}
.overview-transcript p+p{margin-top:1rem}
.overview-chapters summary span{margin-left:1rem;font:400 .7rem/1.5 var(--mono);color:var(--ink-3)}
.overview-chapters nav{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.25rem 1rem;padding:.25rem 0 1rem}
.overview-chapters button{display:flex;align-items:baseline;gap:.7rem;text-align:left;min-height:44px;padding:.6rem .5rem;border:0;border-radius:4px;background:transparent;color:var(--ink-2);font:400 .8rem/1.45 var(--body);cursor:pointer}
.overview-chapters button span{flex-shrink:0;width:3.2em;color:var(--ink-3);font:400 .7rem/1.5 var(--mono)}
.overview-chapters button:hover,.overview-chapters button[aria-current=true]{background:var(--surface-2);color:var(--ink)}
.overview-chapters button[aria-current=true] span{color:var(--accent)}
.overview-note{margin-top:1rem;font-size:.75rem;line-height:1.5;color:var(--ink-3)}
@media(max-width:640px){.overview-heading .kicker{font-size:.75rem}.overview-tabs button{flex:1;justify-content:center;gap:.55rem;padding:.7rem .55rem;font-size:.9rem}.overview-tabs button span{font-size:.65rem}.overview-caption{display:block}.overview-caption a{display:flex;width:fit-content;margin-top:.25rem}.overview-play-inner{min-height:50px;padding:9px 16px 9px 11px}.overview-play svg{width:26px;height:26px}.overview-chapters nav{grid-template-columns:repeat(2,minmax(0,1fr));gap:.25rem .5rem}}
@media(max-width:360px){.overview-tabs button{font-size:.8rem;gap:.4rem}.overview-tabs button span{font-size:.6rem}.overview-chapters nav{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){.overview-play-inner,.overview-tabs button,.overview-tabs button::after{transition:none}.overview-play:hover .overview-play-inner{transform:none}}
.home-video{margin:clamp(2.25rem,4vw,3rem) 0 0}
.home-video-kicker{margin-bottom:1rem}
.home-video .overview-panel-title{display:none}
.home-video .overview-caption{align-items:center}
.home-video .overview-caption .btn.home-video-full{text-decoration:none;color:var(--ink-2);min-height:40px}
.home-video .overview-caption .btn.home-video-full:hover{color:var(--accent)}
@media(max-width:640px){.home-video .overview-caption>span{display:block}.home-video .overview-caption .btn.home-video-full{display:flex;width:fit-content;margin-top:.8rem}.home-video-verb{display:none}}
@media print{.overview-play,.overview-tabs,.overview-chapters{display:none}.overview-screen{box-shadow:none}.overview-transcript>div{display:block}}
'''


JS = r'''
(function(){
  const figure = document.getElementById('overview');
  if (!figure) return;
  const tabs = Array.from(figure.querySelectorAll('[role="tab"]'));
  const panels = Array.from(figure.querySelectorAll('.overview-panel'));
  if (panels.length !== 2 || tabs.length !== 2) return;
  const videos = panels.map(panel => panel.querySelector('video'));
  if (videos.some(video => !video || typeof video.play !== 'function')) return;
  let selected = 0;
  const states = panels.map((panel,index) => ({panel, video:videos[index], button:panel.querySelector('.overview-play'),
    label:panel.querySelector('.overview-play-label'), error:panel.querySelector('.overview-error'),
    title:panel.dataset.title, pendingSeek:null, attempt:0}));

  function restingButton(state){
    state.button.disabled = false;
    const action = state.video.ended ? 'Replay' : state.video.currentTime > .1 ? 'Resume' : 'Play';
    state.label.textContent = action + ' ' + state.title;
    state.button.setAttribute('aria-label', action + ' ' + state.title);
  }
  function select(index){
    if (index !== selected){
      const previous = states[selected];
      previous.attempt++;
      previous.pendingSeek = null;
      previous.video.pause();
      restingButton(previous);
      const next = states[index];
      next.video.volume = previous.video.volume;
      next.video.muted = previous.video.muted;
      next.video.playbackRate = previous.video.playbackRate;
      if (previous.video.textTracks.length && next.video.textTracks.length)
        next.video.textTracks[0].mode = previous.video.textTracks[0].mode;
      selected = index;
    }
    states.forEach((state,i) => {
      const active = i === selected;
      state.panel.hidden = !active;
      tabs[i].setAttribute('aria-selected',String(active));
      tabs[i].tabIndex = active ? 0 : -1;
      if (active && state.video.paused){
        restingButton(state);
        state.button.hidden = false;
        state.video.controls = state.video.currentTime > .1;
      }
    });
  }
  async function play(index,seek){
    if (index !== selected) select(index);
    const state = states[index], video = state.video;
    const attempt = ++state.attempt;
    state.error.hidden = true;
    state.button.disabled = true;
    state.label.textContent = 'Loading…';
    if (Number.isFinite(seek)) state.pendingSeek = seek;
    else if (video.ended) state.pendingSeek = 0;
    if (video.error) video.load();
    if (state.pendingSeek !== null && video.readyState >= 1){
      video.currentTime = Math.min(state.pendingSeek, Math.max(0, video.duration - .05));
      state.pendingSeek = null;
    }
    try {
      await video.play();
      if (attempt !== state.attempt || index !== selected) return;
      state.button.hidden = true;
      video.controls = true;
      video.focus({preventScroll:true});
    } catch (err) {
      if (attempt !== state.attempt || index !== selected) return;
      video.controls = true;
      state.button.hidden = false;
      if (err.name === 'AbortError') restingButton(state);
      else {
        state.label.textContent = 'Try again';
        state.button.setAttribute('aria-label','Try playing ' + state.title + ' again');
        state.error.hidden = false;
      }
    } finally { if (attempt === state.attempt) state.button.disabled = false; }
  }
  states.forEach((state,index) => {
    const {panel,video,button} = state;
    panel.setAttribute('role','tabpanel');
    panel.setAttribute('aria-labelledby',tabs[index].id);
    panel.tabIndex = 0;
    video.controls = false;
    button.hidden = false;
    button.addEventListener('click',() => { if (!button.disabled) play(index); });
    video.addEventListener('loadedmetadata',() => {
      if (state.pendingSeek === null || index !== selected) return;
      video.currentTime = Math.min(state.pendingSeek, Math.max(0,video.duration-.05));
      state.pendingSeek = null;
    });
    video.addEventListener('play',() => {
      if (index !== selected){video.pause();return;}
      button.hidden = true;video.controls = true;state.error.hidden = true;
    });
    video.addEventListener('ended',() => {restingButton(state);button.hidden=false;});
    video.addEventListener('error',() => {
      if (index !== selected) return;
      video.controls = true;button.hidden = false;button.disabled = false;
      state.label.textContent = 'Try again';
      button.setAttribute('aria-label','Try playing ' + state.title + ' again');
      state.error.hidden = false;
    });
    const chapterButtons = Array.from(panel.querySelectorAll('[data-seek]'));
    const chapterDetails = panel.querySelector('.overview-chapters');
    if (chapterDetails) chapterDetails.hidden = false;
    chapterButtons.forEach(link => link.addEventListener('click',() => {
      play(index,Number(link.dataset.seek));
      video.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    }));
    video.addEventListener('timeupdate',() => {
      let current = null;
      chapterButtons.forEach(link => {if (Number(link.dataset.seek) <= video.currentTime + .05) current = link;});
      chapterButtons.forEach(link => {if (link === current) link.setAttribute('aria-current','true'); else link.removeAttribute('aria-current');});
    });
  });
  tabs.forEach((tab,index) => {
    tab.addEventListener('click',() => select(index));
    tab.addEventListener('keydown',event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();select(next);tabs[next].focus();
    });
  });
  figure.classList.add('overview-enhanced');
  figure.querySelector('.overview-tabs').hidden = false;
  select(0);
  if (location.hash === '#walkthrough'){
    select(1);
    requestAnimationFrame(() => figure.scrollIntoView({block:'start'}));
  }
})();
'''


HOME_JS = r'''
(function(){
  const figure = document.getElementById('home-overview');
  if (!figure) return;
  const panel = figure.querySelector('.overview-panel');
  const video = panel && panel.querySelector('video');
  const button = panel && panel.querySelector('.overview-play');
  if (!video || typeof video.play !== 'function' || !button) return;
  const label = panel.querySelector('.overview-play-label');
  const error = panel.querySelector('.overview-error');
  const rest = () => {
    const action = video.ended ? 'Replay' : video.currentTime > .1 ? 'Resume' : 'Play';
    label.textContent = action + ' overview';
    button.setAttribute('aria-label', action + ' overview');
    button.disabled = false;
  };
  video.controls = false;
  button.hidden = false;
  rest();
  button.addEventListener('click', async () => {
    if (button.disabled) return;
    button.disabled = true;
    label.textContent = 'Loading…';
    error.hidden = true;
    if (video.ended) video.currentTime = 0;
    if (video.error) video.load();
    try {
      await video.play();
      button.hidden = true;
      video.controls = true;
      video.focus({preventScroll:true});
    } catch (err) {
      video.controls = true;
      if (err.name === 'AbortError') rest();
      else { label.textContent = 'Try again'; error.hidden = false; }
    } finally { button.disabled = false; }
  });
  video.addEventListener('play', () => { button.hidden = true; video.controls = true; error.hidden = true; });
  video.addEventListener('ended', () => { rest(); button.hidden = false; });
  video.addEventListener('error', () => {
    video.controls = true; button.hidden = false; button.disabled = false;
    label.textContent = 'Try again'; error.hidden = false;
  });
})();
'''
