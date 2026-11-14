# Startup Legacy TikTok ads: playbook

This folder holds the media and drawing kit for the TikTok account **startup.legacy**, which promotes Max's iPhone game **Startup Legacy: Business Career Simulator** (free on the App Store, https://apps.apple.com/app/startup-legacy/id6825573800). Buffer publishes the posts by downloading each file from this repo's raw URL. Everything here is separate from Bedside Bay: never post Startup Legacy media to bedside.bay or the other way round.

## Fixed facts
- Buffer organization `6af52943363c789ae7ff8d6b` ("My organization"). TikTok channel **startup.legacy** = `6af5369662b70b94b0016dc6`. (bedside.bay = `6af529bb62b70b94b000c995`; never touch its posts.)
- Buffer free plan: at most **10 scheduled posts per channel**, 5 hashtags per TikTok post, about 1,000 API requests a month across all of Max's automations (keep calls lean).
- Three posts every day at **6:00am, 2:00pm and 10:00pm Australia/Sydney**. Create posts with `mode: customScheduled`, `schedulingType: automatic`, `dueAt` in Sydney time with the UTC offset taken from Buffer `get_account` `currentTime` (never assume +11:00; it changes with daylight saving).
- Raw URL: `https://raw.githubusercontent.com/OZTEENRUBBISH/bedside-bay-videos/main/startup-legacy/posts/<YYYY-MM-DD>/<file>`. Push to `main` and confirm HTTP 200 before creating a post. Never rename or delete a file whose post is still queued.

## What Max asked for
- "Start broke, end up rich" stories, fully animated and illustrated, with luxury: mansions, supercars, gold watches, a superyacht, a private jet, and a wife (the wedding scene and the partner on the yacht).
- Professional look. Brand (the white "Startup Legacy" pill with the green suit icon) visible from the very first frame; the idea lands in the first two seconds; keep it engaging.
- No real brands, companies, car makes, watch makers or logos. Stock tickers are coined (see `TICKERS` in `kit/sl.py`). No App Store/Apple logo: the end card uses a generic download badge and the words "Free on the App Store".

## The six ad models
Style 1 is illustrated story scenes (`kit/sl.py`). Style 2, added at Max's request, goes into the money side: clean finance-app dashboards, job offers and running a sports club (`kit/sl2.py`). Keep both styles in every day's mix.

Style 1:
1. **Broke to Rich**: the climb, from the broke room to garage startup, company, shares and the dream life. Age or day timeline hooks ("Day 1.", "Age 22:", "Instant noodles for dinner").
2. **Luxury Unlocks**: what the money buys. Watch, supercars, superyacht, private jet, wedding, mansion. POV and list hooks ("POV: 5 years ago you were broke", "What I bought when my startup took off").
3. **Full Game**: what the game really lets you do, told as the same rags-to-riches arc: 29 industries, setting prices and marketing spend, hiring staff, a share market that reacts to news, buying established businesses, film studios, phone companies, insurers and sports clubs, moral choices, a superyacht and private jet in the shop, a full life report at the end, four difficulty levels.

Real game features you may claim (from the game code): price and monthly marketing spend per business; customer acquisition cost, lifetime value, LTV:CAC, payback and break-even in a unit-economics panel; wages with 12% super, rent, company tax; job offers including headhunters offering CEO roles once you have proven yourself, and roles that require a phone, laptop, car or private jet/jet charter; buying sports clubs (22 invented teams across football, cricket, rugby, basketball, ice hockey, baseball, esports) and setting the wage bill, ticket prices, coach level and star signings, with a league table, fans, ticket/sponsor/merch/TV income and league titles.

Style 2:
4. **The Numbers**: the financial side of running the business. Marketing spend vs customers and revenue (`marketing`), cost per customer, lifetime value, payback and LTV:CAC (`unit`), a monthly profit and loss with wages + super, rent, marketing and tax (`pnl`), and a price test showing demand falling as price rises (`pricing`). Hooks like "I spent $20k on marketing. Here's what came back."
5. **Job Offer**: offers arriving on a phone (`offer`, with `args` title / pay / who / tag_), the ladder of accepted offers from Junior Analyst to CEO (`ladder`), being headhunted as CEO, roles that need a suit, car or private jet.
6. **Club Owner**: buying and running a sports club. Match night at the stadium (`stadium`, `args` score / opp), wage bill, ticket price, coach and a star signing (`clubmoney`), revenue from tickets, sponsors, merch and TV plus the league table (`club`), lifting the title (`trophy`). Use the game's own invented clubs (e.g. Ashkettle Rovers, Brammerholt Bulldogs, Sandrevale Strikers, Corvenhall United); never real clubs or leagues.

## Truth rules
- Only claim features listed under Full Game above. The game has **no marriage or spouse feature**: the wedding/wife scenes are lifestyle story only, so never say in a caption or headline that you can marry in the game.
- Net-worth figures on the career card are illustrative; do not present exact amounts as game facts in captions.
- Call to action is always "Free on the App Store" (the end card plus the caption). The app is iPhone only.

## How to make a post
- Kit: `kit/sl.py` (brand, founder character, partner, career card, scenes) and `kit/ad.py` (renders a JSON spec). Shared helpers and the sound engine come from `../kit/lib.py` and `../kit/sound.py`.
- Style 2 scenes (`kit/sl2.py`): `marketing`, `unit`, `pnl`, `pricing`, `offer`, `ladder`, `stadium`, `clubmoney`, `club`, `trophy`. Pass scene options with `"args": {...}`.
- Style 1 scenes available: `broke`, `garage`, `office`, `trading`, `mansion` (`car_in: false` for a parked car), `cars`, `watch`, `yacht`, `jet`, `wedding`, `cta`. New scenes go in `kit/sl.py` and are added to `SCENES`.
- Write a spec in `specs/<date>-<HHMM>-<name>.json` (copy an existing one). Fields: `model`, `format` (`video` or `photos`), `style` (`upbeat`, `tense` or `bright`; vary it), `scenes`, `caption`.
- `python3 kit/ad.py preview specs/X.json prev/X.jpg` and **look at it** (text inside the frame, nothing hidden by the card or headline) before rendering.
- Video: `python3 kit/ad.py video specs/X.json posts/<date>/<name>.mp4`. 1080x1920, 30 fps, 15 to 20 s, 5 to 6 scenes, ending on `cta`. It prints each voice line's timing and refuses to render if a line overruns its scene. Check the result with ffprobe and a frame sheet.
- Photo set: `python3 kit/ad.py photos specs/X.json posts/<date>/<name>` gives `slide-1.jpg` … (5 or 6 slides; the first gets a "Swipe >" chip; last is `cta`).
- Voice (Kokoro `am_michael`): one short punchy line per scene matching the headline; the end line is "Startup Legacy. Free on the App Store." (or a short question then "Startup Legacy."). Print `sound.phonemes(line)` for new lines and reword anything misread (e.g. "live" gets read as "alive": write "living").
- Caption: one or two short sentences + "Free on the App Store: Startup Legacy." + at most 5 hashtags (always end with `#simulationgame`).

## Variety (every post must be different)
- Never reuse a file. Every new ad needs a new hook and a different scene order, style or headline set from the last 6 posts on this account (check `posts.json`).
- Each day: two videos and one photo set.
- Slot rotation from 2026-11-16: list M = [Broke to Rich, The Numbers, Luxury Unlocks, Job Offer, Full Game, Club Owner]. With d = days since 2026-11-16, the 6am, 2pm and 10pm slots take M[(3d) mod 6], M[(3d+1) mod 6], M[(3d+2) mod 6], so every day mixes both styles and each model comes round every two days. The photo set that day is the slot at position (d mod 3) (6am, 2pm or 10pm).
- Spare files: `posts/2026-11-13/game-yourrules.mp4`, `posts/2026-11-14/game-ceo.mp4` and `posts/2026-11-15/btr-noodles.mp4` were (`posts/2026-11-15/game-photos/` was used on 17 Nov 14:00) made but swapped out for style-2 posts before publishing. They have never been posted, so a run may use them once (log them in posts.json when used).

## Daily run (scheduled task)
1. `pip install --break-system-packages skia-python fonttools numpy pillow scipy kokoro-onnx soundfile` if missing; ffmpeg must exist.
2. Read `posts.json` and Buffer `list_posts` (channel `6af5369662b70b94b0016dc6`, status scheduled).
2b. **Daily performance check (Max's rule: keep mixing styles, but when a video does well, make another one like it).** Every run, call `list_posts` once with `status: ["sent"]`, `includeMetrics: true`, the channel above and `dueAt` covering the last 7 days. Record each post's views (and likes, comments, shares if given) in `posts.json`. A post is a **winner** when it has been live at least 24 hours and its views are at least 2x the median of this account's posts from the last 7 days (with fewer than 4 posts live, use the best one only if it has at least 500 views). For each new winner not yet followed up (`followed_up` not set in its posts.json entry), make **one** follow-up post in the next 3 days: same model, same style and hook pattern, the same kind of opening scene, but new headlines, numbers and scene details (never the same file or the same words). Put it in the slot that would have gone to the weakest-performing model, keep at least one style-1 and one style-2 post every day, at most one follow-up per day, and never two posts of the same model back to back. Set `followed_up` on the winner and `follow_up_of` (the winner's buffer_id) on the new post. List winners and their follow-ups in the run report.
3. Fill every empty slot in the **next 3 days** (never more than 10 queued on this channel). Preview, render, check.
4. Commit and push to `main` (end commit messages with the attribution lines in the session's system prompt), confirm each raw URL returns 200, then create the Buffer posts. Append each to `posts.json` (date, slot, model, format, spec, files, hook, scenes, buffer_id) and push.
5. Weekly review, on the first run on or after each Monday (Sydney): `list_posts` with `includeMetrics: true` for the last 7 days of sent posts on this channel, record views in `posts.json`, write the ranking to `performance.md`, and over the next 7 days make one or two extra posts modelled on the best performers (same model and hook style, new content), replacing the weakest model's slots on those days.
6. Buffer `edit_post` re-validates the whole post: resend `assets`, `text` and `metadata`.
7. If Buffer is unavailable, a push fails or a post errors: do not loop, do not delete or recreate posts; stop and report what happened and what is still queued.
