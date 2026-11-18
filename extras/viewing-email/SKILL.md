---
name: viewing-email
description: Email an estate agent to book a viewing of one or more houses, and send it straight away from Bill's Superhuman Mail. Use when Bill says "email to organise a viewing", "book a viewing", "ask the agent for a viewing", "register my interest" or the like, for any house he names or points at (shortlist number, street, link). It finds the agent's correct email address if it isn't already known.
---

# Viewing email

When Bill asks for a viewing, send the email yourself. Don't send him a draft to approve. Afterwards, show him what was sent.

## 1. Pin down each house

For each house he names, find:
- the street, the area, the postcode district, the asking price and how it's quoted (for example "offers around £280,000" or "guide £250,000"), and the agent and branch;
- the listing link.

Look first in the house-hunt registry or shortlist (repo `McGoughBill/house-hunt`, `profiles/<P>/state/`), then in the project docs, then on the listing page.

- **Check that the house is still for sale.** Open the listing. If it says Sold, Sold STC, SSTC, Under offer or Not found, don't email: tell Bill instead.
- **Don't trust a failed fetch.** If the fetch fails or is refused, that doesn't prove the house is gone: go ahead.
- **If two houses match** (say two on Hollythorpe Road), pick the one he has been discussing. If it's still unclear, ask him one short question.

## 2. Find the agent's email address

Group the houses by agent and branch, and send one email per agent.

1. **Known addresses** (use these first):

| Agent | Email | Phone |
|---|---|---|
| Whitehornes (sales, all branches) | enquiries@whitehornes.com (the .co.uk address on their site rejects mail as an unknown user) | 0114 268 8533 |
| Staves (all branches; Woodseats handles S8) | info@stavesea.co.uk | Woodseats 0114 274 6400 |
| Haybrook Gleadless | Gleadless@haybrook.com | 0114 264 6302 |
| Saxton Mee Banner Cross (S7, S8, S11) | BannerCross@saxtonmee.co.uk | 0114 268 3241 |
| Reeds Rains Woodseats | woodseats@reedsrains.co.uk | 0114 258 8522 |
| Hunters, Hunters Bar (S7, S11) | sheffield@hunters.com | 0114 267 2080 |
| ELR (Eadon Lockwood & Riddle), Banner Cross | bannercross@elr.co.uk | 0114 268 3388 |

2. **Earlier emails.** Search his mail (`query_email_and_calendar`) for earlier emails with the agent. If a thread exists, reply on that thread (`type: reply`) and set `to` to the agent only, never to Bill.
3. **Otherwise, find a new address.** Fetch the listing page and ask for every email address and phone number on it, and which branch lists the house. Then try the agent's contact page. Then search the web for "<agent> <branch> Sheffield email".
   - Prefer the branch's own address, then the agent's general address.
   - Never use a portal's contact form or address (Rightmove, Zoopla, OnTheMarket and the like).
   - If you can't find an address, tell Bill and give him the branch's phone number.
4. **Add any new address you found** to the table above, and redeliver this skill to Bill.

## 3. Write the email

**Style** (Bill's standing rule for all outside emails):
- Keep it as short as possible, but in full sentences.
- Be minimally but noticeably polite: one "please" and a "thanks" is enough.
- Use plain English. Leave out filler, sales talk and hedging.

**Template:**

> **Subject:** Viewing: <Street> (or "Viewings: <Street> and <Street>")
>
> Hello,
>
> I'd like to view <Street, Area (price as quoted)> [and <Street, Area (price)>]. [One sentence on why you're writing, if needed, for example "Your website's booking buttons don't work, so I'm writing instead." or "I sent a web enquiry on <date> but haven't heard back."]
>
> Please send me times[, ideally on the same day]. Please also tell me whether [it / either] has an offer on it, and send the floorplan[s].
>
> I'm a first-time buyer with no chain, an agreement in principle and my deposit ready.
>
> Thanks,
> William McGough
> 07842 299504

**Rules:**
- **Never give a figure** for the mortgage, the deposit, the budget or the most he could pay. The broker's certificate shows far more than he means to offer. Just say "agreement in principle" and "deposit ready".
- **Send no offers, opinions or price talk** in a viewing email. Make offers separately, by email, only when Bill says so.
- **If Bill calls a house overpriced,** never name a figure. Add one line: "Please also tell me how long it has been on the market, whether it has any offers, and whether the seller would consider offers below the guide."
- **Adding a house later:** if he adds a house for an agent already emailed, reply on that thread: "I'd also like to view <house>, ideally on the same day as the other(s). Please send its floorplan too."
- **Keep the mortgage line accurate.** Update it if his status changes, for example to a named lender's agreement in principle or a full mortgage offer.

## 4. Send and report

1. **Make the draft.** Call `mcp__Superhuman_Mail__create_or_update_draft` with `type: new`, or `reply` for an existing thread, and with an explicit `body` in HTML. Don't use `instructions`, because the AI writer pads the text.
2. **Check the recipients.** The `to` list must hold only the agent's address. If Bill's own address appears, update the draft to remove it.
3. **Send it.** Call `mcp__Superhuman_Mail__send_draft`, which holds the email for 1 minute so it can be undone.
4. **Space the sends out.** Leave at least 30 seconds between emails. When several went out in the same second, Outlook blocked some of them with "550 5.7.501 Spam abuse detected from IP range".
5. **Check for a bounce.** About two minutes after sending, list the Junk Email label (Outlook files bounce notices there) and look for "Undeliverable". Read the diagnostic line:
   - **5.1.x, "unknown user":** the address is wrong. Find another one and resend.
   - **5.7.501, "spam abuse":** the recipient's server is refusing mail from Outlook's sending servers. Resend once, a few minutes later. If it bounces again, stop and give Bill the branch's phone number. ELR rejected two attempts on 18 Nov.
   When replying on a thread that holds a bounce notice, pass the `message_id` of Bill's own last message, so the reply doesn't go to postmaster.
6. **Tell Bill**, in one or two lines: who it went to, which houses it covers, and the email text quoted. Also give the branch phone number as a fallback, and anything you skipped and why (sold, no address found).

If Superhuman Mail isn't connected, write the email and give it to Bill to paste, with the address.
