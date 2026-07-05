#!/usr/bin/env python3
"""Archive chapter batches and build rolling memory files for long novels.

Usage:
    python skills/novel-master/scripts/chapter_memory.py <project_path> [--span 10]
    python skills/novel-master/scripts/chapter_memory.py <project_path> --span 20 --copy-chapters

Outputs:
    <project_path>/memory/chapters_001_010/
    <project_path>/memory/memory_index.md
    <project_path>/tracking/latest_memory.md

The script copies chapters into memory folders for lookup convenience, but it never
moves or deletes files from drafts/. Export and web-preview scripts should continue
to use drafts/ as the source of truth.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from novel_utils import Chapter, load_chapters, load_config, project_title, resolve_project


DEFAULT_SPAN = 10


def cmd_archive(
    project_path_str: str,
    span: int | None = None,
    copy_chapters: bool = True,
    include_incomplete: bool = False,
) -> None:
    project_path = resolve_project(project_path_str)
    config = load_config(project_path)
    chapters = load_chapters(project_path)
    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    archive_span = span or int(config.get("memory_archive_interval") or DEFAULT_SPAN)
    if archive_span <= 0:
        raise ValueError("--span must be greater than 0")

    memory_dir = project_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

    groups = group_chapters(chapters, archive_span, include_incomplete=include_incomplete)
    if not groups:
        print(f"[WARN] No complete {archive_span}-chapter group found. Use --include-incomplete to archive the current partial group.")
        return

    generated_groups = []
    for group in groups:
        group_dir = memory_dir / group_name(group)
        group_dir.mkdir(parents=True, exist_ok=True)
        write_group_files(project_path, config, group, group_dir, copy_chapters=copy_chapters)
        generated_groups.append(group_dir)

    write_memory_index(project_path, config, groups, memory_dir)
    write_latest_memory(project_path, generated_groups[-1])

    print(f"[OK] Chapter memory archived: {memory_dir}")
    print(f"   Span: {archive_span}")
    print(f"   Groups: {len(generated_groups)}")
    print(f"   Latest memory: {project_path / 'tracking' / 'latest_memory.md'}")


def group_chapters(chapters: list[Chapter], span: int, include_incomplete: bool) -> list[list[Chapter]]:
    groups: list[list[Chapter]] = []
    by_number = {chapter.number: chapter for chapter in chapters}
    if not by_number:
        return groups

    first = min(by_number)
    last = max(by_number)
    start = first - ((first - 1) % span)

    while start <= last:
        end = start + span - 1
        group = [by_number[number] for number in range(start, end + 1) if number in by_number]
        complete = len(group) == span
        if group and (complete or include_incomplete):
            groups.append(group)
        start += span

    return groups


def group_name(group: list[Chapter]) -> str:
    return f"chapters_{group[0].number:03d}_{group[-1].number:03d}"


def write_group_files(project_path: Path, config: dict, group: list[Chapter], group_dir: Path, copy_chapters: bool) -> None:
    if copy_chapters:
        chapters_dir = group_dir / "chapters"
        chapters_dir.mkdir(parents=True, exist_ok=True)
        for chapter in group:
            shutil.copy2(chapter.path, chapters_dir / chapter.path.name)

    (group_dir / "README.md").write_text(group_readme(config, group), encoding="utf-8")
    (group_dir / "chapter_summaries.md").write_text(chapter_summaries(group), encoding="utf-8")
    (group_dir / "continuity_memory.md").write_text(continuity_memory(project_path, config, group), encoding="utf-8")
    (group_dir / "chapters_manifest.json").write_text(
        json.dumps(chapters_manifest(project_path, group), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def group_readme(config: dict, group: list[Chapter]) -> str:
    title = config.get("title") or config.get("project_name") or "Novel"
    return "\n".join(
        [
            f"# {title} - Chapter Memory {group[0].number:03d}-{group[-1].number:03d}",
            "",
            f"- Chapters: {len(group)}",
            f"- Words: {sum(chapter.word_count for chapter in group)}",
            f"- Generated at: {datetime.now(timezone.utc).isoformat()}",
            "",
            "## Files",
            "",
            "- `chapter_summaries.md`: per-chapter lookup notes",
            "- `continuity_memory.md`: compact memory for future chapter generation",
            "- `chapters_manifest.json`: structured chapter metadata",
            "- `chapters/`: copied source chapters for local search",
            "",
            "Keep `drafts/` as the source of truth. This folder is a lookup and memory layer.",
            "",
        ]
    )


def chapter_summaries(group: list[Chapter]) -> str:
    lines = [f"# Chapter Summaries {group[0].number:03d}-{group[-1].number:03d}", ""]
    for chapter in group:
        lines.extend(
            [
                f"## Chapter {chapter.number:03d} {chapter.title}",
                "",
                f"- Words: {chapter.word_count}",
                f"- POV: {chapter.metadata.get('pov', '')}",
                f"- Characters: {format_list(chapter.metadata.get('characters_appearing', []))}",
                f"- Foreshadowing planted: {format_list(chapter.metadata.get('foreshadowing_planted', []))}",
                f"- Foreshadowing resolved: {format_list(chapter.metadata.get('foreshadowing_resolved', []))}",
                "",
                "### Quick Recall",
                "",
                summarize_plain_text(chapter.plain_text),
                "",
            ]
        )
    return "\n".join(lines)


def continuity_memory(project_path: Path, config: dict, group: list[Chapter]) -> str:
    tracking_dir = project_path / "tracking"
    context_summary = read_optional(tracking_dir / "context_summary.md")
    plot_tracker = read_optional(tracking_dir / "plot_tracker.json")
    character_state = read_optional(tracking_dir / "character_state.json")

    lines = [
        f"# Continuity Memory {group[0].number:03d}-{group[-1].number:03d}",
        "",
        f"Novel: {project_title(config, project_path)}",
        f"Chapter range: {group[0].number:03d}-{group[-1].number:03d}",
        f"Total words in range: {sum(chapter.word_count for chapter in group)}",
        "",
        "## Read Before Writing Later Chapters",
        "",
        "- This memory is a compact lookup layer for long-form continuation.",
        "- Read this file together with `framework/spec_lock.md`, `tracking/context_summary.md`, `tracking/plot_tracker.json`, and `tracking/character_state.json`.",
        "- If this file conflicts with a newer tracker, the newer tracker wins.",
        "",
        "## Range Spine",
        "",
    ]

    for chapter in group:
        lines.append(f"- Chapter {chapter.number:03d} `{chapter.title}`: {one_line_recall(chapter.plain_text)}")

    lines.extend(
        [
            "",
            "## Character And Plot Memory To Preserve",
            "",
            "Fill or refine this section after AI/editor review when a deeper semantic summary is needed.",
            "",
            "### Character deltas",
            "",
            "- TBD",
            "",
            "### Relationship deltas",
            "",
            "- TBD",
            "",
            "### Power / item / secret deltas",
            "",
            "- TBD",
            "",
            "### Open hooks after this range",
            "",
            "- TBD",
            "",
        ]
    )

    if context_summary:
        lines.extend(["## Current Rolling Context Snapshot", "", fenced("markdown", context_summary), ""])
    if plot_tracker:
        lines.extend(["## Plot Tracker Snapshot", "", fenced("json", plot_tracker), ""])
    if character_state:
        lines.extend(["## Character State Snapshot", "", fenced("json", character_state), ""])

    return "\n".join(lines)


def chapters_manifest(project_path: Path, group: list[Chapter]) -> dict:
    return {
        "range": {"from": group[0].number, "to": group[-1].number},
        "chapters": [
            {
                "number": chapter.number,
                "title": chapter.title,
                "source_path": chapter.path.relative_to(project_path).as_posix(),
                "word_count": chapter.word_count,
                "metadata": chapter.metadata,
            }
            for chapter in group
        ],
    }


def write_memory_index(project_path: Path, config: dict, groups: list[list[Chapter]], memory_dir: Path) -> None:
    lines = [
        f"# Memory Index - {project_title(config, project_path)}",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Archives",
        "",
    ]
    for group in groups:
        name = group_name(group)
        lines.append(f"- [{name}]({name}/continuity_memory.md): chapters {group[0].number:03d}-{group[-1].number:03d}, {sum(chapter.word_count for chapter in group)} words")
    lines.append("")
    (memory_dir / "memory_index.md").write_text("\n".join(lines), encoding="utf-8")


def write_latest_memory(project_path: Path, latest_group_dir: Path) -> None:
    tracking_dir = project_path / "tracking"
    tracking_dir.mkdir(parents=True, exist_ok=True)
    latest = tracking_dir / "latest_memory.md"
    source = latest_group_dir / "continuity_memory.md"
    latest.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def format_list(value) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value or "")


def summarize_plain_text(text: str, max_chars: int = 520) -> str:
    if len(text) <= max_chars:
        return text
    head = text[: max_chars // 2].strip()
    tail = text[-max_chars // 2 :].strip()
    return f"{head}\n\n...\n\n{tail}"


def one_line_recall(text: str, max_chars: int = 140) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_chars:
        return clean
    return clean[: max_chars - 1].rstrip() + "..."


def read_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8-sig").strip()


def fenced(language: str, content: str) -> str:
    return f"```{language}\n{content}\n```"


def main() -> None:
    parser = argparse.ArgumentParser(description="Archive chapter batches and build long-novel memory files.")
    parser.add_argument("project_path")
    parser.add_argument("--span", type=int, default=None, help="Archive size, usually 10 or 20 chapters.")
    parser.add_argument("--copy-chapters", action="store_true", default=True, help="Copy source chapters into each memory folder.")
    parser.add_argument("--no-copy-chapters", action="store_false", dest="copy_chapters")
    parser.add_argument("--include-incomplete", action="store_true", help="Also archive the current partial range.")
    args = parser.parse_args()

    try:
        cmd_archive(
            args.project_path,
            span=args.span,
            copy_chapters=args.copy_chapters,
            include_incomplete=args.include_incomplete,
        )
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
