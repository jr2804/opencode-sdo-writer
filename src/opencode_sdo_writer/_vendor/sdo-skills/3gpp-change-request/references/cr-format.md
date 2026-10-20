# CR Format Reference

Numbering, status codes, document structure and databases for 3GPP Change
Requests.

## CR Number Format

```text
<specnumber_no_dot>*_CR*<4-character_CR_number>*[r*<revision_number>*]
```

**Components:**

- `<specnumber_no_dot>`: Spec number without dot (e.g., `21.456` for TS 21.456)
- `*`: Literal asterisk
- `<4-character_CR_number>`: 4-digit CR number padded with leading zeros (e.g., `0095`)
- `[r*<revision_number>*]`: Lowercase 'r' + revision number (only for revised CRs)
- `<release>`: Release identifier (Rel-4, Rel-5, etc.)

**Examples:**

- Initial: `31.102_0095` - CR 0095 to spec 31.102
- First revision: `31.102_0095_r1` - Revision 1 of spec 31.102
- Mirror CR: `31.103_0095` - Mirrored CR to spec 31.103

## CR Status Meanings

| Status | TSG | WG | Meaning |
|---------|-----|----|--------|
| use | YES | YES | Valid for use |
| agreed | - | YES | WG agreed, forward to TSG |
| approved | YES | NO | Final decision (implemented) |
| rejected | YES | YES | Sustained objection |
| revised | YES | YES | Modified to new revision |
| merged | YES | YES | Combined with other CRs |
| postponed | YES | YES | Deferred to later date |
| endorsed | NO | YES | WG consensus, technically correct |
| withdrawn | YES | YES | Retracted before discussion |
| reissued | NO | NO | Recast unchanged in another TSG |
| noted | NO | NO | Deprecated (ambiguous term) |

## CR Categories

CRs are classified by category to indicate their nature:

- **Category F (Corrective)**: Corrective CRs, typically to earliest Release version
- **Category A (Mirror)**: Mirrors of CRs to previous Release versions
- **Mirror CRs require**: Same WI code per Release
- **Mirror CRs are marked**: Category A in spec history

### Category Definitions

| Category | Description |
|-----------|-------------|
| F | Corrective CRs applied to earliest Release version |
| A | Mirror CRs of same spec to different Release version |
| TEI | Technical Enhancement or Improvement |

## Step-by-Step Instructions

3GPP provides detailed step-by-step instructions for writing CRs:

- **URL**: <https://www.3gpp.org/specifications-technologies/specifications-by-series/change-requests-step-by-step>

**Key Sections:**

01. Header (meeting details, WG document number)
02. Spec number, CR number
03. CR revision number (for revised CRs only)
04. Current version
05. Title
06. Source to WG
07. Source to TSG
08. Work item code
09. Date
10. Category
11. Release
12. Consequences if not approved
13. Clauses affected
14. Other specs affected
15. Other comments
16. CR revision history
17. Filename convention
18. Body of CR
19. Other considerations

## CR Revision History

Optional field in CR document to track changes as CR passes through revisions:

- Revision 1: Initial CR
- Revision 2: First revision of CR
- Revision 3: Subsequent revisions

## File Naming Convention

**Word™ files for CRs** follow 3GPP naming:

```text
*<specnumber_no_dot>*_CR*<4-character_CR_number>*[r*<revision_number>*]
```

**Zip™ archive** containing CRs:

- Word™ files (CR cover sheet + body + attachments)
- Zip™ file named according to convention
- Contains multiple CRs packaged together for a TSG meeting

## CR Lifecycle

```text
Draft → WG Agreement → TSG Approval → MCC Incorporation → Published Spec
```

## Work Items

Each CR must be associated with a **Work Item (WI) code**:

- Obtained from official WI list: <https://www.3gpp.org/ftp/Specs/html-info/WI-List.htm>
- **Format**: 6-digit numeric code (e.g., `123456`)
- **Purpose**: Justifies the new feature or modification

## CR Database

### Netovate Search Tool

3GPP has an agreement with Netovate to provide a free CR database search:

- **URL**: <http://netovate.com/cr-search/>
- **Access**: Free web-based search tool
- **Features**: Search by spec number, CR number, or status

### 3GPP CR Database

Available on 3GPP FTP:

- **Directory**: `/ftp/Information/Databases/Change_Request/`
- **Format**: MS Access™ (.mdb) database
- **Access**: Direct download or via portal

### CR Status Tracking

Each spec maintains a history box listing all CRs that have been approved for that specification.

## Resources

- 3GPP Official: <https://www.3gpp.org/>
- 3GPP Portal: <https://portal.3gpp.org/>
- Step-by-step: <https://www.3gpp.org/specifications-technologies/specifications-by-series/change-requests-step-by-step>
- CR Database: /ftp/Information/Databases/Change_Request/
- WI List: <https://www.3gpp.org/ftp/Specs/html-info/WI-List.htm>
- Netovate: <http://netovate.com/cr-search/>
