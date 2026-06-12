---
name: proposal-generator
description: >
  Generate professional commercial proposals for digital agency services, retainer contracts, and project scopes.
  Use this skill whenever the user mentions: proposal, presupuesto, propuesta comercial, scope of work, retainer offer,
  "send a proposal", "write a quote", "proposal for a client", "service agreement", "onboarding document",
  "how much to charge", or any request to structure and present a service offering to a prospective or existing client.
  Always use this skill — proposals require specific psychological structure, pricing framing, and scope language
  to convert prospects and set correct expectations.
---

# Proposal Generator Skill

Create proposals that close deals — structured to build value before revealing price, and scoped to protect both parties.

## Workflow

1. **Gather deal context**: prospect name, their problem, services needed, budget signal (if known), decision timeline
2. **Choose proposal type** (see below)
3. **Build the proposal** section by section
4. **Price framing**: anchor high, justify value, offer tiers if appropriate
5. **Next step CTA**: always end with a single clear action

---

## Proposal Types

### Type A: Retainer Proposal (monthly services)
Best for: ongoing clients, full-scope retainers, Riqueza Digital standard model

### Type B: Project Proposal (one-time scope)
Best for: website builds, campaign launches, audits, migrations

### Type C: Audit / Discovery Proposal (paid first step)
Best for: new prospects who need trust built before a full retainer
Converts skeptics: low barrier, delivers value, leads to Type A

---

## Proposal Structure

### 1. Cover / Header
- Client name, company, date
- Proposal title (not "Proposal" — something specific: "Growth Strategy for [Company]: Digital Marketing Retainer")
- Your name/brand, contact info

### 2. Understanding Your Situation (The Mirror)
- Show you listened: restate their problem in their words
- Include: current situation, pain points, goals mentioned in discovery call
- **Never skip this** — it's the difference between a generic quote and a tailored proposal

Example:
> "Based on our conversation, [Company] is currently generating leads primarily through referrals, but you're looking to build a predictable inbound channel before Q4. The main challenge is [X], and the goal is [Y] by [timeframe]."

### 3. Recommended Approach
- What you're proposing and why (connect to their stated goals)
- Brief explanation of methodology — enough to show expertise, not so much it overwhelms
- Timeline / phases if applicable

### 4. Scope of Work
List services clearly. For retainers, break into monthly deliverables:

```
## Monthly Deliverables

### SEO & Content
- X blog posts/month (optimized, published)
- Monthly keyword ranking report
- Technical SEO audit (quarterly)

### Paid Ads Management
- Campaign setup and management (Google/Meta)
- Weekly performance monitoring
- Monthly optimization report

### Email Marketing
- X campaigns/month
- Automation maintenance
- Monthly performance review

### Reporting
- Monthly performance report (delivered by 5th)
- Monthly strategy call (60 min)
```

### 5. Investment (Price Section)
**Framing rules**:
- Show value/ROI before showing price
- Use "investment" not "cost" or "price"
- Anchor: if you have tiers, present most comprehensive first
- If single price: briefly state what they'd pay elsewhere or the value of the outcome

**Tier structure** (if using):
| | Essential | Growth | Scale |
|---|---|---|---|
| Price | €X/mo | €Y/mo | €Z/mo |
| [Service 1] | ✅ | ✅ | ✅ |
| [Service 2] | ❌ | ✅ | ✅ |
| [Service 3] | ❌ | ❌ | ✅ |
| Hours/mo | X | Y | Z |
| Best for | [profile] | [profile] | [profile] |

**Risk reversal**: include a guarantee or first-month clause if appropriate
("30-day satisfaction guarantee" / "We'll refund the first month if you're not satisfied")

### 6. Why Riqueza Digital
- 3–5 bullet differentiators (not generic — specific to this client's situation)
- 1–2 relevant results or case studies (quantified)
- Social proof: client names, testimonials, logos (if permitted)

### 7. Next Steps
- Single clear CTA: "To move forward, reply to this email / book a call / sign below"
- Validity period: "This proposal is valid for 14 days"
- What happens after they say yes (onboarding overview)

### 8. Terms (brief)
- Payment terms: e.g., "Invoiced on the 1st of each month, net 15"
- Contract period: e.g., "Minimum 3-month commitment, then rolling monthly"
- Termination: e.g., "30 days written notice"

---

## Pricing Psychology

- **Anchor high**: present comprehensive option first, even if you expect them to choose middle
- **Monthly vs. annual**: offer annual with 2 months free if cash flow allows
- **Itemized vs. bundled**: bundled ("Growth Retainer €2,500/mo") converts better than itemized lists
- **Round numbers**: €2,500 feels considered; €2,487 feels calculated but awkward
- **Never apologize for price** — confidence in your rate signals confidence in your value

---

## Output Format

Always produce a ready-to-send document, not a skeleton. Fill in all sections with real copy based on the context provided.

```
# [PROPOSAL TITLE]
**Prepared for**: [Client Name / Company]
**Prepared by**: Kevin — Riqueza Digital
**Date**: [Date]
**Valid until**: [Date + 14 days]

---

## Understanding Your Situation
[Mirror section]

## Our Recommended Approach
[Approach section]

## Scope of Work
[Deliverables]

## Investment
[Pricing section]

## Why Riqueza Digital
[Differentiators]

## Next Steps
[CTA]

## Terms
[Brief terms]
```

---

## Agency Context (Riqueza Digital)

- **Default retainer range**: €1,500–€4,000/mo depending on scope (adjust based on market)
- **Always include**: monthly strategy call, reporting, and Notion workspace for client visibility
- **Avoid**: hourly pricing for ongoing work — it penalizes efficiency
- **Follow-up**: if no response in 5 days, send a 2-line check-in (not a push)
- **Language**: Spanish for Spanish clients, English for international clients
- **Save path (regla 5 del orquestador)**: `clients/<nombre>/proposals/YYYY-MM-DD_<tipo>.md` — always save the markdown source here first
- **Delivery format**: Notion page > PDF > Google Doc (in order of preference), generated from the saved markdown
- **Nunca confirmar precios finales sin checkpoint de Kevin** (regla 1: ninguna decisión de gasto/precio sin confirmación)
