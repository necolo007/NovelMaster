#!/usr/bin/env python3
"""Writing style, reader-pull, and POV-adjacent consistency checker.

Usage:
    python3 scripts/style_checker.py <project_path>

Checks:
  - Dialogue ratio against spec_lock target when available
  - Long paragraphs that hurt mobile reading rhythm
  - Stiff summary voice patterns
  - AI 纠偏句式「不是A，是B / 不是A。是B / 不像A，是B」（同句与跨段）
  - Reader hook at opening and next-click hook at ending
  - Ingredient style guide presence and basic sensory/action craft signal
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TOOLS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def prose_body(text: str) -> str:
    _, body = split_frontmatter(text)
    lines = body.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def count_text_chars(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def dialogue_ratio(text: str) -> float:
    total = count_text_chars(text)
    if not total:
        return 0.0
    quoted = sum(len(m.group(0)) for m in re.finditer(r"[“「『](.*?)[”」』]", text, re.S))
    quoted += sum(len(m.group(0)) for m in re.finditer(r'"[^"\n]{2,}"', text))
    return quoted / total


def target_dialogue_ratio(spec_text: str) -> float | None:
    match = re.search(r"dialogue_ratio_target:\s*([0-9.]+)", spec_text)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def has_reader_hook(text: str) -> bool:
    opening = text[:500]
    hook_marks = ["？", "?", "！", "!", "却", "偏偏", "忽然", "没想到", "不对", "为何", "怎么"]
    return any(mark in opening for mark in hook_marks)


def has_next_click_ending(text: str) -> bool:
    ending = text[-350:]
    hook_marks = ["？", "?", "却", "忽然", "门", "信", "人影", "声音", "不对", "下一刻", "终于", "秘密"]
    return any(mark in ending for mark in hook_marks)


def stiff_summary_hits(text: str) -> list[str]:
    patterns = [
        "一番交谈",
        "众人皆",
        "所有人都",
        "不由得",
        "心中暗道",
        "很快便",
        "随即",
        "只见",
        "显得十分",
        "气氛十分",
    ]
    return [pattern for pattern in patterns if text.count(pattern) >= 3]


# AI 「不是A，是B / 不是A。是B」纠偏句式（同句对比 + 跨句/跨段拆分）
_NOT_BUT_INLINE = re.compile(
    r"不(?:是|像)(?![说吗嘛么啊呀])"
    r"[^。！？\n「」\"“”『』]{0,28}"
    r"(?:[，,、]|——|–|-)\s*"
    r"(?:而)?是"
)
_NOT_BUT_CROSS = re.compile(
    r"不(?:是|像)(?![说吗嘛么啊呀])"
    r"[^。！？\n]{1,36}[。！？]\s*"
    r"(?:\n\s*){0,3}"
    r"(?:是|而是)(?![否定非])"
    r"[^。！？\n]{0,48}[。！？]?"
)
_NOT_BUT_TRIPLE = re.compile(
    r"不是[^。！？\n]{1,20}，不是[^。！？\n]{1,20}，(?:而)?是"
)
_AI_CADENCE_OTHER = [
    re.compile(
        r"不(?:是|像)[^。！？\n]{1,30}[。！？]\s*(?:\n\s*){0,2}"
        r"(?:可|却|但)[^。！？\n]{1,45}[。！？]"
    ),
    re.compile(r"(?:像[^。！？\n]{1,30}[。！？]\s*){3,}"),
]


def find_not_but_hits(text: str) -> list[str]:
    """Locate decorative 不是…是… / 不像…是… ladders; return unique snippets."""
    hits: list[str] = []
    seen: set[str] = set()
    for regex in (_NOT_BUT_INLINE, _NOT_BUT_CROSS, _NOT_BUT_TRIPLE):
        for match in regex.finditer(text):
            snippet = re.sub(r"\s+", "", match.group(0))
            if len(snippet) < 4 or snippet in seen:
                continue
            # 排除「是不是」「还不是X」后接无关「他/她是」类假阳性已由 CROSS 要求下句以「是/而是」起头处理
            seen.add(snippet)
            hits.append(snippet[:60])
    return hits


def naturalness_findings(text: str) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for prose naturalness / AI cadence."""
    errors: list[str] = []
    warnings: list[str] = []
    ps = paragraphs(text)
    if not ps:
        return errors, warnings

    fragment_paragraphs = [
        p
        for p in ps
        if count_text_chars(p) <= 8 and not re.search(r"[「」“”『』]", p)
    ]
    if len(fragment_paragraphs) >= 8 and len(fragment_paragraphs) / len(ps) > 0.08:
        warnings.append(
            f"fragment-heavy narration ({len(fragment_paragraphs)} very short non-dialogue paragraphs)"
        )

    not_but_hits = find_not_but_hits(text)
    not_but_count = len(not_but_hits)
    samples = "；".join(not_but_hits[:3])
    if not_but_count >= 4:
        errors.append(
            f"AI 纠偏句式过密：本章「不是/不像…是…」命中 {not_but_count} 处（上限 3）；例：{samples}"
        )
    elif not_but_count >= 2:
        warnings.append(
            f"AI 纠偏句式偏多：本章「不是/不像…是…」命中 {not_but_count} 处（建议 ≤1）；例：{samples}"
        )

    other_cadence = sum(len(rx.findall(text)) for rx in _AI_CADENCE_OTHER)
    if other_cadence >= 3:
        warnings.append(f"repeated AI-literary cadence ({other_cadence} pattern hits)")

    non_dialogue = re.sub(r"[「“『].*?[」”』]", "", text, flags=re.S)
    metaphor_hits = len(re.findall(r"(?:像|仿佛|好似|犹如)", non_dialogue))
    per_1k = metaphor_hits / max(count_text_chars(non_dialogue), 1) * 1000
    if metaphor_hits >= 12 and per_1k > 4.5:
        warnings.append(f"high metaphor density ({metaphor_hits} comparison markers; {per_1k:.1f}/1k chars)")

    recap_patterns = [
        "这句话",
        "那句话",
        "这件事",
        "这种感觉",
        "那种感觉",
        "这不是",
        "那不是",
    ]
    recap_hits = sum(non_dialogue.count(pattern) for pattern in recap_patterns)
    if recap_hits >= 10:
        warnings.append(f"possible decorative emotional recap ({recap_hits} abstract recap markers)")

    return errors, warnings


def naturalness_warnings(text: str) -> list[str]:
    """Backward-compatible helper: warnings only."""
    _errors, warnings = naturalness_findings(text)
    return warnings


def dialogue_quality_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    qs = [
        m.group(1).strip()
        for m in re.finditer(r"[「“『]([^」”』\n]{1,80})[」”』]", text)
    ]
    if not qs:
        return warnings

    empty_replies = {
        "嗯",
        "好",
        "是",
        "不是",
        "没有",
        "知道",
        "明白",
        "来",
        "不懂",
        "不用",
        "没事",
        "问",
        "出",
        "走",
        "坐",
        "停",
        "看",
        "听",
        "条件",
        "越界",
        "收到",
        "成交",
        "先问",
    }
    short_empty = [q for q in qs if q in empty_replies or count_text_chars(q) <= 2]
    if len(short_empty) >= 6 and len(short_empty) / len(qs) > 0.22:
        warnings.append(
            f"too many empty/one-word dialogue replies ({len(short_empty)}/{len(qs)})"
        )
    # Telegram-dialogue: ≤2-char lines over 15% of all dialogue lines
    telegram = [q for q in qs if count_text_chars(q) <= 2]
    if len(qs) >= 8 and len(telegram) / len(qs) > 0.15:
        warnings.append(
            f"telegram dialogue ratio too high ({len(telegram)}/{len(qs)} lines ≤2 chars); expand into characterful speech"
        )

    ps = paragraphs(text)
    max_dialogue_run = 0
    run = 0
    for p in ps:
        is_dialogue_only = bool(re.fullmatch(r"[「“『].{1,120}[」”』][。！？!?…—]*", p, re.S))
        if is_dialogue_only:
            run += 1
            max_dialogue_run = max(max_dialogue_run, run)
        else:
            run = 0
    if max_dialogue_run >= 6:
        warnings.append(f"floating dialogue run ({max_dialogue_run} dialogue-only paragraphs in a row)")

    question_answer_pairs = len(re.findall(r"[？?][」”』]?\s*\n\s*[「“『][^」”』]{1,12}[」”』]", text))
    if question_answer_pairs >= 5:
        warnings.append(f"repetitive question-answer dialogue ({question_answer_pairs} short replies after questions)")

    # Concept-metaphor pileup in one chapter (business/abstract mutual translation)
    metaphor_tokens = ["盐", "壳", "棋", "差价", "货门", "账本", "活靶"]
    metaphor_hits = sum(1 for tok in metaphor_tokens if text.count(tok) >= 2)
    if metaphor_hits >= 4:
        warnings.append(
            "concept-metaphor pileup (salt/shell/chess/price/goods/ledger reused); keep one main metaphor per scene"
        )

    return warnings


def adjective_weirdness_warnings(text: str) -> list[str]:
    """Flag abstract stacked modifiers that read as AI flavor labels."""
    warnings: list[str] = []
    patterns = [
        r"\w{1,6}得(?:克制|过分|刚好|刚刚好|故意)",
        r"(?:笑意|寒意|杀意|香气|茶香|铃|光)[^。\n]{0,8}(?:满|更满|净|真)[^。\n]{0,6}(?:满|更满|净|真)",
        r"安静得像",
        r"(?:香|冷|热|静|亮)得(?:像|仿佛)(?:故意|克制|小心)",
    ]
    hits: list[str] = []
    for pat in patterns:
        for m in re.finditer(pat, text):
            hits.append(m.group(0)[:24])
    if len(hits) >= 2:
        warnings.append(
            f"weird abstract modifiers ({len(hits)}): e.g. {', '.join(hits[:3])}; rewrite to concrete sensory detail"
        )
    return warnings


def has_sensory_or_action_signal(text: str) -> bool:
    return bool(
        re.search(
            r"[风雨雪霜寒热冷香腥疼痛汗血光影声响]"
            r"|[走奔跑跃退拦挡劈刺斩拍抓握抬低转看笑叹]",
            text,
        )
    )


def cmd_check(project_path_str: str) -> dict:
    """Run style checks across all chapters."""
    project_path = Path(project_path_str).resolve()
    spec_lock_path = project_path / "framework" / "spec_lock.md"
    drafts_dir = project_path / "drafts"
    ingredient_guide_path = project_path / "sources" / "ingredient_style_guide.md"

    if not spec_lock_path.exists():
        print("[ERROR] spec_lock.md not found")
        sys.exit(1)

    spec_text = spec_lock_path.read_text(encoding="utf-8", errors="ignore")
    target_ratio = target_dialogue_ratio(spec_text)
    chapters = sorted(drafts_dir.glob("chapter_*.md"))
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    print(f"Checking style across {len(chapters)} chapters...")

    if ingredient_guide_path.exists():
        info.append(f"Ingredient style guide present: {ingredient_guide_path.relative_to(project_path)}")
    else:
        info.append("No ingredient_style_guide.md found; local style assimilation was skipped or not needed")

    for chapter in chapters:
        text = chapter.read_text(encoding="utf-8", errors="ignore")
        body = prose_body(text)
        if not body:
            warnings.append(f"{chapter.name}: empty prose body")
            continue

        ratio = dialogue_ratio(body)
        if target_ratio is not None and ratio < target_ratio * 0.6:
            warnings.append(f"{chapter.name}: low dialogue ratio {ratio:.1%} vs target {target_ratio:.1%}")
        elif target_ratio is None and ratio < 0.18:
            warnings.append(f"{chapter.name}: low dialogue ratio {ratio:.1%}; prose may feel too report-like")

        long_paragraphs = [p for p in paragraphs(body) if count_text_chars(p) > 520]
        if long_paragraphs:
            warnings.append(f"{chapter.name}: {len(long_paragraphs)} paragraph(s) exceed 520 chars; mobile rhythm may feel heavy")

        hits = stiff_summary_hits(body)
        if hits:
            warnings.append(f"{chapter.name}: repeated stiff-summary phrases: {', '.join(hits[:5])}")

        nat_errors, nat_warnings = naturalness_findings(body)
        for err in nat_errors:
            errors.append(f"{chapter.name}: {err}")
        for warning in nat_warnings:
            warnings.append(f"{chapter.name}: {warning}")

        for warning in dialogue_quality_warnings(body):
            warnings.append(f"{chapter.name}: {warning}")

        for warning in adjective_weirdness_warnings(body):
            warnings.append(f"{chapter.name}: {warning}")

        if not has_reader_hook(body):
            warnings.append(f"{chapter.name}: opening may lack a concrete reader hook")

        if not has_next_click_ending(body):
            warnings.append(f"{chapter.name}: ending may lack a next-click hook")

        if ingredient_guide_path.exists() and not has_sensory_or_action_signal(body):
            warnings.append(f"{chapter.name}: ingredient guide exists but chapter shows little sensory/action craft signal")

    print("\n[OK] Style check complete")
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
        print("Usage: style_checker.py <project_path>")
        sys.exit(1)
    result = cmd_check(sys.argv[1])
    if result["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
