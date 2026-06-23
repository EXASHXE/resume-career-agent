#!/usr/bin/env python3
"""Convert PDF pages to PNG images using PyMuPDF."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure script directory is in sys.path for _utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import require_dependency


def main() -> None:
    p = argparse.ArgumentParser(description="Convert PDF pages to PNG images.")
    p.add_argument("pdf", help="Path to PDF file")
    p.add_argument("output_dir", help="Output directory for PNG images")
    p.add_argument("--dpi", type=int, default=160, help="Resolution in DPI (default: 160)")
    args = p.parse_args()

    fitz = require_dependency("fitz", "install `PyMuPDF` (`python -m pip install pymupdf`)")

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    scale = args.dpi / 72
    for i, page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False).save(
            out / f"page-{i + 1:02d}.png"
        )
    print(f"Wrote {len(doc)} image(s) to {out}")


if __name__ == "__main__":
    main()
