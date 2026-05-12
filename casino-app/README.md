# CASINO_APP

A cross-platform (iOS + Android) **social casino** mobile app, slots-only at launch.
Players buy in-app coin packages with real money; coins have no cash value and
cannot be cashed out. This is **not** a real-money gambling product.

> **App name is a placeholder.** Every reference to the product name is the
> literal string `CASINO_APP` (uppercase, with underscore). When the real name
> is chosen, a single find-and-replace will rename the entire codebase.

---

## What's in this folder

This is the mobile app subproject. It lives inside the larger `Cif-website`
repository in its own directory so it doesn't interfere with the existing
website code.

```
casino-app/
├── README.md                  ← you are here
├── ARCHITECTURE.md            ← stack, folders, data model
├── ROADMAP.md                 ← phases 0-7 with checkboxes
├── APP_STORE_STRATEGY.md      ← Apple + Google review playbook
└── COIN_ECONOMY.md            ← coin math, RTP, bonus amounts, pricing
```

The actual app code (React Native project) will be scaffolded in **Phase 1**
inside this same folder. After Phase 1 it will look like:

```
casino-app/
├── (the 5 docs above)
├── app/                       ← React Native source
├── assets/                    ← images, sounds, fonts
├── ios/                       ← native iOS project (generated)
├── android/                   ← native Android project (generated)
├── package.json
└── app.json                   ← Expo config
```

---

## How to run it (placeholder — full instructions come in Phase 1)

Once Phase 1 is done, the workflow on your computer will be:

```bash
cd casino-app
npm install
npx expo run:ios       # to open in the iOS simulator
npx expo run:android   # to open in the Android emulator
```

You'll need either:
- **macOS with Xcode installed** to build for iOS, OR
- **Expo's cloud build (EAS Build)** to build iOS without a Mac (slower but works on any computer)

Android builds work from any operating system.

---

## Developer account setup — start this NOW (Phase 0 task for you)

These take real-world time to provision and **block** Phase 5 (in-app
purchases) and Phase 6 (submission). You should start both today, in
parallel with my work on Phase 1.

### Apple Developer Program ($99/year)

1. Go to https://developer.apple.com/programs/
2. Sign in with the Apple ID you want to use as the company account
   (recommend a **new** Apple ID dedicated to CASINO_APP, not your personal one)
3. Choose **enrollment type**:
   - **Individual** — fastest (24-48h), but the developer name shown in the
     App Store will be your personal name. OK for soft launch.
   - **Organization** — requires a **D-U-N-S number** (free, takes 1-5
     business days to obtain at https://dnb.com). The developer name will be
     your company name. Recommended for a real launch.
4. Pay the $99 enrollment fee
5. Wait for Apple's identity verification (24h for individual, up to 5
   business days for organization)
6. Once approved, log into https://appstoreconnect.apple.com and confirm
   you can see the dashboard
7. **Send me a screenshot** of your App Store Connect dashboard so I know
   you're ready for Phase 5

### Google Play Console ($25 one-time)

1. Go to https://play.google.com/console/signup
2. Sign in with the Google account you want to use
3. Choose **account type**:
   - **Personal** — fastest, fewer requirements
   - **Organization** — requires business verification (D-U-N-S or registration docs)
4. Pay the $25 one-time fee
5. Complete the identity verification (Google verifies via government ID — takes 1-2 days)
6. Complete the **Play Console developer verification** — Google now
   requires this for all new accounts before publishing
7. Set up a **merchant account** (Google Payments) for in-app purchases —
   this is a separate step inside Play Console
8. **Send me a screenshot** of your Play Console dashboard once it's ready

### Both accounts done? Tell me.

When both are provisioned, message me "dev accounts ready" and I'll know
Phase 5 isn't blocked.

---

## A note on what I (Claude) am good at vs. not good at

I'll be doing all of the coding, but I want to be honest about my limits up
front:

- **I'm good at:** writing the React Native app, the slot reel logic, the
  state management, the IAP plumbing, the compliance scaffolding, the
  paperwork templates.
- **I'm not good at:** generating real production-quality slot symbol art
  or composing original music. I'll use clearly labeled placeholder art
  (simple SVGs) and royalty-free sound clips. When you're ready for launch,
  you'll need to commission real art (likely a few thousand dollars on
  Fiverr/Upwork/specialist studio) and license real audio (or commission
  it). I'll flag exactly which files need to be replaced.

---

## Phase status

We are currently in **Phase 0 (planning)**. See `ROADMAP.md` for the full
plan and what's done.
