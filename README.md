# house-hunt

A house-buying search pipeline for any city. It is orchestrated by Claude (Opus) and does its web work through Haiku agents. The skill is in `SKILL.md`, and every deterministic step goes through `hh.py`.

## Protocol

| Stage | Who | What | Output |
|---|---|---|---|
| 0. Profile | Opus + user | Deduce city, budget, beds, strategy, hard rules, anchors and **vibe** from the brief, then ask at most 3 questions | `profiles/P/profile.json` |
| 1. Scout (new profiles only) | 2 Haiku agents | Map the vibe onto look-alike neighbourhoods in the target area; list portals, local agents, auctions and sold-price sources | areas and sources merged into the profile |
| 2. Search | 1 Haiku agent per source (19 for Sheffield) | Find houses that fit the brief and **are not already known** (`known.txt`); report price changes on known ones | `work/P/D/results/search/*.json` |
| 3. Longlist | `hh.py ingest` | Normalise, de-duplicate against the registry, filter to the brief | `state/history/longlist-D.md` (new houses only), `state/longlist.md` (all) |
| 4. Judge | 1 Haiku agent per new house, plus 1 per house whose price change moves its score | Gates, V, W, C, criteria 1–17, risk | compact runs in `state/registry.json`; raw files in `state/raw/D/` |
| 5. Top-up | Haiku | 2 more runs for any house ranked in the top 40, so it has 3 scored runs | medians |
| 6. Shortlist | `hh.py shortlist` | Top 20 that pass. A push notification goes out only when a new house enters | `state/shortlist.md`, `state/history/shortlist-D.md` |
| 7. Save | git | Commit and push the state | this repo |

Weekly runs repeat stages 2–7. Because the registry remembers every house, each longlist is incremental.

## Scoring

- **Rendering.** `profile.json` holds the gates, 18 weighted criteria (weights total 100) and the buy test. `hh.py brief` renders them into `brief.md`, which the judges read.
- **Computed criteria.** The ranker computes criterion 2 (margin = 0.9V − 1.15W − C − asking), criterion 18 (uplift = V ÷ asking) and the budget gate from each run's own V, W and C at the current asking price.
- **Totals and gates.** Total = Σ(weight × median score) ÷ 5. A gate fails when it fails on a majority of runs.
- **Weight presets.** `improve` suits buying cheap and refurbishing; `ready` suits a house to move straight into.

## Layout

```
SKILL.md                 skill instructions (also saved as the user's house-hunt skill)
hh.py                    all helper commands: python3 hh.py -h
agents/                  house-search, house-judge (Haiku, effort xhigh)
templates/               search, judge, scout prompts; weight presets
profiles/<name>/         profile.json, brief.md, state/ (registry, ranking, shortlist, history, raw)
tools/                   one-off importers
work/                    per-run prompts and results (git-ignored)
```

## Lessons from the first run (3 Nov 2026, Sheffield)

- **Concurrency.** About 20 agents at once tripped the WebSearch rate limit for 15 minutes. Run 10 at a time.
- **Blocked portals.** WebFetch often refuses Rightmove and Haybrook. Agents find the same house on Zoopla, OnTheMarket, PrimeLocation, agent sites or Rightmove brochure PDFs.
- **Sold prices.** The records don't say whether a sale was done up, so V runs low and most margins come out negative. Use totals to compare houses, not to price them.
- **Already-done houses.** Without criterion 18, these outscored run-down houses with good bones.
- **Interruptions.** Interrupting the main session silently kills the agents in flight. `hh.py orphans --reset` recovers them.
- **Short replies.** Judges and searchers write their output to files and reply in one line. This keeps the orchestrator's context small.
