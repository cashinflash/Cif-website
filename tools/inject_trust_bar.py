#!/usr/bin/env python3
"""One-shot script: inject the site-wide trust bar above the footer
on every HTML page that has `<footer class="site-footer">`, and remove
the now-duplicate licensed-badge link from footer-bottom-left.

Idempotent: skips files that already contain `class="trust-bar"`.
Safe to re-run.

Run from repo root:  python3 tools/inject_trust_bar.py
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent

TRUST_BAR_BLOCK = """<section class="trust-bar" aria-label="Licenses and reviews">
  <div class="container">
    <ul class="trust-bar-list">
      <li><a href="/licenses/" aria-label="State licensed direct lender"><picture><source srcset="/images/licensed-badge.webp" type="image/webp"><img src="/images/licensed-badge.png" alt="State licensed direct lender" width="80" height="80" loading="lazy" decoding="async"></picture></a></li>
      <li><a href="https://www.google.com/search?q=Cash+in+Flash+reviews" target="_blank" rel="noopener" aria-label="Cash in Flash on Google Reviews"><img src="/images/google-reviews-logo.png" alt="Google Reviews" width="109" height="37" loading="lazy" decoding="async"></a></li>
      <li><a href="https://www.trustpilot.com/review/cashinflash.com" target="_blank" rel="noopener" aria-label="Cash in Flash on TrustPilot"><picture><source srcset="/images/trustpilot-logo.webp" type="image/webp"><img src="/images/trustpilot-logo.png" alt="TrustPilot" width="107" height="28" loading="lazy" decoding="async"></picture></a></li>
      <li><a href="https://www.yelp.com/biz/cash-in-flash" target="_blank" rel="noopener" aria-label="Cash in Flash on Yelp"><img src="/images/yelp-logo.png" alt="Yelp" width="90" height="40" loading="lazy" decoding="async"></a></li>
    </ul>
  </div>
</section>

"""

FOOTER_ANCHOR = '<footer class="site-footer">'

# Match the licensed-badge anchor inside footer-bottom-left, with optional
# surrounding whitespace/newline, so we can drop it cleanly.
FOOTER_BADGE_PATTERN = re.compile(
    r"\s*<a href=\"/licenses/\" class=\"footer-badge\">"
    r"<picture><source srcset=\"/images/licensed-badge\.webp\" type=\"image/webp\">"
    r"<img src=\"/images/licensed-badge\.png\" alt=\"State Licensed Direct Lender\""
    r" width=\"80\" height=\"80\" loading=\"lazy\" decoding=\"async\"></picture></a>"
)


def process_file(path: Path) -> str:
    """Return a status string: 'injected', 'skip-already', 'skip-no-footer', 'error:<msg>'."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return f"error:read:{e}"

    if FOOTER_ANCHOR not in text:
        return "skip-no-footer"
    if 'class="trust-bar"' in text:
        return "skip-already"

    # 1) Inject trust bar above the footer. Preserve the anchor's original
    #    leading whitespace so indentation matches what was there before.
    def replace_footer(m):
        # prefix is the whitespace immediately before the anchor on its line
        return m.group(1) + TRUST_BAR_BLOCK.rstrip("\n") + "\n\n" + m.group(1) + FOOTER_ANCHOR

    new_text, n = re.subn(
        r"([ \t]*)" + re.escape(FOOTER_ANCHOR),
        replace_footer,
        text,
        count=1,
    )
    if n != 1:
        return "error:anchor-not-matched"

    # 2) Remove licensed-badge from footer-bottom-left (duplicate; now in trust bar)
    new_text, _ = FOOTER_BADGE_PATTERN.subn("", new_text)

    if new_text == text:
        return "error:no-change"

    path.write_text(new_text, encoding="utf-8")
    return "injected"


def main():
    html_files = sorted(ROOT.rglob("*.html"))
    # Exclude anything under node_modules / originals / tools if present
    skip_dirs = {"node_modules", "originals", "tools"}
    html_files = [
        p for p in html_files
        if not any(part in skip_dirs for part in p.relative_to(ROOT).parts)
    ]

    counts = {"injected": 0, "skip-already": 0, "skip-no-footer": 0}
    errors = []

    for p in html_files:
        status = process_file(p)
        if status in counts:
            counts[status] += 1
        else:
            errors.append((p.relative_to(ROOT), status))

    print(f"injected:        {counts['injected']}")
    print(f"skip-already:    {counts['skip-already']}")
    print(f"skip-no-footer:  {counts['skip-no-footer']}")
    if errors:
        print(f"errors:          {len(errors)}")
        for rel, msg in errors:
            print(f"  {rel}: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
