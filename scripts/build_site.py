#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "openai-codex-best-practices.ko.md"
DIST = ROOT / "dist"
ASSET_FILES = ["styles.css", "script.js"]


def slugify(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s가-힣-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def parse_inlines(text: str) -> str:
    pattern = re.compile(
        r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|\*([^*]+)\*"
    )
    parts: list[str] = []
    last = 0

    for match in pattern.finditer(text):
        parts.append(html.escape(text[last : match.start()]))

        code, link_text, href, strong_text, em_text = match.groups()
        if code is not None:
            parts.append(f"<code>{html.escape(code)}</code>")
        elif link_text is not None and href is not None:
            safe_href = html.escape(href, quote=True)
            parts.append(
                f'<a href="{safe_href}">{parse_inlines(link_text)}</a>'
            )
        elif strong_text is not None:
            parts.append(f"<strong>{parse_inlines(strong_text)}</strong>")
        elif em_text is not None:
            parts.append(f"<em>{parse_inlines(em_text)}</em>")

        last = match.end()

    parts.append(html.escape(text[last:]))
    return "".join(parts)


def parse_table(lines: list[str], start: int) -> tuple[str, int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        rows.append([cell.strip() for cell in lines[i].strip().strip("|").split("|")])
        i += 1

    header = rows[0]
    body = rows[2:] if len(rows) > 2 else []
    header_html = "".join(f"<th>{parse_inlines(cell)}</th>" for cell in header)
    body_rows = []
    for row in body:
        cells = "".join(f"<td>{parse_inlines(cell)}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")

    table_html = [
        '<div class="table-wrap">',
        "<table>",
        "<thead>",
        f"<tr>{header_html}</tr>",
        "</thead>",
        "<tbody>",
        *body_rows,
        "</tbody>",
        "</table>",
        "</div>",
    ]
    return "\n".join(table_html), i


def parse_list(lines: list[str], start: int, ordered: bool) -> tuple[str, int]:
    tag = "ol" if ordered else "ul"
    pattern = re.compile(r"^\d+\.\s+") if ordered else re.compile(r"^-\s+")
    items: list[str] = []
    i = start

    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            break
        if not pattern.match(stripped):
            break
        item_text = pattern.sub("", stripped, count=1)
        items.append(f"<li>{parse_inlines(item_text)}</li>")
        i += 1

    return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>", i


def parse_blockquote(lines: list[str], start: int) -> tuple[str, int]:
    quote_lines: list[str] = []
    i = start
    while i < len(lines) and lines[i].lstrip().startswith(">"):
        quote_lines.append(lines[i].lstrip()[1:].strip())
        i += 1

    content = " ".join(part for part in quote_lines if part)
    return (
        '<aside class="callout"><div class="callout__content">'
        f"{parse_inlines(content)}</div></aside>",
        i,
    )


def parse_codeblock(lines: list[str], start: int) -> tuple[str, int]:
    first = lines[start].strip()
    lang = first[3:].strip()
    code_lines: list[str] = []
    i = start + 1
    while i < len(lines) and not lines[i].strip().startswith("```"):
        code_lines.append(lines[i])
        i += 1

    if i < len(lines):
        i += 1

    class_attr = f' class="language-{html.escape(lang)}"' if lang else ""
    escaped = html.escape("\n".join(code_lines))
    return f"<pre><code{class_attr}>{escaped}</code></pre>", i


def parse_paragraph(lines: list[str], start: int) -> tuple[str, int]:
    parts: list[str] = []
    i = start
    while i < len(lines):
        raw_line = lines[i]
        stripped = raw_line.strip()
        if not stripped:
            break
        if (
            stripped.startswith("#")
            or stripped == "---"
            or stripped.startswith("> ")
            or stripped.startswith("```")
            or stripped.startswith("|")
            or re.match(r"^\d+\.\s+", stripped)
            or re.match(r"^-\s+", stripped)
        ):
            break
        parts.append(parse_inlines(stripped))
        if raw_line.endswith("  "):
            parts.append("<br />")
        elif i + 1 < len(lines) and lines[i + 1].strip():
            parts.append(" ")
        i += 1

    return f"<p>{''.join(parts)}</p>", i


def keep_last_words_together(text: str, count: int = 2) -> str:
    words = text.split()
    if len(words) <= count:
        return "&nbsp;".join(html.escape(word) for word in words)

    head = html.escape(" ".join(words[:-count]))
    tail = "&nbsp;".join(html.escape(word) for word in words[-count:])
    return f"{head} {tail}"


def extract_section_number(text: str) -> str | None:
    match = re.match(r"^(\d+)\.\s+", text)
    if match:
        return match.group(1)
    return None


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    section_counter = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            output.append("<hr />")
            i += 1
            continue

        if stripped.startswith("```"):
            block, i = parse_codeblock(lines, i)
            output.append(block)
            continue

        if stripped.startswith("### "):
            text = stripped[4:].strip()
            output.append(f'<h3 id="{slugify(text)}">{parse_inlines(text)}</h3>')
            i += 1
            continue

        if stripped.startswith("## "):
            text = stripped[3:].strip()
            display_text = re.sub(r"^\d+\.\s+", "", text)
            badge = ""
            skip_labels = {"목차", "요약"}
            if display_text not in skip_labels:
                section_counter += 1
                badge = f'<span class="section-badge">{section_counter}</span>'
            output.append(f'<h2 id="{slugify(text)}">{badge}{parse_inlines(display_text)}</h2>')
            i += 1
            continue

        if stripped.startswith("# "):
            text = stripped[2:].strip()
            output.append(f'<h1 id="{slugify(text)}">{parse_inlines(text)}</h1>')
            i += 1
            continue

        if stripped.startswith("> "):
            block, i = parse_blockquote(lines, i)
            output.append(block)
            continue

        if stripped.startswith("|") and i + 1 < len(lines):
            separator = lines[i + 1].strip()
            if separator.startswith("|") and set(separator.replace("|", "").strip()) <= {"-", ":", " "}:
                block, i = parse_table(lines, i)
                output.append(block)
                continue

        if re.match(r"^\d+\.\s+", stripped):
            block, i = parse_list(lines, i, ordered=True)
            output.append(block)
            continue

        if re.match(r"^-\s+", stripped):
            block, i = parse_list(lines, i, ordered=False)
            output.append(block)
            continue

        block, i = parse_paragraph(lines, i)
        output.append(block)

    return "\n".join(output)


def extract_metadata(lines: list[str]) -> tuple[str, str, str, list[str]]:
    title = ""
    subtitle = ""
    source_url = ""
    remaining = list(lines)

    if remaining and remaining[0].startswith("# "):
        title = remaining.pop(0)[2:].strip()

    while remaining and not remaining[0].strip():
        remaining.pop(0)

    if remaining and remaining[0].lstrip().startswith(">"):
        subtitle = remaining.pop(0).lstrip()[1:].strip()

    while remaining and not remaining[0].strip():
        remaining.pop(0)

    if remaining and "원문 출처" in remaining[0]:
        match = re.search(r"\((https?://[^)]+)\)", remaining[0])
        if match:
            source_url = match.group(1)
        remaining.pop(0)

    while remaining and not remaining[0].strip():
        remaining.pop(0)

    while remaining and remaining[0].strip() == "---":
        remaining.pop(0)
        while remaining and not remaining[0].strip():
            remaining.pop(0)

    return title, subtitle, source_url, remaining


def render_page(markdown_text: str) -> str:
    title, subtitle, source_url, body_lines = extract_metadata(markdown_text.splitlines())
    body_markdown = "\n".join(body_lines)
    article_html = render_markdown(body_markdown)
    built_at = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M KST")
    safe_title = html.escape(title or "OpenAI Codex Best Practices")
    safe_subtitle = keep_last_words_together(subtitle)
    source_link = html.escape(source_url, quote=True)
    local_copy_link = html.escape(f"./{SOURCE.name}", quote=True)

    return f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{safe_title}</title>
    <meta
      name="description"
      content="OpenAI Codex Best Practices 한국어 문서를 읽기 편한 단일 페이지 형태로 제공하는 GitHub Pages 사이트입니다."
    />
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css"
    />
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap"
    />
    <link rel="stylesheet" href="./styles.css" />
    <script defer src="./script.js"></script>
  </head>
  <body>
    <header class="top-bar">
      <div class="top-bar__inner">
        <span class="top-bar__title">{safe_title}</span>
        <button
          class="theme-toggle"
          type="button"
          data-theme-toggle
          aria-pressed="false"
          aria-label="다크 모드로 전환"
          title="다크 모드로 전환"
        >
          <span class="theme-toggle__icon theme-toggle__icon--sun" aria-hidden="true">
            <svg viewBox="0 0 24 24" focusable="false">
              <path d="M12 3.75v2.5m0 11.5v2.5m8.25-8.25h-2.5m-11.5 0h-2.5m12.485 5.985-1.768-1.768M8.033 8.033 6.265 6.265m11.97 0-1.768 1.768M8.033 15.967l-1.768 1.768M15.5 12a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z" />
            </svg>
          </span>
          <span class="theme-toggle__icon theme-toggle__icon--moon" aria-hidden="true">
            <svg viewBox="0 0 24 24" focusable="false">
              <path d="M14.5 3.5a8.5 8.5 0 1 0 6 14.515A9 9 0 1 1 14.5 3.5Z" />
            </svg>
          </span>
        </button>
      </div>
      <div class="progress-bar" aria-hidden="true"></div>
    </header>

    <main class="main">
      <article class="article">
        <div class="hero">
          <span class="hero__badge">OpenAI Codex</span>
          <h1 class="hero__title">{safe_title}</h1>
          <p class="hero__subtitle">{safe_subtitle}</p>
          <p class="hero__meta">
            원문:
            <a href="{source_link}" target="_blank" rel="noreferrer">platform.openai.com</a>
            &nbsp;·&nbsp; 빌드: <time>{html.escape(built_at)}</time>
          </p>
        </div>
        <hr class="hero__divider" />
        <div class="prose">
          {article_html}
        </div>
      </article>
    </main>

    <footer class="footer">
      <div class="footer__inner">
        <a href="{source_link}" target="_blank" rel="noreferrer">원문 보기</a>
        <span class="footer__sep">·</span>
        <a href="{local_copy_link}">원고 (마크다운)</a>
        <span class="footer__sep">·</span>
        <time>빌드 {html.escape(built_at)}</time>
      </div>
    </footer>

    <button class="back-to-top" type="button" aria-label="맨 위로 이동" title="맨 위로 이동">
      <svg viewBox="0 0 24 24" focusable="false">
        <path d="M12 19V5m-7 7 7-7 7 7" />
      </svg>
    </button>
  </body>
</html>
"""


def main() -> None:
    markdown_text = SOURCE.read_text(encoding="utf-8")
    html_text = render_page(markdown_text)

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(html_text, encoding="utf-8")
    shutil.copy2(SOURCE, DIST / SOURCE.name)

    for asset_name in ASSET_FILES:
        shutil.copy2(ROOT / asset_name, DIST / asset_name)


if __name__ == "__main__":
    main()
