#!/usr/bin/env python3
"""Konvertiert veroeffentlichte Twine-2-HTML-Dateien nach Twee 3."""

import argparse
import html
import json
import re
import sys
from pathlib import Path

STORYDATA_RE = re.compile(r"<tw-storydata\b([^>]*)>(.*?)</tw-storydata>", re.DOTALL)
PASSAGE_RE = re.compile(r"<tw-passagedata\b([^>]*)>(.*?)</tw-passagedata>", re.DOTALL)
TAG_RE = re.compile(r"<tw-tag\b([^>]*)>", re.DOTALL)
STYLE_RE = re.compile(r"<style\b[^>]*type=\"text/twine-css\"[^>]*>(.*?)</style>", re.DOTALL)
SCRIPT_RE = re.compile(
    r"<script\b[^>]*type=\"text/twine-javascript\"[^>]*>(.*?)</script>", re.DOTALL
)
ATTR_RE = re.compile(r"([\w-]+)=\"([^\"]*)\"")


def parse_attrs(raw: str) -> dict[str, str]:
    attrs = {k: html.unescape(v) for k, v in ATTR_RE.findall(raw)}
    # Twee 3 trimmt Passagennamen; ohne Angleichung zeigt "start" sonst ins Leere.
    if "name" in attrs:
        attrs["name"] = attrs["name"].strip()
    return attrs


def escape_name(name: str) -> str:
    # Twee 3 reserviert diese Zeichen im Passagen-Header fuer Tags und Metadaten.
    return re.sub(r"([\\\[\]{}])", r"\\\1", name)


def escape_body(text: str) -> str:
    # Zeilen mit "::" am Anfang wuerden sonst als neuer Passagen-Header gelesen.
    return re.sub(r"^::", r"\\::", text, flags=re.MULTILINE)


def convert(source: str) -> str:
    match = STORYDATA_RE.search(source)
    if not match:
        raise ValueError("kein <tw-storydata> gefunden")
    story = parse_attrs(match.group(1))
    inner = match.group(2)

    passages = [
        (parse_attrs(a), html.unescape(b)) for a, b in PASSAGE_RE.findall(inner)
    ]
    start_name = next(
        (p["name"] for p, _ in passages if p.get("pid") == story.get("startnode")),
        None,
    )

    data: dict[str, object] = {"ifid": story.get("ifid", "")}
    for key in ("format", "format-version"):
        if story.get(key):
            data[key] = story[key]
    if start_name:
        data["start"] = start_name
    tag_colors = {
        t["name"]: t["color"]
        for t in map(parse_attrs, TAG_RE.findall(inner))
        if "name" in t and "color" in t
    }
    if tag_colors:
        data["tag-colors"] = tag_colors
    try:
        data["zoom"] = float(story.get("zoom", "1"))
    except ValueError:
        pass

    out = [
        ":: StoryTitle",
        story.get("name", "").strip(),
        "",
        ":: StoryData",
        json.dumps(data, indent=2, ensure_ascii=False),
        "",
    ]

    style = STYLE_RE.search(inner)
    if style and style.group(1).strip():
        out += [
            ":: StoryStylesheet [stylesheet]",
            html.unescape(style.group(1)).strip(),
            "",
        ]
    script = SCRIPT_RE.search(inner)
    if script and script.group(1).strip():
        out += [":: StoryScript [script]", html.unescape(script.group(1)).strip(), ""]

    for attrs, text in passages:
        header = f":: {escape_name(attrs.get('name', ''))}"
        tags = attrs.get("tags", "").split()
        if tags:
            header += f" [{' '.join(tags)}]"
        meta = {k: attrs[k] for k in ("position", "size") if attrs.get(k)}
        if meta:
            header += " " + json.dumps(meta, ensure_ascii=False)
        out += [header, escape_body(text).rstrip(), "", ""]

    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_file", type=Path)
    parser.add_argument("twee_file", type=Path)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    result = convert(args.html_file.read_text(encoding="utf-8"))
    args.twee_file.parent.mkdir(parents=True, exist_ok=True)
    args.twee_file.write_text(result, encoding="utf-8")
    if not args.quiet:
        count = result.count("\n:: ") + 1
        print(f"{args.html_file} -> {args.twee_file} ({count} Header)")
        if args.verbose:
            print(result[:500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
