"""Minimal presentation for the case studies: open typography and quiet diagrams."""
from html import escape as E


def title(text):
    return E(text)


def schematic(kind="system"):
    workflow = kind == "workflow"
    rows = (
        [("Intent", "I define the task", "Scope, constraints and acceptance", True),
         ("Build", "Agents do the work", "Research, plan and implement", False),
         ("Review", "Independent challenge", "Claude, Codex and Grok", False),
         ("Release", "I decide what ships", "Verify, approve and observe", True)]
        if workflow else
        [("Signals", "Public market signals", "Telegram calls + tracked wallets", False),
         ("Analysis", "Finland / Python", "Rank sources and replay strategies", False),
         ("Execution", "Nuremberg / Rust", "Build the transaction, manage the exit", False),
         ("On-chain", "Solana / program controls", "Per-trade caps and daily limits", True)]
    )
    steps = ''.join(f'''<li class="route-step{' decisive' if decisive else ''}"><span class="route-point" aria-hidden="true"></span><div><span class="route-label">{E(label)}</span><strong>{E(heading)}</strong><span class="route-detail">{E(detail)}</span></div></li>''' for label,heading,detail,decisive in rows)
    return f'''<figure class="route-diagram rv"><figcaption class="route-title">{'How a change ships' if workflow else 'The path of a signal'}</figcaption><ol>{steps}</ol><div class="route-foot">{'Human decisions at the beginning and the release.' if workflow else 'Two servers. One encrypted tunnel. My funds only.'}</div></figure>'''


def bar_chart(rows, maximum, heading, context, caption):
    items = ''.join(f'''<li class="chart-row"><span class="chart-label">{E(label)}</span><span class="chart-track" aria-hidden="true"><i style="width:{value / maximum * 100:.4f}%;--bar-color:{tone}"></i></span><span class="chart-value">{E(shown)}</span></li>''' for label,value,shown,tone in rows)
    return f'''<figure class="data-chart rv"><div class="chart-heading"><h3>{E(heading)}</h3><span class="label">{E(context)}</span></div><ol class="chart-rows">{items}</ol><figcaption class="cap">{E(caption)}</figcaption></figure>'''


JS = r"""
(function () {
 var regions=document.querySelectorAll('.figs-x,.tablewrap');
 function update() {
  regions.forEach(function(region) {
   if(region.clientWidth>0 && region.scrollWidth>region.clientWidth+1) {
    var graphic=region.querySelector('svg[aria-label]');
    region.tabIndex=0;
    region.setAttribute('role','region');
    region.setAttribute('aria-label',(graphic?graphic.getAttribute('aria-label'):'Data table')+'. Scroll horizontally to explore.');
   } else {
    region.removeAttribute('tabindex');region.removeAttribute('role');region.removeAttribute('aria-label');
   }
  });
 }
 update();
 if(typeof ResizeObserver!=='undefined') {
  var observer=new ResizeObserver(update);
  regions.forEach(function(region){observer.observe(region)});
 } else {addEventListener('resize',update,{passive:true})}
})();
"""


CSS = r"""
/* The original near-black palette, with typography doing most of the work. */
:root{
 --bg:#05080f;--surface:#0a1018;--surface-2:#0d141f;
 --ink:#f2f6ff;--ink-2:#a7b4c9;--ink-3:#8491a7;
 --accent:#8ac5d2;--green:#91c4ae;--violet:#aaa4c4;
 --line:rgba(167,180,201,.13);--line-2:rgba(167,180,201,.23);
 /* Font families, type scale, reading measures and gutters inherit theme.py. */
 --r:3px;
 --sec:clamp(3rem,5.7vw,5.2rem);
}
::selection{background:#29424c;color:#fff}
.ground::before,.ground::after,.glow{display:none}
.kicker::before{width:16px;flex:none;background:var(--ink-3)}
.nav{background:rgba(5,8,15,.96);border-bottom:1px solid var(--line);backdrop-filter:none}
.nav .wrap{height:64px}
.tabs{gap:22px}
.tabs a{padding:0;min-height:44px;border-radius:0;color:var(--ink-3)}
.tabs a.on{color:var(--ink);background:none}
.bar{opacity:.38}
.hero{padding-block:clamp(2.5rem,5vw,4.7rem) 2.5rem}
.hero > .hero-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:2.25rem}
.hero > .hero-grid > *{min-width:0;margin-top:0}
.hero-copy > .cap{margin-top:1rem}
.actions{gap:24px;margin-top:1.5rem!important}
.btn,.btn.primary{min-height:44px;border:0;border-radius:0;background:none;color:var(--ink);padding:0;box-shadow:none}
.btn.primary{border-bottom:1px solid var(--ink-3)}
.btn:hover,.btn.primary:hover{background:none;color:var(--accent);border-color:var(--accent)}
.hero-grid > .stats{grid-column:1/-1;margin:0;gap:2rem;padding:1.35rem 0 0;border-top:1px solid var(--line)}
.hero-grid > .stats .stat{border:0;padding:0}
.hero-grid > .hero-notes{grid-column:1/-1}
.authorship{display:grid;grid-template-columns:10rem minmax(0,1fr);gap:2rem;border:0;border-radius:0;background:none;padding:0;margin:0;max-inline-size:none}
.authorship .label{margin:0;padding-top:.1rem;color:var(--ink-3)}
.authorship p{max-width:100ch}
.hero-notes > details.more{margin-top:.65rem}
.hero-notes .shot{max-width:64rem;margin-inline:auto}
.hero-notes .shot.tilt{transform:none}
/* Keep the original stacked heading/lead layout, not half-width columns. */
.sec .head + *{margin-top:2rem}
.sec:target{scroll-margin-top:85px}
.metrics{gap:2rem;margin-top:1.8rem}
.metrics .stat{padding-top:1rem}
.card,.node,.key,.flow .fx,.lanes-strip .ln{background:none;border:0;border-radius:0;box-shadow:none;padding:1.2rem 0;border-top:1px solid var(--line)}
a.card:hover{background:none;transform:none;border-color:var(--line-2)}
.cards,.ba,.tiles,.keys,.gates,.sessions,.infra,.flow{gap:1.25rem 2rem}
.cards.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
.cards.c4 .card{display:grid;grid-template-rows:auto auto 1fr;align-content:start;gap:.8rem}
.cards.c4 .card > *{margin:0}
.ba .card{gap:1rem}
.ba .now .lab{color:var(--ink-2)}
.ba .big{padding-top:1rem}
.tiles{grid-template-columns:repeat(3,minmax(0,1fr))}
.node::before,.key::before{display:none}
.key h3::before{width:5px;height:5px}
.key ul{gap:.4rem 1rem}
.key li{border:0;border-radius:0;padding:0}
.key .no{color:#cda2a2}
.key .no.ok{color:var(--ink-2)}
.rules .lab{color:var(--ink-2)}
.rules span::before{background:var(--ink-3)}
.flow .fx .ar{display:none}
.flow.c3{grid-template-columns:repeat(3,minmax(0,1fr))}
.lanes-strip{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 3rem}
.lanes-strip .ln{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1fr);gap:1rem;padding:1rem 0;align-items:baseline;grid-column:auto}
.lanes-strip .ln b{white-space:normal;align-items:center;gap:8px}
.lanes-strip .ln b i{width:5px;height:5px;opacity:.7}
.lanes-strip .ln span{margin:0}
.lanes-strip .ln:last-child:nth-child(odd){grid-column:1/-1;grid-template-columns:minmax(0,calc((100% - 5rem) * 2 / 9)) minmax(0,1fr)}
.matrix th{padding:.9rem 1.5rem .9rem 0;border-color:var(--line)}
.matrix td{padding:.95rem 1.5rem .95rem 0;border-color:rgba(167,180,201,.09)}
.matrix .dot{width:5px;height:5px;opacity:.7}
.tablewrap{background:none;border:0;scrollbar-width:thin;scrollbar-color:#303a48 #05080f}
.gates{grid-template-columns:repeat(3,minmax(0,1fr))}
.gate .claim{min-block-size:0}
.gate .does{border-left:1px solid var(--line-2)}
.score{gap:1.1rem}
.row .b{height:2px;background:rgba(167,180,201,.09)}
.row .b i,.row.part .b i{background:var(--ink-3)}
.funnel{gap:1.15rem}
.funnel .fr .b{height:3px;border-radius:0}
.funnel .fr .b i{background:var(--ink-3);border-radius:0}
.fig > .figs-x,.banner{background:none;border:0;border-radius:0;box-shadow:none}
.fig svg{max-width:100%;filter:saturate(.45)}
.figs-x{scrollbar-width:thin;scrollbar-color:#303a48 #05080f}
.fig .cap,.shot + .cap{max-width:96ch;margin-top:1rem}
.shot,.pane{border-radius:3px;box-shadow:none;border-color:var(--line)}
.shot,.shot.tilt{transform:none;transition:none}
.pane{background:#080d15;font-size:.75rem;line-height:1.75;padding:1.2rem}
.pane::before,.pane .bar3{display:none}
.pill,.key li,.col li{background:none;border-radius:0}
.points{max-inline-size:none}
.points li{padding-left:1.6rem}
.points li::before{color:var(--ink-3)}
.note{padding-right:0;max-width:98ch}
details.more{border-top:1px solid var(--line);margin-top:1.3rem}
details.more > summary{display:flex;justify-content:space-between;width:100%;gap:1rem;padding:.85rem 0;min-height:44px;line-height:1.55}
details.more > summary .c,details.phase-acc > summary .chev,.acc summary .c{border:0;border-radius:0;width:18px;height:22px;flex:none;color:var(--ink-3)}
details.more .inner{padding-top:.5rem;gap:1.5rem}
details.more[open]{padding-bottom:1rem}
details.more .inner > .points{gap:1.1rem 2.5rem}
details.phase-acc > summary .num{color:var(--ink-3)}
details.phase-acc > summary .cnt{border:0;padding:0}
.acc summary{grid-template-columns:2.75rem minmax(0,1fr) auto;gap:.75rem}
.acc .in{padding-left:3.5rem}
.acc .tag{border:0;border-radius:0;padding:0;margin:.35rem 1rem .35rem 0}
.expand-all{border:0;border-radius:0;padding:.5rem 0;min-height:44px;color:var(--ink-2)}
.ribbon-list li{padding:.65rem 0;border:0;border-bottom:1px solid var(--line);border-radius:0}
.ribbon-list li.me{border-color:var(--line)}
.who{border:0;padding:0}
.nextlink{margin-top:2rem}
.nextlink .card{padding-block:1.5rem;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.foot{padding-block:2rem}
.foot .wrap{gap:1rem 2rem}
.foot .wrap > p:last-child{white-space:nowrap}
.land .about-section{border-top:1px solid var(--line);padding-block:2.5rem 3rem}
.case-selection{padding-bottom:3.5rem}
.selection-title{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;margin-bottom:1.15rem}
.selection-title p{font-size:var(--fs-cap);color:var(--ink-3)}
.case-list{border-bottom:1px solid var(--line)}
.case-entry{display:grid;grid-template-columns:2.5rem minmax(0,1fr) minmax(0,1.2fr);gap:2rem;border-top:1px solid var(--line);padding:2rem 0;color:inherit}
.case-index{font:500 var(--fs-label)/1.8 var(--mono);color:var(--ink-3);padding-top:.1rem}
.case-entry-heading .label{max-width:40ch}
.case-entry h2{font-size:clamp(1.5rem,1vw + 1.2rem,2rem);margin-top:.6rem;max-inline-size:none}
.case-entry-body > p{color:var(--ink-2)}
.case-entry .arrow{color:var(--ink-3);padding-top:1.15rem}
.case-entry:hover h2,.case-entry:hover .arrow{color:var(--accent)}
.case-entry:hover .arrow .a{transform:translateX(3px)}
.case-highlights{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-top:1.5rem}
.case-highlights .n{font:500 1.5rem/1 var(--mono);letter-spacing:-.02em;color:var(--ink-2);display:block}
.case-highlights .l{display:block;font-size:var(--fs-cap);margin-top:.35rem;color:var(--ink-3);max-width:25ch}

/* A diagram drawn in the page, without a frame around each stage. */
.route-diagram{margin:0;padding:0;min-width:0}
.route-title{font:500 var(--fs-label)/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin-bottom:1.5rem}
.route-diagram ol{position:relative;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:2rem;list-style:none}
.route-step{position:relative;min-width:0;padding-top:1.3rem}
.route-step:not(:last-child)::after{content:"";position:absolute;left:9px;right:-2rem;top:4px;height:1px;background:var(--line-2)}
.route-point{width:9px;height:9px;border:1px solid #718298;background:var(--bg);border-radius:50%;position:absolute;top:0;left:0}
.route-step.decisive .route-point{background:var(--accent);border-color:var(--accent)}
.route-label{display:block;font:500 var(--fs-label)/1.3 var(--mono);text-transform:uppercase;letter-spacing:.09em;color:var(--ink-3)}
.route-step strong{display:block;font:500 var(--fs-body)/1.62 var(--body);color:var(--ink-2);margin-top:.35rem}
.route-detail{display:block;color:var(--ink-3);font-size:var(--fs-cap);line-height:1.5;margin-top:.25rem}
.route-foot{font-size:var(--fs-cap);line-height:1.5;color:var(--ink-3);margin-top:1.25rem}

/* Charts retain their scales and labels with much lighter visual weight. */
.data-chart{margin:0;padding:1rem 0 0;border:0;border-radius:0;background:none}
.chart-heading{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;padding-bottom:1.3rem;border-bottom:1px solid var(--line)}
.chart-heading h3{color:var(--ink-2)}
.chart-rows{display:grid;gap:1.3rem;padding:1.5rem 0;list-style:none}
.chart-row{display:grid;grid-template-columns:minmax(15rem,1fr) minmax(0,1.6fr) 4.5rem;align-items:center;gap:2rem}
.chart-label{font-size:var(--fs-cap);color:var(--ink-2);line-height:1.5}
.chart-track{height:3px;background:rgba(167,180,201,.08)}
.chart-track i{display:block;height:100%;min-width:2px;background:var(--bar-color);opacity:.6}
.chart-value{font:500 var(--fs-cap)/1.5 var(--mono);text-align:right;color:var(--ink-2);white-space:nowrap}
.data-chart .cap{max-width:100%;border-top:1px solid var(--line);padding-top:1rem}
html:not(.js) .row .b i,html:not(.js) .funnel .fr .b i{transform:scaleX(1)}

/* Labels and connectors replace the old filled section diagrams. */
.line-figure{margin:0;min-width:0}
.line-stages{display:grid;grid-template-columns:repeat(var(--stages),minmax(0,1fr));gap:1.5rem;list-style:none;padding:1.3rem 0}
.line-stages li{position:relative;min-width:0;padding-top:1.35rem}
.line-stages li::before{content:"";position:absolute;left:0;top:0;width:6px;height:6px;background:var(--bg);border:1px solid #8295a8;border-radius:50%;z-index:1}
.line-stages li::after{content:"";position:absolute;left:8px;right:-1.5rem;top:3px;height:1px;background:var(--line-2)}
.line-stages li:last-child::after{display:none}
.line-stages li:last-child::before{background:var(--accent);border-color:var(--accent)}
.line-stage-label{display:block;font:500 var(--fs-label)/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);margin-bottom:.4rem}
.line-stages strong{display:block;font:500 var(--fs-body)/1.62 var(--body);color:var(--ink-2)}
.line-stages .detail{display:block;font-size:var(--fs-cap);line-height:1.5;color:var(--ink-3);margin-top:.35rem}
.line-figure > .cap{margin-top:1rem;max-width:100%}
.line-loop{padding-bottom:1.3rem;border-bottom:1px dashed var(--line-2);position:relative}
.line-loop::after{content:"↶";position:absolute;right:0;bottom:-12px;color:var(--ink-3);font-size:1.25rem;background:var(--bg);padding-left:1rem}
.gate-lines{list-style:none;display:grid;gap:0}
.gate-lines li{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr) auto;gap:2rem;align-items:baseline;padding:1.25rem 0;border-top:1px solid var(--line)}
.gate-lines strong{font-weight:500;color:var(--ink-2)}
.gate-lines .detail{font-size:var(--fs-cap);line-height:1.5;color:var(--ink-3)}
.gate-outcome{font:500 var(--fs-label)/1.3 var(--mono);letter-spacing:.04em;color:#c59c9c}
.gate-outcome.pass{color:#93b5a4}
.shard-visual{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,1fr);gap:3rem;align-items:center}
.shard-limit{font:500 var(--fs-label)/1.5 var(--mono);color:var(--ink-3);padding-bottom:.7rem}
.shard-bars{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:1.8rem;border-top:1px dashed var(--line-2);padding-top:0}
.shard-bar{display:flex;flex-direction:column;align-items:center;min-width:0}
.shard-track{height:120px;width:100%;position:relative;border-bottom:1px solid var(--line);display:flex;align-items:flex-end;justify-content:center}
.shard-ink{width:16px;height:var(--height);background:rgba(138,197,210,.14);border-top:1px solid var(--accent);position:relative}
.shard-number{position:absolute;top:-25px;left:50%;transform:translateX(-50%);font:500 var(--fs-label)/1.5 var(--mono);color:var(--ink-2)}
.shard-name{font:500 var(--fs-label)/1.5 var(--mono);color:var(--ink-3);padding-top:.7rem}
.shard-caption strong{display:block;font-weight:500;color:var(--ink-2)}
.shard-caption span{display:block;font-size:var(--fs-cap);line-height:1.5;color:var(--ink-3);margin-top:.6rem}
.replay-dimensions{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:2rem;list-style:none;padding:1.2rem 0 1.75rem;border-bottom:1px solid var(--line)}
.replay-dimensions li{position:relative}
.replay-dimensions li:not(:last-child)::after{content:"×";position:absolute;right:0;top:5px;color:#536074;font-size:1.15rem}
.replay-dimensions strong{display:block;font:400 1.85rem/1.25 var(--mono);color:var(--ink-2)}
.replay-dimensions span{display:block;font-size:var(--fs-cap);line-height:1.5;margin-top:.5rem;color:var(--ink-3)}
.replay-result{display:flex;align-items:baseline;justify-content:space-between;gap:2rem;padding-top:1.25rem}
.replay-result strong{font:400 1.5rem/1.4 var(--mono);color:var(--ink-2)}
.replay-result span{font-size:var(--fs-cap);color:var(--ink-3);line-height:1.5}

@supports(grid-template-rows:subgrid){
 .cards.c4 .card,.ba .card{display:grid;grid-template-rows:subgrid;grid-row:span 3}
 .tiles .tile{display:grid;grid-template-rows:subgrid;grid-row:span 3;row-gap:.65rem}
 .tiles .tile > *{margin:0}
 .cards.c4 .stat .l{min-height:0}
 .flow .fx{display:grid;grid-template-rows:subgrid;grid-row:span 3;row-gap:.5rem}
 .flow .fx > *{margin:0}
}
@media(min-width:1000px){
 .hero-notes:has(> .dashboard-detail){display:grid;grid-template-columns:1fr 1fr;gap:0 2rem}
 .hero-notes > .authorship{grid-column:1/-1}
 .hero-notes > .dashboard-detail[open]{grid-column:1/-1}
}
@media(max-width:1050px){
 .cards.c4{grid-template-columns:repeat(2,minmax(0,1fr))}
 .case-entry{gap:1.5rem;grid-template-columns:2rem minmax(0,1fr) minmax(0,1.2fr)}
 .lanes-strip .ln{grid-template-columns:1fr;gap:.3rem}
 .lanes-strip .ln:last-child:nth-child(odd){grid-template-columns:1fr}
}
@media(max-width:800px){
 .hero > .hero-grid{gap:2rem}
 .route-diagram ol{gap:1.25rem}
 .route-step:not(:last-child)::after{right:-1.25rem}
 .hero-grid > .stats{grid-template-columns:repeat(2,minmax(0,1fr));gap:1.5rem}
 .authorship{grid-template-columns:1fr;gap:.6rem}
 .who{grid-template-columns:1fr;gap:1.15rem}
 .tiles,.flow.c3,.gates{grid-template-columns:repeat(2,minmax(0,1fr))}
 .case-entry{grid-template-columns:2rem minmax(0,1fr);gap:1.25rem}
 .case-entry-body{grid-column:2}
 .case-highlights{margin-top:1rem}
 .chart-row{grid-template-columns:minmax(12rem,1fr) minmax(0,1fr) 4.5rem;gap:1rem}
 .line-stages{grid-template-columns:1fr;gap:0;padding:0}
 .line-stages li{padding:0 0 1.35rem 1.75rem}
 .line-stages li::before{top:7px}
 .line-stages li::after{left:3px;right:auto;top:15px;bottom:-7px;width:1px;height:auto}
 .line-stages li:last-child{padding-bottom:0}
 .line-stage-label{margin-bottom:.15rem}
 .line-stages .detail{margin-top:.2rem}
 .line-loop{padding-bottom:1rem}
 .shard-visual{grid-template-columns:1fr;gap:1.5rem}
 .shard-caption{display:flex;flex-wrap:wrap;gap:.3rem 1.5rem;align-items:baseline}
 .shard-caption span{margin:0}
 .gate-lines li{grid-template-columns:1fr auto;gap:.35rem 1rem}
 .gate-lines .detail{grid-column:1;grid-row:2}
 .gate-outcome{grid-column:2;grid-row:1}
}
@media(max-width:540px){
 .nav .wrap{height:58px;gap:.7rem}
 .tabs{gap:14px}
 .tabs a{min-width:26px;justify-content:center}
 .hero{padding-top:2rem;padding-bottom:2rem}
 .actions{gap:1rem;flex-wrap:wrap}
 .route-title{margin-bottom:1.1rem}
 .route-diagram ol{grid-template-columns:repeat(2,minmax(0,1fr));gap:1.2rem 1.5rem}
 .route-step{border-top:1px solid var(--line);padding-top:.8rem}
 .route-point{width:5px;height:5px;top:-3px}
 .route-step::after{display:none}
 .route-foot{margin-top:1rem}
 .hero-grid > .stats{gap:1.4rem}
 .hero-grid > .stats:has(>.stat:nth-child(3):last-child) .stat:last-child{grid-column:1/-1}
 .selection-title{align-items:baseline}
 .case-entry{grid-template-columns:1.4rem minmax(0,1fr);column-gap:.85rem;padding:1.5rem 0}
 .case-highlights{gap:1.5rem}
 .cards.c4,.tiles,.flow.c3,.gates{grid-template-columns:1fr}
 .cards.c4 .card,.ba .card,.tiles .tile,.flow .fx{grid-template-rows:auto;grid-row:auto}
 .metrics{grid-template-columns:repeat(2,minmax(0,1fr));gap:1.2rem}
 .metrics > .stat:last-child:nth-child(odd){grid-column:1/-1}
 .lanes-strip{grid-template-columns:1fr}
 .lanes-strip .ln,.lanes-strip .ln:last-child:nth-child(odd){grid-template-columns:minmax(0,.8fr) minmax(0,1fr);gap:1rem;grid-column:auto}
 .chart-row{grid-template-columns:minmax(0,1fr) auto;gap:.65rem 1rem}
 .chart-value{grid-column:2;grid-row:1}
 .chart-track{grid-column:1/-1;grid-row:2}
 .shard-bars{gap:.8rem}
 .shard-ink{width:13px}
 .replay-dimensions{grid-template-columns:repeat(2,minmax(0,1fr));gap:1.5rem 2rem}
 .replay-dimensions li::after{display:none}
 .replay-result{display:block}
 .replay-result > span{display:block;margin-top:.5rem}
 .acc summary{grid-template-columns:2rem minmax(0,1fr) auto;gap:.6rem}
 .acc .in{padding-left:0}
}
@media(prefers-reduced-motion:reduce){
 .js .rv,.case-entry .a,a.card{transition:none}
 .case-entry:hover .arrow .a{transform:none}
}
@media print{
 .nav{position:static}
 .route-diagram,.line-figure,.data-chart{break-inside:avoid}
}
"""
