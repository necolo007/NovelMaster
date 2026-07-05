# NovelMaster Web App

NovelMaster includes a local static web app for browsing generated project chapters and export files.

## Build Exports

```bash
python3 skills/novel-master/scripts/export_all.py projects/wuxia_yuwen_yuan
```

This writes the project collection to:

- `projects/<project>/export/<project>.txt`
- `projects/<project>/export/<project>.epub`
- `projects/<project>/export/<project>.md`

## Build Web Manifest

```bash
python3 skills/novel-master/scripts/build_web_manifest.py
```

The manifest is written to `web/projects.json`. To limit the app to one project:

```bash
python3 skills/novel-master/scripts/build_web_manifest.py projects/wuxia_yuwen_yuan
```

If Python is not available on the machine, use the Node fallback:

```bash
node build_web_manifest.js
```

## Build Chapter Memory

Archive completed chapter batches without moving files out of `drafts/`:

```bash
python3 skills/novel-master/scripts/chapter_memory.py projects/wuxia_yuwen_yuan --span 10
```

If Python is not available on the machine, use the Node fallback:

```bash
node chapter_memory.js projects/wuxia_yuwen_yuan --span=10
```

This writes:

- `projects/<project>/memory/chapters_001_010/`
- `projects/<project>/memory/memory_index.md`
- `projects/<project>/tracking/latest_memory.md`

## Open The App

Serve the `NovelMaster` directory with any static server, then open:

- `index.html`
- `viewer.html?project=wuxia_yuwen_yuan`

The included static server is:

```bash
node serve_web_app.js 4173
```
