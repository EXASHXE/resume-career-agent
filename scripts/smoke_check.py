#!/usr/bin/env python3
"""Run all pre-push checks: privacy guard, validate example profile, keyword extraction, project scoring, resume linting."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

# Ensure script directory is in sys.path for _utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import get_root, read_file

ROOT = get_root()
EXAMPLE = ROOT / "resources/profiles/example"
EXAMPLE_JD = ROOT / "examples/jd_ai_infra.example.txt"


def _run_py_script(script: Path, *args: str) -> int:
    cmd = [sys.executable, str(script), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"  {'[PASS]' if result.returncode == 0 else '[FAIL]'} {script.name}")
    if result.returncode != 0:
        print(f"    stdout: {result.stdout.strip()[:200]}")
        if result.stderr.strip():
            print(f"    stderr: {result.stderr.strip()[:200]}")
    return result.returncode


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    print("=" * 60)
    print("  Smoke Check")
    print("=" * 60)

    failures = 0

    print("\n[1] Privacy Guard")
    failures += _run_py_script(ROOT / "scripts/privacy_guard.py")

    print("\n[2] Validate Example Profile")
    failures += _run_py_script(ROOT / "scripts/validate_profile.py", str(EXAMPLE))

    print("\n[3] Extract JD Keywords (AI Infra example)")
    mod = _load_module("extract", ROOT / "scripts/extract_jd_keywords.py")
    text = read_file(EXAMPLE_JD)
    data = mod.extract(text)
    if data.get("hard_skills"):
        print(f"  [PASS] extract_jd_keywords.py — {len(data['hard_skills'])} hard skills found")
    else:
        print("  [FAIL] extract_jd_keywords.py — no hard skills extracted")
        failures += 1

    print("\n[4] Score Project Match")
    mod2 = _load_module("score", ROOT / "scripts/score_project_match.py")
    results = mod2.score_projects(data, EXAMPLE / "projects")
    if results:
        top = results[0]
        print(f"  [PASS] score_project_match.py — top match: {top['project']} ({top['score']})")
    else:
        print("  [FAIL] score_project_match.py — no results")
        failures += 1

    print("\n[5] Lint Resume (test string)")
    mod3 = _load_module("lint", ROOT / "scripts/lint_resume.py")
    warnings = mod3.lint("## 项目经历\n- 负责项目，熟悉 Python，优化了系统")
    if warnings:
        print(f"  [PASS] lint_resume.py — {len(warnings)} warning(s) found (expected)")
    else:
        print("  [FAIL] lint_resume.py — no warnings for weak text")
        failures += 1

    print("\n[6] Package Skill (dry-run verify)")
    try:
        mod4 = _load_module("package", ROOT / "scripts/package_skill.py")
        if hasattr(mod4, "main") or hasattr(mod4, "create_zip"):
            print("  [PASS] package_skill.py — module loaded")
        else:
            print("  [PASS] package_skill.py — module loaded (no main/create_zip)")
    except Exception as e:
        print(f"  [FAIL] package_skill.py — {e}")
        failures += 1

    print("\n" + "=" * 60)
    if failures:
        print(f"  Smoke check FAILED — {failures} check(s) failed.")
    else:
        print("  Smoke check PASSED — all checks OK.")
    print("=" * 60)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
