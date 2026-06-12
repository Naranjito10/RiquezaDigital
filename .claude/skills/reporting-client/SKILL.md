---
name: reporting-client
description: >
  Generate, structure, and write client performance reports for digital marketing retainers — covering SEO, paid ads,
  email marketing, social media, and automation results.
  Use this skill whenever the user mentions: client report, monthly report, performance report, results summary,
  KPI report, "report for my client", "summarize results", "agency report", "informe mensual", "reporte de resultados",
  "what to include in a report", or any request to present marketing or automation results to a client.
  Always use this skill — client reports require specific structure, narrative framing, and next-steps formatting
  to maintain trust and justify retainer value.
---

# Client Reporting Skill

Produce clear, professional performance reports that reinforce retainer value and guide next actions.

## Workflow

1. **Identify report type**: monthly retainer / campaign recap / onboarding / quarterly review
2. **Gather data inputs**: metrics from tools (Ahrefs, Meta Ads Manager, MailerLite, GA4, etc.)
3. **Build the narrative**: performance story = what happened + why + what's next
4. **Format the report**: executive summary first, detail below
5. **Add recommendations**: always end with 3 concrete next steps

---

## Report Structure (Monthly Retainer)

### Section 1: Executive Summary (1 page / top of report)
- Month, client name, report period
- 3–5 headline metrics (the numbers that matter most)
- One-paragraph summary: what worked, what didn't, what's next
- Traffic light status: 🟢 On track / 🟡 Attention needed / 🔴 Action required

### Section 2: Channel Performance

**SEO (if included)**
- Organic traffic (vs. prior month, vs. prior year)
- Keyword rankings: top gains, top losses, new entries
- Backlinks: new, lost, DR changes
- Top pages by traffic
- Technical issues resolved / pending

**Paid Ads (Google / Meta)**
- Spend, impressions, clicks, CTR
- Conversions (leads / purchases), CPA, ROAS
- Best-performing ad/creative
- Budget pacing (% spent vs. % of month)

**Email Marketing**
- Campaigns sent, open rate, CTR, unsubscribe rate
- Automation performance (active flows, conversion)
- List growth/decline
- Compare to industry benchmark: avg open rate 20–30% (B2B), 15–25% (B2C)

**Social Media**
- Reach, impressions, engagement rate per platform
- Follower growth
- Top performing post
- Profile visits / link clicks

**Automation / CRM (Riqueza Digital specific)**
- Automations active vs. erroring
- Leads processed, tasks automated
- Hours saved estimate (if trackable)

### Section 3: Highlights & Wins
- 2–3 specific wins with data ("Blog post X reached position 3 for [keyword]")
- Client-facing language: business impact, not just metrics

### Section 4: Issues & Observations
- What underperformed and why (hypothesis)
- External factors (algorithm changes, seasonality, competitor activity)
- What was tested and results

### Section 5: Recommendations & Next Steps
Always 3 concrete actions:
1. **Quick win** (can be done this week)
2. **Strategic move** (1–4 week implementation)
3. **Future consideration** (next quarter or roadmap)

---

## Metric Benchmarks Reference

| Metric | Good | Average | Needs attention |
|---|---|---|---|
| Email open rate (B2B) | >30% | 20–30% | <15% |
| Email CTR | >3% | 1.5–3% | <1% |
| Google Ads CTR (Search) | >5% | 2–5% | <2% |
| Meta Ads CTR | >1.5% | 0.8–1.5% | <0.5% |
| Meta Ads ROAS (e-com) | >3x | 2–3x | <2x |
| Organic traffic MoM growth | >5% | 0–5% | negative |
| Social engagement rate (IG) | >3% | 1–3% | <1% |
| Social engagement rate (LinkedIn) | >2% | 0.5–2% | <0.5% |

---

## Narrative Framing Principles

- **Lead with wins** even if performance was mixed — trust first
- **Attribute results to actions**: "The 15% traffic increase is driven by the 3 blog posts published in March"
- **Contextualize dips**: seasonality, external factors, testing phases
- **Use plain language**: clients don't know what "DR" or "ROAS" means without a brief definition the first time
- **Avoid excuses**: if something underperformed, own it + show the plan

---

## Output Format (Quick Report)

```
## [CLIENT NAME] — Performance Report
### Period: [Month Year]

---

### 📊 Executive Summary

| Metric | This Month | Last Month | Change |
|---|---|---|---|
| [Key metric 1] | | | ↑/↓ % |
| [Key metric 2] | | | |
| [Key metric 3] | | | |

**Summary**: [2–3 sentence narrative]

**Overall status**: 🟢 / 🟡 / 🔴

---

### [Channel] Performance
[Data + narrative]

---

### 🏆 Highlights
- [Win 1 with data]
- [Win 2 with data]

### ⚠️ Attention Areas
- [Issue + hypothesis]

### 🔜 Next Steps
1. [Quick win]
2. [Strategic action]
3. [Future consideration]
```

---

## Agency Context (Riqueza Digital)

- **Execution commands**: `/marketing:reporte-semanal` and `/marketing:reporte-mensual` run the Python pipeline (`pipelines/marketing-digital/reports/monthly_report_generator.py`) that compiles metrics into HTML. This skill is the knowledge layer: narrative framing, structure, and benchmarks for any report
- **Save path (regla 4 del orquestador)**: `clients/<nombre>/reports/YYYY-MM-DD_<tipo>.md`
- **Delivery timing**: reports due by the 5th of the following month
- **Format**: Notion page preferred (client can comment inline); PDF export for formal clients
- **Tone**: professional but warm — you're a partner, not a vendor
- **Retainer justification**: always include an "hours invested" or "value delivered" line if client is questioning value
- **Tools to pull data from**: Ahrefs (SEO), Meta Ads Manager, Google Ads, MailerLite/Klaviyo, GA4
- **Spanish**: default to Spanish for Spanish-market clients unless they've requested English
