---
description: Gather inspiration and world-building materials via web search when the user supplies only a theme without source files. Produces an inspiration document that feeds SKILL.md Step 1.
---

# Topic Brainstorm Workflow

> Standalone pre-processing step. Run before SKILL.md Step 1 when the user supplies only a theme or keywords with no source files. Output is an inspiration document, shaped to feed `project_manager.py import-sources` directly.

This workflow is **independent**: it owns the inspiration-acquisition step when no material exists; subsequent SKILL.md steps proceed normally with the produced materials as input.

## When to Run

| User-supplied input | Action |
|---|---|
| Theme name only (e.g. "写一本关于星际贸易的小说") | Run this workflow |
| Keywords / genre description without substance (e.g. "玄幻 + 种田 + 轻松") | Run this workflow |
| ≥1 paragraph of substantive world/character/plot description already in chat | Skip — feed chat content into SKILL.md Step 1 directly |
| Source file attached (TXT / MD / EPUB) | Skip — go to SKILL.md Step 1 |

---

## Step 1: Confirm Scope

⛔ **BLOCKING**: confirm scope as a single bundled clarifier. Skip when the user's initial message already covers it.

| Item | Default if user did not specify |
|---|---|
| Theme / Core idea | (from user input) |
| Genre preference | Determine from theme keywords |
| Scope / Depth | Broad world-building + comparable works |
| Output language | Match user input |
| Slug for files (`<topic_slug>`) | snake_case English identifier derived from theme |

**Forbidden — itemized confirmation**: do NOT ask each row separately. One bundled clarifier or none.

---

## Step 2: Gather Inspiration

### 2.1 Comparable Works Search

Search for:
- Top 3–5 comparable web novels in the same genre/sub-genre
- Common tropes and reader expectations for this genre
- Successful opening strategies used by comparable works
- Genre word count conventions and pacing expectations

Use web search tools to find lists, reviews, and genre analyses. For each comparable work found, note:
- Title, author, word count
- Core hook / premise
- Distinctive style or innovation
- What readers praise / criticize

### 2.2 World-Building Inspiration

Search for:
- Real-world historical/cultural parallels that could inform world-building
- Scientific concepts relevant to the theme (for sci-fi)
- Mythology/folklore relevant to the theme (for fantasy)
- Existing power systems or magic systems worth studying

### 2.3 Market Context (Optional)

If the user seems interested in platform publication:
- Current trending sub-genres and reader preferences
- Platform-specific length/update expectations
- Saturation level of the chosen genre

---

## Step 3: Produce Inspiration Document

Write `inspiration.md` with the following structure:

```markdown
# Inspiration — {topic}

> Generated: {date}
> Based on: {user_theme_input}

## 1. Core Concept

- **Theme**: {theme}
- **Genre**: {genre} / {sub_genre}
- **Elevator Pitch** (3 candidates):
  1. {pitch_1}
  2. {pitch_2}
  3. {pitch_3}

## 2. Comparable Works

| Title | Author | Genre | Words | Key Takeaway |
|-------|--------|-------|-------|-------------|
| {title} | {author} | {genre} | {words} | {takeaway} |

## 3. World-Building Seeds

- **Era candidates**: {era_options}
- **Power system directions**: {power_options}
- **Faction ideas**: {faction_ideas}
- **Unique world hooks**: {unique_hooks}

## 4. Character Seeds

- **Protagonist archetypes**: {archetype_options}
- **Relationship dynamics**: {dynamic_options}
- **Antagonist concepts**: {antagonist_options}

## 5. Opening Hook Ideas

1. {hook_1}
2. {hook_2}
3. {hook_3}

## 6. Genre Conventions & Reader Expectations

- **Must-have elements**: {must_haves}
- **Common pitfalls**: {pitfalls}
- **Reader retention factors**: {retention_factors}

## 7. Market Notes (if researched)

- **Platform trends**: {trends}
- **Length expectations**: {length}
- **Competition level**: {competition}
```

---

## Step 4: Handoff

Save the inspiration document and hand off to SKILL.md:

```markdown
## ✅ Topic Brainstorm Complete

Inspiration document produced. Ready for SKILL.md Step 1.

**Next**: The Architect will use this material to draft the Six Confirmations.
Proceed with `project_manager.py init <novel_name> --genre <genre>` in SKILL.md Step 2.
```
