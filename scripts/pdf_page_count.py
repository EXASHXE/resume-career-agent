#!/usr/bin/env python3
"""Print the number of pages in a PDF file."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure script directory is in sys.path for _utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import require_dependency


def main() -> None:
    p = argparse.ArgumentParser(description="Print PDF page count.")
    p.add_argument("pdf", help="Path to PDF file")
    args = p.parse_args()

    pypdf = require_dependency("pypdf", "install `pypdf` (`python -m pip install pypdf`)")

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    reader = pypdf.PdfReader(str(pdf_path))
    print(len(reader.pages))


if __name__ == "__main__":
    main()
