# Bedside Bay TikTok ads — playbook

This repo holds the media and the drawing kit for the TikTok account **bedside.bay** (game: Bedside Bay, https://bedsidebay.com, an emergency-medicine career game by Max). Posts are published by Buffer, which downloads each file from this repo's raw URL.

## Fixed facts
- Buffer organization id `6af52943363c789ae7ff8d6b` ("My organization"), TikTok channel id `6af529bb62b70b94b000c995` (bedside.bay). Buffer free plan: at most **10 scheduled posts** in the queue, 5 hashtags per TikTok post, about 1,000 API requests a month (keep calls lean).
- Three posts every day at **6:00am, 2:00pm and 10:00pm Australia/Sydney**. Create posts with `mode: customScheduled`, `schedulingType: automatic`, and `dueAt` in Sydney local time with the correct UTC offset (take it from Buffer `get_account` `currentTime`; never assume the offset).
- Raw URL format: `https://raw.githubusercontent.com/OZTEENRUBBISH/bedside-bay-videos/main/posts/<YYYY-MM-DD>/<file>`. Files must be pushed to `main` and return HTTP 200 before a post is created. Never rename or delete a file whose post is still queued.

## The three ad models
1. **Broke to Rich** — Dr John Smith's career climb from broke intern to wealthy ED Director (poor room, ER cases, surgery, mansion/supercar/gold watch). Kit: `python3 kit/video.py <out.mp4>` (video), `kit/carousel.py` (photo set), scenes in `kit/scenes.py`.
2. **Case** — one real patient from the game as a cliffhanger. Kit: `python3 kit/case.py <case-id> <out.mp4>`; patients are in `kit/cases.json` (real names, ages, presenting problems and quotes copied from the game's case library). **Never state or hint at the diagnosis** — the game hides it, and guessing risks medical errors.
3. **Full Game** — what the whole game is: 163 patients, Talk/Examine/Tests/Treat, five ranks (Intern, Resident, Registrar, Consultant, ED Director), four modes (Career, Quick shift, Case practice, First aid). Kit: `python3 kit/overview.py <out.mp4>`.

## Rules Max has set
- Fully illustrated and professional. **No screenshots or screen recordings.**
- The brand (logo pill or logo) is visible from the very first frame; the idea lands in the first two seconds; keep it engaging.
- The doctor is always **Dr John Smith**.
- Lean into career mode.
- **Every post must be different.** Never post a file that has been posted before. Each new ad needs a visibly new hook and content: a different patient for Case; a new angle, headline set, scene order, setting or music for Broke to Rich and Full Game (copy the model's script to a new file under `kit/variants/` and change it, or write new scenes with the helpers in `kit/lib.py`).
- **Mix formats and slots.** Each day one of the three posts is a photo set (4–6 slides, 1080x1920 JPG, built from the same scene functions at fixed times, as `kit/carousel.py` does); the other two are videos (1080x1920, 30 fps, 12–20 s, with a soundtrack from `kit/sound.py`). Rotate which model takes which slot: with d = days since 2026-11-13, slot order [6am, 2pm, 10pm] is [Case, Full Game, Broke to Rich] rotated left by d mod 3. Rotate which model is the photo set too.
- No Australian references, slang or triage scale wording beyond the game's own "Triage 1–5". Do not mention the App Store (release status unconfirmed); the call to action is "Play free" at bedsidebay.com.
- Only state facts about the game that are listed in this file. Bank amounts after the $2,000 start and the mansion/car/watch are illustrative; do not present them as exact game features in captions.
- Captions: one or two short sentences, "Play free at bedsidebay.com", then at most 5 hashtags.

## Sound
- Every video gets an engaging soundtrack from `kit/sound.py` `build(...)`: a music bed with drums and bass, sound effects on the cuts and pop-ins (whoosh, pop, ding, cash, riser, impact), and a short **AI voiceover** (Kokoro open model, voice `am_michael`; the model files download themselves from GitHub on first use, about 350 MB, and need `pip install kokoro-onnx soundfile scipy`).
- One short spoken line per scene, starting just after the cut, in plain punchy words that match the on-screen headline; end with "Bedside Bay. Play free." Check the report `build` returns: every line must finish before its scene ends and the last line before the video ends. Vary the music style (`upbeat`, `tense`, `bright`), cues and script between posts.
- Each model script has a `soundtrack(...)` function to copy and adapt.

## How a run works
1. `pip install --break-system-packages skia-python fonttools numpy pillow scipy kokoro-onnx soundfile` if missing; ffmpeg is required.
2. Read `posts.json` (the log of every post) and Buffer `list_posts` (status scheduled) to see which of the next slots are already filled.
3. Fill every empty slot for the **next 3 days** (never exceed 10 queued posts). For each: build the ad, draw preview frames and look at them (text overlap, cut-off, contrast) before the full render, check the result with ffprobe, save under `posts/<slot date>/`.
4. Commit, push to `main`, confirm each raw URL returns 200, then create the Buffer posts. Append each to `posts.json` (date, slot, model, format, file(s), hook, case id if any, Buffer post id).
5. **Weekly review (first run on or after each Monday, Sydney time):** `list_posts` with `includeMetrics: true` for the last 7 days of sent posts, record views per post in `posts.json`, write the ranking to `performance.md`, and for the following 7 days make one or two extra posts modelled on the best performers (same model and hook style, new content), replacing the weakest model's slots on those days.
6. Buffer `edit_post` re-validates the whole post: resend `assets`, `text` and `metadata` or it is rejected.
7. If Buffer tools are unavailable, a push fails, or a post errors, do not retry in a loop and do not delete or recreate posts: stop and report what happened and what is still queued.
