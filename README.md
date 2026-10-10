# 🩺 Funnel Doctor

**An AI agent that audits an e-commerce funnel the way a senior product analyst would.**

Give it a raw event log. It explores the data, builds the funnel, finds where and *why* users drop off, designs A/B tests with real sample sizes, and hands you a founder-ready report. You don't script the analysis steps; the agent decides what to investigate next.

📄 **[See a sample report →](Examples/report.html)** · Built with the [Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview)

---

## What it found on a real store

Run on one month of event data from an online cosmetics shop (~400k events, 40k users):

- **The checkout was healthier than it looked.** The raw cart-to-purchase rate was 18.8%. The agent traced a third of all carters to three days of bot-like traffic (19-second sessions, one item, never returned). On clean traffic, the real rate was **26.6%**.
- **The real leak was small carts.** Carts under $10 converted at **5.6%** vs **36.1%** above it, with a sharp step at ~$10 that suggests a shipping-fee barrier.
- **It caught Simpson's paradox on its own.** Weekday and hour-of-day "effects" turned out to be the spike days in disguise, so it told the founder *not* to optimise them.
- **It designed the fixes:** a free-shipping progress bar, an add-on rail and abandoned-cart reminders, each with baseline, MDE, sample size and test duration.

## How it works

The agent runs in four stages, each building on the last:

| Stage | What the agent does | Output |
|---|---|---|
| 1. Profile & funnel | Understands the data, flags quality issues, builds the funnel | `funnel_summary.md` |
| 2. Diagnosis | Segments the weakest step, follows anomalies, checks for mix effects | `diagnosis.md` |
| 3. Experiments | Turns findings into A/B tests with computed sample sizes | `recommendations.md` |
| 4. Report | Builds a single-page HTML report with charts | `report.html` |

At each stage, Claude writes its own Python (pandas), runs it, reads the results and decides what to dig into next. The analyst method (how to approach a funnel, what to be skeptical of, how to word recommendations) is encoded in the system prompt in `funnel_doctor.py`.

## Run it yourself

**Requirements:** Python 3.10+, a Claude account (Pro or higher), and [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) logged in.

```bash
git clone https://github.com/thepalakgupta/funnel-doctor.git
cd funnel-doctor
python -m venv .venv
.venv\Scripts\activate        # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

**Get the data:** download `2019-Oct.csv` from [eCommerce Events History in Cosmetics Shop](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) on Kaggle and put it in a `data/` folder. Then:

```bash
python make_sample.py         # creates a 10% user sample with full journeys intact
python funnel_doctor.py       # runs the full audit
```

Open `output/report.html` when it finishes. To audit the full month instead of the sample, run `python funnel_doctor.py data/2019-Oct.csv`.

## Design choices

- **Sample by user, not by row.** Keeping each sampled user's complete journey keeps funnel rates accurate at a fraction of the runtime.
- **Unique users, not events.** Rates count people, which makes them robust to duplicate events and tracking noise.
- **Skeptical by default.** The agent is told to verify surprising numbers, define each metric once and state caveats. Its findings are presented as correlations and hypotheses, not proven causes.

## Limitations

- The dataset has no shipping, device or traffic-source fields, so some causes (like the $10 shipping barrier) are hypotheses to confirm with the business.
- The playbook currently expects a view → cart → purchase event log.

---

Built by [Palak Gupta](https://github.com/thepalakgupta), an analyst working at the intersection of AI and product analytics.