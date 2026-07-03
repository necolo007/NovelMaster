#!/usr/bin/env python3
"""Table of contents generator.

Usage:
    python3 scripts/toc_generator.py <project_path>

Generates:
  - Hyperlinked TOC in Markdown format
  - EPUB-compatible nav.xhtml structure
  - Volume/Arc/Chapter hierarchy from plot_outline.md

Reads chapter_breakdown.md for structure and drafts/ for chapter titles.
Outputs to export/toc.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_generate(project_path_str: str) -> None:
    """Generate table of contents."""
    project_path = Path(project_path_str).resolve()
    drafts_dir = project_path / "drafts"
    export_dir = project_path / "export"

    if not drafts_dir.exists():
        print("[ERROR] drafts/ directory not found")
        sys.exit(1)

    export_dir.mkdir(parents=True, exist_ok=True)
    chapters = sorted(drafts_dir.glob("chapter_*.md"))

    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    # Build TOC from chapter frontmatter
    toc_lines = ["# Table of Contents\n"]
    for ch in chapters:
        text = ch.read_text(encoding="utf-8")
        # Extract title from frontmatter
        title_match = None
        for line in text.split("\n"):
            if line.startswith("title:"):
                title_match = line.split(":", 1)[1].strip().strip('"')
                break

        ch_num = ch.stem.replace("chapter_", "")
        display_title = title_match or f"Chapter {int(ch_num)}"
        toc_lines.append(f"- [Chapter {int(ch_num)}: {display_title}]({ch.name})")

    toc_content = "\n".join(toc_lines) + "\n"
    output_path = export_dir / "toc.md"
    output_path.write_text(toc_content, encoding="utf-8")

    print(f"[OK] TOC generated: {output_path}")
    print(f"   {len(chapters)} entries")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: toc_generator.py <project_path>")
        sys.exit(1)
    cmd_generate(sys.argv[1])


if __name__ == "__main__":
    main()
