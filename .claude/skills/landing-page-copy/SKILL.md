---
name: landing-page-copy
description: >
  Write and optimize landing page copy for lead generation, sales, and service pages — focused on conversion rate optimization (CRO).
  Use this skill whenever the user mentions: landing page, sales page, lead gen page, squeeze page, homepage copy,
  above the fold, hero section, CRO, conversion rate, page copy, value proposition, headline for a page,
  "rewrite my website", "improve my landing page", "copy for my service page", or any web page meant to convert visitors.
  Also trigger when reviewing or critiquing an existing page's copy. Always use this skill — landing pages require
  specific structural and psychological principles to convert, not just good writing.
---

# Landing Page Copy Skill

Write landing page copy that converts visitors into leads or customers, using proven CRO frameworks.

## Workflow

1. **Identify page goal**: lead capture / book a call / direct sale / free trial / download
2. **Gather context**: offer, audience, traffic source (cold/warm/paid/organic), key objections
3. **Choose page structure** based on goal and offer complexity
4. **Write section by section** using the frameworks below
5. **CRO review**: apply the checklist before finalizing

---

## Page Structure by Goal

### Lead Generation Page (book a call, free audit, download)
```
1. Hero: Headline + Subheadline + CTA
2. Problem/Pain (2–3 bullets or short para)
3. Solution intro (what you offer + how it's different)
4. Social proof (logos, testimonials, numbers)
5. What they get (features → benefits)
6. Objection handling (FAQ or trust block)
7. CTA section (repeated)
```

### Sales / Service Page (longer, higher ticket)
```
1. Hero: Bold promise + context
2. Empathy block: "You're here because..."
3. Agitation: cost of not solving this
4. Solution: your service/product
5. Process: how it works (3–5 steps)
6. Results: case studies or data
7. What's included: clear offer breakdown
8. Guarantee / risk reversal
9. FAQ
10. Final CTA
```

### Short Squeeze Page (lead magnet)
```
1. Headline: what they get + who it's for
2. 3–5 bullet benefits
3. Form + CTA button
4. Trust signals (no spam, privacy note)
```

---

## Headline Frameworks

| Framework | Template | Example |
|---|---|---|
| Outcome-focused | "Get [result] without [pain]" | "Get a Spanish work permit without the paperwork nightmare" |
| Who + What | "[Who] finally have [result]" | "HR managers finally have a compliant permit process" |
| Time-bound | "[Result] in [timeframe]" | "Automate your invoicing in 48 hours" |
| Specificity | "[Specific number/metric]" | "Save 12 hours/week on client reporting" |
| Question | "Tired of [problem]?" | "Tired of chasing clients for feedback?" |
| Bold claim | "[Big promise]. [Credibility anchor]." | "We fill your calendar. Guaranteed." |

**Subheadline**: Clarify who it's for and what happens next. 1–2 sentences max.

---

## CRO Principles

### Above the fold
- Visitor must understand in 5 seconds: what it is, who it's for, what to do next
- CTA button: action verb + specific benefit ("Get My Free Audit", not "Submit")
- No navigation links that take visitors away

### Social proof
- Specific beats generic: "saved 8 hours/week" > "saved time"
- Logo bars add credibility even without testimonials
- Numbers: clients served, projects completed, years in business

### Objection handling
- List the 3 biggest reasons someone wouldn't buy → answer each
- Common objections: price, trust, timing, relevance, complexity

### Risk reversal
- Money-back guarantee, free first session, no-commitment audit
- "If you don't X, we'll Y" language builds confidence

### Friction reduction
- Short forms: ask only what's needed
- Social login or calendar embed reduces drop-off
- Trust seals, privacy notes near CTAs

---

## Copywriting Micro-Patterns

- **You/Your language**: speak directly to the reader, not about yourself
- **Specificity**: "3 days" not "quickly", "€2,400/month saved" not "significant savings"
- **Sensory details in benefits**: help them picture the outcome
- **Short sentences**: especially in hero and CTA sections
- **Bullet format**: benefits list, not features list — "So you can X" framing

---

## Output Format

```
## Landing Page Copy — [Page Name / Offer]

### HERO SECTION
**Headline**: [headline]
**Subheadline**: [subheadline]
**CTA Button**: [button text]
**Supporting text** (optional, under button): [e.g., "No commitment. Free for 30 days."]

---

### [SECTION NAME]
[Copy block]

---

### CTA SECTION (repeated)
**Headline**: [urgency/benefit headline]
**CTA Button**: [button text]
**Microcopy**: [trust line under button]

---

### FAQ
Q: [question]
A: [answer]

---

**CRO Notes**:
- Primary objection addressed: [X]
- Recommended A/B test: [headline variant or CTA variant]
- Traffic source assumption: [cold paid / warm referral / organic SEO]
```

---

## Agency Context (Riqueza Digital)

- For client landing pages: always ask for their current conversion rate if they have one (baseline for improvement)
- Deliver copy in sections so client can approve block by block
- RD stack: WordPress via REST API (`/web:wp-edit`, `/web:wp-page-rd`) or Vercel — use the client's existing CMS, avoid building new dependencies
- For visual/layout work pair this skill with `/web:generar-prompt-web` or `/web:autopilot-diseno` (this skill covers the copy, those cover the build)
- For high-ticket services: long-form pages outperform short ones (trust needs more space)
- GDPR note: forms in Spain/EU must have explicit consent checkbox, not pre-ticked
