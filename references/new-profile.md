# New profile: a new buyer, city or country

Read this only when there is no profile for the buyer, or when they name a new place. Its aim is to get the **vibe** right. Price and size are easy to set. The vibe is what makes a shortlist worth reading.

## 1. Deduce

Read what the buyer has already given: their first message, any brief they attached, the claude.ai project description and memory. From it, infer:

- city, country and currency;
- price ceiling and all-in ceiling (price + works + buying costs), bedrooms and minimum floor area;
- strategy: `improve` (buy cheap, refurbish or extend) or `ready` (move straight in);
- hard rules, which become gates, for example "no front door into the living room";
- anchors: work, a partner's work, family, friends, a station, with how much each matters;
- the **vibe**, from the table below.

| Vibe | Cues in a brief | What the search favours |
|---|---|---|
| Young urban | 20s–30s, no children, "lively", bars, gigs, cycling | independent high streets, walk to the centre, period terraces or flats near nightlife |
| Young professional, homely | a couple, "homely", a park, coffee, working from home | period houses on owner-occupied streets near a big park and an independent high street |
| Family | children or plans for them, schools, garden | good primary schools, quiet streets, gardens, 3–4-bed semis |
| Affluent, established | high budget, "prestige", privacy | leafy detached or semi-detached houses, top schools, large plots |
| Green or rural | dogs, walking, space, remote work | village edge, countryside access, a train to the city |
| Value or project | ROI, "cheap against fundamentals", refurb | rising areas, doer-uppers, room to extend; combines with any vibe above |

Most buyers mix two vibes, for example "young professional, homely" plus "value or project". Write a one-sentence vibe summary, then:

- **Model areas:** 1–3 places where the buyer already feels at home, or that the brief praises.
- **Likes:** concrete things the scout and judges can check, such as "big park within 10 minutes' walk".
- **Avoids:** the same kind of concrete things.

## 2. Ask, as little as possible

Use one `AskUserQuestion` call with at most three questions. Make your deduced answer the first option of each question, labelled "(Recommended)". Skip any question the brief already answers.

Ask in this order of priority:
1. The vibe summary and the model areas.
2. Anchors: what must be near, and how near.
3. Missing numbers, all in one question: budget, bedrooms, works budget and strategy.

If no one is there to answer (a scheduled run), use your deductions and say so in the reply.

## 3. Build the profile

From the repo root:

```bash
python3 scripts/hh.py new P            # copies templates/profile.json: 18 criteria, generic gates, run settings
python3 scripts/hh.py set P owner=… city=… country=… currency=… intent="…" \
  'vibe={"summary":"…","model_areas":[…],"likes":[…],"avoid":[…]}' \
  'anchors=[{"name":"…","note":"…","weight":0}]' \
  search.price_min=… search.price_max=… search.allin_max=… search.beds_min=… search.size_min_m2=… \
  finished_spec="…" buy_test.fees=… buy_test.tax_note="…" 'buy_test.tax_bands=[[upto,rate],…]'
python3 scripts/hh.py preset P improve # or ready
```

- **Gates.** Rewrite them for the country and add the buyer's hard rules: `set P 'gates=[…]'`. Keep the keys `area` and `budget`, because the ranker uses them. The tenure rule depends on the country.
- **Seed areas.** Start the `areas` list with the model areas: `set P 'areas=[{"district":"…","neighbourhoods":["…"],"only_these":true}]'`.
- **Copying a profile.** To copy another buyer's profile instead of the template, use `new P --like Q`. It clears the place-specific fields.

## 4. Scout: spread the vibe across the area

```bash
python3 scripts/hh.py scout P D        # writes two prompts: look-alike areas, and listing sources
```

1. Launch both prompts with the launch loop in `SKILL.md`.
2. Run `python3 scripts/hh.py scout-apply P D --fit 4`. It keeps areas that fit the vibe at 4 or better, out of 5, within budget, and prints them.
3. Show the kept areas in one `AskUserQuestion`. Offer three options: "All of them (Recommended)", "Only the best fits", and free text to add or drop areas.
4. Apply any changes with `set P 'areas=[…]'`.
5. Run `python3 scripts/hh.py brief P`.

## 5. Register and save

1. Register the profile in the repo config: `python3 scripts/hh.py config 'profiles.P={"owner":"…","schedule":null,"notify":"push when a new house enters the shortlist"}'`. If this is the only profile, also run `config default_profile=P`.
2. Run `python3 scripts/hh.py doctor`, then `python3 scripts/hh.py save P D`.
3. Go on to the weekly run in `SKILL.md`. The first run finds everything, so expect 60–120 houses and a few hours of judging.

**A new user with no repo of their own.** This repo is private to its owner. A new user needs their own copy:
1. Copy this repo into a private repo they own.
2. Point the config at it: `config remote=owner/repo`.
3. Change the `Home repo:` line in `SKILL.md` to match.
4. Run `doctor`; it checks that the two agree.
