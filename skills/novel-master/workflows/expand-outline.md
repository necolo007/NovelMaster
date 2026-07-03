---
description: Expand a brief outline into a detailed chapter-by-chapter breakdown. Run when the user has a rough outline and wants to flesh it out before the Writer phase.
---

# Expand Outline Workflow

> Standalone outline expansion. Run when the user provides a brief/rough outline and wants it expanded into a detailed chapter breakdown suitable for the Writer phase.

---

## When to Run

| User input | Action |
|---|---|
| "帮我展开这个大纲" | Run this workflow |
| "把大纲细化到每一章" | Run this workflow |
| Rough outline + request for detailed breakdown | Run this workflow |
| During Architect phase, user wants more detail on a volume/arc | Run as sub-step |

---

## Step 1: Read Current Outline & Framework

```
read_file <project_path>/framework/plot_outline.md       # Current outline
read_file <project_path>/framework/spec_lock.md          # Constraints
read_file <project_path>/framework/character_profiles.md  # Character arcs
read_file <project_path>/framework/world_building.md      # World constraints
```

If no project exists yet, read whatever outline the user provided in conversation.

---

## Step 2: Identify Expansion Target

Confirm with the user:

| Item | Options |
|------|---------|
| **Scope** | Single arc / Single volume / Entire novel |
| **Detail level** | Chapter-by-chapter (default) / Scene-by-scene (detailed) |
| **Chapter word target** | From spec_lock or user preference |

---

## Step 3: Expand to Chapter Breakdown

For each chapter in scope, define:

```markdown
| Ch | Title | Core Conflict | POV | Word Target | Characters | Plant | Resolve | Pleasure Point |
|----|-------|---------------|-----|-------------|------------|-------|---------|----------------|
```

**Expansion principles**:

1. **Conflict per chapter**: Every chapter must have ONE core conflict. No conflict = no chapter.
2. **Pleasure-point distribution**: Ensure the target mix (from spec_lock) is met across the expanded chapters.
3. **Foreshadowing planning**: Every "plant" must have a corresponding "resolve" chapter. No orphaned threads.
4. **Pacing rhythm**: Alternate high-tension and breathing-room chapters per the rhythm mode.
5. **Character arc alignment**: Chapter events map to character arc milestones from `character_profiles.md`.
6. **Cliffhanger chain**: Each chapter ending hooks into the next chapter's opening.
7. **Word count budget**: Sum of chapter word targets should match the volume/arc word target.

**Quality checks** (self-audit before output):

- [ ] Every chapter has a core conflict
- [ ] ≥1 pleasure point per chapter (type annotated)
- [ ] Every "Plant" has a matching "Resolve" (same thread ID in a later chapter)
- [ ] POV is specified for every chapter
- [ ] Character appearances are tracked (no character vanishes for 20+ chapters without reason)
- [ ] Pleasure-point mix approximately matches target distribution
- [ ] Opening chapter is strongest hook (not a "setup" chapter)

---

## Step 4: Write Output

Write `plot_outline.md` and `chapter_breakdown.md` to the project's `framework/` directory.

If the project doesn't exist yet, output as a Markdown document for the user to feed into the pipeline later.

---

## Step 5: Summary

```markdown
## ✅ Outline Expanded

**Scope**: {volume/arc range}
**Chapters**: {count}
**Total word budget**: {sum}
**Pleasure-point distribution**:
  - Power-up: {count}
  - Face-slap: {count}
  - Reward: {count}
  - Reveal: {count}
  - Romance beat: {count}
**Foreshadowing threads**: {count} planted, {count} unresolved (planned for future volumes)
```
