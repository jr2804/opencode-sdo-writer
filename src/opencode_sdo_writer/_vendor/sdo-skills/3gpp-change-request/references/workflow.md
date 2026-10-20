# Change Request Workflow

Quick reference for CR submission and approval process.

## CR Lifecycle

```text
Draft → WG Agreement → TSG Approval → MCC Incorporation → Published Spec
```

### 1. Draft CR

Member organization creates CR document containing:

- **CR Cover Sheet**: Why change is needed, summary of modifications
- **Attached Spec Sections**: Word "Track Changes" showing affected text
- **Summary of Changes**: Brief explanation

### 2. Submit to WG

- Any 3GPP member can propose CR to responsible Working Group
- WG discusses and agrees CR is valid and required

### 3. WG Presents to TSG

- WG presents CR at TSG plenary for final approval
- Status changes from "agreed" to pending TSG decision

### 4. TSG Approval

- TSG approves CR (status becomes "approved")
- CR becomes formal decision

### 5. MCC Incorporates

- 3GPP Support Team (MCC) incorporates CR into new spec version
- Target: 4 weeks after TSG plenary

### 6. Publish

- New spec version becomes available on FTP server

## CR Development and Approval

### Submission Process

1. **WG Level**: Any 3GPP member organization can propose a CR to the Working Group responsible for the spec
2. **WG Agreement**: WG discusses and agrees CR is valid and required
3. **TSG Approval**: WG presents CR to parent TSG plenary for final approval
4. **MCC Incorporation**: After TSG approval, 3GPP Support Team (MCC) incorporates CR into new spec version

## Why CRs Are Needed

| Reason | When |
| ------ | ---- |
| Add new feature | Release still under development |
| Correct/clarify/enhance | Existing feature, Release still open |
| Fix error | Spec is functionally frozen |

## CR Categories

| Category | Description |
| -------- | ----------- |
| F | Corrective - applied to earliest Release version |
| A | Mirror - same CR to different Release version |
| TEI | Technical Enhancement or Improvement |

Full category definitions, including the per-Release F and A wording:
`references/cr-format.md`.

## CR Number Format

```text
<specnumber_no_dot>_CR<4-digit_number>[r<revision>]
```

**Examples:**

- `31102_CR0095` - CR 0095 to spec 31.102
- `31102_CR0095r1` - Revision 1 of that CR
- `31103_CR0095` - Mirror CR to spec 31.103

Full component breakdown, revision suffix rules and additional examples:
`references/cr-format.md`.

## Quick Checklist

Essential fields for CR submission:

- [ ] Work Item code (from [WI List](https://www.3gpp.org/ftp/Specs/html-info/WI-List.htm))
- [ ] Spec number and current version
- [ ] Target Release (one only)
- [ ] Category (F, A, or TEI)
- [ ] Source to WG
- [ ] Title and reason for change
- [ ] Clauses affected
- [ ] Date (yyyy-MM-dd format)

## Common Pitfalls

1. **Wrong Release**: Can't use Rel-6 WI code for Rel-4 spec
2. **Missing mirrors**: Need separate CR for each Release if spec is in multiple
3. **Out-of-date base**: Writing CR against old version that's been updated
4. **Wrong category**: Use TEI for enhancements, F for corrections

## See Also

- [SKILL.md](SKILL.md) - Full CR reference with status codes and detailed fields
- `references/cr-format.md` - CR number format, status table, categories, document sections, WI codes, databases
- `references/cr-checklist.md` - Submission checklist, common pitfalls, best practices, mirror CR concepts
- `3gpp-specifications` - Spec numbering and structure
- `3gpp-releases` - Release freeze concepts
