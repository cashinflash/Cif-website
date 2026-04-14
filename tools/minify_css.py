#!/usr/bin/env python3
"""Minify css/style.css -> css/style.min.css

Conservative, safe regex-based minifier. Preserves semantics:
  - strips /* ... */ comments
  - collapses runs of whitespace to single space
  - removes whitespace adjacent to `{ } ; : , > + ~`
  - drops the final `;` before `}`
  - preserves strings inside `url(...)`, `content: "..."`, and `"..."` as-is

Run from repo root:  python3 tools/minify_css.py
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "css" / "style.css"
DST = ROOT / "css" / "style.min.css"


def minify(css: str) -> str:
    # 1) Protect strings (both single and double quoted) so internal whitespace is preserved.
    strings = []

    def stash_string(m):
        strings.append(m.group(0))
        return f"\x00S{len(strings)-1}\x00"

    # Capture both "..." and '...' (non-greedy, no backslash-escape handling needed for our CSS)
    css = re.sub(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', stash_string, css)

    # 2) Strip comments.
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)

    # 3) Collapse whitespace (any run of whitespace including newlines) to a single space.
    css = re.sub(r"\s+", " ", css)

    # 4) Remove whitespace adjacent to syntactic characters.
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    # Keep space around `(` inside selectors like :not( ) — CSS tolerates no-space so strip it.
    css = re.sub(r"\s*\(\s*", "(", css)
    css = re.sub(r"\s*\)\s*", ")", css)

    # 5) Drop `;` immediately before `}`.
    css = re.sub(r";}", "}", css)

    # 6) Trim leading/trailing whitespace.
    css = css.strip()

    # 7) Restore protected strings.
    def unstash(m):
        return strings[int(m.group(1))]

    css = re.sub(r"\x00S(\d+)\x00", unstash, css)

    return css


def main():
    if not SRC.exists():
        print(f"ERROR: {SRC} not found", file=sys.stderr)
        sys.exit(1)
    src = SRC.read_text(encoding="utf-8")
    mini = minify(src)
    DST.write_text(mini, encoding="utf-8")
    orig_kb = len(src.encode("utf-8")) / 1024
    mini_kb = len(mini.encode("utf-8")) / 1024
    pct = (1 - mini_kb / orig_kb) * 100
    print(f"{SRC.relative_to(ROOT)}  {orig_kb:.1f} KB")
    print(f"{DST.relative_to(ROOT)}  {mini_kb:.1f} KB  (-{pct:.1f}%)")


if __name__ == "__main__":
    main()
