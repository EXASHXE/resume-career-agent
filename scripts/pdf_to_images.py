#!/usr/bin/env python3
from pathlib import Path
import argparse
def main():
    p=argparse.ArgumentParser(); p.add_argument("pdf"); p.add_argument("output_dir"); p.add_argument("--dpi",type=int,default=160); a=p.parse_args(); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    try:
        import fitz
    except ImportError as exc: raise SystemExit("Missing dependency: install `PyMuPDF` (`python -m pip install pymupdf`).") from exc
    doc=fitz.open(a.pdf); scale=a.dpi/72
    for i,page in enumerate(doc): page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).save(out/f"page-{i+1:02d}.png")
    print(f"Wrote {len(doc)} image(s) to {out}")
if __name__ == "__main__": main()
