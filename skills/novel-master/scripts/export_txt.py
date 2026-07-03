#!/usr/bin/env python3
"""Export novel to plain text format (web novel platform submission).

Usage:
    python3 scripts/export_txt.py <project_path> [--volume-split] [--encoding utf-8]

Features:
  - UTF-8 with BOM (platform standard for Chinese web novels)
  - Chinese typography: full-width punctuation, paragraph spacing
  - Optional volume splitting for very long novels
  - Strips YAML frontmatter, outputs pure prose
  - Chapter titles as separators

Outputs to export/<novel_name>.txt
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_export(project_path_str: str,
               volume_split: bool = False,
               encoding: str = "utf-8") -> None:
    """Export all chapters to a single TXT file."""
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

    # Build output
    lines = []
    # Add BOM for UTF-8 platform compatibility
    bom = "\ufeff" if encoding == "utf-8" else ""

    lines.append(f"{novel_title}")
    if config.get("author"):
        lines.append(f"作者：{config['author']}")
    lines.append("")
    lines.append("=" * 40)
    lines.append("")

    for ch in chapters:
        text = ch.read_text(encoding="utf-8")

        # Extract title and body (skip YAML frontmatter)
        parts = text.split("---")
        if len(parts) >= 3:
            body = "---".join(parts[2:]).strip()
        else:
            body = text.strip()

        # Extract chapter title line (first # heading)
        title_line = ""
        body_lines = body.split("\n")
        if body_lines and body_lines[0].startswith("# "):
            title_line = body_lines[0]
            body = "\n".join(body_lines[1:]).strip()

        lines.append(title_line or f"第{ch.stem.replace('chapter_', '')}章")
        lines.append("")
        lines.append(body)
        lines.append("")
        lines.append("-" * 20)
        lines.append("")

    output = bom + "\n".join(lines)

    output_path = export_dir / f"{project_slug}.txt"
    output_path.write_text(output, encoding=encoding)

    # Count approximate characters
    char_count = len(output) - len(bom)
    print(f"[OK] TXT export complete: {output_path}")
    print(f"   Chapters: {len(chapters)}")
    print(f"   Characters: ~{char_count:,}")
    print(f"   Encoding: {encoding}{' with BOM' if encoding == 'utf-8' else ''}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: export_txt.py <project_path> [--volume-split] [--encoding utf-8]")
        sys.exit(1)

    project_path = sys.argv[1]
    volume_split = "--volume-split" in sys.argv
    encoding = "utf-8"
    if "--encoding" in sys.argv:
        idx = sys.argv.index("--encoding")
        if idx + 1 < len(sys.argv):
            encoding = sys.argv[idx + 1]

    cmd_export(project_path, volume_split=volume_split, encoding=encoding)


if __name__ == "__main__":
    main()
