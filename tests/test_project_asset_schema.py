from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "example_distributed_system.md",
    "example_agent_platform.md",
    "example_backend_platform.md",
]
PROJECTS_DIR = ROOT / "resources/profiles/example/projects"

SECTIONS = [
    "## Metadata", "## One-line Summary", "## Problem / Context",
    "## Technical Challenges", "## Architecture", "## Core Modules",
    "## Key Decisions / Trade-offs", "## Personal Contribution Candidates",
    "## Technologies", "## Keywords",
    "## Resume Bullets - zh-CN", "## Resume Bullets - en-US",
    "## Interview Pitch - zh-CN", "### 60 秒版", "### 3 分钟版",
    "## Interview Pitch - en-US", "### 60-second version", "### 3-minute version",
    "## Likely Interview Questions", "## Metrics To Confirm",
    "## Missing Information", "## Red Flags / Risks", "## Evidence Source",
]


def test_assets_follow_schema():
    for name in FILES:
        text = (PROJECTS_DIR / name).read_text(encoding="utf-8")
        assert all(section in text for section in SECTIONS), name


def test_zh_bullets_not_empty():
    for name in FILES:
        text = (PROJECTS_DIR / name).read_text(encoding="utf-8")
        zh_start = text.split("## Resume Bullets - zh-CN", 1)[1]
        zh_content = zh_start.split("## Resume Bullets - en-US", 1)[0]
        assert "- " in zh_content, f"{name}: zh-CN bullets empty"


def test_en_bullets_not_empty():
    for name in FILES:
        text = (PROJECTS_DIR / name).read_text(encoding="utf-8")
        en_start = text.split("## Resume Bullets - en-US", 1)[1]
        en_content = en_start.split("## Interview Pitch", 1)[0]
        assert "- " in en_content, f"{name}: en-US bullets empty"
