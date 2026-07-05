#!/usr/bin/env python3
"""Export a NovelMaster project to EPUB 3 using only the Python standard library.

Usage:
    python skills/novel-master/scripts/export_epub.py <project_path>

Outputs:
    <project_path>/export/<project_name>.epub
"""

from __future__ import annotations

import argparse
import html
import sys
import uuid
import zipfile
from datetime import datetime, timezone

from novel_utils import ensure_export_dir, load_chapters, load_config, markdown_to_html, project_slug, project_title, resolve_project


def cmd_export(project_path_str: str) -> None:
    project_path = resolve_project(project_path_str)
    config = load_config(project_path)
    chapters = load_chapters(project_path)

    if not chapters:
        print("[WARN] No chapter drafts found")
        return

    export_dir = ensure_export_dir(project_path)
    slug = project_slug(config, project_path)
    output_path = export_dir / f"{slug}.epub"
    title = project_title(config, project_path)
    author = str(config.get("author") or "Unknown")
    language = str(config.get("language") or "zh-CN")
    identifier = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, str(project_path))}"
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with zipfile.ZipFile(output_path, "w") as epub:
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        epub.writestr("META-INF/container.xml", container_xml())
        epub.writestr("EPUB/styles/novel.css", stylesheet())
        epub.writestr("EPUB/nav.xhtml", nav_xhtml(title, chapters, language))
        epub.writestr("EPUB/content.opf", content_opf(title, author, language, identifier, modified, chapters))

        for chapter in chapters:
            epub.writestr(
                f"EPUB/chapters/chapter_{chapter.number:03d}.xhtml",
                chapter_xhtml(title, chapter.number, chapter.title, chapter.body_markdown, language),
            )

    print(f"[OK] EPUB export complete: {output_path}")
    print(f"   Chapters: {len(chapters)}")
    print(f"   Identifier: {identifier}")


def container_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def stylesheet() -> str:
    return """body {
  font-family: "Noto Serif CJK SC", "Source Han Serif SC", serif;
  line-height: 1.8;
  margin: 5%;
}
h1, h2 {
  line-height: 1.35;
  text-align: center;
}
p {
  margin: 0 0 0.8em;
  text-indent: 2em;
}
nav ol {
  line-height: 1.8;
}
"""


def nav_xhtml(title: str, chapters, language: str) -> str:
    items = "\n".join(
        f'      <li><a href="chapters/chapter_{chapter.number:03d}.xhtml">Chapter {chapter.number:03d} {html.escape(chapter.title)}</a></li>'
        for chapter in chapters
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{html.escape(language)}">
<head>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="styles/novel.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>{html.escape(title)}</h1>
    <ol>
{items}
    </ol>
  </nav>
</body>
</html>
"""


def content_opf(title: str, author: str, language: str, identifier: str, modified: str, chapters) -> str:
    chapter_items = "\n".join(
        f'    <item id="chapter_{chapter.number:03d}" href="chapters/chapter_{chapter.number:03d}.xhtml" media-type="application/xhtml+xml"/>'
        for chapter in chapters
    )
    spine_items = "\n".join(f'    <itemref idref="chapter_{chapter.number:03d}"/>' for chapter in chapters)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{html.escape(identifier)}</dc:identifier>
    <dc:title>{html.escape(title)}</dc:title>
    <dc:creator>{html.escape(author)}</dc:creator>
    <dc:language>{html.escape(language)}</dc:language>
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="styles/novel.css" media-type="text/css"/>
{chapter_items}
  </manifest>
  <spine>
{spine_items}
  </spine>
</package>
"""


def chapter_xhtml(book_title: str, number: int, chapter_title: str, body_markdown: str, language: str) -> str:
    body = markdown_to_html(body_markdown)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="{html.escape(language)}">
<head>
  <title>{html.escape(chapter_title)} - {html.escape(book_title)}</title>
  <link rel="stylesheet" type="text/css" href="../styles/novel.css"/>
</head>
<body>
  <section>
    <h1>Chapter {number:03d} {html.escape(chapter_title)}</h1>
{body}
  </section>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a NovelMaster project to EPUB.")
    parser.add_argument("project_path")
    parser.add_argument("--volume-split", action="store_true", help="Accepted for compatibility; not used yet.")
    args = parser.parse_args()

    try:
        cmd_export(args.project_path)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
