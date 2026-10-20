# Specification FTP Directory Reference

Where 3GPP specification files live on the FTP server, how a TSG round
directory is organised, and how to find the files programmatically.

## FTP Directory Structure

### Root Directory

```text
https://www.3gpp.org/ftp/Specs/<YYYY>-<MM>/
```

**TSG Round Examples:**

- RAN#110: `https://www.3gpp.org/ftp/Specs/2025-12/`
- SA#110: `https://www.3gpp.org/ftp/Specs/2025-12/`
- CT#110: `https://www.3gpp.org/ftp/Specs/2025-12/SpecslistexTSG/TSG110.htm`

### Directory Contents

Each TSG round directory contains:

- HTML index pages (SpecslistexTSG/TSG#>.htm)
- Individual spec files (.doc, .zip)
- Delta directories for parallel releases (e.g., 21.101d)
- CR database and work item references

## Common Patterns

### Delta Directories

For parallel releases (e.g., Rel-4/5/6), 3GPP creates delta directories containing only changed specs.

**Purpose**: Reduce duplicate storage and make it easy to identify what's new in each release.

## Release Management

### MCC (Mobile Competence Centre)

The MCC aims to make all specs available following TSG round as soon as possible.

### Target Dates

- **Standard**: 4 weeks after TSG plenary
- **Extra time**: Additional week for large volumes or holiday periods

## Usage in Code

### Finding Spec Files

```python
import requests
from bs4 import BeautifulSoup

# FTP directory for Release 18
base_url = "https://www.3gpp.org/ftp/Specs/2018-12/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Parse all spec files
for link in soup.find_all("a", href=True):
    href = link.get("href")
    if href.endswith(".doc") or href.endswith(".zip"):
        print(f"Found spec: {href}")
```

Access is public over HTTPS; no authentication required.
