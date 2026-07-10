# {novel_title} — Novel Framework

> Human-readable design narrative — rationale, world, characters, plot, style. Read once by downstream roles (Writer, Editor) for context.
>
> Machine-readable execution contract: `spec_lock.md` (style / character / world / plot short form). Writer re-reads `spec_lock.md` before every chapter to resist context-compression drift. Keep both in sync; on divergence, `spec_lock.md` wins.

## I. Project Information

| Item | Value |
|------|-------|
| **Project Name** | {project_name} |
| **Title** | {novel_title} |
| **Author** | {author_pen_name} |
| **Genre** | {genre} / {sub_genre} |
| **Total Word Target** | {target_words} |
| **Avg Chapter Words** | {chapter_avg_words} |
| **Language** | {language} |
| **Created Date** | {date_str} |
| **One-liner Hook** | {one_liner} |

---

## II. World Building Summary

> Full details in `world_building.md`. This section provides the essential framework.

### Era & Geography

- **Time Period**: {era}
- **Geography**: {geography_type}
- **Key Locations**: {key_locations_summary}
- **Travel/Transport**: {travel_norms}

### Power System (力量体系)

- **System Type**: {power_system_type} (Cultivation / Magic / Technology / Psionics / None)
- **Tier Structure**: {tier_count} tiers/realms
- **Progression**: {progression_mechanics_summary}
- **Costs & Limits**: {costs_summary}

| Tier | Name | Capabilities | Social Status |
|------|------|-------------|---------------|
| {tier_1} | {name} | {caps} | {status} |
| {tier_2} | {name} | {caps} | {status} |
| ... | ... | ... | ... |

### Factions

| Faction | Goal | Resources | Leader | Relationship to Protagonist |
|---------|------|-----------|--------|----------------------------|
| {faction_1} | {goal} | {resources} | {leader} | {relationship} |
| {faction_2} | {goal} | {resources} | {leader} | {relationship} |
| ... | ... | ... | ... | ... |

### World Rules (Hard Constraints)

1. {rule_1}
2. {rule_2}
3. {rule_3}

---

## III. Character Profiles Summary

> Full dossiers in `character_profiles.md`. This section provides the essential reference.

### Protagonist

| Attribute | Value |
|-----------|-------|
| **Name** | {protagonist_name} |
| **Age** | {age} |
| **Appearance** | {appearance_brief} |
| **Personality** | Surface: {surface} / Middle: {middle} / Deep: {deep} |
| **Core Drive** | {core_drive} |
| **Power Progression** | {starting_power} → {peak_power} |
| **Speech Style** | {speech_style} |
| **Character Arc** | From {arc_start} → To {arc_end} |

### Key Supporting Cast

| Name | Role | Relationship to MC | Independent Desire | Moral Logic | Flaw | Voice Signature | Spotlight Ch | Arc | Thematic Function |
|------|------|-------------------|-------------------|-------------|------|----------------|-------------|-----|-------------------|
| {name} | {role} | {relationship} | {independent_desire} | {moral_logic} | {flaw} | {voice} | {ch} | {arc} | {theme} |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Group Dynamics (Ensemble Only)

| Dimension | Value |
|-----------|-------|
| **Group Identity** | {what binds them} |
| **Internal Frictions** | {tensions} |
| **Pair Chemistries** | {pair_1}: {chemistry}, {pair_2}: {chemistry} |
| **Evolution Arc** | Formation → trust → fracture → reconciliation → transformation |

### Main Antagonist

| Attribute | Value |
|-----------|-------|
| **Name** | {antagonist_name} |
| **Motivation** | {motivation} (NOT "pure evil") |
| **Mirror to Protagonist** | {mirror_contrast} |
| **Power Level** | {power_level} |
| **Arc** | {antagonist_arc} |

---

## IV. Plot Outline Summary

> Full outline in `plot_outline.md`. This section provides the high-level structure.

### Volume Structure

| Vol | Title | Chapters | Core Conflict | Theme | Status |
|-----|-------|----------|---------------|-------|--------|
| 1 | {title} | {range} | {conflict} | {theme} | 进行中 |
| 2 | {title} | {range} | {conflict} | {theme} | 未开始 |
| ... | ... | ... | ... | ... | ... |

### Plot Lines

| Line | Type | Description | Key Milestones |
|------|------|-------------|----------------|
| **A (Main)** | {type} | {description} | {milestones} |
| **B (Romance)** | {type} | {description} | {milestones} |
| **C (Hidden)** | {type} | {description} | {milestones} |

### Opening Hook Strategy

{selected_strategy} — {rationale}

---

## V. Chapter Breakdown (Volume 1)

> Full table in `chapter_breakdown.md`. This is the Writer's primary per-chapter reference.

### POV Rotation Plan (Multi-POV / Ensemble Only)

| POV Character | Total Chapters | % | Chapter Numbers |
|---------------|---------------|-----|-----------------|
| {primary} | {N} | ~{pct}% | {chapter_list} |
| {secondary_1} | {N} | ~{pct}% | {chapter_list} |
| ... | ... | ... | ... |

### Chapter Detail

| Ch | Title | Core Conflict | POV | Word Target | Characters | Foreshadowing Plant | Foreshadowing Resolve | Pleasure Point |
|----|-------|---------------|-----|-------------|------------|---------------------|----------------------|----------------|
| 1 | {title} | {conflict} | {pov} | {words} | {chars} | {plant} | — | {pleasure_type} |
| 2 | {title} | {conflict} | {pov} | {words} | {chars} | {plant} | — | {pleasure_type} |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

## VI. Style & Narrative Specification

### Narrative Mode

| Dimension | Value |
|-----------|-------|
| **POV** | {pov_type} |
| **POV Character(s)** | {pov_characters} |
| **POV Rotation** | (if multi-POV) Primary: {name} ~{pct}%, Secondary: {name} ~{pct}%, ... |
| **Tense** | {tense} |

### Prose Style

| Dimension | Value |
|-----------|-------|
| **Style Descriptor** | {style_descriptor} |
| **Density** | {density} |
| **Register** | {register} |
| **Tone** | {tone} |

### Reader Experience Targets

| Dimension | Value |
|-----------|-------|
| **Target Reader Profiles** | {reader_profiles} |
| **Emotional Pull** | {curiosity/empathy/tension/warmth/next-click strategy} |
| **Anti-Stiffness Rules** | {what to avoid: summary voice, overly archaic phrasing, plot-report narration} |
| **Revision Loop** | Draft pass -> reader-view pass -> style-assimilation pass -> final polish pass |

### Ingredient Style Assimilation Plan

| Dimension | Value |
|-----------|-------|
| **Style Guide Path** | `sources/ingredient_style_guide.md` |
| **Craft Signals To Use** | {rhythm/dialogue/sensory/action/emotion/hook signals} |
| **Hard Boundary** | Never copy plot points, character designs, scene order, or prose passages |

### Rhythm Targets

| Dimension | Target |
|-----------|--------|
| **Chapter Word Count** | {min}–{max} words |
| **Dialogue Ratio** | ≥{dialogue_ratio}% |
| **Pleasure Points** | ≥1 per chapter |
| **Cliffhanger** | Every chapter ending |

### Pleasure-Point Mix (Target Distribution)

| Type | Target Frequency | Notes |
|------|-----------------|-------|
| Power-up (升级) | Every 3–5 chapters | |
| Face-slap (打脸) | Every 5–10 chapters | |
| Reward (收获) | Every 3–5 chapters | |
| Reveal (揭秘) | Every 5–8 chapters | |
| Romance beat (感情升温) | Every 8–15 chapters | |

### Forbidden Patterns (雷区)

1. {forbidden_1}
2. {forbidden_2}
3. {forbidden_3}

---

## VII. Foreshadowing Registry

| ID | Description | Plant Chapter | Planned Resolve Chapter | Urgency | Status |
|----|-------------|---------------|------------------------|---------|--------|
| fs_001 | {description} | {ch} | {ch} | {urgency} | active |
| fs_002 | {description} | {ch} | {ch} | {urgency} | active |
| ... | ... | ... | ... | ... | ... |

---

## VIII. Reference Materials

> Listed for the Writer's awareness. These are context resources, not constraints.

| Material | Type | Path | Relevance |
|----------|------|------|-----------|
| {name} | {type} | {path} | {what to learn from it} |
| ... | ... | ... | ... |

---

## IX. Technical Constraints Reminder

> This section is for AI agents executing the pipeline. It summarizes critical constraints that must not be violated during chapter generation.

1. **spec_lock re-read**: Writer MUST `read_file <project_path>/framework/spec_lock.md` before every chapter
2. **context_summary re-read**: Writer MUST `read_file <project_path>/tracking/context_summary.md` before every chapter
3. **Frontmatter required**: Every chapter file MUST have complete YAML frontmatter
4. **Tracker update**: After every chapter, update all three tracking files
5. **POV discipline**: Never slip into omniscient narration from third-person limited
6. **Pleasure-point minimum**: Every chapter MUST have ≥1 pleasure point
7. **Cliffhanger requirement**: Every chapter MUST end with a hook
8. **Show don't tell**: Emotions, power, beauty, relationships — demonstrate through action and sensory detail
9. **Platform compliance**: Avoid sensitive content; maintain age-appropriate material
10. **Export encoding**: TXT exports MUST use UTF-8 with BOM for platform compatibility
