#!/usr/bin/env python3
"""Build a style guide from local ingredient novels.

Usage:
    python3 scripts/ingredient_analyzer.py <project_path> [--ingredient-dir <dir> ...]

The output is a lightweight, non-extractive guide at
<project_path>/sources/ingredient_style_guide.md. It summarizes rhythm and craft
signals from same-genre reference material without copying plot, characters, or
prose passages.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from statistics import mean
from typing import Iterable
from xml.etree import ElementTree

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent

SUPPORTED_SUFFIXES = {".epub", ".txt", ".md", ".markdown"}
DEFAULT_MAX_CHARS_PER_FILE = 220_000


class _TextHTMLParser(HTMLParser):
    """Small HTML-to-text parser for EPUB XHTML spine files."""

    BLOCK_TAGS = {
        "br",
        "p",
        "div",
        "section",
        "article",
        "h1",
        "h2",
        "h3",
        "h4",
        "li",
    }

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data)

    def text(self) -> str:
        return normalize_text("".join(self.parts))


def normalize_text(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_markdown(text: str) -> str:
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"`{3}.*?`{3}", "", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*]\([^)]*\)", "", text)
    text = re.sub(r"\[[^\]]+]\([^)]*\)", "", text)
    text = re.sub(r"^[#>*\-\s]+", "", text, flags=re.M)
    return normalize_text(text)


def read_text_file(path: Path, max_chars: int) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() in {".md", ".markdown"}:
        text = strip_markdown(text)
    return normalize_text(text[:max_chars])


def read_epub(path: Path, max_chars: int) -> tuple[str, dict[str, str]]:
    metadata: dict[str, str] = {}
    text_parts: list[str] = []

    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        opf_path = _find_opf_path(archive, names)
        spine_items: list[str] = []
        if opf_path:
            try:
                opf_text = archive.read(opf_path).decode("utf-8", errors="ignore")
                metadata = _parse_opf_metadata(opf_text)
                spine_items = _parse_spine_items(opf_text, opf_path)
            except Exception:
                spine_items = []

        candidates = spine_items or [
            name
            for name in names
            if name.lower().endswith((".xhtml", ".html", ".htm"))
            and not name.lower().endswith(("nav.xhtml", "toc.xhtml"))
        ]

        for name in candidates:
            if name not in names:
                continue
            raw = archive.read(name).decode("utf-8", errors="ignore")
            parser = _TextHTMLParser()
            parser.feed(raw)
            part = parser.text()
            if part:
                text_parts.append(part)
            if sum(len(part) for part in text_parts) >= max_chars:
                break

    return normalize_text("\n\n".join(text_parts))[:max_chars], metadata


def _find_opf_path(archive: zipfile.ZipFile, names: list[str]) -> str | None:
    if "META-INF/container.xml" not in names:
        return None
    container = archive.read("META-INF/container.xml").decode("utf-8", errors="ignore")
    root = ElementTree.fromstring(container)
    for node in root.iter():
        if node.tag.endswith("rootfile"):
            value = node.attrib.get("full-path")
            if value:
                return value
    return None


def _parse_opf_metadata(opf_text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for key in ("title", "creator", "language", "description"):
        match = re.search(rf"<dc:{key}[^>]*>(.*?)</dc:{key}>", opf_text, re.S | re.I)
        if match:
            metadata[key] = normalize_text(re.sub(r"<[^>]+>", "", match.group(1)))
    return metadata


def _parse_spine_items(opf_text: str, opf_path: str) -> list[str]:
    manifest: dict[str, str] = {}
    for item in re.finditer(r"<item\b([^>]+)>", opf_text, re.I):
        attrs = _parse_attrs(item.group(1))
        item_id = attrs.get("id")
        href = attrs.get("href")
        media_type = attrs.get("media-type", "")
        if item_id and href and ("html" in media_type or href.lower().endswith((".xhtml", ".html", ".htm"))):
            manifest[item_id] = str((Path(opf_path).parent / href).as_posix()).lstrip("./")

    spine_ids = [
        attrs["idref"]
        for attrs in (_parse_attrs(match.group(1)) for match in re.finditer(r"<itemref\b([^>]+)>", opf_text, re.I))
        if "idref" in attrs
    ]
    return [manifest[item_id] for item_id in spine_ids if item_id in manifest]


def _parse_attrs(text: str) -> dict[str, str]:
    return {
        key: value
        for key, value in re.findall(r'([\w:-]+)\s*=\s*["\']([^"\']*)["\']', text)
    }


def discover_ingredient_files(paths: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            files.append(path)
        elif path.is_dir():
            files.extend(
                file
                for file in path.rglob("*")
                if file.is_file() and file.suffix.lower() in SUPPORTED_SUFFIXES
            )
    return sorted(files)


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) >= 8]


def split_sentences(text: str) -> list[str]:
    pieces = re.split(r"(?<=[。！？!?])", text)
    return [p.strip() for p in pieces if p.strip()]


def analyze_text(text: str) -> dict[str, object]:
    paragraphs = split_paragraphs(text)
    sentences = split_sentences(text)
    non_space_chars = [ch for ch in text if not ch.isspace()]
    char_count = len(non_space_chars)
    dialogue_chars = sum(len(match.group(0)) for match in re.finditer(r"[“「『](.*?)[”」』]", text, re.S))
    dialogue_paragraphs = [p for p in paragraphs if re.search(r"[“「『].+?[”」』]", p, re.S)]

    sensory_words = count_terms(text, "风雨雪霜寒热冷香腥甜苦疼痛麻痒汗血光影声响酒茶衣袖眉眼手指呼吸")
    action_words = count_terms(text, "走奔跑跃退拦挡劈刺斩拍抓握抬低转看笑叹咬摔砸推拉")
    emotion_words = count_terms(text, "喜怒哀惧惊怔慌酸涩委屈羞愧疼惜不甘")

    endings = [p[-18:] for p in paragraphs[-3:] if p]
    return {
        "char_count": char_count,
        "paragraph_count": len(paragraphs),
        "sentence_count": len(sentences),
        "avg_paragraph_len": round(mean([len(p) for p in paragraphs]) if paragraphs else 0, 1),
        "avg_sentence_len": round(mean([len(s) for s in sentences]) if sentences else 0, 1),
        "dialogue_ratio": round(dialogue_chars / char_count, 3) if char_count else 0,
        "dialogue_paragraph_ratio": round(len(dialogue_paragraphs) / len(paragraphs), 3) if paragraphs else 0,
        "sensory_density": round(sensory_words / max(char_count, 1) * 1000, 2),
        "action_density": round(action_words / max(char_count, 1) * 1000, 2),
        "emotion_density": round(emotion_words / max(char_count, 1) * 1000, 2),
        "ending_shapes": endings,
    }


def count_terms(text: str, terms: str) -> int:
    return sum(text.count(term) for term in terms)


def load_sources(files: list[Path], max_chars: int) -> list[dict[str, object]]:
    sources: list[dict[str, object]] = []
    for path in files:
        try:
            if path.suffix.lower() == ".epub":
                text, metadata = read_epub(path, max_chars)
            else:
                text = read_text_file(path, max_chars)
                metadata = {}
        except Exception as exc:
            sources.append({"path": path, "error": str(exc), "text": "", "metadata": {}})
            continue

        sources.append(
            {
                "path": path,
                "text": text,
                "metadata": metadata,
                "metrics": analyze_text(text) if text else {},
            }
        )
    return sources


def aggregate_metrics(sources: list[dict[str, object]]) -> dict[str, float]:
    metric_names = [
        "avg_paragraph_len",
        "avg_sentence_len",
        "dialogue_ratio",
        "dialogue_paragraph_ratio",
        "sensory_density",
        "action_density",
        "emotion_density",
    ]
    result: dict[str, float] = {}
    for name in metric_names:
        values = [
            float(source["metrics"][name])
            for source in sources
            if isinstance(source.get("metrics"), dict) and name in source["metrics"]
        ]
        result[name] = round(mean(values), 3) if values else 0
    return result


def build_style_recommendations(metrics: dict[str, float]) -> list[str]:
    recommendations = [
        "Keep paragraphs mobile-friendly: mix short reaction beats with occasional longer sensory paragraphs.",
        "Before each major decision, add one reader-facing emotional anchor: what the POV character wants, fears, misreads, or refuses to admit.",
        "Use action beats around dialogue so characters feel physically present instead of trading lines in empty space.",
        "Let pleasure points land through cause and reaction: setup the pressure, show the turn, then give one concrete aftershock.",
        "Dialogue must taste like people: ban telegram scraps (问/出/走/条件) and incomplete catalog splits (你主查。我主护。她主听。); give each major speaker at least one line with bite, heat, humor, or evasion.",
        "Prefer verifiable sensory modifiers over abstract stacked adjectives (avoid 香得克制 / 安静得像故意 / 笑意满眼里更满).",
        "One metaphor per emotional beat; ban unlike-like ladders (不像A，也不像B。像C) especially in dialogue; do not chain salt/shell/chess/price/goods abstractions across a whole tea-table scene.",
        "Use em dashes sparingly: interrupted speech only; never as decorative pause or ——不是/像/要 gloss.",
    ]

    if metrics.get("dialogue_ratio", 0) < 0.2:
        recommendations.append("Raise dialogue share during drafting; reference corpus dialogue is sparse, so add living speech to avoid stiffness.")
    else:
        recommendations.append("Preserve a strong dialogue pulse; use speech to reveal status, affection, rivalry, and subtext.")

    if metrics.get("sensory_density", 0) < 10:
        recommendations.append("Add more sensory handles in each scene: light, smell, temperature, texture, bodily strain.")
    else:
        recommendations.append("Borrow the sensory concreteness, but keep details selective so scenes do not become decorative.")

    if metrics.get("emotion_density", 0) < 4:
        recommendations.append("Do not rely on abstract emotion labels; turn feelings into gestures, pauses, and choices.")
    else:
        recommendations.append("Carry emotional language through behavior first, direct naming second.")

    return recommendations


def dialogue_flavor_checklist() -> list[str]:
    return [
        "Each important reply carries identity: diction, status, desire, or pressure — not a plot token.",
        "Terse characters stay short but edged; never collapse into ≤2-character command spam or single-verb catalogs.",
        "Lines must be complete spoken clauses; rewrite 你主查。我主护。她主听。 into natural speech.",
        "Playful/clever characters probe with detours, jokes, and bait; never dump rule sheets.",
        "Interleave speech with cup/sword/sleeve/eye beats so dialogue has body.",
        "At least one line per major scene should make a reader smile, sting, or lean forward.",
        "Ban dialogue unlike-like ladders (不像A，也不像B。像C) and twin 像A，又像B stacks.",
    ]


def adjective_discipline_checklist() -> list[str]:
    return [
        "Replace abstract intensity labels with source + sensation (where the smell comes from, what the hand does).",
        "If deleting a modifier does not change plot or relationship, delete it.",
        "Avoid twin abstract stacks in one sentence (满/更满, 真/净, 克制/故意 as atmosphere stickers).",
        "Keep genre heat through concrete weather, sweat, salt, frost, blood, tea steam — not caption adjectives.",
    ]

def write_markdown(project_path: Path, sources: list[dict[str, object]], output_path: Path, ingredient_dirs: list[Path]) -> None:
    metrics = aggregate_metrics(sources)
    recommendations = build_style_recommendations(metrics)
    successful = [source for source in sources if source.get("text")]
    failed = [source for source in sources if source.get("error")]

    lines = [
        "# Ingredient Style Guide",
        "",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> Project: {project_path.name}",
        "> Use as style and craft reference only. Do not copy plot points, character designs, or prose passages.",
        "",
        "## Input Scope",
        "",
    ]
    for directory in ingredient_dirs:
        lines.append(f"- `{safe_relpath(directory)}`")

    lines.extend(
        [
            "",
            "## Corpus Metrics",
            "",
            "| Signal | Value | Writer Use |",
            "|--------|-------|------------|",
            f"| Avg paragraph length | {metrics['avg_paragraph_len']} chars | Tune mobile reading rhythm |",
            f"| Avg sentence length | {metrics['avg_sentence_len']} chars | Balance breath and velocity |",
            f"| Dialogue character ratio | {metrics['dialogue_ratio']:.3f} | Keep scenes voiced and social |",
            f"| Dialogue paragraph ratio | {metrics['dialogue_paragraph_ratio']:.3f} | Check conversation density |",
            f"| Sensory density / 1k chars | {metrics['sensory_density']:.2f} | Add concrete scene texture |",
            f"| Action density / 1k chars | {metrics['action_density']:.2f} | Keep bodies moving in scene |",
            f"| Emotion density / 1k chars | {metrics['emotion_density']:.2f} | Humanize choices and reactions |",
            "",
            "## Style Moves To Borrow",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in recommendations)

    lines.extend(
        [
            "",
            "## Dialogue Flavor Checklist",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in dialogue_flavor_checklist())

    lines.extend(
        [
            "",
            "## Adjective Discipline Checklist",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in adjective_discipline_checklist())

    lines.extend(
        [
            "",
            "## Reader-View Polish Checklist",
            "",
            "- Curiosity: the opening paragraph gives the reader a concrete question or discomfort.",
            "- Empathy: the POV character has a small, human want in the scene, not only a plot task.",
            "- Heat: every argument, fight, or reward changes status, intimacy, safety, or self-image.",
            "- Texture: at least one non-visual detail grounds the location.",
            "- Freshness: replace formal summary with a gesture, a line of subtext, or an observed contradiction.",
            "- Mouthfeel: dialogue sounds spoken by distinct people, not a dry briefing.",
            "- Modifier sanity: no weird abstract adjective stacks.",
            "- Next-click: the ending leaves an unresolved promise, cost, discovery, or decision.",
            "",
            "## Per-Source Notes",
            "",
            "| Source | Title | Author | Chars Sampled | Paragraph | Sentence | Dialogue | Notes |",
            "|--------|-------|--------|---------------|-----------|----------|----------|-------|",
        ]
    )

    for source in successful:
        path = source["path"]
        metadata = source.get("metadata") if isinstance(source.get("metadata"), dict) else {}
        metric = source["metrics"]
        notes = source_notes(metric)
        lines.append(
            "| {source} | {title} | {author} | {chars} | {para} | {sent} | {dialogue} | {notes} |".format(
                source=escape_table(safe_relpath(path)),
                title=escape_table(metadata.get("title", "")),
                author=escape_table(metadata.get("creator", "")),
                chars=metric.get("char_count", 0),
                para=metric.get("avg_paragraph_len", 0),
                sent=metric.get("avg_sentence_len", 0),
                dialogue=metric.get("dialogue_ratio", 0),
                notes=escape_table(notes),
            )
        )

    if failed:
        lines.extend(["", "## Files Skipped", ""])
        for source in failed:
            lines.append(f"- `{safe_relpath(source['path'])}`: {source['error']}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def source_notes(metric: dict[str, object]) -> str:
    notes: list[str] = []
    if metric.get("dialogue_ratio", 0) >= 0.25:
        notes.append("dialogue-forward")
    if metric.get("avg_paragraph_len", 0) <= 90:
        notes.append("short mobile rhythm")
    if metric.get("action_density", 0) >= 20:
        notes.append("action-rich")
    if metric.get("sensory_density", 0) >= 12:
        notes.append("sensory concrete")
    if metric.get("emotion_density", 0) >= 5:
        notes.append("emotionally explicit")
    return ", ".join(notes) or "baseline style signal"


def escape_table(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def safe_relpath(path: object) -> str:
    p = Path(path)
    try:
        return str(p.resolve().relative_to(REPO_ROOT)).replace("\\", "/")
    except Exception:
        return str(p).replace("\\", "/")


def default_ingredient_dirs() -> list[Path]:
    return [path for path in (REPO_ROOT / "ingredient", REPO_ROOT / "ingredients") if path.exists()]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path", help="Novel project path")
    parser.add_argument(
        "--ingredient-dir",
        action="append",
        dest="ingredient_dirs",
        help="Ingredient directory or file. Repeatable. Defaults to ingredient/ and ingredients/.",
    )
    parser.add_argument(
        "--max-chars-per-file",
        type=int,
        default=DEFAULT_MAX_CHARS_PER_FILE,
        help=f"Maximum characters sampled per source file (default: {DEFAULT_MAX_CHARS_PER_FILE}).",
    )
    parser.add_argument(
        "--output",
        help="Output markdown path. Defaults to <project_path>/sources/ingredient_style_guide.md.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])
    project_path = Path(args.project_path).resolve()
    if not project_path.exists():
        print(f"[ERROR] Project not found: {project_path}")
        sys.exit(1)

    ingredient_dirs = [Path(p).resolve() for p in args.ingredient_dirs] if args.ingredient_dirs else default_ingredient_dirs()
    files = discover_ingredient_files(ingredient_dirs)
    if not files:
        print("[WARN] No supported ingredient files found (.epub, .txt, .md)")
        output = Path(args.output).resolve() if args.output else project_path / "sources" / "ingredient_style_guide.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            "# Ingredient Style Guide\n\n"
            "> No local ingredient files found. Add same-genre EPUB/TXT/MD files under ingredient/ or ingredients/.\n",
            encoding="utf-8",
        )
        print(f"[OK] Empty style guide written to {output}")
        return

    sources = load_sources(files, args.max_chars_per_file)
    output_path = Path(args.output).resolve() if args.output else project_path / "sources" / "ingredient_style_guide.md"
    write_markdown(project_path, sources, output_path, ingredient_dirs)

    successful = sum(1 for source in sources if source.get("text"))
    print(f"[OK] Ingredient style guide written to {output_path}")
    print(f"   Sources analyzed: {successful}/{len(sources)}")
    print(f"   Output: {safe_relpath(output_path)}")


if __name__ == "__main__":
    main()
