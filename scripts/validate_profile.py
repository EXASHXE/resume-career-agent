#!/usr/bin/env python3
"""Validate a profile directory for required files and sections."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Metadata",
    "## One-line Summary",
    "## Problem / Context",
    "## Technical Challenges",
    "## Core Modules",
    "## Key Decisions / Trade-offs",
    "## Personal Contribution Candidates",
    "## Technologies",
    "## Keywords",
    "## Resume Bullets - zh-CN",
    "## Resume Bullets - en-US",
    "## Interview Pitch - zh-CN",
    "### 60 秒版",
    "### 3 分钟版",
    "## Interview Pitch - en-US",
    "### 60-second version",
    "### 3-minute version",
    "## Likely Interview Questions",
    "## Metrics To Confirm",
    "## Missing Information",
    "## Red Flags / Risks",
    "## Evidence Source",
]


def validate(profile_dir: Path) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    files_found: list[str] = []

    self_paths = list(profile_dir.glob("self_profile*"))
    resume_paths = list(profile_dir.glob("resume_base*"))
    projects_dir = profile_dir / "projects"

    if not self_paths:
        issues.append("Missing self_profile.md or self_profile.example.md")
    else:
        files_found.append(str(self_paths[0].relative_to(profile_dir.parent)))

    if not resume_paths:
        issues.append("Missing resume_base.md or resume_base.example.md")
    else:
        files_found.append(str(resume_paths[0].relative_to(profile_dir.parent)))

    if not projects_dir.is_dir():
        issues.append("Missing projects/ directory")
    else:
        project_files = sorted(projects_dir.glob("*.md"))
        if not project_files:
            issues.append("No project asset files in projects/")
        for pf in project_files:
            files_found.append(str(pf.relative_to(profile_dir.parent)))
            try:
                text = pf.read_text(encoding="utf-8")
            except Exception:
                issues.append(f"Cannot read {pf.name}")
                continue
            missing = [s for s in REQUIRED_SECTIONS if s not in text]
            if missing:
                issues.append(f"{pf.name}: missing sections: {', '.join(missing)}")
            if "- " not in text.split("## Resume Bullets - zh-CN", 1)[-1].split(
                "## Resume Bullets - en-US", 1
            )[0]:
                warnings.append(f"{pf.name}: zh-CN bullets section may be empty")
            if "- " not in text.split("## Resume Bullets - en-US", 1)[-1].split(
                "## Interview Pitch", 1
            )[0]:
                warnings.append(f"{pf.name}: en-US bullets section may be empty")
            if "## Metrics To Confirm" not in text:
                issues.append(f"{pf.name}: missing Metrics To Confirm")
            if "## Missing Information" not in text:
                issues.append(f"{pf.name}: missing Missing Information")

    return {
        "profile": str(profile_dir),
        "valid": len(issues) == 0,
        "files": sorted(files_found),
        "issues": issues,
        "warnings": warnings,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Validate a profile directory.")
    p.add_argument("profile_dir", help="Path to the profile directory")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    args = p.parse_args()
    result = validate(Path(args.profile_dir))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Profile: {result['profile']}")
        print(f"Valid: {result['valid']}")
        print(f"Files found: {len(result['files'])}")
        for f in result["files"]:
            print(f"  {f}")
        if result["issues"]:
            print(f"\nIssues ({len(result['issues'])}):")
            for i in result["issues"]:
                print(f"  - {i}")
        if result["warnings"]:
            print(f"\nWarnings ({len(result['warnings'])}):")
            for w in result["warnings"]:
                print(f"  - {w}")
        if result["valid"]:
            print("\nProfile is valid.")
        else:
            print(f"\nProfile has {len(result['issues'])} issue(s).")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
