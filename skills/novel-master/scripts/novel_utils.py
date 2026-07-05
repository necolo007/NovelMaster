#!/usr/bin/env python3
"""Shared helpers for NovelMaster project inspection and export."""

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CHAPTER_RE = re.compile(r"chapter_(\d+)\.md$", re.IGNORECASE)


@dataclass(frozen=True)
class Chapter:
    number: int
    path: Path
    title: str
    body_markdown: str
    plain_text: str
    metadata: dict[str, Any]
    word_count: int


def resolve_project(project_path_str: str) -> Path:
    project_path = Path(project_path_str).expanduser().resolve()
    if not (project_path / "novel_config.json").exists():
        raise FileNotFoundError(f"novel_config.json not found: {project_path}")
    return project_path


def load_config(project_path: Path) -> dict[str, Any]:
    config_path = project_path / "novel_config.json"
    return json.loads(config_path.read_text(encoding="utf-8-sig"))


def project_slug(config: dict[str, Any], project_path: Path) -> str:
    return str(config.get("project_name") or project_path.name or "novel")


def project_title(config: dict[str, Any], project_path: Path) -> str:
    return str(config.get("title") or project_path.name)


def iter_chapter_paths(project_path: Path) -> list[Path]:
    drafts_dir = project_path / "drafts"
    paths = [path for path in drafts_dir.glob("chapter_*.md") if CHAPTER_RE.match(path.name)]
    return sorted(paths, key=lambda path: int(CHAPTER_RE.match(path.name).group(1)))


def parse_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    if not raw.startswith("---"):
        return {}, raw.strip()

    lines = raw.splitlines()
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        return {}, raw.strip()

    metadata = parse_simple_yaml(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :]).strip()
    return metadata, body


def parse_simple_yaml(lines: list[str]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        metadata[key.strip()] = parse_yaml_value(value.strip())
    return metadata


def parse_yaml_value(value: str) -> Any:
    if value == "":
        return ""
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            inner = value[1:-1].strip()
            if not inner:
                return []
            return [item.strip().strip('"').strip("'") for item in inner.split(",")]
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def split_heading(body: str) -> tuple[str | None, str]:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            rest = "\n".join(lines[:index] + lines[index + 1 :]).strip()
            return title, rest
    return None, body.strip()


def load_chapter(path: Path) -> Chapter:
    raw = path.read_text(encoding="utf-8-sig")
    metadata, body = parse_frontmatter(raw)
    heading, body_without_heading = split_heading(body)
    match = CHAPTER_RE.match(path.name)
    number = int(match.group(1)) if match else 0
    title = str(metadata.get("title") or heading or f"Chapter {number}")
    plain = markdown_to_plain_text(body_without_heading)
    word_count = int(metadata.get("words") or count_cjk_aware_words(plain))
    return Chapter(
        number=number,
        path=path,
        title=title,
        body_markdown=body_without_heading,
        plain_text=plain,
        metadata=metadata,
        word_count=word_count,
    )


def load_chapters(project_path: Path) -> list[Chapter]:
    return [load_chapter(path) for path in iter_chapter_paths(project_path)]


def markdown_to_plain_text(markdown: str) -> str:
    text = markdown.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`>#-]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def markdown_to_html(markdown: str) -> str:
    blocks = re.split(r"\n\s*\n", markdown.strip())
    parts: list[str] = []
    for block in blocks:
        stripped = block.strip()
        if not stripped:
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = min(len(heading.group(1)) + 1, 6)
            parts.append(f"<h{level}>{html.escape(heading.group(2))}</h{level}>")
            continue
        paragraph = "<br/>".join(html.escape(line.strip()) for line in stripped.splitlines())
        parts.append(f"<p>{paragraph}</p>")
    return "\n".join(parts)


def count_cjk_aware_words(text: str) -> int:
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    words = re.findall(r"[A-Za-z0-9_]+", text)
    return len(cjk) + len(words)


def chapter_anchor(chapter: Chapter) -> str:
    return f"chapter-{chapter.number:03d}"


def ensure_export_dir(project_path: Path) -> Path:
    export_dir = project_path / "export"
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir
