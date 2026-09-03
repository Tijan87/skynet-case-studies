# v2 theme: one accent, fluid type, one card, quiet motion. Spec: audit2/report_site_design.md
CSS = r"""
:root{
  --bg:#05080f; --surface:#0a1018; --surface-2:#0d141f;
  --ink:#f2f6ff; --ink-2:#a7b4c9; --ink-3:#7d8ba3;
  --accent:#31d9ff; --violet:#a877ff; --green:#58e7ad; --red:#ff8f8f;
  --line:rgba(167,180,201,.13); --line-2:rgba(167,180,201,.24);
  --display:"Space Grotesk","IBM Plex Sans",system-ui,sans-serif;
  --body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  --fs-h1:clamp(2.125rem,3.24vw + 1.34rem,4.25rem);
  --fs-h2:clamp(1.625rem,1.33vw + 1.3rem,2.5rem);
  --fs-h3:clamp(1.125rem,.48vw + 1.01rem,1.375rem);
  --fs-lead:clamp(1.125rem,.38vw + 1.03rem,1.375rem);
  --fs-body:clamp(1rem,.1vw + .98rem,1.0625rem);
  --fs-num:clamp(2.25rem,2vw + 1.7rem,3.5rem);
  --fs-label:.8125rem; --fs-cap:.875rem;
  --w:70rem; --w-prose:42rem; --gutter:clamp(1.25rem,5vw,3rem);
  --sec:clamp(4.5rem,9vw,8.5rem); --stack:clamp(1rem,1.6vw,1.5rem);
  --ease:cubic-bezier(.23,1,.32,1); --r:14px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:400 var(--fs-body)/1.62 var(--body);-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
:where(a,button):focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
img{max-width:100%;display:block}
h1,h2,h3{margin:0;font-family:var(--display);font-weight:600;text-wrap:balance}
h1{font-size:var(--fs-h1);line-height:1.04;letter-spacing:-.025em;max-inline-size:20ch}
h2{font-size:var(--fs-h2);line-height:1.12;letter-spacing:-.018em;max-inline-size:26ch}
h3{font-size:var(--fs-h3);line-height:1.25;letter-spacing:-.01em}
p{margin:0;text-wrap:pretty}
ul,ol{margin:0;padding:0;list-style:none}
.lead{font-size:var(--fs-lead);line-height:1.45;color:var(--ink-2);max-inline-size:58ch}
.body{color:var(--ink-2);max-inline-size:68ch}
.label{font:500 var(--fs-label)/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3)}
.kicker{font:500 var(--fs-label)/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2);display:flex;align-items:center;gap:10px}
.kicker::before{content:"";width:16px;height:1px;background:var(--accent)}
.cap{font-size:var(--fs-cap);line-height:1.5;color:var(--ink-3);max-inline-size:60ch}
.wrap{width:min(100% - 2*var(--gutter),var(--w));margin-inline:auto}
.prose{max-inline-size:var(--w-prose)}

/* ground: static tint + grain; the only moving thing is the hero glow */
.ground{position:fixed;inset:0;z-index:-1;background:var(--bg);pointer-events:none}
.ground::before{content:"";position:absolute;inset:0;background:radial-gradient(70% 45% at 50% -10%,rgba(49,217,255,.06),transparent 70%)}
.ground::after{content:"";position:absolute;inset:0;opacity:.45;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .05 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.glow{position:absolute;top:-22%;left:50%;width:min(90vw,900px);aspect-ratio:1;pointer-events:none;z-index:-1;
  background:radial-gradient(circle,rgba(49,217,255,.14),transparent 62%);filter:blur(60px);opacity:0;
  animation:glow-in 1.2s var(--ease) .3s forwards,drift 26s ease-in-out 1.5s infinite}
@keyframes glow-in{to{opacity:.55}}
@keyframes drift{0%,100%{transform:translate(-50%,0)}50%{transform:translate(-46%,3%)}}

/* nav */
.nav{position:sticky;top:0;z-index:50;background:rgba(5,8,15,.72);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid transparent;transition:border-color .2s var(--ease)}
.nav.solid{border-bottom-color:var(--line)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;height:56px}
.brand{font:500 var(--fs-label)/1 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2);white-space:nowrap}
.brand b{color:var(--ink);font-weight:600}
.brand .x{display:none}
@media (min-width:720px){.brand .x{display:inline}}
.tabs{display:flex;gap:2px}
.tabs a{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 12px;border-radius:999px;font:500 var(--fs-label)/1 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);transition:color .15s var(--ease),background .15s var(--ease)}
.tabs a:hover{color:var(--ink)}
.tabs a.on{color:var(--accent)}
.tabs .lbl{display:none}
@media (min-width:720px){.tabs .lbl{display:inline}}
.bar{position:absolute;left:0;bottom:-1px;height:1px;width:100%;background:var(--accent);transform-origin:0 50%;transform:scaleX(0)}
@supports (animation-timeline:scroll(root block)){@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}.bar{animation:grow linear;animation-timeline:scroll(root block)}}

/* hero */
.hero{position:relative;padding-block:clamp(5rem,11vw,9.5rem) clamp(3rem,6vw,5rem)}
.hero > .wrap > * + *{margin-top:var(--stack)}
.hero h1{margin-top:.75rem}
.hero .lead{margin-top:1.25rem}
.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:2rem!important}
.btn{display:inline-flex;align-items:center;gap:10px;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid var(--line-2);font:500 var(--fs-label)/1 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink);transition:border-color .15s var(--ease),color .15s var(--ease),background .15s var(--ease)}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.primary{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.btn.primary:hover{background:var(--accent);border-color:var(--accent);color:var(--bg)}
.btn .a{transition:transform .2s var(--ease)}
.btn:hover .a{transform:translateX(3px)}

/* proof strip */
.stats{display:grid;gap:clamp(1.25rem,3vw,2.5rem);grid-template-columns:repeat(auto-fit,minmax(min(100%,11rem),1fr))}
.stat{border-top:1px solid var(--line);padding-top:.85rem}
.stat .n{display:block;font:500 var(--fs-num)/.95 var(--mono);letter-spacing:-.03em;font-variant-numeric:tabular-nums;color:var(--ink)}
.stat .l{display:block;margin-top:.55rem;font-size:var(--fs-cap);color:var(--ink-3);line-height:1.35}
.fn{margin-top:1.25rem;font-size:var(--fs-cap);line-height:1.5;color:var(--ink-3);max-inline-size:68ch}

/* sections */
.sec{padding-block:var(--sec);border-top:1px solid var(--line)}
.sec .head > * + *{margin-top:.75rem}
.sec .head .lead{margin-top:1.25rem}
.sec .head + *{margin-top:clamp(2rem,4vw,3.5rem)}
.grid2{display:grid;gap:clamp(1.75rem,4vw,3.5rem);align-items:start}
.grid2 > *{min-width:0}
@media (min-width:900px){.grid2{grid-template-columns:minmax(0,5fr) minmax(0,6fr)}.grid2.rev{grid-template-columns:minmax(0,6fr) minmax(0,5fr)}}
.points{display:flex;flex-direction:column;gap:1.1rem;counter-reset:pt;max-inline-size:60ch}
.points li{position:relative;padding-left:2.4rem;color:var(--ink-2)}
.points li::before{counter-increment:pt;content:counter(pt,decimal-leading-zero);position:absolute;left:0;top:.42em;font:500 .75rem/1 var(--mono);letter-spacing:.09em;color:var(--accent)}
.note{margin-top:clamp(2rem,4vw,3rem);padding-top:1.25rem;border-top:1px solid var(--line);color:var(--ink-2);max-inline-size:68ch}
.note .kicker{display:inline-flex;margin-right:12px;vertical-align:1px}
.quote{font-family:var(--display);font-size:clamp(1.25rem,.6vw+1.1rem,1.6rem);line-height:1.3;color:var(--ink);max-inline-size:32ch;letter-spacing:-.01em}
.quote + .cap{margin-top:.75rem}
.metrics{display:grid;gap:clamp(1.25rem,3vw,2.5rem);grid-template-columns:repeat(auto-fit,minmax(min(100%,11rem),1fr));margin-top:clamp(2rem,4vw,3.5rem)}
.metrics .stat .n{font-size:clamp(1.75rem,1.2vw+1.4rem,2.5rem)}

/* the one card */
.card{background:linear-gradient(180deg,var(--surface-2),var(--surface));border:1px solid var(--line);border-radius:var(--r);padding:clamp(1.25rem,2.5vw,2rem);
  transition:border-color .18s var(--ease),transform .18s var(--ease),background .18s var(--ease)}
.card > * + *{margin-top:.75rem}
a.card:hover{border-color:var(--line-2);transform:translateY(-2px);background:var(--surface-2)}
.card .card{border:0;padding:0;background:none}
.card p{color:var(--ink-2)}
.card .kicker{color:var(--ink-3)}
.cards{display:grid;gap:14px}
.c2{grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))}
.c3{grid-template-columns:repeat(auto-fit,minmax(min(100%,17rem),1fr))}
.c4{grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr))}
.arrow{display:inline-flex;align-items:center;gap:8px;font:500 var(--fs-label)/1 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--accent)}
.arrow .a{transition:transform .2s var(--ease)}
a.card:hover .arrow .a{transform:translateX(3px)}
.pill{display:inline-flex;align-items:center;gap:.5em;font:500 .75rem/1 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2);background:rgba(167,180,201,.05);border:1px solid var(--line);border-radius:999px;padding:.5em .8em}
.pill.me{color:var(--accent);border-color:rgba(49,217,255,.35)}
.pill.me::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent)}

/* figures */
.shot{border-radius:var(--r);overflow:hidden;border:1px solid var(--line-2);background:#0b1220;box-shadow:0 30px 80px -30px rgba(0,0,0,.8)}
.fig{overflow-x:auto;-webkit-overflow-scrolling:touch;min-width:0;max-width:100%}
.fig svg{width:100%;height:auto;display:block}
@media (max-width:640px){.fig svg{min-width:600px}}
.fig .cap,.shot + .cap{margin-top:.75rem}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:var(--fs-cap);color:var(--ink-2);margin-top:.75rem}
.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:8px;vertical-align:-1px}

/* timeline */
.tl{display:grid;position:relative;margin-top:clamp(2rem,4vw,3rem)}
.tl::before{content:"";position:absolute;left:5px;top:8px;bottom:8px;width:1px;background:var(--line-2)}
.tl .m{position:relative;padding:0 0 1.4rem 1.75rem}
.tl .m::before{content:"";position:absolute;left:2px;top:8px;width:7px;height:7px;border-radius:50%;background:var(--bg);border:1px solid var(--accent)}
.tl .d{font:500 var(--fs-label)/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3)}
.tl .t{color:var(--ink-2);margin-top:.35rem;max-inline-size:48ch}
@media (min-width:900px){.tl{grid-template-columns:repeat(4,1fr);gap:1.5rem}.tl::before{left:0;right:0;top:3px;bottom:auto;width:auto;height:1px}.tl .m{padding:1.4rem .75rem 0 0}.tl .m::before{left:0;top:0}}

/* infra diagram: colour is a legend here, not decoration */
.infra{display:grid;gap:14px}
@media (min-width:900px){.infra{grid-template-columns:repeat(2,minmax(0,1fr))}}
.node{border:1px solid var(--line);border-radius:var(--r);padding:1.25rem;background:linear-gradient(180deg,var(--surface-2),var(--surface));position:relative}
.node::before{content:"";position:absolute;left:1.25rem;right:1.25rem;top:-1px;height:1px;background:var(--c)}
.node.v{--c:var(--violet)} .node.c{--c:var(--accent)} .node.g{--c:var(--green)}
.node .label{color:var(--c)}
.node h3{margin-top:.5rem}
.node .sub{font-size:var(--fs-cap);color:var(--ink-3);margin-top:.15rem}
.node ul{margin-top:.9rem;display:flex;flex-direction:column;gap:.5rem}
.node li{font-size:var(--fs-cap);color:var(--ink-2);line-height:1.45;padding-left:.9rem;position:relative}
.node li::before{content:"";position:absolute;left:0;top:.6em;width:4px;height:4px;border-radius:50%;background:var(--c)}

/* before / after */
.ba{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,17rem),1fr))}
.ba .card{display:flex;flex-direction:column;gap:.9rem}
.ba .card > * + *{margin-top:0}
.ba .lab{font:500 .75rem/1.3 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin-bottom:.35rem}
.ba .now .lab{color:var(--green)}
.ba .broke,.ba .now{font-size:var(--fs-cap);line-height:1.5;color:var(--ink-2)}
.ba .now{color:var(--ink)}
.ba .big{margin-top:auto;padding-top:.8rem;border-top:1px solid var(--line);display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.ba .big .n{font:500 1.35rem/1 var(--mono);letter-spacing:-.02em;color:var(--ink)}
.ba .big .l{font-size:var(--fs-cap);color:var(--ink-3)}
.ba .when{font:500 .75rem/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3)}

/* tiles */
.tiles{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,18rem),1fr))}
.tile .n{display:block;font:500 clamp(2rem,1.5vw+1.5rem,2.75rem)/1 var(--mono);letter-spacing:-.03em;font-variant-numeric:tabular-nums;color:var(--ink)}
.tile .l{color:var(--ink);margin-top:.75rem;font-weight:500}
.tile .s{color:var(--ink-3);font-size:var(--fs-cap);margin-top:.35rem;line-height:1.5}

/* keys */
.keys{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,14rem),1fr))}
.key{border:1px solid var(--line);border-radius:var(--r);padding:1.25rem;background:linear-gradient(180deg,var(--surface-2),var(--surface));position:relative}
.key::before{content:"";position:absolute;left:1.25rem;right:1.25rem;top:-1px;height:1px;background:var(--c)}
.key.g{--c:var(--green)} .key.c{--c:var(--accent)}
.key h3{display:flex;align-items:center;gap:10px}
.key h3::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--c)}
.key ul{margin-top:.9rem;display:flex;flex-wrap:wrap;gap:6px}
.key li{font-size:var(--fs-cap);color:var(--ink-2);border:1px solid var(--line);border-radius:8px;padding:.3rem .6rem}
.key .no{margin-top:.9rem;font:500 .75rem/1.3 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--red)}
.rules{margin-top:14px;border-top:1px solid var(--line);padding-top:1rem;display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;font-size:var(--fs-cap);color:var(--ink-2)}
.rules .lab{width:100%;font:500 .75rem/1.3 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--green)}
.rules span{position:relative;padding-left:.8rem}
.rules span::before{content:"";position:absolute;left:0;top:.62em;width:4px;height:4px;border-radius:50%;background:var(--green)}

/* loop */
.loop{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,18rem),1fr))}
.stage{position:relative}
.stage .idx{font:500 var(--fs-label)/1 var(--mono);letter-spacing:.09em;color:var(--accent)}
.stage h3{margin-top:.5rem}
.stage p{font-size:var(--fs-cap);line-height:1.5}
.stage .ev{margin-top:.9rem;padding-top:.75rem;border-top:1px solid var(--line);font-size:var(--fs-cap);color:var(--ink-3);line-height:1.45}
.stage .ev b{display:block;font:500 .75rem/1.3 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin-bottom:.25rem}
.stage .pill{position:absolute;top:1.1rem;right:1.1rem;margin:0}
.routes{display:flex;flex-wrap:wrap;gap:.5rem 1.75rem;margin-top:1.5rem;font-size:var(--fs-cap);color:var(--ink-2)}
.routes b{color:var(--ink);font-weight:500}

/* lanes */
.lanes{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,17rem),1fr))}
.lane ul{display:flex;flex-direction:column;gap:.5rem}
.lane li{font-size:var(--fs-cap);color:var(--ink-2);padding:.5rem .75rem;border:1px solid var(--line);border-radius:10px;line-height:1.4}
.lane li.x{border-style:dashed}
.lane.ext .label{color:var(--violet)}

/* scorecard */
.score{display:flex;flex-direction:column;gap:.7rem}
.row{display:grid;grid-template-columns:1fr auto;gap:.3rem .9rem;align-items:center}
.row .l{font-size:var(--fs-cap);color:var(--ink)}
.row .v{font:500 .8rem/1 var(--mono);color:var(--ink-2);white-space:nowrap}
.row .b{grid-column:1/-1;height:3px;border-radius:2px;background:rgba(167,180,201,.1);overflow:hidden}
.row .b i{display:block;height:100%;width:var(--w);background:var(--green);transform-origin:0 50%;transform:scaleX(0);transition:transform .9s var(--ease) .15s}
.row.part .b i{background:var(--accent)}
.in .row .b i{transform:scaleX(1)}
.row .s{grid-column:1/-1;font-size:var(--fs-cap);color:var(--ink-3)}
.lineage{display:flex;flex-direction:column}
.lineage li{display:grid;grid-template-columns:9rem 1fr;gap:.75rem;font-size:var(--fs-cap);color:var(--ink-2);line-height:1.45;padding:.7rem 0;border-top:1px solid var(--line)}
.lineage li b{color:var(--ink);font-weight:500}
@media (max-width:480px){.lineage li{grid-template-columns:1fr;gap:.2rem}}

/* chain */
.chain{display:grid;gap:1.25rem 1.25rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,10rem),1fr));counter-reset:ch}
@media (min-width:900px){.chain{grid-template-columns:repeat(3,1fr)}}
.chain .c{border-top:1px solid var(--line);padding-top:.8rem}
.chain .c::before{counter-increment:ch;content:counter(ch,decimal-leading-zero);font:500 .75rem/1 var(--mono);letter-spacing:.09em;color:var(--accent)}
.chain .c h3{font-size:1rem;margin-top:.45rem}
.chain .c p{font-size:var(--fs-cap);color:var(--ink-2);line-height:1.45;margin-top:.35rem}
.gaplife{margin-top:clamp(2rem,4vw,3rem)}
.gaplife ol{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,11rem),1fr));margin-top:.9rem}
.gaplife li{font-size:var(--fs-cap);color:var(--ink-2);line-height:1.45}
.gaplife li b{display:block;font:500 .75rem/1.3 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-bottom:.25rem}

/* gates */
.gates{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,19rem),1fr))}
.gate{display:grid;gap:.5rem}
.gate > * + *{margin-top:0}
.gate .claim{color:var(--ink);font-weight:500;line-height:1.4}
.gate .does{color:var(--ink-2);font-size:var(--fs-cap);line-height:1.5;padding-left:.8rem;border-left:2px solid var(--accent)}
.gate .lab{font:500 .75rem/1.3 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}

/* recent runs */
.runs li{display:grid;grid-template-columns:3rem 1fr;gap:.15rem .9rem;padding:.65rem 0;border-top:1px solid var(--line);font-size:var(--fs-cap)}
.runs li:first-child{border-top:0;padding-top:0}
.runs .n{font:500 .8rem/1.4 var(--mono);color:var(--accent);grid-row:span 2}
.runs .t{color:var(--ink)}
.runs .s{color:var(--ink-3);font-size:var(--fs-cap)}

/* knowledge columns */
.cols{display:grid;gap:1.5rem 1.25rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,16rem),1fr))}
.col{border-top:1px solid var(--line);padding-top:1rem}
.col .sub{font-size:var(--fs-cap);color:var(--ink-3);margin-top:.3rem}
.col ul{margin-top:.8rem;display:flex;flex-wrap:wrap;gap:6px}
.col li{font-size:var(--fs-cap);color:var(--ink-2);border:1px solid var(--line);border-radius:8px;padding:.25rem .55rem}

/* who + close */
.who{display:grid;gap:1rem 3rem;align-items:start;border-top:1px solid var(--line);padding-top:1.5rem}
@media (min-width:800px){.who{grid-template-columns:1fr 1.4fr}}
.who .role{font:500 var(--fs-label)/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin-top:.4rem}
.who .contact{margin-top:.9rem;font-size:var(--fs-cap);color:var(--ink-2)}
.who .contact a{color:var(--accent)}
.who p{color:var(--ink-2);max-inline-size:60ch}
.sessions{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,18rem),1fr))}
.nextlink{margin-top:clamp(2.5rem,5vw,4rem)}
.nextlink .card{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}
.nextlink .card > * + *{margin-top:0}

/* footer */
.foot{border-top:1px solid var(--line);padding:2.5rem 0 3rem}
.foot .wrap{display:flex;flex-wrap:wrap;gap:1rem 3rem;justify-content:space-between;align-items:baseline}
.foot p{font-size:var(--fs-cap);color:var(--ink-3);max-inline-size:70ch;line-height:1.55}
.foot a{color:var(--ink-2)}
.foot a:hover{color:var(--accent)}

/* landing */
.pick{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))}
.pick .card{display:flex;flex-direction:column;padding:clamp(1.5rem,3vw,2.25rem)}
.pick h2{font-size:clamp(1.5rem,1vw+1.2rem,2rem);margin-top:.6rem;max-inline-size:none}
.name{font:600 var(--fs-h3)/1.25 var(--display);letter-spacing:-.01em}
.skip{position:absolute;left:-999px;top:8px;z-index:100;background:var(--ink);color:var(--bg);padding:10px 14px;border-radius:8px;font:500 var(--fs-label)/1 var(--mono);letter-spacing:.09em;text-transform:uppercase}
.skip:focus{left:8px}
.pick .nums{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1.25rem;padding-top:1rem;border-top:1px solid var(--line)}
.pick .nums .n{display:block;font:500 1.5rem/1 var(--mono);letter-spacing:-.02em;color:var(--ink)}
.pick .nums .l{display:block;font-size:var(--fs-cap);color:var(--ink-3);margin-top:.35rem}
.pick .arrow{margin-top:auto;padding-top:1.5rem}
.land .sec{border-top:0;padding-top:0}

@media print{.js .rv{opacity:1!important;transform:none!important}.ground,.glow,.skip,.bar{display:none}.nav{position:static}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}.sec{break-inside:auto}.card{break-inside:avoid}}

/* motion */
.js .rv{opacity:0;transform:translateY(14px);transition:opacity .48s var(--ease) calc(var(--i,0)*50ms),transform .48s var(--ease) calc(var(--i,0)*50ms)}
.js .rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .js .rv{opacity:1;transform:none;transition:none}
  .glow{opacity:.35;animation:none}
  a.card:hover{transform:none}
  .row .b i{transition:none;transform:scaleX(1)}
  .btn .a,.arrow .a{transition:none}
  .bar{animation:none!important;transform:none!important}
}
@media (max-width:480px){
  :root{--fs-cap:.9375rem}
  .stage .ev b,.gate .lab,.ba .lab,.gaplife li b,.ba .when,.rules .lab,.key .no,.pill{font-size:.75rem}
}
"""

JS = r"""
document.documentElement.classList.add('js');
(function(){
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = [].slice.call(document.querySelectorAll('.rv'));
  document.querySelectorAll('[data-stagger]').forEach(function(g){
    [].slice.call(g.children).filter(function(e){return e.classList.contains('rv');}).forEach(function(el,i){ el.style.setProperty('--i', i); });
  });
  function all(){ els.forEach(function(e){ e.classList.add('in'); }); }
  if (RM || !('IntersectionObserver' in window)) { all(); }
  else {
    var io = new IntersectionObserver(function(entries, obs){
      entries.forEach(function(en){ if (en.isIntersecting) { en.target.classList.add('in'); obs.unobserve(en.target); } });
    }, {threshold: 0.12, rootMargin: '0px 0px -10% 0px'});
    var hero = [].slice.call(document.querySelectorAll('.hero .rv'));
    els.forEach(function(e){ if (hero.indexOf(e) < 0) io.observe(e); });
    var play = function(){ hero.forEach(function(e){ e.classList.add('in'); }); };
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(play);
    setTimeout(play, 900);
  }
  var nav = document.querySelector('.nav'), bar = document.querySelector('.bar');
  var noSDA = !(window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll(root block)'));
  var tick = false;
  function onScroll(){
    if (tick) return; tick = true;
    requestAnimationFrame(function(){
      var y = window.scrollY || document.documentElement.scrollTop;
      nav.classList.toggle('solid', y > 24);
      if (noSDA && bar) { var max = document.documentElement.scrollHeight - innerHeight; bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')'; }
      tick = false;
    });
  }
  addEventListener('scroll', onScroll, {passive: true}); onScroll();
  addEventListener('beforeprint', all);
})();
"""
