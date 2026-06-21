#!/usr/bin/env python3
from pathlib import Path
import argparse
def main():
    p=argparse.ArgumentParser(); p.add_argument("pdf"); a=p.parse_args()
    try: from pypdf import PdfReader
    except ImportError as exc: raise SystemExit("Missing dependency: install `pypdf` (`python -m pip install pypdf`).") from exc
    print(len(PdfReader(str(Path(a.pdf))).pages))
if __name__ == "__main__": main()
