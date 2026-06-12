---
name: notion-workspace
description: >
  Design, structure, and build Notion workspaces for digital agencies and their clients — including client portals,
  project management systems, SOPs, and internal operations databases.
  Use this skill whenever the user mentions: Notion setup, Notion workspace, client portal in Notion, Notion database,
  Notion template, Notion structure, "set up Notion for my client", "organize my Notion", "Notion for my agency",
  "create a Notion page for X", "build a client hub", or any request to design or improve a Notion-based system.
  Always use this skill — Notion setups require specific database design, relational linking, and UX decisions
  that go beyond basic page creation.
---

# Notion Workspace Skill

Design and build Notion systems that agencies and clients actually use — clean, navigable, and built to scale.

## Workflow

1. **Identify use case**: internal agency / client portal / project management / SOP library / CRM
2. **Map the entities**: what are the main databases needed?
3. **Design the structure**: pages, databases, relations, views
4. **Define properties** for each database
5. **Output the setup plan** with exact database/property specs
6. **Build or guide** the Notion setup step by step

---

## Core Workspace Types

### 1. Agency Internal Workspace (Riqueza Digital)
```
🏠 Home (dashboard)
├── 📋 Projects (database)
├── 👥 Clients (database)
├── 📅 Calendar (linked view from Projects)
├── 🧠 Knowledge Base
│   ├── SOPs
│   ├── Templates
│   └── Resources
├── 🔧 Gestión Interna
│   ├── Finances
│   ├── Team / Contractors
│   └── 20% Time / Innovation
└── 📊 Reporting Hub
```

### 2. Client Portal (shared with client)
```
[CLIENT NAME] Portal
├── 📌 Overview (status, KPIs, links)
├── 📁 Projects
│   ├── Active tasks (shared view, filtered)
│   └── Completed
├── 📊 Monthly Reports (gallery or list)
├── 📞 Meeting Notes
├── 🗂️ Assets & Deliverables (docs, files)
└── 📬 Requests & Feedback
```

### 3. Content Calendar Workspace
```
Content Hub
├── 📅 Calendar (database, calendar view)
├── 📝 Posts (main database)
│   ├── Views: By platform / By status / By pillar
│   └── Properties: Platform, Pillar, Status, Publish Date, Copy, Assets
├── 🎯 Content Pillars (reference)
└── ✅ Approval Queue (filtered view: Status = "Pending Review")
```

### 4. SOP Library
```
SOPs
├── 📌 Index (table with category, owner, last updated)
├── 🔁 Onboarding
├── 📈 Marketing Ops
├── 🛠️ Technical / Automations
├── 👤 HR / Contractors
└── 📋 Client Management
```

---

## Database Design Guide

### Projects Database
| Property | Type | Notes |
|---|---|---|
| Name | Title | Project name |
| Client | Relation → Clients | Link to client record |
| Status | Select | Not started / Active / Review / Complete / Paused |
| Type | Select | Retainer / Project / Internal |
| Start Date | Date | |
| Due Date | Date | |
| Owner | Person | |
| Priority | Select | High / Medium / Low |
| Budget | Number | Monthly or project total |
| Tags | Multi-select | SEO, Ads, Email, Dev, etc. |

### Clients Database
| Property | Type | Notes |
|---|---|---|
| Name | Title | Company name |
| Status | Select | Lead / Active / Paused / Churned |
| Contact | Text | Main contact name |
| Email | Email | |
| Phone | Phone | |
| Retainer | Number | Monthly value |
| Start Date | Date | |
| Industry | Select | |
| Projects | Relation → Projects | Backlink |
| Notes | Text | |

### Tasks Database (linked to Projects)
| Property | Type | Notes |
|---|---|---|
| Task | Title | |
| Project | Relation → Projects | |
| Assignee | Person | |
| Status | Select | To do / In progress / Blocked / Done |
| Due Date | Date | |
| Priority | Select | |
| Type | Select | Deliverable / Internal / Review |

---

## Views to Create

For most databases, create these standard views:

1. **Table** (default) — full data, for editing
2. **Board** (grouped by Status) — visual workflow
3. **Calendar** (by Due Date) — timeline visibility
4. **Gallery** (for content/assets) — visual browsing
5. **Filtered view per client** — "Client = [Name]" filter for client portals

---

## Notion Best Practices

### Navigation
- Use emoji consistently for visual scanning
- Keep homepage as a dashboard with linked views, not raw databases
- "Hub" pages aggregate views; "Databases" store data
- Avoid deeply nested pages — max 3 levels

### Database relations
- Always create both directions (Clients ↔ Projects)
- Use rollups to surface child data in parent (e.g., count of active tasks in project)
- Formulas: use for calculated fields (days until due, total retainer value, etc.)

### Permissions (client portals)
- Share database with filtered view (hide internal notes, budget, etc.)
- Use "Can view" for clients; "Can edit" only for task status if you want them to update
- Duplicate workspace before giving client access — test permissions first

### Templates
- Create a "New Client Onboarding" template page that auto-populates standard tasks
- Create "Monthly Report" template with pre-filled sections
- Templates live in the database, activated via the "+ New" button

---

## Output Format

When designing a workspace, always output:

```
## Notion Workspace Design — [Client/Purpose]

### Structure Overview
[Indented tree showing all pages and databases]

### Databases

#### [Database Name]
| Property | Type | Options/Notes |
|---|---|---|
| ... | ... | ... |

**Views to create**: [list]
**Key filters**: [list]

### Relations
- [Database A] ↔ [Database B]: [relationship description]

### First 5 pages to build (in order):
1. [Page name + brief description]
2. ...

### Setup notes:
- [Any important decisions or caveats]
```

---

## Agency Context (Riqueza Digital)

- **Política repo vs Notion**: RD tiene un split aprobado de source-of-truth por tipo de información (ver `ARQUITECTURA.md`). Lo ejecutable y versionable vive en el repo; CRM, tareas y colaboración viven en Notion. No dupliques información entre ambos.
- **Bases existentes**: ya hay una DB de Tareas (estados: Backlog / Por hacer / Revisar / Hecho) y una DB "Contenido a grabar" — extiende las existentes antes de crear nuevas
- **Client portals**: always set up before kickoff call — it signals professionalism
- **Internal workspace**: keep client data in a dedicated "Clients" section, not mixed with internal ops
- **Handoff**: when offboarding a client, export their portal to PDF and deliver as final package
- **Automation**: connect Notion databases to n8n for task creation, status updates, and report delivery
- **Language**: Spanish by default for internal workspace; match client's preference for portals
