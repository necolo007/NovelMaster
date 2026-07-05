#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = process.cwd();
const projectArg = process.argv[2];
const spanArg = process.argv.find((arg) => arg.startsWith('--span='));
const includeIncomplete = process.argv.includes('--include-incomplete');

if (!projectArg) {
  console.error('Usage: node chapter_memory.js <project_path> [--span=10] [--include-incomplete]');
  process.exit(1);
}

const projectPath = path.resolve(root, projectArg);
const configPath = path.join(projectPath, 'novel_config.json');
if (!fs.existsSync(configPath)) {
  console.error(`[ERROR] novel_config.json not found: ${projectPath}`);
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const span = Number(spanArg ? spanArg.slice('--span='.length) : config.memory_archive_interval || 10);
if (!Number.isInteger(span) || span <= 0) {
  console.error('[ERROR] --span must be a positive integer');
  process.exit(1);
}

function parseChapter(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  let body = raw;
  const metadata = {};

  if (raw.startsWith('---')) {
    const end = raw.indexOf('\n---', 3);
    if (end >= 0) {
      const frontmatter = raw.slice(3, end).trim().split(/\r?\n/);
      body = raw.slice(end + 4).trim();
      for (const line of frontmatter) {
        const match = line.match(/^([^:]+):\s*(.*)$/);
        if (!match) continue;
        let value = match[2].trim();
        if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
          value = value.slice(1, -1);
        }
        metadata[match[1].trim()] = value;
      }
    }
  }

  const number = Number(path.basename(filePath).match(/chapter_(\d+)/i)[1]);
  const heading = body.match(/^#\s+(.+)$/m);
  const title = metadata.title || (heading ? heading[1].trim() : `Chapter ${number}`);
  const bodyMarkdown = body.replace(/^#\s+.+$/m, '').trim();
  const plain = bodyMarkdown
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/[>*_`#-]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  const wordCount = Number(metadata.words) || (plain.match(/[\u4e00-\u9fff]/g) || []).length + (plain.match(/[A-Za-z0-9_]+/g) || []).length;

  return { number, title, bodyMarkdown, plain, metadata, wordCount, filePath };
}

function formatList(value) {
  return String(value || '').replace(/^\[/, '').replace(/\]$/, '');
}

function shortText(text, maxChars = 520) {
  if (text.length <= maxChars) return text;
  return `${text.slice(0, Math.floor(maxChars / 2)).trim()}\n\n...\n\n${text.slice(-Math.floor(maxChars / 2)).trim()}`;
}

function oneLine(text, maxChars = 140) {
  const clean = text.replace(/\s+/g, ' ').trim();
  return clean.length <= maxChars ? clean : `${clean.slice(0, maxChars - 1).trim()}...`;
}

function groupName(group) {
  return `chapters_${String(group[0].number).padStart(3, '0')}_${String(group[group.length - 1].number).padStart(3, '0')}`;
}

function readOptional(filePath) {
  return fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf8').trim() : '';
}

function writeGroup(group, memoryDir) {
  const name = groupName(group);
  const groupDir = path.join(memoryDir, name);
  const copiedDir = path.join(groupDir, 'chapters');
  fs.mkdirSync(copiedDir, { recursive: true });

  for (const chapter of group) {
    fs.copyFileSync(chapter.filePath, path.join(copiedDir, path.basename(chapter.filePath)));
  }

  const totalWords = group.reduce((sum, chapter) => sum + chapter.wordCount, 0);
  fs.writeFileSync(path.join(groupDir, 'README.md'), [
    `# ${config.title || config.project_name || 'Novel'} - Chapter Memory ${String(group[0].number).padStart(3, '0')}-${String(group[group.length - 1].number).padStart(3, '0')}`,
    '',
    `- Chapters: ${group.length}`,
    `- Words: ${totalWords}`,
    `- Generated at: ${new Date().toISOString()}`,
    '',
    'Keep `drafts/` as the source of truth. This folder is a lookup and memory layer.',
    '',
  ].join('\n'), 'utf8');

  const summaries = [`# Chapter Summaries ${String(group[0].number).padStart(3, '0')}-${String(group[group.length - 1].number).padStart(3, '0')}`, ''];
  for (const chapter of group) {
    summaries.push(
      `## Chapter ${String(chapter.number).padStart(3, '0')} ${chapter.title}`,
      '',
      `- Words: ${chapter.wordCount}`,
      `- POV: ${chapter.metadata.pov || ''}`,
      `- Characters: ${formatList(chapter.metadata.characters_appearing)}`,
      `- Foreshadowing planted: ${formatList(chapter.metadata.foreshadowing_planted)}`,
      `- Foreshadowing resolved: ${formatList(chapter.metadata.foreshadowing_resolved)}`,
      '',
      '### Quick Recall',
      '',
      shortText(chapter.plain),
      ''
    );
  }
  fs.writeFileSync(path.join(groupDir, 'chapter_summaries.md'), summaries.join('\n'), 'utf8');

  const trackingDir = path.join(projectPath, 'tracking');
  const memory = [
    `# Continuity Memory ${String(group[0].number).padStart(3, '0')}-${String(group[group.length - 1].number).padStart(3, '0')}`,
    '',
    `Novel: ${config.title || config.project_name || path.basename(projectPath)}`,
    `Chapter range: ${String(group[0].number).padStart(3, '0')}-${String(group[group.length - 1].number).padStart(3, '0')}`,
    `Total words in range: ${totalWords}`,
    '',
    '## Read Before Writing Later Chapters',
    '',
    '- Read this file together with `framework/spec_lock.md`, `tracking/context_summary.md`, `tracking/plot_tracker.json`, and `tracking/character_state.json`.',
    '- If this file conflicts with a newer tracker, the newer tracker wins.',
    '',
    '## Range Spine',
    '',
    ...group.map((chapter) => `- Chapter ${String(chapter.number).padStart(3, '0')} \`${chapter.title}\`: ${oneLine(chapter.plain)}`),
    '',
    '## Character And Plot Memory To Preserve',
    '',
    '### Character deltas',
    '',
    '- TBD',
    '',
    '### Relationship deltas',
    '',
    '- TBD',
    '',
    '### Power / item / secret deltas',
    '',
    '- TBD',
    '',
    '### Open hooks after this range',
    '',
    '- TBD',
    '',
  ];

  const context = readOptional(path.join(trackingDir, 'context_summary.md'));
  const plot = readOptional(path.join(trackingDir, 'plot_tracker.json'));
  const character = readOptional(path.join(trackingDir, 'character_state.json'));
  if (context) memory.push('## Current Rolling Context Snapshot', '', '```markdown', context, '```', '');
  if (plot) memory.push('## Plot Tracker Snapshot', '', '```json', plot, '```', '');
  if (character) memory.push('## Character State Snapshot', '', '```json', character, '```', '');
  fs.writeFileSync(path.join(groupDir, 'continuity_memory.md'), memory.join('\n'), 'utf8');

  fs.writeFileSync(path.join(groupDir, 'chapters_manifest.json'), `${JSON.stringify({
    range: { from: group[0].number, to: group[group.length - 1].number },
    chapters: group.map((chapter) => ({
      number: chapter.number,
      title: chapter.title,
      source_path: path.relative(projectPath, chapter.filePath).replace(/\\/g, '/'),
      word_count: chapter.wordCount,
      metadata: chapter.metadata,
    })),
  }, null, 2)}\n`, 'utf8');

  return groupDir;
}

const draftsDir = path.join(projectPath, 'drafts');
const chapters = fs.readdirSync(draftsDir)
  .filter((file) => /^chapter_\d+\.md$/i.test(file))
  .sort()
  .map((file) => parseChapter(path.join(draftsDir, file)));

const byNumber = new Map(chapters.map((chapter) => [chapter.number, chapter]));
const maxChapter = Math.max(...chapters.map((chapter) => chapter.number));
const groups = [];
for (let start = 1; start <= maxChapter; start += span) {
  const group = [];
  for (let number = start; number < start + span; number += 1) {
    if (byNumber.has(number)) group.push(byNumber.get(number));
  }
  if (group.length === span || (includeIncomplete && group.length)) groups.push(group);
}

if (!groups.length) {
  console.log(`[WARN] No complete ${span}-chapter group found.`);
  process.exit(0);
}

const memoryDir = path.join(projectPath, 'memory');
fs.mkdirSync(memoryDir, { recursive: true });
const groupDirs = groups.map((group) => writeGroup(group, memoryDir));

const index = [
  `# Memory Index - ${config.title || config.project_name || path.basename(projectPath)}`,
  '',
  `Generated at: ${new Date().toISOString()}`,
  '',
  '## Archives',
  '',
  ...groups.map((group) => {
    const name = groupName(group);
    const words = group.reduce((sum, chapter) => sum + chapter.wordCount, 0);
    return `- [${name}](${name}/continuity_memory.md): chapters ${String(group[0].number).padStart(3, '0')}-${String(group[group.length - 1].number).padStart(3, '0')}, ${words} words`;
  }),
  '',
];
fs.writeFileSync(path.join(memoryDir, 'memory_index.md'), index.join('\n'), 'utf8');

const latestMemory = path.join(projectPath, 'tracking', 'latest_memory.md');
fs.copyFileSync(path.join(groupDirs[groupDirs.length - 1], 'continuity_memory.md'), latestMemory);

console.log(`[OK] Chapter memory archived: ${memoryDir}`);
console.log(`   Span: ${span}`);
console.log(`   Groups: ${groupDirs.length}`);
console.log(`   Latest memory: ${latestMemory}`);
