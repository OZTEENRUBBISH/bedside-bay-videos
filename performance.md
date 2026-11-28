# bedside.bay performance

Last weekly review: **2026-11-23** (Monday, Sydney time). Next review: first run on or after Monday 2026-11-30.

## Planned extras from this review (read before choosing models for a day)

| Slot (Sydney) | Replaces | Extra to make | Status |
|---|---|---|---|
| Fri 27 Nov, 10:00pm | Full Game photos | Case photo set in the style of "Would you catch this?" (612 views: the patient's quote in a speech bubble on slide 1, then the chart with the diagnosis row locked), with a patient not used before. It is that day's photo set. 27 Nov then has Case at 2pm and 10pm: different patients and treatments. | Done 24 Nov: "What's wrong with Mark?" (Mark Ellis), `kit/variants/case_photos_06_whats_wrong.py` |
| Sun 29 Nov, 6:00am | Full Game video | Broke to Rich video in the style of "What Dr John Smith eats at every rank" (773 views: one everyday thing upgrading rank by rank, rank name as the headline), with a new object. 29 Nov then has Broke to Rich at 6am and 2pm: give the 2pm one a different treatment, such as a split-screen comparison like "Mattress or mansion?" (612 views). | Done 28 Nov: "Dr John Smith's phone at every rank", `kit/variants/b2r_18_phone.py`; the 2pm post is the split screen "Same 24 hours. Intern vs ED Director." |

All other slots follow the normal rotation in CLAUDE.md. Note: no run happened on 25–27 Nov, so the 28 Nov 6am and 2pm slots went unfilled; the 25 Nov 2pm post ("Done watching medical dramas?", Buffer id 6b026f69d5eabfb8cc808042) is in Buffer with status error and was left as it is. The run on 28 Nov filled 28 Nov 10pm to 1 Dec 10pm (10 posts, the queue limit). The posts already queued for 24 and 25 Nov were left as they are.

## Review of 16–22 Nov (metrics from Buffer, updated 2026-11-22 16:02 UTC)

21 posts, about 4,640 views in total (week one: about 1,820 across 11 posts). The two newest posts (22 Nov 2pm and 10pm) had under a day of data and are listed but left out of the averages. The 23 Nov posts had no data yet.

| Rank | Views | Likes | Avg watch | Posted (Sydney) | Model | Format | Hook |
|---|---|---|---|---|---|---|---|
| 1 | 773 | 11 | 6.8 s | 21 Nov 6am | Broke to Rich | video | What Dr John Smith eats at every rank. |
| 2 | 612 | 14 | 6.0 s | 19 Nov 2pm | Broke to Rich | video | Same doctor. Mattress or mansion? (split screen; last review's extra) |
| 2 | 612 | 1 | 5.7 s | 17 Nov 10pm | Case | photos | Would you catch this? (Clive Dunn: quote bubble, then locked chart) |
| 4 | 229 | 5 | 4.6 s | 19 Nov 6am | Case | video | Incoming. (Jack Thompson, emergency doors) |
| 5 | 227 | 3 | 4.8 s | 16 Nov 10pm | Broke to Rich | photos | One doctor. Five ranks. (staircase) |
| 6 | 226 | 0 | 3.9 s | 17 Nov 6am | Full Game | video | Think you could run an ER? (the job in numbers) |
| 7 | 225 | 9 | 6.5 s | 16 Nov 2pm | Full Game | video | 4 ways to play doctor. |
| 8 | 212 | 5 | 9.8 s | 16 Nov 6am | Case | video | Quote first, then A-D quiz (Chloe Marsh) |
| 9 | 189 | 0 | 5.8 s | 19 Nov 10pm | Broke to Rich | photos | Broke intern starter pack vs ED Director starter pack |
| 10 | 168 | 2 | 3.0 s | 22 Nov 6am | Case | video | Triage 1. Drop everything. (Victor Petrov). About 21 h of data |
| 11 | 156 | 0 | 2.5 s | 20 Nov 10pm | Case | photos | New wristband. New patient. (Paul Morgan) |
| 12 | 141 | 2 | 3.4 s | 18 Nov 2pm | Case | video | You're being paged. (Nicole Barnes) |
| 13 | 133 | 2 | 2.9 s | 21 Nov 2pm | Case | video | Who's behind curtain 3? (Tom Silva) |
| 14 | 127 | 0 | 3.3 s | 18 Nov 10pm | Full Game | photos | Now hiring: Emergency doctor. |
| 15 | 112 | 1 | 4.3 s | 17 Nov 2pm | Broke to Rich | video | Watch this number. (bank balance) |
| 16 | 100 | 1 | 1.8 s | 20 Nov 6am | Full Game | video | 163 patients. All of them talking. |
| 17 | 94 | 0 | 4.5 s | 21 Nov 10pm | Full Game | photos | The bill for running your own ER. |
| 18 | 92 | 1 | 3.2 s | 22 Nov 2pm | Case | video | Your next patient (Sean Murphy; last review's extra). About 13 h of data |
| 19 | 87 | 2 | 3.2 s | 20 Nov 2pm | Broke to Rich | video | Mom keeps texting Dr John Smith. |
| 20 | 84 | 3 | 3.7 s | 18 Nov 6am | Broke to Rich | video | 4 promotions from broke. |
| 21 | 43 | 0 | 3.1 s | 22 Nov 10pm | Broke to Rich | photos | How Dr John Smith gets to work. Every rank. About 5 h of data |

### By model (19 posts with about a day of data or more)

| Model | Posts | Mean views | Median | Notes |
|---|---|---|---|---|
| Broke to Rich | 7 | 298 | 189 | Two of the three breakout posts, and the most likes. Also three posts under 115, so it is the least even. |
| Case | 7 | 236 | 168 | One breakout (the photo set); the videos sit between 133 and 229. |
| Full Game | 5 | 154 | 127 | No post above 226. The two plain "numbers" videos did best; the document-style photo sets (job ad, bill) and the quote wall were the three weakest mature Full Game posts. |

### What this says, and how sure it is

- Three posts reached 600 to 770 views, about three times anything else. That is the first sign of a post breaking out of the 100 to 240 band, but it is three posts, so treat the pattern as a lead, not a rule.
- The clearest lead: Broke to Rich hooks built on one everyday thing ("what he eats at every rank", "mattress or mansion?") beat the abstract ones (bank balance, promotion stamps, text thread). The split-screen extra planned at the last review was one of the three.
- For Case, the patient's quote on the first frame or slide ("Would you catch this?", the Chloe Marsh quote video, last week's Megan Lewis set) has done better than opening on a prop (wristband, pager, curtain). The second "Your next patient" extra did not repeat week one's result, on 13 hours of data.
- Slot and format made little difference this week: mean views were 256 at 6am, 218 at 2pm and 234 at 10pm; videos 239, photo sets 234.
- Weakest model: Full Game, for the second week. It gives up two slots to the extras above. Its remaining posts should stay with short number-led videos rather than document-style photo sets.

## Review of 12–16 Nov (metrics from Buffer, updated 2026-11-15 22:55 UTC)

The account's first week. Buffer refreshes TikTok metrics about once a day, so the three newest posts had only a few hours of data and the 16 Nov 2pm post had none; they are listed but not used in the model averages.

| Rank | Views | Likes | Avg watch | Posted (Sydney) | Model | Format | Hook |
|---|---|---|---|---|---|---|---|
| 1 | 242 | 5 | 5.9 s | 14 Nov 6am | Full Game | video | 163 patients. One doctor. |
| 2 | 236 | 10 | 7.0 s | 15 Nov 6am | Broke to Rich | video | Same doctor. Two futures. (split screen) |
| 3 | 233 | 5 | 3.3 s | 13 Nov 6am | Case | video | Your next patient (Graham Peters) |
| 4 | 222 | 2 | 5.7 s | 14 Nov 10pm | Case | photos | "Why does it smell of burning in here?" (Megan Lewis) |
| 5 | 221 | 4 | 10.1 s | 13 Nov 10pm | Broke to Rich | photos | Broke intern to ED Director |
| 6 | 197 | 1 | 4.2 s | 15 Nov 2pm | Case | video | Your next patient (Priya Sharma), about 20 h of data |
| 7 | 169 | 2 | 3.3 s | 14 Nov 2pm | Broke to Rich | video | How did he afford this? (rewind) |
| 8 | 134 | 6 | 3.2 s | 13 Nov 2pm | Full Game | video | Run your own emergency room. |
| 9 | 89 | 0 | 2.5 s | 15 Nov 10pm | Full Game | photos | New here? The whole game in 4 swipes. About 12 h of data |
| 10 | 41 | 1 | 4.3 s | 16 Nov 6am | Case | video | Quote first, then A-D quiz (Chloe Marsh). About 4 h of data |
| 11 | 38 | 5 | 3.9 s | 12 Nov 10pm | Broke to Rich | video | Day 1. Broke intern. (first post on a new account) |
| – | no data yet | – | – | 16 Nov 2pm | Full Game | video | 4 ways to play doctor. |

Total: about 1,820 views across 11 posts with data.

### By model (posts with at least a day of data)

| Model | Posts | Mean views | Notes |
|---|---|---|---|
| Case | 2 | 228 | 217 if Priya (20 h) is included. The most consistent model: every Case post with a day of data is above 190. |
| Broke to Rich | 4 | 166 | 209 without the very first post, which went out to an account with no history. Holds the best likes (10) and the longest watch time (10.1 s on the photo set). |
| Full Game | 2 | 188 | Has the single best post and the weakest mature one; its photo set was trailing at 89 after 12 h. |

### What this says, and how sure it is

- The differences are small and the sample is tiny (two to four posts per model), so treat this as a first read, not a verdict. Nothing has broken out: every post is in the 130–240 range once it has a day of data.
- 6am posts hold three of the top three places. That may be the slot rather than the content; worth watching next week.
- Best performers to model on: "Same doctor. Two futures." (best engagement), "Your next patient" Case videos (most consistent), "163 patients. One doctor." (most views).
- Weakest model: Full Game, narrowly, once the first-ever post is set aside (mean 188, and the least consistent). It gives up two slots this week to the extras above. If its newer posts ("4 ways to play doctor", "Think you could run an ER?", "Now hiring") do well, the next review should reverse this.
