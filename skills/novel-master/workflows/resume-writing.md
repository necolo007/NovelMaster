---
description: Resume chapter writing in a fresh chat after the framework phase (Steps 1–4) completed in another session. Enters directly into Writer Step 6 without re-running the Architect phase.
---

# Resume Writing Workflow

> Standalone Phase B entry point. Run when the user opens a fresh chat and says "继续写作 projects/<novel_name>" or similar, after the framework phase completed in another session.

This workflow enters directly into the Writer phase, picking up from where the previous session left off.

## When to Run

| User input | Action |
|---|---|
| "继续写作 projects/<novel_name>" | Run this workflow |
| "继续生成 projects/<novel_name>" | Run this workflow |
| "resume writing projects/<novel_name>" | Run this workflow |
| Any phrase indicating continuation of a started novel project | Run this workflow |

---

## Step 1: Locate Project

```bash
python3 ${SKILL_DIR}/scripts/project_manager.py validate <project_path>
```

If the project doesn't exist or is corrupted, report to user and stop.

---

## Step 2: Assess Project State

Read `novel_config.json` to determine `pipeline_state`:

| pipeline_state | Meaning | Action |
|---------------|---------|--------|
| `framing` | Framework complete, writing not started | Resume from Writer Step 6 pre-writing setup |
| `drafting` | Writing in progress | Resume from last completed chapter + 1 |
| `editing` | Writing complete, editing needed | Resume from Editor Step 7 |
| `exporting` | Editing complete, export pending | Resume from Post-processing Step 8 |

---

## Step 3: Reconstruct Context

### If resuming writing (`drafting`):

1. **Read framework files** (speed-read for global awareness):
   ```
   read_file <project_path>/framework/spec_lock.md
   read_file <project_path>/framework/world_building.md
   read_file <project_path>/framework/character_profiles.md
   read_file <project_path>/framework/plot_outline.md
   read_file <project_path>/framework/chapter_breakdown.md
   ```

2. **Read tracker files** (current state):
   ```
   read_file <project_path>/tracking/context_summary.md
   read_file <project_path>/tracking/plot_tracker.json
   read_file <project_path>/tracking/character_state.json
   ```

3. **Determine next chapter**:
   - Count existing `drafts/chapter_*.md` files
   - Next chapter = count + 1
   - Verify against `chapter_breakdown.md`

4. **Output resumption summary**:
   ```markdown
   ## 📖 Resuming Writing — {novel_title}

   **Project**: {project_name}
   **Chapters completed**: {completed_count} / {total_count}
   **Words written**: {words_written} / {words_target}
   **Next chapter**: Chapter {N} "{chapter_title}"
   **Current context**: {brief_summary_from_context_summary}

   Ready to continue from Chapter {N}.
   ```

### If resuming from editing or exporting:

Follow the appropriate SKILL.md step directly.

---

## Step 4: Continue Pipeline

Proceed with the appropriate SKILL.md step:

| Resuming from | Enter SKILL.md at |
|--------------|-------------------|
| `framing` → Writer not started | Writer Step 6, Pre-writing Setup (§1) |
| `drafting` → Chapter N | Writer Step 6, Chapter Generation Loop (§2), starting at chapter N |
| `editing` | Editor Step 7 |
| `exporting` | Post-processing Step 8 |

> ⚠️ **Full Writer discipline applies**: re-read `spec_lock.md` + `context_summary.md` before EVERY chapter, even when resuming. Follow all SKILL.md Step 6 rules exactly.
