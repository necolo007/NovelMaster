# Shared Writing Standards

Common web novel writing constraints for Novel Master, eliminating cross-role file duplication. These rules apply to the Writer role and are audited by the Editor role.

---

## 1. Web Novel Format Conventions (网文格式规范)

### 1.1 Chapter Structure

Every chapter file (`drafts/chapter_NNN.md`) MUST include:

```markdown
---
chapter: <N>
title: "<title>"
pov: "<POV character>"
words: <count>
characters_appearing: ["<name>", ...]
foreshadowing_planted: ["<description>", ...]
foreshadowing_resolved: ["<ref>", ...]
pleasure_points: ["<type>: <brief>", ...]
---

# 第<N>章 <title>

<prose>
```

**Rules**:
- `chapter`: 1-based integer, zero-padded to 3 digits in filename
- `title`: Chinese quotation marks `「」` preferred over `""` for chapter titles in prose body
- `words`: count of Chinese characters + punctuation in the prose body (not including frontmatter)
- Frontmatter MUST be valid YAML between `---` delimiters
- Body begins after the second `---` with the chapter heading

### 1.2 Prose Formatting

| Rule | Standard |
|------|----------|
| Paragraph separation | Blank line between paragraphs |
| Paragraph indent | None (web novel platform standard — blank-line separation replaces indentation) |
| Dialogue | Each speaker's dialogue in its own paragraph |
| Internal monologue | No special markers needed; integrate naturally or use 「」 for direct thoughts |
| Scene breaks | Use `* * *` or `---` on its own line |
| Chapter title in body | `# 第N章 <title>` as H1 heading |
| Section breaks within chapter | `## <section title>` as H2 if needed |

### 1.3 Punctuation & Typography

| Rule | Standard |
|------|----------|
| Quotation marks | `「」` for dialogue (web novel convention) or `""` (traditional). Be consistent throughout. |
| Thought markers | `『』` for direct thoughts if distinguished from dialogue |
| Dashes | `——` (em dash × 2 in Chinese) for breaks/interruptions |
| Ellipsis | `……` (×2) for trailing off |
| Emphasis | **Bold** for key terms on first introduction; *italic* sparingly for internal emphasis |
| Foreign terms | Keep in original Latin script if untranslatable; add Chinese gloss in parentheses on first use |

---

## 2. Banned Patterns (禁止写法)

The following patterns are FORBIDDEN in generated chapters. These rules have the same severity as SVG banned features in PPT-Master — violating any one of them constitutes a quality failure.

### 2.1 Narrative Bans

| Banned Pattern | Explanation | Example of Violation |
|---------------|-------------|---------------------|
| **Omniscient slip** (上帝视角旁白) | Third-person limited POV must not reveal information the POV character doesn't know | "林星河不知道的是，在城市的另一端，苏晴正在…" |
| **Character IQ drop** (角色智商下线) | Characters must not act against their established intelligence/experience for plot convenience | Genius strategist falls for obvious trap with no misdirection |
| **Power scaling collapse** (战力崩坏) | Power levels established in the world system must remain consistent | B级 defeats SSS级 "through willpower" |
| **Exposition dump** (设定说明文) | World-building info must be woven into action/dialogue, not delivered as lecture paragraphs | 500+ character block of pure world history |
| **Coincidence abuse** (巧合过多) | Plot resolution through coincidence rather than character agency | Protagonist "happens to be passing by" for the 5th critical moment |
| **Emotion telling** (情感直白) | Stating emotions instead of showing them through action/physiology | "他很愤怒" instead of "他的拳头攥紧了" |

### 2.2 Prose Quality Bans

| Banned Pattern | Explanation | Example of Violation |
|---------------|-------------|---------------------|
| **Adjective stacking** | 3+ consecutive adjectives modifying the same noun | "那是一个巨大的、宏伟的、令人震撼的、无与伦比的宫殿" |
| **Cliché battle** | Overused combat descriptions | "电光火石之间" for every fight scene |
| **Reaction-shot loop** | Same pattern: event → crowd gasps → protagonist smirks → repeat | Used ≥3 times in one chapter |
| **Empty intensifiers** | Filler words that don't add meaning | "非常", "十分", "极其" used as crutches |
| **Floating dialogue** | Extended dialogue exchanges with no attribution, action, or setting | 10+ lines of pure dialogue with no beats |
| **Redundant inner monologue** | Protagonist narrates what the reader already saw happen | "刚才那一剑，他用的是家传剑法的第三式——" (reader just read the fight) |

---

## 3. Chinese Web Novel Craft Standards (网文写作工艺标准)

### 3.1 "Show, Don't Tell" Implementation

| Instead of… | Show… |
|-------------|-------|
| "他很紧张" | "他的手指无意识地敲击着桌面，额角渗出了细密的汗珠。" |
| "房间里很豪华" | "水晶吊灯将光线折射成七彩的光斑，洒在波斯手工地毯上。脚下的大理石打磨得能照出人影。" |
| "她非常漂亮" | "她走进来时，茶馆里有那么一瞬安静得只剩下风铃声。" |
| "两人关系很好" | "他把最后一块红烧肉夹到她碗里，动作熟练得像呼吸。" |
| "他很强大" | "他站在那里，甚至没有拔出武器。对面三个壮汉却齐齐后退了一步。" |

### 3.2 Dialogue Craft

**Attribution beats**: prefer action over "said":

| Weak | Strong |
|------|--------|
| "你来晚了。"他说。 | 老陈头也没抬，手里的烟斗在桌角磕了磕。"你来晚了。" |
| "我不知道！"她急切地说。 | 苏晴猛地站起来，椅子在地板上刮出刺耳的声响。"我不知道！" |

**Subtext requirement**: dialogue should often convey more than the literal words. Characters lie, deflect, hint, and talk past each other.

**Voice differentiation**: each major character should have identifiable speech patterns:
- Word choice (formal/colloquial, technical/plain)
- Sentence length (terse/elaborate)
- Verbal tics (catchphrases, filler words, silence patterns)
- What they DON'T say (taboo topics, avoidance patterns)

### 3.3 Pleasure-Point Engineering (爽点工程)

Every chapter MUST contain ≥1 pleasure point. Types and execution:

| Type | Execution Standard |
|------|-------------------|
| **Power-up** (升级) | Show struggle → breakthrough moment → sensory detail of transformation → others' reactions → immediate application |
| **Face-slap** (打脸) | Build antagonist arrogance → protagonist understated response → reveal/twist → antagonist humiliation → witness reactions (amplifier) → protagonist moves on without gloating (magnanimity = extra satisfaction) |
| **Reward** (收获) | Setup: effort/risk invested → payout: concrete, usable, exceeds expectation slightly → hook: this opens new possibilities |
| **Reveal** (揭秘) | Plant clues earlier → reveal reframes previous events → "so THAT'S why!" reaction → new questions raised |
| **Romance beat** (感情升温) | Show through action (protection, sacrifice, understanding) → emotional resonance > physical description → relationship status change is earned |

### 3.4 Chapter Ending Hook Patterns (断章钩子)

Every chapter MUST end with a hook that compels reading the next chapter:

| Hook Type | Pattern | Example |
|-----------|---------|---------|
| **Cliffhanger** | Cut at moment of maximum tension | "门开了。门外站着的人，是他以为这辈子都不会再见到的那张脸。" |
| **Reveal teaser** | Promise information next chapter | "他终于明白了那块玉佩的真正含义——但这个答案，远比他想得更可怕。" |
| **Consequence anticipation** | Show that current action will have big repercussions | "他不知道的是，今天说的这句话，会在三天后让整个宗门倾巢而出。" |
| **Mystery plant** | Pose a new question | "信上的笔迹，他认识。但写信的人，三年前就已经死了。" |
| **Goal shift** | Protagonist makes new decision | "他原本只想活下去。但现在，他要让整个林家……血债血偿。" |

**Anti-patterns** (weak endings):
- Characters going to sleep
- "And then they continued their journey"
- Resolution with no new question
- Summary narration ("接下来的几天平静无事")

---

## 4. Platform Compliance (平台合规)

### 4.1 Content Sensitivity (内容敏感词)

The Editor's sensitivity check scans for:

- Political references to real-world entities/events
- Excessive graphic violence (torture scenes, detailed gore)
- Sexual content (platforms have strict rules; keep to implied/off-screen)
- Real-world religious/cultural sensitivity
- Platform-specific banned categories (varies by platform)

### 4.2 Chapter Title Compliance

- Keep chapter titles within platform character limits (typically ≤20 Chinese characters)
- Avoid clickbait that doesn't match chapter content
- Number format: use Chinese numerals (第一章) or Arabic (第1章) consistently

### 4.3 Serialization Readiness

- First 20 chapters are critical — platform algorithms judge retention here
- Chapter 1 MUST establish: protagonist, world hook, core conflict, and genre promise within first 500 characters
- Volume endings should feel like season finales (climax + partial resolution + new direction)

---

## 5. Tracker Format Standards

### 5.1 `context_summary.md` — Must include:

```markdown
# Context Summary — {novel_title}

> Current chapter: {N}
> Next chapter: {N+1}

## Story So Far
(3–5 sentence flowing narrative of recent events)

## Character States
| Character | Location | Status | Recent Changes |
|-----------|----------|--------|-----------------|

## Active Foreshadowing
| ID | Description | Planted Ch | Urgency | Notes |
|----|-------------|------------|---------|-------|

## Recent Rhythm
(Visual bar chart of last 5 chapters)
```

### 5.2 `plot_tracker.json` — Valid JSON, schema:

```json
{
  "foreshadowing": [
    {
      "id": "fs_NNN",
      "description": "string",
      "planted_chapter": "integer",
      "planted_detail": "string",
      "urgency": "low|medium|high",
      "status": "active|resolved|abandoned",
      "resolved_chapter": "integer|null",
      "resolved_detail": "string|null",
      "abandoned_reason": "string|null"
    }
  ],
  "summary": {
    "total_planted": "integer",
    "total_resolved": "integer",
    "total_abandoned": "integer",
    "active": "integer"
  }
}
```

### 5.3 `character_state.json` — Valid JSON

Must track location, health, power level, relationship states, active goals, and key inventory for every active character. Updated after every chapter.

---

## 6. Word Count Standards

### 6.1 Counting Method

- Chinese text: count all characters including punctuation via standard `len()` on the prose body
- Mixed CJK + Latin: count each CJK character as 1, each Latin word as 1 (approximately)
- Chapter word count = count of prose body text only (exclude frontmatter, exclude chapter title heading)

### 6.2 Target Tolerance

- Per chapter: target ±15% (e.g., 3000 word target → 2550–3450 acceptable)
- Per volume: total target ±5%
- Total novel: total target ±3%

---

## 7. File Naming Conventions

| File | Pattern | Example |
|------|---------|---------|
| Chapter drafts | `chapter_NNN.md` | `chapter_001.md`, `chapter_042.md` |
| Framework files | `snake_case.md` | `world_building.md`, `character_profiles.md` |
| Tracker files | `snake_case.md` / `snake_case.json` | `context_summary.md`, `plot_tracker.json` |
| Export files | `<novel_slug>.<ext>` | `star_river_emporium.txt` |
| Source files | Original name preserved in `sources/` | `inspiration.md`, `reference_notes.txt` |
