# Content for the responsive case-study site. Every number is the verified figure from
# .claude/future_plans/2026-09-03_builder_case_study_v2.md and the deck-2 copy doc (3 Sep 2026).
DATE = "3 September 2026"
NAME = "Lukasz Rodzen"
ROLE = "architect · release owner · operator"
CONTACT = "[ADD LINKEDIN / EMAIL]"
CONTACT_HTML = ""  # contact details live on the CV that links here; fill in later if wanted
LOCATION = "Poland · remote"
OPMODEL = ("I own the architecture, the acceptance criteria, the controls, the release decision and production verification. "
           "AI models write the implementation inside a delivery workflow I built; I review the evidence, adjudicate their disagreements "
           "and sign every deploy. Nothing ships that I have not reviewed and accepted.")
BOUNDARY = ("And I will tell you where the boundary is: the changes I would not make this way, "
            "and who I would bring in instead.")

LANDING = dict(
    kicker="Architect · AI delivery owner · Poland, remote",
    h1="One person built a live trading system, then the workflow that ships it.",
    lead=("I designed and operate an automated trading system that runs on Solana with my own funds, and the AI delivery workflow that ships every change to it. "
          "Two case studies: one for product and engineering readers, one for anyone hiring AI-native builders."),
    boundary="Personal engineering project. It trades only my own funds: no client assets, no investment service, no advice.",
    stats=[("16", "months, one architect"), ("1,300", "confirmed trades, my own funds"), ("66 ms", "engine time per trade, median"), ("112", "documented delivery runs")],
    fn="A trade here is one position. 2,843 on-chain signatures stand behind the 1,300 positions, 1,685 buy legs and 1,158 sell legs, because a position can close in several legs. Engine time is the engine's own work per trade, from price quote to submitted transaction; 66 ms is the median across the 1,228 buys with stage timings, 90% of them under 200 ms. From signal to confirmation on chain the median is 1.3 s, most of it the blockchain's own confirmation (625 ms median) and the message's delivery from Telegram. Runs from 26 March to 1 September 2026, numbered 1 to 134. Measured " + DATE + ".",
    cards=[
        dict(n="01", title="The system", who="for product and engineering readers", href="the-system.html", accent="cyan",
             text=("A production system that turns public market signals into capped, auditable on-chain trades, with my own funds only: 66 ms of engine time per trade, about 1.3 seconds from signal to confirmation. "
                   "Two servers, a custom Rust engine, and on-chain limits a trading key cannot bypass."),
             nums=[("66 ms", "engine time per trade, median"), ("2,843", "on-chain signatures, verifiable")]),
        dict(n="02", title="How I ship", who="for anyone hiring AI-native builders", href="how-i-ship.html", accent="green",
             text=("One AI coordinates the job; specialist agents research, plan, build and test it; models from two other vendors challenge the work before anything risky ships. "
                   "Ten phases, 62 steps, 34 gates, and a memory loop that turns failures into rules, across 112 documented runs."),
             nums=[("112", "documented runs"), ("3", "AI vendors on every review")]),
    ],
)

# ---------------------------------------------------------------- case study 1
S1 = dict(
    slug="the-system", num="01", title="The system", tab="The system",
    subtitle="A live Solana trading system, specified, hardened and run by one person.",
    sections=[
    dict(id="cover", kind="cover",
         kicker="Case study 1 of 2 · the system",
         h1="One person. Two servers. A live trading system with my own money on-chain.",
         lead=("SKYNET turns Telegram calls and tracked wallets into ranked strategies and executes them on Solana "
               "with 66 ms of engine time per trade, from a Rust engine I specified, had built, tested and hardened."),
         metrics=[("16", "months, one architect"), ("1,300", "confirmed trades, my own funds"), ("66 ms", "engine time per trade, median")],
         fn="A trade is one position. 2,843 on-chain signatures stand behind the 1,300 confirmed positions: 1,685 buy legs and 1,158 sell legs, because a position can close in several legs. Engine time is the engine's own work per trade, from price quote to submitted transaction, the dashboard's Bot Speed: 66 ms median across the 1,228 buys with stage timings, 90% under 200 ms. From signal to confirmation on chain the median is 1.3 s, most of it the blockchain's confirmation (625 ms median) and delivery from Telegram. Measured " + DATE + ".",
         first="journey", other=("Case study 2 · How I ship", "how-i-ship.html"),
         shot="health.webp", shot_caption="Operator home · live services, host vitals and database"),
    dict(id="journey", kind="journey",
         kicker="How it was built",
         h1="From a Grok chat window to a two-server operation in sixteen months",
         lead="Commits per month from git across the three repositories, April 2025 to September 2026. One file at the start; three codebases and an on-chain program at the end.",
         milestones=[
            ("Apr 2025", "One 1,295-line Python file, written in a Grok web chat. I had never opened an IDE."),
            ("Jul 2025", "Dashboard. Continuous tracking begins."),
            ("Oct 2025", "Claude Code becomes the workshop. Sharded price feed. First independent AI auditors."),
            ("Nov 2025", "Second server, Rust engine, encrypted tunnel. The delivery workflow is born."),
            ("Feb 2026", "Specialist sub-agents: research, plan, implement, audit, verify."),
            ("Mar 2026", "First confirmed on-chain trade."),
            ("Jun 2026", "On-chain program live on mainnet."),
            ("Sep 2026", "Three codebases, 112 documented workflow runs, my own funds in production."),
         ],
         note="The delivery loop is its own case study. This one is about what it produced."),
    dict(id="what", kind="four",
         kicker="What it does",
         h1="From a chat message to an on-chain trade, unattended",
         banner="pipeline",
         lead="Four jobs, one dashboard. I choose which public signals to follow with my own funds; the system listens, ranks, executes inside fixed caps and contains the damage when something goes wrong.",
         cards=[
            ("Listen", "149", "live sources: 63 groups, 86 wallets, 4 chains", "Every message and every wallet transaction, around the clock."),
            ("Rank", "17", "exit strategies replayed per source, per regime", "Every source scored by what each strategy would have done."),
            ("Execute", "66 ms", "engine time per trade, median of 1,228", "A Rust engine on its own server builds the transaction itself, from quote to submit, and manages the exit. The chain then takes about 0.6 s to confirm."),
            ("Contain", "4", "fail-closed control layers", "Kill switch, per-trade and daily caps, circuit breakers."),
         ],
         note="I choose which public signals to follow with my own funds. Execution stays inside fixed caps, and every step is observable on one dashboard."),
    dict(id="infra", kind="infra",
         kicker="Infrastructure",
         h1="Two servers, one encrypted tunnel, and the Solana blockchain",
         lead="Analysis is heavy and chatty; execution has to be fast and quiet. So the brain and the hands live on two Hetzner machines joined by an encrypted tunnel, and the hands keep closing positions even if the brain goes down.",
         feeds=[("Telegram", "63 groups, read as messages arrive"),
                ("Birdeye price WebSocket", "15-second candles · 8 sharded connections"),
                ("Helius wallet WebSocket", "every transaction of 86 tracked wallets"),
                ("Market data", "Nansen · DefiLlama · CoinGecko · CoinMarketCap")],
         brain=("Finland · the brain · Python", ["Detection and queues · 8 workers, 5-layer dedup", "TimescaleDB · 28 GB · 12.3M rows",
                "Replay and sizing engine · nightly, 17 strategies", "Regime classifier · 27 signals, daily",
                "Operator dashboard · 202 endpoints"]),
         hands=("Nuremberg · the hands · Rust", ["Signal subscriber · verify, dedupe, fan out", "Jupiter routing · hand-built transactions",
                "Helius Sender · ~1 s to confirmation", "Position monitor · prices decoded on-chain",
                "Two lanes · main wallet · program-owned account", "Controls · kill switch, caps, breakers"]),
         chain=("Solana mainnet", ["Anchor program · on-chain limits on the trading key", "Jupiter v6 · live since Jun 2026"]),
         note=("Why two servers? Analysis is heavy and chatty. Execution has to be fast and quiet. Splitting them keeps a "
               "dashboard spike or a nightly job off the trade's critical path, and the engine keeps closing positions if the brain goes down.")),
    dict(id="engine", kind="points",
         kicker="The execution engine · built, not bought",
         h1="No trading library. The engine assembles the transaction itself.",
         lead="22 modules and 54,000 lines of Rust on their own server, doing one job: turn a verified signal into a landed Solana transaction and manage the exit.",
         more_label="How the transaction is built and hardened",
         points=[
            "Exactly one compute-unit limit and one price, Jupiter's instructions verbatim, a validator tip from a 10-account pool, address lookup tables. Preflight off, zero retries, confirmation polled every 200 ms against a ~400 ms block.",
            "Solana gives a transaction 1,232 bytes, and a fresh pump.fun route does not fit. Seven constant venue accounts are pre-warmed into the engine's own lookup table, appended and never prepended, because prepending re-inflates every healthy route.",
            "Exit prices are decoded from the pool's own bytes on-chain, 8 venues at exact byte offsets, with the router only as fallback. Signals cross the tunnel HMAC-signed with a freshness window and an idempotency cache, so a duplicate message is designed never to become a duplicate buy.",
         ],
         visual="stages",
         metrics=[("66 ms", "engine time per trade, median"), ("196 ms", "90th percentile"), ("1,245", "test functions in the engine")],
         fn="Engine time counts the engine's own work per trade: price quote, route, transaction build and submit. Median 66 ms and 90th percentile 196 ms across the 1,228 buys with stage timings; 90% under 200 ms. The chain's confirmation adds a median 625 ms on top. Every control fails closed: kill switch on entries, a 30 SOL cap enforced in three independent places, sizing that refuses on a missing SOL/USD price, a sell circuit breaker at three retries. 32K lines of tests."),
    dict(id="data", kind="points",
         kicker="Real-time data",
         h1="The price provider caps a connection at 100 addresses. I needed 552.",
         lead="So the live price feed is split across auto-scaling connections, placed by a stable hash so nothing moves on a restart, and every 15-second candle lands in a time-series database built for exactly this.",
         more_label="How the feed is sharded",
         points=[
            "The feed is sharded across auto-scaling WebSocket connections, placed by SHA-256 hash so placement survives restarts. Python's built-in hash is salted per process and was rejected.",
            "The scaler acts on the busiest shard, not the average, with hysteresis and a dry run before any scale-down. An average of 77 can hide a shard at 85.",
            "Every 15-second candle lands in TimescaleDB. The hot read runs 230× faster through a continuous aggregate.",
         ],
         banner="shards",
         metrics=[("8", "shards live · 6 needed, 2 headroom"), ("552", "contracts on the feed"), ("12.3M", "rows in TimescaleDB")],
         note="Still open, and written down: the feed is certified for today's load, not for 1,500 contracts. The docs say so, and they list the defects that block the next step."),
    dict(id="controls", kind="controls",
         kicker="On-chain controls",
         h1="A trading key that cannot move the money",
         lead="My funds sit in a program-owned account on Solana. The engine holds a separate trading key that can open and close positions inside limits the program enforces on every transaction, and can never withdraw.",
         points=[
            "My funds sit in a program-owned account on Solana. My wallet key is the only authority that can deposit, withdraw, pause, or revoke the trader.",
            "The engine holds a separate executor key that can only open and close positions, inside limits the program enforces on every transaction.",
            "Router instructions arrive as opaque account lists, so they are constrained rather than trusted: capped at 64 accounts, every writable account allowlisted, only two route discriminators accepted.",
         ],
         keys=[("My wallet key", ["Deposit", "Withdraw", "Pause", "Revoke the trading key"], "green"),
               ("Trading key, held by the engine", ["Open positions", "Close positions"], "cyan")],
         forbidden="cannot withdraw · ever",
         rules=["0.5 SOL per trade", "2 SOL per day", "lamports spent and tokens sold counted separately",
                "10 Token-2022 extensions rejected", "transfer fee capped at 200 bps", "the account pays its own fees from a separate counter"],
         metrics=[("73", "tests run on a fork of mainnet"), ("46", "unit tests"), ("14", "program instructions · 43 error codes")]),
    dict(id="intelligence", kind="points",
         kicker="Intelligence",
         h1="Every tracked source replayed through 17 strategies, nightly",
         lead="Every source is scored by what each of 17 exit strategies would have done, across chains and market regimes, precomputed each night so every page loads instantly.",
         more_label="How the replay works",
         points=[
            "300+ sources ever tracked × 17 exit strategies × 5 chains × 4 market regimes, precomputed nightly so every page loads instantly.",
            "Any result can be re-rendered at operator-defined position sizes, seven market-cap tiers deep.",
            "The market-regime label is validated on 21,345 real outcomes (z = 4.07, p < 0.0001). Caveat kept: 183 of 407 labeled days are backfilled with a simpler classifier, so this validates the labeling concept, not retroactive production accuracy.",
         ],
         visual="cube",
         metrics=[("17", "exit strategies"), ("6.2M", "precomputed rows"), ("27", "regime signals")],
         fn="The replay table carries five chain values; today's 40,908 tracked contracts sit on four of them. 17,820 tasks a night, about 25 minutes."),
    dict(id="failures", kind="beforeafter",
         kicker="Failures → controls",
         h1="The controls that exist because something broke",
         lead="Three real failures, and the permanent check each one left behind. None of them can happen the same way twice.",
         items=[
            ("A guard that was too eager deleted 28 real wallet trades across four instruction shapes.",
             "A 7,150-cell differential corpus that asserts every improvement is consumed, run before any parser change ships.",
             "7,150", "cells checked before a parser change"),
            ("A concentrated pool was priced 3.02× wrong by reserve ratio, producing a phantom stop-loss.",
             "A structural gate before any decoded price is trusted: decimals match, legs move opposite, both non-zero, then drift bands.",
             "3.02×", "the error the gate now refuses"),
            ("The nightly sizing job froze the web process 24 ms per spawn: uvloop's fork against a 3.3 GB address space.",
             "The worker moved out of process, 2,623 s → 329 s, and refuses to boot on uvloop at all.",
             "7.97×", "faster, and a boot-time assertion"),
         ],
         note="These three failures are retained as regression gates. Each now fails a build before it can reach production."),
    dict(id="measured", kind="tiles",
         kicker="Measured on the production system · " + DATE,
         h1="Measured, with the populations printed",
         lead="Six numbers from the live database, each with the population it was measured on.",
         tiles=[
            ("1,300", "confirmed trades, one per position", "2,843 on-chain signatures behind them, verifiable on any explorer: 1,685 buy legs, 1,158 sell legs."),
            ("66 ms", "engine time per trade · median of 1,228 buys", "Quote to submitted transaction, the dashboard's Bot Speed; 90% under 200 ms. Signal to on-chain confirmation: 1.3 s median, of which the chain's confirmation is 625 ms."),
            ("40,908", "contracts tracked · 4 chains", "SOL 34,215 · BSC 3,060 · ETH 2,870 · Base 763"),
            ("12.3M", "rows in TimescaleDB", "28 GB · 95 tables"),
            ("1,245", "engine test functions", "32K lines of tests"),
            ("119", "on-chain program tests", "46 unit + 73 mainnet-fork"),
         ],
         note="371K implementation lines and 5,066 commits across three repositories were generated under the delivery workflow. They measure the workflow's output, not me."),
    dict(id="close", kind="close",
         kicker="See it running",
         h1="The system is the proof.",
         lead="Two things I can show live in an interview.",
         sessions=[("The product, live", "Any page of the running system: the feed, the engine, the on-chain controls, and the data behind every number here."),
                   ("The workflow, live", "A real task taken through the delivery loop: research, plan, AI implementation, separate review lanes, my go / no-go, verification in production.")],
         boundary="Where I would not use this: a change to key custody or withdrawal authority. That gets a human specialist and a formal audit, not a review panel.",
         next=("Case study 2 · How I ship", "how-i-ship.html")),
    ],
)

# ---------------------------------------------------------------- case study 2
GROWTH = [("2025-11-26", 284), ("2025-11-30", 1162), ("2025-12", 4533), ("2026-01", 5302), ("2026-02", 5386), ("2026-03", 5386), ("2026-04", 6292), ("2026-05", 10307), ("2026-06", 10405), ("2026-07", 10700), ("2026-08", 10837), ("2026-09-03", 11009)]
GROWTH_FLAGS = [("2025-11-26", "born · 284 lines"), ("2026-02-22", "sub-agents"), ("2026-04-14", "harness · reviews"),
                ("2026-05-05", "skills · self-audit"), ("2026-07-13", "third vendor · routing"), ("2026-09-03", "run 134 · 11,009")]

# case study 2 lives in s2_v6.py
