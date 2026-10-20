# Working Group FTP Structure & Meeting Codes

## Meeting Code Convention

### Meeting URL Pattern

3GPP meeting lists use dynamic pages at:

```text
https://www.3gpp.org/dynareport?code=Meetings-<ID>.htm
```

Where `<ID>` is a two-digit code:

- `RP` for RAN Plenary
- `SP` for SA Plenary
- `CP` for CT Plenary
- `R1-R6` for RAN1-RAN6 (e.g., R1, R2, etc.)
- `S1-S6` for SA1-SA6 (e.g., S1, S2, etc.)
- `C1-C6` for CT1-CT6 (e.g., C1, C2, etc.)

**Example URLs:**

- RAN meetings: `https://www.3gpp.org/dynareport?code=Meetings-RP.htm`
- SA4 meetings: `https://www.3gpp.org/dynareport?code=Meetings-S4.htm`
- CT3 meetings: `https://www.3gpp.org/dynareport?code=Meetings-C3.htm`

### Meeting Name Formats

Meeting names are **inconsistent** across years and groups:

- `SA4#134` - Standard SA4 format
- `SA4-e (AH) Audio SWG post 130` - Ad-hoc meeting
- `3GPPSA4-e (AH) Audio SWG post 130` - With 3GPP prefix
- `RAN1#98` - Standard RAN1 format
- `S4-133-e` - Alternative SA4 format

**Important**: Do NOT parse information from meeting names directly. Use database with proper `meeting_id` integer identifiers.

## Common Patterns

### Meeting ID Resolution

When resolving portal meeting names to database meeting IDs:

1. Try exact match (case-insensitive)
2. Try normalized name match
3. Try prefix/suffix matching (handle "3GPPSA4" vs "SA4")
4. Use Levenshtein distance for minor typos

**Avoid**: Substring matching (`%SA4%`) which matches fragments

### FTP Directory Names

FTP directory names on server do NOT match official WG names:

- `WG1_RL1` vs official "RAN1"
- `WG2_RL2` vs official "RAN2"
- `TSG_RAN` vs official "RAN Plenary"

**Use official codes** (tbid/SubTB) for database lookups.

## FTP Directory Structures

### RAN structure (`tsg_ran/`)

```text
tsg_ran/
├── WG1_RL1/
├── WG2_RL2/
├── WG3_RL3/
├── WG4_RL4/
├── WG5_RL5/
└── TSG_RAN/
```

### SA structure (`tsg_sa/`)

```text
tsg_sa/
├── WG1_S1/
├── WG2_S2/
├── WG3_S3/
├── WG4_S4/
├── WG5_S5/
├── WG6_S6/
└── TSG_SA/
```

### CT structure (`tsg_ct/`)

```text
tsg_ct/
├── WG1_C1/
├── WG2_C2/
├── WG3_C3/
├── WG4_C4/
├── WG5_C5/
├── WG6_C6/
└── TSG_CT/
```

## Meeting Table Structure

Each TSG meeting list page contains tables with:

- **Meeting column**: Short name (links to meeting details)
- **Files column**: Link to TDoc FTP directory (empty if not yet setup)
- **Dates column**: Start and end dates
- **Location column**: Physical location

**Critical**: If "Files" column is empty, skip that meeting for TDoc crawling.
