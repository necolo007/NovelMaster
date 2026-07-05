#!/usr/bin/env python3
"""Build the JSON manifest consumed by the built-in NovelMaster web app."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from novel_utils import load_chapters, load_config, project_slug, project_title, resolve_project


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent


def find_projects() -> list[Path]:
    projects_dir = REPO_ROOT / "projects"
    if not projects_dir.exists():
        return []
    return sorted(path for path in projects_dir.iterdir() if (path / "novel_config.json").exists())


def relative_to_root(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def project_to_manifest(project_path: Path, embed_content: bool = False) -> dict:
    config = load_config(project_path)
    chapters = load_chapters(project_path)
    export_dir = project_path / "export"
    memory_dir = project_path / "memory"
    export_files = []
    if export_dir.exists():
        for file_path in sorted(export_dir.iterdir()):
            if file_path.is_file() and not file_path.name.startswith("."):
                export_files.append(
                    {
                        "name": file_path.name,
                        "path": relative_to_root(file_path),
                        "size": file_path.stat().st_size,
                    }
                )

    memory_archives = []
    if memory_dir.exists():
        for archive_dir in sorted(memory_dir.glob("chapters_*_*")):
            if not archive_dir.is_dir():
                continue
            continuity = archive_dir / "continuity_memory.md"
            summaries = archive_dir / "chapter_summaries.md"
            manifest = archive_dir / "chapters_manifest.json"
            memory_archives.append(
                {
                    "name": archive_dir.name,
                    "path": relative_to_root(archive_dir),
                    "continuityPath": relative_to_root(continuity) if continuity.exists() else "",
                    "summariesPath": relative_to_root(summaries) if summaries.exists() else "",
                    "manifestPath": relative_to_root(manifest) if manifest.exists() else "",
                }
            )

    chapter_items = []
    for chapter in chapters:
        item = {
            "number": chapter.number,
            "title": chapter.title,
            "path": relative_to_root(chapter.path),
            "wordCount": chapter.word_count,
            "metadata": chapter.metadata,
            "plainPreview": chapter.plain_text[:240],
        }
        if embed_content:
            item["contentMarkdown"] = chapter.body_markdown
        chapter_items.append(item)

    return {
        "id": project_slug(config, project_path),
        "title": project_title(config, project_path),
        "author": config.get("author") or "",
        "genre": config.get("genre") or "",
        "genreLabel": config.get("genre_label") or config.get("genre") or "",
        "language": config.get("language") or "zh-CN",
        "pipelineState": config.get("pipeline_state") or "",
        "targetWords": config.get("target_words") or 0,
        "chapterAvgWords": config.get("chapter_avg_words") or 0,
        "createdAt": config.get("created_at") or "",
        "path": relative_to_root(project_path),
        "stats": {
            "chapters": len(chapters),
            "words": sum(chapter.word_count for chapter in chapters),
            "exports": len(export_files),
            "memories": len(memory_archives),
        },
        "exports": export_files,
        "memoryArchives": memory_archives,
        "chapters": chapter_items,
    }


def build_manifest(project_paths: list[str], output_path_str: str, embed_content: bool = False) -> Path:
    if project_paths:
        projects = [resolve_project(path) for path in project_paths]
    else:
        projects = find_projects()

    output_path = Path(output_path_str)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "projects": [project_to_manifest(path, embed_content=embed_content) for path in projects],
    }
    manifest["stats"] = {
        "projects": len(manifest["projects"]),
        "chapters": sum(project["stats"]["chapters"] for project in manifest["projects"]),
        "words": sum(project["stats"]["words"] for project in manifest["projects"]),
        "exports": sum(project["stats"]["exports"] for project in manifest["projects"]),
        "memories": sum(project["stats"].get("memories", 0) for project in manifest["projects"]),
    }

    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build NovelMaster web app manifest.")
    parser.add_argument("project_paths", nargs="*", help="Project paths. Omit to include every project in projects/.")
    parser.add_argument("--output", default="web/projects.json")
    parser.add_argument("--embed-content", action="store_true", help="Embed chapter Markdown in JSON instead of fetching files lazily.")
    args = parser.parse_args()

    try:
        output_path = build_manifest(args.project_paths, args.output, embed_content=args.embed_content)
        print(f"[OK] Web manifest built: {output_path}")
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
