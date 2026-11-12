# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add at least five advanced song attributes, use them in recommendation
scoring, and document the AI-assisted workflow and manual checks.

**Prompts used:**

> Introduce **5 or more** complex attributes to your dataset that are not
> currently present in the baseline data, such as **Song Popularity (0-100)**,
> **Release Decade**, or **Detailed Mood Tags** (e.g., "nostalgic,"
> "aggressive," "euphoric"). Update both `data/songs.csv` and the scoring logic
> in `src/recommender.py` so scoring accounts for the new attributes. In
> `ai_interactions.md`, document the agentic workflow: the example prompt(s)
> you used, a summary of the changes the AI generated, and your manual
> verification notes.

**What did the agent generate or change?**

- Added popularity, release decade, mood tags, language, and instrumentalness
  to the song model and CSV catalog.
- Added optional user preferences and similarity points for those attributes.
  Profiles that omit them keep the original scoring; each enabled preference
  can add up to one point.
- Added an advanced-preference CLI profile and score denominator, plus tests
  for loading, scoring, and invalid preferences.
- Updated the README and model card to describe the optional features and
  synthetic example metadata.

**What did you verify or fix manually?**

I checked that all 18 catalog rows load with the five new columns and numeric
values are converted by the CSV loader. The advanced CLI profile matches all
five optional preferences for Velvet Groove and prints 9.00/9; ordinary
profiles still use a maximum of 4. I also checked the single-feature tests
against the existing four-point baseline so they measure only the advanced
feature being changed. `python3 -m pytest -q` passed all 46 tests, and
`python3 -m src.main` completed with the advanced profile and the existing
weight-shift experiment.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
