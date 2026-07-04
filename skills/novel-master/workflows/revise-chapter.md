---
description: Revise a single chapter and automatically update all affected trackers. Run when the user wants to modify an already-written chapter without re-running the full pipeline.
---

# Revise Chapter Workflow

> Standalone single-chapter revision. Run when the user wants to modify a specific chapter's content and have trackers auto-updated to reflect the changes.

---

## When to Run

| User input | Action |
|---|---|
| "修改第N章" | Run this workflow |
| "重写第N章" | Run this workflow |
| "第N章需要改一下…" | Run this workflow |
| Specific change request for a chapter | Run this workflow |

---

## Step 1: Identify Target Chapter

Confirm with the user:
- Which chapter number to revise
- What needs to change (specific scenes, dialogue, pacing, foreshadowing, etc.)
- Whether this affects subsequent chapters (plot logic changes)

---

## Step 2: Read Chapter Context

Before revising, read:
```
read_file <project_path>/framework/spec_lock.md
read_file <project_path>/framework/chapter_breakdown.md  # target chapter's row
read_file <project_path>/tracking/context_summary.md     # state before this chapter
read_file <project_path>/drafts/chapter_NNN.md           # current version
read_file <project_path>/sources/ingredient_style_guide.md # if present
```

Also read the **preceding chapter** (`drafts/chapter_{N-1}.md`) for continuity hook.

---

## Step 3: Revise Chapter

Generate the revised chapter prose following all Writer standards:
- Same frontmatter format
- Same POV, style, and voice constraints
- Same word count target
- Updated `pleasure_points` and `foreshadowing_*` frontmatter fields
- Apply the Writer reader-view loop: diagnose target-reader weak points, revise for curiosity/empathy/tension/warmth, then do a final polish pass
- If `ingredient_style_guide.md` exists, use it for rhythm/dialogue/sensory/action craft only; do not borrow source plot, characters, or phrasing

Save to `drafts/chapter_NNN.md` (overwrite).

---

## Step 4: Cascade Check

Determine if the revision affects subsequent chapters:

| Change Type | Cascade Required? | Action |
|-------------|-------------------|--------|
| Prose polish (same events, better writing) | No | Skip to Step 5 |
| Minor dialogue change (same outcome) | No | Skip to Step 5 |
| Character action changed (different outcome) | **Yes** | Review chapters N+1 onward for continuity |
| Foreshadowing added/removed | **Yes** | Update `plot_tracker.json`; review resolve chapters |
| Power level / item / location change | **Yes** | Update `character_state.json`; review affected chapters |
| Major plot point changed | **Yes** | Full downstream review — may need to revise N+1, N+2, … |

### If cascade required:

1. Read chapters N+1, N+2, … until continuity is restored
2. For each affected chapter, either:
   - **Minor fix**: edit in-place (update a reference, adjust a detail)
   - **Major break**: mark the chapter as needing revision, report to user with specific issues

```markdown
## 🔄 Cascade Impact Report

| Chapter | Impact | Action |
|---------|--------|--------|
| N+1 | Minor — references old power level | Fixed in-place |
| N+2 | Major — plot logic depends on removed event | **Needs revision** — {specific issue} |
| N+3 | None — continuity restored | — |
```

---

## Step 5: Update Trackers

Update all three tracker files to reflect the revision:

1. **`context_summary.md`**: If the chapter's events changed, update the "Story So Far" summary for all affected chapters
2. **`plot_tracker.json`**: Add/remove/modify foreshadowing entries; update summary counts
3. **`character_state.json`**: Update character states for all affected chapters

---

## Step 6: Chapter Summary

Output revision summary:

```markdown
## ✅ Chapter {N} Revised

**Changes made**: {summary_of_changes}
**Word count**: {old} → {new}
**Cascade impact**: {none | N chapters affected | see report}
**Trackers updated**: context_summary.md, plot_tracker.json, character_state.json
```
