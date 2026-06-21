# How to Audit a Resume

This guide shows how to use the `resume-career-agent` skill to audit your resume.

## Prerequisites

1. A private profile at `resources/profiles/my-profile/` (see `usage_private_profile.md`)
2. Your current resume in Markdown format, placed in a local (gitignored) directory

## Steps

1. **Load your profile**: Ask the agent to read `resources/profiles/my-profile/`.
2. **Provide your resume**: Point the agent to your resume file.
3. **Request an audit**: Ask the agent something like:
   > "Audit my resume against my profile. Find weak bullets, red flags, missing evidence, and ATS issues. Generate an audit report."
4. **Review the report**: The agent will produce a report following `templates/resume_audit_report.md` with:
   - 30-second verdict
   - Role-fit score
   - Top strengths and risks
   - Red flags identified
   - Weak bullets with rewrite suggestions
   - Missing information
5. **Iterate**: Ask the agent to rewrite specific sections based on the audit findings.

## What the agent uses

- `references/audit-checklist.md` — structured audit dimensions
- `references/red-flags.md` — common resume problems
- `references/tech-resume-rubric.md` — scoring rubric
- Your profile and project assets for evidence comparison
- `scripts/lint_resume.py` — automated linting for weak expressions
