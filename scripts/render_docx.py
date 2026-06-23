#!/usr/bin/env python3
"""Convert Markdown or HTML to DOCX using python-docx."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Ensure script directory is in sys.path for _utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import require_dependency


def main() -> None:
    p = argparse.ArgumentParser(description="Convert Markdown/HTML to DOCX.")
    p.add_argument("input", help="Path to input Markdown or HTML file")
    p.add_argument("output_docx", help="Path to output DOCX file")
    args = p.parse_args()

    docx_mod = require_dependency("docx", "install `python-docx` (`python -m pip install python-docx`)")

    src = Path(args.input)
    if not src.exists():
        print(f"Error: input file not found: {src}", file=sys.stderr)
        sys.exit(1)

    text = src.read_text(encoding="utf-8")
    if src.suffix.lower() in {".html", ".htm"}:
        text = re.sub(r"<[^>]+>", "\n", text)

    doc = docx_mod.Document()
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("### "):
            doc.add_heading(s[4:], level=3)
        elif s.startswith("## "):
            doc.add_heading(s[3:], level=2)
        elif s.startswith("# "):
            doc.add_heading(s[2:], level=1)
        elif re.match(r"^[-*] ", s):
            doc.add_paragraph(s[2:], style="List Bullet")
        else:
            doc.add_paragraph(s)

    out = Path(args.output_docx)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    print(f"DOCX rendered: {out}")


if __name__ == "__main__":
    main()
