#!/usr/bin/env python3
"""Daily reminder for writing blog post (NO auto-writing).

Policy: content must be written by XiaoYi (manually). This script only:
- checks whether today's post file exists (any posts/*YYYY-MM-DD*.html)
- if missing, creates a local draft prompt file in drafts/YYYY-MM-DD.txt
- optionally triggers a macOS notification (best-effort)

Safe: does NOT commit/push, does NOT generate the actual post.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"
DRAFTS = ROOT / "drafts"


def today() -> str:
    return dt.datetime.now().date().isoformat()


def has_post_for(date_str: str) -> bool:
    # Accept either a dedicated daily slug, or any post that mentions the date in filename.
    # You can tighten this later.
    return any(p.name.find(date_str) != -1 for p in POSTS.glob("*.html"))


def notify(title: str, message: str) -> None:
    # Best-effort macOS notification. If not available, ignore.
    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                f'display notification "{message}" with title "{title}"',
            ],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def main() -> None:
    date_str = today()

    if has_post_for(date_str):
        return

    DRAFTS.mkdir(parents=True, exist_ok=True)
    draft = DRAFTS / f"{date_str}.txt"

    if not draft.exists():
        draft.write_text(
            "\n".join(
                [
                    f"【小一博客·日更提醒】{date_str}",
                    "", 
                    "要求：这篇必须是我自己写的真实内容（不准用占位水文）。",
                    "", 
                    "快速提纲：", 
                    "1) 今天我做了什么（3-5条，尽量具体）", 
                    "2) 一个踩坑 / 一个小发现", 
                    "3) 明天要做什么（1-3条）", 
                    "4) 一句结尾", 
                    "", 
                    "素材入口：", 
                    f"- memory/{date_str}.md（如果有）", 
                    "- 飞书/Telegram 今日对话", 
                ]
            ),
            encoding="utf-8",
        )

    notify("小一：博客日更提醒", f"今天还没发博客：{date_str}。已在 drafts/ 生成提纲。")


if __name__ == "__main__":
    main()
