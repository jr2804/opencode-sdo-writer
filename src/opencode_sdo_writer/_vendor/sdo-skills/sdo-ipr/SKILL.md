---
name: sdo-ipr
description: 'Intellectual property rights in standards work: essential patents, disclosure duties, FRAND licensing, and the declaration forms of the individual standards bodies. Use when the agent needs to know what patent obligations apply to a contribution or a deliverable, how to disclose a patent, which licensing options exist, what a FRAND undertaking is, which clauses must not be modified, or how to answer a patent disclosure question at a meeting. Covers the ITU-T Common Patent Policy (RF / RAND / refusal, Patent Statement and Licensing Declaration Forms) and the ETSI IPR Policy (RoP Annex 6, essentiality test, Chairs duties).'
---

# IPR in Standards Work

Every standards body runs the same bargain: **disclose what you have, license
on fair terms, and do not block the standard**. The details differ per body,
so this skill gives the shared frame and points to the per-body rules.

## The shared frame

1. **Disclosure** -- a participant tells the body about a patent that may be
   essential to the work. Disclosure is normally best-effort: no patent
   search is required.
2. **Essentiality** -- whether a patent is *essential* is a technical
   question (is the invention unavoidable to implement the standard?), not a
   commercial one.
3. **Licensing commitment** -- the patent holder states under which terms it
   will license: free of charge, on RAND terms, or (in some bodies) refuses to
   license, in which case the standard must not depend on the patent.
4. **No interference** -- the body does not evaluate patent validity, does not
   define what "reasonable" means, does not mediate licensing negotiations
   and does not settle disputes.
5. **Meeting ritual** -- chairs open every meeting with a patent disclosure
   question; affirmative answers are recorded in the meeting report.

## Which body, which rule

| Body | Instrument | Where the rules are |
|------|-----------|---------------------|
| ITU-T | Common Patent Policy for ITU-T / ITU-R / ISO / IEC (2022) | [references/itut.md](references/itut.md), [references/itut-patent-policy.md](references/itut-patent-policy.md) |
| ETSI | IPR Policy (Rules of Procedure, Annex 6, normative) + Guide on IPR | [references/etsi.md](references/etsi.md) and `etsi-directives` (Ch 4) |
| 3GPP | 3GPP Working Procedures and the IPR policy of the 3GPP Partnership | not covered here -- check the current 3GPP Working Procedures |

## Drafting rules that hold everywhere

- Never invent licensing conditions: use only the options the body's form
  provides.
- Keep the body's IPR clause in the deliverable **unmodified** -- the skeleton
  carries it, and it is a protected clause.
- When a contribution proposes text that may require a patent to implement,
  say so at the meeting and file the declaration the body requires.
- If a patent is discovered after the deliverable was approved, the body's
  post-approval route applies (a new declaration, a revision, or a FRAND
  undertaking request).

## Cross-references

- `etsi-directives` -- the ETSI IPR Policy and the Chairs' duties (normative source)
- `itut-reference` -- ITU-T organisation and Recommendation structure
- `itut-contributions` -- contribution submission, including IPR declarations
- `etsi-governance` -- ETSI deliverables and their lifecycle
- `sdo-drafting` -- skeletons and protected clauses
