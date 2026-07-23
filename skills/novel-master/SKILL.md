---
name: novel-master
description: >
  AI-driven web novel generation system. Converts inspiration and ideas into complete
  web novels through multi-role collaboration (Architect → Writer → Editor), with
  consistency tracking and multi-format export (TXT/EPUB/Markdown). Supports single-POV
  and multi-POV ensemble cast (群像) narratives. Use when user asks
  to "写小说", "写网文", "generate novel", "create web novel", or mentions "novel-master".
---

# Novel Master Skill

> AI-driven web novel generation system. Converts inspiration and ideas into complete novels through multi-role collaboration and exports to TXT/EPUB/Markdown.

**Core Pipeline**: `Inspiration → Create Project → [Genre Template] → Architect Seven Confirmations → [Reference Search] → Writer Chapter-by-Chapter → Editor Audit → Post-processing → Export`

> [!CAUTION]
> ## 🚨 Global Execution Discipline (MANDATORY)
>
> **This workflow is a strict serial pipeline. The following rules have the highest priority — violating any one of them constitutes execution failure:**
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order; the output of each step is the input for the next. Non-BLOCKING adjacent steps may proceed continuously once prerequisites are met, without waiting for the user to say "continue"
> 2. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require a full stop; the AI MUST wait for an explicit user response before proceeding and MUST NOT make any decisions on behalf of the user
> 3. **NO CROSS-PHASE BUNDLING** — Cross-phase bundling is FORBIDDEN. (Note: the Seven Confirmations in Step 4 are ⛔ BLOCKING — the AI MUST present recommendations and wait for explicit user confirmation before proceeding. Once the user confirms, all subsequent non-BLOCKING steps — framework output, chapter writing, and post-processing — may proceed automatically without further user confirmation)
> 4. **GATE BEFORE ENTRY** — Each Step has prerequisites (🚧 GATE) listed at the top; these MUST be verified before starting that Step
> 5. **NO SPECULATIVE EXECUTION** — "Pre-preparing" content for subsequent Steps is FORBIDDEN (e.g., writing chapter drafts during the Architect phase)
> 6. **NO SUB-AGENT CHAPTER GENERATION** — Writer Step 6 chapter generation is context-dependent and MUST be completed by the current main agent end-to-end. Delegating chapter text generation to sub-agents is FORBIDDEN
> 7. **SEQUENTIAL CHAPTER GENERATION ONLY** — In Writer Step 6, after the global framework context is confirmed, chapters MUST be generated sequentially one by one in one continuous pass. Grouped chapter batches (for example, 5 chapters at a time) are FORBIDDEN
> 8. **SPEC_LOCK RE-READ PER CHAPTER** — Before generating each chapter, Writer MUST `read_file <project_path>/framework/spec_lock.md` + `read_file <project_path>/tracking/context_summary.md`. All style rules, character traits, and plot constraints MUST come from these files — no values from memory or invented on the fly. This rule exists to resist context-compression drift on long novels

> [!IMPORTANT]
> ## 🌐 Language & Communication Rule
>
> - **Response language**: match the user's input and source materials. Explicit user override (e.g., "请用英文回答") takes precedence.
> - **Output language**: novel content is generated in the project's configured language (default `zh-CN`).

> [!IMPORTANT]
> ## 🔌 Compatibility With Generic Coding Skills
>
> - `novel-master` is a repository-specific workflow, not a general application scaffold
> - Do NOT create `.worktrees/`, `tests/`, branch workflows, or generic engineering structure by default
> - On conflict with a generic coding skill, follow this skill unless the user explicitly says otherwise

## Main Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `${SKILL_DIR}/scripts/project_manager.py` | Project init / import-sources / validate |
| `${SKILL_DIR}/scripts/reference_search.py` | Web search for reference materials (conditional) |
| `${SKILL_DIR}/scripts/ingredient_analyzer.py` | Local same-genre ingredient style guide generation |
| `${SKILL_DIR}/scripts/consistency_checker.py` | Cross-chapter consistency audit |
| `${SKILL_DIR}/scripts/character_checker.py` | Character behavior consistency audit |
| `${SKILL_DIR}/scripts/plot_checker.py` | Plot logic & foreshadowing audit |
| `${SKILL_DIR}/scripts/style_checker.py` | Writing style & viewpoint audit |
| `${SKILL_DIR}/scripts/pacing_checker.py` | Chapter pacing & pleasure-point audit |
| `${SKILL_DIR}/scripts/novel_audit.py` | Full audit orchestrator (runs all 5 checkers) |
| `${SKILL_DIR}/scripts/chapter_normalizer.py` | Unified chapter numbering |
| `${SKILL_DIR}/scripts/chapter_memory.py` | Archive every 10/20 chapters into memory folders |
| `${SKILL_DIR}/scripts/toc_generator.py` | Table of contents generation |
| `${SKILL_DIR}/scripts/export_txt.py` | Export to plain text (web novel platform) |
| `${SKILL_DIR}/scripts/export_epub.py` | Export to EPUB e-book |
| `${SKILL_DIR}/scripts/export_markdown.py` | Export to Markdown collection |

## Template Index

| Index | Path | Purpose |
|-------|------|---------|
| Framework spec reference | `${SKILL_DIR}/templates/framework_spec_reference.md` | Full structure for Architect's framework output |
| Spec lock reference | `${SKILL_DIR}/templates/spec_lock_reference.md` | Machine-readable execution lock template |
| Genre templates | `${SKILL_DIR}/templates/genres/` | Optional genre-specific world-building / plot skeletons |

## Standalone Workflows

| Workflow | Path | Purpose |
|----------|------|---------|
| `topic-brainstorm` | `workflows/topic-brainstorm.md` | Pre-pipeline — gather inspiration when the user supplies only a theme with no source files |
| `resume-writing` | `workflows/resume-writing.md` | Phase B entry — resume chapter writing in a fresh chat after the framework phase completed in another session (split mode) |
| `revise-chapter` | `workflows/revise-chapter.md` | Single-chapter revision — modify a chapter and auto-update trackers |
| `expand-outline` | `workflows/expand-outline.md` | Outline expansion — flesh out a brief outline into detailed chapter breakdown |
| `character-deep-dive` | `workflows/character-deep-dive.md` | Character deep-dive — generate backstory or standalone arc for a character |

---

## Workflow

### Step 1: Inspiration Ingestion

🚧 **GATE**: User has provided inspiration material (document / link / brain-dump description / keywords / setting references — any form is acceptable).

> **No inspiration material?** When the user supplies only a theme name or requirements without any substantive description, run the [`topic-brainstorm`](workflows/topic-brainstorm.md) workflow first, then return here with its products as input.

When the user provides source content, process immediately:

| User Provides | Action |
|---------------|--------|
| TXT / MD inspiration document | Read directly — will be imported in Step 2 |
| EPUB reference novel | Save to `ingredient/` for style/trope reference |
| Web link (reference setting) | Read with `web_fetch` tool; save key points |
| Brain-dump in conversation | Organize as `sources/inspiration.md` in Step 2 |
| Keywords / theme only | This IS material — note them for Architect in Step 4 |

> **Ingredient philosophy**: reference novels in `ingredient/` serve as style exemplars and trope libraries. The Architect and Writer may reference them for genre conventions, but never copy plot or characters. Each `ingredient/` subdirectory should contain a `README.md` noting which aspects are worth studying (prose style, pacing pattern, world-building approach, etc.).
>
> **Same-genre style ingestion**: if local reference novels exist under `ingredient/` or `ingredients/`, build a project-level style guide with `ingredient_analyzer.py` after project initialization. The guide extracts craft signals only (rhythm, dialogue ratio, sensory/action/emotion density, reader-polish checklist). It must not quote or reuse reference prose.

**✅ Checkpoint — Confirm inspiration material is ready, proceed to Step 2.**

---

### Step 2: Project Initialization

🚧 **GATE**: Step 1 complete; inspiration material is ready.

```bash
python3 ${SKILL_DIR}/scripts/project_manager.py init <novel_name> --genre <genre>
```

Genre options: `xuanhuan` / `xiuzhen` / `dushi` / `kehuan` / `qihuan` / `wuxia` / `xianxia` / `lishi` / `youxi` / `moshi` / `xuanyi` / `tongren` / `custom`

> Genre selection influences the Architect's default recommendations (world-building templates, common trope libraries, reference word-count ranges). The user may override any recommendation.

Project naming convention: `<genre>_<slug>`, e.g. `xuanhuan_fanren_xiuxian`. Slug is English snake_case.

Import inspiration material:

| Situation | Action |
|-----------|--------|
| Has source files (TXT/MD/etc.) | `python3 ${SKILL_DIR}/scripts/project_manager.py import-sources <project_path> <source_files...> --move` |
| User provided text directly in conversation | Write inspiration to `<project_path>/sources/inspiration.md` |
| Has EPUB reference novels | Keep in `ingredient/`; note path in `sources/references.md` |

> ⚠️ **MUST use `--move`** (not copy): all source files go into `sources/` via `import-sources --move`. After execution they no longer exist at the original location.

**Project directory structure created:**

```
projects/<novel_name>/
├── novel_config.json          # Project config
├── framework/                 # Architect output
├── sources/                   # Inspiration & reference
├── drafts/                    # Writer output
├── tracking/                  # Auto-maintained trackers
├── memory/                    # Chapter batch archives and long-term memory
├── notes/                     # Editor notes
└── export/                    # Final output
```

**✅ Checkpoint — Confirm project structure created, `sources/` contains inspiration, proceed to Step 3.**

---

### Step 3: Genre Template (Optional)

🚧 **GATE**: Step 2 complete; project directory structure is ready.

**Default — free design.** Proceed directly to Step 4. Do NOT suggest templates. Do NOT ask the user.

**Template flow triggers ONLY on an explicit template directory path** supplied by the user in their initial message. The trigger rule is mechanical, not interpretive:

| User input contains | Step 3 action |
|---|---|
| An explicit path to a template directory (e.g. `skills/novel-master/templates/genres/xuanhuan_classic/`) | Copy that directory's template files into `framework/`, advance |
| Anything else — genre names ("玄幻", "凡人流"), style descriptions ("爽文", "慢热"), or silence | Skip Step 3, free design |

```bash
TEMPLATE_DIR=<user-supplied path>
cp ${TEMPLATE_DIR}/world_building_template.md <project_path>/framework/
cp ${TEMPLATE_DIR}/character_archetypes.md <project_path>/framework/
cp ${TEMPLATE_DIR}/plot_patterns.md <project_path>/framework/
```

> Genre names ("凡人流", "洪荒流") do NOT trigger Step 3. They flow naturally into Architect's Six Confirmations as style briefs.

> Bare template names ("xuanhuan_classic") do NOT trigger Step 3 even if a folder by that name exists. The user must give a path.

**✅ Checkpoint — Default path proceeds to Step 4. If user supplied an explicit template path, that directory is copied before advancing.**

---

### Step 4: Architect Phase ⛔ BLOCKING (MANDATORY — cannot be skipped)

🚧 **GATE**: Step 3 complete; default free-design path taken, or (if triggered) template files copied.

First, read the role definition:
```
Read references/architect.md
```

> ⚠️ **Mandatory gate**: before writing any framework file, Architect MUST `read_file templates/framework_spec_reference.md` and follow its complete structure. See `architect.md` Section 1.

#### Seven Confirmations (捆绑呈现)

⛔ **BLOCKING**: present the Seven Confirmations as a single bundled recommendation set and **wait for explicit user confirmation or modification** before outputting any framework files. This is the single core confirmation point — once confirmed, all subsequent steps proceed automatically.

##### a. Work Positioning (作品定位)

| Dimension | Recommendation | Notes |
|-----------|---------------|-------|
| **Title** | AI recommends 3–5 candidates | User confirms or customizes |
| **Author pen name** | User provides or AI suggests | — |
| **Genre / sub-genre** | Based on Step 2 genre + AI refinement | e.g. "科幻/星际种田" |
| **One-liner hook** | AI generates 3 versions | For reader attraction |

##### b. Length & Rhythm (篇幅与节奏)

| Dimension | Recommended Range | Notes |
|-----------|-------------------|-------|
| **Total word count** | 300K / 500K / 1M / 2M+ | Platform convention |
| **Avg chapter words** | 2000 / 3000 / 4000 / 5000 | Platform & genre preference |
| **Update frequency** | Daily / 3× per week | Affects chapter granularity |
| **Rhythm mode** | Fast-paced wish-fulfillment / Slow-burn build-up / Alternating tension | Affects per-chapter conflict density |

##### c. World Building (世界观设定)

| Dimension | Recommendation | Notes |
|-----------|---------------|-------|
| **Era** | Ancient / Modern / Near-future / Far-future / Alternate | — |
| **Geography** | Single continent / Multi-planet / Realm system | — |
| **Core supernatural** | Cultivation / Magic / Tech / Psionics / None | Top-level power system design |
| **Faction structure** | Recommend 3–5 core factions | With goals and conflicts |
| **Social hierarchy** | Commoners / Nobles / Cultivators / … | Affects character behavior logic |

##### d. Character Design (人物设定)

⛔ **Key confirmation**: first present protagonist group (1–3), key supporting cast (3–5), main antagonist (1–2) as quick sketches. Wait for confirmation before expanding to full profiles.

| Dimension | Content |
|-----------|---------|
| **Protagonist** | Name, appearance, personality layers, backstory, core drive, power progression |
| **Female lead / Partner** | Same + relationship evolution arc with protagonist |
| **Mentor / Elder** | Same |
| **Key supporting × 3–5** | Quick sketch (identity, relationship to protagonist, narrative function) |
| **Main antagonist** | Motivation (cannot be pure evil), mirror contrast with protagonist |

##### e. Plot Outline (情节大纲)

| Dimension | Recommendation | Notes |
|-----------|---------------|-------|
| **Volume structure** | 3–5 volumes | Each volume: one core conflict + theme |
| **Volume 1 arcs** | 3–5 arcs | Each arc: 10–20 chapters |
| **Opening hook** | 3 candidate approaches | Chapter 1's core attraction |
| **Main plot lines** | A-line (main) / B-line (romance) / C-line (hidden) | Interweave plan |
| **Climax nodes** | Per-volume climax positions | — |
| **Ending direction** | Open / Happy / Tragic / Twist | Mark TBD if uncertain |

##### f. Style & Narrative Strategy (文风与叙事策略)

| Dimension | Recommendation | Notes |
|-----------|---------------|-------|
| **Narrative POV** | First person / Third person limited / Third person omniscient / Multi-POV rotating | With reasoning |
| **Prose style** | Plain / Ornate / Humorous / Hot-blooded / Healing / Dark | Combinable |
| **Dialogue ratio** | Low (20%) / Medium (35%) / High (50%+) | — |
| **Pleasure-point types** | Power-up / Face-slap / Reward / Reveal / Romance escalation | ≥1 per chapter |

##### g. Ensemble Cast Design (群像设计) — When Applicable

> For multi-POV/ensemble cast novels only. For single-protagonist novels, note "不适用" and skip.

| Dimension | Recommendation | Notes |
|-----------|---------------|-------|
| **Ensemble tier** | T1 (轻群像) / T2 (均衡群像) / T3 (全景群像) | T1 recommended for most web novels |
| **POV rotation plan** | Primary ~60%, Secondary ~20% each, Tertiary ~5% each | Return-to-primary every 3 chapters |
| **Support character depth** | Each POV support: independent desire + moral logic + flaw + voice signature + spotlight chapter | 8-point checklist (see architect.md §g.2) |
| **Group dynamics** | Group identity, internal frictions, pair chemistries, evolution arc | — |

---

#### Post-Confirmation Output

After user confirms, Architect produces all framework files in one pass:

```
framework/
├── world_building.md       # Complete world setting
├── character_profiles.md   # Full character dossiers
├── plot_outline.md         # Volume → Arc → Chapter outline
├── chapter_breakdown.md    # Per-chapter breakdown table
└── spec_lock.md            # Execution lock
```

**✅ Architect Phase Complete**:
```markdown
## ✅ Architect Phase Complete
- [x] Seven Confirmations user-confirmed
- [x] world_building.md produced
- [x] character_profiles.md produced (with relationship descriptions + group dynamics for ensemble)
- [x] plot_outline.md produced (volumes / arcs / chapters)
- [x] chapter_breakdown.md produced (per chapter: core conflict + POV + word count + foreshadowing + POV rotation plan for ensemble)
- [x] spec_lock.md generated (with §ensemble section if applicable)
- [ ] **Next**: Auto-proceed to [Reference Search / Writer] phase
```

---

### Step 5: Reference Assimilation & Search Phase

🚧 **GATE**: Step 4 complete; user confirmed framework.

#### 5.1 Local Ingredient Assimilation (Default)

If same-genre reference material exists in `ingredient/` or `ingredients/`, run:

```bash
python3 ${SKILL_DIR}/scripts/ingredient_analyzer.py <project_path>
```

When the relevant corpus is in a specific subdirectory, pass it explicitly:

```bash
python3 ${SKILL_DIR}/scripts/ingredient_analyzer.py <project_path> --ingredient-dir ingredient/<same_genre_dir>
```

Output:

```
<project_path>/sources/ingredient_style_guide.md
```

This guide is mandatory writing context when present. It is a craft summary, not a source of plot, character, or quotable prose.

#### 5.2 External Reference Search (Conditional)

> **Trigger**: Architect marked items in `spec_lock.md` that need external reference material (e.g. specific scene reference images, historical background, scientific validation). Only execute when the framework genuinely needs external references; skip to Step 6 otherwise.

```bash
python3 ${SKILL_DIR}/scripts/reference_search.py <project_path>
```

**✅ Checkpoint — Confirm local ingredient style guide is generated or intentionally absent; confirm external reference search complete or skipped. Proceed to Step 6.**

---

### Step 6: Writer Phase (Chapter-by-Chapter Generation)

🚧 **GATE**: Step 4 (and Step 5 if triggered) complete; all framework files ready.

Read the role definitions:
```
Read references/writer.md
Read references/shared-standards.md   # Web novel writing constraints
```

#### Pre-writing Setup (One-time)

1. **Design parameter confirmation**: output key writing parameters (style, POV, chapter word count range, pleasure-point strategy) derived from `spec_lock.md`
2. **Framework speed-read**: batch-read all files under `framework/` to establish global awareness
3. **Ingredient style guide read**: if `<project_path>/sources/ingredient_style_guide.md` exists, read it and extract 3-5 concrete craft targets for the current project (rhythm, dialogue, sensory detail, action beats, emotional warmth)
4. **Initialize trackers**: create initial state for:
   - `tracking/context_summary.md` — initial context
   - `tracking/plot_tracker.json` — empty foreshadowing registry
   - `tracking/character_state.json` — initial character states
5. **Long-memory setup**: if `tracking/latest_memory.md` exists, read it before continuing; otherwise create `memory/` on the first archive boundary.

#### Chapter Generation Loop

> ⚠️ **Main-agent only**: Chapter generation MUST stay in the current main agent — chapter continuity depends on full upstream context. Do NOT delegate to sub-agents.
>
> ⚠️ **Re-read spec_lock every chapter**: before each chapter, `read_file <project_path>/framework/spec_lock.md` + `read_file <project_path>/tracking/context_summary.md` to prevent context-compression drift.
>
> ⚠️ **Read long-memory when present**: before each chapter, also read `<project_path>/tracking/latest_memory.md` if it exists. It is a compact historical layer; newer tracker files override it on conflict.
>
> ⚠️ **Re-read ingredient style guide when present**: before each chapter, also read `<project_path>/sources/ingredient_style_guide.md`. Use it for craft moves only; never copy reference plot, characters, or wording.

**Per-chapter flow (authoritative updated flow)**:

```
FOR each chapter (from chapter_breakdown.md in order):
  1. Read spec_lock.md + context_summary.md + latest_memory.md (if present) + ingredient_style_guide.md (if present)
  2. Look up chapter_breakdown.md entry (core conflict, POV, word target, foreshadowing to plant/resolve)
  3. Look up character_profiles.md and character_state.json for appearing characters
  4. Draft pass: generate complete chapter prose
  5. Reader-view pass: simulate 2-3 target readers and note where curiosity, empathy, desire, humor, tension, or emotional warmth feels weak
  6. Style-assimilation pass: revise using ingredient_style_guide craft targets (rhythm, dialogue flavor, sensory/action detail, chapter hook) without copying any source wording; must land ≥2 concrete craft moves, not metric checkboxing
  7. Final polish pass: remove stiff/formal summary narration, cut decorative filler and weird abstract adjectives, expand telegram dialogue into characterful lines, keep one metaphor per beat, tighten mobile paragraphs, then save final prose to drafts/chapter_NNN.md
  8. Self-review (word count tolerance, pleasure point, POV, reader warmth, prose naturalness, dialogue flavor ≠ dry Q&A, adjective sanity, safe ingredient usage)
  9. Update context_summary.md, plot_tracker.json, and character_state.json
  10. If chapter number is divisible by memory_archive_interval (default 10), run chapter_memory.py to archive the latest complete batch
  11. Output chapter summary (word count, key events, reader-view fixes, style-guide craft moves, foreshadowing operations, memory archive status)
NEXT
```

**Legacy short summary (do not use when it conflicts with the authoritative updated flow above)**:

```
FOR each chapter (from chapter_breakdown.md in order):
  1. Read spec_lock.md + context_summary.md
  2. Look up chapter_breakdown.md entry (core conflict, POV, word target, foreshadowing to plant/resolve)
  3. Look up character_profiles.md for current state of appearing characters
  4. Generate prose → drafts/chapter_NNN.md
  5. Self-review (word count ±15%, ≥1 pleasure point, no POV violation)
  6. Update context_summary.md (summary + character states + foreshadowing status)
  7. Update plot_tracker.json (foreshadowing planted/resolved)
  8. Update character_state.json (location/relationship/power changes)
  9. Output chapter summary (word count, key events, foreshadowing operations)
NEXT
```

**Chapter file format** (`drafts/chapter_NNN.md`):

```markdown
---
chapter: 43
title: "暗夜救援"
pov: "林星河"
words: 3150
characters_appearing: ["林星河", "苏晴", "黑衣人头目"]
foreshadowing_planted: ["仓库地下通道通往何处"]
foreshadowing_resolved: ["第15章-前任店主身份暗示"]
---

# 第四十三章 暗夜救援

(prose content…)
```

**Continuity safeguards**:
- `context_summary.md` serves as Writer's per-chapter entry document with "immediately preceding" narrative hook
- `tracking/latest_memory.md` serves as long-range memory after each archive batch; read it before writing later chapters
- `memory/chapters_001_010/` style folders preserve searchable batch archives without moving source drafts
- Character state tracking ensures consistent behavior
- Foreshadowing tracker ensures every planted thread is eventually resolved

**Long-memory archive cadence**:

```bash
# Default: archive complete 10-chapter batches
python3 ${SKILL_DIR}/scripts/chapter_memory.py <project_path>

# Larger projects may prefer 20-chapter batches
python3 ${SKILL_DIR}/scripts/chapter_memory.py <project_path> --span 20
```

Use `novel_config.json` field `memory_archive_interval` to set the project default. Archives are additive and non-destructive: `drafts/` remains the source of truth.

**✅ Writer Phase Complete**:
```markdown
## ✅ Writer Phase Complete
- [x] All chapters generated (N chapters total, M words total)
- [x] context_summary.md continuously updated through final chapter
- [x] memory/ archives generated for each completed archive batch
- [x] tracking/latest_memory.md points to the latest completed archive memory
- [x] plot_tracker.json: all foreshadowing status = 'resolved' or marked 'abandoned' (with reason)
- [x] character_state.json: complete character arc tracking
```

---

### Step 7: Editor Audit Phase

🚧 **GATE**: Step 6 complete; all chapter drafts ready.

Read the role definition:
```
Read references/editor.md
```

**Audit dimensions**:

| Dimension | Script | Checks |
|-----------|--------|--------|
| **Consistency** | `consistency_checker.py` | Name consistency, kinship/title/surname logic, timeline no contradiction, item ownership no errors |
| **Character** | `character_checker.py` | Behavior consistency, power growth no jumps, relationship evolution reasonable |
| **Plot** | `plot_checker.py` | All foreshadowing resolved, no logic holes, power system no collapse |
| **Style** | `style_checker.py` | Style matches spec_lock, dialogue ratio meets target, no POV violations |
| **Pacing** | `pacing_checker.py` | Per-chapter conflict density, pleasure-point distribution, climax/valley rhythm |

```bash
# Run individual checkers
python3 ${SKILL_DIR}/scripts/consistency_checker.py <project_path>
python3 ${SKILL_DIR}/scripts/character_checker.py <project_path>
python3 ${SKILL_DIR}/scripts/plot_checker.py <project_path>
python3 ${SKILL_DIR}/scripts/style_checker.py <project_path>
python3 ${SKILL_DIR}/scripts/pacing_checker.py <project_path>

# Or run full audit
python3 ${SKILL_DIR}/scripts/novel_audit.py <project_path>
```

- **error**: must fix (name confusion, timeline contradiction, lost foreshadowing)
- **warning**: should fix (slow pacing in chapter X, low dialogue ratio)
- **info**: for reference only

**✅ Editor Audit Complete**:
```markdown
## ✅ Editor Audit Complete
- [x] consistency_checker: 0 errors, N warnings
- [x] character_checker: 0 errors, N warnings
- [x] plot_checker: 0 errors, N warnings
- [x] style_checker: pass
- [x] pacing_checker: pass
```

---

### Step 8: Post-processing & Export

🚧 **GATE**: Step 7 complete; audit passed.

#### 8.1 Chapter Number Normalization

```bash
python3 ${SKILL_DIR}/scripts/chapter_normalizer.py <project_path>
```

Unified chapter title format per project language config.

#### 8.2 Table of Contents

```bash
python3 ${SKILL_DIR}/scripts/toc_generator.py <project_path>
```

Auto-generate hyperlinked TOC (for Markdown and EPUB).

#### 8.3 Export

> ⚠️ Run exports one at a time — each must complete successfully before the next.

```bash
# Plain text (web novel platform submission)
python3 ${SKILL_DIR}/scripts/export_txt.py <project_path>
# → export/<novel_name>.txt

# EPUB e-book
python3 ${SKILL_DIR}/scripts/export_epub.py <project_path>
# → export/<novel_name>.epub

# Markdown collection
python3 ${SKILL_DIR}/scripts/export_markdown.py <project_path>
# → export/<novel_name>.md
```

**Export parameters**:
- `--volume-split`: split into multiple files per volume (for very long novels)
- `--encoding`: encoding selection (default UTF-8 with BOM for TXT, platform-compatible)
- `--no-frontmatter`: export without YAML frontmatter, pure prose only

---

## Role Switching Protocol

Before switching roles, **MUST first read** the corresponding reference file. Output marker:

```markdown
## [Role Switch: <Role Name>]
📖 Reading role definition: references/<filename>.md
📋 Current task: <brief description>
```

---

## Reference Resources

| Resource | Path |
|----------|------|
| Shared writing standards | `references/shared-standards.md` |
| Framework spec reference | `templates/framework_spec_reference.md` |
| Spec lock reference | `templates/spec_lock_reference.md` |

---

## Notes

- **Ingredient usage**: reference novels in `ingredient/` are style/trope references only. Never copy plot points, character designs, or prose passages. The `ingredient/` directory is read-only for the pipeline.
- **Split-mode execution**: the framework phase (Steps 1–4) and writing phase (Steps 5–8) can run in separate sessions. After Step 4, the user may say "先到这里" to pause; resume later with the [`resume-writing`](workflows/resume-writing.md) workflow.
- **Manual intervention points**: the pipeline is designed for AI execution, but three points welcome human intervention — (a) post-confirmation framework tweaks, (b) per-chapter manual edits before tracker updates, (c) post-audit manual fixes before export.
