#!/usr/bin/env python3
"""Export novel to Markdown collection.

Usage:
    python3 scripts/export_markdown.py <project_path> [--no-frontmatter] [--volume-split]

Features:
  - Single Markdown file with all chapters
  - Optional YAML frontmatter preservation
  - Auto-generated TOC with anchor links
  - Volume/section dividers
  - GitHub-flavored Markdown compatible

Outputs to export/<novel_name>.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_export(project_path_str: str,
               no_frontmatter: bool = False,
               volume_split: bool = False) -> None:
    """Export all chapters to a single Markdown file."""
    project_path = Path(project_path_str).resolve()
    config_path = project_path / "novel_config.json"
    drafts_dir = project_path / "drafts"
    export_dir = project_path / "export"

    if not config_path.exists():
        print("[ERROR] novel_config.json not found")
        sys.exit(1)

    config = json.loads(config_path.read_text(encoding="utf-8"))
    novel_title = config.get("title", project_path.name)
    project_slug = config.get("project_name", "novel")

    export_dir.mkdir(parents=True, exist_ok=True)
    chapters = sorted(drafts_dir.glob("chapter_*.md"))

    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    lines = []
    lines.append(f"# {novel_title}")
    if config.get("author"):
        lines.append(f"*作者：{config['author']}*")
    lines.append("")
    lines.append(f"> Genre: {config.get('genre_label', config.get('genre', 'N/A'))}")
    lines.append(f"> Chapters: {len(chapters)}")
    lines.append(f"> Language: {config.get('language', 'zh-CN')}")
    lines.append("")

    # TOC
    lines.append("## 目录")
    lines.append("")
    for ch in chapters:
        ch_num = int(ch.stem.replace("chapter_", ""))
        title = ""
        text = ch.read_text(encoding="utf-8")
        for line in text.split("\n"):
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip('"')
                break
        anchor = f"chapter-{ch_num}"
        lines.append(f"- [第{ch_num}章 {title}](#{anchor})")
    lines.append("")

    # Chapter content
    for ch in chapters:
        ch_num = int(ch.stem.replace("chapter_", ""))
        text = ch.read_text(encoding="utf-8")

        if no_frontmatter:
            # Strip YAML frontmatter
            parts = text.split("---")
            if len(parts) >= 3:
                body = "---".join(parts[2:]).strip()
            else:
                body = text.strip()
            lines.append(body)
        else:
            lines.append(text)

        lines.append("")
        lines.append("---")
        lines.append("")

    output_content = "\n".join(lines)
    output_path = export_dir / f"{project_slug}.md"
    output_path.write_text(output_content, encoding="utf-8")

    print(f"[OK] Markdown export complete: {output_path}")
    print(f"   Chapters: {len(chapters)}")
    print(f"   Characters: ~{len(output_content):,}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: export_markdown.py <project_path> [--no-frontmatter] [--volume-split]")
        sys.exit(1)

    project_path = sys.argv[1]
    no_frontmatter = "--no-frontmatter" in sys.argv
    volume_split = "--volume-split" in sys.argv
    cmd_export(project_path, no_frontmatter=no_frontmatter, volume_split=volume_split)


if __name__ == "__main__":
    main()
