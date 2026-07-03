# AGENTS.md

This file is the project entry point for general AI agents.

Before any novel generation task, **you MUST first read [`skills/novel-master/SKILL.md`](skills/novel-master/SKILL.md)** — the authoritative workflow for project creation, role switching, serial execution, quality gates, post-processing, and export.

## Project Overview

Novel Master is an AI-driven web novel generation system. Multi-role collaboration (Architect → Writer → Editor) converts inspiration and ideas into complete web novels with consistency tracking and multi-format export.

**Core Pipeline**: `Inspiration → Create Project → [Genre Template] → Architect Six Confirmations → [Reference Search] → Writer Chapter-by-Chapter → Editor Audit → Post-processing → Export`

> Topic-only requests with no source material: run the standalone [`topic-brainstorm`](skills/novel-master/workflows/topic-brainstorm.md) workflow before SKILL.md Step 1 to gather inspiration and world-building materials.
>
> Resuming a project after the framework phase (split-mode execution): when the user opens a fresh chat and says "继续写作 projects/<x>" or similar, run the standalone [`resume-writing`](skills/novel-master/workflows/resume-writing.md) workflow to enter the Writer phase without re-running the Architect phase.
>
> Revising a single chapter: run the standalone [`revise-chapter`](skills/novel-master/workflows/revise-chapter.md) workflow to modify a chapter and auto-update trackers.
>
> Expanding a brief outline: run the standalone [`expand-outline`](skills/novel-master/workflows/expand-outline.md) workflow to flesh out a rough outline into a detailed chapter breakdown.
>
> Character deep-dive / side story: run the standalone [`character-deep-dive`](skills/novel-master/workflows/character-deep-dive.md) workflow to generate a character's backstory or standalone arc.

## Execution Requirements

- Read [`skills/novel-master/SKILL.md`](skills/novel-master/SKILL.md) before starting a novel task.
- Role-specific rules live in [`skills/novel-master/references/`](skills/novel-master/references/).
- Web novel writing constraints live in [`skills/novel-master/references/shared-standards.md`](skills/novel-master/references/shared-standards.md).
- Framework spec template lives in [`skills/novel-master/templates/framework_spec_reference.md`](skills/novel-master/templates/framework_spec_reference.md).
- Ingredient (reference material) lives in `ingredient/` and per-project `sources/`.

## Compatibility Boundary

- This repository is a workflow/skill package, not an app or service scaffold.
- Do NOT assume conventions like `.worktrees/`, `tests/`, or mandatory branch setup unless the user explicitly requests them.
- On conflict with a generic coding skill, prioritize [`skills/novel-master/SKILL.md`](skills/novel-master/SKILL.md) and this file inside this repository.

## Command Quick Reference

Convenience summary only — full workflow in [`skills/novel-master/SKILL.md`](skills/novel-master/SKILL.md).

```bash
# Project management
python3 skills/novel-master/scripts/project_manager.py init <novel_name> --genre <genre>
python3 skills/novel-master/scripts/project_manager.py import-sources <project_path> <source_files...> --move
python3 skills/novel-master/scripts/project_manager.py validate <project_path>

# Reference search (conditional)
python3 skills/novel-master/scripts/reference_search.py <project_path>

# Quality audits
python3 skills/novel-master/scripts/consistency_checker.py <project_path>
python3 skills/novel-master/scripts/character_checker.py <project_path>
python3 skills/novel-master/scripts/plot_checker.py <project_path>
python3 skills/novel-master/scripts/style_checker.py <project_path>
python3 skills/novel-master/scripts/pacing_checker.py <project_path>
python3 skills/novel-master/scripts/novel_audit.py <project_path>

# Post-processing
python3 skills/novel-master/scripts/chapter_normalizer.py <project_path>
python3 skills/novel-master/scripts/toc_generator.py <project_path>
python3 skills/novel-master/scripts/export_txt.py <project_path>
python3 skills/novel-master/scripts/export_epub.py <project_path>
python3 skills/novel-master/scripts/export_markdown.py <project_path>
```

## Core Directories

- `skills/novel-master/SKILL.md` — main workflow authority.
- `skills/novel-master/references/` — role definitions and writing standards.
- `skills/novel-master/scripts/` — runnable tool scripts.
- `skills/novel-master/templates/` — framework templates, spec lock templates, genre templates.
- `skills/novel-master/workflows/` — standalone sub-workflows.
- `skills/novel-master/examples/` — example projects.
- `projects/` — user project workspace.
- `ingredient/` — reference web novels and inspiration material.
