#!/usr/bin/env python3
from pathlib import Path
import argparse, re
def main():
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("output_docx"); a=p.parse_args()
    try: from docx import Document
    except ImportError as exc: raise SystemExit("Missing dependency: install `python-docx` (`python -m pip install python-docx`).") from exc
    src=Path(a.input); text=src.read_text(encoding="utf-8")
    if src.suffix.lower() in {".html",".htm"}: text=re.sub(r"<[^>]+>","\n",text)
    doc=Document()
    for line in text.splitlines():
        s=line.strip()
        if not s: continue
        if s.startswith("### "): doc.add_heading(s[4:],level=3)
        elif s.startswith("## "): doc.add_heading(s[3:],level=2)
        elif s.startswith("# "): doc.add_heading(s[2:],level=1)
        elif re.match(r"^[-*] ",s): doc.add_paragraph(s[2:],style="List Bullet")
        else: doc.add_paragraph(s)
    out=Path(a.output_docx); out.parent.mkdir(parents=True,exist_ok=True); doc.save(out)
if __name__ == "__main__": main()
