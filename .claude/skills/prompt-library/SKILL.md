---
name: prompt-library
description: >
  Create, organize, and improve reusable prompts for recurring tasks in marketing, client work, and agency operations.
  Use this skill whenever the user mentions: prompt template, reusable prompt, prompt for X task, prompt library,
  "save this prompt", "make a prompt for my team", "prompt to use every month", "sistemática de prompts",
  "write a prompt for [task]", or any request to create a prompt that will be used repeatedly across clients or tasks.
  Also trigger when the user wants to improve an existing prompt or turn a one-time workflow into a reusable asset.
  Always use this skill — reusable prompts need specific structure (context injection, output format, variables)
  that one-off prompts don't require.
---

# Prompt Library Skill

Build prompts that work reliably every time — structured for repeatability, variable injection, and team use.

## Workflow

1. **Identify the recurring task**: what will this prompt be used for?
2. **Define variables**: what changes between uses? (client name, topic, data, tone...)
3. **Choose prompt pattern** (see patterns below)
4. **Write the prompt** with clear structure
5. **Test it mentally**: walk through a real use case
6. **Output the final prompt** in copy-paste format with usage notes

---

## Prompt Anatomy

Every reusable prompt needs:

```
[ROLE/CONTEXT]       → Who Claude is acting as, what situation we're in
[VARIABLES]          → What the user fills in before sending (use {{brackets}})
[TASK]               → Exactly what to do
[CONSTRAINTS]        → What NOT to do, limits, format rules
[OUTPUT FORMAT]      → How the response should be structured
[EXAMPLE] (optional) → One example of ideal output
```

---

## Prompt Patterns by Category

### Marketing Prompts

**Ad Copy Generator**
```
You are a direct response copywriter specializing in {{platform}} ads for {{industry}} businesses.

Write ad copy for the following offer:
- Product/Service: {{product_or_service}}
- Target audience: {{audience}}
- Key benefit/USP: {{usp}}
- Funnel stage: {{awareness|consideration|conversion}}
- Tone: {{professional|casual|urgent|warm}}

Produce:
- {{n}} headlines (max {{char_limit}} characters each)
- {{n}} descriptions (max {{char_limit}} characters each)
- 1 CTA recommendation

Format each variant on its own line with character count in parentheses.
Do not use superlatives without proof (best, #1, guaranteed) unless specified.
```

**Email Subject Line Generator**
```
You are an email marketing specialist with expertise in {{industry}}.

Generate 10 subject line options for an email about:
- Topic: {{topic}}
- Audience: {{audience_segment}}
- Goal: {{open_for_click|open_for_reply|open_for_awareness}}
- Tone: {{professional|casual|urgent}}
- Personalization token available: {{yes|no}} ({{first_name}})

For each subject line, include:
1. The subject line text
2. Character count
3. One-line rationale for the angle used

Avoid: ALL CAPS, excessive punctuation, spam trigger words (free, guarantee, click here).
End with your top 3 recommendations and why.
```

**Monthly Content Calendar**
```
You are a social media strategist for a {{industry}} business.

Create a 4-week content calendar for {{platform}} with the following:
- Brand: {{brand_name}}
- Audience: {{target_audience}}
- Content pillars: {{pillar_1}}, {{pillar_2}}, {{pillar_3}}
- Posts per week: {{frequency}}
- Tone: {{tone}}
- Language: {{Spanish|English}}

For each post provide:
1. Week number and day
2. Content pillar
3. Post format (text/carousel/reel/story)
4. Hook/opening line
5. 2-sentence copy summary (full draft in follow-up if needed)
6. Hashtag suggestions (5 per post)

Output as a markdown table.
```

---

### Client Operations Prompts

**Monthly Report Narrative**
```
You are writing a marketing performance report for a client.

Context:
- Client: {{client_name}}
- Industry: {{industry}}
- Period: {{month}} {{year}}
- Services: {{services_list}}

Data:
{{paste_raw_metrics_here}}

Write a professional performance report with:
1. Executive summary (3–4 sentences, lead with wins)
2. Channel-by-channel analysis (one paragraph per channel)
3. What worked and why
4. What needs improvement and the hypothesis
5. 3 concrete recommendations for next month

Tone: professional but approachable, as a trusted advisor not a vendor.
Language: {{Spanish|English}}
Avoid: jargon without explanation, excuses without solutions, vague statements.
```

**Client Onboarding Welcome Email**
```
You are writing a welcome email from a digital agency to a new client.

Context:
- Agency: Riqueza Digital
- Client name: {{client_first_name}}
- Company: {{company_name}}
- Services starting: {{services}}
- Kickoff date: {{kickoff_date}}
- Account manager: Kevin

Write a warm, professional welcome email that:
1. Expresses genuine excitement about working together
2. Confirms next steps (kickoff call date/time)
3. Outlines what to expect in the first 2 weeks
4. Provides a link to the Notion client portal: {{notion_url}}
5. Ends with a clear CTA (confirm the kickoff call)

Length: 200–300 words. Tone: warm, confident, organized.
Subject line: provide 3 options.
Language: {{Spanish|English}}
```

**Proposal Value Section**
```
You are a senior consultant writing the "Why Us" section of a commercial proposal.

Context:
- Agency: Riqueza Digital
- Client challenge: {{client_main_challenge}}
- Services proposed: {{services}}
- Relevant results/experience: {{past_results_or_context}}

Write a "Why Riqueza Digital" section for a proposal that:
1. Opens with a positioning statement (1 sentence)
2. Lists 4–5 specific differentiators relevant to THIS client's situation
3. Includes 1–2 quantified results or relevant case study references
4. Ends with a confidence statement (not arrogant, but certain)

Do NOT use generic claims like "we are passionate" or "we work hard".
Focus on: specificity, relevance to their problem, and proof.
Length: 150–250 words.
```

---

### SEO & Content Prompts

**Blog Post Brief**
```
You are an SEO content strategist.

Create a detailed blog post brief for the following:
- Target keyword: {{primary_keyword}}
- Secondary keywords: {{secondary_keywords}}
- Audience: {{audience}}
- Funnel stage: {{awareness|consideration|decision}}
- Brand voice: {{voice_description}}
- Word count target: {{word_count}}
- Competitor URLs to differentiate from: {{competitor_urls}}

Brief should include:
1. Recommended title (H1) with keyword
2. Meta description (155 chars max)
3. Outline: H2s and H3s with brief description of each section
4. Key points to cover that competitors miss
5. Internal link suggestions
6. CTA recommendation

Output as a structured document ready for a writer.
```

---

## Prompt Storage Format

When saving prompts to a library (e.g., Notion), use this structure:

```
Prompt Name: [descriptive name]
Category: [Marketing / Client Ops / SEO / Admin]
Use case: [when to use this]
Variables required: [list {{variables}}]
Last tested: [date]
Notes: [any gotchas or tips]

---
[PROMPT TEXT]
---
```

---

## Prompt Quality Checklist

Before finalizing any reusable prompt:
- ✅ All changing elements are in {{variables}}
- ✅ Output format is specified
- ✅ Constraints are explicit (what NOT to do)
- ✅ Length/format expectations are set
- ✅ Tone is defined
- ✅ Tested with at least one real example mentally
- ✅ Saved with a descriptive name and category

---

## Agency Context (Riqueza Digital)

- **Source of truth**: store approved prompts in the repo under `shared/prompts/<categoria>/` (versioned with git, accessible to Kevin and Andrés). Example: the strategic onboarding pack lives in `shared/prompts/onboarding-estrategico/`
- Notion is optional, only as a visibility mirror — never the primary copy (política repo vs Notion, ver `ARQUITECTURA.md`)
- Tag prompts with the client type they work for (B2B / e-com / local / SaaS)
- Version control: when updating a prompt, keep the old version as "v1 (archived)"
- Share prompt library with contractors so output quality is consistent
- Language: most prompts should have a `{{Spanish|English}}` variable
