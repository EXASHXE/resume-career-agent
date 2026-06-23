#!/usr/bin/env python3
"""Lint resume prose for weak language and missing evidence signals."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Ensure script directory is in sys.path for _utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import read_file, add_json_arg, load_config

# Load configuration from external JSON
_cfg = load_config("lint_rules.json")
WEAK_ZH = _cfg["weak_zh"]
WEAK_EN = _cfg["weak_en"]
FABRICATION_RISK = _cfg["fabrication_risk"]
CONTRIBUTION_VERBS_ZH = _cfg["contribution_verbs_zh"]
CONTRIBUTION_VERBS_EN = _cfg["contribution_verbs_en"]
THIN_BULLET_THRESHOLD = _cfg["thin_bullet_threshold"]


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
                rf"{CONTRIBUTION_VERBS_ZH}|{CONTRIBUTION_VERBS_EN}",
                line, re.I,
            ):
                warnings.append({
                    "line": n, "code": "missing-contribution",
                    "message": "个人动作或贡献边界不清。",
                })
            if len(stripped) < THIN_BULLET_THRESHOLD:
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
    add_json_arg(p)
    p.add_argument("--fail-on-warning", action="store_true", help="Exit 1 if any warnings found")
    args = p.parse_args()

    text = read_file(args.resume)
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
