# Diagnosis: why users drop off (October 2019, 10% user sample)

*Stage 2. Builds on `output/funnel_summary.md` and uses its metric definitions unchanged (Viewed → Carted → Bought, nested, unique users).*
*Scripts: `work/d1_build_users.py` … `work/d7_final_numbers.py`. Clean-funnel numbers are saved in `work/d_final_funnels.json`.*

---

## Headline

> **The "weak checkout" in the blended funnel (19.0% cart → buy) is mostly not real.** 4,347 of the carters are what I call *ghost carts*. They come from the Oct 2/6/7 burst, and each one viewed one product, fired 1–3 cart events within seconds, and never came back. They make up **43% of everyone who carted and didn't buy**. Remove them, and cart → buy is **29.0%** while view → cart is **23.6%**. So the real weakest step is **getting browsers to add to cart**.
>
> Among genuine carters, the leak is concentrated in **small baskets** (≤ $20 carts buy 13% of the time vs 43% above $20) and in **carters who never come back after their first day** (20% vs 41%).

### Clean funnel (excluding the 4,347 ghost carts)

| Group | Viewed | Carted | View → Cart | Bought | Cart → Buy | Overall |
|---|---:|---:|---:|---:|---:|---:|
| All users, as reported in stage 1 | 39,269 | 12,596 | 32.1% | 2,395 | 19.0% | 6.10% |
| **All users, clean** | 34,922 | 8,249 | **23.6%** | 2,395 | **29.0%** | **6.86%** |
| Burst cohort (first seen Oct 2/6/7), clean | 3,847 | 1,026 | 26.7% | 370 | 36.1% | 9.62% |
| Regular cohort | 31,075 | 7,223 | 23.2% | 2,025 | 28.0% | 6.52% |

No buyers are removed. Every one of the 2,395 buyers is kept.

---

## Findings, ranked by business impact

### 1. About 4,300 "ghost carts" on Oct 2/6/7 create the apparent checkout problem, and they are probably not real shoppers

**What they look like.** 4,347 users were first seen on Oct 2, 6 or 7. Each one's entire month of activity is a single session containing:
- 1 product view;
- 1–3 cart events of that same product, 1–10 seconds apart (median 6 s);
- nothing else.

70% of them follow the exact sequence view → cart → cart → cart. 96% end on the cart event.

**Why I think they are not genuine shoppers.** Their timing doesn't look human:
- **31% of them carted between 00:00 and 05:59 UTC**, against 9% of real carters. Their activity is almost flat across the 24 hours.
- They make up 84%, 86% and 76% of first-time carters on Oct 2, 6 and 7.

Caveat: these users can't have bought by definition, so their 0% buy rate isn't evidence on its own. The evidence is the timing and the concentration on three days.

**Effect.** Once the ghost carts are removed:
- **Cart → buy goes from 19.0% to 29.0%.**
- **View → cart goes from 32.1% to 23.6%.**
- Overall conversion goes from 6.10% to 6.86%.

**The burst cohort's real users are actually above average.** The 3,847 non-ghost users from Oct 2/6/7 bought at **9.6% overall** (36% of their carters), against 6.5% for the regular cohort. On those days, real first-time carters were 351, 254 and 287, against a median of 224 on other days. So the burst did add real traffic, about +13–57%, and that traffic was good. **This reverses stage 1's reading that the burst was "low-intent campaign traffic".** The low-quality part is the ghost layer on top of it.

**Simpson's paradox check.** Blended, burst carters buy at 6.9% vs 28.0% for regular carters. Among carters with 2+ items, though, burst carters buy *more* often: **42.3% vs 38.6%**. The whole gap comes from the mix of single-item ghost carts.

**Users affected:** 4,347 users. That's 11% of viewers, 35% of carters, and 43% of carted-not-bought.

**Action:**
1. Find the traffic source for Oct 2/6/7, and Oct 1–8 more broadly, since 5,185 of all 5,410 single-view-and-cart-only users first carted in that week. Check referrer, UTM, IP/ASN and user agent.
2. If it was paid, ask for a refund or block the source.
3. Filter this pattern out of every funnel KPI going forward. Otherwise any cart-abandonment number is about 10 points too pessimistic.

---

### 2. Small baskets almost never check out: carts of $20 or less convert at 13% vs 43%

Among the 8,249 clean carters, buy rate rises steadily with the total value of what's in the cart:

| Cart value (unique products) | Carters | Bought |
|---|---:|---:|
| ≤ $10 | 2,387 | **6.0%** |
| $10–20 | 1,482 | 23.9% |
| $20–30 | 852 | 32.6% |
| $30–50 | 1,145 | 38.2% |
| $50–100 | 1,283 | 45.8% |
| $100+ | 1,100 | 54.1% |

**Robustness checks:**
- **Same pattern with a 7-day buy window** (≤ $10 converts at 5.8%), so it isn't caused by carts late in the month having less time to convert.
- **Same pattern in both the regular and burst cohorts.**
- **Single-item carts convert at 7.6% vs 39.1% for 2+ items** (2,634 users).
- **Within single-item carts, cheaper items convert *worse*:** <$2 at 2.0%, $2–4 at 3.2%, $4–7 at 3.6%, $7–12 at 7.4%, $12+ at 17.9%.

**Mix effect to watch.** Blended, cheap items look *fine*: carters whose median carted price is <$2 buy at 30%. That's because cheap items are usually part of large baskets. Split by basket size, a lone cheap item is the worst case.

**Likely cause (hypothesis, needs checking against the shipping policy).** A fixed shipping fee or minimum order makes a $3 order uneconomic for the customer. Two things are consistent with that:
- Only 7.8% of real orders are ≤ $10.
- Median order value is $28.53.

**Users affected:** 3,869 carters with ≤ $20 carts. That's **58% of all genuine carted-not-bought users (3,372 of 5,854)**.

**Action:** A/B test a visible free-shipping threshold in the cart, with an "add $X more" progress bar. Also test bundles or "frequently bought together" for low-value single items. As a sizing guide only: raising the ≤ $20 group from 13% to 20% would add about 280 buyers, roughly +12%.

---

### 3. Carters who don't come back after the first day rarely buy: 20% vs 41%

| Active days in October | Clean carters | Bought | Bought within 7 days (carts up to Oct 24) |
|---|---:|---:|---:|
| 1 | 4,566 | **19.5%** | 19.0% |
| 2 | 1,555 | 33.5% | 31.4% |
| 3–4 | 1,232 | 40.7% | 33.2% |
| 5+ | 896 | 53.8% | 37.4% |

**This is not just a basket-size effect.** Among carters with 2+ items, one-day users buy at 30.3% vs 39.3% for two-day users.

**When buyers buy.** 47.5% buy within an hour of their first cart, but **29% buy more than 24 hours later**. So bringing people back clearly works.

**Caveat.** Part of this is reverse causality: people who intend to buy come back in order to buy. Treat it as a pointer to where the opportunity is, not as a measured lift.

**Users affected:** 4,566 one-day carters, of whom **3,676 didn't buy (63% of genuine non-buyers)**. 2,522 of them also have a cart of $20 or less, so findings 2 and 3 overlap.

**Action:** Set up abandoned-cart reminders (email or push at 1 h and 24 h), which requires capturing an email early. Try including the free-shipping nudge from finding 2 in those reminders.

---

### 4. The real weakest step is view → cart, and it is mostly single-page bounces plus higher-priced product pages

- **Single-view bounces.** In the clean funnel, **53% of viewers (18,411) looked at exactly one product in one session and left.** Only 10.3% of them added anything to cart. Viewers who looked at 2 products carted at 16%, 3–4 products at 27%, 5–9 at 47%, and 10+ at 80%.
- **Higher-priced product pages.** Viewers whose median viewed price is **$12+ cart only 15.1% of the time**, against 28–30% for $2–7 items. That's 10,196 viewers, the largest price group. The gap holds at both depths:
  - 1 view: 6.6% vs about 12%.
  - 2+ views: 25.5% vs about 45%.

  So the gap isn't just because expensive pages attract bounces.

**Users affected:** 18,411 single-view viewers, and 10,196 viewers of $12+ items (these groups overlap).

**Action:**
- Find out which landing pages and referrers produce single-page sessions.
- Add product recommendations to product pages to get a second click.
- Audit the pages of $12+ products (photos, specs, reviews, delivery and returns information), where intent clearly drops.

*Device and referrer are not in the data, so I can't split this any further.*

---

### 5. Evening carts (18–23 UTC) convert about 10 points worse

| First-cart hour (UTC) | Clean carters | Bought |
|---|---:|---:|
| 00–05 | 680 | 28.8% |
| 06–11 | 2,858 | 32.5% |
| 12–17 | 2,579 | 30.2% |
| 18–23 | 2,132 | **23.0%** |

**This holds when basket size is held constant** (2+ items: 34.7% vs 43.1% in the morning; 1 item: 4.0% vs 9.3%) and with the 7-day buy window (20.3% vs 29.3%). The brands suggest a shop based around UTC+3, which would make this late evening local time. That points to casual or mobile browsing, or to support and payment availability at night.

**Users affected:** 2,132 carters. Closing half the gap would mean about 100 more buyers.

**Action:** This ranks below findings 1–4. Check whether checkout, payment or support behaves differently in the evening. Evening carters are also a natural first target for the reminders in finding 3.

---

## Checked and *not* a problem

These are listed so nobody chases them.

- **Removing items from the cart is a good sign, not friction.** Carters with any removal buy at 38–52%, vs 12% for those with none. This holds within 2+ item baskets: 20% with no removals vs 42–53% with removals. Removals mean active basket editing.
- **Day-of-week.** Blended, Sunday, Monday and Wednesday look terrible (11–16%). That is *entirely* burst/ghost mix. Clean, every weekday is 25–33%. Tuesday and Saturday are a few points lower (about 25%), which isn't material.
- **Cart → buy falls across the month** (39% → 25%). This is because late-month carters had less time to buy. With a fixed 7-day window it is flat to rising (24.9% → 30.6%).
- **Brand.** Named brands differ only modestly among regular users (about 26–41%). There's one exception: carts with **no brand on any item** convert at 12.6% vs 32.9%. Within 2+ item baskets the gap is 22.8% vs 40.8%, but that's only 526 users. It's worth a look (it may be unbranded or own-label stock), but it's small.
- **Heavy users and resellers.** Stage 1 already showed these don't change the funnel.

## Definitions and caveats

- **Ghost cart (suspect):** first seen Oct 2, 6 or 7, **and** the whole month's history is 1 view plus 1–3 cart events of a single product. That's 4,347 users. Another 1,063 users have the same pattern on other days, but their carting times look like normal daytime hours. They are **kept** as genuine (low-intent) users.
- **Cart value:** the sum of prices of the distinct products carted in the month.
- **Active days:** distinct calendar days (UTC) with any event.
- **Bought within 7 days:** first purchase within 168 h of first cart, among carters whose first cart was on or before Oct 24. This is used to correct for late-month carters having less time to buy.
- **Limits of the data:** there is no device, referrer, shipping-fee or campaign data. The shipping-threshold and traffic-source explanations are hypotheses to confirm with the business.
