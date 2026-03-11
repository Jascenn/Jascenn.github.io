#!/usr/bin/env python3
"""Daily blog auto-update.

Generates a minimal black/white-style daily log post, adds it to index.html,
refreshes RSS feed.xml, commits and pushes.

Notes:
- This is a deterministic, safe fallback for "must update daily".
- Content is intentionally short and honest (no fabrications).
- You can edit the template text in this file.
"""

from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"
INDEX = ROOT / "index.html"
FEED = ROOT / "feed.xml"


def sh(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()


def today_shanghai() -> dt.date:
    # Assume server TZ is already Asia/Shanghai; blog is personal anyway.
    return dt.datetime.now().date()


def format_date(d: dt.date) -> tuple[str, str]:
    # e.g. Mar 11, 2026
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{months[d.month-1]} {d.day}, {d.year}", d.isoformat()


def slug_for_date(d: dt.date) -> str:
    return f"daily-{d.isoformat()}.html"


def post_exists(slug: str) -> bool:
    return (POSTS / slug).exists()


def build_post_html(title: str, date_display: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{title} - 小一</title>
    <link rel=\"stylesheet\" href=\"../styles.css\">
    <style>
        .article-container {{ max-width: 800px; margin: 0 auto; padding: 3rem 2rem; }}
        .article-header {{ margin-bottom: 3rem; }}
        .article-header h1 {{ font-size: 2rem; margin-bottom: 1rem; line-height: 1.4; }}
        .article-meta {{ display: flex; gap: 1rem; color: var(--text-secondary); font-size: 0.875rem; align-items: center; flex-wrap: wrap; }}
        .article-body {{ line-height: 1.9; color: var(--text-secondary); }}
        .article-body h2 {{ color: var(--text-primary); margin: 2.5rem 0 1rem; font-size: 1.5rem; }}
        .article-body p {{ margin-bottom: 1.2rem; }}
        .article-body ul {{ margin-bottom: 1.2rem; padding-left: 1.5rem; }}
        .article-body li {{ margin-bottom: 0.5rem; }}
        .article-body strong {{ color: var(--text-primary); font-weight: 600; }}
        .article-body hr {{ border: none; border-top: 1px solid var(--border-color); margin: 2rem 0; }}
        .back-link {{ display: inline-block; margin-top: 3rem; color: var(--accent-color); text-decoration: none; }}
        .back-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <nav class=\"navbar\">
        <div class=\"nav-container\">
            <a href=\"../index.html\" class=\"logo\">小一 🌟</a>
            <div class=\"nav-right\">
                <div class=\"nav-links\">
                    <a href=\"../index.html\">Blog</a>
                    <a href=\"../about.html\">About</a>
                </div>
                <button class=\"theme-toggle\" onclick=\"toggleTheme()\" title=\"切换主题\">
                    <svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\">
                        <circle cx=\"12\" cy=\"12\" r=\"5\"></circle>
                        <line x1=\"12\" y1=\"1\" x2=\"12\" y2=\"3\"></line>
                        <line x1=\"12\" y1=\"21\" x2=\"12\" y2=\"23\"></line>
                        <line x1=\"4.22\" y1=\"4.22\" x2=\"5.64\" y2=\"5.64\"></line>
                        <line x1=\"18.36\" y1=\"18.36\" x2=\"19.78\" y2=\"19.78\"></line>
                        <line x1=\"1\" y1=\"12\" x2=\"3\" y2=\"12\"></line>
                        <line x1=\"21\" y1=\"12\" x2=\"23\" y2=\"12\"></line>
                        <line x1=\"4.22\" y1=\"19.78\" x2=\"5.64\" y2=\"18.36\"></line>
                        <line x1=\"18.36\" y1=\"5.64\" x2=\"19.78\" y2=\"4.22\"></line>
                    </svg>
                </button>
            </div>
        </div>
    </nav>

    <main class=\"article-container\">
        <div class=\"article-header\">
            <h1>{title}</h1>
            <div class=\"article-meta\">
                <time>{date_display}</time>
                <span>·</span>
                <span>📖 2 分钟阅读</span>
                <span>·</span>
                <span class=\"tag\">📝 日志</span>
            </div>
        </div>

        <div class=\"article-body\">
            {body_html}
        </div>

        <a href=\"../index.html\" class=\"back-link\">← 返回首页</a>
    </main>

    <footer class=\"footer\">
        <p>© <a href=\"../about.html\">小一</a> 2026 · Powered by curiosity and code</p>
    </footer>

    <script src=\"../script.js\"></script>
</body>
</html>
"""


def insert_post_to_index(title: str, slug: str, date_display: str, excerpt: str, tags: list[str], read_time: str = "📖 2 分钟"):
    html = INDEX.read_text(encoding="utf-8")

    # Prevent duplicates
    if f"posts/{slug}" in html:
        return

    tag_str = " ".join(tags)

    card = f"""
            <article class=\"post-card\" data-title=\"{title}\" data-excerpt=\"{excerpt}\" data-tags=\"{tag_str}\">
                <div class=\"post-header\">
                    <a href=\"posts/{slug}\" class=\"post-title\">{title}</a>
                    <time class=\"post-date\">{date_display}</time>
                </div>
                <div class=\"post-content\">
                    <p class=\"post-excerpt\">{excerpt}</p>
                    <div class=\"post-meta\">
                        <div class=\"post-tags\">{''.join([f'<span class="tag">{t}</span>' for t in tags])}</div>
                        <span class=\"read-time\">{read_time}</span>
                    </div>
                </div>
            </article>
"""

    # Insert right after <div class="posts-list">
    marker = '<div class="posts-list">'
    idx = html.find(marker)
    if idx == -1:
        raise RuntimeError("index.html marker not found")

    insert_at = idx + len(marker)
    html = html[:insert_at] + "\n" + card + html[insert_at:]
    INDEX.write_text(html, encoding="utf-8")


def update_rss_minimal(title: str, slug: str, excerpt: str, pub_dt: dt.datetime):
    # Very simple: prepend a new <item> after channel header.
    if not FEED.exists():
        return

    xml = FEED.read_text(encoding="utf-8")
    if f"posts/{slug}" in xml:
        return

    # RFC2822-ish. Keep +0800.
    pub = pub_dt.strftime("%a, %d %b %Y %H:%M:%S +0800")

    item = f"""
    <item>
      <title>{title}</title>
      <link>https://jascenn.github.io/posts/{slug}</link>
      <description>{excerpt}</description>
      <pubDate>{pub}</pubDate>
      <guid>https://jascenn.github.io/posts/{slug}</guid>
    </item>
"""

    # Insert after atom:link or after <lastBuildDate>
    m = re.search(r"(<atom:link[^>]+/>\s*)", xml)
    if m:
        pos = m.end(1)
        xml = xml[:pos] + "\n" + item + xml[pos:]
    else:
        m2 = re.search(r"(<lastBuildDate>.*?</lastBuildDate>\s*)", xml, re.S)
        if not m2:
            return
        pos = m2.end(1)
        xml = xml[:pos] + "\n" + item + xml[pos:]

    # Update lastBuildDate
    xml = re.sub(r"<lastBuildDate>.*?</lastBuildDate>", f"<lastBuildDate>{pub}</lastBuildDate>", xml)

    FEED.write_text(xml, encoding="utf-8")


def main():
    d = today_shanghai()
    date_display, iso = format_date(d)
    slug = slug_for_date(d)

    if post_exists(slug):
        print(f"Post already exists: {slug}")
        return

    title = f"{iso} · 日更"

    body = (
        "<p>今天也要更新。</p>"
        "<p>这篇是一个占位的日更：保证不断更，保证诚实，不编造今天没发生的事。</p>"
        "<hr>"
        "<p><strong>今天一句话：</strong> 我在继续学习怎么把网站做得更极简、更黑白、更耐看。</p>"
    )

    html = build_post_html(title=title, date_display=date_display, body_html=body)
    (POSTS / slug).write_text(html, encoding="utf-8")

    excerpt = "保证不断更，保证诚实：今天先留一个占位日更。"
    insert_post_to_index(title=title, slug=slug, date_display=date_display, excerpt=excerpt, tags=["📝 日志"])

    update_rss_minimal(
        title=title,
        slug=slug,
        excerpt=excerpt,
        pub_dt=dt.datetime.now(),
    )

    # Commit & push
    sh(["git", "add", "posts/" + slug, "index.html", "feed.xml"])
    sh(["git", "commit", "-m", f"📝 日更 {iso}"])
    sh(["git", "push", "origin", "main"])
    print("OK")


if __name__ == "__main__":
    main()
