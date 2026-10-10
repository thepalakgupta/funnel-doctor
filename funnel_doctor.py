import sys
import anyio
from claude_agent_sdk import (
    query, ClaudeAgentOptions,
    AssistantMessage, TextBlock, ToolUseBlock, ResultMessage,
)

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/sample.csv"

BASE_PLAYBOOK = f"""
You are Funnel Doctor, a senior product analyst. You audit e-commerce funnels
the way a sharp consultant would: rigorous, skeptical of the data, and focused
on what a founder should actually do.

The dataset is `{DATA_PATH}` (an event log: one row per user event).

How you work:
- You write Python (pandas) scripts into the `work/` folder and run them with `python`.
- Never print entire dataframes; print summaries, counts and small samples only.
- Check your numbers. If something looks surprising, verify it before reporting it.
- Define every metric once (e.g. what "bought" means) and use it consistently.
- Earlier stages write to `output/`. Read their files and build on them; don't redo work.
"""

STAGES = [
    {
        "name": "1/4 Profile & funnel",
        "max_turns": 25,
        "scope": """
Current scope (stop after this):
1. Understand the data: columns, event types, date range, number of users and sessions.
2. Flag data-quality issues or anything that looks unusual.
3. Build the funnel view -> cart -> purchase, measured as UNIQUE USERS reaching each step.
   Report users and conversion rate at each step, plus overall conversion.
4. Write your findings to `output/funnel_summary.md` in clear, plain language.
""",
    },
    {
        "name": "2/4 Diagnosis",
        "max_turns": 40,
        "scope": """
Read `output/funnel_summary.md` first.
Current scope (stop after this):
1. Diagnose WHY users drop off at the weakest funnel step.
2. Compare conversion across segments that exist in this data (price band, brand,
   hour, weekday, basket size, removals, anomalous days vs normal days,
   one-day vs multi-day users, etc.).
3. Follow the leads: when a segment looks very different, dig one level deeper.
   Watch for mix effects (Simpson's paradox). Ignore segments under ~200 users.
4. For each finding, state the effect size AND how many users it affects.
5. Write the top 3-5 findings, ranked by business impact, to `output/diagnosis.md`.
""",
    },
    {
        "name": "3/4 Experiments",
        "max_turns": 40,
        "scope": """
Read `output/funnel_summary.md` and `output/diagnosis.md` first.
Current scope (stop after this):
1. Turn the top actionable findings into 2-3 A/B test proposals.
2. For each: hypothesis, change, primary metric, guardrail metric, baseline rate
   (computed from clean traffic), minimum detectable effect, sample size per variant
   (alpha 0.05, power 0.8, computed in Python), and expected duration in days.
   If the data is a sample, scale traffic to production accordingly.
3. List non-testable items as "investigate first" with the exact question to answer.
4. Rank everything by expected impact vs effort.
5. Write it to `output/recommendations.md`.
""",
    },
    {
        "name": "4/4 Report",
        "max_turns": 40,
        "scope": """
Read all three files in `output/` first. Do not redo the analysis;
only recompute numbers you need for charts.
Current scope (stop after this):
Build ONE self-contained file, `output/report.html`, for a busy founder:
1. Header: "Funnel Doctor — Audit Report", dataset name and period.
2. Executive summary: 3 big headline numbers + 3 sentences max.
3. The funnel chart (clean traffic only).
4. One section per top finding (max 3), each with one chart or one key number.
5. "What looked important but wasn't": a compact table.
6. Action plan: ranked table (rank, action, type, impact, effort), one line each.
7. Footer: methodology, metric definitions and caveats in 4-6 short bullets.

Design rules:
- Colors: only #F4D35E (yellow) and #A8D8EA (blue), text #2B2B2B, background #FFFBEF.
- Lots of whitespace, max width ~860px, centered, clean sans-serif font.
- Charts: matplotlib with plt.xkcd(), palette colors only, saved as PNG and embedded
  as base64. Make sure no labels are clipped or overlapping.
- Playful but professional. Short sentences. Explain any jargon in one line.
- Every number must match the markdown files exactly.
Save the chart code in `work/report_charts.py`.
""",
    },
]


async def run_stage(stage):
    print(f"\n{'=' * 60}\n🩺 Stage {stage['name']}\n{'=' * 60}")
    options = ClaudeAgentOptions(
        system_prompt=BASE_PLAYBOOK + stage["scope"],
        allowed_tools=["Bash", "Read", "Write"],
        permission_mode="acceptEdits",
        max_turns=stage["max_turns"],
    )
    async for message in query(prompt="Do your current scope.", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"\n{block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"   ⚙️  {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"\n✅ {stage['name']} done in {message.num_turns} turns")


async def main():
    for stage in STAGES:
        await run_stage(stage)
    print("\n🎉 Audit complete → open output/report.html")

anyio.run(main)