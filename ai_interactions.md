# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add advanced song features and an alternate ranking mode, then record the
prompt, generated changes, and manual verification.

**Prompts used:**

**Advanced song features**

> Introduce **5 or more** complex attributes to your dataset that are not
> currently present in the baseline data, such as **Song Popularity (0-100)**,
> **Release Decade**, or **Detailed Mood Tags** (e.g., "nostalgic,"
> "aggressive," "euphoric"). Update both `data/songs.csv` and the scoring logic
> in `src/recommender.py` so scoring accounts for the new attributes. In
> `ai_interactions.md`, document the agentic workflow: the example prompt(s)
> you used, a summary of the changes the AI generated, and your manual
> verification notes.

**Alternate ranking mode**

> Now do some variations of **Step 3: Run a Small Data Experiment**
> - Choose one change to test your system's sensitivity:
> - **Weight Shift:** Double the importance of energy and half the importance
>   of genre.
> - **Feature Removal:** Temporarily comment out the mood check to see how the
>   rankings change.
> - Use your AI coding assistant to quickly apply one of these experimental
>   changes across `recommender.py`. In your prompt, describe the specific
>   logic change you want to see and ask it to verify that the math remains
>   valid.
> - Run your `main.py` again. Note whether the change made the recommendations
>   more accurate or just different.

I chose the weight-shift variation.

**What did the agent generate or change?**

- Added popularity, release decade, mood tags, language, and instrumentalness
  to the song model and all 18 CSV rows.
- Added optional user preferences and up to one similarity point per enabled
  feature. Profiles that omit advanced preferences keep the original score.
- Kept the standard ranker and added a weight-shift mode: genre changes from
  2 points to 1, and energy from up to 1 point to up to 2; mood remains 1.
- Added an advanced-preference CLI profile with a matching score denominator,
  and tests for feature loading, scoring, validation, and ranking behavior.
- Updated the README and model card to describe the optional features and
  synthetic example metadata.

**What did you verify or fix manually?**

I checked that all 18 catalog rows load with the five new columns and numeric
values are converted by the CSV loader. The advanced CLI profile matches all
five optional preferences for Velvet Groove and prints 9.00/9; ordinary
profiles still use a maximum of 4. I checked the weight-shift arithmetic:
Gym Hero remains first, while Storm Runner moves above Sunrise City because
the energy match has more weight. I corrected the single-feature tests to
compare each advanced feature's contribution against the four-point baseline.
`python3 -m pytest -q` passed all 46 tests, and `python3 -m src.main`
completed with both the advanced profile and weight-shift mode.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
