#!/usr/bin/env python3
"""Erzeugt build/index.html mit Links auf alle gebauten Spiele."""

import argparse
import html
import re
from pathlib import Path
from urllib.parse import quote

ROOT_DIR = Path(__file__).resolve().parent.parent

PAGE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spiele: Praxisseminar WiSe 2026/27</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 40rem; margin: 3rem auto;
       padding: 0 1rem; line-height: 1.5; }}
li {{ margin: 0.5rem 0; }}
.format {{ color: #666; font-size: 0.9em; }}
</style>
</head>
<body>
<h1>Spiele</h1>
<p>Praxisseminar (Digitale) Spiele in der Sozialen Arbeit, WiSe 2026/27</p>
<ul>
{items}
</ul>
</body>
</html>
"""


def story_format(twee: Path) -> str:
    text = twee.read_text(encoding="utf-8")
    name = re.search(r'"format"\s*:\s*"([^"]+)"', text)
    version = re.search(r'"format-version"\s*:\s*"([^"]+)"', text)
    if not name:
        return ""
    return f"{name.group(1)} {version.group(1) if version else ''}".strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, default=ROOT_DIR / "src")
    parser.add_argument("--build", type=Path, default=ROOT_DIR / "build")
    args = parser.parse_args()

    items = []
    for game_dir in sorted(p for p in args.src.iterdir() if p.is_dir()):
        game = game_dir.name
        if not (args.build / game / f"{game}.html").exists():
            continue
        twees = sorted(game_dir.glob("*.twee"))
        fmt = story_format(twees[0]) if twees else ""
        href = f"{quote(game)}/{quote(game)}.html"
        items.append(
            f'<li><a href="{href}">{html.escape(game)}</a> '
            f'<span class="format">{html.escape(fmt)}</span></li>'
        )

    out = args.build / "index.html"
    out.write_text(PAGE.format(items="\n".join(items)), encoding="utf-8")
    print(f"OK {out} ({len(items)} Spiele)")


if __name__ == "__main__":
    main()
