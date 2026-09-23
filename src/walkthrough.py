"""Published full walkthrough transcript and chapter cues."""

DURATION = 511

TRANSCRIPT = ['Skynet brings research, strategy design, position sizing, and trade execution into one '
 'connected workspace. Let’s walk through how it works.',
 'It starts with signals from Telegram and tracked wallets. The research layer puts those '
 'signals in context. Strategies define the rules, sizing defines the exposure, and the terminal '
 'brings execution and monitoring together.',
 'Start with the source rankings. Open a profile, and you can look beyond the headline numbers: '
 'how active the source is, the market caps it enters, and how different models perform. Time, '
 'chain, and market filters help narrow the comparison.',
 'Here’s Trader A. We’re using a hundred-dollar paper entry across the full history. The leading '
 'models are below zero, but the regime labels reveal a pattern: positive results in bull '
 'markets, and losses in sideways and bear markets. Let’s follow Model Six through the filters.',
 'Select Bull, and the ranking changes. Model Six moves to the top, with three thousand two '
 'hundred and fifty dollars in historical replay profit. Models Four and Two are positive as '
 'well. We haven’t changed the entry size. We’re looking at the calls that fell within '
 'bull-market conditions.',
 'Now switch to Bear. Model Six shows a replay loss of one thousand five hundred and fifty '
 'dollars, and the leading models are below zero. That’s why market context matters. The overall '
 'result combines periods where the same strategy behaved very differently.',
 'Before changing the sizing, return to all regimes. Model Six shows a three thousand five '
 'hundred dollar loss across seven hundred and seventy-two cases. Its exit rules are a '
 'fifty-percent stop loss and a five-times take profit. We’ll keep those rules fixed for the '
 'comparison.',
 'Open Custom Sizing and select Test Four. This preset switches off entries below three hundred '
 'thousand dollars in market cap. From there, it allocates one thousand dollars to the next '
 'tier, two thousand to the one-to-ten-million tier, and three thousand above ten million. The '
 'two-percent limit is set to trim mode.',
 'Apply the preset, and the strategy cards update. The date range, chain, and exit rules stay '
 'the same. In this recorded snapshot, Model Six moves from a three thousand five hundred dollar '
 'loss to fifty-five thousand dollars in historical replay profit. Models Four and Two are also '
 'positive. The monthly curves, regime breakdown, and ranking all reflect the new settings. '
 'Model Six now includes three hundred and fifteen cases.',
 'Switch back to Paper, and Model Six returns to its three thousand five hundred dollar loss. '
 'Apply Test Four again, and the positive replay returns. Two things have changed: which entries '
 'are included, and how much is allocated to them. That changes both the results and the '
 'exposure. Maximum drawdown in the custom view is twenty-eight thousand dollars. These are '
 'historical simulations with trading costs excluded. The comparison helps you understand the '
 'effect of your rules; it doesn’t establish how they’ll perform in future trading.',
 'Strategy Center brings these trader-and-model combinations into one view. Compare exit rules, '
 'replay results, market regimes, and consistency across the cards. When something deserves a '
 'closer look, open its statistics or continue into simulation.',
 'Market Intelligence adds the wider context: daily regimes, intraday alerts, and reversal '
 'indicators. Coverage and freshness are shown alongside the signals, so you can see how much '
 'information is available and how recently it was updated.',
 'Now let’s move into the trading terminal. The chart, swap controls, strategies, and trade '
 'history share one workspace. You can move from researching a setup to managing its execution, '
 'then come back to inspect the result.',
 'The wallet balances are loaded here. You can see the available Solana balance and the tokens '
 'held in the wallet. Open the selector to inspect quantities and displayed values. Choose a '
 'holding, and its available balance appears in the swap panel, ready for the amount you want to '
 'enter.',
 'For a manual Phantom swap, the system prepares an unsigned transaction. You review and approve '
 'it in your wallet. Phantom signs it, and the selected engine handles submission.',
 'The Ultra option uses Jupiter’s order and execution flow. With Phantom connected, the prepared '
 'transaction returns to the wallet for signing. The selected tokens, amount, and active engine '
 'remain visible together in the swap panel.',
 'The custom route is labelled Legacy in the terminal. Jupiter supplies the quote and swap '
 'instructions. The Rust engine builds the transaction, Phantom signs it, and the custom '
 'submission path sends it through Helius Sender.',
 'Automation uses a different signing flow. The bot checks incoming signals against the '
 'configured strategy, and its execution wallet handles signing. The Rust service connects '
 'transaction preparation, submission, confirmation, and the monitoring of the resulting '
 'position.',
 'Inside the custom engine, the instructions become a transaction with the configured compute '
 'budget, priority fees, and submission settings. Once the trade is confirmed, that execution '
 'connects back to its position record.',
 'The published measurements report a median engine time of sixty-six milliseconds, and around '
 'one point three seconds from signal to confirmation. Those figures describe different stages. '
 'Next, let’s inspect the timings of an individual recorded trade.',
 'Open a recent copy trade from Positions. This entry was triggered by the automation. The '
 'record brings its outcome, costs, and entry context together. From here, we can open the '
 'timing breakdown and follow what happened after the signal arrived.',
 'The displayed end-to-end time for this entry is two point four two three seconds. Within that, '
 'quoting, swap instructions, transaction building, and submission took eighty-one milliseconds '
 'combined. Network confirmation is shown separately at four hundred and seventeen milliseconds. '
 'You can see the engine’s speed in context, alongside the rest of the recorded workflow.',
 'This position was later closed manually. The exit record shows seventy-nine milliseconds of '
 'engine work, with confirmation measured separately at four hundred and sixteen milliseconds. '
 'You can also inspect the route, slippage, fees, and transaction links. Open the log trace to '
 'follow the recorded events in more detail. The timing numbers connect to evidence you can '
 'check.',
 'That’s what makes this view useful. You can inspect the stages behind an execution, see where '
 'time was spent, and follow the transaction evidence. Manual swaps and copy trades each keep '
 'their own breakdown.',
 'Back in the terminal, the strategy rail lists each configured source and model, its status, '
 'and recent performance. Search or sort to find a strategy, then open its overview, positions, '
 'history, or configuration. Those views stay connected within the same workspace.',
 'The overview brings net profit and loss, win rate, trade count, and exit outcomes together. '
 'The realized performance curve shows how results developed over time. The fee breakdown helps '
 'explain how gross trading results translate into net performance.',
 'Open Configuration to see the rules behind those results: base investment, daily trade limits, '
 'take profit, stop loss, the selected wallet, and buy and sell slippage. The model and status '
 'stay visible, keeping the strategy’s setup close to the activity it produced.',
 'Positions connects each open lot to its source and model. Entry details, valuation fields, '
 'exit rules, and transaction links sit together. You can move directly from a strategy to the '
 'positions it created and inspect their current state.',
 'Trade History gives you the individual records behind the summary: entries, exits, execution '
 'status, outcomes, and transaction references. Together with the fee breakdown, it helps '
 'explain the result over time. These execution records are kept distinct from the historical '
 'replays used in research.',
 'The wider system also includes vault and wallet views. Portfolio monitoring, manual wallet '
 'approval, and automated execution each have their own role, with different signing '
 'responsibilities.',
 'Monitoring continues throughout the workflow. Token tracking keeps entry context, current '
 'observations, historical highs, and data freshness visible. Wallet research adds another view '
 'of activity, while the strategy and execution records show how the system responded to the '
 'information it received.',
 'That’s Skynet: from the first signal to the strategy, the trade, and the evidence behind the '
 'result.']

CHAPTERS = [{'title': 'The system', 'start': 0},
 {'title': 'System map', 'start': 10.5},
 {'title': 'Source research', 'start': 24.566666666666666},
 {'title': 'Trader A: regime labels', 'start': 39.2},
 {'title': 'Bull filter', 'start': 56.0},
 {'title': 'Bear filter', 'start': 73.0},
 {'title': 'Paper baseline', 'start': 88.26666666666667},
 {'title': 'Custom sizing preset', 'start': 104.96666666666667},
 {'title': 'Custom sizing results', 'start': 123.4},
 {'title': 'Paper vs custom sizing', 'start': 149.46666666666667},
 {'title': 'Strategy Center', 'start': 181.36666666666667},
 {'title': 'Market Intelligence', 'start': 197.13333333333333},
 {'title': 'Trading terminal', 'start': 211.76666666666668},
 {'title': 'Balances and holdings', 'start': 225.06666666666666},
 {'title': 'Phantom swaps', 'start': 240.73333333333332},
 {'title': 'Ultra execution', 'start': 251.33333333333334},
 {'title': 'Custom swap engine', 'start': 265.46666666666664},
 {'title': 'Automated bot engine', 'start': 278.5},
 {'title': 'Transaction pipeline', 'start': 294.6},
 {'title': 'Published measurements', 'start': 307.6666666666667},
 {'title': 'Open a copy trade', 'start': 322.3333333333333},
 {'title': 'Entry timing breakdown', 'start': 336.9},
 {'title': 'Exit and log trace', 'start': 358.03333333333336},
 {'title': 'Execution you can inspect', 'start': 380.1666666666667},
 {'title': 'Strategy workspace', 'start': 392.3},
 {'title': 'Strategy overview', 'start': 408.53333333333336},
 {'title': 'Strategy configuration', 'start': 424.1333333333333},
 {'title': 'Open positions', 'start': 440.7},
 {'title': 'Trade history', 'start': 455.3333333333333},
 {'title': 'Vault and wallet context', 'start': 473.06666666666666},
 {'title': 'Ongoing monitoring', 'start': 484.7},
 {'title': 'SKYNET', 'start': 503.1}]
