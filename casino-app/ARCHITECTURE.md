# Architecture

This document describes **how** the app is built: the technology stack, why
each piece was chosen, the folder layout, and the shape of the data that
flows through it.

---

## Stack at a glance

| Layer                 | Choice                                                 |
| --------------------- | ------------------------------------------------------ |
| Framework             | **React Native** via **Expo (bare / prebuild)**        |
| Language              | **TypeScript**                                         |
| 2D rendering          | **@shopify/react-native-skia**                         |
| Animation             | **react-native-reanimated** v3                         |
| State management      | **Zustand**                                            |
| Local persistence     | **react-native-mmkv**                                  |
| Navigation            | **@react-navigation/native** (native stack + tabs)     |
| Audio                 | **expo-av**                                            |
| In-app purchases      | **react-native-iap** (StoreKit + Google Play Billing)  |
| Backend (Phase 7)     | **Firebase** (Auth, Firestore, Functions, Remote Config, Analytics, Crashlytics) |
| Crash reporting       | **Firebase Crashlytics** (Phase 6)                     |
| Analytics             | **Firebase Analytics** (Phase 6)                       |
| Build / submit        | **EAS Build** + **EAS Submit** (Expo's cloud service)  |

### Why this stack — short version

- **One codebase for iOS + Android.** A non-developer maintainer should
  not have to learn two ecosystems.
- **Skia + Reanimated** is the closest thing in React Native to a real
  2D game engine. It runs animations on the UI thread (not the JS
  thread), which is what we need for 60fps slot reels.
- **Expo** gives us a normal app shell, a fast dev loop, and cloud
  builds so you don't need a Mac to ship the iOS version.
- **Zustand + MMKV** is the simplest possible state + persistence
  combo. Each store is one file you can read top to bottom.
- **Firebase** is deferred to Phase 6/7 — until then the app is fully
  offline. This means we can build, polish, and even soft-launch a
  basic version without operating a backend.

### Why NOT each rejected alternative

- **Flutter** — also viable, but its IAP ecosystem on iOS is rougher,
  and Dart is a less common language if you ever hire a contractor to
  help maintain this. RN/TypeScript has a much larger labor market.
- **Unity** — overkill for 2D slots, adds significant build complexity,
  pain to integrate with normal mobile UI (lobby, store, settings),
  and the runtime fee fiasco of 2023 made many studios skittish about
  building new products on it.
- **Native iOS + native Android (two codebases)** — doubles every
  piece of work, including yours.
- **Web app in a WebView** — Apple is hostile to "thin wrapper"
  WebView casino apps. Almost certain rejection.
- **Redux** — too much boilerplate for a project this size.
- **AsyncStorage** instead of MMKV — 10-100x slower for the kinds of
  reads/writes a slot game does on every spin.

---

## Folder structure (after Phase 1 scaffold)

The goal: someone who has never opened this codebase should be able to
find any feature by reading the folder names. **No clever tricks.**

```
casino-app/
├── app/
│   ├── App.tsx                    ← root component, navigation container
│   │
│   ├── screens/                   ← one file per top-level screen
│   │   ├── SplashScreen.tsx
│   │   ├── AgeGateScreen.tsx
│   │   ├── LobbyScreen.tsx
│   │   ├── SlotGameScreen.tsx     ← hosts whichever slot is selected
│   │   ├── PaytableScreen.tsx
│   │   ├── CoinStoreScreen.tsx
│   │   ├── DailyBonusScreen.tsx
│   │   ├── ProfileScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   └── ResponsibleGamingScreen.tsx
│   │
│   ├── slots/                     ← one folder per slot game
│   │   ├── _shared/               ← reel engine, base components
│   │   │   ├── ReelStrip.tsx
│   │   │   ├── SpinEngine.ts      ← weighted RNG, RTP enforcement
│   │   │   ├── PaylineEvaluator.ts
│   │   │   ├── WinAnimations.tsx
│   │   │   └── SlotMachine.tsx    ← the template every slot uses
│   │   ├── velvet-vegas/          ← Phase 2 slot
│   │   │   ├── config.ts          ← symbols, paytable, RTP, theme
│   │   │   ├── symbols/           ← symbol art (SVG/PNG)
│   │   │   └── sounds/            ← spin, win, jackpot
│   │   ├── (more slots in Phase 3)
│   │
│   ├── components/                ← reusable UI (not slot-specific)
│   │   ├── CoinDisplay.tsx
│   │   ├── PrimaryButton.tsx
│   │   ├── MarqueeHeader.tsx
│   │   ├── Modal.tsx
│   │   └── ...
│   │
│   ├── stores/                    ← Zustand stores (state)
│   │   ├── walletStore.ts         ← coin balance, gems, last-bonus timestamps
│   │   ├── profileStore.ts        ← name, avatar, XP, level
│   │   ├── settingsStore.ts       ← sound on/off, music on/off, age confirmed
│   │   └── sessionStore.ts        ← in-memory only (current bet, last win, etc)
│   │
│   ├── features/                  ← non-slot game features
│   │   ├── daily-bonus/
│   │   ├── hourly-vault/
│   │   ├── lucky-wheel/
│   │   ├── quests/
│   │   └── level-up/
│   │
│   ├── compliance/                ← age gate, geofence, RG tools
│   │   ├── AgeGate.tsx
│   │   ├── geofence.ts            ← country + WA-state check
│   │   └── disclosures.ts         ← "no cash value" copy
│   │
│   ├── iap/                       ← in-app purchase plumbing (Phase 5)
│   │   ├── products.ts            ← SKU definitions
│   │   ├── purchaseFlow.ts
│   │   └── receiptValidator.ts
│   │
│   ├── theme/                     ← design system
│   │   ├── colors.ts              ← red/black/gold palette
│   │   ├── typography.ts
│   │   ├── spacing.ts
│   │   └── shadows.ts
│   │
│   ├── lib/                       ← framework-agnostic helpers
│   │   ├── rng.ts                 ← seeded RNG, used by spin engine
│   │   ├── storage.ts             ← MMKV wrapper
│   │   ├── format.ts              ← coin formatting (1,234,567 etc)
│   │   └── time.ts                ← bonus cooldown math
│   │
│   └── types/                     ← shared TypeScript types
│       ├── slot.ts
│       ├── player.ts
│       └── ...
│
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
│
├── ios/                           ← generated by Expo prebuild
├── android/                       ← generated by Expo prebuild
├── app.json                       ← Expo config (app name, icons, version)
├── eas.json                       ← EAS Build config (Phase 6)
├── package.json
└── tsconfig.json
```

### "Where is the file that controls X?" cheat sheet

| You want to change...           | Open this file                                |
| ------------------------------- | --------------------------------------------- |
| Starting coin balance           | `app/stores/walletStore.ts`                   |
| Daily bonus amount              | `app/features/daily-bonus/config.ts`          |
| RTP / payout odds of a slot     | `app/slots/<slot-name>/config.ts`             |
| Coin package prices             | `app/iap/products.ts`                         |
| Theme colors                    | `app/theme/colors.ts`                         |
| Which countries are blocked     | `app/compliance/geofence.ts`                  |
| Age gate copy                   | `app/compliance/AgeGate.tsx`                  |
| The app name (CASINO_APP)       | `app.json` + global find/replace              |

---

## Data model

All data is **local** on the device until Phase 7. Persisted state lives in
MMKV; in-memory-only state lives in Zustand without persistence.

### Persisted (survives app restart)

```ts
// walletStore.ts
type Wallet = {
  coins: number;              // soft currency, used to bet
  gems: number;               // premium currency, earned from level-ups
                              //   and bonus events (NOT purchasable at
                              //   launch — see COIN_ECONOMY.md)
  lifetimeCoinsWon: number;   // for "biggest win" display
  lastDailyBonusAt: number;   // unix ms
  dailyBonusStreak: number;   // 0-7 (resets if a day is missed)
  lastHourlyVaultAt: number;  // unix ms
  lastLuckyWheelAt: number;   // unix ms
};

// profileStore.ts
type Profile = {
  displayName: string;        // editable, no profanity filter at launch
  avatarId: string;           // one of ~12 preset avatars
  xp: number;
  level: number;              // derived from xp via level curve
  createdAt: number;
};

// settingsStore.ts
type Settings = {
  soundEnabled: boolean;
  musicEnabled: boolean;
  hapticsEnabled: boolean;
  ageConfirmed: boolean;      // set true after AgeGate passes
  ageConfirmedAt: number;
  responsibleGaming: {
    dailySpendLimitUSD: number | null;   // user-set, optional
    selfExcludedUntil: number | null;    // unix ms, blocks all play until then
  };
};

// per-slot stats (one entry per slot)
// stored under key `slotStats:<slotId>` in MMKV
type SlotStats = {
  totalSpins: number;
  totalWagered: number;
  totalWon: number;
  biggestWin: number;
  lastBet: number;            // remembers bet size between sessions
};
```

### In-memory only (resets on app close)

```ts
// sessionStore.ts
type Session = {
  currentSlotId: string | null;
  isSpinning: boolean;
  lastSpinResult: SpinResult | null;
  autoSpinRemaining: number;
};
```

### Slot game configuration (compiled into the app, not user-editable)

```ts
// app/slots/<slot-name>/config.ts
type SlotConfig = {
  id: string;                 // "velvet-vegas"
  displayName: string;        // "Velvet Vegas"
  theme: SlotTheme;           // colors, background, music
  reels: ReelStrip[];         // 5 weighted strips
  paylines: Payline[];        // 20 lines, defined as coordinate arrays
  paytable: Paytable;         // symbol -> payout multiplier per match count
  rtpTarget: number;          // 0.96
  bonusFeatures: BonusFeature[];
  minBet: number;
  maxBet: number;
  defaultBet: number;
};
```

The **RTP target** is enforced by tuning the weighted reel strips. The
spin engine ships with a test script (`SpinEngine.test.ts`) that runs
1,000,000 simulated spins and asserts the realized RTP is within 0.5% of
the target. If a tweak to symbol weights drops RTP below 95.5% or above
96.5%, the test fails. This is what keeps the math honest.

---

## How a spin works (end-to-end)

This is the most important code path in the entire app. Read it once and
you'll understand how the rest is shaped.

```
1. Player taps SPIN
   ↓
2. SlotGameScreen calls walletStore.deduct(currentBet)
   ↓ (if balance insufficient, show "buy coins" modal and stop)
3. SpinEngine.spin(slotConfig, rng) computes:
     - stop position on each of the 5 reels (using weighted RNG)
     - resulting symbol grid (5x3)
     - payline wins (using PaylineEvaluator)
     - total payout in coins
   ↓
4. The result is handed to the reel renderer (Skia + Reanimated):
     - reels start spinning immediately
     - reel 1 lands first, reel 5 lands last (with slight anticipation
       pause if reels 1-4 set up a possible big win)
     - landing physics: small bounce overshoot, then settle
   ↓
5. After all reels land, WinAnimations evaluates the result:
     - line wins flash one at a time
     - any "big win" / "mega win" thresholds trigger fullscreen celebration
     - coins are credited via walletStore.add(payout)
   ↓
6. sessionStore records lastSpinResult; SlotStats are updated in MMKV
   ↓
7. If autoSpinRemaining > 0, queue the next spin
```

The spin is **fully decided before the reels start moving.** The
animation is theater — the math is over by the time the reels start.
This is how real slot machines work, and it's what makes "anticipation"
animations possible (the engine knows reel 5 is going to land on a
jackpot symbol, so it can slow down reel 5's deceleration).

---

## How we keep things honest

- **RTP test** (mentioned above): 1M-spin simulation in CI catches any
  accidental change to expected payout.
- **No "near miss" cheating.** Real-money slot machines are regulated to
  prevent fake near-misses (where a reel is biased toward stopping just
  above/below a jackpot symbol). We mirror that standard even though
  we're not regulated — it's the right thing to do.
- **No predatory pacing.** Bet sizes scale linearly; we don't bury the
  player in "double or nothing" loops. The Cashman model is the ceiling
  of what we'll do.
- **Server-authoritative balances (Phase 7).** Until Phase 7, coin
  balance is on the device, which means a determined cheater could
  modify it. That's fine — they're only cheating themselves out of
  buying coins. When we add the backend, balances move server-side.

---

## What's deliberately NOT in the architecture

To keep this maintainable for a non-developer owner, I'm avoiding:

- **A monorepo with packages/.** Single project, single package.json.
- **Code generation / GraphQL clients.** Plain `fetch` is fine.
- **Microservices.** Even when we add a backend, it's one Firebase project.
- **Custom CI scripts.** EAS Build + GitHub Actions defaults.
- **A custom build system.** Expo's defaults all the way.

If we ever genuinely need any of these, we'll add them then. Not now.
