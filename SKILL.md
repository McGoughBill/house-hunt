---
name: house-hunt
description: Run a house-buying search pipeline for any city. Haiku agents search every listing source, new finds go on a longlist, one Haiku judge scores each house against the buyer's brief, and the top 20 form a shortlist. Weekly runs pick up new listings only and send a push notification when the shortlist gains a house. The skill is its own git repo. Use it to set up a house hunt for a buyer or city, run or schedule one, ask how it stands, or change the brief.
---

# House hunt

Skill version: `2026-11-04.1` · Home repo: `McGoughBill/house-hunt` (private)

This repo is the skill. `SKILL.md` sits at its root beside everything it uses: the scripts, prompt templates, agent definitions, the buyers' profiles and their saved state. Nothing lives outside it except installed copies of the agents. A saved copy of this file is only a way back here.

You orchestrate, on Opus at high effort where the session lets you choose. Haiku agents at extra-high effort do the web work; their settings are in `agents/`. Every step that needs no judgement runs through `scripts/hh.py`. Keep your context small:
- Never read registry, result or prompt files.
- Work from the one-line summaries `hh.py` prints and the one-line replies agents send.

## 0. Find the repo (every session)

1. **Find the root.**
   - If `scripts/hh.py` sits beside this file, this file's folder is the root.
   - If not, you are reading a saved copy:
     - Call `add_repo` with the home repo above and `access: "push"`.
     - Clone it into `house-hunt/` in the working directory, or `git pull` if that folder exists.
     - Read `house-hunt/SKILL.md` and follow that instead of this copy.
     - If the two copies differ, finish the task, then offer once to update the saved skill to the repo's text.
2. **Set up.** From the root, run `python3 scripts/hh.py setup`. It installs the agents, pulls, and runs `doctor`.
   - FAILs in paths or commands mean a broken skill: fix them before a run.
   - "behind" means `sync` failed: say so and stop.
3. **Choose the profile and date.** P is the profile the user names, otherwise `default_profile` in `house-hunt.json`. D is today, as YYYY-MM-DD.
4. **Agent types.** The two agent types are `house-search` and `house-judge`. If the Agent tool rejects them, which happens early in a session, use the `fallback` in `house-hunt.json` (general-purpose on Haiku) with the same one-line prompt.

## Map

| Path | What it holds |
|---|---|
| `house-hunt.json` | home repo, version, default profile, each profile's schedule, agent fallback |
| `scripts/hh.py` | every mechanical step; `python3 scripts/hh.py -h` lists the commands |
| `agents/` | the two Haiku agent definitions, installed by `setup` |
| `templates/` | search, judge and scout prompts; `templates/profile.json` for new profiles; `templates/presets.json` for weights |
| `references/new-profile.md` | setting up a new buyer, city or country: deduce the vibe, ask at most 3 questions, scout |
| `references/protocol.md` | stages, scoring rules, lessons; for changing the skill or explaining a score |
| `profiles/<P>/` | `profile.json`, `brief.md` (rendered for judges), and `state/` (registry, ranking, longlists, shortlists, raw results) |
| `work/` | scratch for each run; not committed |

## 1. Choose the mode

- **Weekly run**, or a scheduled task fired: go to section 2.
- **New buyer, new city, or no profile:** follow `references/new-profile.md`, then section 2.
- **"How's it going":** run `python3 scripts/hh.py status P D`. Read `profiles/P/state/shortlist.md` only if they ask for the list.
- **Change the brief or weights:**
  1. Run `hh.py set` or `hh.py preset`.
  2. Run `python3 scripts/hh.py brief P`, then `python3 scripts/hh.py shortlist P D` (it ranks first).
  3. Run `python3 scripts/hh.py save P D`.
- **Change the skill itself:**
  1. Edit the files here.
  2. Bump the version in both `SKILL.md` and `house-hunt.json`.
  3. Run `python3 scripts/hh.py doctor`, then `python3 scripts/hh.py save --skill -m "what changed"`.

## 2. Weekly run

The registry remembers every house ever seen. Searches therefore report only new houses, plus price changes on known ones.

1. **Search.** Run `python3 scripts/hh.py search P D`, then launch every prompt (section 3).
2. **Longlist.** Run `python3 scripts/hh.py ingest P D`. This writes the longlist of new houses.
3. **Judge.** Run `python3 scripts/hh.py judge P D` and `python3 scripts/hh.py reprice P D`, then launch every prompt. Reprice writes a prompt only when a price change would move a total or a gate.
4. **Collect.** Run `python3 scripts/hh.py collect P D`. If it prints "requeued N", launch those and collect again. A blank run gets one retry.
5. **Top up.** Run `python3 scripts/hh.py topup P D`. This gives each of the top 40 three scored runs. Launch the prompts, then collect again.
6. **Shortlist.** Run `python3 scripts/hh.py shortlist P D`. Exit code 10 means a new house entered the top 20:
   - Load PushNotification with ToolSearch.
   - Send one message under 200 characters, built from the printed `NEW` lines, for example "House hunt: 2 new in top 20. #3 Rushdale Rd, Meersbrook £265k (66)."
   - In a scheduled run, wrap the message in `<routine_summary>` tags.
   - If no house is new, send nothing.
7. **Optional project copy.** If a claude.ai project is attached, upload `profiles/P/state/shortlist.md` when it changed, and the day's longlist when it lists new houses. Both go under the `mirror.prefix` in `house-hunt.json`. The repo stays the record.
8. **Save.** Run `python3 scripts/hh.py save P D`. Pass any commit trailers the session asks for as extra `-m` lines.
9. **Reply** in 2–4 lines: new houses found, houses judged, any change to the shortlist, anything blocked.

## 3. Launch loop

1. Run `python3 scripts/hh.py next P D K`, where K is 10 minus the number of agents running. Each line it prints is `agent<TAB>path`.
2. For each line, call `Agent` with:
   - that agent type;
   - `run_in_background: true`;
   - a 3–5-word description;
   - exactly this prompt: `Read <path> and do exactly what it says.`
3. Each time an agent finishes, run `next P D 1` and launch what it prints. Don't read or quote the agent's JSON.
4. A phase is done when `next` prints `# 0 left` and no agents are running. Then run `python3 scripts/hh.py orphans P D`. If it lists anything, run `orphans P D --reset` and launch again.

Problems:
- **Rate limits.** If replies mention 429 or a rate limit, stop launching. Use `send_later` to resume in 10 minutes, then launch one probe before refilling.
- **Interruptions.** An interrupted main session kills the agents that are running, without warning. `orphans --reset` recovers them.

Send no progress reports unless asked.

## 4. Schedule

- **Create.** Make one weekly scheduled task with `create_trigger`:
  - a jittered evening time in the user's time zone;
  - the prompt "Use the house-hunt skill: weekly run for profile P."
- **Record.** Save it in the repo with `python3 scripts/hh.py config 'profiles.P.schedule="weekly, <day> <time> <tz>, task <name>"'`, then `save --skill`.
- **Tell the user**, in one sentence, which approval setting the task got.
