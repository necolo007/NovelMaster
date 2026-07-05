#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = process.cwd();
const projectArgs = process.argv.slice(2).filter((arg) => !arg.startsWith('--'));
const outputArg = process.argv.find((arg) => arg.startsWith('--output='));
const outputPath = path.resolve(root, outputArg ? outputArg.slice('--output='.length) : 'web/projects.json');

function findProjects() {
  if (projectArgs.length) {
    return projectArgs.map((projectPath) => path.resolve(root, projectPath));
  }
  const projectsDir = path.join(root, 'projects');
  if (!fs.existsSync(projectsDir)) return [];
  return fs.readdirSync(projectsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(projectsDir, entry.name))
    .filter((projectPath) => fs.existsSync(path.join(projectPath, 'novel_config.json')));
}

function relativeToRoot(filePath) {
  return path.relative(root, filePath).replace(/\\/g, '/');
}

function parseFrontmatter(raw) {
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

  const heading = body.match(/^#\s+(.+)$/m);
  const title = metadata.title || (heading ? heading[1].trim() : '');
  const bodyMarkdown = body.replace(/^#\s+.+$/m, '').trim();
  const plain = bodyMarkdown
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/[>*_`#-]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  const words = (plain.match(/[\u4e00-\u9fff]/g) || []).length + (plain.match(/[A-Za-z0-9_]+/g) || []).length;

  return { metadata, title, bodyMarkdown, plain, words };
}

function projectToManifest(projectPath) {
  const config = JSON.parse(fs.readFileSync(path.join(projectPath, 'novel_config.json'), 'utf8'));
  const draftsDir = path.join(projectPath, 'drafts');
  const chapters = fs.existsSync(draftsDir)
    ? fs.readdirSync(draftsDir)
      .filter((file) => /^chapter_\d+\.md$/i.test(file))
      .sort()
      .map((file) => {
        const number = Number(file.match(/chapter_(\d+)/i)[1]);
        const filePath = path.join(draftsDir, file);
        const parsed = parseFrontmatter(fs.readFileSync(filePath, 'utf8'));
        return {
          number,
          title: parsed.title || `Chapter ${number}`,
          path: relativeToRoot(filePath),
          wordCount: Number(parsed.metadata.words) || parsed.words,
          metadata: parsed.metadata,
          plainPreview: parsed.plain.slice(0, 240),
        };
      })
    : [];

  const exportDir = path.join(projectPath, 'export');
  const memoryDir = path.join(projectPath, 'memory');
  const exports = fs.existsSync(exportDir)
    ? fs.readdirSync(exportDir)
      .map((file) => path.join(exportDir, file))
      .filter((filePath) => fs.statSync(filePath).isFile() && !path.basename(filePath).startsWith('.'))
      .sort()
      .map((filePath) => ({
        name: path.basename(filePath),
        path: relativeToRoot(filePath),
        size: fs.statSync(filePath).size,
      }))
    : [];

  const memoryArchives = fs.existsSync(memoryDir)
    ? fs.readdirSync(memoryDir)
      .map((file) => path.join(memoryDir, file))
      .filter((filePath) => fs.statSync(filePath).isDirectory() && /^chapters_\d+_\d+$/i.test(path.basename(filePath)))
      .sort()
      .map((archivePath) => {
        const continuityPath = path.join(archivePath, 'continuity_memory.md');
        const summariesPath = path.join(archivePath, 'chapter_summaries.md');
        const manifestPath = path.join(archivePath, 'chapters_manifest.json');
        return {
          name: path.basename(archivePath),
          path: relativeToRoot(archivePath),
          continuityPath: fs.existsSync(continuityPath) ? relativeToRoot(continuityPath) : '',
          summariesPath: fs.existsSync(summariesPath) ? relativeToRoot(summariesPath) : '',
          manifestPath: fs.existsSync(manifestPath) ? relativeToRoot(manifestPath) : '',
        };
      })
    : [];

  return {
    id: config.project_name || path.basename(projectPath),
    title: config.title || path.basename(projectPath),
    author: config.author || '',
    genre: config.genre || '',
    genreLabel: config.genre_label || config.genre || '',
    language: config.language || 'zh-CN',
    pipelineState: config.pipeline_state || '',
    targetWords: config.target_words || 0,
    chapterAvgWords: config.chapter_avg_words || 0,
    createdAt: config.created_at || '',
    path: relativeToRoot(projectPath),
    stats: {
      chapters: chapters.length,
      words: chapters.reduce((sum, chapter) => sum + (chapter.wordCount || 0), 0),
      exports: exports.length,
      memories: memoryArchives.length,
    },
    exports,
    memoryArchives,
    chapters,
  };
}

const projects = findProjects().map(projectToManifest);
const manifest = {
  generatedAt: new Date().toISOString(),
  projects,
  stats: {
    projects: projects.length,
    chapters: projects.reduce((sum, project) => sum + project.stats.chapters, 0),
    words: projects.reduce((sum, project) => sum + project.stats.words, 0),
    exports: projects.reduce((sum, project) => sum + project.stats.exports, 0),
    memories: projects.reduce((sum, project) => sum + (project.stats.memories || 0), 0),
  },
};

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
console.log(`[OK] Web manifest built: ${outputPath}`);
