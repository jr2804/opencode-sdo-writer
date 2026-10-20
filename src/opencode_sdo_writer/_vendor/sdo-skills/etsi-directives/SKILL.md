---
name: etsi-directives
description: "Knowledge base from the ETSI Directives v53 (1 September 2026). Use when working with ETSI governance and procedures: which instrument governs a question, how ETSI decisions are voted (Weighted National/Individual Voting, quorum, majorities), membership and the General Assembly/Board/OCG/Finance Committee, how standards are approved (ENAP, SRdAP, MAP, EN/ES/TS/TR/GS), Work Items and the Technical Working Procedures, the ETSI IPR Policy and FRAND/essentiality, antitrust compliance in standards meetings, Codes of Conduct, the ETSI Drafting Rules and modal verbs, or the Financial Regulations."
---

<!-- argument-hint: [topic, instrument name, or chapter number] -->

# ETSI Directives — Version 53 (1 September 2026)

**Author**: ETSI (Institut Européen des Normes de Télécommunication) | **Pages**: 286 | **Instruments**: 17 + version history | **Chapters**: 13 | **Generated**: 2026-10-05

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `standstill`, `weighted national voting`, `FRAND`, `modal verbs`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch11`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### 1. The Directives are 17 instruments in one compilation (Ch 1)

Never cite "the Directives" — **name the instrument and its clause**; numbering restarts per instrument. Ask **who adopts it** before asking what it says, because the adopting body sets the change threshold:

| Adopted by | Instruments | Amendment route |
|---|---|---|
| Heads of National Delegations | Statutes; Rules of Procedure | **Specially Convened GA, ≥ 6 weeks' notice**; ≥ 75 % (Statutes) / ≥ 71 % (RoP) of total weighted votes |
| General Assembly | Values; Codes of Conduct; Delegated Powers; Financial Regulations; ToR of FC and GoSR | GA |
| Board | Board Working Procedures; ToR of OCG; **TWP\***; **IPR Guide\***; **Antitrust Guidelines\***; Honours | Board, or agreed at a GA meeting (\*) |
| Director-General | Information Policy; ETSI Drafting Rules | Director-General |

**Guides explain; Policies bind.** The Guide on IPR states the Policy "takes precedence in all cases"; the Information Policy is expressly non-normative.

### 2. Voting: subject matter picks the procedure (Ch 3, RoP Art. 11.2)

- **11.2.1 Weighted National Voting** (National Delegations, Annex 3 weights): dissolution; RoP disputes; **EN adoption/withdrawal**; Statutes/RoP amendments; new National Delegation weightings.
- **11.2.2 Weighted Individual — Full members**: Full-member rights/admonition/termination; **EU-regulatory documents**; EU standardization policies; EU-only Work Programme priorities.
- **11.2.3 Weighted Individual — Full + Associate**: **everything else (the default)**.
- **≥ 71 % of votes cast**; abstentions and non-votes are **excluded**; one vote per Academic/Corporate/Public Group (the last cast counts); a weighted vote **cannot be split** (Annex 7's Board elections excepted).
- **Quorum**: ≥ 40 % of Full-member weighted votes; **plus** ≥ 50 % of National-Delegation weight for 11.2.1. Proxy: written notice ≥ 17 h, max 3 per decision.
- **Consensus first** in all bodies; minority rights protected; secret ballot is the norm and never waivable for expulsions and officer elections.

### 3. Organs and membership (Ch 2–3)

- **Statutes**: ETSI is a French 1901-law non-profit association; **CEPT-area** establishment is required for **Full** membership; **Associate** and **Observer** cover other cases; admission runs on a **four-times-yearly Consensus poll** with dues at 100/75/50/25 %.
- **General Assembly** is the highest authority (38 enumerated powers); **Board** acts for it between meetings within **35 delegated powers**; **Director-General** holds chief executive authority and is the **only** person entitled to speak for the Institute publicly.
- Expulsion: **non-payment → Director-General**; other substantial breach → **General Assembly**, with registered-letter notice and an opportunity to be heard.

### 4. How a standard gets made (Ch 11, TWP)

- **A Work Item is the atom**: one responsible Technical Group, one named **Rapporteur**, ≥ 4 Full/Associate supporters, one deliverable per WI, and **the WI must be adopted before any final draft is approved**. A WI **shall be stopped after one year without progress**.
- **Body types**: **EP** (market sector, limited duration), **TC** (technical area, no term limit), **EPP** (external partners, approves its own deliverables, own legal status/budget), **ISG** (fast lane, GR/GS only, **no EC/EFTA-mandated work**), **SDG** (software, **no ETSI Deliverables**).
- **Approval routes**: **EN** → ENAP (NSOG vote, after Standstill + Public Enquiry) or **SRdAP** (NSBG, SReq-derived); **ES/EG** → **MAP** (all-member vote, **14 → 30 → 60 → 10 days**); **TS/TR** → **Technical Body adoption only**.
- Technical-group votes: Consensus first, then ≥ 71 % of votes cast — **if that fails, recalculate on Full members' votes alone**; no quorum, no proxy, no splitting.

### 5–9. IPR, antitrust, conduct, board and finance, drafting

The remaining frameworks are in [references/core-frameworks.md](references/core-frameworks.md):

- **5. The IPR regime is FRAND, not royalty-free (Ch 4)** — disclosure duties, essentiality test, FRAND undertakings, Chairs' Annex C duties.
- **6. Antitrust: a standards meeting is also a competitors' meeting (Ch 5)** — forbidden topics, the appearance principle, reporting duty.
- **7. Conduct and the opening ritual (Ch 6)** — ETSI Values, the seven principles, Chair and Board duties.
- **8. Board, finance and committees (Ch 7–10)** — quorum and voting, 21-day correspondence votes, inclusive budget, committee ToRs.
- **9. Drafting deliverables (Ch 13, EDR)** — modal verbs are the legal effect, skeleton mandate, protected clauses, transposition table.

---

## Chapter and Topic Index

[references/indexes.md](references/indexes.md) holds the full lookup tables: the
chapter index (13 chapters with their key frameworks) and the topic index
(~40 topics mapped to chapters, e.g. `standstill` → ch03, `FRAND` → ch04,
`Work Items` → ch11).

## Supporting Files

- [references/indexes.md](references/indexes.md) — chapter index and topic→chapter map
- [references/core-frameworks.md](references/core-frameworks.md) — frameworks 5–9 (IPR, antitrust, conduct, board/finance, drafting)
- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — procedures and design patterns
- [cheatsheet.md](cheatsheet.md) — thresholds, clocks, decision tables, tells
- [chapters/](chapters/) — one file per chapter of the Directives

---

## Scope & Limits

This skill covers the Directives v53 (1 September 2026) only. Two extraction limitations should be kept in mind: (1) the **Information Policy's** per-category access tables are presented as tables/images in the source and did not survive PDF text extraction — chapter 12 records its status, scope and cross-references but not the access tables; (2) large parts of the TWP's annexes and the EDR's editorial clauses (5–9) are summarised at framework level rather than in full — consult the source for exact wording before relying on it in a formal submission. For the operative text of any provision, read the source document. The source is ETSI's own governance compilation and carries ETSI's copyright; do not redistribute extracted content.
