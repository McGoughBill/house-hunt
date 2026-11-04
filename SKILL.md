---
name: house-hunt
description: Run a house-buying search pipeline for any city. Haiku agents search every listing source, new finds go on a longlist, one Haiku judge scores each house against the buyer's brief, and the top 20 form a shortlist. Weekly runs pick up new listings only and send a push notification when the shortlist gains a house. Use it to set up a house hunt, run or schedule one, or ask how it stands.
---

# House hunt

You orchestrate; Haiku agents do the web work. Everything deterministic runs through one helper, `hh.py`, in the user's private `house-hunt` repo. Keep your own context small. Never read registry, result or prompt files into context. Use the one-line summaries that `hh.py` prints and the one-line replies the agents return.

Run the orchestrator on Opus at high effort, where the session lets you choose. The agents run on Haiku at extra-high effort, set in `agents/*.md`.

## 0. Session setup (every run)

1. **Find the repo.** Read the project doc `claude/house-hunt-config.md` for `repo`, `profile` and `schedule`. If it isn't there, ask the user once for `owner/repo`.
2. **Attach and clone it.** Call `add_repo(owner, repo, access="push")`, then clone to `/home/claude/house-hunt`, or `git pull` if it is already there. Run `cd /home/claude/house-hunt && python3 hh.py install`.
3. **Agent types.** Agents use `subagent_type` `house-search` or `house-judge`. If the Agent tool says the type is unknown, which happens early in a session, use `general-purpose` with `model: "haiku"` and the same one-line prompt.
4. **Date.** Set `D` to today as YYYY-MM-DD and `P` to the profile name.

## 1. Choose the mode
- The profile exists and the user wants a run, or a scheduled task fired: go to **3. Weekly run**.
- There is no profile, or the user names a new city or buyer: go to **2. New profile**, then run 3.
- They ask how it stands: run `python3 hh.py status P D`, and read `profiles/P/state/shortlist.md` only if they ask for the list.

## 2. New profile: deduce first, ask little

**Deduce.** Read the buyer's brief: the project description, their first message, any attached brief, and memory. From it, infer:
- city, country and currency;
- price ceiling, all-in ceiling, bedrooms and minimum size;
- strategy: `improve` (buy cheap, refurbish or extend) or `ready` (move straight in);
- hard rules: these become gates, such as "no front door into the living room";
- anchors: work, a partner's work, family, friends, a station;
- the **vibe**, from the list below.

| Vibe | Cues in a brief | What the search favours |
|---|---|---|
| Young urban | 20s–30s, no kids, "lively", bars, gigs, cycling | indie high streets, walk to centre, period terraces or flats near nightlife |
| Young professional, homely | couple, "homely", a park, coffee, working from home | period houses on owner-occupied streets near a big park and an indie high street |
| Family | kids or planning them, schools, garden | good primary schools, quiet streets, gardens, 3–4-bed semis |
| Affluent, established | high budget, "prestige", privacy | leafy detached or semi-detached houses, top schools, large plots |
| Green or rural | dogs, walking, space, remote work | village edge, countryside access, train to the city |
| Value or project | ROI, "cheap against fundamentals", refurb | rising areas, doer-uppers, room to extend; combines with any vibe above |

Most buyers mix two vibes, for example "young professional, homely" plus "value or project". Write a one-sentence vibe summary. Name 1–3 model areas where the buyer is happy, or areas the brief praises.

**Ask.** Use one `AskUserQuestion` call with at most three questions. Each question opens with your deduced answer, labelled "(Recommended)". Skip any question the brief already answers. In order of priority:
1. The vibe summary and the model areas.
2. Anchors: what must be near, and how near.
3. Missing numbers, in one question: budget, bedrooms, works budget and strategy.

**Build the profile.**
```bash
python3 hh.py new P                     # starts from the Sheffield profile: criteria, gates, run settings
python3 hh.py set P city=… country=… currency=… intent="…" 'vibe={"summary":"…","model_areas":[…],"likes":[…],"avoid":[…]}' \
  'anchors=[{"name":"…","note":"…","weight":0}]' search.price_min=… search.price_max=… search.allin_max=… search.beds_min=… \
  search.size_min_m2=… finished_spec="…" buy_test.fees=… buy_test.tax_note="…" 'buy_test.tax_bands=[[upto,rate],…]'
python3 hh.py preset P improve          # or ready
```
- **Gates.** Rewrite `gates` for the country and for the buyer's hard rules with `set 'gates=[…]'`. Keep the keys `area` and `budget`. For example, the leasehold rule is UK-only.
- **Places.** Seed `areas` with the model areas as `[{"district":"…","neighbourhoods":["…"],"only_these":true}]`.

**Scout.** Generalise the vibe across the target area.
```bash
python3 hh.py scout P D          # writes prompts/scout/areas.md and sources.md
```
- Launch both prompts with the launch loop (section 4).
- Then run `python3 hh.py scout-apply P D --fit 4`, which prints the kept areas.
- Show the kept areas in one `AskUserQuestion`. Offer "All of them (Recommended)", "Only the best fits", and a free-text option to add or drop areas.
- Apply any changes with `hh.py set P 'areas=[…]'`.

**Save the config.**
- Write `claude/house-hunt-config.md` to the project. It holds `repo`, `profile` and `schedule`, plus one line on the vibe.
- Commit and push (section 3, step 8).

## 3. Weekly run

The registry remembers every house ever seen, so searches report new houses only, and price changes on known ones.

1. `git pull`, then `python3 hh.py search P D`. Launch all search prompts (section 4).
2. Run `python3 hh.py ingest P D`. This merges the results and writes `state/history/longlist-D.md`, listing only the new houses.
3. Run `python3 hh.py judge P D` and `python3 hh.py reprice P D`. Reprice writes a prompt only when a price change would move a house's total or gate status. Launch them all.
4. Run `python3 hh.py collect P D`. If it says "requeued N", launch those, then collect again. Blank runs are retried once only.
5. Run `python3 hh.py topup P D`. This adds runs until every house in the top 40 has 3 scored runs. Launch them, then collect again.
6. Run `python3 hh.py shortlist P D`. If it exits 10, a new house has entered the top 20:
   - Load the PushNotification tool with ToolSearch.
   - Send one message under 200 characters, built from the printed `NEW` lines. For example: "House hunt: 2 new in top 20. #3 Rushdale Rd, Meersbrook £265k (66). See shortlist." In a scheduled run, wrap it in `<routine_summary>` tags.
   - Send nothing when no house is new.
7. If a project is attached, upload `state/shortlist.md` only if it changed, and `state/history/longlist-D.md` only if it lists new houses. Put both under `claude/house-hunt/`.
8. Commit and push the state: `git add -A profiles && git commit -qm "house-hunt P D" && git push -q`. If the push fails, say so in one line; the state is still on disk.
9. Reply in 2–4 lines: new houses found, houses judged, any change to the shortlist, and anything blocked.

## 4. Launch loop
- Run `python3 hh.py next P D K`, where K is `run.concurrency` (10) minus the number of agents in flight. Each output line is `agent<TAB>path`.
- For each line, call `Agent` with:
  - `subagent_type` set to the agent from that line;
  - `run_in_background: true`;
  - a 3–5-word description;
  - the prompt exactly as follows: `Read <path> and do exactly what it says.`
- On each completion, launch `next P D 1`. Don't read or quote the agent's JSON; it replies in one line.
- The phase is done when `next` prints `# 0 left` and nothing is in flight. Before moving on, run `python3 hh.py orphans P D`. If it lists anything, run `orphans P D --reset` and launch again.
- **Rate limits.** If replies mention HTTP 429 or a rate limit, stop launching. Schedule a resume with `send_later` in 10 minutes, then send one probe agent before you refill.
- **Interruptions.** An interruption of the main session kills the agents in flight without notice. `orphans --reset` recovers them.
- Don't send progress reports unless the user asks.

## 5. Schedule
- To make the run weekly, create one scheduled task with `create_trigger`. Pick a jittered evening time in the user's time zone, outside 06:00–09:00 Pacific. Use this prompt: "Use the house-hunt skill: weekly run for profile P. Repo owner/repo."
- Record the schedule in `claude/house-hunt-config.md`.
- Tell the user, in one sentence, which approval setting the task got.

## 6. Scoring, briefly
- `hh.py brief P` renders `profiles/P/brief.md` from the profile, and the judges read it.
- The ranker computes criterion 2 (margin), criterion 18 (uplift, V ÷ asking) and the budget gate from each judge's own V, W and C at the current asking price. A price cut therefore re-scores a house for free.
- Total = Σ(weight × median score) ÷ 5. Weights sum to 100. A gate fails on a majority of runs. A house is GONE when its latest run finds it sold.
- To change weights, use `preset` or `set criteria.<i>.w=…`. Weights must still total 100.
