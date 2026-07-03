#!/usr/bin/env python3
"""Reference search for novel world-building validation.

Usage:
    python3 scripts/reference_search.py <project_path> [--topic <topic>]

Searches for:
  - Historical/cultural references relevant to the world setting
  - Scientific/technical validation for sci-fi elements
  - Comparable works for style/trope reference
  - Image references for scene visualization

Reads spec_lock.md to determine what references are needed.
Outputs findings to sources/reference_search.md.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def cmd_search(project_path_str: str, topic: str | None = None) -> None:
    """Search for reference materials based on project framework.

    Reads spec_lock.md to identify items tagged for external reference.
    Outputs findings to sources/reference_search.md.
    """
    project_path = Path(project_path_str).resolve()
    spec_lock_path = project_path / "framework" / "spec_lock.md"

    if not spec_lock_path.exists():
        print("[ERROR] spec_lock.md not found — run Architect phase first")
        sys.exit(1)

    # Placeholder: in full implementation, this would:
    # 1. Parse spec_lock.md for §ingredients.external_references entries
    # 2. Search web for each reference topic
    # 3. Compile findings into structured Markdown
    output_path = project_path / "sources" / "reference_search.md"
    output_path.write_text(
        f"# Reference Search Results\n\n"
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"> Project: {project_path.name}\n\n"
        f"## Search Topics\n\n"
        f"_Run reference_search.py with web access to populate._\n",
        encoding="utf-8",
    )

    print(f"[OK] Reference search template written to {output_path}")
    print("   This is a placeholder — full implementation requires web search integration.")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: reference_search.py <project_path> [--topic <topic>]")
        sys.exit(1)

    project_path = sys.argv[1]
    topic = None
    if "--topic" in sys.argv:
        idx = sys.argv.index("--topic")
        if idx + 1 < len(sys.argv):
            topic = sys.argv[idx + 1]

    cmd_search(project_path, topic)


if __name__ == "__main__":
    main()
