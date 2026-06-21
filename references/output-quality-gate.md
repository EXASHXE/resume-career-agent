# Output Quality Gate

Before delivering any resume draft, audit report, or interview prep material, verify:

## 1. No Fabrication

- [ ] No invented metrics (numbers, percentages, latencies, throughput, scale)
- [ ] No invented production status or user counts
- [ ] No invented employer, title, or date
- [ ] No invented certification, degree, or award
- [ ] No invented open-source contribution or publication
- [ ] All uncertain claims marked with `[TODO / 待补]`

## 2. No Team-to-Individual Rewriting

- [ ] "Designed" only used when the candidate personally designed
- [ ] "Led" only used when the candidate personally led
- [ ] "Owned" only used when the candidate personally owned
- [ ] Team-level results clearly scoped with personal contribution boundary
- [ ] When evidence is insufficient, use weaker verbs like "contributed to", "implemented part of"

## 3. JD Keyword Coverage

- [ ] Must-have keywords present and supported by evidence
- [ ] Nice-to-have keywords present where real evidence exists
- [ ] No keyword stuffing (hidden text, unnatural repetition, unverifiable claims)
- [ ] Keywords appear in resume body text, not just skills section

## 4. Bullet Quality

Each key bullet has:

- [ ] Action verb matching true ownership level
- [ ] Technical artifact or deliverable
- [ ] Result or impact — OR `[TODO: metric placeholder]`
- [ ] Context (what problem, what constraint, what scale)

Weak bullet patterns caught by `lint_resume.py`:

- Chinese: 负责, 参与, 熟悉, 了解, 优化了, 提升了
- English: responsible for, helped with, familiar with, participated in

## 5. ATS Safety

- [ ] Standard section headers (Experience, Projects, Skills, Education)
- [ ] Single-column layout
- [ ] Contact info in plain text, not in header/footer/images
- [ ] No complex tables, text boxes, or multi-column layouts
- [ ] Consistent date format throughout
- [ ] No hidden text or invisible keyword padding

## 6. Bilingual Consistency

- [ ] Chinese and English versions agree on facts, ownership, dates, metrics
- [ ] Both versions include the same set of TODO placeholders
- [ ] Both versions use the correct tense (CN: past context implied, EN: past tense for completed work)
- [ ] Both versions are grammatically correct in their respective languages

## 7. Interview Defensibility

- [ ] Every bullet can be expanded into a 2-minute explanation
- [ ] Technical terms used correctly and verifiably
- [ ] Project-level claims consistent with the candidate's project asset evidence
- [ ] No claim that would collapse under "tell me more about that"

## 8. Missing Information Listed

- [ ] All TODO/待补 placeholders from resume bullets collected
- [ ] Sorted by urgency: blocking submission / strengthens case / optional
- [ ] Each missing item states what evidence the user should provide
- [ ] User knows what to bring to their next session

## 9. Format-Specific Rules

### Markdown
- [ ] Headings use `#` / `##` / `###`
- [ ] Bullets use `- ` (not `* ` for better ATS parsing)
- [ ] Code or technical terms use backticks
- [ ] File is UTF-8 encoded

### PDF
- [ ] Single A4 page (or two pages maximum for senior roles)
- [ ] Fonts embedded and text copyable
- [ ] No garbled characters, no orphan lines across pages
- [ ] Validated with `pdf_page_count.py` and `pdf_to_images.py`

### DOCX
- [ ] Uses paragraph styles (Heading 1/2/3, Normal)
- [ ] Bullet lists are actual list paragraphs
- [ ] No manual spacing hacks
- [ ] Opens correctly in Word and LibreOffice

## 10. Privacy

- [ ] No real name, email, phone, address in any tracked file
- [ ] No real JD content in tracked files
- [ ] No real profile data in tracked files
- [ ] `python scripts/privacy_guard.py` passes
- [ ] Generated documents are in gitignored directories or temp paths

---

**If any check fails, do not deliver. Fix or mark as TODO first.**
