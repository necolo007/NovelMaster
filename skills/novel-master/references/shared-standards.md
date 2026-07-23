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
| **Head-hopping** (视角跳跃) | Switching POV within a scene without a scene break. Multi-POV novels switch at chapter boundaries or explicit scene breaks only | Paragraph 1: from 林星河's head, Paragraph 2: suddenly in 苏晴's head, same scene |
| **POV knowledge leak** (视角知识泄露) | In multi-POV novels, a POV character must not know or intuit information they only learned in another character's POV chapter | 冷月婵 in her POV chapter suddenly knowing a secret that was revealed to the reader in 林星河's POV chapter, with no narrative transmission |
| **Character IQ drop** (角色智商下线) | Characters must not act against their established intelligence/experience for plot convenience | Genius strategist falls for obvious trap with no misdirection |
| **Power scaling collapse** (战力崩坏) | Power levels established in the world system must remain consistent | B级 defeats SSS级 "through willpower" |
| **Kinship/name contradiction** (亲属姓名逻辑错误) | Relatives' surnames, aliases, titles, ages, or inheritance status conflict without in-story explanation | Father is named 剑无极 and daughter 冷月婵, but no profile/prose explains that 剑无极 is a title or alias |
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
| **Ornamental metaphor chain** | Multiple abstract metaphors explain the same feeling without new action or decision | "那句话像针，又像旧伤，又像火星…" after the scene already shows pressure |
| **Unlike-like ladder** (双否一肯比喻梯) | 用「不像A，也不像B。像C」或对白里「像A，又像B」代替直接判断；对白中尤为假 | 「这股劲……不像血煞，也不像正道。像把路封死的闸。」；**对白禁止**，叙述每章最多 1 处且优先改写 |
| **AI-literary cadence** | Repeated paragraph shapes used to sound profound rather than natural | "它不像X。X会Y。可它像Z。" / "不是A。是B。" / **同句**「不是A，是B」「不是A——是B」反复当解释器用 |
| **Empty fragment stacking** | Several single-sentence or single-word paragraphs that do not create rhythm, tension, or emphasis | "很轻。很冷。很疼。不是疼。" |
| **Incomplete catalog dialogue** (残缺对白/分工电报) | 对白用单字谓、目录式短句切分工，句子不完整 | 「你主查。我主护。她主听。」→ 应写成完整口语句 |
| **Decorative em dash** (装饰破折号) | 用「——」制造文艺停顿、纠偏解释，或替代逗号/句号；同章装饰性破折号过密 | 「钉尖对准丹田——不是刺心，是封种」；「他忽然很清楚一件事——自己怕的是…」 |
| **Not-but gloss ladder** (纠偏句式) | 先否后肯的标签式讲解：用「不是/不像…是/而是…」替读者下结论，而不是直接写动作、感官或判断 | 「钉尖对准丹田——不是刺心，是封种」「点头不是拜，是认」；**每章最多 1 处**，且仅当角色认知当场翻转时可用 |
| **Undifferentiated POV voice** (群像声音雷同) | In multi-POV novels, different POV characters' narration reads with the same perception style, vocabulary, and internal concerns | 冷月婵's POV chapter reads like 林星河's with the name swapped |
| **Cheerleader syndrome** (配角啦啦队化) | Supporting characters in a scene exist only to react to/admire/validate the protagonist, with no independent perspective or action | Every support character's line is a variation of "你说得对" or "太厉害了" |

---

### 2.3 Reader-Experience Bans

| Banned Pattern | Explanation | Example of Violation |
|---------------|-------------|---------------------|
| **Stiff summary voice** | Important emotional or action moments are summarized at a distance instead of dramatized | "他们交谈许久，终于互相信任" with no lived exchange |
| **Reader-hook vacuum** | Scene has plot facts but no question, pressure, desire, threat, intimacy shift, or next-click reason | Chapter ends after logistics with no new promise |
| **Reference copying** | Borrowing ingredient plot, character design, scene order, or recognizable prose instead of craft signals | Same setup/twist/line shape as a reference novel |
| **Decorative emotional recap** | A paragraph restates what the previous action/dialogue already proved | After a character is publicly humiliated, adding a long explanation that humiliation hurts |
| **Generic dialogue voice** | Lines can be swapped between characters with no loss of identity | Every character answers in the same clipped "嗯/知道/好/不是" rhythm |
| **POV-character-as-camera** | A POV chapter where the POV character merely observes events happening to others, with no personal stakes, choices, or emotional arc | 冷月婵's chapter is just her watching 林星河 fight someone |
| **Group-scene agreement spiral** | In a group scene (3+ characters), everyone takes turns agreeing with or supporting the same character, creating no friction or dynamic | A planning scene where every character says "我同意" in their own words |

---

### 2.4 Ensemble-Specific Quality Standards (群像质量标准)

When the novel uses multi-POV/ensemble cast, the following additional standards apply:

#### 2.4.1 POV Voice Differentiation Standard

Each POV character's narration MUST differ in at least 3 of these 5 dimensions:

| Dimension | How to Differentiate |
|-----------|---------------------|
| **Perception priority** | What sensory input does this character notice first? (Visual details / sounds / body language / spatial relationships / emotional atmosphere) |
| **Vocabulary range** | Formal vs. colloquial, technical jargon from their profession, metaphors drawn from their life experience |
| **Sentence rhythm** | Short and punchy vs. flowing and layered. Do they think in fragments or complete arguments? |
| **Value filter** | What do they judge automatically? (Fairness / efficiency / beauty / discipline / loyalty / truth) |
| **Memory palette** | What kind of memories surface unbidden? (Failures / betrayals / moments of peace / faces of the dead / promises made) |

#### 2.4.2 Screen Time Balance Standard

- Primary POV (protagonist): must NOT exceed 70% of total chapters
- Each secondary POV character: minimum 3 dedicated chapters per volume
- No named supporting character should vanish for >15 consecutive chapters without narrative reason
- Antagonist POV: at least 1 chapter per volume to maintain threat credibility

#### 2.4.3 Supporting Character Arc Standard

- Each supporting character with a POV must have at least 1 belief that is challenged and evolves
- Their arc must intersect with the main plot at ≥3 points (not run parallel indefinitely)
- Their independent desire must create friction with the protagonist's goal at least once

---

## 3. Chinese Web Novel Craft Standards (网文写作工艺标准)

### 3.0 Reader-View Revision Standard

Before a chapter is finalized, revise it from the reader's seat:

| Reader Need | Chapter Requirement |
|-------------|---------------------|
| Curiosity | The first 1-3 paragraphs create a concrete question, pressure, or promise |
| Empathy | The POV character has a human-scale want, fear, embarrassment, tenderness, or stubbornness |
| Presence | Scenes include grounded physical action and at least one non-visual sensory detail |
| Social charge | Dialogue changes status, trust, affection, rivalry, or hidden information |
| Payoff | The chapter's pleasure point has setup, turn, and aftershock |
| Next click | The ending leaves a cost, discovery, decision, threat, or emotional shift unresolved |

Ingredient-derived style guides may influence rhythm, density, dialogue craft, sensory texture, and hook shape. They must not supply plot events, character designs, or quotable phrasing.

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

**Dialogue audit requirements**:
- Every exchange must have a purpose: power shift, intent reveal, pressure, intimacy, humor, or useful plot movement.
- Avoid long runs of question-answer-confirmation. Interrupt with motive, action, evasion, or a line that could only belong to that character.
- One-word replies are allowed only when the silence is the point. Otherwise replace them with a characterful line or an action beat.
- If a line can be spoken by another character without changing wording, rewrite it using that character's diction, status, and current desire.

**对白有味硬规则（防电报腔 / 防干涩）**：
- **短 ≠ 瘪**：「冷冽」「简洁」指句子有刃、有身份、有潜台词，不是把人写成只会回「嗯 / 问 / 出 / 走 / 条件」。
- **句子要完整**：对白禁止目录式单字谓分工。「你主查。我主护。她主听。」必须改成能上口的完整句（例：「你查。我护着。她听风。」仍偏电报 → 「你主查脚印，我护侧翼，她听铃。」或更自然的口语句）。单字谓语「主X」连续出现视为失败。
- **电报腔上限**：单章内 ≤2 字的对白（如「问。」「出。」「走。」「越界。」）合计不超过对白条数的 **15%**；超过必须扩写成带身份信息的短句，或并入动作节拍。
- **每场关键对谈 ≥1 句带刺/带热/带笑**：机锋、护短、嘲讽、心虚掩饰、故意偏题均可——纯情报交换式对白视为失败。
- **角色口吻要「听得出是谁」**：冷角色可以短，但短句里仍要有判断与压力（例：✗「越界。」→ ✓「你问到这儿，就别装做客。」）；俏皮角色要有绕弯与试探，不能只丢规则说明书。
- **素材同款呼吸**：有 `ingredient_style_guide.md` 时，对白优先学其「有来有回、夹动作、夹气味/触感」的写法，禁止只保留剧情要点的提纲腔。

**形容词 / 修饰怪味禁令**：
- 禁止「抽象副词 + 抽象形容词」叠味：如「香得克制」「笑意满，眼里更满」「安静得像故意」「茶香真，水汽净」——读起来像在给气氛贴标签，不像人在场。
- 优先改成**可感可验**的细节：温度、触感、气味来源、肢体小动作、器物反应。
  - ✗「茶香得克制」→ ✓「茶香淡，刚揭盖那一下才闻得清」
  - ✗「腕铃安静，安静得像故意」→ ✓「腕铃被她用指腹按住，一响也无」
- 禁止概念隐喻连射：同一场戏里不要连续用「盐 / 壳 / 棋 / 差价 / 货 / 账」互译人际关系；一场保留 **一个** 主隐喻即可，其余改成直接利害与动作。
- 形容词服务判断，不服务「文艺感」：若删掉该修饰句，情节与人物关系不变，则删。

**Prose naturalness requirements**:
- Keep only one strong image per emotional beat.
- Cut paragraphs that merely explain a metaphor or repeat an already clear feeling.
- Prefer concrete verbs and scene movement over abstract commentary.
- Do not use repeated "不是/是", "不像/像", "可/却" sentence ladders as a default literary effect.
- **纠偏句式硬限制**：同句「不是A，是B / 不是A——是B / 不是A，而是B」与跨句「不是A。是B。」合并计数；**每章默认 ≤1 处**。超过即视为质量失败，须改写后再过稿。
- **双否一肯比喻梯硬限制**：禁止「不像A，也不像B。像C」及对白内「像A，又像B」叠喻。对白中出现即失败；叙述每章最多 1 处，优先改成直接判断或单一具体喻体。
  - ✗「这股劲……不像血煞，也不像正道。像把路封死的闸。」 → ✓「这股劲邪门，像闸门把路封死。」 / 「这股劲不是血煞，也不是正道剑气——」仍用破折号也不如：✓「这股劲邪门，路都被封死了。」
  - ✗「像生怕被落下，又像生怕他们并坐太熟。」 → ✓「她挤到中间，生怕被落下。」
- **破折号硬限制**：「——」默认少用。仅允许：(1) 对白被打断/话说一半；(2) 极少数不得不插入的同位说明。禁止用「——」制造文艺停顿、纠偏解释（「——不是/像/要…」），也禁止拿它代替逗号或句号。装饰性破折号同章建议 ≤4，超过须改写。
  - ✗「他忽然很清楚一件事——自己怕的是被活着拿走。」 → ✓「他忽然很清楚：自己怕的是被活着拿走。」
  - ✗「钉尖对准丹田——不是刺心，是封种。」 → ✓「钉尖对准丹田，要封种。」
- **改写优先直接陈述**：删掉「不是…」半句，只保留真实动作/判断；或改成感官/后果描写。
  - ✗「脚步不是慌乱。是故意的试探。」 → ✓「脚步轻得不像慌，倒像故意试探。」 / 「有人在附近丢石子试探。」
  - ✗「钉尖对准丹田——不是刺心，是封种。」 → ✓「钉尖对准丹田，要封种。」
  - ✗「点头不是拜，是认。」 → ✓「那一点头，等于认：从此同路。」
- A polished paragraph should sound like a confident storyteller, not a caption explaining why the moment matters.

### 3.2.1 Logic & Name Audit

Before finalizing a chapter, verify named characters against the framework and trackers:

- Family members should share the expected surname unless the story explicitly establishes a title, alias, courtesy name, adopted relationship, maternal surname, or other cultural reason.
- If a character is usually called by title or江湖名号, the real name and title relationship must be recorded in `character_profiles.md`, `spec_lock.md`, and `character_state.json`.
- Do not repair a name contradiction only in narration. Update the framework/tracker anchor so future chapters inherit the fix.
- Check ages, ranks, sect positions, injuries, possessions, and relationship status whenever they are mentioned in dialogue or narration.

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
