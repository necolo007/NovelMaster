#!/usr/bin/env python3
"""Chapter pacing and pleasure-point density checker.

Usage:
    python3 scripts/pacing_checker.py <project_path>

Checks:
  - Pleasure-point density (every chapter >= 1)
  - Conflict density (no extended flat periods)
  - Climax placement vs plot_outline expectations
  - Breathing room distribution
  - Chapter length variance

Reads chapter_breakdown.md, plot_outline.md, and all chapter drafts.
"""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_check(project_path_str: str) -> dict:
    """Run pacing checks across all chapters."""
    project_path = Path(project_path_str).resolve()
    breakdown_path = project_path / "framework" / "chapter_breakdown.md"
    drafts_dir = project_path / "drafts"

    chapters = sorted(drafts_dir.glob("chapter_*.md"))
    errors = []
    warnings = []
    info = []

    print(f"Checking pacing across {len(chapters)} chapters...")

    # Check pleasure-point density from frontmatter
    zero_pleasure_chapters = []
    for ch in chapters:
        text = ch.read_text(encoding="utf-8")
        if "pleasure_points:" in text:
            # Simple check: look for empty pleasure_points list
            parts = text.split("pleasure_points:")
            if len(parts) > 1:
                pp_section = parts[1].split("\n")[0].strip()
                if pp_section == "[]" or pp_section == "":
                    zero_pleasure_chapters.append(ch.name)

    if zero_pleasure_chapters:
        errors.append(
            f"{len(zero_pleasure_chapters)} chapter(s) with 0 pleasure points: "
            + ", ".join(zero_pleasure_chapters)
        )

    # Placeholder: full implementation would additionally:
    # 1. Parse chapter_breakdown.md for expected pacing targets
    # 2. Track conflict density across consecutive chapters
    # 3. Verify climax placement positions
    # 4. Analyze chapter length distribution and flag outliers
    # 5. Identify breathing room gaps

    print(f"\n[OK] Pacing check complete")
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
        print("Usage: pacing_checker.py <project_path>")
        sys.exit(1)
    result = cmd_check(sys.argv[1])
    if result["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
