"""Responsive, unboxed figures using the original banner facts and populations."""
from html import escape as E


def stages(items, caption, loop=False):
    rows = ''.join(f'<li><span class="line-stage-label">{E(label)}</span><strong>{E(title)}</strong><span class="detail">{E(detail)}</span></li>' for label,title,detail in items)
    return f'<figure class="line-figure rv"><ol class="line-stages{" line-loop" if loop else ""}" style="--stages:{len(items)}">{rows}</ol><figcaption class="cap">{E(caption)}</figcaption></figure>'


def pipeline():
    return stages([
        ("Public inputs", "Signals", "Telegram calls, tracked wallets and live prices"),
        ("Analysis", "Detect and rank", "8 workers · 17 strategies"),
        ("Execution", "Rust engine", "66 ms engine time, median"),
        ("On-chain", "Solana", "Program-enforced caps")
    ], "Kill switch, per-trade and daily caps, and circuit breakers. Controls fail closed.")


def servers():
    return stages([
        ("External", "Four input streams", "Telegram, wallets, prices and market data"),
        ("Finland", "Analysis", "Python · TimescaleDB"),
        ("Nuremberg", "Execution", "Rust · signed signals"),
        ("Blockchain", "Solana mainnet", "Transactions out; prices and confirmations back")
    ], "The two servers communicate through an encrypted WireGuard tunnel. Heavy analysis stays separate from execution.")


def layers():
    return stages([
        ("Always loaded", "Constitution", "The rules for every agent"),
        ("2,110 lines", "Navigation index", "Find the relevant component"),
        ("19,514 lines", "Architecture map", "Read how it works today"),
        ("Three contracts", "Shared definitions", "One source of truth each"),
        ("Decisive evidence", "The code", "Validate the map against source")
    ], "One reading order, every agent, every run. Map before code; the code wins when they disagree.")


def loop():
    return stages([
        ("Begin", "audit-task", "Scope, plan and implementation"),
        ("Resume", "Handover", "Context for the next session"),
        ("Retain", "Archive", "The run and its evidence"),
        ("Evaluate", "Progress review", "Score the completed work"),
        ("Update", "Documentation audit", "Keep the architecture current")
    ], "One run ID and its evidence, stored on disk. The model forgets; the run does not. Recorded spans include 30 hours, 28 hours and four days.", loop=True)


def chain():
    return stages([
        ("Input", "A skill", "Vendor documentation"),
        ("Checkpoints 1–2", "The planner cites", "The relevant instruction"),
        ("Checkpoints 3–4", "The implementer applies", "The rule in the code"),
        ("Checkpoints 5–7", "The auditor proves", "A file and line, not a claim")
    ], "Seven checkpoints establish that a skill was used. A citation without a file and line fails.")


def gate():
    return '''<figure class="line-figure rv"><ul class="gate-lines">
<li><strong>“I edited the file”</strong><span class="detail">The diff shows zero changes. The claim has no supporting evidence.</span><span class="gate-outcome">Stops</span></li>
<li><strong>Claim + receipt</strong><span class="detail">The evidence is present and verified.</span><span class="gate-outcome pass">Passes</span></li>
</ul><figcaption class="cap">34 gates · 146 hard blocks. Claims alone do not move the run forward.</figcaption></figure>'''


def shards():
    counts = [70,68,71,69,70,67,69,68]
    bars = ''.join(f'<div class="shard-bar"><div class="shard-track"><div class="shard-ink" style="--height:{count}%"><span class="shard-number">{count}</span></div></div><span class="shard-name">S{i+1}</span></div>' for i,count in enumerate(counts))
    return f'''<figure class="line-figure rv" aria-label="552 contracts across eight connections, each below the 100-address provider cap">
<div class="shard-visual"><div><div class="shard-limit">100 addresses / connection · provider limit</div><div class="shard-bars">{bars}</div></div><div class="shard-caption"><strong>Stable placement</strong><span>SHA-256, not a salted hash.<br>A restart returns each contract to the same shard.</span></div></div>
<figcaption class="cap">552 contracts · 8 connections · 6 needed, 2 headroom.</figcaption></figure>'''


def replay():
    dimensions = [("300+", "sources ever tracked"),("17", "exit strategies"),("5", "chain values"),("4", "market regimes")]
    axes = ''.join(f'<li><strong>{E(number)}</strong><span>{E(label)}</span></li>' for number,label in dimensions)
    return f'''<figure class="line-figure rv"><ul class="replay-dimensions">{axes}</ul>
<div class="replay-result"><div><strong>6.2M</strong> <span>precomputed rows</span></div><span>17,820 replay tasks · about 25 minutes · nightly</span></div>
<figcaption class="cap">The replay cube · one cell per source × strategy × chain × regime · 6.2M rows, refilled by 17,820 replay tasks a night</figcaption></figure>'''


BANNERS = dict(pipeline=pipeline,servers=servers,layers=layers,loop=loop,chain=chain,gate=gate,shards=shards)
