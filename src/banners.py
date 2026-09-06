# Custom section visuals: one consistent language (dotted field, hairline boxes, gradient wires, glowing nodes, few mono labels).
from html import escape as E

CY, VI, GR, INK, INK2, INK3, RED = "#31d9ff", "#a877ff", "#58e7ad", "#f2f6ff", "#a7b4c9", "#7d8ba3", "#ff8f8f"
MONO = "JetBrains Mono,monospace"; SANS = "IBM Plex Sans,sans-serif"

def defs(p, W=720):
    return (f'<defs><linearGradient id="{p}w" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0"><stop offset="0" stop-color="{VI}"/><stop offset=".55" stop-color="{CY}"/><stop offset="1" stop-color="{GR}"/></linearGradient>'
            f'<linearGradient id="{p}h" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0"><stop offset="0" stop-color="{VI}" stop-opacity=".7"/><stop offset=".5" stop-color="{CY}" stop-opacity=".8"/><stop offset="1" stop-color="{GR}" stop-opacity=".6"/></linearGradient>'
            f'<radialGradient id="{p}g"><stop offset="0" stop-color="{CY}" stop-opacity=".22"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="{p}gv"><stop offset="0" stop-color="{VI}" stop-opacity=".18"/><stop offset="1" stop-color="{VI}" stop-opacity="0"/></radialGradient>'
            f'<filter id="{p}b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>'
            f'<pattern id="{p}d" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="{INK2}" fill-opacity=".16"/></pattern></defs>')

def field(p, W, H, glows=((0.2, 0.1, "g"), (0.85, 0.9, "gv"))):
    s = f'<rect width="{W}" height="{H}" fill="url(#{p}d)"/>'
    for fx, fy, g in glows:
        s += f'<circle cx="{fx*W:.0f}" cy="{fy*H:.0f}" r="{H*0.9:.0f}" fill="url(#{p}{g})"/>'
    return s

def box(p, x, y, w, h, title, sub=None, accent=None, small=False):
    a = accent or CY
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#0b1220" fill-opacity=".92" stroke="url(#{p}h)" stroke-opacity=".75"/>'
         f'<rect x="{x+12}" y="{y}" width="{w-24}" height="1" fill="{a}" fill-opacity=".9"/>')
    fs = 11 if small else 12.5
    s += f'<text x="{x+14}" y="{y+ (22 if small else 26)}" font-size="{fs}" font-weight="500" fill="{INK}" font-family="{SANS}">{E(title)}</text>'
    if sub: s += f'<text x="{x+14}" y="{y+(38 if small else 44)}" font-size="9.5" fill="{INK3}" font-family="{MONO}">{E(sub)}</text>'
    return s

def wire(p, pts, dashed=False, w=1.5):
    d = " ".join(f"{x},{y}" for x, y in pts)
    extra = ' stroke-dasharray="3 5"' if dashed else ""
    return (f'<polyline points="{d}" fill="none" stroke="url(#{p}w)" stroke-width="{w*3}" stroke-opacity=".18" filter="url(#{p}b)" stroke-linejoin="round"/>'
            f'<polyline points="{d}" fill="none" stroke="url(#{p}w)" stroke-width="{w}" stroke-linejoin="round"{extra}/>')

def dot(p, x, y, c=CY, r=4):
    return f'<circle cx="{x}" cy="{y}" r="{r*2.4:.1f}" fill="{c}" fill-opacity=".28" filter="url(#{p}b)"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'

def ring(p, x, y, c=INK2, r=4):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#05080f" stroke="{c}" stroke-width="1.5"/>'

def chip(p, x, y, text, c=INK2, w=None):
    w = w or (len(text) * 6.3 + 18)
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="20" rx="10" fill="#0b1220" fill-opacity=".9" stroke="{c}" stroke-opacity=".45"/>'
            f'<text x="{x+w/2:.0f}" y="{y+13.5}" text-anchor="middle" font-size="9.5" letter-spacing="1" fill="{c}" font-family="{MONO}">{E(text.upper())}</text>')

def label(x, y, text, c=INK3, anchor="start", size=9.5):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" letter-spacing="1" fill="{c}" font-family="{MONO}">{E(text.upper())}</text>'

def svg(p, W, H, body, aria):
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{E(aria)}">{defs(p, W)}{body}</svg>'

def wrap(inner, cls="banner"):
    return f'<div class="{cls} rv">{inner}</div>'

# ---------------------------------------------------------------- banners (720 × 200)
def pipeline():
    p, W, H = "pp", 720, 200
    b = field(p, W, H)
    b += chip(p, 24, 44, "Telegram", VI, 90) + chip(p, 24, 90, "Tracked wallets", VI, 120) + chip(p, 24, 136, "Live prices", VI, 100)
    b += wire(p, [(114, 54), (150, 54), (176, 100), (200, 100)]) + wire(p, [(144, 100), (200, 100)]) + wire(p, [(124, 146), (150, 146), (176, 100)])
    b += box(p, 200, 66, 166, 68, "Detect and rank", "8 workers · 17 strategies")
    b += wire(p, [(366, 100), (404, 100)]) + box(p, 404, 66, 150, 68, "Rust engine", "66 ms engine time")
    b += wire(p, [(554, 100), (592, 100)]) + box(p, 592, 66, 104, 68, "Solana", "on-chain · caps", GR)
    b += f'<path d="M200,152 L696,152" stroke="{INK3}" stroke-opacity=".35" stroke-dasharray="2 4"/>' + label(448, 172, "kill switch · per-trade and daily caps · circuit breakers, fail closed", INK3, "middle")
    return wrap(svg(p, W, H, b, "Signals in, a ranked and contained trade out"))

def servers():
    p, W, H = "sv", 720, 200
    b = field(p, W, H, ((0.32, 0.5, "g"), (0.66, 0.5, "g")))
    b += chip(p, 20, 34, "Telegram", VI, 84) + chip(p, 20, 64, "Wallet stream", VI, 108) + chip(p, 20, 94, "Price stream", VI, 100) + chip(p, 20, 124, "Market data", VI, 100)
    for y in (44, 74, 104, 134): b += wire(p, [(128 if y != 44 else 104, y), (150, y), (168, 90), (190, 90)])
    b += box(p, 186, 46, 176, 92, "Finland · the brain", "Python · TimescaleDB")
    b += f'<line x1="362" x2="420" y1="92" y2="92" stroke="{CY}" stroke-width="6" stroke-opacity=".12"/>' + wire(p, [(362, 92), (420, 92)], dashed=True) + label(391, 78, "WireGuard", CY, "middle", 7.5)
    b += box(p, 420, 46, 172, 92, "Nuremberg · the hands", "Rust · signed signals")
    b += wire(p, [(592, 92), (630, 92)]) + box(p, 630, 60, 72, 64, "Solana", "mainnet", GR, small=True)
    b += label(275, 166, "analysis, heavy and chatty", INK3, "middle", 8.5) + label(503, 166, "execution, fast and quiet", INK3, "middle", 8.5)
    return wrap(svg(p, W, H, b, "Two servers joined by an encrypted tunnel, and the chain"))

def layers():
    p, W, H = "ly", 720, 200
    b = field(p, W, H, ((0.5, 0.5, "g"),))
    names = [("Constitution", "always loaded"), ("Navigation index", "2,110 lines"), ("Architecture map", "19,514 lines"), ("Three contracts", "one truth each"), ("The code", "source of truth")]
    for i, (n, s) in enumerate(names):
        x = 37 + i * 132
        acc = GR if i == 4 else (VI if i == 0 else CY)
        b += box(p, x, 52, 118, 60, n, s, acc, small=True)
        if i < 4: b += wire(p, [(x + 118, 82), (x + 132, 82)])
    b += f'<path d="M37,140 L683,140" stroke="url(#{p}w)" stroke-opacity=".5"/>' + label(360, 162, "one read path, every agent, every run: map before code, code wins", INK3, "middle", 8.5)
    b += dot(p, 37, 140, VI, 3) + dot(p, 683, 140, GR, 3)
    return wrap(svg(p, W, H, b, "The reading order every agent follows"))

def loop():
    import math
    p, W, H = "lp", 720, 200
    b = field(p, W, H, ((0.5, 0.5, "g"),))
    cx, cy, r = 360, 104, 70
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#{p}w)" stroke-width="1.5" stroke-opacity=".9"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#{p}w)" stroke-width="5" stroke-opacity=".15" filter="url(#{p}b)"/>'
    names = ["audit-task", "handover", "archive", "progress review", "documentation audit"]
    for i, n in enumerate(names):
        a = -math.pi / 2 + i * 2 * math.pi / 5; x = cx + r * math.cos(a); y = cy + r * math.sin(a)
        b += dot(p, f"{x:.1f}", f"{y:.1f}", CY if i else GR, 4)
        lx = cx + (r + 22) * math.cos(a); ly = cy + (r + 22) * math.sin(a)
        anchor = "middle" if abs(math.cos(a)) < 0.3 else ("start" if math.cos(a) > 0 else "end")
        if anchor == "end": lx -= 4
        b += label(f"{lx:.0f}", f"{ly+3:.0f}", n, INK2, anchor, 9)
    b += f'<text x="{cx}" y="{cy-2}" text-anchor="middle" font-size="11" font-weight="500" fill="{INK}" font-family="{SANS}">run ID + evidence</text><text x="{cx}" y="{cy+14}" text-anchor="middle" font-size="9" fill="{INK3}" font-family="{MONO}">ON DISK, NOT IN MEMORY</text>'
    b += chip(p, 40, 118, "memory reset", RED, 110) + wire(p, [(150, 128), (206, 128), (291, 107)], dashed=True) + label(40, 152, "the model forgets", INK3, "start", 8.5) + label(40, 168, "the run does not", INK3, "start", 8.5)
    b += chip(p, 566, 118, "2-day runs", GR, 96) + label(566, 152, "30 h · 28 h · 4 days", INK3, "start", 8.5)
    return wrap(svg(p, W, H, b, "Five commands passing one run's state around a loop"))

def chain():
    p, W, H = "ch", 720, 200
    b = field(p, W, H, ((0.15, 0.5, "gv"), (0.8, 0.5, "g")))
    b += box(p, 24, 68, 118, 64, "A skill", "vendor docs", VI, small=True)
    b += wire(p, [(142, 100), (190, 100)])
    xs = [190 + i * 82 for i in range(7)]
    b += wire(p, [(xs[0], 100), (xs[-1], 100)])
    for i, x in enumerate(xs):
        b += dot(p, x, 100, CY if i < 6 else GR, 4.5) + f'<text x="{x}" y="{104}" text-anchor="middle" font-size="8" font-weight="600" fill="#05080f" font-family="{MONO}">{i+1}</text>'
    groups = [(xs[0], xs[1], "planner cites", VI), (xs[2], xs[3], "implementer applies", CY), (xs[4], xs[6], "auditor proves", GR)]
    for x1, x2, t, c in groups:
        b += f'<path d="M{x1},124 L{x1},134 L{x2},134 L{x2},124" fill="none" stroke="{c}" stroke-opacity=".6"/>' + label((x1 + x2) / 2, 152, t, c, "middle", 8.5)
    b += label(xs[3], 44, "a citation without a file and line fails", INK3, "middle", 8.5)
    return wrap(svg(p, W, H, b, "Seven checkpoints that prove a skill was used"))

def gate():
    p, W, H = "gt", 720, 200
    b = field(p, W, H, ((0.5, 0.5, "g"),))
    # lane 1: claim without evidence stops
    b += chip(p, 20, 50, "“I edited the file”", INK2, 150) + wire(p, [(170, 60), (310, 60)])
    b += f'<rect x="316" y="36" width="4" height="48" rx="2" fill="{RED}"/><rect x="316" y="36" width="4" height="48" rx="2" fill="{RED}" filter="url(#{p}b)" fill-opacity=".8"/>'
    b += f'<line x1="326" x2="450" y1="60" y2="60" stroke="{INK3}" stroke-opacity=".25" stroke-dasharray="2 4"/>' + label(332, 100, "diff shows zero changes · hard block", RED, "start", 8.5)
    # lane 2: claim with receipt passes
    b += chip(p, 20, 130, "claim + receipt", INK2, 150) + wire(p, [(170, 140), (310, 140)])
    b += f'<rect x="316" y="116" width="4" height="20" rx="2" fill="{GR}"/><rect x="316" y="144" width="4" height="20" rx="2" fill="{GR}"/>'
    b += wire(p, [(326, 140), (540, 140)]) + dot(p, 540, 140, GR, 4) + label(332, 180, "evidence verified · passes", GR, "start", 8.5)
    b += box(p, 580, 68, 116, 64, "34 gates", "146 hard blocks", CY, small=True)
    return wrap(svg(p, W, H, b, "A claim without evidence stops; a claim with a receipt passes"))

def pulse():
    p, W, H = "pl", 720, 160
    b = field(p, W, H, ((0.5, 0.5, "g"),))
    pts = [(24, 80), (200, 80), (230, 80), (250, 40), (270, 120), (290, 80), (420, 80), (450, 80), (470, 52), (490, 108), (510, 80), (696, 80)]
    b += wire(p, pts, w=1.8) + dot(p, 696, 80, GR, 4.5)
    b += chip(p, 200, 120, "the product, live", CY, 130) + chip(p, 420, 120, "the workflow, live", GR, 136)
    b += label(24, 34, "no slides in the interview: two live sessions", INK3, "start", 8.5)
    return wrap(svg(p, W, H, b, "Two live sessions instead of slides"))

def mini_system():
    p, W, H = "ms", 560, 120
    b = field(p, W, H, ((0.2, 0.5, "gv"), (0.85, 0.5, "g")))
    b += chip(p, 20, 50, "signals", VI, 76) + wire(p, [(96, 60), (140, 60)]) + box(p, 140, 32, 130, 56, "Two servers", "Python · Rust", CY, small=True)
    b += wire(p, [(270, 60), (312, 60)]) + box(p, 312, 32, 120, 56, "Rust engine", "66 ms", CY, small=True) + wire(p, [(432, 60), (470, 60)]) + box(p, 470, 32, 72, 56, "Solana", "capped", GR, small=True)
    return wrap(svg(p, W, H, b, "Signals to a capped on-chain trade"), "banner mini")

def mini_loop():
    import math
    p, W, H = "ml", 560, 120
    b = field(p, W, H, ((0.5, 0.5, "g"),))
    xs = [60 + i * 88 for i in range(6)]
    b += wire(p, [(xs[0], 60), (xs[-1], 60)])
    names = ["understand", "route", "plan", "build", "review", "decide"]
    for i, x in enumerate(xs):
        mine = i in (1, 3, 5)
        b += (dot(p, x, 60, CY, 4.5) if mine else ring(p, x, 60, INK2, 4)) + label(x, 86, names[i], CY if mine else INK3, "middle", 8.5)
    b += label(xs[0], 30, "three decisions are mine", INK3, "start", 8.5)
    return wrap(svg(p, W, H, b, "Six stages, three of them my decision"), "banner mini")

def shards():
    p, W, H = "sh", 720, 200
    b = field(p, W, H, ((0.35, 0.5, "g"),))
    counts = [70, 68, 71, 69, 70, 67, 69, 68]
    x0, gap, bw = 36, 58, 36
    b += f'<line x1="{x0-12}" x2="{x0+7*gap+bw+12}" y1="56" y2="56" stroke="{RED}" stroke-opacity=".6" stroke-dasharray="3 4"/>' + label(x0 - 12, 46, "provider cap · 100 per connection", RED, "start", 8.5)
    for i, c in enumerate(counts):
        x = x0 + i * gap; h = c * 1.0; y = 156 - h
        b += f'<rect x="{x}" y="56" width="{bw}" height="100" rx="8" fill="#0b1220" fill-opacity=".9" stroke="url(#{p}h)" stroke-opacity=".55"/>'
        b += f'<rect x="{x+4}" y="{y:.0f}" width="{bw-8}" height="{h:.0f}" rx="6" fill="{CY}" fill-opacity=".22"/><rect x="{x+4}" y="{y:.0f}" width="{bw-8}" height="1.5" fill="{CY}"/>'
        b += label(x + bw / 2, 176, f"s{i+1}", INK3, "middle", 8) + f'<text x="{x+bw/2}" y="{y-5:.0f}" text-anchor="middle" font-size="8.5" fill="{INK2}" font-family="{MONO}">{c}</text>'
    # restart demonstration, right side
    rx = 528
    b += box(p, rx, 56, 168, 100, "Placed by hash", "SHA-256, not salted", GR, small=True)
    b += dot(p, rx + 40, 122, GR, 3.5) + f'<path d="M{rx+40},122 C {rx+60},96 {rx+100},96 {rx+120},122" fill="none" stroke="{GR}" stroke-opacity=".85" stroke-dasharray="3 3"/>' + dot(p, rx + 120, 122, GR, 3.5)
    b += label(rx + 80, 142, "restart → same shard", GR, "middle", 8)
    b += label(x0 - 12, 194, "552 contracts · 8 connections · 6 needed, 2 headroom", INK3, "start", 8.5)
    return wrap(svg(p, W, H, b, "552 contracts spread over 8 connections under a 100-address cap; placement survives restarts"))

BANNERS = dict(pipeline=pipeline, servers=servers, layers=layers, loop=loop, chain=chain, gate=gate, pulse=pulse, shards=shards)
