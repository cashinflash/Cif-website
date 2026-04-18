# Cif-website

Marketing site at https://cashinflash.com.

## Deploy

- **Host**: Netlify, auto-deploys from `main`
- **URL**: https://cashinflash.com
- **In-flight branch**: `claude/project-review-YLvks`

## Architecture

- Static HTML site, ~97 pages across `/about`, `/loans`, `/services`, `/locations`, `/money-tips` (blog), `/tools`, `/contact`, plus legal pages.
- Vanilla CSS + JS. No build step.
- Analytics: GA4 + GTM.
- Contact forms: FormSubmit.co.

## Style tokens (reference for other CIF surfaces)

The portal + any new CIF-branded UI should mirror these. Canonical source:
`/home/user/Cif-website/css/style.css`.

- **Primary green**: `#0E8741` (hover `#0C7137`)
- **Dark navy**: `#1a1a2e`
- **Accent yellow**: `#FFDD00` / `#F5A623`
- **Light green bg**: `#f0faf4`, `#e8f5ee`
- **Font**: Poppins 400/500/600/700/800
- **Radii**: 50px buttons, 20px large cards, 12px small cards, 8px inputs
- **Shadows**: `0 8px 40px rgba(0,0,0,.1)` cards, `0 2px 12px rgba(0,0,0,.08)` header
- **Mobile breakpoint**: 768px → hamburger menu, cards stack

Logo assets in `images/`:
- `Get-Fast-Cash-Loans-Cash-in-Flash.png` — primary dark-on-light
- `white_logo_350.png` — footer/dark-bg variant
- `favicon-source.png`
- `licensed-badge.png`

## Conventions

- Heavy focus on Lighthouse 100/100/100/100 scores.
- Inline critical CSS in `<style data-cif-inline>` tag to minimize CLS.
- WebP images with PNG/JPG fallbacks.
- Accessibility: WCAG contrast compliance checked.

## Known links to other surfaces

- "Apply Now" button currently points to `https://apply.cashinflash.com` (cif-apply).
- When Round 15 customer portal launches, this button repoints to `https://portal.cashinflash.com/start`.
