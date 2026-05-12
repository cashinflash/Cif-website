# Roadmap

Phased build plan. **Each phase ends with a checkpoint** — I (Claude) will
stop, summarize, and wait for your "go" before starting the next phase.

Status legend:
- `[ ]` not started
- `[~]` in progress
- `[x]` complete

---

## Phase 0 — Planning artifacts (no code)

**Goal:** Documents that tell us what we're building, how, and what to
watch for. No code yet.

- [~] `README.md` — project overview, run instructions, dev account setup
- [~] `ARCHITECTURE.md` — stack rationale, folders, data model
- [~] `ROADMAP.md` — this file
- [~] `APP_STORE_STRATEGY.md` — Apple + Google review playbook
- [~] `COIN_ECONOMY.md` — coin math, RTP, bonuses, pricing
- [ ] **Checkpoint:** product owner reads all five, gives "go Phase 1"

**Decisions locked in Phase 0:**
- Target geos: US + Canada, excluding Washington State
- Monetization stance: generous / retention-first (~96% RTP)
- Stack: React Native + Expo + Skia + Reanimated + Zustand + MMKV
- IAP: react-native-iap
- Backend: deferred to Phase 7; Firebase when needed

**Decisions deferred:**
- Actual product name (using `CASINO_APP` placeholder)
- First slot game theme (I'll propose in Phase 2)
- Art & sound vendor (commissioned after Phase 2 proof-of-feel)

---

## Phase 1 — Project scaffold + design system

**Goal:** Get the app shell on your phone. No real gameplay yet — just
the look and feel.

- [ ] Initialize Expo (bare workflow) + TypeScript project in `casino-app/`
- [ ] Configure `app.json` with `CASINO_APP` placeholder name, bundle ID
- [ ] Install core deps (Skia, Reanimated, Zustand, MMKV, Navigation)
- [ ] Set up `app/theme/` (colors, typography, spacing, shadows)
- [ ] Build core reusable components:
  - [ ] `PrimaryButton` (gold gradient on red, art-deco corners)
  - [ ] `CoinDisplay` (animated coin counter)
  - [ ] `MarqueeHeader` (Vegas marquee bulb effect)
  - [ ] `Modal` (red velvet, gold trim)
- [ ] Splash screen (gold logo on red curtain, brief fade)
- [ ] Static lobby mockup (3 fake slot tiles, coin balance up top, bottom tabs)
- [ ] App icon placeholder (Vegas-glam SVG)
- [ ] Test on iOS simulator AND Android emulator
- [ ] **Checkpoint:** product owner runs the app and approves the vibe

---

## Phase 2 — One complete, polished slot game

**Goal:** Build ONE slot machine end-to-end. This is the template every
other slot will copy. **Most important phase of the project.**

- [ ] `app/slots/_shared/` reel engine:
  - [ ] `SpinEngine.ts` — weighted RNG, RTP-tuned reel strips
  - [ ] `PaylineEvaluator.ts` — left-to-right line evaluation
  - [ ] 1M-spin RTP simulation test, asserts target ±0.5%
- [ ] `app/slots/_shared/SlotMachine.tsx` — Skia-rendered reels with:
  - [ ] Smooth spin (CSS-equivalent ease-in-out, ~2.5s total)
  - [ ] Staggered reel stops (reel 1 first, reel 5 last)
  - [ ] Anticipation pause when 4 scatters land (reel 5 slows dramatically)
  - [ ] Reel-stop bounce / overshoot physics
- [ ] First slot (theme: I'll propose — likely **"Velvet Vegas"**):
  - [ ] 5 reels × 3 rows × 20 paylines
  - [ ] ~10 symbols (3 low-pay card ranks, 5 themed mid/high, wild, scatter)
  - [ ] Placeholder SVG art (clearly labeled `placeholder_*.svg`)
  - [ ] Royalty-free spin/win/jackpot sound clips
- [ ] Paytable screen
- [ ] Bet adjuster (±, min, max)
- [ ] Auto-spin (10 / 25 / 50 / 100 spin options, stop on big win)
- [ ] Win animations:
  - [ ] Line win highlight
  - [ ] Big win threshold (10×+ bet) — fullscreen counter
  - [ ] Mega win threshold (50×+ bet) — fullscreen + particles
- [ ] Local coin balance persisted in MMKV
- [ ] **Checkpoint:** product owner plays the slot and approves feel

---

## Phase 3 — Lobby + second and third slot games

**Goal:** Prove the template scales. Players can switch between slots
with a persistent balance.

- [ ] Real lobby screen (replaces Phase 1 mockup):
  - [ ] Scrollable grid of slot tiles
  - [ ] Tile shows: thumbnail, name, "play" button, unlock requirement (if any)
  - [ ] "Featured" carousel at top
- [ ] Second slot (different theme, different bonus feature)
- [ ] Third slot (different theme, different bonus feature — e.g., free spins)
- [ ] Coin balance persists across game switches
- [ ] Per-slot stats (last bet, biggest win) persisted
- [ ] **Checkpoint:** product owner approves variety + lobby flow

---

## Phase 4 — Player progression and engagement loop

**Goal:** Reasons to come back tomorrow.

- [ ] Player level / XP system
  - [ ] XP earned per spin (small) + bonus XP for big wins
  - [ ] Level-up celebration with coin/gem reward
  - [ ] Level curve from `COIN_ECONOMY.md`
- [ ] Daily login bonus (7-day escalating streak)
- [ ] Hourly free coins ("vault" mechanic with cooldown timer)
- [ ] Daily quests / challenges (3 per day, e.g. "spin 100 times in Velvet Vegas")
- [ ] Lucky wheel (free spin every 4 hours)
- [ ] Local profile screen (avatar picker, editable name, level, stats)
- [ ] Push notification setup
  - [ ] Permission prompt (deferred — only ask after user accepts a daily bonus)
  - [ ] Daily reminder at user's typical play time
- [ ] **Checkpoint:** product owner reviews retention mechanics

---

## Phase 5 — Coin store + in-app purchases

**Goal:** Money in.

> **Blocker:** requires Apple Developer + Play Console accounts to be
> provisioned (see `README.md`). Cannot start Phase 5 until done.

- [ ] Coin store screen with packages from `COIN_ECONOMY.md`:
  - [ ] Small ($1.99 / $4.99)
  - [ ] Medium ($9.99)
  - [ ] Large ($19.99)
  - [ ] Mega ($49.99)
  - [ ] Best-value ($99.99)
- [ ] "No cash value" disclosure visible on the store screen
- [ ] react-native-iap integration
  - [ ] Product fetching from App Store / Play Store
  - [ ] Purchase flow with loading + error states
  - [ ] Receipt validation (client-side at launch; server-side in Phase 7)
  - [ ] Restore purchases button
- [ ] Sandbox testing instructions for product owner (StoreKit Configuration
      file for iOS, test track for Android)
- [ ] First-purchase bonus offer (one-time, marketed in onboarding)
- [ ] **Checkpoint:** product owner test-buys with sandbox account

---

## Phase 6 — Compliance + App Store readiness

**Goal:** Submit to both stores and pass review.

- [ ] Age gate on first launch (18+ confirmation; permanent until app reinstall)
- [ ] Geofence logic
  - [ ] Country detection (StoreKit storefront on iOS, locale + IP on Android)
  - [ ] Block list: WA state + countries from `APP_STORE_STRATEGY.md`
  - [ ] Friendly "not available in your region" screen
- [ ] Responsible gaming screen
  - [ ] Optional daily spend limit (user-set)
  - [ ] Self-exclusion (24h / 7d / 30d / permanent)
  - [ ] Links to NCPG (1-800-GAMBLER) and equivalents
- [ ] Privacy policy + ToS templates (placeholder text for product owner to customize)
- [ ] Firebase Analytics integration (retention, day-N funnels, ARPDAU)
- [ ] Firebase Crashlytics integration
- [ ] App Store / Play Store listing copy templates
- [ ] App Store age rating questionnaire answers (drafted in `APP_STORE_STRATEGY.md`)
- [ ] Apple App Review Notes drafted (critical — explains we're not gambling)
- [ ] Screenshot generation (one per slot + lobby + store)
- [ ] EAS Build configured for both platforms
- [ ] Submission checklist walkthrough with product owner
- [ ] **Checkpoint:** product owner approves submission

---

## Phase 7 — Backend + accounts (OPTIONAL; only on explicit "go")

**Goal:** Server-authoritative coin balances, cross-device sync,
leaderboards, friend gifting. **Adds operating cost and complexity.**
Only proceed if the product is showing traction.

- [ ] Firebase project setup (Auth, Firestore, Functions, Crashlytics already wired)
- [ ] Anonymous auth at launch; optional Apple/Google sign-in
- [ ] Server-authoritative wallet (coin/gem ledger in Firestore)
- [ ] Spin result signing (server validates spin outcomes for high-stakes spins)
- [ ] Cross-device sync
- [ ] Leaderboard (weekly biggest win, weekly total spins)
- [ ] Friend code / gifting (send coins, 1/day)
- [ ] Server-side receipt validation (replaces client-side)
- [ ] **Checkpoint:** product owner approves migration plan

---

## Out of scope (will not build at launch)

- Real-money gambling. Not now, not ever, not on this codebase.
- Cash-out / sweepstakes mechanics.
- Tournament play.
- Social features (chat, clubs) — possible future phase.
- Table games (blackjack, poker, roulette).
- Bingo, keno.
- Live dealer.
- Cryptocurrency anything.
