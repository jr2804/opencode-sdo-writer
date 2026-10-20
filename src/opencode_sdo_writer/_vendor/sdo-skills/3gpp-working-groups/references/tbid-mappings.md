# TBID / SubTB Mapping Reference

## Working Group Identifiers

### TBID (Technical Body ID)

Each TSG has a unique `tbid` identifier used in 3GPP systems:

| TSG | tbid | FTP Root URL |
|------|------|--------------|
| RAN | 373 | <https://www.3gpp.org/ftp/tsg_ran/> |
| SA | 375 | <https://www.3gpp.org/ftp/tsg_sa/> |
| CT | 649 | <https://www.3gpp.org/ftp/tsg_ct/> |

### SubTB (Sub-Technical Body ID)

Each Working Group within a TSG has a unique `SubTB` identifier:

| TSG | WG | SubTB | Focus Area |
|------|-----|-------|-----------|
| RAN | RAN Plenary | 373 | TSG RAN overview |
| RAN | RAN1 | 379 | Radio Layer 1 (Physical layer) |
| RAN | RAN2 | 380 | Radio Layer 2/3 (Radio Resource Control) |
| RAN | RAN3 | 381 | UTRAN/E-UTRAN/NG-RAN architecture |
| RAN | RAN4 | 382 | Radio Performance and Protocol Aspects |
| RAN | RAN5 | 657 | Mobile terminal conformance testing |
| RAN | RAN6 | 843 | Radio Access Network (Legacy/Closed) |
| SA | SA Plenary | 375 | TSG SA overview |
| SA | SA1 | 384 | Services |
| SA | SA2 | 385 | System Architecture and Services |
| SA | SA3 | 386 | Security and Privacy |
| SA | SA4 | 387 | Multimedia Codecs, Systems and Services |
| SA | SA5 | 388 | Management, Orchestration and Charging |
| SA | SA6 | 825 | Application Enablement and Critical Communication Applications |
| CT | CT Plenary | 649 | TSG CT overview |
| CT | CT1 | 651 | User Equipment to Core Network protocols |
| CT | CT2 | 652 | Interworking with External Networks & Policy and Charging Control |
| CT | CT3 | 653 | Closed Group (was GERAN coordination) |
| CT | CT4 | 654 | Core Network Protocols |
| CT | CT5 | 655 | Core Network and Terminals (Architecture) |
| CT | CT6 | 656 | Smart Card Application Aspects |

The table above is the canonical mapping - keep exactly one copy of it.

## TSG Responsibilities

Each TSG is responsible for:

- Preparation of detailed time frame and management of each Release
- Proposal and approval of work items
- Technical coordination
- Maintenance of TSG voting list

## TSG Working Groups Details

### RAN (Radio Access Network) - tbid 373

**Responsibilities**: Radio access technologies like LTE and 5G NR

**Working Groups:**

- **RAN Plenary** (SubTB: 373): Overall TSG RAN coordination
- **RAN1** (SubTB: 379): Radio Layer 1 (Physical layer)
- **RAN2** (SubTB: 380): Radio Layer 2/3 (Radio Resource Control)
- **RAN3** (SubTB: 381): UTRAN/E-UTRAN/NG-RAN architecture
- **RAN4** (SubTB: 382): Radio Performance and Protocol Aspects
- **RAN5** (SubTB: 657): Mobile terminal conformance testing
- **RAN6** (SubTB: 843): Radio Access Network (Legacy, closed group)

**FTP Structure:** see `references/ftp-structure.md`.

### SA (Service and System Aspects) - tbid 375

**Responsibilities**: Overall architecture, service requirements, system capabilities

**Working Groups:**

- **SA Plenary** (SubTB: 375): TSG SA coordination and overall technical work
- **SA1** (SubTB: 384): Services
- **SA2** (SubTB: 385): System Architecture and Services
- **SA3** (SubTB: 386): Security and Privacy
- **SA4** (SubTB: 387): Multimedia Codecs, Systems and Services
- **SA5** (SubTB: 388): Management, Orchestration and Charging
- **SA6** (SubTB: 825): Application Enablement and Critical Communication Applications

**FTP Structure:** see `references/ftp-structure.md`.

### CT (Core Network and Terminals) - tbid 649

**Responsibilities**: Core network protocols, interfaces, and user equipment

**Working Groups:**

- **CT Plenary** (SubTB: 649): TSG CT coordination
- **CT1** (SubTB: 651): User Equipment to Core Network protocols
- **CT2** (SubTB: 652): Interworking with External Networks & Policy and Charging Control
- **CT3** (SubTB: 653): Closed Group (was GERAN coordination)
- **CT4** (SubTB: 654): Core Network Protocols
- **CT5** (SubTB: 655): Core Network and Terminals (Architecture)
- **CT6** (SubTB: 656): Smart Card Application Aspects

**FTP Structure:** see `references/ftp-structure.md`.

## Usage in Code

### Normalizing Working Groups

When parsing CLI arguments or user input:

1. **Plenary Aliases** (short codes):

   - `RP` → `RAN` Plenary
   - `SP` → `SA` Plenary
   - `CP` → `CT` Plenary

2. **Subgroup Codes**:

   - Use canonical codes: `R1`, `S4`, `C1`, etc. (not `RAN1`, `SA4`, `C1`)
   - For CLI parameters, normalize `SA4` → `S4`, `RAN1` → `R1`, `CT1` → `C1`

3. **TBID Mappings** (used in database):

   - RAN groups: tbid=373, SubTB: 373-389
   - SA groups: tbid=375, SubTB: 375-388
   - CT groups: tbid=649, SubTB: 649-656

### Code Example

```python
from tdoc_crawler.models import WorkingGroup


def normalize_meeting_code(code: str) -> str:
    """Normalize meeting codes to canonical format."""
    plenary_aliases = {"RP": "RAN", "SP": "SA", "CP": "CT"}
    upper = code.upper().strip()

    if upper in plenary_aliases:
        return plenary_aliases[upper]

    # Extract prefix for subgroups (R1, S4, C1, etc.)
    # Code example: "R1" → RAN group, subgroup RAN1
    return upper[0] if len(upper) > 1 else upper


def get_tbid_from_wg(wg: WorkingGroup) -> int:
    """Get TBID from WorkingGroup enum."""
    return wg.tbid
```
