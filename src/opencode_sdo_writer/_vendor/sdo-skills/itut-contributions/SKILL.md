---
name: itut-contributions
description: 'ITU-T contribution and TDoc submission procedures, deadlines, liaison statement format, and IPR requirements. Use when the agent needs to understand how to submit, format, or process ITU-T contributions (C-series documents), TDocs (Temporary Documents), or liaison statements. Covers submission deadlines, translation rules, patent/copyright declarations, and electronic posting. Sources: Rec. ITU-T A.1 (09/2019) clause 3.'
---

# ITU-T Contributions & TDoc Procedures

## Terminology guardrails (important)

- **Contribution (C-series meeting input):** regular pre-meeting submission
  by authorized members, subject to contribution deadlines.
- **Temporary Document (TD):** ITU-T internal working document category with
  distinct process and role expectations (e.g., chairman/rapporteur/editor
  workflows and meeting-time handling).

Do not assume `TD` in ITU-T is synonymous with generic "TDoc" usage in
other SDO contexts. In ITU-T workflows, treat `Contribution` and `TD` as
separate document types with different handling rules.

## Official template / portal sources

Local artifacts (preferred for reproducible/offline use):

- `../sdo-drafting/assets/itut/itu-t-sg12-contribution-template.docx`

Upstream source URLs (for refresh):

- Contribution template (example SG12):
  `https://www.itu.int/dms_pub/itu-t/oth/0A/0F/T0A0F00002F0012MSWE.docx`
- TD portal entry point:
  `https://www.itu.int/oth/T0A0F00000A/en`

Use the local Contribution template for regular pre-meeting submissions and
use the TD portal entry point for TD-specific workflow orientation under
chair/rapporteur/editor processes.

## Contribution submission

### Who submits

Member States and other duly authorized entities registered with a study group.

### Deadlines

| Timing | Effect |
|--------|--------|
| >= 2 months before meeting | May be translated; posted on web; printed copies on request at meeting |
| >= 12 calendar days, < 2 months | **Cannot be translated**; still accepted for meeting |
| < 12 calendar days | Not on agenda; not distributed; held for next meeting (exceptions: contributions of extreme importance at Director's discretion with meeting approval — e.g., urgent security vulnerabilities or regulatory deadlines requiring immediate action, as judged by the TSB Director) |

### Presentation

Must follow ITU-T A.2 clause 2 rules. TSB Director may return non-compliant documents.

### Web posting

Posted within 3 working days of receipt by TSB.

### Multiple study groups

Submit to the primary study group. For others, send a single summary sheet
(title, source, summary).

______________________________________________________________________

## TDocs (Temporary Documents)

Working documents produced during or between meetings.

### Content

- Extracts from other study group reports
- Chairman/rapporteur/drafting group reports
- Chairman proposals, compilations, ad hoc group reports
- Documents specifically requested by a meeting

### Submission deadlines

| Timing | Rule |
|--------|------|
| >= 7 calendar days before meeting | TDs posted within 3 working days of receipt |
| < 7 calendar days | Exception for: administrative docs, reports on events < 21 days before meeting, ad hoc group outputs, chairman compilations |
| Reports < 21 days before meeting | Posted >= 2 calendar days before discussion |

### Rapporteur TDoc requirement

Rapporteurs must submit each draft new or revised Recommendation as a
**separate TD** at least **six weeks** prior to the parent group's meeting.

______________________________________________________________________

## Liaison statements

Formal communication between ITU-T groups or with other SDOs.

### Required fields

| Field | Description |
|-------|-------------|
| Question(s) | Originating and destination Question numbers |
| Meeting, date | Where/when prepared |
| Study Group / Working Party | Originating group |
| Source | Group that prepared it |
| Title | Concise; if reply, make explicit ("Reply to liaison statement from...") |
| Destination | Group(s) or organization(s); indicate "For action/comment/information" per destination |
| If action | Deadline date |
| Approval level | SG, WP, or rapporteur group meeting |
| Contact | Name, organization, country, tel, e-mail |

### Format example

```text
Question(s):  4
Meeting, date: London, 2-6 October 2017
Study Group:  15         Working Party: 1
Source:       ITU-T SG15, Rapporteur group for Q4/15
Title:        LS/o/r on Object identifier registration
              - Reply to liaison statement from Q11/17
              (Geneva, 5-9 February 2017)

LIAISON STATEMENT

For action to:      ITU-T Q11/17
For information to: ITU-R SG11, ISO/IEC JTC 1/SC 6
Approval:           Q4/15 rapporteur group meeting (London, 6 October 2017)
Deadline:           22 January 2018
Contact:            John Jones, rapporteur for Q4/15
                    ABC Company, USA
                    Tel: +1 576 980 9987
                    E-mail: jj@abcco.com
```

______________________________________________________________________

## IPR and declarations

- **Patent disclosure**: Early disclosure encouraged. Use the Patent Statement
  and Licensing Declaration Form at <https://www.itu.int/ITU-T/ipr>.
- **General patent statement**: Voluntary blanket declaration covering all
  of an organization's contributions (alternative to per-Recommendation).
- **Copyright**: By submitting, contributors acknowledge no restrictions on
  normal distribution and possible use in resulting Recommendations.
- **Software copyright**: Must provide software copyright statement and
  licensing declaration to TSB at time of submission.
- **Normative references to external docs**: Source document must be clearly
  identified; procedures per ITU-T A.5 or A.25 apply.

______________________________________________________________________

## Translation

- Contributions >= 2 months before meeting: may be translated (TSB discretion)
- If study group works in original language: no translations
- Contributions received between 12 days and 2 months: cannot be translated

______________________________________________________________________

## References

- [references/a1-contributions-tdocs.md](references/a1-contributions-tdocs.md) -- detailed extract from Rec. ITU-T A.1 clause 3

## Cross-references

- `itut-reference` -- ITU-T organization, roles, terminology
- `itut-reference` -- Recommendation structure and approval
- `sdo-drafting` -- ITU-T contribution .docx template and formatting
- `sdo-ipr` -- patent policy, IPR disclosure, licensing declarations
- `sdo-project-setup` -- project bootstrap workflow
