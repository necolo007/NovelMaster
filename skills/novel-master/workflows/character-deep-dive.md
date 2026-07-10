---
description: Generate a deep-dive backstory, character study, or standalone side-story arc for a specific character. Run when the user wants to explore a character beyond the main plot. Supports ensemble cast (群像) integration — deep-dives feed into the main novel's multi-POV narrative.
---

# Character Deep-Dive Workflow

> Standalone character exploration. Run when the user wants to generate a character's detailed backstory, psychological profile, or standalone side-story arc. This enriches the main novel's character depth without bloating the main narrative. For ensemble cast novels, deep-dives on supporting characters directly serve as POV chapter preparation material.

---

## When to Run

| User input | Action |
|---|---|
| "深挖一下XX这个角色" | Run this workflow |
| "给XX写个外传" | Run this workflow |
| "XX的背景故事是什么" | Run this workflow |
| Request for character backstory / side story | Run this workflow |
| "这个配角还需要丰富一下" | Run this workflow with ensemble integration |
| Preparing for a support character's POV chapter | Run Option A+B (backstory + psychological) to establish the character's interiority before writing their POV |

---

## Step 1: Identify Target Character

Read the character's profile:
```
read_file <project_path>/framework/character_profiles.md
```

If no project exists, work from the user's description of the character.

Confirm scope with the user:

| Option | Output |
|--------|--------|
| **A) Backstory deep-dive** | Detailed pre-novel history: childhood, formative events, trauma, key relationships before Chapter 1 |
| **B) Psychological profile** | Personality analysis: defense mechanisms, attachment style, cognitive biases, moral framework |
| **C) Side-story arc** | Standalone narrative (3–10 chapters): a mission, adventure, or relationship that happens off-screen from the main plot |
| **D) Future trajectory** | Post-novel or future-volume arc outline: where this character is heading and why |
| **E) Full package** | All of the above |

---

## Step 2: Gather Context

Read relevant framework files:
```
read_file <project_path>/framework/world_building.md    # World constraints
read_file <project_path>/framework/plot_outline.md      # Where character appears in main plot
read_file <project_path>/framework/spec_lock.md         # Style constraints
read_file <project_path>/tracking/character_state.json  # Current state
```

---

## Step 3: Generate Deep-Dive

### Option A: Backstory Deep-Dive

```markdown
# {Character Name} — Backstory

## Childhood & Origin
- Birthplace, family, early environment
- Formative events (positive and negative)
- First encounter with the power system / world conflict

## Adolescence & Identity Formation
- Key relationships during formative years
- Early ambitions and how they changed
- First major failure / loss

## The Turning Point
- The event that set them on the path to Chapter 1
- What they wanted before vs after
- Who helped / hindered them

## Hidden Scars
- Emotional wounds they conceal
- Lies they tell themselves
- What they're most afraid of

## Timeline
| Age | Event | Impact |
|-----|-------|--------|
| {age} | {event} | {impact} |
```

### Option B: Psychological Profile

```markdown
# {Character Name} — Psychological Profile

## Personality Architecture
- **Surface presentation**: What others see
- **Middle layer**: What close friends see
- **Core**: What only they know

## Defense Mechanisms
- Primary coping strategy under stress
- Secondary / breakdown behavior
- What breaks them completely

## Attachment & Relationships
- Attachment style + origin
- Pattern in friendships
- Pattern in romance
- Blind spots in reading others

## Moral Framework
- Line they won't cross (and why)
- Line they THINK they won't cross (but will)
- Greatest moral contradiction they live with

## Cognitive Patterns
- Decision-making style (impulsive / analytical / intuitive)
- Confirmation bias / blind spots
- Intelligence type (strategic / emotional / creative / practical)
```

### Option C: Side-Story Arc

Generate a complete mini-arc following novel writing standards:

```markdown
# {Character Name} — Side Story: {arc_title}

## Arc Overview
- **Timeline**: When this happens relative to main plot
- **Premise**: {one_sentence}
- **Chapters**: {count} × {word_target} words
- **Tone**: {consistent with main novel or deliberate contrast}

## Chapter Breakdown
| Ch | Title | Core Conflict | Characters | Pleasure Point |
|----|-------|---------------|------------|----------------|

## Chapter 1: {title}
(Full prose, following all Writer standards)
```

---

## Step 4: Cross-Reference Check

Ensure the deep-dive is consistent with:
- Established world rules (no contradictions with `world_building.md`)
- Character's established personality (deep-dive should explain, not contradict)
- Main plot timeline (side-story must fit in gaps without creating continuity errors)

---

## Step 5: Save Output

Save to `notes/character_{name_slug}_{type}.md` in the project directory.

### Ensemble Cast Integration (群像集成)

When the project uses multi-POV ensemble cast, deep-dive output serves double duty:

1. **POV chapter preparation**: Before writing a supporting character's first POV chapter, generate Option A+B for that character. The Writer uses the backstory and psychological profile to construct authentic interiority.
2. **Voice calibration**: The psychological profile's "Personality Architecture" and "Cognitive Patterns" sections become the voice signature reference for that character's POV narration.
3. **Independent desire documentation**: The backstory's "Turning Point" section should crystallize the character's independent desire — what THEY want beyond helping the protagonist. This becomes the emotional engine for their POV chapters.
4. **Update spec_lock.md**: After a deep-dive, update the character's entry in `spec_lock.md §ensemble` with any new voice signature details, independent desire refinements, or arc milestone adjustments discovered during the deep-dive.

```markdown
## ✅ Character Deep-Dive Complete

**Character**: {name}
**Type**: {backstory | psychological | side-story | future | full}
**Saved to**: notes/character_{slug}_{type}.md
**Consistency**: Verified against world_building.md and character_profiles.md
**Ensemble Integration** (if applicable):
  - Voice signature documented for POV narration
  - Independent desire crystallized
  - spec_lock.md §ensemble updated

This material enriches the Writer's understanding of {name} for future chapters.
```
