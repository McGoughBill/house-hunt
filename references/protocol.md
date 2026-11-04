# Protocol, scoring and lessons

Background for changing the skill or explaining a result. A run does not need it.

## Stages

| Stage | Who | What | Output |
|---|---|---|---|
| 0. Profile | Opus + buyer | Deduce city, budget, beds, strategy, hard rules, anchors and vibe; ask at most 3 questions (`references/new-profile.md`) | `profiles/P/profile.json` |
| 1. Scout (new profiles only) | 2 Haiku agents | Map the vibe onto look-alike neighbourhoods; list portals, local agents, auctions and sold-price sources | areas and sources in the profile |
| 2. Search | 1 Haiku agent per source | Houses that fit the brief and are **not already known** (`known.txt`); price changes on known ones | `work/P/D/results/search/` |
| 3. Longlist | `hh.py ingest` | Normalise, match against the registry, filter to the brief | `state/history/longlist-D.md` (new only), `state/longlist.md` (all) |
| 4. Judge | 1 Haiku agent per new house; 1 per house whose price change moves its score | Gates, V, W, C, criteria, risk | compact runs in `state/registry.json`, raw files in `state/raw/D/` |
| 5. Top-up | Haiku | More runs for the top 40, to 3 scored runs each | medians |
| 6. Shortlist | `hh.py shortlist` | Top 20 that pass; a phone notification only when a new house enters | `state/shortlist.md`, `state/history/shortlist-D.md` |
| 7. Save | `hh.py save` | Commit and push the state | this repo |

Weekly runs repeat stages 2–7. The registry remembers every house, so each longlist holds only what is new.

## How a house is scored

- **Brief.** `profile.json` holds the gates, 18 weighted criteria (weights total 100) and the buy test. `hh.py brief` renders them into `brief.md`, which the judges read.
- **Judges' estimates.** Each judge estimates three things: V, the value once done up (the median of 3 done-up sales of the same type, on the same street, in the last 2 years); W, the cost of the works; and C, the buying costs.
- **Computed criteria.** The ranker works out three things from each run's V, W and C at the current asking price, so a price cut re-scores a house without a new judge:
  - criterion 2, the margin: 0.9V − 1.15W − C − asking;
  - criterion 18, the uplift: V ÷ asking;
  - the budget gate.
- **Totals.**
  - Total = Σ(weight × median score) ÷ 5.
  - A missing median counts as a neutral 3 and is flagged.
  - A gate fails when it fails on a majority of runs.
  - A house is GONE when its latest run finds it sold, or most runs do.
- **Re-judging after a price change.** One Haiku agent re-judges, given the earlier run as context, only when the change would move the total by 0.5 or more, or change the gate status.
- **Weight presets.** In `templates/presets.json`: `improve` (buy cheap, refurbish) and `ready` (move straight in, with no uplift weight).

## Lessons from the first run (Sheffield, 3 Nov 2026)

- **Concurrency.** About 20 agents at once tripped the web-search rate limit for 15 minutes. Run 10.
- **Blocked portals.** WebFetch often refuses Rightmove and Haybrook. Agents find the same house on Zoopla, OnTheMarket, PrimeLocation, the agent's own site, or a Rightmove brochure PDF.
- **Sold prices.** Sold-price records rarely say whether a house was done up, so V runs low and most margins come out negative. Use totals to compare houses, not to price them.
- **Criterion 18.** Without it, houses already done up outscored run-down houses with good bones.
- **Interruptions.** Interrupting the main session kills the agents still running, without warning. `hh.py orphans --reset` finds and relaunches them.
- **Agent output.** Agents write JSON to a file and reply in one line. Never read their files into the orchestrator's context.
- **Saved skills.** A saved copy of `SKILL.md` lacks the scripts, so it must clone this repo first. The repo's copy always wins.
