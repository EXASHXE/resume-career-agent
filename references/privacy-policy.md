# Privacy Policy (for the Skill, not for users)

## What this skill does NOT store

- Candidate full name, email, phone, address, ID numbers
- Employer names, client names, department names
- Proprietary system names, internal project code names
- JD files from real employers
- Generated resumes, cover letters, or interview materials
- Any files under `resources/profiles/*` except `example/`

## What local profile data means

Users store their own profile data locally in gitignored directories:

```text
resources/profiles/my-profile/
  self_profile.md
  resume_base.md
  projects/
```

This data is:

- **Never committed to the repository**
- **Never shipped in the distributed skill zip**
- **Only accessible to the agent through file reads at the user's explicit direction**

## Privacy guard enforcement

`scripts/privacy_guard.py` runs deterministically to:

1. Block any `resources/profiles/default/` path from being tracked
2. Block any non-example profile directory from being tracked
3. Scan all tracked files for known forbidden personal project phrases
4. Exit with failure if violations are found

Run before every commit:

```bash
python scripts/privacy_guard.py
```

## If you accidentally commit private data

1. Remove the files from the working tree
2. Use `git filter-repo` to purge from history (NOT `git rm` alone)
3. Force push the cleaned history
4. If the data contained credentials or keys, rotate them immediately
5. If you pushed to a public repo, assume the data is compromised

## What the example profile contains

All example profiles use:

- `[Your Name]`, `[Company A]`, `[Company B]`
- `[University Name]`, `[City, Country]`
- `[your.email@example.com]`, `[github.com/your-handle]`
- Fictional project descriptions with no real architecture details
- `[量化指标待补]` / `[metrics TBD]` placeholders for all quantitative claims

**Nothing in the example profile can be used to identify any real person.**
