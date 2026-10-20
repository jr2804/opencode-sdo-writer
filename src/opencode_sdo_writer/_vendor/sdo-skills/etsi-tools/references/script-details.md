# Script Details

How `scripts/get_etsi_spec.py` resolves a specification and where it
fails. The manual fallback lives in `manual-retrieval.md`.

## How It Works

The script retrieves ETSI specification metadata through these steps:

1. **Parse specification number** from various input formats, including document type (EN/ES/EG/TS/TR/SR/GS/GR/PAS) and optional part (-1, -2, etc.)

2. **Construct delivery directory URL** using ETSI's predictable structure:

   - Pattern: `https://www.etsi.org/deliver/etsi_<type>/<prefix>00_<prefix>99/<full_spec>/`
   - Example for TS 103 224: `https://www.etsi.org/deliver/etsi_ts/103200_103299/103224/`

3. **Scrape version directories** from delivery page

   - Format: `XX.YY.ZZ_AA` (major.minor.patch_release)
   - Example: `01.07.01_60` = version 1.7.1, release 60
   - Some specs may use different formats (e.g., no release code)

4. **Identify latest version** by sorting directories

5. **Construct PDF download URL** by trying common filename patterns:

   - `<type>_<spec>v<version_no_dots>p.pdf`
   - `<type>_<spec>v<version_no_dots>.pdf`
   - `<spec>v<version_no_dots>.pdf`
   - EG specs may use `.m.pdf` extension instead of `.p.pdf`

6. **Extract metadata from PDF**:

   - Parse PDF metadata for title and creation date
   - If title missing, extract from first page content

## Limitations

1. **Spec numbering**: Not all specification numbers exist or follow expected patterns. Some specs may be:

   - Withdrawn
   - Superseded by newer versions
   - Located in different directory structures
   - Have unique numbering schemes

2. **URL variations**: ETSI delivery URLs may vary by document type and series. The script tries common patterns but may not handle all cases.

3. **Parts detection**: Multi-part standards (e.g., ES 200 381-1, -2, -3) are detected from spec number but all parts must be queried separately for complete version history.

4. **EG specifications**: EG specs sometimes use different PDF file extensions (e.g., `.m.pdf` instead of `.p.pdf`).

5. **Multi-part spec directories**: Multi-part specifications like "EG 202 396-3" may use directory naming that differs from single-part specs. The script attempts to find the correct directory by:

   - Checking if the full spec number (including part) appears in directory names
   - For single-part specs, using standard 100-number range calculation

6. **Known issue with EG 202 396-3**: This specification exists at `https://www.etsi.org/deliver/etsi_eg/202300_202399/20239603/` but the script's range detection logic may not always identify the correct directory for multi-part EG specifications. Manual verification may be required for such cases.

## Manual Retrieval Fallback

If the script fails, retrieve metadata manually:

1. **Find spec directory**: Browse to `https://www.etsi.org/deliver/etsi_<type>/`

   - Where `<type>` is `ts`, `es`, `eg`, `tr`, etc.

2. **Locate spec number** in the appropriate prefix range directory (e.g., `103000_103099/`)

3. **List version directories** (sorted alphabetically = chronological)

   - Latest version is last directory in list

4. **Download PDF** from version directory

   - Try common filename patterns

5. **Extract metadata** from PDF:

   - Title: First page or PDF metadata
   - Date: PDF creation date (`/CreationDate` field)
