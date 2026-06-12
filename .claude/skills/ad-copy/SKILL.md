---
name: ad-copy
description: >
  Generate high-converting ad copy for Google Ads (Search, Display, Performance Max) and Meta Ads (Facebook/Instagram).
  Use this skill whenever the user mentions: writing ads, ad copy, Google Ads, Meta Ads, Facebook Ads, Instagram Ads,
  campaign copy, headlines, descriptions, CTAs, ad creatives, A/B copy variants, or anything related to paid advertising copy.
  Also trigger for requests like "write me ads for X", "create campaign for Y", "copy for Google", "anuncios para Z".
  Always use this skill even if the request seems simple — ad copy has specific character limits and structural rules
  that require this skill's guidance to get right.
---

# Ad Copy Skill

Produce ad copy that converts — structured, within platform limits, and adapted to the audience and funnel stage.

## Workflow

1. **Gather context** (if not provided): product/service, target audience, USP, funnel stage (awareness/consideration/conversion), landing page URL if available, any brand voice or tone notes.
2. **Select platform format** from the table below.
3. **Write copy variants** — always produce at least 3 headline variants and 2 description variants per ad type.
4. **Apply copywriting principles** (see below).
5. **Character count check** — verify every line fits the limit.
6. **Output structured copy** in a clear table or labeled blocks.

---

## Platform Formats & Limits

### Google Search Ads (RSA — Responsive Search Ads)
| Element | Limit | Notes |
|---|---|---|
| Headlines | 30 chars each | Provide 10-15; Google picks combinations |
| Descriptions | 90 chars each | Provide 4; Google picks 2 at a time |
| Display URL paths | 15 chars each | 2 path fields after domain |
| Final URL | — | Must match ad topic |

### Google Performance Max
- Same headline/description limits as RSA
- Also need: long headlines (90 chars), business name, call to action label

### Meta Ads (Facebook / Instagram)
| Element | Limit | Recommended |
|---|---|---|
| Primary text | 125 chars (preview) / 2200 max | Keep key message in first 125 chars |
| Headline | 27 chars | Direct benefit or CTA |
| Description | 27 chars | Supporting detail |
| CTA button | Fixed options | See list below |

Meta CTA options: Learn More, Shop Now, Sign Up, Get Quote, Book Now, Contact Us, Apply Now, Download, Watch More, Send Message

---

## Copywriting Principles

### Hook formulas (headlines)
- **Benefit-first**: "Reduce HR costs by 40%"
- **Problem-agitation**: "Still managing payroll manually?"
- **Social proof**: "Trusted by 500+ SMBs in Spain"
- **Urgency/scarcity**: "Free audit — only 10 spots"
- **Question**: "Need a work permit in Spain?"
- **Number**: "3 steps to automate your invoicing"

### Description structure
- Lead with the strongest benefit
- Include one specific differentiator (speed, price, guarantee, exclusivity)
- End with a clear CTA verb: "Get a free quote", "Book a call", "Start today"

### B2B vs B2C tone
- **B2B**: professional, ROI-focused, specific metrics, decision-maker language
- **B2C**: emotional, benefit-driven, conversational, urgency

### Keyword insertion (Google)
- Include the primary keyword in at least 3 headlines naturally
- Match intent: informational vs transactional vs navigational

---

## Output Format

Always output copy in this structure:

```
## [Platform] Ad Copy — [Campaign/Product Name]

### Headlines (pick best combinations)
1. [Headline] — [X chars]
2. [Headline] — [X chars]
...

### Descriptions
1. [Description] — [X chars]
2. [Description] — [X chars]

### Display URL
domain.com / [path1] / [path2]

### Notes
- Primary keyword: [keyword]
- Funnel stage: [awareness/consideration/conversion]
- A/B test recommendation: [which variants to test first]
```

---

## Agency Context (Riqueza Digital)

When writing for agency clients:
- **Always read `clients/<cliente>/profile.md` first** for tone, audience and active services (regla 7 del orquestador)
- **Save output** to `clients/<cliente>/copy/YYYY-MM-DD_<tipo>_v1.md`
- For the full guided workflow (client selection, Content Manager agent, saving), use the `/marketing:generar-copy` command — this skill is its knowledge layer (limits, formulas, formats)
- Note character counts explicitly — clients and media buyers need to verify
- Provide 2–3 "bold" variants and 1–2 "safe" variants so client has options
- Flag any compliance risks (financial, legal, health claims) with a ⚠️
- Include a brief rationale for the copy angle chosen

---

## Quick Reference: Common Client Verticals

| Vertical | Proven angles |
|---|---|
| Legal / Permits | Speed, certainty, risk reduction |
| SaaS / Automation | Time saved, cost reduction, integration ease |
| E-commerce | Price, social proof, scarcity |
| Professional services | Expertise, track record, free first step |
| Real estate | Location, ROI, lifestyle |
