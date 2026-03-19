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
            section_num = extract_section_number(text)
            badge = ""
            if section_num:
                badge = f'<span class="section-badge">{section_num}</span>'
            output.append(f'<h2 id="{slugify(text)}">{badge}{parse_inlines(text)}</h2>')
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


def collect_sections(lines: list[str]) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("## "):
            continue

        label = stripped[3:].strip()
        if label == "목차":
            continue

        slug = slugify(label)
        nav_label = re.sub(r"^\d+\.\s*", "", label)
        sections.append((slug, nav_label))

    return sections


def build_section_nav(sections: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'<li><a href="#{slug}"><span>{html.escape(label)}</span></a></li>'
        for slug, label in sections
    )


def render_page(markdown_text: str) -> str:
    title, subtitle, source_url, body_lines = extract_metadata(markdown_text.splitlines())
    body_markdown = "\n".join(body_lines)
    article_html = render_markdown(body_markdown)
    sections = collect_sections(body_lines)
    nav_html = build_section_nav(sections)
    built_at = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M KST")
    safe_title = html.escape(title or "OpenAI Codex Best Practices")
    safe_subtitle = keep_last_words_together(subtitle)
    source_link = html.escape(source_url, quote=True)
    local_copy_link = html.escape(f"./{SOURCE.name}", quote=True)
    section_count = str(len(sections))
    feature_labels = [html.escape(label) for _, label in sections[:3]]
    feature_tags = "\n".join(
        f'<li class="hero-tag">{label}</li>' for label in feature_labels
    )

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
    <link rel="stylesheet" href="./styles.css" />
    <script defer src="./script.js"></script>
  </head>
  <body>
    <div class="progress-bar" aria-hidden="true"></div>
    <div class="page-backdrop" aria-hidden="true">
      <div class="page-backdrop__orb page-backdrop__orb--one"></div>
      <div class="page-backdrop__orb page-backdrop__orb--two"></div>
      <div class="page-backdrop__mesh"></div>
    </div>

    <div class="page-shell">
      <header class="hero">
        <div class="hero-panel">
          <div class="hero-bar">
            <div class="hero-brand">
              <span class="hero-brand__mark" aria-hidden="true">C</span>
              <div>
                <p class="eyebrow">OpenAI Developers · Codex</p>
                <p class="hero-kicker">Korean Edition</p>
              </div>
            </div>

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

          <div class="hero-grid">
            <div class="hero-copy">
              <p class="hero-label">Operational guide for high-signal Codex work</p>
              <h1>{safe_title}</h1>
              <p class="subtitle">{safe_subtitle}</p>
              <div class="hero-actions">
                <a class="button primary" href="{source_link}" target="_blank" rel="noreferrer">원문 보기</a>
                <a class="button secondary" href="{local_copy_link}">원고 보기</a>
              </div>
              <ul class="hero-tags">
                {feature_tags}
              </ul>
            </div>

            <aside class="hero-meta" aria-label="문서 개요">
              <p class="hero-meta__label">문서 개요</p>
              <dl class="hero-stats">
                <div>
                  <dt>Sections</dt>
                  <dd>{section_count}</dd>
                </div>
                <div>
                  <dt>Format</dt>
                  <dd>Single page</dd>
                </div>
                <div>
                  <dt>Theme</dt>
                  <dd>Adaptive</dd>
                </div>
              </dl>
              <p class="hero-note">
                프롬프트 설계부터 계획, 설정, 검증, MCP, 스킬, 자동화까지 한 번에 읽을 수 있도록 정리한 가이드입니다.
              </p>
              <p class="build-stamp">마지막 빌드: <time>{html.escape(built_at)}</time></p>
            </aside>
          </div>
        </div>
      </header>

      <main class="layout">
        <aside class="side-nav">
          <div class="side-nav__inner">
            <p class="side-nav__eyebrow">Navigator</p>
            <div class="side-nav__header">
              <p class="side-nav__title">빠른 이동</p>
              <span class="side-nav__count">{section_count}</span>
            </div>
            <p class="side-nav__description">긴 문서를 섹션 단위로 탐색할 수 있습니다.</p>
            <ol>
              {nav_html}
            </ol>
          </div>
        </aside>

        <article class="doc-card">
          <div class="doc-card__header">
            <p class="doc-card__eyebrow">Guide</p>
            <div>
              <h2 class="doc-card__title">문서 본문</h2>
              <p class="doc-card__description">정제된 읽기 레이아웃과 고정 내비게이션으로 긴 문서도 빠르게 따라갈 수 있게 구성했습니다.</p>
            </div>
          </div>
          <div class="doc-prose">
            {article_html}
          </div>
        </article>
      </main>

    </div>

    <button class="back-to-top" type="button" aria-label="맨 위로 이동" title="맨 위로 이동">
      <svg viewBox="0 0 24 24" focusable="false">
        <path d="M12 19V5m-7 7 7-7 7 7" />
      </svg>
    </button>

    <button class="mobile-nav-toggle" type="button" aria-label="목차 열기" title="목차 열기" aria-expanded="false">
      <svg viewBox="0 0 24 24" focusable="false">
        <path d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <div class="mobile-nav-overlay" aria-hidden="true">
      <div class="mobile-nav-drawer">
        <div class="mobile-nav-drawer__header">
          <div>
            <p class="side-nav__eyebrow">Navigator</p>
            <p class="side-nav__title">빠른 이동</p>
          </div>
          <button class="mobile-nav-close" type="button" aria-label="닫기">
            <svg viewBox="0 0 24 24" focusable="false">
              <path d="M18 6 6 18M6 6l12 12" />
            </svg>
          </button>
        </div>
        <p class="side-nav__description">문서 섹션 {section_count}개</p>
        <ol>
          {nav_html}
        </ol>
      </div>
    </div>
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
