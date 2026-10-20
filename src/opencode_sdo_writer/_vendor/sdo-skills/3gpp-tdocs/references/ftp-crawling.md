# TDoc FTP/HTTP Crawling Reference

## TDoc FTP/HTTP Server Access

### Server Structure

3GPP maintains a file server at FTP-like HTTP URLs:

```text
https://www.3gpp.org/ftp/tsg_<working_group_identifier>/
```

### FTP Root URLs by Working Group

| Working Group | Identifier | FTP Root URL |
|--------------|-------------|------------|
| RAN | `ran` | `https://www.3gpp.org/ftp/tsg_ran/` |
| SA | `sa` | `https://www.3gpp.org/ftp/tsg_sa/` |
| CT | `ct` | `https://www.3gpp.org/ftp/tsg_ct/` |

### TDoc URL Pattern

TDocs are available at:

```text
https://www.3gpp.org/ftp/tsg_<wg>/<sub-working_group_identifier>/<meeting_identifier>/Docs/<tdoc_nbr>.zip
```

**URL Components:**

- `tsg_<wg>` - Working group root (e.g., `tsg_ran`, `tsg_sa`)
- `<sub-working_group_identifier>` - Arbitrary path name (NOT official subgroup ID)
- `<meeting_identifier>` - Arbitrary path name (NOT official meeting ID)
- `Docs/` - Typical subdirectory containing TDocs (case-insensitive)
- `<tdoc_nbr>` - TDoc filename stem
- `.zip` - File extension (99%+ of TDocs)

### Example URLs

```text
RAN WG1 TDoc R1-2301234:
https://www.3gpp.org/ftp/tsg_ran/WG1_RL1/RAN1_98/Docs/R1-2301234.zip

SA4 TDoc S4-251209:
https://www.3gpp.org/ftp/tsg_sa/WG4_S4/SA4_134/Docs/S4-251209.zip
```

**Important Notes:**

- Server uses HTTP protocol, not FTP (accessible via standard HTTP requests)
- `<sub-working_group_identifier>` and `<meeting_identifier>` are arbitrary path names, do NOT correspond to official IDs
- More than 99% of TDocs are `.zip` format
- Rare cases use `.pdf` or `.txt` extension

## TDoc Subdirectory Detection

### Problem

TDocs are typically stored in subdirectories like "Docs/" rather than directly in the base meeting directory.

### Detection Process

1. **Fetch base meeting directory** from `files_url`
2. **Parse HTML** to extract directory links
3. **Check for TDoc subdirectories** (case-insensitive matching)
4. **If subdirectories found**: Crawl each subdirectory
5. **If no subdirectories**: Crawl base directory directly

### TDoc Subdirectories

**Common subdirectory names** (case-insensitive matching):

- `Docs/`
- `Documents/`
- `Tdocs/`
- `TDocs/`
- `DOCS/`

### Excluded Directories

Non-TDoc directories to skip during crawling:

```text
EXCLUDED_DIRS = {"Inbox", "Draft", "Drafts", "Agenda", "Invitation", "Report"}
```

The same set is available as `EXCLUDED_DIRS` in `scripts/tdoc_pattern.py`,
together with `TDOC_SUBDIR_NAMES` (`docs`, `documents`, `tdocs`).

## TDoc Direct Links

### Portal TDoc View URL

When TDoc number is known, use 3GPP portal to query metadata:

```text
https://portal.3gpp.org/ngppapp/CreateTdoc.Aspx?mode=view&contributionUid=<tdoc_nbr>
```

**Example:**

```text
https://portal.3gpp.org/ngppapp/CreateTdoc.Aspx?mode=view&contributionUid=R1-2301234
```

## Usage in Code

### When Crawling TDocs

1. **Use TDOC_PATTERN** to match files in HTTP directory listings
2. **Extract TDoc ID** from filename stem using `group(1)` of regex match
3. **Store normalized ID** (uppercase) in database
4. **Build full HTTP URL** to TDoc file
5. **Validate via portal** if needed (uses `3gpp-portal-authentication` skill)

### Example Implementation

```python
import re
from bs4 import BeautifulSoup
import requests

from tdoc_pattern import TDOC_PATTERN

# Match TDoc file
for href in directory_links:
    match = TDOC_PATTERN.search(href)
    if match:
        tdoc_id = match.group(1).upper()
        full_url = base_url + match.group(0)

        # Later validate via portal
        metadata = fetch_tdoc_metadata(tdoc_id, credentials)
```
