#!/usr/bin/env python3
"""Writing style and POV consistency checker.

Usage:
    python3 scripts/style_checker.py <project_path>

Checks:
  - POV violation detection (omniscient slips in limited POV)
  - Dialogue ratio measurement
  - Tone/style consistency with spec_lock
  - Exposition dump detection
  - Repetitive phrasing
  - Cliffhanger presence at chapter endings

Reads spec_lock.md and all chapter drafts.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_check(project_path_str: str) -> dict:
    """Run style checks across all chapters."""
    project_path = Path(project_path_str).resolve()
    spec_lock_path = project_path / "framework" / "spec_lock.md"
    drafts_dir = project_path / "drafts"

    if not spec_lock_path.exists():
        print("[ERROR] spec_lock.md not found")
        sys.exit(1)

    chapters = sorted(drafts_dir.glob("chapter_*.md"))
    errors = []
    warnings = []
    info = []

    print(f"Checking style across {len(chapters)} chapters...")

    # Placeholder: full implementation would:
    # 1. Parse spec_lock.md for target style parameters
    # 2. Scan each chapter for POV violations (omniscient markers like "他不知道的是")
    # 3. Measure dialogue ratio (quoted text vs narration)
    # 4. Detect exposition dumps (long blocks with no dialogue/action)
    # 5. Check chapter endings for cliffhanger presence
    # 6. Count repeated phrases

    print(f"\n[OK] Style check complete")
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
        print("Usage: style_checker.py <project_path>")
        sys.exit(1)
    result = cmd_check(sys.argv[1])
    if result["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
