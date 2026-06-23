#!/usr/bin/env python3
"""Deterministically extract normalized keywords from a JD (no LLM needed)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Ensure script directory is in sys.path for _utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import get_root, read_file, write_file, add_json_out_arg, output_json, load_config

# Load configuration from external JSON
_cfg = load_config("jd_keywords.json")
ALIASES = _cfg["aliases"]
SOFT = _cfg["soft"]
SENIORITY = _cfg["seniority"]
RISK_SIGNALS = _cfg["risk_signals"]
ROLE_PATTERNS = _cfg["role_patterns"]
DOMAIN_SET = set(_cfg["domain_set"])


def hits(text: str, mapping: dict[str, list[str]]) -> list[str]:
    low = text.lower()
    return [
        name
        for name, terms in mapping.items()
        if any(
            re.search(r"(?<![\w-])" + re.escape(t.lower()) + r"(?![\w-])", low)
            for t in terms
        )
    ]


def nearby_items(text: str, markers: list[str], limit: int = 240) -> list[str]:
    result = []
    for line in text.splitlines():
        low = line.lower()
        if any(m in low for m in markers):
            item = re.sub(r"^[\s*#\-\d.)]+", "", line).strip()
            if item and len(item) <= limit:
                result.append(item)
    return list(dict.fromkeys(result))


def extract(text: str) -> dict:
    role = ""
    for pattern in ROLE_PATTERNS:
        match = re.search(pattern, text, re.I | re.M)
        if match:
            role = match.group(1).strip(" -*#：:")
            break

    hard = hits(text, ALIASES)
    soft = hits(text, SOFT)
    domain = [x for x in hard if x in DOMAIN_SET]
    seniority = [s for s in SENIORITY if re.search(s, text, re.I)]
    risk = [r for r in RISK_SIGNALS if re.search(r, text, re.I)]

    return {
        "role_title": role,
        "hard_skills": hard,
        "soft_skills": soft,
        "domain_keywords": domain,
        "seniority_signals": seniority,
        "must_have": nearby_items(text, ["must", "required", "requirement", "必须", "任职要求"]),
        "nice_to_have": nearby_items(text, ["nice to have", "preferred", "plus", "加分", "优先"]),
        "risk_signals": risk,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Extract normalized keywords from a job description.")
    p.add_argument("jd", help="Path to JD file (text)")
    add_json_out_arg(p)
    args = p.parse_args()

    text = read_file(args.jd)
    data = extract(text)
    output_json(data, json_out=args.json_out)


if __name__ == "__main__":
    main()
