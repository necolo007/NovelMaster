#!/usr/bin/env python3
"""Novel Master project management helpers.

Usage:
    python3 scripts/project_manager.py init <novel_name> [--genre xuanhuan] [--dir projects]
    python3 scripts/project_manager.py import-sources <project_path> <source1> [<source2> ...] [--move | --copy]
    python3 scripts/project_manager.py validate <project_path>
    python3 scripts/project_manager.py info <project_path>
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent

GENRES = [
    "xuanhuan",      # 玄幻
    "xiuzhen",       # 修真
    "dushi",         # 都市
    "kehuan",        # 科幻
    "qihuan",        # 奇幻
    "wuxia",         # 武侠
    "xianxia",       # 仙侠
    "lishi",         # 历史
    "youxi",         # 游戏
    "moshi",         # 末世
    "xuanyi",        # 悬疑
    "tongren",       # 同人
    "custom",        # 自定义
]

GENRE_LABELS = {
    "xuanhuan": "玄幻",
    "xiuzhen": "修真",
    "dushi": "都市",
    "kehuan": "科幻",
    "qihuan": "奇幻",
    "wuxia": "武侠",
    "xianxia": "仙侠",
    "lishi": "历史",
    "youxi": "游戏",
    "moshi": "末世",
    "xuanyi": "悬疑",
    "tongren": "同人",
    "custom": "自定义",
}

SOURCE_DIRNAME = "sources"
FRAMEWORK_DIRNAME = "framework"
DRAFTS_DIRNAME = "drafts"
TRACKING_DIRNAME = "tracking"
NOTES_DIRNAME = "notes"
EXPORT_DIRNAME = "export"

PROJECT_DIRS = [
    SOURCE_DIRNAME,
    FRAMEWORK_DIRNAME,
    DRAFTS_DIRNAME,
    TRACKING_DIRNAME,
    NOTES_DIRNAME,
    EXPORT_DIRNAME,
]

TEXT_SOURCE_SUFFIXES = {".md", ".markdown", ".txt"}
EPUB_SUFFIXES = {".epub"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}

PIPELINE_STATES = ["framing", "drafting", "editing", "exporting", "done"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sanitize_name(value: str) -> str:
    """Sanitize a user-facing name into a filesystem-safe slug."""
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value.strip())
    safe = safe.strip("._")
    while "__" in safe:
        safe = safe.replace("__", "_")
    return safe[:120] or "novel"


def derive_project_dir(workspace: Path, novel_name: str) -> Path:
    """Derive the full project directory path."""
    safe_name = sanitize_name(novel_name)
    return workspace / safe_name


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_init(novel_name: str, genre: str = "custom", workspace_dir: Optional[str] = None) -> Path:
    """Initialize a new novel project directory structure.

    Returns the project path.
    """
    if genre not in GENRES:
        print(f"[ERROR] Unknown genre: {genre}")
        print(f"   Valid genres: {', '.join(GENRES)}")
        sys.exit(1)

    workspace = Path(workspace_dir) if workspace_dir else REPO_ROOT / "projects"
    workspace.mkdir(parents=True, exist_ok=True)

    project_path = derive_project_dir(workspace, novel_name)
    if project_path.exists():
        print(f"[ERROR] Project already exists: {project_path}")
        sys.exit(1)

    # Create directory structure
    for dirname in PROJECT_DIRS:
        (project_path / dirname).mkdir(parents=True, exist_ok=True)

    # Generate novel_config.json
    config = {
        "project_name": sanitize_name(novel_name),
        "title": novel_name,
        "author": "",
        "genre": genre,
        "genre_label": GENRE_LABELS.get(genre, genre),
        "target_words": 500000,
        "chapter_avg_words": 3000,
        "language": "zh-CN",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "pipeline_state": "framing",
    }

    config_path = project_path / "novel_config.json"
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Create .gitkeep in empty directories
    for dirname in PROJECT_DIRS:
        keep = project_path / dirname / ".gitkeep"
        if not any(project_path.joinpath(dirname).iterdir()):
            keep.write_text("", encoding="utf-8")

    _print_init_success(project_path, config)
    return project_path


def _print_init_success(project_path: Path, config: dict) -> None:
    """Print a human-friendly init summary."""
    print(f"[OK] Novel project initialized: {project_path}")
    print(f"   Title:    {config['title']}")
    print(f"   Genre:    {config['genre_label']} ({config['genre']})")
    print(f"   Language: {config['language']}")
    print()
    print("   Created directories:")
    for d in PROJECT_DIRS:
        print(f"     {d}/")
    print()
    print("   Next step: Architect Six Confirmations (SKILL.md Step 4)")


def cmd_import_sources(project_path_str: str, sources: list[str], move: bool = False) -> None:
    """Import source files into a project's sources/ directory."""
    project_path = Path(project_path_str).resolve()
    sources_dir = project_path / SOURCE_DIRNAME

    if not project_path.exists():
        print(f"[ERROR] Project not found: {project_path}")
        sys.exit(1)
    if not sources_dir.exists():
        print(f"❌ sources/ directory missing in project: {sources_dir}")
        sys.exit(1)

    imported = 0
    for src in sources:
        src_path = Path(src).resolve()
        if not src_path.exists():
            print(f"[WARN]  Source not found, skipping: {src_path}")
            continue

        dest = sources_dir / src_path.name
        if dest.exists():
            base = src_path.stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = sources_dir / f"{base}_{timestamp}{src_path.suffix}"

        if move:
            shutil.move(str(src_path), str(dest))
        else:
            if src_path.is_file():
                shutil.copy2(str(src_path), str(dest))
            elif src_path.is_dir():
                shutil.copytree(str(src_path), str(dest))

        imported += 1
        print(f"   {'Moved' if move else 'Copied'}: {src_path.name} → {dest.relative_to(REPO_ROOT)}")

    # Remove .gitkeep if it exists and there are real files
    keep_file = sources_dir / ".gitkeep"
    if keep_file.exists() and imported > 0:
        keep_file.unlink()

    print(f"\n[OK] Imported {imported} source(s) into {sources_dir.relative_to(REPO_ROOT)}")


def cmd_validate(project_path_str: str) -> dict:
    """Validate a project's structure and return project info.

    Returns project info dict or exits with error.
    """
    project_path = Path(project_path_str).resolve()

    errors = []
    warnings = []

    if not project_path.exists():
        print(f"[ERROR] Project path does not exist: {project_path}")
        sys.exit(1)

    # Check novel_config.json
    config_path = project_path / "novel_config.json"
    if not config_path.exists():
        errors.append("Missing novel_config.json")
    else:
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            required_keys = ["project_name", "title", "genre", "pipeline_state"]
            for key in required_keys:
                if key not in config:
                    errors.append(f"novel_config.json missing key: {key}")
            if config.get("pipeline_state") not in PIPELINE_STATES:
                warnings.append(f"Unknown pipeline_state: {config['pipeline_state']}")
        except json.JSONDecodeError as e:
            errors.append(f"novel_config.json is invalid JSON: {e}")
            config = {}

    # Check required directories
    for dirname in PROJECT_DIRS:
        dir_path = project_path / dirname
        if not dir_path.exists():
            errors.append(f"Missing directory: {dirname}/")

    # State-specific checks
    state = config.get("pipeline_state", "framing")
    if state in ("drafting", "editing", "exporting", "done"):
        framework_dir = project_path / FRAMEWORK_DIRNAME
        if framework_dir.exists():
            framework_files = list(framework_dir.glob("*.md"))
            expected = {"world_building.md", "character_profiles.md", "plot_outline.md",
                        "chapter_breakdown.md", "spec_lock.md"}
            missing = expected - {f.name for f in framework_files}
            if missing:
                warnings.append(f"Framework files missing: {', '.join(sorted(missing))}")

    if state in ("drafting", "editing", "exporting", "done"):
        drafts = list((project_path / DRAFTS_DIRNAME).glob("chapter_*.md"))
        if not drafts:
            warnings.append(f"No chapter drafts found but pipeline_state is '{state}'")

    if state in ("editing", "exporting", "done"):
        tracking_dir = project_path / TRACKING_DIRNAME
        tracking_files = list(tracking_dir.glob("*"))
        expected_tracking = {"context_summary.md", "plot_tracker.json", "character_state.json"}
        missing = expected_tracking - {f.name for f in tracking_files}
        if missing:
            warnings.append(f"Tracking files missing: {', '.join(sorted(missing))}")

    # Report
    if errors:
        print(f"[ERROR] Validation failed for {project_path.relative_to(REPO_ROOT)}")
        for e in errors:
            print(f"   [ERROR] {e}")
        for w in warnings:
            print(f"   [WARN] {w}")
        sys.exit(1)

    if warnings:
        print(f"[WARN]  Validation passed with warnings for {project_path.relative_to(REPO_ROOT)}")
        for w in warnings:
            print(f"   [WARN] {w}")
    else:
        print(f"[OK] Project validated: {project_path.relative_to(REPO_ROOT)}")
        config = config if 'config' in dir() else {}
        print(f"   Title:  {config.get('title', 'N/A')}")
        print(f"   Genre:  {config.get('genre', 'N/A')}")
        print(f"   State:  {config.get('pipeline_state', 'N/A')}")

    return config


def cmd_info(project_path_str: str) -> None:
    """Print project information summary."""
    project_path = Path(project_path_str).resolve()

    if not project_path.exists():
        print(f"[ERROR] Project not found: {project_path}")
        sys.exit(1)

    config_path = project_path / "novel_config.json"
    config = {}
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))

    print(f"[Novel] Project: {project_path.relative_to(REPO_ROOT)}")
    print(f"   Title:        {config.get('title', 'N/A')}")
    print(f"   Author:       {config.get('author', '(not set)')}")
    print(f"   Genre:        {config.get('genre_label', 'N/A')} ({config.get('genre', 'N/A')})")
    print(f"   Target words: {config.get('target_words', 'N/A'):,}")
    print(f"   Chapter avg:  {config.get('chapter_avg_words', 'N/A')} words")
    print(f"   Language:     {config.get('language', 'N/A')}")
    print(f"   State:        {config.get('pipeline_state', 'N/A')}")
    print(f"   Created:      {config.get('created_at', 'N/A')}")

    # File counts
    for dirname in PROJECT_DIRS:
        dir_path = project_path / dirname
        if dir_path.exists():
            files = [f for f in dir_path.iterdir() if f.is_file() and f.name != ".gitkeep"]
            if files:
                print(f"   {dirname}/:     {len(files)} file(s)")
                if dirname == DRAFTS_DIRNAME:
                    # Count total words in drafts
                    total_words = 0
                    for f in files:
                        text = f.read_text(encoding="utf-8")
                        # Count after frontmatter
                        parts = text.split("---")
                        if len(parts) >= 3:
                            prose = "---".join(parts[2:])
                            total_words += len(prose)
                    print(f"              -> ~{total_words:,} characters of prose")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        _print_usage()
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) < 3:
            print("[ERROR] Usage: project_manager.py init <novel_name> [--genre <genre>] [--dir <workspace>]")
            sys.exit(1)

        novel_name = sys.argv[2]
        genre = "custom"
        workspace_dir = None

        # Parse optional flags
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--genre" and i + 1 < len(args):
                genre = args[i + 1]
                i += 2
            elif args[i] == "--dir" and i + 1 < len(args):
                workspace_dir = args[i + 1]
                i += 2
            else:
                i += 1

        cmd_init(novel_name, genre, workspace_dir)

    elif command == "import-sources":
        if len(sys.argv) < 4:
            print("[ERROR] Usage: project_manager.py import-sources <project_path> <source...> [--move | --copy]")
            sys.exit(1)

        project_path = sys.argv[2]
        move = "--move" in sys.argv
        sources = [a for a in sys.argv[3:] if a not in ("--move", "--copy")]
        cmd_import_sources(project_path, sources, move=move)

    elif command == "validate":
        if len(sys.argv) < 3:
            print("[ERROR] Usage: project_manager.py validate <project_path>")
            sys.exit(1)
        cmd_validate(sys.argv[2])

    elif command == "info":
        if len(sys.argv) < 3:
            print("[ERROR] Usage: project_manager.py info <project_path>")
            sys.exit(1)
        cmd_info(sys.argv[2])

    else:
        print(f"[ERROR] Unknown command: {command}")
        _print_usage()
        sys.exit(1)


def _print_usage() -> None:
    print(__doc__)
    print()
    print("Commands:")
    print("  init <novel_name> [--genre <g>] [--dir <d>]   Create a new novel project")
    print("  import-sources <path> <files...> [--move]      Import source files into project")
    print("  validate <path>                                 Validate project structure")
    print("  info <path>                                     Print project info")
    print()
    print(f"Genres: {', '.join(GENRES)}")


if __name__ == "__main__":
    main()
