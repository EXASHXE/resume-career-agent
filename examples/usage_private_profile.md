# How to Set Up a Private Profile

Your real profile data is **never committed to the repository**. Follow these steps to create a local private profile.

## Quick Start

```bash
# Create a private profile from the example template
python scripts/init_private_profile.py --name my-profile

# This creates resources/profiles/my-profile/ with template files
# The directory is automatically gitignored
```

## Manual Setup

```bash
cp -r resources/profiles/example resources/profiles/my-profile
```

Then edit each file with your real information.

## What goes in each file

### `self_profile.md`

- Your verified identity (name, location, contact — keep this local, never commit)
- Target roles and seniority level
- Languages and work authorization
- Verified skills summary
- Work history timeline

### `resume_base.md`

- Your current resume in structured Markdown
- Links to your project asset files
- Known gaps and missing evidence

### `projects/*.md`

One file per significant project. Follow the `templates/project_asset.md` schema.

Each project must have:
- Metadata section (project name, role, period, team size)
- Technical problem and context
- Your personal contributions (not team output)
- Resume bullets in Chinese and English
- Interview pitch
- Metrics to confirm and missing information

## Validate Your Profile

```bash
python scripts/validate_profile.py resources/profiles/my-profile
```

This checks that all required files and sections are present.

## Privacy Check

```bash
# Confirm your profile is gitignored
git check-ignore resources/profiles/my-profile/self_profile.md

# Run the privacy guard before committing
python scripts/privacy_guard.py
```

## Important

- **Never** run `git add resources/profiles/my-profile/`
- **Never** commit generated resumes or cover letters
- **Always** run `privacy_guard.py` before `git push`
- If you accidentally commit private data, follow the remediation steps in `references/privacy-policy.md`
