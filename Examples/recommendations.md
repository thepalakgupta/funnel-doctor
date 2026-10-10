# Recommendations: what to test, what to investigate first (October 2019, 10% user sample)

*Stage 3. Builds on `output/funnel_summary.md` (stage 1) and `output/diagnosis.md` (stage 2) and keeps their definitions unchanged.*
*Scripts: `work/r1_test_baselines.py` (baselines, sample sizes, durations) and `work/r2_achieved_mde.py` (what each run length can detect, impact sizing). Numbers: `work/r1_test_plan.json`, `work/r2_achieved.json`.*

---

## Headline

> **Run two tests now and one after a quick check:**
> 1. A **free-shipping threshold progress bar in the cart**. This is the biggest lever: about **+1,400 buyers a month** if it hits its minimum detectable effect. It takes 3 weeks.
> 2. **Recommendations on product pages** to fix the weakest step (view → cart). It is cheap, the traffic is large, and it reads out in 3 weeks.
> 3. **Abandoned-cart reminders.** These are worth roughly 800 buyers a month at full reach, but whether and how fast the test works depends on how many carters you can actually email. Answer that question first.
>
> **Before any test starts, filter out the "ghost cart" traffic.** On Oct 2, 6 and 7 it made up 76–86% of first-time carters. Across October it made up 35% of all carters, so if it gets into an experiment it dilutes the cart tests by up to a third and can mask any real effect.

---

## Shared rules for every test

| Item | Rule |
|---|---|
| **Clean traffic** | All users **except** the stage-2 "ghost" pattern: first seen on a burst day, and the whole history is 1 view plus 1–3 cart events of one product. In a live test, decide the exclusion rule **before** launch and apply it equally to both arms. For example, exclude users whose bucketed session is 1 view + only cart events of that product within 10 s, or exclude a blocked source once one is identified. |
| **Bought (7d)** | First purchase within 168 h of the user's **first cart** (same as stage 2's "bought within 7 days"). Baselines use carters whose first cart was on or before Oct 24, so every user has a full window. |
| **Carted (7d)** | *(New, for test C only. It is the view-stage version of the same rule.)* The user viewed something **and** carted within 168 h of their **first event**, which is when they would be bucketed. Baseline uses clean viewers first seen on or before Oct 24. |
| **Unit / split** | Randomize by user, 50/50, and keep each user in the same arm for the whole test. |
| **Stats** | Two-sided two-proportion z-test, α = 0.05, power = 0.80. Sample sizes are computed in Python; the formula is checked against a textbook value. |
| **Production scale** | The sample is every `user_id` ending in 0, which is about 10% of users. All traffic figures are **×10**. Daily volumes use the **median non-burst day** in clean traffic, which is a conservative figure: 224 new clean carters/day → **2,240 in production**; 1,062 new clean viewers/day → **10,625**. |
| **Duration** | Time to enrol both arms, rounded **up to full weeks** with a **14-day minimum** (to cover weekly cycles), **plus 7 days** for the last users' 7-day purchase window. |
| **Health checks** | A sample-ratio check (the arms should split 50/50) every day. Don't stop early when results look significant; read the result only at the planned date. |

---

## The tests

### Test A: free-shipping threshold progress bar in the cart  *(from diagnosis finding 2)*

| | |
|---|---|
| **Hypothesis** | Small baskets rarely check out because shipping makes a small order uneconomic. Buy rate is 15% for carts of $20 or less vs 39% above $20, and 6% for carts of $10 or less. Showing "Add $X more for free shipping" with a progress bar will lead some of these shoppers to add items and check out. |
| **Change** | Control: the current cart. Treatment: a persistent bar in the cart and mini-cart that shows the distance to free shipping, plus 3 low-price add-on suggestions. **The threshold has to be decided first** (see Investigate #2). As a starting point, about $30 sits just above the median order ($27.32 in this window; 36.6% of orders are $20 or less). |
| **Who is in the test** | Clean users at their first add-to-cart. |
| **Primary metric** | **Bought (7d)** among assigned carters. |
| **Guardrail metric** | **Net revenue per carter after the shipping subsidy** (7-day). The current gross baseline is **$10.88 per carter**; the shipping cost per order has to come from finance. Secondary guardrail: Bought (7d) among carts above $20 (baseline 38.9%). This should not fall. |
| **Baseline** | **25.87%** (1,769 of 6,839 clean carters). For the ≤$20 segment (cart value in the first 24 h), the pre-planned secondary metric: **15.07%** (n = 3,742; 55% of carters). |
| **MDE** | **+8% relative = +2.07 pp (25.87% → 27.94%).** This is a conservative two-thirds of stage 2's sizing: lifting the ≤$20 group from 13% to 20% would be about +12%. |
| **Sample size** | **7,208 per variant** (14,416 total). |
| **Duration** | 6.4 days of production traffic to enrol, rounded up to the **14-day minimum, so results come in 21 days after launch**. Running the full 14 days gives 15,680 per arm, so the test can actually detect **+1.40 pp (+5.4%)**, and **+10.4%** in the ≤$20 segment. |
| **Impact if it hits the MDE** | About **+1,390 buyers/month** in production. That is +8% on roughly 17,400 buyers/month, measured on a typical-day basis. |
| **Effort** | Medium: a cart UI change plus a decision on shipping policy and margin. |

### Test B: abandoned-cart reminders (email or push at 1 h and 24 h)  *(from diagnosis finding 3)*

| | |
|---|---|
| **Hypothesis** | Carters who leave without buying rarely come back: one-day carters buy at 20% vs 41% for those active on more days. Yet 29% of buyers buy more than 24 h after their first cart, so bringing people back works. A reminder will bring some of the rest back. |
| **Change** | Control: no reminder. Treatment: a reminder 1 h after the cart is abandoned and another at 24 h, showing the cart contents and, if test A has shipped, the free-shipping gap. **No discount** in the first version, so the test measures the reminder itself and doesn't give away margin. |
| **Who is in the test** | Clean carters who **can be contacted** (logged in or with an email or push token) and **haven't bought within 1 h** of their first cart. This is 86.6% of clean carters, before taking contactability into account. Randomize only among contactable carters, so that the result isn't diluted by people who can't receive the message. |
| **Primary metric** | **Bought (7d)**. |
| **Guardrail metric** | **Unsubscribe and spam-complaint rate** on the reminder (it should stay under about 0.5% of sends; the data has no baseline). Secondary guardrail: 7-day revenue per carter. |
| **Baseline** | **14.36%** (n = 5,920). Of these, 8.2% buy between 1 and 24 h and 6.2% between 24 h and 7 d. **Caveat:** contactable carters probably convert better than this, so recompute the baseline on the contactable group before launch. |
| **MDE** | **+10% relative = +1.44 pp (14.36% → 15.79%).** That is about 1 extra buyer per 70 reminded carters, a low bar for abandoned-cart reminders. |
| **Sample size** | **9,748 per variant** (19,496 total). |
| **Duration** | **Depends on contactability:** <br>• 100% contactable (1,939/day in production): 14 days enrolment, **results in 21 days** <br>• 50% contactable: 21 days, **results in 28 days** <br>• 30% contactable: 35 days, **results in 42 days** |
| **Impact if it hits the MDE** | About **+835 buyers/month × the share of carters who are contactable**. For example, roughly 420 at 50%. |
| **Effort** | Low if an email service and email capture already exist. **High** if email has to be captured before checkout first. |

### Test C: "You may also like" recommendations on product pages  *(from diagnosis finding 4)*

| | |
|---|---|
| **Hypothesis** | The weakest step is view → cart: in the clean funnel only 23.6% of viewers add to cart. 51% of viewers look at one product and leave, and their cart rate is about 10%, against 47% for those who view 5–9 products. Giving people an obvious second click will increase browsing depth and add-to-cart. |
| **Change** | Control: the current product page. Treatment: a row of 4–8 same-category recommendations, each with a quick-add button, placed above the fold on mobile. |
| **Who is in the test** | Clean users, at their first page load. |
| **Primary metric** | **Carted (7d)**. |
| **Guardrail metric** | **Bought within 7 days of first event** among viewers. Baseline **5.93%**. Extra carts must not come at the cost of purchases, and the quick-add button could produce low-intent carts. Also watch product-page load time. |
| **Baseline** | **23.49%** (n = 27,947 clean viewers first seen on or before Oct 24). |
| **MDE** | **+5% relative = +1.17 pp (23.49% → 24.67%).** |
| **Sample size** | **20,801 per variant** (41,602 total). |
| **Duration** | 4 days of production traffic (10,625 viewers/day), rounded up to the **14-day minimum, so results come in 21 days**. Over 14 days the test enrols about 74,000 per arm. At that size it can detect **+0.62 pp (+2.6%)** on cart rate, and a **5.7% relative drop** in the purchase guardrail. |
| **Impact if it hits the MDE** | About 3,700 extra carters a month. If they buy at between 15% (the small-basket rate) and 26% (the average), that is about **+560 to +970 buyers/month**. |
| **Effort** | Low to medium. Recommendation widgets are standard; "same category" works even though `category_code` is missing, because `category_id` is populated. |

**Running them together:** A (cart page) and C (product page) can run **at the same time** with independent randomization, because they change different pages. Don't run B alongside A unless B's reminders are identical in both A arms. Otherwise run B after A has been decided.

---

## Investigate first (not testable yet)

| # | Question to answer | Why it matters | Who / how |
|---|---|---|---|
| 1 | **Which referrer, UTM, IP/ASN or user agent produced the 4,347 users on Oct 2, 6 and 7 who viewed one product and fired 1–3 cart events of it within seconds? Was this traffic paid for?** | This traffic makes cart-abandonment look about 10 points worse than it is. If it is paid, it is wasted spend. If it is not filtered, it **contaminates tests A and B**. | Marketing calendar, ad invoices, and server/CDN logs for Oct 1–8. |
| 2 | **What are the current shipping fee and free-shipping threshold (if any), and what does an order cost to ship?** | Test A depends on this. If free shipping already applies to everything, finding 2 has another cause, such as minimum-order rules or payment fees. | Ops and finance. A one-day task. |
| 3 | **What share of carters are logged in or have an email or push token at the moment they add to cart?** | This sets whether test B is worth running and how long it takes: 21 days at 100% contactable, 42 days at 30%. | CRM and email platform. |
| 4 | **Does payment or checkout success differ by hour, especially 18–23 UTC (late evening local time)? Are payment providers, support chat, or delivery-slot availability different at night?** | Evening carters buy about 10 pp less often, even when basket size is held constant (finding 5). It might be a bug rather than a behaviour pattern. | Payment-provider logs: declines and errors by hour. |
| 5 | **On product pages above $12, what is missing compared with the $2–7 pages: photos, specs, reviews, delivery and returns information?** | The cart rate is 15% vs 28–30% at both browsing depths. A content audit tells you which change to test next. | A 1–2 day heuristic audit of the top 50 $12+ products by views. |
| 6 | **What are the items with no brand, and why do baskets made up only of them convert at 13% vs 33%?** | This is small (526 users in 2+ item baskets), but it may be an own-label or catalogue-data problem. | Merchandising. |
| 7 | **Can purchases carry an `order_id`, and can the double-firing of cart and remove events be fixed?** | Today a purchase row is a line item, and 5% of rows are duplicates. Both would distort any order-level or event-level test metric. | Engineering. Do this before measuring test A's average order value. |

---

## Ranking: expected impact vs effort

Impact = production buyers per month if the effect equals the MDE (on a typical-day basis, so a conservative figure), or the decision it unblocks.

| Rank | Item | Type | Expected impact | Effort | Why this rank |
|---:|---|---|---|---|---|
| 1 | Find and filter the ghost traffic (Investigate #1) | Investigate | **High** (protects every metric and test; may save spend) | Low | Cheap, and every test needs it. |
| 2 | Shipping fee and threshold facts (Investigate #2) | Investigate | Unblocks the biggest test | Very low | One question to ops. |
| 3 | **Test A: free-shipping progress bar** | A/B test | **About +1,390 buyers/mo (+8%)** | Medium | Largest effect, on the biggest segment of genuine non-buyers (58% have carts of $20 or less). |
| 4 | **Test C: product-page recommendations** | A/B test | About +560–970 buyers/mo | Low–Med | Attacks the weakest step; plenty of traffic. It can run alongside A. |
| 5 | Payment and checkout errors by hour (Investigate #4) | Investigate | Up to about +1,000 buyers/mo if it is a fixable bug (stage 2 estimated about 100 in the sample if half the evening gap closes) | Low | A cheap check with a possibly large payoff. |
| 6 | Contactability check (Investigate #3), then **Test B: abandoned-cart reminders** | Investigate → A/B test | About +835 buyers/mo × contactable share | Low if email exists; high if not | Proven tactic, but size and speed depend on reach. |
| 7 | Tracking fixes: order_id and de-duplication (Investigate #7) | Investigate / eng | Indirect (measurement quality) | Medium | Needed before order-level guardrails can be trusted. |
| 8 | Audit of $12+ product pages (Investigate #5) | Investigate | Feeds the next test | Low | Turns finding 4b into a concrete change. |
| 9 | Unbranded items (Investigate #6) | Investigate | Small | Low | Only 526 users are affected. |

---

## Caveats

- **The impact figures are what you get *if* the MDE is reached.** They are not forecasts. A test can come back flat.
- **Test B's effect** (more people coming back to the site) is partly reverse causality in the observational data: people who intend to buy come back in order to buy. Only the test can measure the real effect.
- **Production volumes come from October 2019 and a 10% user sample ×10.** Re-check daily traffic in the test tool before fixing the duration.
- **Monthly baseline buyers differ by method:** about 17,400 on the typical-day basis versus 23,950 from stage-1 sample buyers ×10. The typical-day basis leaves out burst days and repeat carters, so the impact estimates here are deliberately on the low side.
- **The data has no device, referrer, shipping or campaign fields.** Every "why" in the hypotheses above is a hypothesis, which is exactly what the tests are for.
