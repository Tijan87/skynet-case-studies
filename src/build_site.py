#!/usr/bin/env python3
"""Responsive, animated case-study site. Usage: python3 build_site.py [--links links.json] [--out DIR]"""
import base64, html, json, os, sys
import content as C
import banners as BN
import s2_v6
C.S2 = s2_v6.S2

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img") if os.path.isdir(os.path.join(HERE, "img")) else os.path.join(HERE, "..", "deck", "img")
JOURNEY = os.path.join(HERE, "journey_data.json") if os.path.exists(os.path.join(HERE, "journey_data.json")) else os.path.join(HERE, "..", "deck", "journey_data.json")
E = html.escape

def img_uri(name):
    with open(os.path.join(IMG, name), "rb") as f:
        return "data:image/webp;base64," + base64.b64encode(f.read()).decode()

# ------------------------------------------------------------------ tokens + css
from theme import CSS, JS

# ------------------------------------------------------------------ helpers
def kicker(t, accent=None, plain=False):
    return f'<div class="{"label" if plain else "kicker"}">{E(t)}</div>'

def metrics(ms):
    if not ms: return ""
    return '<div class="metrics" data-stagger>' + "".join(
        f'<div class="stat rv"><span class="n">{E(n)}</span><span class="l">{E(l)}</span></div>' for n, l in ms[:3]) + "</div>"

def note(t):
    return f'<p class="note rv">{t}</p>' if t else ""

def fn(t):
    return f'<p class="fn rv">{E(t)}</p>' if t else ""

def stats(ms):
    return '<div class="stats" data-stagger>' + "".join(f'<div class="stat rv"><span class="n">{E(n)}</span><span class="l">{E(l)}</span></div>' for n, l in ms) + "</div>"

def who(cls="who"):
    return f'<div class="{cls} rv"><div><div class="name">{E(C.NAME)}</div><div class="role">{E(C.ROLE)}</div><div class="contact">{(C.CONTACT_HTML + " · ") if C.CONTACT_HTML else ""}{E(C.LOCATION)}</div></div><p>{E(C.OPMODEL)}</p></div>'

def head(s, accent="cyan"):
    lead = f'<p class="lead rv">{E(s["lead"])}</p>' if s.get("lead") else ""
    return f'<div class="head" data-stagger><div class="rv">{kicker(s["kicker"])}</div><h2 class="rv">{E(s["h1"])}</h2>{lead}</div>'

def points(ps):
    return '<ul class="points" data-stagger>' + "".join(f'<li class="rv">{E(p)}</li>' for p in ps) + "</ul>"

def figbox(svg, tail="", cls="fig rv"):
    """Figure = a scrolling band (.figs-x) plus a static tail (legend, caption)."""
    return f'<div class="{cls}"><div class="figs-x">{svg}</div>{tail}</div>'

def shot(name, cap, tilt=False):
    return f'<figure class="rv" style="margin:0"><div class="shot{" tilt" if tilt else ""}"><img src="{img_uri(name)}" alt="{E(cap)}"></div><figcaption class="cap">{E(cap)}</figcaption></figure>'

# ------------------------------------------------------------------ svg figures
def pane(lines, cap=None):
    out = []
    for ln in lines:
        # markup: [k]..[/k] cyan, [g] green, [v] violet, [d] dim, [r] red, [w] white
        t = E(ln)
        for tag in ("k", "g", "v", "d", "r", "w"):
            t = t.replace(f"[{tag}]", f'<span class="{tag}">').replace(f"[/{tag}]", "</span>")
        out.append(f'<div class="ln">{t}</div>')
    c = f'<p class="cap">{E(cap)}</p>' if cap else ""
    return f'<div class="rv"><div class="pane"><div class="bar3"><i></i><i></i><i></i></div>{"".join(out)}</div>{c}</div>'


def fig_loop(stages):
    W, H = 760, 96; n = len(stages); gap = (W - 150) / (n - 1)
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The six stages of the loop; the three decisions that are mine are highlighted">'
    s += '<defs><linearGradient id="lg" x1="0" x2="1"><stop offset="0" stop-color="#a877ff"/><stop offset=".55" stop-color="#31d9ff"/><stop offset="1" stop-color="#58e7ad"/></linearGradient><filter id="gl"><feGaussianBlur stdDeviation="3"/></filter></defs>'
    s += f'<line x1="75" x2="{W-75}" y1="34" y2="34" stroke="url(#lg)" stroke-width="1.5" opacity=".9"/>'
    for i, (t, p, mine, ev) in enumerate(stages):
        x = 75 + i * gap
        if mine:
            s += f'<circle cx="{x:.1f}" cy="34" r="11" fill="#31d9ff" opacity=".35" filter="url(#gl)"/><circle cx="{x:.1f}" cy="34" r="6" fill="#31d9ff"/>'
        else:
            s += f'<circle cx="{x:.1f}" cy="34" r="5.5" fill="#05080f" stroke="#a7b4c9" stroke-width="1.5"/>'
        s += f'<text x="{x:.1f}" y="66" text-anchor="middle" font-size="11" fill="{"#f2f6ff" if mine else "#a7b4c9"}" font-family="IBM Plex Sans,sans-serif">{E(t)}</text>'
        if mine: s += f'<text x="{x:.1f}" y="86" text-anchor="middle" font-size="11" fill="#31d9ff" font-family="JetBrains Mono,monospace" letter-spacing="1">MY DECISION</text>'
    s += "</svg>"
    lst = '<ol class="ribbon-list">' + "".join(f'<li{" class=me" if mine else ""}><span>{E(t)}</span>{"<b>my decision</b>" if mine else ""}</li>' for t, p, mine, ev in stages) + "</ol>"
    return figbox(s, lst, "fig rv ribbon")


def fig_bytes():
    W, H = 720, 200
    LIM = 1232
    def bar(y, segs, label, over=False):
        x = 0; out = []
        sx = (W - 0) / 1400.0
        for name, b, col in segs:
            w = b * sx
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w-1.5,0):.1f}" height="26" rx="3" fill="{col}"/>')
            if w > 60: out.append(f'<text x="{x+6:.1f}" y="{y+17}" font-size="10" fill="#05080f" font-family="JetBrains Mono,monospace">{E(name)}</text>')
            x += w
        return "".join(out) + f'<text x="0" y="{y-8}" font-size="11" fill="#a7b4c9" font-family="JetBrains Mono,monospace">{E(label)}</text>'
    lim_x = LIM * (W / 1400.0)
    healthy = [("signature 64", 64, "#a7b4c9"), ("header 35", 35, "#6b7a94"), ("12 keys × 32", 384, "#31d9ff"), ("LUT refs", 40, "#58e7ad"),
               ("compute", 24, "#6b7a94"), ("Jupiter route", 520, "#a877ff"), ("tip", 60, "#6b7a94")]
    fresh = [("signature 64", 64, "#a7b4c9"), ("header 35", 35, "#6b7a94"), ("30 keys × 32 = 960", 960, "#31d9ff"), ("compute", 24, "#6b7a94"), ("route", 280, "#a877ff")]
    s = f'<svg viewBox="0 -4 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Byte budget of one transaction against the 1,232-byte limit">'
    s += bar(30, healthy, "healthy route · lookup table present · fits")
    s += bar(110, fresh, "fresh pump.fun route · no lookup table · overflows", True)
    s += f'<line x1="{lim_x:.1f}" x2="{lim_x:.1f}" y1="8" y2="150" stroke="#ff8f8f" stroke-dasharray="3 4"/>'
    s += f'<text x="{lim_x-4:.1f}" y="168" text-anchor="end" font-size="11" fill="#ff8f8f" font-family="JetBrains Mono,monospace">1,232-byte wire limit</text>'
    s += f'<text x="{W}" y="168" text-anchor="end" font-size="11" fill="#7d8ba3" font-family="JetBrains Mono,monospace">→ over</text>'
    s += "</svg>"
    return figbox(s, '<div class="cap">Illustrative composition. Each account referenced through a lookup table costs 1 byte instead of 32.</div>')

def fig_stages():
    rows = [("Route quote from Jupiter", 13), ("Build and sign the transaction", 4), ("Submit through Helius Sender", 14),
            ("On-chain program checks", 80), ("Wait for the blockchain to confirm", 621), ("Not instrumented per stage", 292)]
    W = 720; total = 1024; lx = 250; bw = W - lx - 20; H = 34 * len(rows) + 10
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="One production trade stage by stage, 1,024 ms end to end">'
    for i, (n, ms) in enumerate(rows):
        y = i * 34 + 6; w = max(2, ms / total * bw)
        col = "#6b7a94" if "Not" in n else ("#58e7ad" if "confirm" in n else "#31d9ff")
        s += f'<text x="0" y="{y+15}" font-size="12" fill="#a7b4c9" font-family="IBM Plex Sans,sans-serif">{E(n)}</text>'
        s += f'<rect x="{lx}" y="{y+2}" width="{bw}" height="18" rx="3" fill="rgba(255,255,255,.04)"/>'
        dim = ' opacity="0.55"' if "Not" in n else ""
        s += f'<rect x="{lx}" y="{y+2}" width="{w:.1f}" height="18" rx="3" fill="{col}"{dim}/>'
        s += f'<text x="{lx+w+8:.1f}" y="{y+15}" font-size="12" fill="#f2f6ff" font-family="JetBrains Mono,monospace">{ms} ms</text>'
    s += "</svg>"
    return figbox(s, '<div class="cap">One production trade, stage by stage · 1,024 ms end to end, of which 292 ms is not instrumented per stage · latest confirmed trade. 31 ms of the engine\'s own work; 621 ms waiting for the chain.</div>')

def fig_cube():
    s = '''<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The replay cube: sources by strategies by chains by regimes">
<defs><linearGradient id="cg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#31d9ff" stop-opacity=".9"/><stop offset="1" stop-color="#a877ff" stop-opacity=".9"/></linearGradient></defs>
<g transform="translate(40,20)">
<polygon points="0,90 120,30 240,90 120,150" fill="rgba(49,217,255,.10)" stroke="#31d9ff" stroke-opacity=".8"/>
<polygon points="0,90 120,150 120,270 0,210" fill="rgba(168,119,255,.10)" stroke="#a877ff" stroke-opacity=".8"/>
<polygon points="120,150 240,90 240,210 120,270" fill="rgba(88,231,173,.08)" stroke="#58e7ad" stroke-opacity=".8"/>
<g stroke="rgba(255,255,255,.14)"><line x1="40" y1="70" x2="160" y2="130"/><line x1="80" y1="50" x2="200" y2="110"/><line x1="60" y1="120" x2="180" y2="60"/><line x1="0" y1="150" x2="120" y2="210"/><line x1="0" y1="180" x2="120" y2="240"/><line x1="120" y1="180" x2="240" y2="120"/><line x1="120" y1="210" x2="240" y2="150"/><line x1="120" y1="240" x2="240" y2="180"/><line x1="40" y1="110" x2="40" y2="230"/><line x1="80" y1="130" x2="80" y2="250"/><line x1="160" y1="130" x2="160" y2="250"/><line x1="200" y1="110" x2="200" y2="230"/></g>
</g>
<g font-family="JetBrains Mono,monospace" font-size="11" fill="#a7b4c9">
<text x="330" y="60"><tspan fill="#31d9ff" font-size="20">300+</tspan> sources ever tracked</text>
<text x="330" y="110"><tspan fill="#a877ff" font-size="20">17</tspan> exit strategies</text>
<text x="330" y="160"><tspan fill="#58e7ad" font-size="20">5</tspan> chains × <tspan fill="#58e7ad" font-size="20">4</tspan> market regimes</text>
<line x1="330" x2="700" y1="185" y2="185" stroke="rgba(255,255,255,.16)"/>
<text x="330" y="222"><tspan fill="#f2f6ff" font-size="26">6.2M</tspan> precomputed rows</text>
<text x="330" y="252" fill="#6b7a94">17,820 tasks · about 25 minutes · every night</text>
</g></svg>'''
    return figbox(s, '<div class="cap">The replay cube · one cell per source × strategy × chain × regime · 6.2M rows, refilled by 17,820 replay tasks a night</div>')

def fig_journey():
    data = json.load(open(JOURNEY))
    W, H, L, B = 760, 260, 28, 34
    n = len(data); gw = (W - L - 10) / n
    mx = max(d["analytics_c"] + d["engine_c"] + d["program_c"] for d in data)
    sc = (H - B - 20) / mx
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Commits per month across three repositories">'
    for t in range(0, mx + 1, 200):
        y = H - B - t * sc
        s += f'<line x1="{L}" x2="{W}" y1="{y:.1f}" y2="{y:.1f}" stroke="rgba(255,255,255,.06)"/><text x="{L-6}" y="{y+4:.1f}" text-anchor="end" font-size="11" fill="#7d8ba3" font-family="JetBrains Mono,monospace">{t}</text>'
    for i, d in enumerate(data):
        x = L + i * gw + 2; w = gw - 4; y = H - B
        for key, col in (("analytics_c", "#31d9ff"), ("engine_c", "#a877ff"), ("program_c", "#58e7ad")):
            h = d[key] * sc
            if h > 0:
                s += f'<rect x="{x:.1f}" y="{y-h:.1f}" width="{w:.1f}" height="{max(h-1.5,0):.1f}" rx="2" fill="{col}"/>'
                y -= h
        if i % 2 == 0:
            s += f'<text x="{x+w/2:.1f}" y="{H-B+16}" text-anchor="middle" font-size="11" fill="#7d8ba3" font-family="JetBrains Mono,monospace">{d["m"][2:4]}·{d["m"][5:]}</text>'
    s += "</svg>"
    leg = '<div class="legend"><span><i style="background:#31d9ff"></i>Analytics · Python</span><span><i style="background:#a877ff"></i>Execution engine · Rust</span><span><i style="background:#58e7ad"></i>On-chain program · Anchor</span></div>'
    return figbox(s, leg + '<div class="cap">Commits per month, from git across the three repositories · Apr 2025 to Sep 2026</div>')

def fig_growth():
    import datetime as dt
    def ts(k):
        parts = k.split("-"); y, m = int(parts[0]), int(parts[1]); d = int(parts[2]) if len(parts) > 2 else 15
        return dt.date(y, m, d).toordinal()
    pts = [(ts(k), v) for k, v in C.GROWTH]
    t0, t1 = pts[0][0], ts("2026-09-10"); mx = 14000
    W, H, L, B = 760, 260, 30, 30
    def X(t): return L + (t - t0) / (t1 - t0) * (W - L - 12)
    def Y(v): return H - B - v / mx * (H - B - 24)
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Lines in the workflow file over time">'
    s += '<defs><linearGradient id="ga" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#31d9ff" stop-opacity=".25"/><stop offset="1" stop-color="#31d9ff" stop-opacity="0"/></linearGradient></defs>'
    for v in (0, 4000, 8000, 12000):
        s += f'<line x1="{L}" x2="{W}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="rgba(255,255,255,.06)"/><text x="{L-6}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="11" fill="#7d8ba3" font-family="JetBrains Mono,monospace">{v//1000}k</text>'
    path = " ".join(f'{"M" if i==0 else "L"}{X(t):.1f},{Y(v):.1f}' for i, (t, v) in enumerate(pts))
    area = path + f' L{X(pts[-1][0]):.1f},{Y(0):.1f} L{X(pts[0][0]):.1f},{Y(0):.1f} Z'
    s += f'<path d="{area}" fill="url(#ga)"/><path d="{path}" fill="none" stroke="#31d9ff" stroke-width="2" stroke-linejoin="round"/>'
    for t, v in pts:
        s += f'<circle cx="{X(t):.1f}" cy="{Y(v):.1f}" r="3.5" fill="#05080f" stroke="#31d9ff" stroke-width="1.5"/>'
    for i, (k, lab) in enumerate(C.GROWTH_FLAGS):
        x = X(ts(k)); yt = (14, 34, 54, 14, 34, 14)[i % 6]
        anchor = "end" if x > W * 0.72 else "start"; dx = -4 if anchor == "end" else 4
        s += f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(0):.1f}" y2="{yt+4}" stroke="rgba(255,255,255,.12)" stroke-dasharray="2 3"/>'
        s += f'<text x="{x+dx:.1f}" y="{yt}" text-anchor="{anchor}" font-size="10.5" fill="#a7b4c9" font-family="JetBrains Mono,monospace">{E(lab)}</text>'
    for k, lab in (("2025-12-01", "Dec 25"), ("2026-03-01", "Mar 26"), ("2026-06-01", "Jun 26"), ("2026-09-01", "Sep 26")):
        s += f'<text x="{X(ts(k)):.1f}" y="{H-8}" text-anchor="middle" font-size="11" fill="#7d8ba3" font-family="JetBrains Mono,monospace">{lab}</text>'
    s += "</svg>"
    return figbox(s, '<div class="cap">Lines in the workflow file, from git · growth is rules added after failures, not features</div>')

# ------------------------------------------------------------------ section renderers
def r_cover(s, study):
    right = ""
    if s.get("shot"):
        right = shot(s["shot"], s["shot_caption"])
    elif s.get("runs"):
        right = ""  # recent-runs list removed by request
    return f'''<section class="hero" id="{s["id"]}"><div class="glow"></div><div class="wrap" data-stagger>
<div class="rv">{kicker(s["kicker"])}</div><h1 class="rv">{E(s["h1"])}</h1><p class="lead rv">{E(s["lead"])}</p>
<div class="actions rv"><a class="btn primary" href="#{s["first"]}">Start reading <span class="a">↓</span></a><a class="btn" href="{LINKS[s["other"][1]]}">{E(s["other"][0])} <span class="a">→</span></a></div>
<div class="authorship rv"><div class="label">A note on authorship</div><p>{E(C.AUTHORSHIP)}</p></div>
</div></section>
<section class="sec" style="border-top:0;padding-top:0"><div class="wrap">{stats(s["metrics"])}{fn(s.get("fn"))}
{f'<div style="margin-top:clamp(2.5rem,5vw,4rem)">{right}</div>' if right else ""}</div></section>'''

def r_journey(s):
    tl = "".join(f'<div class="m rv"><div class="d">{E(d)}</div><div class="t">{E(t)}</div></div>' for d, t in s["milestones"])
    return f'''<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}
<div class="fig">{fig_journey()}</div>
<div class="tl" data-stagger>{tl}</div>{note(E(s["note"]))}</div></section>'''

def r_four(s):
    cards = "".join(f'<div class="card rv"><div class="label">{E(t)}</div><div class="stat" style="border:0;padding:0"><span class="n" style="font-size:clamp(1.75rem,1.2vw + 1.4rem,2.5rem)">{E(n)}</span><span class="l">{E(l)}</span></div><p>{E(p)}</p></div>' for t, n, l, p in s["cards"])
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="cards c4" data-stagger>{cards}</div>{note(E(s["note"]))}</div></section>'

def r_infra(s):
    def node(cls, kick, title, sub, items):
        li = "".join(f"<li>{E(i)}</li>" for i in items)
        return f'<div class="node {cls} rv"><div class="label">{E(kick)}</div><h3>{E(title)}</h3><div class="sub">{E(sub)}</div><ul>{li}</ul></div>'
    feeds = node("v", "External feeds", "Signals in", "raw signals · prices · transactions", [f"{a} · {b}" for a, b in s["feeds"]])
    brain = node("c", "My servers", "Finland · Hetzner", "the brain · Python", s["brain"][1])
    hands = node("c", "My servers · WireGuard tunnel between them", "Nuremberg · Hetzner", "the hands · Rust", s["hands"][1])
    chain = node("g", "On-chain", "Solana mainnet", "signed transactions out · confirmations and live prices back", s["chain"][1])
    leg = '<div class="legend rv"><span><i style="background:var(--violet)"></i>external inputs</span><span><i style="background:var(--accent)"></i>my servers</span><span><i style="background:var(--green)"></i>on-chain</span></div>'
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="infra" data-stagger>{feeds}{brain}{hands}{chain}</div>{leg}{note(E(s["note"]))}</div></section>'

def r_points(s, accent="cyan"):
    vis = ""
    if s.get("visual") == "bytes": vis = fig_bytes()
    elif s.get("visual") == "stages": vis = fig_stages()
    elif s.get("visual") == "cube": vis = fig_cube()
    elif s.get("shot"): vis = shot(s["shot"], s["shot_caption"])
    body = f'<div class="grid2"><div>{points(s["points"])}</div><div>{vis}</div></div>' if vis else points(s["points"])
    return f'''<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}
{body}{metrics(s.get("metrics"))}{fn(s.get("fn"))}{note(E(s["note"])) if s.get("note") else ""}</div></section>'''

def r_controls(s):
    keys = ""
    for title, can, col in s["keys"]:
        li = "".join(f"<li>{E(c)}</li>" for c in can)
        no = f'<div class="no">{E(s["forbidden"])}</div>' if col == "cyan" else '<div class="no ok">the only key that can move funds</div>'
        keys += f'<div class="key {col[0]} rv"><h3>{E(title)}</h3><ul>{li}</ul>{no}</div>'
    rules = '<div class="rules rv"><div class="lab">Rules enforced by the program, not by policy</div>' + "".join(f"<span>{E(r)}</span>" for r in s["rules"]) + "</div>"
    return f'''<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}
<div class="grid2"><div>{points(s["points"])}</div><div data-stagger><div class="keys">{keys}</div>{rules}</div></div>{metrics(s["metrics"])}
{fn("Signing detail: Phantom rewrites the message at signing, so raw-byte binding is impossible. Authorization verifies Ed25519 at the signer's slot index and binds each meaningful field individually.")}</div></section>'''

def r_beforeafter(s):
    cards = ""
    for broke, now, n, l in s["items"]:
        big = (f'<div class="big"><span class="when">{E(n)} · {E(l)}</span></div>' if "2026" in l
               else f'<div class="big"><span class="n">{E(n)}</span><span class="l">{E(l)}</span></div>')
        cards += f'<div class="card rv"><div class="broke"><div class="lab">What broke</div>{E(broke)}</div><div class="now"><div class="lab">What exists now</div>{E(now)}</div>{big}</div>'
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="ba" data-stagger>{cards}</div>{note(E(s["note"]))}</div></section>'

def r_tiles(s):
    t = "".join(f'<div class="card tile rv"><span class="n">{E(n)}</span><div class="l">{E(l)}</div><div class="s">{E(sub)}</div></div>' for n, l, sub in s["tiles"])
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="tiles" data-stagger>{t}</div>{fn(s["note"])}</div></section>'

def r_close(s, study):
    ss = "".join(f'<div class="card rv"><div class="label">0{i+1}</div><h3>{E(t)}</h3><p>{E(p)}</p></div>' for i, (t, p) in enumerate(s["sessions"]))
    team = f'<p class="note rv">{E(s["team"])}</p>' if s.get("team") else ""
    nt, nh = s["next"]
    return f'''<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}
<div style="margin-top:clamp(2rem,4vw,3rem)">{BN.pulse()}</div>
<div class="sessions" data-stagger style="margin-top:14px">{ss}</div>
{note('<span class="kicker">the boundary</span>' + E(s.get("boundary", C.BOUNDARY)))}{team}
<div style="margin-top:clamp(2.5rem,5vw,4rem)">{who()}</div>
<div class="nextlink rv"><a class="card" href="{LINKS[nh]}"><div><div class="label">Next</div><h3 style="margin-top:.5rem">{E(nt)}</h3></div><span class="arrow">Open <span class="a">→</span></span></a></div>
</div></section>'''

def r_growth(s):
    tl = ""
    if s.get("milestones"):
        tl = '<div class="tl" data-stagger>' + "".join(f'<div class="m rv"><div class="d">{E(d)}</div><div class="t">{E(t)}</div></div>' for d, t in s["milestones"]) + "</div>"
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="fig">{fig_growth()}</div>{tl}{note(E(s["note"]))}</div></section>'

def r_loop(s):
    st = ""
    for i, (t, p, mine, ev) in enumerate(s["stages"]):
        pill = '<span class="pill me">My decision</span>' if mine else ""
        st += f'<div class="card stage rv">{pill}<div class="idx">0{i+1}</div><h3>{E(t)}</h3><p>{E(p)}</p><div class="ev"><b>Evidence left behind</b>{E(ev)}</div></div>'
    routes = '<div class="routes rv">' + "".join(f"<span><b>{E(a)}</b> · {E(b)}</span>" for a, b in s["routes"]) + "</div>"
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="loop" data-stagger>{st}</div>{routes}{note(E(s["note"]))}</div></section>'

def r_reviewers(s):
    lanes = ""
    for i, (t, items) in enumerate(s["lanes"]):
        li = "".join(f'<li{" class=x" if "·" in it and i == 1 else ""}>{E(it)}</li>' for it in items)
        lanes += f'<div class="card lane{" ext" if i == 2 else ""} rv"><div class="label">{E(t)}</div><ul>{li}</ul></div>'
    return f'''<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}
<div class="grid2 rev"><div>{points(s["points"])}</div><div class="rv"><p class="quote">“You are the auditor, not a rubber stamp.”</p><p class="cap">The instruction every reviewer receives, verbatim.</p></div></div>
<div class="lanes" data-stagger>{lanes}</div>{metrics(s["metrics"])}</div></section>'''

def r_knowledge(s):
    cols = ""
    for t, sub, items in s["columns"]:
        li = "".join(f"<li>{E(i)}</li>" for i in items)
        cols += f'<div class="col rv"><h3>{E(t)}</h3><div class="sub">{E(sub)}</div><ul>{li}</ul></div>'
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="cols" data-stagger>{cols}</div><div style="margin-top:clamp(2rem,4vw,3.5rem)">{points(s["points"])}</div>{metrics(s["metrics"])}</div></section>'

def r_scorecards(s):
    rows = ""
    for l, a, b, sub in s["rows"]:
        pct = a / b * 100
        rows += f'<div class="row{" part" if a < b else ""}"><span class="l">{E(l)}</span><span class="v">{a} / {b}</span><div class="b"><i style="--w:{pct:.0f}%"></i></div>{f"<span class=s>{E(sub)}</span>" if sub else ""}</div>'
    lin = "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in s["lineages"])
    return f'''<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}
<div class="grid2"><div class="card rv"><div class="label">{E(s["card_caption"])}</div><div class="score" style="margin-top:1rem">{rows}</div></div>
<div class="rv"><div class="label" style="margin-bottom:.5rem">Who does what · five model lineages</div><ul class="lineage">{lin}</ul></div></div>
{metrics(s["metrics"])}{note(E(s["note"]))}</div></section>'''

def r_gates(s):
    g = "".join(f'<div class="card gate rv"><div class="lab">The claim</div><div class="claim">{E(c)}</div><div class="lab">What the workflow does</div><div class="does">{E(d)}</div></div>' for c, d in s["gates"])
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="gates" data-stagger>{g}</div>{metrics(s["metrics"])}{note(E(s["note"]))}</div></section>'

def r_memory(s):
    ch = "".join(f'<div class="c rv"><h3>{E(t)}</h3><p>{E(p)}</p></div>' for t, p in s["chain"])
    gl = "".join(f"<li><b>{E(a)}</b>{E(b)}</li>" for a, b in s["gap"])
    return f'''<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="chain" data-stagger>{ch}</div>
<div class="card gaplife rv"><div class="label">{E(s["gap_caption"])}</div><ol>{gl}</ol></div>{metrics(s["metrics"])}{note(E(s["note"]))}</div></section>'''

RENDER = dict(journey=r_journey, four=r_four, infra=r_infra, points=r_points, controls=r_controls, beforeafter=r_beforeafter,
              tiles=r_tiles, growth=r_growth, loop=r_loop, reviewers=r_reviewers, knowledge=r_knowledge, scorecards=r_scorecards,
              gates=r_gates, memory=r_memory)

# ------------------------------------------------------------------ v6 renderers (case study 2 rebuild)
LANE_CLASS = {"Claude Opus": "opus", "Claude Sonnet": "opus", "OpenAI Codex": "codex", "xAI Grok": "grok", "script": "script", "me": "me", "Me": "me"}

def r_steps(s):
    out = []
    for ph in s["phases"]:
        items = ""
        for st in ph["steps"]:
            tags = "".join(f'<span class="tag {LANE_CLASS.get(w, "")}">{E(w)}</span>' for w in st.get("who", []))
            dl = ""
            if st.get("reads"): dl += f'<dt>Must read first</dt><dd>{E(st["reads"])}</dd>'
            if st.get("leaves"): dl += f'<dt>Evidence left behind</dt><dd>{E(st["leaves"])}</dd>'
            if st.get("block"): dl += f'<dt>Stops the run when</dt><dd class="block">{E(st["block"])}</dd>'
            if st.get("mine"): dl += f'<dt>My decision</dt><dd class="me">{E(st["mine"])}</dd>'
            items += ('<details class="acc rv"><summary><span class="i">' + E(st["id"]) + '</span><span class="t">' + E(st["title"]) + '<small>' + E(st.get("sub", "")) + '</small></span><span class="c" aria-hidden="true"></span></summary>'
                      '<div class="dbody"><div><div class="in"><div><p>' + E(st["what"]) + '</p><div style="margin-top:.6rem">' + tags + '</div></div><dl>' + dl + '</dl></div></div></div></details>')
        out.append(f'<div class="phase rv"><div class="ph"><span class="num">{E(ph["num"])}</span><h3>{E(ph["title"])}</h3><span class="who">{E(ph.get("who", ""))}</span></div>{items}</div>')
    btn = '<div style="margin-top:clamp(1.5rem,3vw,2rem)"><button class="expand-all" type="button">Expand all steps</button></div>'
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}{btn}{"".join(out)}{metrics(s.get("metrics"))}{fn(s.get("fn"))}{note(E(s["note"])) if s.get("note") else ""}</div></section>'

def r_flow(s):
    bx = "".join(f'<div class="fx rv"><div class="label">{E(l)}</div><h3>{E(t)}</h3><p>{E(p)}</p><span class="ar"></span></div>' for l, t, p in s["boxes"])
    pts = f'<div style="margin-top:clamp(2rem,4vw,3rem)">{points(s["points"])}</div>' if s.get("points") else ""
    pn = f'<div style="margin-top:clamp(2rem,4vw,3rem)">{pane(s["pane"], s.get("pane_cap"))}</div>' if s.get("pane") else ""
    cls = " c3" if len(s["boxes"]) == 6 else ""
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="flow{cls}" data-stagger>{bx}</div>{pts}{pn}{metrics(s.get("metrics"))}{fn(s.get("fn"))}{note(E(s["note"])) if s.get("note") else ""}</div></section>'

def r_matrix(s):
    th = "".join(f"<th>{E(c)}</th>" for c in s["cols"])
    tr = ""
    for row in s["rows"]:
        name, col, *cells = row
        tr += f'<tr><td><span class="dot" style="background:{col}"></span>{E(name)}</td>' + "".join(f"<td>{E(c)}</td>" for c in cells) + "</tr>"
    pts = f'<div style="margin-top:clamp(2rem,4vw,3rem)">{points(s["points"])}</div>' if s.get("points") else ""
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}<div class="tablewrap rv"><table class="matrix"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>{pts}{metrics(s.get("metrics"))}{fn(s.get("fn"))}{note(E(s["note"])) if s.get("note") else ""}</div></section>'

def r_funnel(s):
    fr = "".join(f'<div class="fr"><span class="n">{E(n)}</span><div class="b"><i style="--w:{p}%"></i></div><span class="l">{E(l)}</span></div>' for n, l, p in s["rows"])
    pn = pane(s["pane"], s.get("pane_cap")) if s.get("pane") else ""
    return (f'<section class="sec" id="{s["id"]}"><div class="wrap">{head(s)}'
            f'<div class="grid2"><div class="rv"><div class="funnel">{fr}</div></div><div>{points(s["points"])}</div></div>'
            f'<div style="margin-top:clamp(2rem,4vw,3rem)">{pn}</div>{metrics(s.get("metrics"))}{fn(s.get("fn"))}{note(E(s["note"])) if s.get("note") else ""}</div></section>')

RENDER.update(dict(steps=r_steps, flow=r_flow, matrix=r_matrix, funnel=r_funnel))

# ------------------------------------------------------------------ v8: progressive disclosure overrides
def more(inner_html, label="Read more", two=False):
    if not inner_html.strip(): return ""
    return (f'<details class="more rv"><summary><span class="def">{E(label)}</span><span class="alt">Show less</span><span class="c" aria-hidden="true"></span></summary>'
            f'<div class="dbody"><div><div class="inner{" two" if two else ""}">{inner_html}</div></div></div></details>')

def desc(s):
    return f'<p class="summ rv">{E(s["summ"])}</p>' if s.get("summ") else ""

def head8(s):
    lead = f'<p class="lead rv">{E(s["lead"])}</p>' if s.get("lead") else ""
    return f'<div class="head" data-stagger><div class="rv">{kicker(s["kicker"])}</div><h2 class="rv">{E(s["h1"])}</h2>{lead}</div>'

def notes(s):
    return (fn(s.get("fn")) if s.get("fn") else "") + (note(E(s["note"])) if s.get("note") else "")

def r_growth(s):
    tl = ""
    if s.get("milestones"):
        tl = '<div class="tl" data-stagger>' + "".join(f'<div class="m rv"><div class="d">{E(d)}</div><div class="t">{E(t)}</div></div>' for d, t in s["milestones"]) + "</div>"
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div class="fig">{fig_growth()}</div>{more(tl + notes(s), "The milestones")}</div></section>'

def r_journey(s):
    tl = "".join(f'<div class="m rv"><div class="d">{E(d)}</div><div class="t">{E(t)}</div></div>' for d, t in s["milestones"])
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div class="fig">{fig_journey()}</div>{more(f"<div class=tl data-stagger>{tl}</div>" + notes(s), "The milestones")}</div></section>'

def r_four(s):
    cards = "".join(f'<div class="card rv"><div class="label">{E(t)}</div><div class="stat" style="border:0;padding:0"><span class="n" style="font-size:clamp(1.75rem,1.2vw + 1.4rem,2.5rem)">{E(n)}</span><span class="l">{E(l)}</span></div><p>{E(p)}</p></div>' for t, n, l, p in s["cards"])
    sh = shot(s["shot"], s["shot_caption"]) if s.get("shot") else ""
    bn = BN.BANNERS[s["banner"]]() if s.get("banner") else ""
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div style="margin-top:clamp(2rem,4vw,3rem)">{bn}</div><div class="cards c4" data-stagger style="margin-top:14px">{cards}</div>{more(sh + notes(s), "See it on the dashboard")}</div></section>'

def r_infra(s):
    def node(cls, kick, title, sub, items):
        li = "".join(f"<li>{E(i)}</li>" for i in items)
        return f'<div class="node {cls} rv"><div class="label">{E(kick)}</div><h3>{E(title)}</h3><div class="sub">{E(sub)}</div><ul>{li}</ul></div>'
    feeds = node("v", "External feeds", "Signals in", "raw signals · prices · transactions", [f"{a} · {b}" for a, b in s["feeds"]])
    brain = node("c", "My servers", "Finland · Hetzner", "the brain · Python", s["brain"][1])
    hands = node("c", "My servers · WireGuard tunnel between them", "Nuremberg · Hetzner", "the hands · Rust", s["hands"][1])
    chain = node("g", "On-chain", "Solana mainnet", "signed transactions out · confirmations and live prices back", s["chain"][1])
    leg = '<div class="legend rv"><span><i style="background:var(--violet)"></i>external inputs</span><span><i style="background:var(--accent)"></i>my servers</span><span><i style="background:var(--green)"></i>on-chain</span></div>'
    bn = BN.servers()
    hidden = f'<div class="infra" data-stagger>{feeds}{brain}{hands}{chain}</div>{leg}' + notes(s)
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div style="margin-top:clamp(2rem,4vw,3rem)">{bn}</div>{more(hidden, "The full map, box by box")}</div></section>'

def r_points(s, accent=None):
    vis = ""
    if s.get("visual") == "bytes": vis = fig_bytes()
    elif s.get("visual") == "stages": vis = fig_stages()
    elif s.get("visual") == "cube": vis = fig_cube()
    elif s.get("visual") == "routing": vis = fig_routing()
    elif s.get("banner"): vis = BN.BANNERS[s["banner"]]()
    elif s.get("shot"): vis = shot(s["shot"], s["shot_caption"])
    figs = []
    if s.get("visual2") == "bytes": figs.append(fig_bytes())
    for nm, cp in s.get("shots", []): figs.append(shot(nm, cp))
    extra = f'<div class="figs two" data-stagger>{"".join(figs)}</div>' if figs else ""
    hidden = points(s["points"]) + extra + notes(s)
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}{desc(s)}<div style="margin-top:clamp(2rem,4vw,3rem)">{vis}</div>{metrics(s.get("metrics"))}{more(hidden, s.get("more_label", "How it works"))}</div></section>'

def r_controls(s):
    keys = ""
    for title, can, col in s["keys"]:
        li = "".join(f"<li>{E(c)}</li>" for c in can)
        no = f'<div class="no">{E(s["forbidden"])}</div>' if col == "cyan" else ""
        keys += f'<div class="key {col[0]} rv"><h3>{E(title)}</h3><ul>{li}</ul>{no}</div>'
    rules = '<div class="rules rv"><div class="lab">Rules enforced by the program, not by policy</div>' + "".join(f"<span>{E(r)}</span>" for r in s["rules"]) + "</div>"
    hidden = points(s["points"]) + rules + fn("Signing detail: Phantom rewrites the message at signing, so raw-byte binding is impossible. Authorization verifies Ed25519 at the signer's slot index and binds each meaningful field individually.")
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}{desc(s)}<div class="keys" data-stagger style="margin-top:clamp(2rem,4vw,3rem)">{keys}</div>{metrics(s["metrics"])}{more(hidden, "How the program enforces it")}</div></section>'

def ba_cards(items):
    cards = ""
    for broke, now, n, l in items:
        big = (f'<div class="big"><span class="n">{E(n)}</span><span class="l">{E(l)}</span></div>' if not n.startswith("Run") and not n[0].isdigit() or "×" in n or "," in n
               else f'<div class="big"><span class="when">{E(n)} · {E(l)}</span></div>')
        cards += f'<div class="card rv"><div class="broke"><div class="lab">What broke</div>{E(broke)}</div><div class="now"><div class="lab">What exists now</div>{E(now)}</div>{big}</div>'
    return cards

def r_beforeafter(s):
    first, rest = s["items"][:3], s["items"][3:]
    hidden = (f'<div class="ba" data-stagger>{ba_cards(rest)}</div>' if rest else "") + notes(s)
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}{desc(s)}<div class="ba" data-stagger style="margin-top:clamp(2rem,4vw,3rem)">{ba_cards(first)}</div>{more(hidden, f"{len(rest)} more" if rest else "In their own words")}</div></section>'

def r_tiles(s):
    t = "".join(f'<div class="card tile rv"><span class="n">{E(n)}</span><div class="l">{E(l)}</div><div class="s">{E(sub)}</div></div>' for n, l, sub in s["tiles"])
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}{desc(s)}<div class="tiles" data-stagger style="margin-top:clamp(2rem,4vw,3rem)">{t}</div>{more(fn(s["note"]), "Where the numbers come from")}</div></section>'

def r_flow(s):
    bx = "".join(f'<div class="fx rv"><div class="label">{E(l)}</div><h3>{E(t)}</h3><p>{E(p)}</p><span class="ar"></span></div>' for l, t, p in s["boxes"])
    cls = " c3" if len(s["boxes"]) == 6 else ""
    flow = f'<div class="flow{cls}" data-stagger>{bx}</div>'
    pts = points(s["points"]) if s.get("points") else ""; pn = pane(s["pane"], s.get("pane_cap")) if s.get("pane") else ""
    if s.get("banner"):
        vis = f'<div style="margin-top:clamp(2rem,4vw,3rem)">{BN.BANNERS[s["banner"]]()}</div>'
        hidden = flow + (f'<div class="inner two" style="padding:0">{pts}{pn}</div>' if (pts and pn) else pts + pn) + notes(s)
        return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}{vis}{metrics(s.get("metrics"))}{more(hidden, s.get("more_label", "Read more"))}</div></section>'
    hidden = (f'<div class="inner two" style="padding:0">{pts}{pn}</div>' if (pts and pn) else pts + pn) + notes(s)
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div style="margin-top:clamp(2rem,4vw,3rem)">{flow}</div>{metrics(s.get("metrics"))}{more(hidden, s.get("more_label", "Read more"))}</div></section>'

def r_matrix(s):
    strip = '<div class="lanes-strip" data-stagger>' + "".join(f'<div class="ln rv"><b><i style="background:{col}"></i>{E(name)}</b><span>{E(short)}</span></div>' for name, col, short in s["strip"]) + "</div>"
    th = "".join(f"<th>{E(c)}</th>" for c in s["cols"])
    tr = ""
    for row in s["rows"]:
        name, col, *cells = row
        tr += f'<tr><td><span class="dot" style="background:{col}"></span>{E(name)}</td>' + "".join(f"<td>{E(c)}</td>" for c in cells) + "</tr>"
    table = f'<div class="tablewrap"><table class="matrix"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    hidden = table + (points(s["points"]) if s.get("points") else "") + notes(s)
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div style="margin-top:clamp(2rem,4vw,3rem)">{strip}</div>{metrics(s.get("metrics"))}{more(hidden, "Who caught what")}</div></section>'

def r_funnel(s):
    fr = "".join(f'<div class="fr"><span class="n">{E(n)}</span><div class="b"><i style="--w:{p}%"></i></div><span class="l">{E(l)}</span></div>' for n, l, p in s["rows"])
    hidden = points(s["points"]) + (pane(s["pane"], s.get("pane_cap")) if s.get("pane") else "") + notes(s)
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div class="rv" style="margin-top:clamp(2rem,4vw,3rem);max-width:44rem"><div class="funnel">{fr}</div></div>{more(hidden, "The triage rule, and four gaps that became rules", two=True)}</div></section>'

def r_scorecards(s):
    rows = ""
    for l, a, b, sub in s["rows"]:
        pct = a / b * 100
        rows += f'<div class="row{" part" if a < b else ""}"><span class="l">{E(l)}</span><span class="v">{a} / {b}</span><div class="b"><i style="--w:{pct:.0f}%"></i></div>{f"<span class=s>{E(sub)}</span>" if sub else ""}</div>'
    lin = "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in s["lineages"])
    hidden = f'<div><div class="label" style="margin-bottom:.5rem">Who does what · five model lineages</div><ul class="lineage">{lin}</ul></div>' + notes(s)
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div class="grid2" style="margin-top:clamp(2rem,4vw,3rem)"><div class="card rv"><div class="label">{E(s["card_caption"])}</div><div class="score" style="margin-top:1rem">{rows}</div></div><div class="rv"><div class="label" style="margin-bottom:.5rem">Who does what · five lanes</div><ul class="lineage">{lin}</ul></div></div>{metrics(s.get("metrics"))}{more(notes(s), "How the rubric works")}</div></section>'

def r_gates(s):
    g = "".join(f'<div class="card gate rv"><div class="lab">The claim</div><div class="claim">{E(c)}</div><div class="lab">What the workflow does</div><div class="does">{E(d)}</div></div>' for c, d in s["gates"][:3])
    g2 = "".join(f'<div class="card gate rv"><div class="lab">The claim</div><div class="claim">{E(c)}</div><div class="lab">What the workflow does</div><div class="does">{E(d)}</div></div>' for c, d in s["gates"][3:])
    hidden = (f'<div class="gates" data-stagger>{g2}</div>' if g2 else "") + (pane(s["pane"], s.get("pane_cap")) if s.get("pane") else "") + notes(s)
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}<div style="margin-top:clamp(2rem,4vw,3rem)">{BN.gate()}</div><div class="gates" data-stagger style="margin-top:14px">{g}</div>{metrics(s.get("metrics"))}{more(hidden, "Three more, and the gates in the file")}</div></section>'

def r_steps(s):
    out = []
    for ph in s["phases"]:
        items = ""
        for st_ in ph["steps"]:
            tags = "".join(f'<span class="tag {LANE_CLASS.get(w, "")}">{E(w)}</span>' for w in st_.get("who", []))
            dl = ""
            if st_.get("reads"): dl += f'<dt>Must read first</dt><dd>{E(st_["reads"])}</dd>'
            if st_.get("leaves"): dl += f'<dt>Evidence left behind</dt><dd>{E(st_["leaves"])}</dd>'
            if st_.get("block"): dl += f'<dt>Stops the run when</dt><dd class="block">{E(st_["block"])}</dd>'
            if st_.get("mine"): dl += f'<dt>My decision</dt><dd class="me">{E(st_["mine"])}</dd>'
            items += ('<details class="acc"><summary><span class="i">' + E(st_["id"]) + '</span><span class="t">' + E(st_["title"]) + '<small>' + E(st_.get("sub", "")) + '</small></span><span class="c" aria-hidden="true"></span></summary>'
                      '<div class="dbody"><div><div class="in' + ('' if dl else ' one') + '"><div><p>' + E(st_["what"]) + '</p><div style="margin-top:.6rem">' + tags + '</div></div>' + ('<dl>' + dl + '</dl>' if dl else '') + '</div></div></div></details>')
        n = len(ph["steps"])
        out.append(f'<details class="phase-acc rv"><summary><span class="num">{E(ph["num"])}</span><h3>{E(ph["title"])}</h3><span class="owner">{E(ph.get("who", ""))}</span><span class="cnt">{n} steps</span><span class="chev" aria-hidden="true"></span></summary><div class="dbody"><div>{items}</div></div></details>')
    ribbon = fig_loop(s["ribbon"]) if s.get("ribbon") else ""
    btn = '<div style="margin:clamp(1.5rem,3vw,2rem) 0 .5rem"><button class="expand-all" type="button" aria-expanded="false" aria-controls="phases">Expand every phase and step</button></div>'
    return f'<section class="sec" id="{s["id"]}"><div class="wrap">{head8(s)}{ribbon}{btn}<div id="phases">{"".join(out)}</div>{metrics(s.get("metrics"))}{more(notes(s), "About the numbering")}</div></section>'

def fig_routing():
    rows = [("Before routing: every lane at maximum", 100, "#7d8ba3", "100%"), ("Standard runs after routing", 42.5, "#31d9ff", "42.5%"), ("Deep reviews after routing", 15.2, "#a877ff", "15.2%"), ("Money-moving work, always", 100, "#58e7ad", "100%")]
    W, lx, bw = 720, 270, 380; H = 34 * len(rows) + 10
    s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Review cost before and after routing">'
    for i, (n, pct, col, lab) in enumerate(rows):
        y = i * 34 + 6; w = pct / 100 * bw
        s += f'<text x="0" y="{y+15}" font-size="12" fill="#a7b4c9" font-family="IBM Plex Sans,sans-serif">{E(n)}</text>'
        s += f'<rect x="{lx}" y="{y+2}" width="{bw}" height="18" rx="3" fill="rgba(255,255,255,.04)"/><rect x="{lx}" y="{y+2}" width="{w:.1f}" height="18" rx="3" fill="{col}"/>'
        s += f'<text x="{lx+bw+10}" y="{y+15}" font-size="12" fill="#f2f6ff" font-family="JetBrains Mono,monospace">{E(lab)}</text>'
    s += "</svg>"
    return figbox(s, '<div class="cap">Token use per review as a share of the pre-routing control run, which consumed about 13.4 million tokens. From the routing A/B recorded in the repository.</div>')

def r_cover(s, study):
    right = ""
    if s.get("shot"): right = shot(s["shot"], s["shot_caption"], tilt=True)
    elif s.get("ribbon"): right = fig_loop(s["ribbon"])
    return f'''<section class="hero" id="{s["id"]}"><div class="glow"></div><div class="wrap" data-stagger>
<div class="rv">{kicker(s["kicker"])}</div><h1 class="rv">{E(s["h1"])}</h1><p class="lead rv">{E(s["lead"])}</p>
<div class="actions rv"><a class="btn primary" href="#{s["first"]}">Start reading <span class="a">↓</span></a><a class="btn" href="{LINKS[s["other"][1]]}">{E(s["other"][0])} <span class="a">→</span></a></div>
</div></section>
<section class="sec" style="border-top:0;padding-top:0"><div class="wrap">{stats(s["metrics"])}{more(fn(s.get("fn")), "Populations and dates")}
{f'<div style="margin-top:clamp(2.5rem,5vw,4rem)">{right}</div>' if right else ""}</div></section>'''

RENDER.update(dict(journey=r_journey, four=r_four, infra=r_infra, points=r_points, controls=r_controls, beforeafter=r_beforeafter,
                   tiles=r_tiles, growth=r_growth, flow=r_flow, matrix=r_matrix, funnel=r_funnel, scorecards=r_scorecards, gates=r_gates, steps=r_steps))

# ------------------------------------------------------------------ page chrome
LINKS = {"index.html": "index.html", "the-system.html": "the-system.html", "how-i-ship.html": "how-i-ship.html"}

def nav(current):
    def tab(href, num, lbl):
        on = href == current
        al = {"index.html": "Home", "the-system.html": "Case study 1: The system", "how-i-ship.html": "Case study 2: How I ship"}[href]
        return f'<a href="{LINKS[href]}" class="{"on" if on else ""}" aria-label="{al}"{" aria-current=page" if on else ""}><span class="num">{num}</span><span class="lbl">{lbl}</span></a>'
    return f'''<a class="skip" href="#content">Skip to content</a><nav class="nav" aria-label="Primary"><div class="wrap"><a class="brand" href="{LINKS["index.html"]}"><b>{E(C.NAME)}</b><span class="x"> · case studies</span></a>
<div class="tabs">{tab("index.html", "Home", "")}{tab("the-system.html", "01", "The system")}{tab("how-i-ship.html", "02", "How I ship")}</div></div><div class="bar"></div></nav>'''

def footer():
    return f'''<footer class="foot"><div class="wrap"><p>Specified, reviewed and released by {E(C.NAME)}. Implemented by AI models under the delivery workflow in case study 2. Numbers measured on the production system, the run archive and git, {E(C.DATE)}. Replay and simulation figures are analytical outputs, not returns.</p><p>{(C.CONTACT_HTML + " · ") if C.CONTACT_HTML else ""}{E(C.LOCATION)} · 2026</p></div></footer>'''

BASE = None  # public base URL, e.g. https://tijan87.github.io/skynet-case-studies ; set with --base-url
INDEX = True  # --index removes the noindex robots meta

def meta(title, desc, current):
    m = "" if INDEX else '<meta name="robots" content="noindex">'
    if BASE:
        url = BASE.rstrip("/") + "/" + ("" if current == "index.html" else current)
        m += (f'<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:url" content="{url}">'
              f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">'
              f'<meta property="og:image" content="{BASE.rstrip("/")}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
              f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BASE.rstrip("/")}/og.png">')
    return m

def page(title, body, current, desc, cls=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">{meta(title, desc, current)}
<meta name="color-scheme" content="dark"><meta name="theme-color" content="#05080f"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2305080f'/%3E%3Ccircle cx='16' cy='16' r='6' fill='%2331d9ff'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=IBM+Plex+Sans:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap">
<style>{CSS}</style></head><body class="{cls}"><div class="ground"></div>{nav(current)}<main id="content">{body}</main>{footer()}<script>{JS}</script></body></html>'''

def study_page(S):
    parts = []
    for s in S["sections"]:
        k = s["kind"]
        if k == "cover": parts.append(r_cover(s, S))
        elif k == "close": parts.append(r_close(s, S))
        else: parts.append(RENDER[k](s))
    body = "".join(parts)
    return page(f"{C.NAME} · {S['title']}", body, S["slug"] + ".html", S["subtitle"])

def landing():
    L = C.LANDING
    cards = ""
    for c in L["cards"]:
        nums = "".join(f'<div><span class="n">{E(n)}</span><span class="l">{E(l)}</span></div>' for n, l in c["nums"])
        mini = BN.mini_system() if c["n"] == "01" else BN.mini_loop()
        cards += f'''<a class="card rv" href="{LINKS[c["href"]]}">{mini}<div class="label">Case study {c["n"]} · {E(c["who"])}</div><h2>{E(c["title"])}</h2><p>{E(c["text"])}</p><div class="nums">{nums}</div><span class="arrow">Open case study {c["n"][-1]} <span class="a">→</span></span></a>'''
    body = f'''<section class="hero"><div class="glow"></div><div class="wrap" data-stagger><div class="rv">{kicker(L["kicker"])}</div><h1 class="rv">{E(L["h1"])}</h1><p class="lead rv">{E(L["lead"])}</p><p class="cap rv" style="margin-top:1rem">{E(L["boundary"])}</p>
<div class="stats hero-stats rv" style="margin-top:2rem">{"".join(f'<div class="stat"><span class="n">{E(n)}</span><span class="l">{E(l)}</span></div>' for n, l in L["stats"])}</div>
<div class="actions rv"><a class="btn primary" href="{LINKS["the-system.html"]}">01 · The system <span class="a">→</span></a><a class="btn" href="{LINKS["how-i-ship.html"]}">02 · How I ship <span class="a">→</span></a></div>
<div class="authorship rv"><div class="label">A note on authorship</div><p>{E(C.AUTHORSHIP)}</p></div></div></section>
<section class="sec"><div class="wrap">{who()}{more(fn(L["fn"]), "Populations and dates")}</div></section>
<section class="sec"><div class="wrap"><div class="pick" data-stagger>{cards}</div></div></section>'''
    return page(f"{C.NAME} · Case studies", body, "index.html", "Two case studies: a live Solana trading system, and the AI delivery workflow that ships it.", "land")

def main():
    out = os.path.join(HERE, "out"); links = None
    a = sys.argv[1:]
    if "--out" in a: out = a[a.index("--out") + 1]
    if "--links" in a: links = json.load(open(a[a.index("--links") + 1]))
    global BASE, INDEX
    if "--base-url" in a: BASE = a[a.index("--base-url") + 1]
    INDEX = "--index" in a
    if links: LINKS.update(links)
    os.makedirs(out, exist_ok=True)
    pages = {"index.html": landing(), "the-system.html": study_page(C.S1), "how-i-ship.html": study_page(C.S2)}
    art = "--artifact" in a
    for n, h in pages.items():
        if art:  # the Artifact host wraps the page in its own document skeleton: keep head bits + body inner only
            head = h[h.index("<title>"):h.index("</head>")]
            body = h[h.index("<body"):]
            body = body[body.index(">") + 1:]
            cls = "land" if 'class="land"' in h else ""
            body = body[:body.rindex("</body>")]
            h = head + f'<div class="{cls}">' + body + "</div>"
            h = h.replace('href="index.html"', f'href="{LINKS["index.html"]}"')
        open(os.path.join(out, n), "w").write(h)
        print(n, len(h) // 1024, "KB")

if __name__ == "__main__":
    main()
