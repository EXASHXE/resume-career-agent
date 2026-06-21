#!/usr/bin/env python3
"""Score Markdown project assets against extracted JD keywords without an LLM."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def tokens(value):
    if isinstance(value, list):
        value = " ".join(map(str, value))
    return set(re.findall(r"[a-z0-9+#.-]{2,}|[\u4e00-\u9fff]{2,}", str(value).lower()))


def score_projects(keywords: dict, project_dir: Path) -> list[dict]:
    hard = tokens(keywords.get("hard_skills", []))
    domain = tokens(keywords.get("domain_keywords", []))
    role = tokens(keywords.get("role_title", ""))
    must = tokens(keywords.get("must_have", []))
    nice = tokens(keywords.get("nice_to_have", []))
    wanted = hard | domain | role | must | nice

    results = []
    for path in sorted(project_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").lower()
        body = tokens(text)
        matched = sorted(wanted & body)
        missing = sorted(wanted - body)

        hard_hits = len(hard & body)
        domain_hits = len(domain & body)
        role_hits = len(role & body)
        must_hits = len(must & body)
        nice_hits = len(nice & body)

        raw = hard_hits * 4 + domain_hits * 5 + role_hits * 3 + must_hits * 2 + nice_hits * 1
        denom = max(1, len(hard) * 4 + len(domain) * 5 + len(role) * 3 + len(must) * 2 + len(nice) * 1)

        results.append({
            "project": path.stem,
            "score": round(100 * raw / denom, 2),
            "matched_keywords": matched,
            "missing_keywords": missing,
            "breakdown": {
                "hard_skill_hits": hard_hits,
                "domain_hits": domain_hits,
                "role_hits": role_hits,
                "must_have_hits": must_hits,
                "nice_to_have_hits": nice_hits,
            },
            "reasons": [
                f"Hard skills: {hard_hits}/{len(hard)}",
                f"Domain: {domain_hits}/{len(domain)}",
                f"Role: {role_hits}/{len(role)}",
                f"Must-have: {must_hits}/{len(must)}",
                f"Nice-to-have: {nice_hits}/{len(nice)}",
            ],
        })

    return sorted(results, key=lambda x: (-x["score"], x["project"]))


def main() -> None:
    p = argparse.ArgumentParser(description="Score project assets against JD keywords.")
    p.add_argument("keywords_json", help="Path to JD keywords JSON")
    p.add_argument("projects_dir", help="Path to projects directory")
    p.add_argument("-o", "--json-out", help="Write JSON output to file")
    p.add_argument("--json", action="store_true", help="Print as JSON to stdout")
    args = p.parse_args()

    data = json.loads(Path(args.keywords_json).read_text(encoding="utf-8"))
    result = score_projects(data, Path(args.projects_dir))
    payload = json.dumps(result, ensure_ascii=False, indent=2)

    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
