# How to Prepare for an Interview

This guide shows how to use the `resume-career-agent` skill to prepare for a technical interview.

## Prerequisites

1. A private profile at `resources/profiles/my-profile/` with filled project assets
2. Target role and company information

## Steps

1. **Tell the agent your target**:
   > "I'm interviewing for a {{role}} position at {{company}}. Generate an interview prep pack using my profile."
2. **Specify language**: 
   > "I'll be interviewing in English." / "面试是中文的。"
3. **Review the prep pack**: The agent generates content following `templates/interview_prep_pack.md`:
   - Self-introduction (60 seconds)
   - Project deep-dive for each selected project
   - Behavioral question frameworks
   - Risk questions to prepare for
   - Questions to ask the interviewer
4. **Practice pitches**: 
   > "Generate a 60-second project pitch for {{project_name}} in English."
   > "Now expand that to 3 minutes."
5. **Mock Q&A**:
   > "Ask me 5 likely interview questions based on my profile."

## What the agent uses

- `references/interview-question-bank.md` — question templates and frameworks
- `templates/pitch_script_bilingual.md` — structured pitch format
- `templates/interview_prep_pack.md` — complete prep pack template
- Your filled project assets for project-specific questions

## What the agent does NOT do

- Generate fabricated answers to behavioral questions
- Invent accomplishments you don't have
- Create a script that sounds robotic — it provides frameworks you personalize
