# Coin Economy

The math of CASINO_APP — how many coins a player starts with, how fast
they bleed, how fast they refill from free sources, and where the
purchase tiers sit. **Tuned for a generous / retention-first launch**
per Phase 0 decision.

> All numbers in this doc are starting values. They will be tuned in
> Phase 4-5 based on playtesting and (eventually) real telemetry. The
> goal of this doc is to make every number defensible and changeable
> from one place.

---

## Currencies

| Currency | What it's for | Earned via | Purchasable? |
| -------- | ------------- | ---------- | ------------ |
| **Coins** | Betting in slots | Spinning wins, daily/hourly bonuses, level-ups, quests, lucky wheel, purchase | **Yes** |
| **Gems** | Premium boosts (extra spins on lucky wheel, refill from empty, skip cooldowns) | Level-ups, milestone achievements, very rare drops | **No, not at launch** |

**Why gems aren't sold at launch:** Selling two currencies introduces
"loot box adjacent" complexity that some jurisdictions regulate. We
keep monetization to one simple currency (coins) and use gems as a
"premium feel" reward that money can't buy — counterintuitively this
makes the game feel less predatory. If we later add gem sales it will
be a deliberate Phase 7+ decision.

---

## Starting balance

| Setting | Value | Why |
| ------- | ----- | --- |
| Starting coins | **50,000** | Enough for ~250 spins at the default 200-coin bet — about an hour of casual play. Generous compared to industry norm of 10,000-25,000. |
| Starting gems | **5** | Lets the player try one premium-feel feature (e.g., skip a cooldown) to learn what gems do. |
| Starting level | **1** | XP starts at 0. |

A new player should be able to play for **at least 45 minutes** on
their first session without feeling pushed to buy. Day-1 retention
research from social casino studios suggests this is the strongest
single lever for long-term LTV.

---

## Bet sizes and RTP

### Default slot bet structure (per slot, configurable in `slots/<id>/config.ts`)

| Tier | Total bet (20 lines × per-line bet) |
| ---- | --- |
| Min  | **20 coins** (1/line) |
| Low  | 100 coins (5/line) |
| Mid  | 500 coins (25/line) |
| High | 2,000 coins (100/line) |
| Max  | **10,000 coins** (500/line) |

Default opening bet for a new player: **200 coins** (10/line). Bet
remembered per slot between sessions.

### RTP target

**96.0% per slot.** This is the high end of social casino norms
(typical range 88-95%), in line with the "generous" stance.

What 96% RTP means concretely: over a large number of spins, the slot
pays back 96 coins for every 100 wagered. The remaining 4 coins are
the "house edge" — except since coins have no cash value, the "house"
is just the rate at which the player's balance trends down. A higher
RTP means slower bleed, more time between purchases.

#### How RTP is enforced

Every slot has a `config.ts` that defines:
- The **reel strips** (sequences of symbols, e.g. 30-50 symbols per reel)
- The **paytable** (multipliers for 3/4/5-of-a-kind on each symbol)
- The **paylines** (20 fixed)
- **Bonus features** (free spins, multipliers, etc.)

The realized RTP of any configuration is fully determined by these
inputs. A test (`SpinEngine.test.ts`) runs **1,000,000 simulated spins**
and asserts the realized RTP is within ±0.5% of target. The build
fails CI if RTP drifts.

Volatility (variance of payouts) is a separate dial: at 96% RTP, a
"low volatility" slot pays small wins often, a "high volatility" slot
pays rarely but bigger. The launch slot (Phase 2) will be **medium
volatility** — most accessible feel for new players.

### What this means for run-rate (rough)

A player betting the default 200 coins/spin at 96% RTP loses about
8 coins per spin on average. Spins take ~3 seconds with auto-spin.

- 50,000 starting coins ÷ 8 coins/spin ≈ **6,250 spins of theoretical play**
- 6,250 spins × 3 seconds ≈ **5+ hours of pure spinning**

That ignores variance — in practice, a streak of bad luck could halve
that, a streak of good luck could double it. Daily bonuses extend it
further. **New player should comfortably reach Day 3 without buying.**
This is the design intent.

---

## Free coin sources

Free coins are the spine of retention. The math below targets a player
who logs in **twice per day for ~10 minutes** — they should be able to
sustain play indefinitely on free coins alone (slowly), and only
"need" to buy if they want to play more aggressively or for longer
sessions.

### Daily login bonus (escalating 7-day streak)

Reset to Day 1 if a calendar day is missed.

| Streak day | Coin reward |
| ---------- | ----------- |
| 1 | 5,000 |
| 2 | 7,500 |
| 3 | 12,500 |
| 4 | 20,000 |
| 5 | 35,000 |
| 6 | 60,000 |
| 7 | **100,000** (mega bonus + 5 gems) |
| 8+ | Loops back to Day 1, but with a +10% "veteran" boost |

A consistent daily player gets **240,000 coins/week** from this alone.

### Hourly vault (free coin pickup every 4 hours)

> Branding: "The Vault" — players see a vault that fills up over time
> and tap to collect.

- Cooldown: **4 hours**
- Reward: **5,000 coins** (scales with player level)
- Bonus: 1 gem on every 10th pickup
- Max stored: 1 pickup at a time (no banking — drives daily logins)

A 2x/day player gets ~10,000/day from this. A 4x/day player gets 20,000.

### Lucky wheel (free spin every 4 hours)

- Cooldown: **4 hours** (same timer as vault — they're separate UI to
  feel like more, which is honest because rewards differ)
- Wheel segments (with probabilities):
  - 2,500 coins — 35%
  - 5,000 coins — 25%
  - 10,000 coins — 15%
  - 25,000 coins — 10%
  - 50,000 coins — 8%
  - 100,000 coins — 5%
  - 1 gem — 1.5%
  - **JACKPOT (500,000 coins)** — 0.5%
- Expected value per spin: **~14,375 coins**

A 2x/day spinner gets ~28,750 coins/day.

### Daily quests (3 quests, refresh at midnight local time)

Examples:
- "Spin 100 times in any slot" → 5,000 coins
- "Win 50,000 coins in a single session" → 10,000 coins
- "Try a new slot" → 7,500 coins + 1 gem

Average quest completion (2 of 3 typical): **~15,000 coins/day**.

### Level-up rewards

Level curve: XP-to-next-level grows roughly geometrically. Sample levels:

| Level | XP needed (cumulative) | Reward on reaching |
| ----- | ---------------------- | ------------------ |
| 2  | 500    | 10,000 coins |
| 3  | 1,500  | 15,000 coins + 1 gem |
| 5  | 5,000  | 30,000 coins |
| 10 | 25,000 | 100,000 coins + 5 gems |
| 25 | 200,000 | 500,000 coins + 25 gems |
| 50 | 1,000,000 | 1,500,000 coins + 100 gems + cosmetic avatar |
| 100| 10,000,000 | 10,000,000 coins + bragging rights |

XP earned: 1 XP per spin baseline, +bonus XP scaled to win size.

### Total free-coin run-rate

A "typical" engaged casual player (2 logins/day, 15 min/session) earns
roughly:

- Daily bonus: ~35,000 (mid-streak average)
- Hourly vault (2x): ~10,000
- Lucky wheel (2x): ~28,750
- Daily quests: ~15,000
- Level XP (slow): ~2,000 amortized

**Total: ~90,000 coins/day from free sources.**

At 200 coin/spin average bet and 96% RTP, that funds ~11,250 spins/day
of theoretical play. A casual player spins maybe 500-1,500 times a day,
so **free coins more than sustain a casual player** — by design.

A player who wants to bet higher (1,000+ coins/spin) will outrun the
free supply and will be the conversion target for the coin store.

---

## Coin store — packages and pricing

Prices follow standard mobile IAP tiers (Apple/Google price points).

| Pack | Price (USD) | Coins | Bonus | Coins-per-$1 | Best for |
| ---- | ----------- | ----- | ----- | ------------ | -------- |
| **Starter** (one-time offer, first 24h) | $0.99 | 100,000 | +50,000 first-time | 151,515 | First purchase — best deal |
| **Handful** | $1.99 | 100,000 | — | 50,251 | Try-it tier |
| **Stack** | $4.99 | 300,000 | — | 60,120 | Casual top-up |
| **Pile** | $9.99 | 700,000 | +50,000 | 75,075 | Sweet spot — most purchases |
| **Heap** | $19.99 | 1,500,000 | +200,000 | 85,043 | "Smart buyer" tier |
| **Mountain** | $49.99 | 4,500,000 | +750,000 | 105,021 | Whale on-ramp |
| **Vault** | $99.99 | 10,000,000 | +2,500,000 | 125,012 | Whale tier |

### Why these tiers

- **Tier count of 6 + 1 starter** is standard. Fewer feels limited;
  more induces choice paralysis.
- **Value escalation** (coins-per-dollar grows with price) is the
  social casino norm and frames bigger purchases as the smart move.
- **The $9.99 "Pile" is the conversion target** — most purchases in
  social casino apps cluster here. Pricing it as the "sweet spot"
  visually (e.g., "MOST POPULAR" badge) is industry standard.
- **Starter is a one-time offer** shown after the player has played
  through their initial 50k. Highest-value pack, available for 24h
  from first lobby visit. This is the standard "first-purchase" hook
  and it should be marketed clearly (with a countdown), not hidden.

### Pricing across geos

At launch (US + Canada), Apple/Google will auto-convert USD to CAD.
No special pricing for Canada. When/if we expand to other geos, we
will set per-country prices because the default conversion is awful
in some markets (looks at you, India and Brazil).

### Refunds

- iOS: Apple handles refunds. We listen for the refund webhook (when
  we have a backend in Phase 7) and deduct coins. Until then, we accept
  that refunded purchases keep their coins — acceptable risk for soft
  launch.
- Android: Google handles refunds. Same posture.

---

## How a player should feel at different spend levels

This is the most important table in the doc.

### Spent $0 (free player)

- Can play indefinitely if they log in once or twice a day.
- Will occasionally see "buy coins" prompts when they bet aggressively
  and run dry.
- "Buy coins" prompts close easily (single tap). No paywalls. No
  rage moments.
- Should feel: **respected**. The game doesn't beg.

### Spent $5-20 (light spender, most common paying player)

- Buys 1-3 times in their first 30 days, typically the $4.99 or $9.99 packs.
- Has access to higher bets and longer play sessions.
- Should feel: **rewarded** — purchase felt like a treat, not a rescue.

### Spent $50-200 (regular spender)

- Buys monthly, usually $9.99-$19.99 packs.
- Plays daily, hits Level 25+.
- Should feel: **valued** — VIP perks (already considering: bigger
  daily bonus multipliers, exclusive avatars).

### Spent $500+ (whale, ~1% of players, ~50% of revenue)

- Buys Mountain or Vault packs regularly.
- High-bet player; needs the volume.
- Should feel: **important** — eventually we'll add a VIP tier
  (Phase 4 or later) with concierge bonuses.
- **What we will NEVER do:** harass whales with personalized "limited
  time" offers designed to exploit. We're a social casino, not a
  predator. We will offer a fair VIP rewards tier; we will not
  fabricate urgency.

### What "predatory" looks like — what we don't do

- **No "you're losing — buy now to get it back!" prompts.**
- **No fake countdown timers** on packages "exclusive to you."
- **No loot boxes** (random-content paid purchases).
- **No social pressure** designs ("Your friend just won! Buy coins
  to compete!"). When we add friends in Phase 7, gifting is one-way.
- **No "double or nothing" double-up after a win.** (Real-money
  slots sometimes do this. We don't.)
- **No paying to skip self-exclusion or spending limits.** Period.

---

## Where each of these numbers lives in code (after Phase 4)

| Number | File | Constant |
| ------ | ---- | -------- |
| Starting coins | `app/stores/walletStore.ts` | `STARTING_COINS` |
| Starting gems | `app/stores/walletStore.ts` | `STARTING_GEMS` |
| Daily bonus table | `app/features/daily-bonus/config.ts` | `DAILY_BONUS_TABLE` |
| Vault amount + cooldown | `app/features/hourly-vault/config.ts` | `VAULT_REWARD`, `VAULT_COOLDOWN_MS` |
| Lucky wheel segments | `app/features/lucky-wheel/config.ts` | `WHEEL_SEGMENTS` |
| Daily quest pool | `app/features/quests/config.ts` | `QUEST_POOL` |
| XP curve / level rewards | `app/features/level-up/config.ts` | `LEVEL_CURVE`, `LEVEL_REWARDS` |
| Per-slot bet tiers | `app/slots/<slot>/config.ts` | `BET_TIERS`, `DEFAULT_BET` |
| RTP target | `app/slots/<slot>/config.ts` | `RTP_TARGET` |
| Coin packages | `app/iap/products.ts` | `COIN_PACKAGES` |

**Everything in one constant per file.** No magic numbers in component
code. You can tune the entire economy without touching gameplay logic.

---

## Honest caveats

- **These numbers are starting points.** No social casino survives launch
  with its initial economy unchanged. Phase 6 ships with Firebase
  Analytics + Remote Config so we can A/B test bonus amounts and
  package pricing post-launch without app updates.
- **96% RTP is high for the industry.** Expect post-launch pressure to
  lower it for ARPDAU. I'd resist this until we have ~100k DAU and
  data to inform it. Generous-RTP slots get better reviews and word of
  mouth, which is what matters for a no-name brand.
- **I'm not a casino math expert.** The reel strip math (matching
  symbol weights to a target RTP for a given paytable) is well-trodden
  territory but specialized. The 1M-spin simulation test is our safety
  net. If we ever want to license a "real" RNG and math model from a
  studio supplier, that's a Phase 7+ decision (and adds licensing
  cost — typically $10k-50k upfront).
