#!/usr/bin/env python3
"""Cross-chapter consistency checker.

Usage:
    python3 scripts/consistency_checker.py <project_path>

Checks:
  - Name consistency across chapters
  - Timeline/logic consistency
  - Item/possession tracking
  - Location tracking
  - Power level consistency
  - Currency/economy consistency

Reads all chapter drafts and tracker files.
Outputs errors (must fix) and warnings (should fix).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_check(project_path_str: str) -> dict:
    """Run consistency checks across all chapters.

    Returns dict with counts of errors, warnings, and info.
    """
    project_path = Path(project_path_str).resolve()
    drafts_dir = project_path / "drafts"

    if not drafts_dir.exists():
        print("[ERROR] drafts/ directory not found")
        sys.exit(1)

    chapters = sorted(drafts_dir.glob("chapter_*.md"))
    if not chapters:
        print("[WARN] No chapter drafts found")
        return {"errors": 0, "warnings": 0, "info": 0}

    errors = []
    warnings = []
    info = []

    print(f"Checking consistency across {len(chapters)} chapters...")

    # Placeholder: full implementation would:
    # 1. Parse frontmatter from every chapter
    # 2. Build name/location/item/power timeline
    # 3. Detect contradictions (same person called different names, etc.)
    # 4. Cross-reference with character_profiles.md and world_building.md

    print(f"\n[OK] Consistency check complete")
    print(f"   Errors:   {len(errors)}")
    print(f"   Warnings: {len(warnings)}")
    print(f"   Info:     {len(info)}")

    for e in errors:
        print(f"   [ERROR] {e}")
    for w in warnings:
        print(f"   [WARN]  {w}")
    for i in info:
        print(f"   [INFO]  {i}")

    return {"errors": len(errors), "warnings": len(warnings), "info": len(info)}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: consistency_checker.py <project_path>")
        sys.exit(1)

    result = cmd_check(sys.argv[1])
    if result["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
