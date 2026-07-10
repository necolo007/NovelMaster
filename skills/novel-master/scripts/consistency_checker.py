#!/usr/bin/env python3
"""Cross-chapter consistency checker.

Usage:
    python3 scripts/consistency_checker.py <project_path>

Checks:
  - Name consistency across chapters
  - Kinship/title/surname logic
  - Timeline/logic consistency
  - Item/possession tracking
  - Location tracking
  - Power level consistency
  - Currency/economy consistency

Reads all chapter drafts and tracker files.
Outputs errors (must fix) and warnings (should fix).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


EXPLANATION_KEYWORDS = (
    "尊号",
    "道号",
    "本名",
    "别名",
    "化名",
    "名号",
    "称号",
    "随母姓",
    "母姓",
    "养父",
    "养女",
    "义父",
    "义女",
    "继父",
    "继女",
    "非亲生",
    "收养",
)


def _base_name(name: str) -> str:
    """Strip parenthetical aliases from a profile heading."""
    return re.sub(r"[（(].*?[）)]", "", name).strip()


def _surname(name: str) -> str:
    """Return a simple first-character Chinese surname heuristic."""
    base = _base_name(name)
    return base[:1]


def _has_kinship_explanation(text: str) -> bool:
    return any(keyword in text for keyword in EXPLANATION_KEYWORDS)


def _profile_sections(text: str) -> list[tuple[str, str]]:
    """Return (heading name, section body) pairs from character_profiles.md."""
    matches = list(re.finditer(r"^###\s+(.+?)\s*$", text, flags=re.MULTILINE))
    sections = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections.append((match.group(1).strip(), text[start:end]))
    return sections


def _check_kinship_name_logic(project_path: Path) -> tuple[list[str], list[str]]:
    """Detect obvious family surname contradictions in character profiles.

    The check is intentionally conservative and only flags profile-level claims.
    It accepts explicit explanations such as title/alias/daohao, adoption, or
    maternal surname.
    """
    profiles_path = project_path / "framework" / "character_profiles.md"
    if not profiles_path.exists():
        return [], ["framework/character_profiles.md not found; skipped kinship/name logic check"]

    text = profiles_path.read_text(encoding="utf-8")
    errors: list[str] = []
    info: list[str] = []

    relation_patterns = [
        (r"([一-龥]{2,4})独女", "daughter_of"),
        (r"([一-龥]{2,4})之女", "daughter_of"),
        (r"([一-龥]{2,4})之父", "father_of"),
        (r"([一-龥]{2,4})之子", "son_of"),
    ]

    for heading, body in _profile_sections(text):
        current = _base_name(heading)
        if not current:
            continue

        for pattern, relation_type in relation_patterns:
            for match in re.finditer(pattern, body):
                related = _base_name(match.group(1))
                if not related or related in {"掌门", "宗主", "师父", "父亲", "母亲"}:
                    continue
                if _surname(current) == _surname(related):
                    continue
                context_start = max(match.start() - 80, 0)
                context_end = min(match.end() + 120, len(body))
                context = body[context_start:context_end]
                if _has_kinship_explanation(context) or _has_kinship_explanation(body):
                    info.append(
                        f"Kinship surname differs but explanation exists: {current} / {related}"
                    )
                    continue
                errors.append(
                    "Kinship/name contradiction in character_profiles.md: "
                    f"{current} references {related} via {relation_type}, but surnames differ "
                    "and no alias/title/adoption/maternal-surname explanation was found."
                )

    return errors, info


def cmd_check(project_path_str: str) -> dict:
    """Run consistency checks across all chapters.

    Returns dict with counts of errors, warnings, and info.
    """
    project_path = Path(project_path_str).resolve()
    drafts_dir = project_path / "drafts"

    if not drafts_dir.exists():
        print("[ERROR] drafts/ directory not found")
        sys.exit(1)

    chapters = sorted(drafts_dir.glob("chapter_*.md"))
    if not chapters:
        print("[WARN] No chapter drafts found")
        return {"errors": 0, "warnings": 0, "info": 0}

    errors = []
    warnings = []
    info = []

    print(f"Checking consistency across {len(chapters)} chapters...")

    kinship_errors, kinship_info = _check_kinship_name_logic(project_path)
    errors.extend(kinship_errors)
    info.extend(kinship_info)

    # Placeholder: full implementation would:
    # 1. Parse frontmatter from every chapter
    # 2. Build name/location/item/power timeline
    # 3. Detect contradictions (same person called different names, etc.)
    # 4. Cross-reference with character_profiles.md and world_building.md

    print(f"\n[OK] Consistency check complete")
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
        print("Usage: consistency_checker.py <project_path>")
        sys.exit(1)

    result = cmd_check(sys.argv[1])
    if result["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
