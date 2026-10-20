# TDoc Metadata Reference

## TDoc Metadata Fields

When validating TDocs via portal page, parse these fields:

### Required Fields

- **title**: Document title
- **meeting**: The meeting identifier (e.g., "SA4#133")
- **contact**: Contact person
- **source**: Responsible organization
- **tdoc_type**: Document type classification
- **for**: Purpose (agreement, discussion, information, etc.)
- **agenda_item**: Associated agenda item (split into `agenda_item_nbr` and `agenda_item_title`)
- **status**: Document status

### Optional Fields

- **is_revision_of**: Reference to previous TDoc version (self-referencing FK)

### Metadata Parsing

1. **Ensure authenticated** with 3GPP portal before fetching
2. **Fetch portal page** with mode=view parameter
3. **Parse HTML** using BeautifulSoup
4. **Extract form fields** (labels and values)
5. **Handle agenda_item split**: Separate number and title
6. **Return dictionary** of key-value pairs

### Code Pattern

```python
from bs4 import BeautifulSoup


def parse_tdoc_metadata(html_content: str, tdoc_id: str) -> dict[str, str]:
    """Parse TDoc metadata from portal HTML page."""
    soup = BeautifulSoup(html_content, "html.parser")

    metadata = {}

    # Parse form fields (simplified example)
    for label in soup.find_all("label"):
        value_element = label.find_next_sibling("input")
        if value_element and value_element.get("value"):
            field_name = label.get_text().strip(": ").lower()
            metadata[field_name] = value_element.get("value")

    return metadata
```

A tested implementation with automatic authentication is available in the
`3gpp-portal-authentication` skill
(`PortalSession.get_tdoc_metadata`), which fetches the portal page with
`mode=view` and returns the same key-value dictionary.
