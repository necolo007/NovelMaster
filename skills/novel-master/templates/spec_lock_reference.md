# Spec Lock — {novel_title}

> **Machine-readable execution contract.**
>
> Writer MUST `read_file` this file before generating each chapter.
> Architect produces this once; it locks for the entire pipeline.
>
> This file is the single source of truth. On any divergence with `framework/*.md` files, this file wins.

---

## §style — Style Parameters

```yaml
style:
  pov: "{first_person|third_person_limited|third_person_omniscient|multi_pov_rotating}"
  pov_character: "{character_name}"  # for limited POV; for multi-POV, list primary
  pov_characters: ["{primary}", "{secondary_1}", "{secondary_2}"]  # for multi-POV only
  pov_rotation:  # for multi-POV only
    primary_pov: "{protagonist_name}"
    primary_pov_pct: {float}  # e.g. 0.60 for 60%
    secondary_povs:
      - name: "{char_name}"
        pct: {float}
        chapters: [{int_list}]
        voice_signature: "{perception_style + vocabulary + internal_concerns}"
        independent_desire: "{one_sentence}"
        spotlight_chapters: [{int_list}]
        arc_milestones:
          - chapter: {int}
            milestone: "{description}"
    tertiary_povs:
      - name: "{antagonist_name}"
        pct: {float}
        chapters: [{int_list}]
        voice_signature: "{description}"
    rotation_rules:
      - "return_to_primary_every_3_chapters"
      - "no_head_hopping_within_scene"
      - "convergence_per_volume"
    convergence_chapters: [{int_list}]  # chapters where all POV threads intersect
  tense: "past"
  prose_style: "{style_descriptor}"
  register: "{colloquial|literary|mixed}"
  tone: "{tone_list}"
  dialogue_ratio_target: {float}  # e.g. 0.30 for 30%
  reader_lens:
    target_readers: ["{reader_profile_1}", "{reader_profile_2}"]
    emotional_pull: ["curiosity", "empathy", "tension", "warmth", "next_click"]
    avoid_voice: ["stiff_summary", "overly_archaic", "plot_report"]
  revision_loop:
    draft_pass: true
    reader_view_pass: true
    style_assimilation_pass: true
    final_polish_pass: true

  chapter_word_target: {int}
  chapter_word_min: {int}  # target × 0.85
  chapter_word_max: {int}  # target × 1.15

  pleasure_point_min_per_chapter: 1
  cliffhanger_required: true

  forbidden_patterns:
    - "no_omniscient_slip"
    - "no_character_iq_drop"
    - "no_power_scaling_collapse"
    - "no_exposition_dump"
    - "no_coincidence_abuse"
    - "no_emotion_telling"
```

---

## §world — World Quick Reference

```yaml
world:
  era: "{era}"
  geography: "{geography_type}"
  key_locations:
    - name: "{location_name}"
      type: "{city|region|realm|building}"
      significance: "{why it matters}"

  power_system:
    type: "{cultivation|magic|tech|psionics|none}"
    tiers:
      - name: "{tier_1_name}"
        rank: 1
        capabilities: "{summary}"
      - name: "{tier_2_name}"
        rank: 2
        capabilities: "{summary}"
      # ...
    rules:
      - "{hard_rule_1}"
      - "{hard_rule_2}"

  factions:
    - name: "{faction_name}"
      goal: "{goal}"
      relationship_to_mc: "{hostile|neutral|allied|complicated}"
    # ...

  world_rules:
    - "{unbreakable_world_rule_1}"
    - "{unbreakable_world_rule_2}"
```

---

## §characters — Character Quick Reference

```yaml
characters:
  protagonist:
    name: "{full_name}"
    aliases: ["{alias_1}"]  # if any
    age: {int}
    appearance: "{brief}"
    personality:
      surface: "{surface_trait}"
      middle: "{middle_trait}"
      deep: "{deep_trait}"
    core_drive: "{one_sentence}"
    speech_style: "{description}"
    power_level_current: "{tier_name}"
    power_level_peak: "{tier_name}"
    character_arc: "From {start} → To {end}"

  supporting:
    - name: "{name}"
      role: "{mentor|friend|rival|love_interest|comic_relief}"
      relationship_to_mc: "{description}"
      independent_desire: "{what they want beyond helping MC}"
      moral_logic: "{their ethical framework}"
      flaw: "{recurring mistake with real consequences}"
      personality_keywords: ["{kw1}", "{kw2}"]
      voice_signature: "{speech rhythm, vocabulary, verbal tics}"
      function: "{narrative_function}"
      spotlight_chapter: {int}  # chapter where their unique skill/choice changes outcome
      speech_style: "{description}"
      thematic_function: "{which theme they embody/challenge}"
      arc: "From {start} → To {end} (belief change, not just power change)"

  antagonists:
    - name: "{name}"
      motivation: "{motivation}"  # NOT "pure evil"
      mirror_to_mc: "{contrast}"
      power_level: "{tier}"
      arc: "{brief}"

  # Relationship network
  relationships:
    - pair: ["{char_a}", "{char_b}"]
      type: "{friends|romance|rivalry|mentor_student|enemies|family}"
      evolution: "From {start} → To {end}"

  # Group dynamics (ensemble only)
  group_dynamics:
    identity: "{what binds them together}"
    internal_frictions: ["{tension_1}", "{tension_2}"]
    evolution: "Formation → trust building → fracture → reconciliation → transformation"
    pair_chemistries:
      - pair: ["{char_a}", "{char_b}"]
        chemistry: "{mentor_student|rivals_with_respect|old_friends_with_baggage|reluctant_allies|unspoken_attraction}"
```

---

## §plot — Plot Quick Reference

```yaml
plot:
  volumes:
    - number: 1
      title: "{volume_title}"
      chapter_range: [1, {N}]
      core_conflict: "{conflict}"
      theme: "{theme}"
      climax_chapter: {int}

  plot_lines:
    A_main:
      description: "{description}"
      key_milestones: ["{m1}", "{m2}", "{m3}"]
    B_romance:
      description: "{description}"
      key_milestones: ["{m1}", "{m2}"]
    C_hidden:
      description: "{description}"
      key_milestones: ["{m1}", "{m2}"]

  opening_hook:
    strategy: "{strategy_name}"
    chapter_1_first_500_chars_must: "{requirement}"
```

---

## §chapters — Chapter Blueprint (Volume 1)

```yaml
chapters:
  - number: 1
    title: "{chapter_title}"
    core_conflict: "{one_sentence}"
    pov: "{character_name}"
    word_target: {int}
    characters_appearing: ["{name_1}", "{name_2}"]
    foreshadowing_plant: ["{brief_description}"]
    foreshadowing_resolve: []  # empty for chapter 1
    pleasure_point_type: "{power_up|face_slap|reward|reveal|romance_beat}"
    notes: "{any special instruction}"

  - number: 2
    # ...
```

---

## §foreshadowing — Foreshadowing Registry

```yaml
foreshadowing:
  - id: "fs_001"
    description: "{brief}"
    plant_chapter: {int}
    resolve_chapter: {int}
    urgency: "{low|medium|high}"

  # ...
```

---

## §constraints — Hard Constraints

```yaml
constraints:
  # Things the Writer must NEVER do
  never:
    - "Switch POV mid-chapter without scene break"
    - "Have characters act against established intelligence for plot convenience"
    - "Introduce new power tiers that contradict the established system"
    - "End a chapter without a hook/cliffhanger"
    - "Use omniscient narration phrases like '他不知道的是...'"
    - "Write exposition dumps longer than 3 sentences without breaking into action/dialogue"
    - "Create family-name contradictions unless the relationship explicitly explains alias, courtesy name, adopted status, maternal surname, or title/respect-name usage"

  # Things the Writer must ALWAYS do
  always:
    - "Include ≥1 pleasure point per chapter"
    - "Show emotions through action and physiology, not labels"
    - "Vary paragraph length for rhythm (1–5 sentences)"
    - "Use dialogue attribution via action beats, not '他说'"
    - "Track character power levels exactly — no unearned jumps"
    - "End every chapter with a hook"
    - "Audit appearing characters' kinship, aliases, surnames, ages, ranks, titles, and inheritance status against character profiles and trackers before drafting"

  # Word count targets
  word_count:
    per_chapter_target: {int}
    per_chapter_min: {int}
    per_chapter_max: {int}
    total_novel_target: {int}
```

---

## §ingredients — Reference Materials

```yaml
ingredients:
  style_guide:
    path: "sources/ingredient_style_guide.md"
    status: "{generated|absent|manual}"
    usage: "Craft influence only: rhythm, dialogue, sensory/action texture, emotional warmth, hook patterns"
    do_not_copy: ["plot_points", "character_designs", "scene_order", "prose_passages"]

  # Reference novels that inform style/tropes (read-only, never copy)
  reference_novels:
    - path: "{relative_path}"
      relevance: "{what aspects to study}"
      do_not_copy: ["plot_points", "character_designs", "prose_passages"]

  inspiration_docs:
    - path: "sources/{filename}"
      relevance: "{what to use}"

  # External references needed (populated by Reference Search phase if triggered)
  external_references: []
```
