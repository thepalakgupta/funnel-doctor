# Funnel Summary: October 2019 (10% user sample)

*Stage 1: data understanding, data quality, and the view → cart → purchase funnel.*
*Scripts: `work/s1_explore.py` … `work/s5_spike_check.py`. Machine-readable numbers: `output/funnel_metrics.json`.*

---

## Headline

> **Of 39,269 users who viewed a product in October, 12,596 (32.1%) added something to cart, and 2,395 of those (19.0%) bought. That is 6.1% overall, view to purchase.**
>
> **Those blended numbers hide two very different groups.** About 8,300 users who first arrived in a burst on **Oct 2, 6 and 7** add to cart at a very high rate (66%) but almost never buy (7% of carters). Everyone else adds to cart less often (23%) but **buys 28% of the time**. The real cart problem is narrower than the blended number suggests, and it is concentrated in that burst.

---

## 1. The data

| Item | Value |
|---|---|
| Source | `data/sample.csv`, a ~10% sample of users (every `user_id` ending in 0) from the Oct-2019 event log, with each user's full journey kept |
| Rows (events) | 407,521 (387,000 after removing exact duplicates) |
| Columns | `event_time, event_type, product_id, category_id, category_code, brand, price, user_id, user_session` |
| Event types | view 185,897 · cart 121,838 · remove_from_cart 74,965 · purchase 24,821 |
| Date range | 2019-10-01 00:00 → 2019-10-31 23:59 UTC (31 full days, no gaps) |
| Users | 40,382 |
| Sessions | 88,799 (median user has 1 session; mean 2.2) |
| Products | 30,370 |
| Price | median $4.11, max $299.81. Mostly low-ticket items (brands like *lovely*, *runail*, *irisk* suggest a cosmetics / nail-supply shop) |

**A "purchase" row is a line item, not an order.** The 24,781 de-duplicated purchase rows make up **2,993 orders** (grouped by user + session + timestamp) from **2,589 buyers**. That is about 8.3 items per order, an average order value of **$40.38**, and **$120,856** in revenue in this sample.

---

## 2. Data-quality issues and anomalies

Ranked by how much each one matters for the analysis.

1. **Traffic burst on Oct 2, 6 and 7 (most important).** On these days the number of users adding to cart jumped from about 430/day to **2,276, 2,004 and 1,373**, while daily buyers stayed flat at about 90–110. Of the users carting on those days, 88–96% were **brand-new that day**.
   - It does **not** look like a bot. Nearly all of them (96–99%) viewed products, carts were spread across thousands of products (the top product had under 0.5% of carts), activity followed normal daytime hours, and they removed items and sometimes bought.
   - It most likely reflects a **marketing campaign or promo that brought in low-intent visitors**. Only about 9% of these users bought during the month, against about 38% of carters on a typical day (Oct 15, used for comparison). **This needs confirming against the marketing calendar.**
   - Because of this burst, the blended funnel overstates view → cart and understates cart → purchase (see section 3).
2. **Purchase rows are line items.** Counting rows as orders would overstate orders about 8x. All "bought" metrics below count **users**, so they are not affected.
3. **Add-to-cart often happens without a product view.**
   - 1,041 users added to cart but never had a view event, and 179 buyers never had one.
   - Only about 20% of carted products had been viewed by that user beforehand, and about 2,200 users added to cart *before* their first view.
   - This means add-to-cart is mostly done from listing or category pages (quick-add), so a "view" event is not a product-page step that users must pass through. The funnel below treats "viewed" as **"was active on the site and browsed"**.
4. **Exact duplicate rows: 20,546 (5.0%)**, almost all `remove_from_cart` (17,576) and `cart` (2,920). These are probably double-fired tracking events. They are removed for all metrics here. They don't change user counts, but they would inflate any event-count metric.
5. **Missing category data.**
   - `category_code` is missing on **98.5%** of rows, so category analysis must use `category_id` (numeric codes only).
   - `brand` is missing on 40% of rows.
6. **Odd prices.** 448 rows have price = $0 (mostly views) and 1 row has a negative price (−$15.87). This is negligible for a user-based funnel, but these rows should be excluded from revenue work.
7. **Heavy users and possible resellers or bots.**
   - 37 users have more than 500 events each. Together they account for 7% of events and 5% of purchase lines.
   - One user has **1,044 sessions** in a month (session IDs appear to reset on nearly every event).
   - Another bought 329 line items with only 10 views, which looks like a wholesale or reseller pattern.
   - Removing these heavy users barely changes the funnel (6.10% → 6.03% overall), so they are kept.
8. **Minor issues.** 72 rows have no `user_session` (kept for user-level metrics). No session ID maps to more than one user, which is a good sign.

---

## 3. The funnel: unique users

### Metric definitions (used everywhere from here on)

- **Viewed** = the user has at least one `view` event in October.
- **Carted** = the user viewed **and** has at least one `cart` event.
- **Bought** = the user viewed, carted **and** has at least one `purchase` event.
- The funnel is *nested*: each step only counts users who reached the step before it. Step conversion = this step ÷ previous step. **Overall conversion = Bought ÷ Viewed.**
- Time order within the month is not enforced, because of issue 3 above.

### Primary funnel: all users

| Step | Users | Conversion from previous step | Conversion from View |
|---|---:|---:|---:|
| Viewed | 39,269 | – | 100% |
| Carted | 12,596 | **32.1%** | 32.1% |
| Bought | 2,395 | **19.0%** | **6.10%** |

**Biggest absolute drop:** 26,673 viewers (68%) never add anything to cart, and 10,201 carters (81%) never buy.

### The burst cohort changes the picture

| Group | Viewed | Carted | View → Cart | Bought | Cart → Buy | Overall |
|---|---:|---:|---:|---:|---:|---:|
| Users first seen Oct 2/6/7 (burst) | 8,194 | 5,373 | 65.6% | 370 | **6.9%** | 4.5% |
| All other users | 31,075 | 7,223 | 23.2% | 2,025 | **28.0%** | 6.5% |
| **All users** | 39,269 | 12,596 | 32.1% | 2,395 | 19.0% | 6.1% |

**What this means:**

- The burst users make up only 21% of viewers, but **43% of carters and 49% of the "carted but never bought" volume**: of the 10,201 carters who never bought, 5,003 come from the burst.
- For the **regular base**, the funnel looks like this: **under 1 in 4 viewers add to cart, but more than 1 in 4 carters buy.** In that group, the bigger leak is **getting browsers to add to cart**, not checkout.

### Cross-checks (to confirm the numbers hold up)

- **Loose definition** (count anyone with the event, regardless of earlier steps):
  - 13,637 users carted and 2,589 bought.
  - Cart → buy is **19.0%**, the same as the nested funnel.
  - Overall conversion is **6.4% of all 40,382 users**.
  - The nested funnel drops 194 buyers who have no view or no cart event (issue 3).
- **Excluding heavy users** (more than 500 events after removing duplicates; 31 users): 32.0% → 18.8% → 6.03%. This is essentially unchanged.
- **Session-level funnel** (for reference only, since users take several sessions to buy):
  - 84,018 sessions had a view.
  - 23.1% of those reached cart.
  - 10.4% of sessions with a cart ended in a purchase.
  - 2.4% of sessions with a view ended in a purchase.

---

## 4. What this means for a founder (preliminary)

- **Treat 6.1% (view → purchase, users) as the baseline**, but always split out the Oct 2/6/7 cohort. Otherwise any month-over-month comparison will be misleading.
- **Find out what happened on Oct 2, 6 and 7.** If it was paid acquisition, it brought in about 8,300 users who produced only 370 buyers. Before repeating it, compare the spend against that result.
- **For regular users, the add-to-cart step is the weak point (23%).** Checkout converts reasonably well (28% of carters buy).
- **Fix tracking before going deeper:** remove duplicate cart and remove events, log an order ID with purchases, and populate `category_code`.

*Next stage (not done here): diagnose why users drop off at each step, e.g. by device, price band, category, new vs returning, and time-to-purchase.*
