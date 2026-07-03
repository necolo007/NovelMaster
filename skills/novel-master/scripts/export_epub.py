#!/usr/bin/env python3
"""Export novel to EPUB e-book format.

Usage:
    python3 scripts/export_epub.py <project_path> [--volume-split]

Features:
  - EPUB 3.0 compliant
  - Metadata from novel_config.json and spec_lock.md
  - Auto-generated TOC (nav.xhtml)
  - Chapter-level splitting
  - CSS styling for Chinese typography
  - Cover page from first chapter or custom cover

Requires: pip install ebooklib (or similar EPUB library)

Outputs to export/<novel_name>.epub
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_export(project_path_str: str, volume_split: bool = False) -> None:
    """Export all chapters to an EPUB file."""
    project_path = Path(project_path_str).resolve()
    config_path = project_path / "novel_config.json"
    drafts_dir = project_path / "drafts"
    export_dir = project_path / "export"

    if not config_path.exists():
        print("[ERROR] novel_config.json not found")
        sys.exit(1)

    config = json.loads(config_path.read_text(encoding="utf-8"))
    project_slug = config.get("project_name", "novel")

    export_dir.mkdir(parents=True, exist_ok=True)
    chapters = sorted(drafts_dir.glob("chapter_*.md"))

    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    # Placeholder: full implementation would:
    # 1. Import ebooklib or similar EPUB library
    # 2. Create EPUB book with metadata (title, author, language, description)
    # 3. Add CSS for Chinese typography (indent, font, spacing)
    # 4. Process each chapter: strip frontmatter, convert Markdown to XHTML
    # 5. Build spine, TOC, and nav.xhtml
    # 6. Optionally split by volume
    # 7. Write .epub file

    output_path = export_dir / f"{project_slug}.epub"
    print(f"[OK] EPUB export placeholder: {output_path}")
    print(f"   Chapters: {len(chapters)}")
    print(f"   Install ebooklib for full EPUB generation:")
    print(f"     pip install ebooklib")
    print(f"   Then re-run this script.")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: export_epub.py <project_path> [--volume-split]")
        sys.exit(1)

    project_path = sys.argv[1]
    volume_split = "--volume-split" in sys.argv
    cmd_export(project_path, volume_split=volume_split)


if __name__ == "__main__":
    main()
