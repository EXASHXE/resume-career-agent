#!/usr/bin/env python3
"""Render HTML to PDF using Playwright first, then WeasyPrint."""
from pathlib import Path
import argparse
def main():
    p=argparse.ArgumentParser(); p.add_argument("input_html"); p.add_argument("output_pdf"); a=p.parse_args()
    src=Path(a.input_html).resolve(); out=Path(a.output_pdf).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser=pw.chromium.launch(); page=browser.new_page(); page.goto(src.as_uri(),wait_until="networkidle"); page.pdf(path=str(out),format="A4",print_background=True); browser.close()
        return
    except ImportError: pass
    except Exception as exc: print(f"Playwright failed: {exc}")
    try:
        from weasyprint import HTML
        HTML(filename=str(src)).write_pdf(str(out)); return
    except ImportError as exc:
        raise SystemExit("No PDF renderer installed. Install `playwright` then run `playwright install chromium`, or install `weasyprint` and its system libraries.") from exc
if __name__ == "__main__": main()
