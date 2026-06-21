# How to Tailor a Resume to a JD

This guide shows how to use the `resume-career-agent` skill to tailor your resume for a specific job description.

## Prerequisites

1. A private profile at `resources/profiles/my-profile/` (see `usage_private_profile.md`)
2. The JD text (paste directly or save as a file in a gitignored directory)

## Steps

1. **Provide the JD**: Paste the JD text to the agent, or point to a file like `jd/company_role.txt`.
2. **Ask for analysis**: 
   > "Analyze this JD against my profile. Extract keywords, must-haves, nice-to-haves. Score my projects against this JD."
3. **Review the match report**: The agent produces a report following `templates/jd_match_report.md`:
   - Must-have coverage with evidence mapping
   - Project ranking by keyword match
   - Missing evidence flagged
4. **Request tailor**: 
   > "Generate a tailored resume for this JD. Use only verified evidence from my profile."
5. **Review output**: The agent generates a tailored resume draft with:
   - Reordered projects and bullets based on relevance
   - Natural JD keyword coverage
   - TODO placeholders for missing metrics
6. **Lint and validate**:
   ```bash
   python scripts/lint_resume.py tailored_resume.md
   ```
7. **Iterate** until satisfied.

## What the scripts do

- `extract_jd_keywords.py` — deterministic keyword extraction (no LLM)
- `score_project_match.py` — score projects against extracted keywords
- `lint_resume.py` — check for weak expressions and missing evidence

## What the agent handles

- Selecting the right rubric for the role
- Mapping evidence from your profile to JD requirements
- Rewriting bullets in the appropriate narrative style
- Handling bilingual output if needed
