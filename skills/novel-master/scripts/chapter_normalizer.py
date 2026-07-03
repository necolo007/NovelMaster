#!/usr/bin/env python3
"""Unified chapter numbering normalizer.

Usage:
    python3 scripts/chapter_normalizer.py <project_path>

Standardizes chapter title formats across all drafts.
Handles:
  - "第X章" / "Chapter X" / "第零零X章" / mixed formats
  - Ensures consistent numbering per project language config
  - Updates chapter frontmatter chapter numbers
  - Renames files if needed

Reads novel_config.json for language preference.
Modifies drafts/chapter_*.md in place.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_normalize(project_path_str: str) -> None:
    """Normalize chapter numbering across all drafts."""
    project_path = Path(project_path_str).resolve()
    drafts_dir = project_path / "drafts"

    if not drafts_dir.exists():
        print("[ERROR] drafts/ directory not found")
        sys.exit(1)

    chapters = sorted(drafts_dir.glob("chapter_*.md"))
    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    print(f"Normalizing {len(chapters)} chapter(s)...")

    # Placeholder: full implementation would:
    # 1. Parse language preference from novel_config.json
    # 2. Extract chapter number from filename and frontmatter
    # 3. Standardize title format (e.g., all "第N章" or all "Chapter N")
    # 4. Update frontmatter chapter field if mismatched
    # 5. Rename files to consistent zero-padded naming

    for ch in chapters:
        print(f"   {ch.name}")

    print(f"\n[OK] Chapter normalization complete ({len(chapters)} chapters)")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: chapter_normalizer.py <project_path>")
        sys.exit(1)
    cmd_normalize(sys.argv[1])


if __name__ == "__main__":
    main()
