# Chapter 13: ETSI Drafting Rules (EDR)

**Adopted by the Director-General; version dated 30 June 2025.** Nine clauses plus Glossary, Acronyms and History. It specifies the **structure and drafting** of documents intended to become ETSI deliverables, complementing the Technical Working Procedures.

## Core Idea

Standards fail when they are ambiguous — they get implemented, translated and litigated. So the EDR's governing purpose is **clear and unambiguous provisions**, enforced through two mechanisms: **mandatory skeletons** from the editHelp! website (structure is not a matter of taste) and the **modal-verb regime** (`shall` / `should` / `may` / `can` / `will` / `is`), which tells every reader exactly which sentences are binding.

## Frameworks Introduced

- **Purpose and its place (preamble)**: the EDR specifies rules for the structure and drafting of documents intended to become ETSI deliverables, **complementing the TWP**. Examples in the text are illustrative only. ETSI maintains guides on templates and tools such as deliverable skeletons and *"Principles for drafting ETSI deliverables with the use of skeletons"*.
- **The mandatory skeleton rule (1.1)**: choose a deliverable type from the types defined in **TWP Annex A.3**, and use the **pre-structured deliverable skeleton** available from the **editHelp! website** as the basis for drafting.
  - Consequence: the EDR's structural clauses describe a skeleton you are obliged to use — not a style you may approximate.
- **The objective test (1.2)**: deliverables **shall**:
  - be as complete as necessary within the limits specified by their scope;
  - be **consistent, clear and accurate**;
  - provide a framework for future technological development;
  - be comprehensible to **qualified persons who have not participated in its preparation**;
  - respect the drafting rules.
  - Rationale: deliverables are meant to be implemented and translated, so misinterpretation produces faulty implementation.
- **Homogeneity across the whole corpus (1.3)**: uniformity of structure, style and terminology is required **not only within each deliverable but across all ETSI deliverables**. **The same term shall be used throughout** to designate a given concept — the use of a synonym for an already-defined concept **shall not** be used. The stated pay-off is twofold: comprehension, and **automated text processing**.
- **Consistency domains (1.4)**: text shall accord with the rules especially in standardized terminology, terminology principles and methods, **quantities, units and their symbols**, abbreviations, **table and figure numbering**, bibliographic references, and graphical symbols.
- **Language (1.5)**: **ETSI deliverables shall be in English only** (with further detail in the "Use of English" guide) — the definitive statement behind RoP Art. 17's publication rule.
- **Fitness for implementation (1.6)**: content shall be drawn up to facilitate **direct application and adoption without change** as a national, regional or international standard.
- **Planning and subdivision (1.7–1.8)**: planning follows TWP clause 1.6; when creating Work Items, consider whether the result is one or more deliverables, and where multiple related deliverables are planned, **define their structure and interrelationships at Work Item creation**. Subdivision of subject matter covers general rules, subdivision within a series of parts, and parts and sub-parts. Clause 1.9 covers the **legal master** of a deliverable, and 1.10 **neutrality and impartiality**.
- **The structure of a deliverable (2.0–2.16)** — with **numbered** and **unnumbered** clauses carefully distinguished:
  - **Arrangement (2.0)**: an overview of the major subdivisions and their arrangement (Table 1). Cover page (2.1), second page (2.2), table of contents and list of figures/tables (2.3).
  - **The IPR clause (2.4)**: the **"Intellectual Property Rights (IPR)" clause is the first unnumbered clause** — a **required informative** element. Its **entire text blocks are as given in the applicable skeleton and shall not be modified in any way**, and the **Secretariat is responsible for its final layout**.
  - **The Foreword (2.5)**: the **second unnumbered clause, on the same page as the IPR clause**; a **required informative** element that **shall not contain requirements, figures or tables**. It always carries a **general part provided by the Secretariat** (the designation and name of the Responsible Body that prepared the deliverable, and information on approval) and **optionally** a Responsible-Body part covering any of: other organizations that contributed; a statement than it cancels and replaces other documents in whole or in part; significant technical changes from the previous version; its relationship to other ETSI deliverables or documents; and the existence of an electronic attachment.
    - **Multi-part deliverables**: two options — (a) the first part's Foreword explains the intended series structure with each part listing known parts; (b) a specific **part 1** explains the intended structure together with the titles of all parts and sub-parts. **Option (b) is the preferred option.**
  - **Transposition table (2.5.1)**: **each EN shall contain a transposition table as the last element in the Foreword clause**, provided by the Secretariat.
  - **Modal verbs terminology clause (2.6)**: a **required informative element appearing after the Foreword**, **unnumbered**; its content — provided by the Secretariat — is as given in the skeleton and **shall not be modified**.
  - **Executive summary (2.7)**: **optional informative**, enabling readers to become acquainted with the whole document without reading it; **shall not contain requirements**; unnumbered; appears after the modal verbs clause and before the Introduction.
  - **Introduction (2.8)**: may give specific information or commentary on the technical content and the reasons prompting preparation.
  - **Scope (2.9) and References (2.10)**: references split into **normative references** (with rules on general treatment, **public availability**, specific and non-specific references, how to refer to them, and the **IPR policy for normative references**) and **informative references**, plus rules for **referring to EPP deliverables**.
  - **Definitions, abbreviations and symbols (2.11)**: general information, then terms, abbreviations and symbols separately.
  - **Clauses (2.12)**: general information, clause numbering (including **automatic clause numbering**), and paragraphs.
  - **Annexes (2.13)**: general information, then the distinction that matters everywhere in the Directives — **normative annexes (2.13.1)** versus **informative annexes (2.13.2)**.
  - **Bibliography (2.14), change history/change request (2.15), history (2.16).**
- **Requirements and the expression of provisions (3)** — the EDR's most consequential clause:
  - **The Requirements element (3.1) is optional.** If present it **shall** contain (a) all characteristics relevant to the aspects of the product(s), process(es) or service(s) covered, either explicitly or by reference, and (b) the **required limiting values of quantifiable characteristics**. A **clear distinction shall be made between requirements, statements and recommendations**. **Contractual requirements** — claims, guarantees, covering of expenses — **shall not be included**. Where the deliverable lists characteristics for which suppliers must state values that the deliverable itself does not specify, it **shall specify how such values are to be measured**.
  - **Verbal forms for the expression of provisions (3.2)** — seven tables, driven by one requirement: a user must be able to identify which provisions are **obligatory** in order to claim compliance.
    - **Requirement — `shall` / `shall not`**: to be followed strictly; **no deviation permitted**. *Do not use "must"* (except in direct citation); *do not use "may not" or "has not" instead of "shall not"* to express a prohibition.
    - **Recommendation — `should` / `should not`**: one option is recommended as particularly suitable without excluding others. Equivalent expressions (*it is recommended that*, *ought to*) only in exceptional cases — meaning where the verbal form would change the meaning or make the sentence hard to understand.
    - **Permission — `may` / `need not`**: what the deliverable permits (values, actions, support/use of features, presence or absence of options). *Do not use "possible"/"impossible" to express permission*, and **do not use "can" instead of "may"**: "may" signifies permission expressed by the standard, while "can" signifies possibility.
    - **Possibility and capability — `can` / `cannot`**: statements of possibility and capability, whether material, physical or causal. *Do not use "may" instead of "can"*. The deliberate contrast with Permission is the rule most often broken in practice.
    - **Inevitability — `will` / `will not`**: behaviour of equipment or sub-systems **outside the scope** of the deliverable in which they appear, where describing that behaviour is essential. Distinguish from `shall`/`shall not`.
    - **Fact — `is` / `is not`**: statements of fact, using any verb in the indicative mood, present tense. *Do not use the present indicative to express requirements.*
- **Legally protected material (4)**:
  - **General (4.1)**: the **IPR Policy and IPR Guide shall be respected**; use and reproduction of third parties' text, signs and protected material **should be avoided**; if, in exceptional circumstances, it cannot be avoided, **the IPR owner's authorisation shall be obtained**; **reference to the source and the owner shall always be provided**.
  - **Trade names and trademarks (4.2)**: their use **should be avoided**; instead use the correct **generic term**; if unavoidable, follow the editHelp! recommendations.
  - **Copyrights (4.3)**: copyright may attach to text, a figure, a photograph or source code; where use of a copyrighted work cannot be avoided, **its nature shall be indicated by the symbol ©**. **Referencing third-party material is preferred over reproducing it**; if reproduction cannot be avoided, the **Secretariat should be informed at the earliest possible stage of drafting** so authorisation can be obtained, and source and owner always referenced. For **software elements**, reproduction **shall be avoided** and otherwise requires the software owner's authorisation; for **open-source elements**, the **risk of contamination** of ETSI deliverables **shall be assessed before** introducing them. For **photographs** showing a person where personality rights are in doubt, a written confirmation is required.
- **Elements and layout (5–6)**: figures (usage, format, numbering, title layout, notes, references), tables (usage, notes), mathematical formulae (types, layout, numbering), lists, notes/examples and footnotes; then editorial rules on ETSI styles, capital letters, dimensions and tolerances, **quantities, units, symbols and signs**, representation of numbers and numerical values, **referencing the deliverable in its own text** (single, multi-part, elements of text), pagination, and numbering (page numbering/headers/footers, sequence numbering and bookmarking).
- **Specialised technical languages (7)**: common aspects, **SDL and MSC diagrams**, testing and test specifications.
- **Harmonised Standards (8)**: general directions; the **Foreword of a hEN**; **EMC statements**; normative references in a hEN; the **annex of a hEN**; and **the EN title in the official languages** (and its citation in the OJEU).
- **Endorsement of documents from other standards organizations (9)**: general information; the **endorsement notice**; **endorsement without modifications**; **endorsement with modifications**; the **annex in an endorsement document**; and **reproduction of text from other standards organizations** — general and copyright, inclusion without change, and inclusion with change.

## Key Concepts

- **Mandatory skeleton**: the pre-structured template that shall be used as the basis for any deliverable.
- **Unnumbered clauses**: the IPR clause, Foreword, Modal verbs terminology and Executive summary — the front matter that must not be renumbered.
- **Normative vs informative annexes**: carried through the EDR from the TWP's taxonomy.
- **Transposition table**: the mandatory element of every EN.
- **The modal-verb regime**: shall/should/may/can/will/is — the compliance vocabulary.
- **`may` vs `can`**: permission granted by the standard versus possibility in the world — the most frequently confused pair.
- **Legal master**: the single authoritative version of a deliverable.
- **Contamination risk**: the open-source assessment required before embedding software elements.
- **Generic term rule**: use the correct generic term instead of a trade name or trademark.

## Mental Models

- "**If it isn't `shall`, it isn't binding**" — the modal verb, not the tone, determines obligation.
- "**`may` is the standard talking; `can` is the world talking**" — permission versus possibility.
- "**Structure is prescribed, not negotiated**" — the skeleton from editHelp! is the starting point by rule.
- "**One concept, one term, everywhere**" — homogeneity is enforced across the entire corpus, not just within a document, so that machines can process it too.
- "**Reference rather than reproduce**" — third-party material is cited whenever possible, and embedding it triggers authorisation and early Secretariat involvement.
- "**Unnumbered means fixed**" — the front-matter clauses carry Secretariat-supplied, unmodifiable text.

## Anti-patterns

- **Writing "must" in a normative sentence**: only `shall` expresses a requirement; "must" is reserved for direct citation.
- **Using "may" for possibility or "can" for permission**: the two are deliberately distinguished and commonly confused.
- **Expressing a requirement with the present indicative**: "the terminal sends…" is a statement of fact (`is`), not a requirement (`shall`).
- **Rewriting the IPR clause or modal-verbs clause**: both are Secretariat-supplied, unnumbered and **shall not be modified**; the Secretariat owns the IPR clause's final layout.
- **Putting requirements, figures or tables in the Foreword**: expressly prohibited for that clause.
- **Omitting the transposition table from an EN**: it is mandatory and is the last element of the Foreword.
- **Reproducing third-party text, figures or trademarks instead of referencing them**: referencing is preferred; reproduction needs the owner's authorisation and early Secretariat involvement.
- **Dropping open-source code into a deliverable without assessing contamination**: the assessment is mandatory before introduction.
- **Drafting a non-English deliverable**: ETSI deliverables are English-only.
- **Treating an informative annex as binding (or vice versa)**: the EDR and TWP separate normative from informative annexes for good reason.

## Reference Tables

| Modal verb | Provision type | Meaning |
|---|---|---|
| `shall` / `shall not` | Requirement | strictly to be followed; no deviation permitted |
| `should` / `should not` | Recommendation | one option recommended without excluding others |
| `may` / `need not` | Permission | what the deliverable permits |
| `can` / `cannot` | Possibility / capability | what is materially, physically or causally possible |
| `will` / `will not` | Inevitability | behaviour of equipment outside the deliverable's scope |
| `is` / `is not` | Fact | statement of fact (indicative present) |

| Front-matter clause | Numbered? | Status | Author of text |
|---|---|---|---|
| Intellectual Property Rights (IPR) | no — first unnumbered | required, informative | skeleton; Secretariat owns layout |
| Foreword | no — second unnumbered | required, informative | general part: Secretariat; specific part: RB |
| Transposition table (in Foreword) | — | mandatory for every EN | Secretariat |
| Modal verbs terminology | no | required, informative | Secretariat; unmodifiable |
| Executive summary | no | optional, informative (no requirements) | RB |
| Introduction | no | optional | RB |

## Worked Example

**Writing one requirement correctly.** Suppose a terminal must send a TIMEOUT message on expiry of timer T3, and the network independently releases after a fixed period.

1. **The binding obligation** → `shall`: *"On expiry of timer T3, the terminal **shall** send a TIMEOUT message to the network and shall start timer T4."* Not "must send", not "sends".
2. **A merely suggested option** → `should`: if the deliverable prefers but does not compel an action, it says **should**, with "it is recommended that" only in an exceptional case.
3. **Something the deliverable permits** → `may`: *"The terminal **may** include an optional identifier field."* Never "can" here.
4. **A physical or causal possibility** → `can`: *"The timer **can** be implemented in hardware."* Never "may" here.
5. **Behaviour of equipment outside the deliverable's scope** → `will`: *"The network **will** release the connection after 30 s."* Distinguish from `shall`.
6. **A plain statement of fact** → `is`: *"Timer T3 **is** 5 s."* Never use the present indicative to impose a requirement.
7. **The legal overlay**: if the requirement quotes or embeds third-party material, reference it rather than reproduce it; if reproduction is unavoidable, seek the owner's authorisation and tell the Secretariat early (§4).

- Takeaway: each sentence's modal verb is a legal determination — the EDR turns drafting into a disciplined act, not a writing style.

## Key Takeaways

1. The EDR's purpose is clear, unambiguous provisions, achieved via mandatory editHelp! skeletons and the modal-verb regime.
2. **`shall` is the only requirement verb**; `should` recommends, `may` permits, `can` states possibility, `will` describes out-of-scope behaviour, `is` states fact.
3. The IPR clause, Foreword, modal verbs clause and Executive summary are **unnumbered**; the IPR and modal-verbs text is Secretariat-supplied and unmodifiable, and ENs must carry a **transposition table**.
4. ETSI deliverables are **English only**, and homogeneity of terminology is required **across the whole corpus** — partly for automated processing.
5. Legally protected material is to be avoided or referenced; reproduction needs authorisation, the **©** marking, and early Secretariat involvement; open-source elements need a **contamination-risk assessment** before introduction.
6. Normative versus informative annexes is a distinction the EDR enforces, matching the TWP's taxonomy.

## Connects To

- **Ch 11**: the EDR complements the TWP; deliverable types come from **TWP Annex A.3**, and the MAP gate requires EDR compliance before the Secretariat prepares a draft for member vote.
- **Ch 4**: §4.1 requires the IPR Policy and IPR Guide to be respected — the EDR is the drafting-level implementation of the IPR regime's notice and copyright obligations.
- **Ch 3**: RoP Art. 17 (languages and publication in English) is operationalized by EDR 1.5.
- **Ch 8**: harmonised standards (EDR 8) are the deliverables whose withdrawal Art. 21.6 covers, and whose citation in the OJEU carries legal effect.
- **Ch 12**: the IPR and copyright markings required by the EDR affect who may copy and distribute a deliverable.
