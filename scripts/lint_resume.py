#!/usr/bin/env python3
"""Lint resume prose for weak language and missing evidence signals."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

WEAK_ZH = ["负责", "参与", "熟悉", "了解", "优化了", "提升了"]
WEAK_EN = [
    "responsible for", "helped with", "familiar with", "participated in",
    "assisted with", "worked on", "involved in",
]
FABRICATION_RISK = ["显著提升", "大幅降低", "极大改善", "彻底解决", "100%", "零故障"]


def lint(text: str) -> list[dict]:
    warnings = []
    text_lower = text.lower()
    for n, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        for word in WEAK_ZH:
            if word in line:
                warnings.append({
                    "line": n, "code": "weak-expression",
                    "message": f"弱表达\"{word}\"：改为可验证的动作、产物和边界。",
                })
        for word in WEAK_EN:
            if word in text_lower and word in line.lower():
                warnings.append({
                    "line": n, "code": "weak-expression-en",
                    "message": f"Weak expression \"{word}\": replace with action verb and artifact.",
                })
        for word in FABRICATION_RISK:
            if word in line:
                warnings.append({
                    "line": n, "code": "fabrication-risk",
                    "message": f"绝对化表述\"{word}\"：若无精确对照实验和基线和时间窗证据，标记 TODO。",
                })
        if re.match(r"^\s*[-*]", line):
            if not re.search(r"\d|\[.+待补", line):
                warnings.append({
                    "line": n, "code": "missing-metric",
                    "message": "bullet 缺少数字或明确的指标待补占位符。",
                })
            if not re.search(
                r"设计|实现|构建|开发|定位|解决|交付|验证|主导|协作|"
                r"built|designed|implemented|developed|delivered|resolved|"
                r"contributed|integrated|optimized|automated|migrated",
                line, re.I,
            ):
                warnings.append({
                    "line": n, "code": "missing-contribution",
                    "message": "个人动作或贡献边界不清。",
                })
            if len(stripped) < 24:
                warnings.append({
                    "line": n, "code": "thin-bullet",
                    "message": "bullet 可能缺少问题背景、工程产物或结果。",
                })
    if not re.search(r"项目|project|experience|经历", text, re.I):
        warnings.append({
            "line": 0, "code": "missing-context",
            "message": "未发现项目/经历章节，可能缺少背景。",
        })
    return warnings


def main() -> None:
    p = argparse.ArgumentParser(description="Lint resume for weak language and missing evidence.")
    p.add_argument("resume", help="Path to resume file (Markdown)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.add_argument("--fail-on-warning", action="store_true", help="Exit 1 if any warnings found")
    args = p.parse_args()

    text = Path(args.resume).read_text(encoding="utf-8")
    ws = lint(text)

    if args.json:
        print(json.dumps(ws, ensure_ascii=False, indent=2))
    else:
        for w in ws:
            print(f"WARNING {w['code']} line {w['line']}: {w['message']}")
        print(f"{len(ws)} warning(s)")

    if args.fail_on_warning and ws:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
