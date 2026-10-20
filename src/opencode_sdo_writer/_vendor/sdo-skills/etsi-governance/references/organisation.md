# ETSI Basics -- deliverable types and lifecycle

Extracted from: ETSI "A Guide to Writing World Class Standards" + ETSI Directives (EDR)

## ETSI organisation

ETSI (European Telecommunications Standards Institute) is one of three
European Standards Organizations (ESOs), alongside CEN and CENELEC.
ETSI produces globally recognized standards for information and
communications technologies (ICT).

## What is a standard?

A standard is a collection of the minimum requirements necessary for
something to:

- Co-exist and interoperate correctly with another
- Meet national and international regulations
- Operate safely without causing harm to people or equipment

### World class standard attributes

- Well-defined objectives responding to real needs in a timely manner
- Complete and accurate technical content
- Easy to understand and implement
- Clear and unambiguous requirements
- Validated
- Well-maintained

______________________________________________________________________

## ETSI deliverable types

| Type | Full name | Content | Approved by |
|------|-----------|---------|-------------|
| **TS** | Technical Specification | Normative | Responsible ETSI Technical Committee |
| **ES** | ETSI Standard | Normative | ETSI membership |
| **EN** | European Standard | Normative, transposed into national standards | TC + National Standards Organizations / National Delegations |
| **HS** | Harmonised Standard | Normative (special EN, EU mandate) | EN process + EC publication |
| **CS** | Community Specification | Normative (EN for civil aviation) | EN process |
| **TR** | Technical Report | Informative (preferred) | Responsible TC |
| **EG** | ETSI Guide | Informative (guidance for ETSI organisation) | ETSI membership |
| **SR** | Special Report | Informative (public reference) | Responsible TC |
| **GS** | Group Specification | Normative or informative | Responsible Industry Specification Group (ISG) |

### Key distinction

- **Normative** = prescriptive = tells how to comply with the standard
- **Informative** = descriptive = helps with conceptual understanding
- **Requirement** = the criteria to be fulfilled to comply with the standard
- **Provision** = collective term for requirements, recommendations, and
  permissible actions

### Choosing the right type

When deciding on a deliverable type with normative provisions, focus on
the stakeholders who will approve it. The approval process is more complex
and time-consuming for larger stakeholder groups (EN > ES > TS). Use TS
unless broader approval is necessary. TS requires approval by just the
Technical Committee that created it.

### Deliverable numbering

ETSI deliverable numbers consist of the type prefix + number:

- ETSI TS 123 456
- ETSI ES 201 999
- ETSI EN 300 356

Multi-part: ETSI ES 201 999-1, ETSI ES 201 999-2
Sub-parts: ETSI EN 300 356-33-10

______________________________________________________________________

## Standards development lifecycle

```text
Work Item -> Draft -> Validate & Review -> Editorial Check
    -> Approval -> Publication -> Maintenance & Evolution
                                          |
                                    Feedback loop
```

1. **Create Work Item**: Define scope, title, deliverable type, milestones,
   responsible committee/WG/rapporteur, validation plan
2. **Develop draft**: Structured approach; clear, unambiguous, complete,
   accurate requirements; use specialised notations (ASN.1, SDL, MSC)
3. **Validate**: Peer review, interoperability events, implementation
   feedback; test development, design guides
4. **Editorial check**: Submit to editHelp! Service (via Technical Officer);
   checks English, references, abbreviations, definitions; does NOT
   evaluate technical content
5. **Approve and publish**: Process differs per deliverable type; ETSI's
   web-based voting tools collect feedback
6. **Maintain and evolve**: On-going maintenance; correction of defects;
   alignment with related standards

### Work Item proposal considerations

- Is the document normative or informative?
- What type of deliverable (EN, ES, TS, etc.)?
- Title: concise indication of content
- Scope: intended contents
- Is it part of a Hierarchical Work Item?
- Realistic schedule of milestones
- Validation activities needed (test specs, conformance tests)?
- Who is responsible (committee, working group, rapporteur, STF)?

______________________________________________________________________

## Key roles

| Role | Description |
|------|-------------|
| **Technical Committee (TC)** | Responsible for developing and approving deliverables |
| **Working Group (WG)** | Subset of TC focused on specific topics |
| **Rapporteur** | Coordinates detailed study of a work item |
| **Industry Specification Group (ISG)** | Creates GS deliverables; lighter process |
| **Technical Officer** | Secretariat support; in-depth knowledge of rules and technology |
| **editHelp! Service** | Checks editing, English, references, abbreviations, definitions |
| **Specialist Task Force (STF)** | Funded experts for specific drafting tasks |

______________________________________________________________________

## Harmonised Standards

Harmonised Standards are ENs with special status, produced in response to
an EC mandate. They provide the technical detail to achieve the "essential
requirements" of an EU Directive. Manufacturers can claim a product's
compliance with the relevant Directive by conforming to the HS.

EG 201 399 provides guidance on writing Harmonised Standards.

## Community Specifications

ENs produced under the Single European Sky Interoperability Regulation
(civil aviation). Co-operation with EUROCAE. Acquire CS status when
published in the Official Journal of the EU.

## System Reference Documents (SRdoc)

A specific type of TR that provides technical, legal and economic
background to new radio systems/services/applications. Advises on need
for spectrum allocation or regulatory change.

______________________________________________________________________

## ETSI resources

- ETSI Portal: <https://portal.etsi.org/>
- editHelp!: <https://portal.etsi.org/edithelp/home.asp> (skeletons, templates)
- TEDDI (Terms and Definitions Database): <https://webapp.etsi.org/Teddi/>
- ETSI Directives: <https://portal.etsi.org/Resources/ETSIDirectives.aspx>
- Making Better Standards: <https://portal.etsi.org/mbs/>
- ETSI "Use of English" guide: <https://ocgwiki.etsi.org/index.php?title=Use_of_English>
