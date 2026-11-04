# house-hunt

A Claude skill that hunts for houses to buy, and the repo that holds it. The skill is `SKILL.md`. Every file it uses sits beside it, and so does each buyer's saved search.

**What it does.** For each buyer it:
1. sends one Haiku agent to each listing source to find houses that fit the brief and are new since the last run;
2. has one Haiku judge score each new house;
3. gives the top 40 three judges each;
4. keeps the 20 best that pass the brief's hard rules as a shortlist.

A weekly run sends a phone notification only when a new house enters the shortlist.

## Install

- **claude.ai or Claude cloud sessions:** save `SKILL.md` as a skill. On first use it clones this repo and follows the repo's copy. It needs the Claude GitHub App on this repo.
- **Claude Code on your own machine:** clone the repo straight into your skills folder: `git clone <this repo> ~/.claude/skills/house-hunt`.

Then ask: "Use the house-hunt skill: weekly run".

## Check it

From the repo root, run `python3 scripts/hh.py doctor`. It checks:
- every path and command the docs name exists;
- `SKILL.md` and `house-hunt.json` agree on name, version and home repo;
- the agents are installed;
- the repo is in step with GitHub;
- each profile's weights total 100 and its brief is up to date.

The full layout is in the map in `SKILL.md`. How scoring works, and what the first run taught, is in `references/protocol.md`.

## Use it for another buyer or city

Copy the repo into a private repo of your own. Then:
1. Run `python3 scripts/hh.py config remote=owner/repo`.
2. Edit the `Home repo:` line in `SKILL.md` to match.
3. Ask Claude to set up a house hunt for your city.

It deduces what kind of place you want from your brief and asks at most three questions. The details are in `references/new-profile.md`.
