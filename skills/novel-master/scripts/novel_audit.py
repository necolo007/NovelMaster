#!/usr/bin/env python3
"""Full novel audit orchestrator — runs all 5 checkers and aggregates results.

Usage:
    python3 scripts/novel_audit.py <project_path>

Runs in order:
  1. consistency_checker.py  — name, timeline, item, location consistency
  2. character_checker.py    — personality, voice, relationship, power growth
  3. plot_checker.py         — foreshadowing, logic holes, power system
  4. style_checker.py        — POV, dialogue ratio, tone, exposition
  5. pacing_checker.py       — pleasure points, conflict density, climax

Exits with code 1 if any checker reports errors.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent

CHECKERS = [
    ("consistency_checker.py", "Consistency"),
    ("character_checker.py", "Character"),
    ("plot_checker.py", "Plot"),
    ("style_checker.py", "Style"),
    ("pacing_checker.py", "Pacing"),
]


def cmd_audit(project_path_str: str) -> dict:
    """Run all 5 checkers and aggregate results."""
    project_path = Path(project_path_str).resolve()

    if not project_path.exists():
        print(f"[ERROR] Project not found: {project_path}")
        sys.exit(1)

    results = {}
    total_errors = 0
    total_warnings = 0
    total_info = 0

    print(f"=== Novel Audit: {project_path.name} ===\n")

    for script_name, label in CHECKERS:
        script_path = TOOLS_DIR / script_name
        if not script_path.exists():
            print(f"  [{label}] [WARN] Script not found: {script_name}")
            continue

        print(f"--- {label} Check ---")
        result = subprocess.run(
            [sys.executable, str(script_path), str(project_path)],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        # Parse result from exit code and output
        if result.returncode != 0:
            # Errors detected
            results[label.lower()] = "FAIL"
        else:
            results[label.lower()] = "PASS"

    print("\n=== Audit Summary ===")
    for label, status in results.items():
        marker = "[OK]" if status == "PASS" else "[FAIL]"
        print(f"  {marker} {label}")

    has_failures = any(s == "FAIL" for s in results.values())
    if has_failures:
        print("\n[FAIL] Audit found errors — fix before export.")
        sys.exit(1)
    else:
        print("\n[OK] All checks passed — ready for export.")

    return results


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: novel_audit.py <project_path>")
        sys.exit(1)
    cmd_audit(sys.argv[1])


if __name__ == "__main__":
    main()
