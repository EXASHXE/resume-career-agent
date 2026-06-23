from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_core_structure():
    required = [
        "README.md", "SKILL.md", "LICENSE",
        "agents/openai.yaml", "agents/codex.yaml",
        "agents/claude-code.yaml", "agents/opencode.yaml",
    ]
    required += [
        f"references/{x}" for x in [
            "audit-checklist.md", "red-flags.md", "narrative-tools.md",
            "jd-keyword-map.md", "ats-checklist.md", "one-page-resume.md",
            "tech-resume-rubric.md", "ai-infra-resume-rubric.md",
            "agent-engineer-resume-rubric.md", "cloudops-resume-rubric.md",
            "backend-platform-resume-rubric.md",
            "interview-question-bank.md", "bilingual-style-guide.md",
            "no-fabrication-policy.md",
            "privacy-policy.md", "output-quality-gate.md",
        ]
    ]
    required += [
        f"templates/{x}" for x in [
            "resume_zh_tech.html", "resume_en_tech.html",
            "resume_zh_markdown.md", "resume_en_markdown.md",
            "cover_letter_zh.md", "cover_letter_en.md",
            "recruiter_message_zh.md", "recruiter_message_en.md",
            "pitch_script_bilingual.md", "jd_match_report.md",
            "resume_audit_report.md", "changes_plan.md",
            "project_asset.md", "self_profile.md", "resume_base.md",
            "missing_info_checklist.md", "interview_prep_pack.md",
        ]
    ]
    required += [
        f"scripts/{x}" for x in [
            "privacy_guard.py", "init_private_profile.py",
            "validate_profile.py", "extract_jd_keywords.py",
            "score_project_match.py", "lint_resume.py",
            "render_pdf.py", "pdf_page_count.py", "pdf_to_images.py",
            "render_docx.py", "package_skill.py", "smoke_check.py",
            "_utils.py",
        ]
    ]
    required += [
        f"configs/{x}" for x in [
            "jd_keywords.json", "lint_rules.json",
            "privacy_rules.json", "profile_schema.json",
        ]
    ]
    assert not [p for p in required if not (ROOT / p).is_file()]


def test_no_default_profile():
    assert not (ROOT / "resources/profiles/default").exists()


def test_example_profile_exists():
    assert (ROOT / "resources/profiles/example/self_profile.example.md").exists()
    assert (ROOT / "resources/profiles/example/resume_base.example.md").exists()
    assert (ROOT / "resources/profiles/example/projects/example_distributed_system.md").exists()
    assert (ROOT / "resources/profiles/example/projects/example_agent_platform.md").exists()
    assert (ROOT / "resources/profiles/example/projects/example_backend_platform.md").exists()


def test_examples_exist():
    assert (ROOT / "examples/README.md").exists()
    assert (ROOT / "examples/jd_ai_infra.example.txt").exists()
    assert (ROOT / "examples/jd_agent_engineer.example.txt").exists()
    assert (ROOT / "examples/jd_cloudops_engineer.example.txt").exists()
    assert (ROOT / "examples/jd_backend_platform.example.txt").exists()
