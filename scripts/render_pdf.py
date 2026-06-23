#!/usr/bin/env python3
"""Render HTML to PDF using Playwright first, then WeasyPrint."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure script directory is in sys.path for _utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import require_dependency


def main() -> None:
    p = argparse.ArgumentParser(description="Render HTML to PDF.")
    p.add_argument("input_html", help="Path to input HTML file")
    p.add_argument("output_pdf", help="Path to output PDF file")
    args = p.parse_args()

    src = Path(args.input_html).resolve()
    out = Path(args.output_pdf).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        print(f"Error: input file not found: {src}", file=sys.stderr)
        sys.exit(1)

    # Try Playwright first
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(src.as_uri(), wait_until="networkidle")
            page.pdf(path=str(out), format="A4", print_background=True)
            browser.close()
        print(f"PDF rendered: {out}")
        return
    except ImportError:
        pass
    except Exception as exc:
        print(f"Playwright failed: {exc}")

    # Fallback to WeasyPrint
    try:
        from weasyprint import HTML

        HTML(filename=str(src)).write_pdf(str(out))
        print(f"PDF rendered: {out}")
        return
    except ImportError as exc:
        raise SystemExit(
            "No PDF renderer installed. Install `playwright` then run "
            "`playwright install chromium`, or install `weasyprint` and its system libraries."
        ) from exc


if __name__ == "__main__":
    main()
