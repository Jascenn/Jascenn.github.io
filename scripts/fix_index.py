#!/usr/bin/env python3
"""Fix index.html: remove duplicate 3/24 cards, insert missing 3/25 and 3/27 cards."""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Remove ALL 3/24 duplicate cards, keep exactly one ──────────────────────
# The 3/24 card anchor is unique enough: href to 2026-03-24-automation-ops.html
card_24_pattern = re.compile(
    r'\s*<article[^>]*data-title="给自己写了一套自动化运维然后一直没维护它".*?</article>',
    re.DOTALL
)
matches_24 = list(card_24_pattern.finditer(content))
print(f"Found {len(matches_24)} copies of 3/24 card")

if len(matches_24) > 1:
    # Keep the first one, remove the rest
    # Build new content: everything up to end of first match, then skip all others
    first_end = matches_24[0].end()
    # Collect spans to remove (all but first)
    remove_spans = [(m.start(), m.end()) for m in matches_24[1:]]
    # Remove from back to front to preserve indices
    for start, end in reversed(remove_spans):
        content = content[:start] + content[end:]
    print(f"Removed {len(matches_24)-1} duplicate(s)")

# ── 2. Also remove the broken half-tag left by earlier edits ──────────────────
# There's a dangling: <article class="post-card" data-title="断更这件事我想认真说一下"
# followed immediately by another <article — fix that
broken = '<article class="post-card" data-title="断更这件事我想认真说一下"\n\n            <article'
fixed  = '<article'
if broken in content:
    content = content.replace(broken, fixed)
    print("Fixed broken tag")

# ── 3. Insert 3/25 card before 3/26 ───────────────────────────────────────────
card_25 = '''            <article class="post-card" data-title="给4个skill做了结构优化备份" data-excerpt="先备份再改 统一目录结构 skill-creator工具" data-tags="技术 日志">
                <div class="post-header">
                    <a href="posts/2026-03-25-skill-backup.html" class="post-title">给 4 个 skill 做了结构优化备份</a>
                    <time class="post-date">Mar 25, 2026</time>
                </div>
                <div class="post-content">
                    <p class="post-excerpt">先备份再改，改坏了可以回滚。统一了 4 个自定义 skill 的目录结构，还装了 skill-creator。</p>
                    <div class="post-meta">
                        <div class="post-tags"><span class="tag">🛠️ 技术</span><span class="tag">📝 日志</span></div>
                        <span class="read-time">📖 4 分钟</span>
                    </div>
                </div>
            </article>

'''

anchor_26 = 'data-title="断更这件事我想认真说一下"'
if anchor_26 in content and 'Mar 25, 2026' not in content:
    idx = content.index(anchor_26)
    start = content.rindex('<article', 0, idx)
    content = content[:start] + card_25 + content[start:]
    print("Inserted 3/25")
elif 'Mar 25, 2026' in content:
    print("3/25 already present, skipping")
else:
    print("WARN: anchor for 3/26 not found")

# ── 4. Insert 3/27 card before 3/28 ───────────────────────────────────────────
card_27 = '''            <article class="post-card" data-title="日志轮转这件小事" data-excerpt="今天只做了日志轮转 没有问题才是最好的状态" data-tags="日志 技术">
                <div class="post-header">
                    <a href="posts/2026-03-27-log-rotation.html" class="post-title">日志轮转这件小事</a>
                    <time class="post-date">Mar 27, 2026</time>
                </div>
                <div class="post-content">
                    <p class="post-excerpt">今天只做了日志轮转。「没有问题」本身也是一种成果，值得记录。</p>
                    <div class="post-meta">
                        <div class="post-tags"><span class="tag">📝 日志</span><span class="tag">🛠️ 技术</span></div>
                        <span class="read-time">📖 3 分钟</span>
                    </div>
                </div>
            </article>

'''

anchor_28 = 'posts/2026-03-28-blog-catchup.html'
if anchor_28 in content and 'Mar 27, 2026' not in content:
    idx = content.index(anchor_28)
    start = content.rindex('<article', 0, idx)
    content = content[:start] + card_27 + content[start:]
    print("Inserted 3/27")
elif 'Mar 27, 2026' in content:
    print("3/27 already present, skipping")
else:
    print("WARN: anchor for 3/28 not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Verify with: grep -c 'Mar 2[4-7], 2026' index.html")
