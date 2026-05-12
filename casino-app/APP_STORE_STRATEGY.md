# App Store Strategy

An honest assessment of what Apple and Google will scrutinize for a
**social casino app from a first-time gaming publisher**, and what we
need to have in place to pass review on the first try.

> **Important caveat:** I'm not a lawyer. Nothing in this document is
> legal advice. Before submission you should have a lawyer experienced
> in gaming law review the privacy policy, ToS, and the "no cash value"
> disclosures. Budget ~$500-2,000 for a one-hour consultation + review.

---

## TL;DR: what gets a social casino rejected

Both stores will scrutinize four things, in order of how often they
cause rejections:

1. **"Is this disguised real-money gambling?"** They'll look for any
   way coins can be converted back to real money, traded between
   players, or used to win physical/cash prizes. If any of that exists,
   instant rejection.
2. **"Are children protected?"** Age rating must be 17+/18+, age gate
   must be on first launch, no targeting of children in any marketing
   asset (no cartoon mascots, no playgrounds, no toys, no children in
   screenshots).
3. **"Are the disclosures clear?"** "No cash value" must appear in the
   app, in the store listing, and ideally in the icon/title context.
4. **"Is the developer credible?"** First-time publishers get more
   scrutiny. Expect 1-2 review cycles even if everything is right.

Cashman Casino, Slotomania, House of Fun, and similar apps are all live
on both stores, so the path is well-trodden — but each of them has been
rejected at some point and had to argue back. Plan for one rejection
cycle.

---

## Apple App Store

### Relevant guidelines

| Guideline | What it says | What we do |
| --------- | ------------ | ---------- |
| **3.2.1(vii)** | "Social casino games... may be acceptable" if no real-money gambling. | We are clearly social casino, no cash-out. |
| **5.3** (Gaming, gambling, lotteries) | Real-money gambling needs licenses. Social casino is exempt **but** must make clear it's not gambling. | "No cash value" disclosures throughout. |
| **1.4.4** | Apps simulating cash gambling must indicate they are simulations. | Disclosure copy in onboarding + store. |
| **3.1.1** | In-app purchases must use Apple's IAP — no external payment. | We use StoreKit only. |
| **4.0** (Design) | Apps must look like they belong on iOS. | Native navigation, proper safe-area handling. |
| **5.1.1** (Privacy) | Privacy policy required, data collection disclosed. | App Privacy questionnaire + privacy policy. |

### App Privacy questionnaire (the nutrition label)

Apple will ask what data we collect. Our intended answers for launch
(Phase 6, no backend yet):

- **Crash data:** YES (Crashlytics) — linked to user, used for app
  functionality
- **Performance data:** YES (Crashlytics) — linked to user, used for app
  functionality
- **Product interaction:** YES (Firebase Analytics) — not linked to
  user, used for analytics
- **Purchase history:** YES (StoreKit) — linked to user, used for app
  functionality
- **User ID:** YES (Firebase install ID) — linked to user, used for
  analytics
- **Everything else:** NO

We do **not** collect: name, email, phone, address, photos, contacts,
location (beyond country for geofencing, which is derived not collected),
health, financial info, browsing history, search history, sensitive info.

### Age rating

Apple's age rating questionnaire — our answers:

- Frequent/intense simulated gambling: **YES** (forces 17+ rating)
- Frequent/intense cartoon or fantasy violence: NO
- Frequent/intense realistic violence: NO
- Frequent/intense sexual content or nudity: NO
- Frequent/intense profanity or crude humor: NO
- Frequent/intense alcohol, tobacco, drug use: NO
- Frequent/intense mature/suggestive themes: NO
- Frequent/intense horror/fear themes: NO
- Frequent/intense medical/treatment info: NO
- Unrestricted web access: NO
- Gambling and contests: NO (because no real money)

Result: **17+ rating.**

### App Review Notes (CRITICAL — write this carefully)

This is the message we send Apple's reviewers in App Store Connect. It's
free text and it's the single most important thing for a clean first
review. Draft:

> Hi App Review team,
>
> CASINO_APP is a free-to-play **social casino** app featuring
> slot-machine-style games. We want to flag a few things up front to
> make the review smoother:
>
> 1. **No real-money gambling.** Players cannot wager real money, win
>    real money, or convert in-app coins back to real money. All
>    in-app coins are entertainment-only and have no cash value. This
>    is stated on the coin store screen, in onboarding, and in the
>    Terms of Service.
> 2. **No prizes.** Players cannot win physical goods, cash, or any
>    item of monetary value. Winnings are in-app coins only, used to
>    play more games within the app.
> 3. **Age-gated 17+.** First launch shows an age confirmation screen
>    (18+ required). The app is rated 17+ in App Store Connect.
> 4. **No coins purchased outside Apple IAP.** All coin purchases use
>    StoreKit.
> 5. **Geographic restriction:** The app is available in the US and
>    Canada only, and within the US is unavailable in Washington State
>    due to local social-casino law.
> 6. **Responsible gaming tools** are accessible from the main menu:
>    optional spending limits, self-exclusion (24h/7d/30d/permanent),
>    and links to the National Council on Problem Gambling
>    (1-800-GAMBLER).
>
> Test account: not required (no login at launch). Coin balance is
> local to the device.
>
> If anything is unclear, please contact us at <support email>.
>
> Thanks!

### Apple-specific rejection reasons to avoid

- **Generic icon.** Icon must clearly show this is a slot/casino app,
  not just abstract gold-and-red art.
- **Screenshots without disclosures.** At least one screenshot should
  show "no cash value" wording.
- **Marketing copy with prize language.** Never write "win big!" without
  context. "Win virtual coins" or "win in-game coins" is fine.
- **TestFlight beta with real-money implication.** Even in beta
  description, no mention of cash prizes.
- **External links to anything cashable.** No referral programs, no
  "rate us for coins" that could be construed as paying for behavior.

### Apple-specific gotchas

- **Sign in with Apple** is required if we offer any other social login
  (Google/Facebook). At launch we have no login at all, so this doesn't
  apply yet. When we add login in Phase 7, we'll add SIWA alongside.
- **App Tracking Transparency (ATT) prompt** is required if we use any
  attribution / ad SDK. We don't ship ads at launch, so we skip this.
  If we add Facebook/AppLovin SDK later, we add the prompt.
- **StoreKit Configuration file** is the way to test IAP without
  uploading to App Store Connect — saves hours in Phase 5.

---

## Google Play Store

### Relevant policies

| Policy | What it says | What we do |
| ------ | ------------ | ---------- |
| **Real-Money Gambling, Games, and Contests** | Real-money gambling needs Play's gambling app approval. | We are not real-money; this doesn't apply. |
| **Gambling-related content** (general) | Apps with simulated gambling must be rated appropriately and follow ads policy. | We are 18+ on Google. |
| **In-app purchases** | Must use Google Play Billing. | We use react-native-iap with Play Billing. |
| **Data safety** | Disclose data collected, similar to Apple. | Data safety form filled out. |
| **Target audience** | Cannot target children. | We declare 18+ target audience. |
| **Loot boxes** | If we add randomized purchasable items, must disclose odds. | We do NOT sell loot boxes. Coin packs are fixed-value. |

### Google Play age rating (IARC)

Google uses the IARC questionnaire — same idea as Apple. Our answers
yield:

- **ESRB:** Adults Only (AO) for simulated gambling — wait, this is
  actually a gotcha. ESRB's stance: if there's simulated gambling with
  real-money purchases, it can hit AO. Google Play does NOT distribute
  AO-rated games. **However**, Google Play has its own override for
  social casino: as long as it's clearly entertainment-only and
  gated 18+, it's accepted as Mature 17+.
- **PEGI:** 18 (gambling)
- **USK:** 16 or 18 depending on jurisdiction
- **Effective Google rating:** **Mature 17+ / 18+**

When filling out the IARC questionnaire on Play Console:
- "Does the app contain simulated gambling?" — YES
- "Is there a real-money element?" — NO
- "Can items be purchased with real money?" — YES (coins)
- "Can items won be converted to real money or items of value?" — NO

### Google-specific rejection reasons to avoid

- **Pre-launch report failures.** Google runs an automated test on a
  bot device before publishing. Crashes during the bot test = rejection.
  We mitigate by testing on Android emulator early and fixing crashes
  pre-submission.
- **Permissions we don't use.** Don't request notification permission
  until we actually need it. Don't request location.
- **"Restricted content" misclassification.** On the content rating
  form, classify carefully — Google has caught apps that under-disclosed
  simulated gambling and rejected for "deceptive behavior."
- **Account holds.** Google has been aggressive lately about suspending
  new developer accounts for "policy violations" during the first 3
  months. Mitigation: complete Google Play **Pre-launch app testing**
  (closed testing with 12+ testers for 14 days) before promoting to
  production. This is now a Google requirement for new developer
  accounts anyway.

### Google Play closed testing requirement (NEW, important)

As of late 2024, Google requires new personal developer accounts to:
1. Run a **closed test** with at least 12 testers for at least 14 days
2. Demonstrate the app is stable

Plan accordingly: budget 3 weeks between "we're code-complete" and "we
can publish" on Google.

We'll handle the 12 testers via a Google Group (you invite friends/family
with their Google accounts; they install via a tester link). I'll write
the exact invitation copy in Phase 6.

---

## Privacy policy and ToS

We need both, live on a public URL, before submission.

### Privacy policy must cover

- What data we collect (see Apple App Privacy section)
- How we use it
- Who we share with (Firebase, Apple, Google — all subprocessors)
- How users can delete it (since we have no account at launch:
  uninstalling the app + Apple/Google's data deletion request flows)
- Children's privacy (we don't allow under-18; comply with COPPA
  by default since we have no children data)
- Contact email
- Last updated date

### ToS must cover

- "No cash value" / no gambling clauses
- Conduct policy (no cheating, no reverse engineering)
- Account termination conditions (Phase 7 only)
- Dispute resolution (binding arbitration clause — standard for US apps)
- Limitation of liability
- Governing law (Delaware or your state)
- Refunds: deferred to Apple/Google's policies (we don't process refunds
  directly because we don't handle payment)

**I'll write placeholder templates in Phase 6.** You'll need to:
1. Replace `[COMPANY_NAME]`, `[CONTACT_EMAIL]`, `[STATE]` with real values
2. Have a lawyer review (recommended)
3. Host both on a public URL (we'll add them to the cif-website domain
   under `/casino-app/privacy` and `/casino-app/terms`)

---

## Geofencing — countries and US states

### Launch: US + Canada, excluding Washington State

**Why exclude Washington State:** In 2018, the 9th Circuit ruled
(Kater v. Churchill Downs) that virtual coins purchasable for real money
in a casino-style app constitute "things of value" under Washington's
gambling statute. That ruling has led to class-action settlements
against Big Fish Casino, DoubleDown, Huuuge, and others totaling
hundreds of millions of dollars. Until/unless we have meaningful
revenue to justify the legal cost, **don't operate in WA**.

### Detection methods (Phase 6)

- **Country:** Apple's `SKStorefront` (iOS) / Play Install Referrer
  (Android) gives us reliable storefront country. Backup: device locale.
- **US state:** trickier without GPS. We will:
  1. On first launch in the US, show a state picker as part of the age
     gate ("Please select your state of residence")
  2. If user selects WA, show "not available in your state" and exit
  3. We do NOT use GPS at launch — that's a permission we want to avoid
- **VPN evasion:** we accept that determined users can lie about state.
  The legal protection of geofencing is what matters; we're not in the
  fraud-prevention business at launch.

### Other jurisdictions to monitor (NOT blocked at launch since US+CA only)

For reference if we expand later:
- **Australia (post-2024):** social casinos must hold a license
- **Belgium, Netherlands:** loot box laws can apply
- **South Korea:** social casino is restricted
- **Quebec (Canada):** historically tolerant but evolving — monitor

---

## Pre-submission checklist (Phase 6 gate)

Nothing gets submitted until every box is checked.

### Build / technical
- [ ] App tested on physical iPhone (latest iOS) and physical Android
      (Android 12+, ideally Pixel and a Samsung)
- [ ] No crashes during 30 minutes of gameplay on either device
- [ ] All placeholder art replaced OR clearly labeled and intentional
- [ ] App icon finalized (1024×1024 master)
- [ ] Splash screens for both platforms
- [ ] Sound on/off and music on/off both work
- [ ] App works in airplane mode (no crashes; just shows "offline"
      gracefully for any network-required features)
- [ ] App works at smallest supported device size (iPhone SE, ~4.7")
- [ ] Dark mode (we are dark-mode by design, so n/a)
- [ ] No console.log spam in production build
- [ ] Build size under 100MB (probably 30-50MB)

### Content
- [ ] All copy reviewed for "win", "prize", "cash", "real" wording
- [ ] "No cash value" appears on coin store, age gate, ToS, store
      listing description
- [ ] No mascot resembles a child or appeals to children
- [ ] No reference to alcohol, drugs, etc.
- [ ] Privacy policy URL live and accessible
- [ ] Terms of service URL live and accessible

### Store listing
- [ ] App name (TBD, no "Casino" alone — Apple sometimes flags;
      "CASINO_APP" or "CASINO_APP Slots" pattern is safe)
- [ ] Subtitle (~30 chars) — no "win cash" / "win real prizes"
- [ ] Description (4000 chars) — gameplay-focused, includes "no cash
      value" disclaimer
- [ ] Keywords (Apple, 100 chars) — "slots casino spin reels jackpot
      free coins social" etc., no "gambling money cash bet"
- [ ] Screenshots (5-10 per device size) — show gameplay, lobby, big
      win, store with disclaimer
- [ ] Preview video (optional but boosts conversion)
- [ ] Promotional text (170 chars Apple)
- [ ] Privacy policy URL
- [ ] Support URL
- [ ] Marketing URL (optional)

### Compliance
- [ ] Age gate works on first launch
- [ ] WA state block works
- [ ] Responsible gaming page accessible from main menu
- [ ] Self-exclusion actually blocks gameplay
- [ ] Spend limit actually enforces
- [ ] 1-800-GAMBLER link present
- [ ] Apple App Privacy questionnaire filled
- [ ] Google Data Safety form filled
- [ ] IARC questionnaire submitted
- [ ] App Review Notes written and reviewed
- [ ] Google Play closed test completed (12+ testers, 14+ days)

### IAP
- [ ] All coin packages defined in App Store Connect with the same
      product IDs as in code
- [ ] All coin packages defined in Play Console with the same product
      IDs as in code
- [ ] Sandbox-tested purchase succeeds, coins delivered
- [ ] Restore purchases works
- [ ] Refund flow tested (sandbox refund → coin balance handled)

### Legal
- [ ] Privacy policy reviewed by lawyer (recommended, not required)
- [ ] ToS reviewed by lawyer (recommended)
- [ ] Trademark search for chosen product name (definitely do this
      BEFORE filing — costs ~$200 with a search company)
- [ ] Business entity formed (LLC recommended for liability shield;
      ~$200-500 depending on state)

---

## Realistic timeline from "Phase 6 starts" to "live in store"

- **Apple:** 1-3 days for first review. Plan for one rejection cycle
  (typical for first-time gaming publishers). Resubmission review is
  usually 24h. Total: ~1 week.
- **Google:** 3-7 days for review of a new account's first app. Plus
  the mandatory 14-day closed test before promoting to production.
  Total: ~3 weeks.

So the longest pole is Google's closed test requirement. **Start the
closed test as soon as Phase 5 is done**, in parallel with Phase 6
work.

---

## What we expect to be hard

- **Getting the age gate to actually look good.** Most casino apps
  have an ugly age gate. We can do better.
- **First Apple review.** Even doing everything right, there's a 30-40%
  chance of a first-review rejection over disclosures wording.
- **Google account holds.** Random and frustrating; the closed test
  helps.
- **Producing 5-10 polished screenshots per device size.** Requires
  finished art in Phase 2-3.

## What we expect to be easy

- **IAP integration.** react-native-iap is mature; sandbox testing is
  straightforward once the accounts exist.
- **Crashlytics setup.** A few config files.
- **Geofencing US states.** Manual state picker is reliable and avoids
  GPS permissions.
