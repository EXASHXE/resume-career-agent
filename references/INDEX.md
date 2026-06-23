# References Index

This directory contains rubrics, checklists, policies, and methodology guides used by the resume-career-agent skill.

## Rubrics (Role-Specific)

| File | Purpose | When to Use |
|------|---------|-------------|
| `tech-resume-rubric.md` | General technical resume scoring rubric | Default rubric for any technical role |
| `ai-infra-resume-rubric.md` | AI Infrastructure / ML Systems rubric | AI Infra, ML platform, training infra roles |
| `agent-engineer-resume-rubric.md` | Agent Platform Engineer rubric | LLM agent, RAG, tool-use roles |
| `cloudops-resume-rubric.md` | CloudOps / DevOps / SRE rubric | Cloud operations, SRE, platform reliability roles |
| `backend-platform-resume-rubric.md` | Backend / Platform Engineering rubric | Backend, platform, infrastructure roles |

## Checklists

| File | Purpose | When to Use |
|------|---------|-------------|
| `audit-checklist.md` | Full resume audit checklist | During resume audit workflow |
| `ats-checklist.md` | ATS compatibility checklist | When optimizing for Applicant Tracking Systems |
| `red-flags.md` | Common resume red flags | During audit and review |
| `output-quality-gate.md` | Pre-delivery quality gate | Before delivering any output to user |

## Policies

| File | Purpose | When to Use |
|------|---------|-------------|
| `no-fabrication-policy.md` | Rules against inventing experience or metrics | Always — applies at all times |
| `privacy-policy.md` | Privacy model and data handling rules | When handling user profile data |

## Guides

| File | Purpose | When to Use |
|------|---------|-------------|
| `narrative-tools.md` | Project narrative frameworks and verb ownership rules | When writing project narratives or bullet rewrites |
| `bilingual-style-guide.md` | Chinese/English bilingual resume rules | When producing bilingual resumes |
| `jd-keyword-map.md` | JD keyword normalization reference | When extracting or mapping JD keywords |
| `one-page-resume.md` | One-page resume formatting rules | When producing one-page resumes |
| `interview-question-bank.md` | Common interview questions by role | During interview prep workflow |

## Configuration

Config files have been externalized to the `configs/` directory at the project root:

| Config File | Source Script | Content |
|-------------|---------------|---------|
| `configs/jd_keywords.json` | `extract_jd_keywords.py` | Keyword aliases, soft skills, seniority signals, risk signals |
| `configs/lint_rules.json` | `lint_resume.py` | Weak expressions, fabrication risk patterns, thresholds |
| `configs/privacy_rules.json` | `privacy_guard.py` | Forbidden paths, generic secret patterns, skip directories |
| `configs/profile_schema.json` | `validate_profile.py` | Required project asset sections |
