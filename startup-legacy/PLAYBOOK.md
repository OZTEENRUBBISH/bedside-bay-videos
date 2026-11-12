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

## The three ad models
1. **Broke to Rich**: the climb, from the broke room to garage startup, company, shares and the dream life. Age or day timeline hooks ("Day 1.", "Age 22:", "Instant noodles for dinner").
2. **Luxury Unlocks**: what the money buys. Watch, supercars, superyacht, private jet, wedding, mansion. POV and list hooks ("POV: 5 years ago you were broke", "What I bought when my startup took off").
3. **Full Game**: what the game really lets you do, told as the same rags-to-riches arc: 29 industries, setting prices and marketing spend, hiring staff, a share market that reacts to news, buying established businesses, film studios, phone companies, insurers and sports clubs, moral choices, a superyacht and private jet in the shop, a full life report at the end, four difficulty levels.

## Truth rules
- Only claim features listed under Full Game above. The game has **no marriage or spouse feature**: the wedding/wife scenes are lifestyle story only, so never say in a caption or headline that you can marry in the game.
- Net-worth figures on the career card are illustrative; do not present exact amounts as game facts in captions.
- Call to action is always "Free on the App Store" (the end card plus the caption). The app is iPhone only.

## How to make a post
- Kit: `kit/sl.py` (brand, founder character, partner, career card, scenes) and `kit/ad.py` (renders a JSON spec). Shared helpers and the sound engine come from `../kit/lib.py` and `../kit/sound.py`.
- Scenes available: `broke`, `garage`, `office`, `trading`, `mansion` (`car_in: false` for a parked car), `cars`, `watch`, `yacht`, `jet`, `wedding`, `cta`. New scenes go in `kit/sl.py` and are added to `SCENES`.
- Write a spec in `specs/<date>-<HHMM>-<name>.json` (copy an existing one). Fields: `model`, `format` (`video` or `photos`), `style` (`upbeat`, `tense` or `bright`; vary it), `scenes`, `caption`.
- `python3 kit/ad.py preview specs/X.json prev/X.jpg` and **look at it** (text inside the frame, nothing hidden by the card or headline) before rendering.
- Video: `python3 kit/ad.py video specs/X.json posts/<date>/<name>.mp4`. 1080x1920, 30 fps, 15 to 20 s, 5 to 6 scenes, ending on `cta`. It prints each voice line's timing and refuses to render if a line overruns its scene. Check the result with ffprobe and a frame sheet.
- Photo set: `python3 kit/ad.py photos specs/X.json posts/<date>/<name>` gives `slide-1.jpg` … (5 or 6 slides; the first gets a "Swipe >" chip; last is `cta`).
- Voice (Kokoro `am_michael`): one short punchy line per scene matching the headline; the end line is "Startup Legacy. Free on the App Store." (or a short question then "Startup Legacy."). Print `sound.phonemes(line)` for new lines and reword anything misread (e.g. "live" gets read as "alive": write "living").
- Caption: one or two short sentences + "Free on the App Store: Startup Legacy." + at most 5 hashtags (always end with `#simulationgame`).

## Variety (every post must be different)
- Never reuse a file. Every new ad needs a new hook and a different scene order, style or headline set from the last 6 posts on this account (check `posts.json`).
- Each day: two videos and one photo set.
- Slot rotation from 2026-11-16: with d = days since 2026-11-16, the slot order [6am, 2pm, 10pm] is [Broke to Rich, Full Game, Luxury Unlocks] rotated left by d mod 3. The photo set that day is the model at position (d mod 3) of [Luxury Unlocks, Broke to Rich, Full Game].

## Daily run (scheduled task)
1. `pip install --break-system-packages skia-python fonttools numpy pillow scipy kokoro-onnx soundfile` if missing; ffmpeg must exist.
2. Read `posts.json` and Buffer `list_posts` (channel `6af5369662b70b94b0016dc6`, status scheduled).
3. Fill every empty slot in the **next 3 days** (never more than 10 queued on this channel). Preview, render, check.
4. Commit and push to `main` (end commit messages with the attribution lines in the session's system prompt), confirm each raw URL returns 200, then create the Buffer posts. Append each to `posts.json` (date, slot, model, format, spec, files, hook, scenes, buffer_id) and push.
5. Weekly review, on the first run on or after each Monday (Sydney): `list_posts` with `includeMetrics: true` for the last 7 days of sent posts on this channel, record views in `posts.json`, write the ranking to `performance.md`, and over the next 7 days make one or two extra posts modelled on the best performers (same model and hook style, new content), replacing the weakest model's slots on those days.
6. Buffer `edit_post` re-validates the whole post: resend `assets`, `text` and `metadata`.
7. If Buffer is unavailable, a push fails or a post errors: do not loop, do not delete or recreate posts; stop and report what happened and what is still queued.
