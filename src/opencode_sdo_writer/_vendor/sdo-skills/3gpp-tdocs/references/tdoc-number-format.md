# TDoc Number Format Reference

## TDoc Allocation

Every TDoc is always allocated to a specific 3GPP meeting.

## TDoc Number Format

### Pattern

**Regex Pattern:**

```python
TDOC_PATTERN = re.compile(r"([RSC][1-6P].{4,10})\.(zip|txt|pdf)", re.IGNORECASE)
```

The same pattern is implemented and tested in `scripts/tdoc_pattern.py`
(`TDOC_PATTERN`, `is_valid_tdoc()`, `parse_tdoc()`).

### Breakdown

| Part | Pattern | Description |
|-------|---------|-------------|
| **1st char** | `[RSC]` | Working group: R (RAN), S (SA), C (CT) |
| **2nd char** | `[1-6P]` | Subgroup: 1-6 for WGs, or P for Plenary |
| **3rd part** | `.{4,10}` | 4-10 identifier characters |
| **Extension** | `\.(zip|txt|pdf)` | Required file extension |

### Examples that Match

**Standard format:**

- `R1-2301234.zip` - RAN1 TDoc
- `S4-251209.txt` - SA4 TDoc
- `C1-2345678.pdf` - CT1 TDoc

**Plenary format:**

- `RP-230045.txt` - RAN Plenary TDoc
- `SP-240001.zip` - SA Plenary TDoc
- `CP-123456.zip` - CT Plenary TDoc

**Ad-hoc format:**

- `S4aA220001.zip` - SA4 ad-hoc meeting
- `R1eE230045.txt` - RAN1 ad-hoc meeting

**Case variations:**

- `r1-2301234.ZIP` - Case-insensitive matching
- `S4-251209.TXT` - Case-insensitive matching

### Examples that Don't Match

**Wrong working group:**

- `T1-2300456.zip` - T is invalid (use C for CT)
- `X1-2300456.zip` - X is invalid (use R, S, or C)

**Wrong subgroup:**

- `R7-2300456.zip` - Subgroup 7 doesn't exist (1-6 only)
- `R1-12.zip` - Only 2 characters after R1 (need 4-10)
- `R1-12345678901.zip` - 11 characters, exceeds maximum of 10

**Wrong extension:**

- `R1-2301234.doc` - Invalid extension (must be .zip, .txt, or .pdf)
- `R1-2301234` - Missing extension

**Not a TDoc:**

- `README.txt` - Not a TDoc
- `data.csv` - Not a TDoc
- `agenda.zip` - Administrative file, not a TDoc

## TDoc ID Normalization

Always normalize TDoc IDs to uppercase for case-insensitive matching and database lookups:

```python
def normalize_tdoc_id(tdoc_id: str) -> str:
    """Normalize TDoc ID to uppercase for case-insensitive lookup."""
    return tdoc_id.upper().strip()
```

The tested implementation lives in `scripts/tdoc_pattern.py` ->
`normalize_tdoc_id`.

### Example

```python
# User input (any case)
tdoc_id = "r1-2301234"

# Normalized for database/storage
normalized_id = normalize_tdoc_id("r1-2301234")  # Returns "R1-2301234"
```

## Working Group Inference

Infer working group from TDoc ID first character:

| First Char | Working Group |
|-----------|---------------|
| R | RAN |
| S | SA |
| C | CT |

```python
def infer_working_group_from_tdoc(tdoc_id: str) -> str | None:
    """Infer working group from TDoc ID."""
    mapping = {"R": "RAN", "S": "SA", "C": "CT"}
    return mapping.get(tdoc_id[0].upper(), None)
```

See also `scripts/tdoc_pattern.py` ->
`infer_working_group_from_tdoc`.
