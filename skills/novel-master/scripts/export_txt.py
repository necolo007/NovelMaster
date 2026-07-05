#!/usr/bin/env python3
"""Export a NovelMaster project to a single TXT file.

Usage:
    python skills/novel-master/scripts/export_txt.py <project_path> [--encoding utf-8]

Outputs:
    <project_path>/export/<project_name>.txt
"""

from __future__ import annotations

import argparse
import sys

from novel_utils import ensure_export_dir, load_chapters, load_config, project_slug, project_title, resolve_project


def cmd_export(project_path_str: str, encoding: str = "utf-8") -> None:
    project_path = resolve_project(project_path_str)
    config = load_config(project_path)
    chapters = load_chapters(project_path)

    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    lines: list[str] = [
        project_title(config, project_path),
    ]
    if config.get("author"):
        lines.append(f"Author: {config['author']}")
    lines.extend(["", "=" * 40, ""])

    for chapter in chapters:
        lines.append(f"Chapter {chapter.number:03d} {chapter.title}")
        lines.append("")
        lines.append(chapter.plain_text)
        lines.extend(["", "-" * 20, ""])

    content = "\n".join(lines).strip() + "\n"
    if encoding.lower().replace("_", "-") == "utf-8":
        content = "\ufeff" + content

    export_dir = ensure_export_dir(project_path)
    output_path = export_dir / f"{project_slug(config, project_path)}.txt"
    output_path.write_text(content, encoding=encoding)

    char_count = len(content.lstrip("\ufeff"))
    print(f"[OK] TXT export complete: {output_path}")
    print(f"   Chapters: {len(chapters)}")
    print(f"   Characters: ~{char_count:,}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a NovelMaster project to TXT.")
    parser.add_argument("project_path")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--volume-split", action="store_true", help="Accepted for compatibility; not used yet.")
    args = parser.parse_args()

    try:
        cmd_export(args.project_path, encoding=args.encoding)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
