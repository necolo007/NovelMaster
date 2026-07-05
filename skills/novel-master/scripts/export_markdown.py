#!/usr/bin/env python3
"""Export a NovelMaster project to a single Markdown collection.

Usage:
    python skills/novel-master/scripts/export_markdown.py <project_path>

Outputs:
    <project_path>/export/<project_name>.md
"""

from __future__ import annotations

import argparse
import sys

from novel_utils import chapter_anchor, ensure_export_dir, load_chapters, load_config, project_slug, project_title, resolve_project


def cmd_export(project_path_str: str, include_frontmatter: bool = False) -> None:
    project_path = resolve_project(project_path_str)
    config = load_config(project_path)
    chapters = load_chapters(project_path)

    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    title = project_title(config, project_path)
    lines: list[str] = [f"# {title}", ""]
    if config.get("author"):
        lines.extend([f"Author: {config['author']}", ""])
    lines.extend(
        [
            f"> Genre: {config.get('genre_label') or config.get('genre') or 'N/A'}",
            f"> Chapters: {len(chapters)}",
            f"> Language: {config.get('language', 'zh-CN')}",
            "",
            "## Table of Contents",
            "",
        ]
    )

    for chapter in chapters:
        lines.append(f"- [Chapter {chapter.number:03d} {chapter.title}](#{chapter_anchor(chapter)})")

    lines.append("")

    for chapter in chapters:
        lines.append(f'<a id="{chapter_anchor(chapter)}"></a>')
        lines.append("")
        lines.append(f"## Chapter {chapter.number:03d} {chapter.title}")
        lines.append("")
        if include_frontmatter and chapter.metadata:
            lines.append("```yaml")
            for key, value in chapter.metadata.items():
                lines.append(f"{key}: {value}")
            lines.append("```")
            lines.append("")
        lines.append(chapter.body_markdown.strip())
        lines.extend(["", "---", ""])

    content = "\n".join(lines).strip() + "\n"
    export_dir = ensure_export_dir(project_path)
    output_path = export_dir / f"{project_slug(config, project_path)}.md"
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Markdown export complete: {output_path}")
    print(f"   Chapters: {len(chapters)}")
    print(f"   Characters: ~{len(content):,}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a NovelMaster project to Markdown.")
    parser.add_argument("project_path")
    parser.add_argument("--include-frontmatter", action="store_true")
    parser.add_argument("--no-frontmatter", action="store_true", help="Accepted for compatibility; default behavior.")
    parser.add_argument("--volume-split", action="store_true", help="Accepted for compatibility; not used yet.")
    args = parser.parse_args()

    try:
        cmd_export(args.project_path, include_frontmatter=args.include_frontmatter)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
