#!/usr/bin/env python3
"""Export a NovelMaster project to TXT, EPUB, and Markdown."""

from __future__ import annotations

import argparse
import sys

from export_epub import cmd_export as export_epub
from export_markdown import cmd_export as export_markdown
from export_txt import cmd_export as export_txt
from novel_utils import ensure_export_dir, load_chapters, load_config, project_slug, resolve_project


def cmd_export_all(project_path_str: str) -> None:
    project_path = resolve_project(project_path_str)
    config = load_config(project_path)
    chapters = load_chapters(project_path)
    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    export_txt(str(project_path))
    export_epub(str(project_path))
    export_markdown(str(project_path))

    export_dir = ensure_export_dir(project_path)
    slug = project_slug(config, project_path)
    expected = [export_dir / f"{slug}.txt", export_dir / f"{slug}.epub", export_dir / f"{slug}.md"]
    print("[OK] All exports collected in:")
    print(f"   {export_dir}")
    for path in expected:
        status = "ready" if path.exists() else "missing"
        print(f"   - {path.name}: {status}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export TXT, EPUB, and Markdown for a NovelMaster project.")
    parser.add_argument("project_path")
    args = parser.parse_args()

    try:
        cmd_export_all(args.project_path)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
