# Manual Retrieval Fallback

If the script fails, retrieve metadata manually:

1. **Find spec directory**: Browse to `https://www.etsi.org/deliver/etsi_<type>/`

   - Where `<type>` is `ts`, `es`, `eg`, `tr`, etc.

2. **Locate spec number** in the appropriate prefix range directory (e.g., `103000_103099/`)

3. **List version directories** (sorted alphabetically = chronological)

   - Latest version is last directory in list

4. **Download PDF** from version directory

   - Try common filename patterns

5. **Extract metadata** from PDF**:

   - Title: First page or PDF metadata
   - Date: PDF creation date (`/CreationDate` field)
