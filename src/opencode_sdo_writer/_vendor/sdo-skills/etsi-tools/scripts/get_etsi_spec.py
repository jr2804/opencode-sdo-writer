#!/usr/bin/env python3
# /// script
# dependencies = [
#   "PyPDF2",
#   "beautifulsoup4",
#   "requests",
# ]
# ///
"""
ETSI Specification Metadata Retrieval

Retrieves metadata for ETSI specifications including:
- Latest version
- Full title
- Release/publication date
- Download URL
- Version history

Supports all ETSI document types:
- EN (European Standard)
- ES (ETSI Standard)
- EG (ETSI Guide)
- TS (ETSI Technical Specification)
- TR (ETSI Technical Report)
- SR (ETSI Special Report)
- GS (ETSI Group Specification)
- GR (ETSI Group Report)
- PAS (Publicly Available Specification)

Usage:
    mise x uv -- uv run get_etsi_spec.py <spec-number>
    mise x uv -- uv run get_etsi_spec.py 103224
    mise x uv -- uv run get_etsi_spec.py 103 224
    mise x uv -- uv run get_etsi_spec.py "EG 202 396-3"
    mise x uv -- uv run get_etsi_spec.py "TR 103 907"
Example output:
    Spec: ETSI TS 103 224
    Latest version: V1.7.1
    Title: Speech and multimedia Transmission Quality (STQ); A sound field reproduction method...
    Publication date: 2025-11-20
    Download URL: https://www.etsi.org/deliver/etsi_ts/103200_103299/103224/01.07.01_60/ts_103224v010701p.pdf
"""

import io
import re
import sys
import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader


def main():
    """Main function to retrieve and display ETSI spec metadata."""
    if len(sys.argv) < 2:
        print("Usage: mise x uv -- uv run get_etsi_spec.py <spec-number>")
        print()
        print("Examples:")
        print("  mise x uv -- uv run get_etsi_spec.py 103224")
        print("  mise x uv -- uv run get_etsi_spec.py 103 224")
        print("  mise x uv -- uv run get_etsi_spec.py ETSI TS 103 224")
        print("  mise x uv -- uv run get_etsi_spec.py EG 202 396-3")
        print("  mise x uv -- uv run get_etsi_spec.py TR 103 907")
        print("  mise x uv -- uv run get_etsi_spec.py ES 200 381-1")
        sys.exit(1)

    spec_input = sys.argv[1]

    try:
        # Parse specification number
        spec_info = parse_spec_number(spec_input)

        # Format spec for display
        if spec_info["part"]:
            full_spec = (
                f"{spec_info['prefix']}{spec_info['number']}-{spec_info['part']}"
            )
        else:
            full_spec = f"{spec_info['prefix']}{spec_info['number']}"

        print(f"Searching for ETSI {spec_info['doc_type']} {full_spec}...")
        print()

        # Get directory URL
        directory_url = get_spec_directory_url(spec_info)
        print(f"Directory: {directory_url}")

        # Get version directories
        version_dirs = get_version_directories(directory_url, spec_info)

        if not version_dirs:
            print(
                f"Error: No versions found for ETSI {spec_info['doc_type']} {full_spec}"
            )
            print()
            print("Possible reasons:")
            print("  - Specification number does not exist")
            print("  - Different URL structure for this document type")
            print("  - Try checking: https://www.etsi.org/deliver/etsi_<type>/")
            sys.exit(1)

        # Get latest version
        latest_dir, latest_num, release_code = version_dirs[0]
        print(f"Latest version: {format_version(latest_num)} (release {release_code})")
        print()

        # Get PDF URL
        pdf_url = get_pdf_url(directory_url, latest_dir, spec_info)

        # Extract metadata from PDF
        print("Extracting metadata from PDF...")
        metadata = extract_pdf_metadata(pdf_url)

        # Display results
        print("=" * 70)
        print(f"SPECIFICATION: ETSI {spec_info['doc_type']} {full_spec}")
        print("=" * 70)
        print(f"Latest Version:  {format_version(latest_num)}")
        print(f"Release Code:    {release_code}")
        print(f"Directory:       {latest_dir}")

        if metadata.get("title"):
            print(f"Title:           {metadata['title']}")

        if metadata.get("publication_date"):
            pub_date = metadata["publication_date"]
            # Format as month name
            try:
                dt = datetime.strptime(pub_date, "%Y-%m-%d")
                pub_date_formatted = dt.strftime("%b %Y").lower()
            except:
                pub_date_formatted = pub_date
            print(f"Publication Date: {pub_date_formatted}")

        print(f"Download URL:    {pdf_url}")
        print("=" * 70)
        print()
        print(f"Full versions available: {len(version_dirs)}")
        if len(version_dirs) > 1:
            print("Version history:")
            for version_dir, version_num, release_code in version_dirs:
                pub_year = version_num.split(".")[0][:2]
                print(
                    f"  - {format_version(version_num)} (release {release_code}) ~ 20{pub_year}"
                )

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")

        traceback.print_exc()
        sys.exit(1)


def parse_spec_number(spec_input):
    """
    Parse specification number from various input formats.

    Accepts:
    - "103224" (six digits, defaults to TS)
    - "103 224" (three digits, space, three digits)
    - "ETSI TS 103 224" (prefix + three digits, space, three digits)
    - "EG 202 396-3" (document type + prefix + number + part)
    - "TR 103 907" (document type + six digits)
    - "ES 200 381-1" (document type + six digits + part)

    Returns:
        dict: {'doc_type': 'TS', 'prefix': '103', 'number': '224', 'part': None}
    """
    spec_input = spec_input.strip().upper()

    # Extract document type (EN, ES, EG, TS, TR, SR, GS, GR, PAS)
    doc_types = ["EN", "ES", "EG", "TS", "TR", "SR", "GS", "GR", "PAS"]
    doc_type = "TS"  # Default

    for dt in doc_types:
        if spec_input.startswith(f"ETSI {dt}"):
            doc_type = dt
            spec_input = spec_input.replace(f"ETSI {dt}", "").strip()
            break
        elif spec_input.startswith(dt):
            doc_type = dt
            spec_input = spec_input[len(dt) :].strip()
            break

    # Extract part number if present (e.g., "-3", "-1", "-2")
    part = None
    part_match = re.search(r"-(\d+)$", spec_input)
    if part_match:
        part = part_match.group(1)
        spec_input = spec_input[: -len(part_match.group(0))].strip()

    # Match pattern: three digits, space, three digits (e.g., "103 224")
    match = re.match(r"(\d{3})\s+(\d{3})", spec_input)
    if match:
        return {
            "doc_type": doc_type,
            "prefix": match.group(1),
            "number": match.group(2),
            "part": part,
        }

    # Match pattern: six digits (e.g., "103224")
    match = re.match(r"(\d{3})(\d{3})", spec_input)
    if match:
        return {
            "doc_type": doc_type,
            "prefix": match.group(1),
            "number": match.group(2),
            "part": part,
        }

    # Match pattern: two digits, space, three digits (e.g., "01 001")
    match = re.match(r"(\d{2})\s+(\d{3})", spec_input)
    if match:
        return {
            "doc_type": doc_type,
            "prefix": match.group(1),
            "number": match.group(2),
            "part": part,
        }

    raise ValueError(f"Invalid ETSI specification number: {spec_input}")


def get_spec_directory_url(spec_info):
    """
    Construct ETSI delivery directory URL for specification.

    For multi-part specs (e.g., EG 202 396-3), searches all range directories
    to find the one containing the spec.

    Args:
        spec_info: dict with 'doc_type', 'prefix', 'number', 'part'

    Returns:
        str: Directory URL
    """
    doc_type = spec_info["doc_type"].lower()
    prefix = spec_info["prefix"]
    number = spec_info["number"]

    # Format spec number with part if present
    if spec_info["part"]:
        full_spec = f"{prefix}{number}-{spec_info['part']}"
    else:
        full_spec = f"{prefix}{number}"

    # For multi-part specs, we need to search for the directory that contains the spec
    # First, construct the base URL for the document type
    base_url = f"https://www.etsi.org/deliver/etsi_{doc_type}/"

    try:
        # Get the directory listing to find the correct range
        response = requests.get(base_url, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Look for the directory containing our full spec number
            # For EG 202 396-3, we look for a directory named "20239603"
            for link in soup.find_all("a"):
                href = link.get("href", "")

                # Check if this is a directory link and contains our spec
                if full_spec in href and "dir" in href:
                    # Extract the directory path (without trailing slash)
                    dir_path = href.rstrip("/")
                    url = f"{base_url}{dir_path}"
                    return url

    except Exception:
        pass

    # Fallback: try to determine the range based on spec number (without part)
    # This is for single-part specs
    if spec_info["part"]:
        # For multi-part, use spec without part for range calculation
        dir_spec_num = int(f"{prefix}{number}")
    else:
        dir_spec_num = int(f"{prefix}{number}")

    # Determine the appropriate 100-number range
    if dir_spec_num < 100:
        range_suffix = "00_099"
    elif dir_spec_num < 200:
        range_suffix = "100_199"
    elif dir_spec_num < 300:
        range_suffix = "200_299"
    elif dir_spec_num < 400:
        range_suffix = "300_399"
    elif dir_spec_num < 500:
        range_suffix = "400_499"
    elif dir_spec_num < 600:
        range_suffix = "500_599"
    elif dir_spec_num < 700:
        range_suffix = "600_699"
    elif dir_spec_num < 800:
        range_suffix = "700_799"
    elif dir_spec_num < 900:
        range_suffix = "800_899"
    else:
        range_suffix = "900_999"

    url = f"https://www.etsi.org/deliver/etsi_{doc_type}/{prefix}{range_suffix}/{full_spec}/"
    return url


def get_version_directories(directory_url, spec_info):
    """
    Retrieve list of version directories from ETSI delivery page.

    Args:
        directory_url: URL of spec directory
        spec_info: dict with spec details

    Returns:
        list of tuples: [(version_name, version_number, release_date), ...]
        sorted by version number (descending)
    """
    response = requests.get(directory_url, timeout=30)

    # 404 means spec doesn't exist or different URL structure
    if response.status_code == 404:
        return []

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    version_dirs = []

    # Find all links that look like version directories
    # Format: 01.07.01_60/ (major.minor.patch_release)
    for link in soup.find_all("a"):
        href = link.get("href", "")

        # Match version directory pattern: XX.YY.ZZ_AA or XX.YY.ZZ
        match = re.search(r"(\d{2}\.\d{2}\.\d{2}(?:_\d{2})?", href)
        if match:
            version_dir = match.group(1)

            # Extract version components
            parts = version_dir.split("_")
            version_num = parts[0]  # e.g., 01.07.01
            release_code = parts[1] if len(parts) > 1 else "00"  # e.g., 60

            version_dirs.append((version_dir, version_num, release_code))

    # Sort by version number (descending)
    version_dirs.sort(key=lambda x: x[1], reverse=True)

    return version_dirs


def get_pdf_url(directory_url, version_dir, spec_info):
    """
    Construct PDF download URL for specific version.

    Args:
        directory_url: Base directory URL
        version_dir: Version directory (e.g., "01.07.01_60")
        spec_info: dict with spec details

    Returns:
        str: PDF URL
    """
    doc_type = spec_info["doc_type"].lower()

    # Format spec number with part if present
    if spec_info["part"]:
        full_spec = f"{spec_info['prefix']}{spec_info['number']}-{spec_info['part']}"
    else:
        full_spec = f"{spec_info['prefix']}{spec_info['number']}"

    # Construct version directory URL
    version_url = f"{directory_url.rstrip('/')}/{version_dir}/"

    # PDF filename pattern varies by document type
    # TS/EN/ES/TR: ts_<spec_number>v<version_no_dots>p.pdf or en_<spec>v<version_no_dots>.pdf
    # EG/SR/GS/GR: often just a spec name with version

    version_num = version_dir.split("_")[0]
    version_no_dots = version_num.replace(".", "")

    # Try common filename patterns
    possible_filenames = [
        f"{doc_type}_{full_spec}v{version_no_dots}p.pdf",
        f"{doc_type}_{full_spec}v{version_no_dots}.pdf",
        f"{full_spec}v{version_no_dots}.pdf",
        f"{full_spec}v{version_no_dots}p.pdf",
    ]

    for filename in possible_filenames:
        pdf_url = f"{version_url}{filename}"
        # Check if PDF exists
        test_response = requests.head(pdf_url, timeout=10)
        if test_response.status_code == 200:
            return pdf_url

    raise ValueError(f"Could not find PDF file in {version_url}")


def extract_pdf_metadata(pdf_url):
    """
    Extract metadata from PDF document.

    Args:
        pdf_url: URL of PDF document

    Returns:
        dict: Metadata including title, publication date
    """
    response = requests.get(pdf_url, timeout=30)
    response.raise_for_status()

    pdf_file = io.BytesIO(response.content)
    reader = PdfReader(pdf_file)

    metadata = {}

    # Get PDF metadata
    if reader.metadata:
        metadata["title"] = reader.metadata.get("/Title", "")
        metadata["creation_date"] = reader.metadata.get("/CreationDate", "")

    # If title not in metadata, try to extract from first page
    if not metadata.get("title"):
        first_page = reader.pages[0]
        text = first_page.extract_text()

        # ETSI specs typically have title on first page
        # Look for pattern: "ETSI XXX YYY" or similar
        lines = text.split("\n")
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            if line and len(line) > 20:  # Reasonable title length
                # Skip lines with only special characters
                if not re.match(r"^[^\w\s]+$", line):
                    metadata["title"] = line
                    break

    # Parse publication date from metadata
    if metadata.get("creation_date"):
        # ETSI date format: D:YYYYMMDDHHmmSS+HH'mm'
        match = re.search(r"D:(\d{4})(\d{2})(\d{2})", metadata["creation_date"])
        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            metadata["publication_date"] = f"{year}-{month}-{day}"

    return metadata


def format_version(version_num):
    """
    Convert ETSI version number to human-readable format.

    Args:
        version_num: Version like "01.07.01"

    Returns:
        str: Formatted version like "V1.7.1"
    """
    parts = version_num.split(".")
    if len(parts) >= 3:
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2])
        return f"V{major}.{minor}.{patch}"
    return version_num


if __name__ == "__main__":
    main()
