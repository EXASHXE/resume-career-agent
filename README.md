# resume-career-agent

A privacy-safe, profile-driven resume and career skill for technical roles. Supports resume audit, JD tailoring, project narrative, ATS optimization, bilingual resume drafting, cover letters, recruiter messages, and interview preparation.

## What This Is

- A **generic skill** that any agent can load to help with technical resume writing.
- A **privacy-first** system where your real data stays local and never enters the repository.
- A **deterministic toolchain** with Python scripts for keyword extraction, project scoring, resume linting, and format rendering.
- A **multi-role rubric system** covering AI Infra, Agent Engineer, CloudOps, Backend/Platform, and general tech roles.

## What This Is Not

- A resume builder with a web UI.
- A place to store your real resume or profile — that stays on your local machine.
- A replacement for your own judgment — it flags issues and suggests rewrites, but you make the final call.
- A tool that fabricates experience or metrics to make you look better.

## Privacy Model

**Real profiles are local-only.** This repository contains only sanitized fictional examples.

```
resources/profiles/example/       ← committed (fictional template)
resources/profiles/my-profile/    ← gitignored (your real data)
```

Your real profile data is:
- Never committed to this repository
- Never shipped in the distributed skill zip
- Only accessible when you explicitly point the agent to your local profile directory

Run `python scripts/privacy_guard.py` before every commit. If you accidentally commit private data, follow the remediation steps in `references/privacy-policy.md`.

## Directory Structure

```
resume-career-agent/
  SKILL.md                  # Agent-operable manual (the main file agents read)
  README.md                 # This file — installation and usage
  LICENSE                   # MIT

  agents/                   # Agent-platform specific metadata
    openai.yaml, codex.yaml, claude-code.yaml, opencode.yaml

  references/               # Rubrics, checklists, and methodology
    audit-checklist.md, red-flags.md, narrative-tools.md
    jd-keyword-map.md, ats-checklist.md, one-page-resume.md
    tech-resume-rubric.md, ai-infra-resume-rubric.md
    agent-engineer-resume-rubric.md, cloudops-resume-rubric.md
    backend-platform-resume-rubric.md, interview-question-bank.md
    bilingual-style-guide.md, no-fabrication-policy.md
    privacy-policy.md, output-quality-gate.md

  templates/                # Output templates — what agents produce
    resume_zh_markdown.md, resume_en_markdown.md
    resume_zh_tech.html, resume_en_tech.html
    cover_letter_zh.md, cover_letter_en.md
    recruiter_message_zh.md, recruiter_message_en.md
    pitch_script_bilingual.md, jd_match_report.md
    resume_audit_report.md, changes_plan.md
    project_asset.md, self_profile.md, resume_base.md
    missing_info_checklist.md, interview_prep_pack.md

  scripts/                  # Deterministic Python tools
    privacy_guard.py        # Scan for privacy violations
    init_private_profile.py # Create local gitignored profile
    validate_profile.py     # Check profile completeness
    extract_jd_keywords.py  # Extract keywords from JD text
    score_project_match.py  # Score projects against JD keywords
    lint_resume.py          # Find weak expressions and missing evidence
    render_pdf.py           # HTML → PDF
    pdf_page_count.py       # Count PDF pages
    pdf_to_images.py        # PDF → PNG for visual review
    render_docx.py          # Markdown/HTML → DOCX
    package_skill.py        # Package skill into zip for distribution
    smoke_check.py          # Run all pre-push checks

  resources/profiles/       # Profile data (only example/ is committed)
    example/                # Sanitized fictional example
      self_profile.example.md
      resume_base.example.md
      projects/
        example_distributed_system.md
        example_agent_platform.md
        example_backend_platform.md

  examples/                 # Example JDs and usage guides
    jd_ai_infra.example.txt, jd_agent_engineer.example.txt
    jd_cloudops_engineer.example.txt, jd_backend_platform.example.txt
    usage_resume_audit.md, usage_jd_tailor.md
    usage_interview_prep.md, usage_private_profile.md

  tests/                    # Pytest test suite

  .github/workflows/        # CI pipeline
    test.yml
```

## Installation

Copy the entire `resume-career-agent/` directory into your agent's skills directory.

### Codex

```bash
cp -r resume-career-agent ~/.codex/skills/
```

### Claude Code

```bash
cp -r resume-career-agent ~/.claude/skills/
```

### OpenCode

```bash
cp -r resume-career-agent ~/.config/opencode/skills/
```

### Generic Agent / Custom Skill Folder

Copy the directory to wherever your agent loads skills from. Ensure `SKILL.md` is at the root of the installed folder.

The agent discovers the skill via `SKILL.md`'s frontmatter and the metadata files in `agents/`.

## Create a Private Profile

```bash
# Recommended: use the init script
python scripts/init_private_profile.py --name my-profile

# Manual: copy the example
cp -r resources/profiles/example resources/profiles/my-profile
```

Then edit each file under `resources/profiles/my-profile/` with your real information.

Validate your profile:
```bash
python scripts/validate_profile.py resources/profiles/my-profile
```

The `my-profile/` directory is automatically gitignored. **Do not commit it.**

## Use with an Agent

Once installed, the agent loads this skill automatically when you ask about resume-related tasks.

Typical prompts:
- "Audit my resume against my profile."
- "Tailor my resume for this JD: [paste JD]."
- "Generate a 60-second project pitch for the distributed training project."
- "Create an English CV from my Chinese resume."
- "Prepare an interview prep pack for a Senior Platform Engineer role at [company]."

The agent follows the workflows defined in `SKILL.md`.

## Common Workflows

```bash
# Create local private profile
python scripts/init_private_profile.py --name my-profile

# Validate profile
python scripts/validate_profile.py resources/profiles/my-profile

# Extract JD keywords
python scripts/extract_jd_keywords.py examples/jd_ai_infra.example.txt

# Score project match
python scripts/score_project_match.py jd_keywords.json resources/profiles/my-profile/projects

# Lint resume draft
python scripts/lint_resume.py draft_resume.md

# Package skill for distribution
python scripts/package_skill.py

# Run privacy guard and tests before push
python scripts/privacy_guard.py
python -m pytest -q

# Full pre-push smoke check
python scripts/smoke_check.py
```

## Scripts

| Script | Purpose |
|--------|---------|
| `privacy_guard.py` | Scan repo for privacy violations. Must pass before push. |
| `init_private_profile.py` | Create a gitignored local profile from example template. |
| `validate_profile.py` | Check a profile directory has all required files and sections. |
| `extract_jd_keywords.py` | Deterministic JD keyword extraction (no LLM). |
| `score_project_match.py` | Score projects against extracted JD keywords. |
| `lint_resume.py` | Lint resume for weak expressions, missing metrics, ATS issues. |
| `render_pdf.py` | Render HTML resume to PDF (requires playwright or weasyprint). |
| `pdf_page_count.py` | Print PDF page count (requires pypdf). |
| `pdf_to_images.py` | Convert PDF to PNG for visual review (requires PyMuPDF). |
| `render_docx.py` | Convert Markdown resume to DOCX (requires python-docx). |
| `package_skill.py` | Package skill into a reproducible zip. |
| `smoke_check.py` | Run privacy guard + validate example + extract + score + lint in one pass. |

## Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
python -m pytest -q

# Run specific test file
python -m pytest tests/test_privacy_guard.py -q
```

## Packaging

```bash
python scripts/package_skill.py
# Output: dist/resume-career-agent.zip
```

The zip excludes: `.git`, caches, `dist/`, `build/`, venvs, and all gitignored private profile data.

## Security and Privacy Checklist

Before every push:

- [ ] `python scripts/privacy_guard.py` passes
- [ ] `python -m pytest -q` passes
- [ ] No real profile content in staged files
- [ ] No real JD content in staged files
- [ ] No generated resumes or cover letters in staged files
- [ ] `.gitignore` correctly blocks `resources/profiles/*` except `example/`

## Troubleshooting

### "playwright not found" when rendering PDF
```bash
pip install playwright && playwright install chromium
# Or use the fallback:
pip install weasyprint
```

### "pypdf not found" when counting PDF pages
```bash
pip install pypdf
```

### "fitz not found" when converting PDF to images
```bash
pip install PyMuPDF
```

### "python-docx not found" when rendering DOCX
```bash
pip install python-docx
```

### Profile validation fails
Check that your `self_profile.md` and `resume_base.md` exist and that projects have all required sections. Run `scripts/validate_profile.py` for details.

### Privacy guard fails after adding real data
Your real profile data should be in gitignored directories. If you accidentally staged it:
```bash
git rm --cached resources/profiles/my-profile/*
# Then check .gitignore is correct
```

## License

MIT License — see `LICENSE`. User-provided profile content is not covered by this license; users retain their own rights.
