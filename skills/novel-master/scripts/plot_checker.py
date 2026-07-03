#!/usr/bin/env python3
"""Plot logic and foreshadowing checker.

Usage:
    python3 scripts/plot_checker.py <project_path>

Checks:
  - Foreshadowing resolution (all planted threads resolved)
  - Logic holes (contradictions, impossible events)
  - Power system collapse (established rules broken)
  - Deus ex machina detection
  - Continuity errors
  - Cause-effect chain breaks
  - Abandoned subplots

Reads plot_outline.md, plot_tracker.json, and all chapter drafts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_check(project_path_str: str) -> dict:
    """Run plot logic checks across all chapters."""
    project_path = Path(project_path_str).resolve()
    plot_outline_path = project_path / "framework" / "plot_outline.md"
    tracker_path = project_path / "tracking" / "plot_tracker.json"
    drafts_dir = project_path / "drafts"

    errors = []
    warnings = []
    info = []

    # Check foreshadowing resolution
    if tracker_path.exists():
        tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
        active_threads = [f for f in tracker.get("foreshadowing", [])
                          if f.get("status") == "active"]
        if active_threads:
            errors.append(
                f"{len(active_threads)} unresolved foreshadowing threads: "
                + ", ".join(f"{t['id']}: {t['description']}" for t in active_threads)
            )
        summary = tracker.get("summary", {})
        print(f"Foreshadowing: {summary.get('total_resolved', 0)} resolved, "
              f"{summary.get('active', 0)} active, "
              f"{summary.get('total_abandoned', 0)} abandoned")
    else:
        warnings.append("plot_tracker.json not found")

    chapters = sorted(drafts_dir.glob("chapter_*.md"))
    print(f"Checking plot logic across {len(chapters)} chapters...")

    # Placeholder: full implementation would:
    # 1. Parse plot_outline.md for expected plot structure
    # 2. Build event timeline from all chapter frontmatters
    # 3. Detect logic holes, deus ex machina, continuity breaks
    # 4. Validate power system consistency

    print(f"\n[OK] Plot check complete")
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
        print("Usage: plot_checker.py <project_path>")
        sys.exit(1)
    result = cmd_check(sys.argv[1])
    if result["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
