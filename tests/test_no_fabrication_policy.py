from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_policy_and_skill_are_explicit():
    assert "禁止编造" in (ROOT / "references/no-fabrication-policy.md").read_text(encoding="utf-8")
    assert "Do not fabricate" in (ROOT / "SKILL.md").read_text(encoding="utf-8")


def test_assets_track_unknowns():
    for p in sorted((ROOT / "resources/profiles/example/projects").glob("*.md")):
        text = p.read_text(encoding="utf-8")
        assert "## Missing Information" in text, f"{p.name}: missing Missing Information"
        assert "## Metrics To Confirm" in text, f"{p.name}: missing Metrics To Confirm"


def test_templates_include_todos():
    templates = [
        "project_asset.md", "resume_zh_markdown.md", "resume_en_markdown.md",
        "resume_audit_report.md", "jd_match_report.md", "missing_info_checklist.md",
    ]
    # project_asset.md is a schema template — it uses field labels without {{}}.
    SCHEMA_TEMPLATES = {"project_asset.md"}
    for t in templates:
        path = ROOT / "templates" / t
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if t in SCHEMA_TEMPLATES:
                assert (
                    "## Metadata" in text
                    or "## Missing Information" in text
                ), f"{t}: missing required schema sections"
            else:
                assert (
                    "{{" in text
                    or "TODO" in text
                    or "待补" in text
                    or "[指标" in text
                ), f"{t}: no placeholder or TODO patterns found"


def test_privacy_policy_exists():
    privacy = ROOT / "references/privacy-policy.md"
    assert privacy.exists()
    content = privacy.read_text(encoding="utf-8")
    assert "never committed" in content.lower() or "never commit" in content.lower()


def test_output_quality_gate_exists():
    qg = ROOT / "references/output-quality-gate.md"
    assert qg.exists()
    content = qg.read_text(encoding="utf-8")
    assert "fabrication" in content.lower()
