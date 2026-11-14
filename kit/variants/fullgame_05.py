"""Full Game variant 05 — "Think you could run an ER?" A challenge told in numbers: 163 patients (card deck), 4 moves (level
map), 5 ranks (vertical ladder), 4 modes (one big card cycling), then "Prove it." Music: tense.
Video: python3 fullgame_05.py <out.mp4>          Preview: python3 fullgame_05.py preview <sheet.jpg>"""
from common import *
import json
from case import bg, card, chip, TRI, RED

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
BYID = {k['id']: k for k in CASES}
GREEN = '#1f9d63'
LIST = ['163 patients', '4 moves', '5 ranks', '4 modes']


def h_hook(c, t):
    bg(c, t); brand_bar(c)
    headline(c, ['Think you could', 'run an ER?'], 372, 100)
    c.drawCircle(280, 1030, 260, P(TEAL, 60, blur=90))
    doctor(c, 280, 1340, .86, 'resident', t, la=10, ra=-150 + math.sin(t * 6) * 12, mood='happy')
    card(c, 520, 640, 500, 620, 44)
    text(c, 'THE JOB', 560, 712, 30, '#5b7083', 800)
    for i, lab in enumerate(LIST):
        a0 = .05 + i * .25; y = 760 + i * 118
        if t < a0: continue
        k = ease((t - a0) / .3)
        c.save(); c.translate((1 - k) * 200, 0)
        rr(c, 556, y, 428, 96, 24, P('#f3f6f9', 255 * k))
        rr(c, 576, y + 22, 52, 52, 12, P('#c3cfda', 255 * k, stroke=5))
        text(c, lab, 650, y + 64, 44, INK, 900, a=255 * k); c.restore()
    if t > 1.6: pill(c, 540, 1440, 'Prove it.', GOLD, INK, 60, pop((t - 1.6) / .4))
    chip(c, 60, 1500, 'DR JOHN SMITH', '#ffffff', INK, 28, dot=TEAL)


DECK = ['nina-kaur', 'mark-ellis', 'rita-alvarez', 'ethan-brooks', 'bob-harris', 'zoe-martin', 'josh-nguyen', 'paul-morgan']
COUNT = [1, 24, 47, 68, 92, 118, 141, 163]


def h_patients(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, '163 patients', 'Triage 1 to 5.', 356, a=255 * k0, dy=(1 - k0) * 30)
    step = .36; i = min(7, int(t / step)); lt = t - i * step; K = BYID[DECK[i]]
    for j, (ang, dx) in enumerate(((-5, -26), (4, 22))):  # the rest of the deck
        c.save(); c.translate(540 + dx, 960); c.rotate(ang); rr(c, -400, -350, 800, 700, 44, P('#ffffff', 110 + j * 50)); c.restore()
    k = ease(lt / .16)
    c.save(); c.translate((1 - k) * 420, 0)
    card(c, 140, 610, 800, 700, 44)
    face(c, 540, 810, 150, K['skin'], K['hair'], K['style'], 'pain' if i % 2 == 0 else 'ok', t + i)
    text(c, f"{K['name']}, {K['age']}", 540, 1050, 62, INK, 900, 'c')
    w1 = tw(K['problem'], 34) + 44; lab = f"TRIAGE {K['triage']}"; w2 = tw(lab, 34, 900) + 48; x = 540 - (w1 + 16 + w2) / 2
    chip(c, x, 1090, K['problem'], '#e2f4f1', TEAL_D, 34)
    rr(c, x + w1 + 16, 1090, w2, 60, 30, P(TRI[K['triage']])); text(c, lab, x + w1 + 16 + w2 / 2, 1132, 34, '#ffffff', 900, 'c')
    text(c, 'Diagnosis:  ?', 540, 1240, 44, '#8a9bab', 800, 'c')
    c.restore()
    pill(c, 540, 1420, f'PATIENT {COUNT[i]} OF 163', RED, '#ffffff', 44)


STEPS = [('talk', 'Talk', 200, 800), ('examine', 'Examine', 427, 1060), ('tests', 'Tests', 653, 800), ('treat', 'Treat', 880, 1060)]


def h_moves(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, '4 moves', 'Talk. Examine. Tests. Treat.', 356, a=255 * k0, dy=(1 - k0) * 30)
    prog = clamp((t - .3) / 1.65) * 3
    for i in range(3):  # the path between the stops
        (x0, y0), (x1, y1) = STEPS[i][2:], STEPS[i + 1][2:]
        c.drawLine(x0, y0, x1, y1, P('#ffffff', 70, stroke=14))
        f = clamp(prog - i)
        if f > 0: c.drawLine(x0, y0, lerp(x0, x1, f), lerp(y0, y1, f), P(GOLD, stroke=14))
    for i, (ic, lab, x, y) in enumerate(STEPS):
        a0 = .3 + i * .55; on = t >= a0; k = pop((t - a0) / .35) if on else 1
        c.save(); c.translate(x, y); c.scale(k, k)
        c.drawCircle(0, 8, 104, P('#000000', 80, blur=18)); c.drawCircle(0, 0, 104, P('#ffffff'))
        c.drawCircle(0, 0, 88, P(TEAL if on else '#c3cfda')); icon(c, ic, 0, 0, 104)
        c.drawCircle(-76, -76, 34, P(GOLD if on else '#eef2f6')); text(c, str(i + 1), -76, -60, 44, INK, 900, 'c')
        c.restore()
        pill(c, x, y + 150, lab, '#ffffff' if on else '#8a9bab', INK, 36)
    if t > 2.3: pill(c, 540, 1400, 'Then make the call.', GOLD, INK, 52, pop((t - 2.3) / .4))


OUT = ['intern', 'resident', 'surgeon', 'consultant', 'director']


def h_ranks(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, '5 ranks', 'Intern to ED Director.', 356, a=255 * k0, dy=(1 - k0) * 30)
    step = .5; cur = min(4, int(max(0, t - .25) / step)); lt = max(0, t - .25) - cur * step
    for i in range(5):
        y = 1330 - i * 150; on = i <= cur and t >= .25; top = i == 4
        k = pop(lt / .3) if (i == cur and on) else 1
        c.save(); c.translate(340, y + 64); c.scale(k, k); c.translate(-340, -(y + 64))
        card(c, 60, y, 560, 128, 36, col=(GOLD if top else TEAL) if on else '#ffffff')
        c.drawCircle(128, y + 64, 40, P('#ffffff' if on else '#eef2f6')); text(c, str(i + 1), 128, y + 81, 48, INK if on else '#8a9bab', 900, 'c')
        text(c, RANKS[i], 192, y + 82, 50, (INK if top else '#ffffff') if on else '#8a9bab', 900)
        c.restore()
    c.drawCircle(840, 1130, 230, P(GOLD if cur == 4 else TEAL, 70, blur=90))
    doctor(c, 840, 1458, .78, OUT[cur], t, la=10, ra=-150 + math.sin(t * 6) * 12 if cur == 4 else -12, mood='tired' if cur == 0 else 'happy')
    if cur > 0 and lt < .4:
        k = lt / .4
        for j in range(6):
            a = j * math.pi / 3 + t; sparkle(c, 840 + math.cos(a) * (150 + 110 * k), 1130 + math.sin(a) * (170 + 110 * k), 22, 255 * (1 - k), GOLD)


MODES = [('career', 'Career'), ('shift', 'Quick shift'), ('practice', 'Case practice'), ('firstaid', 'First aid')]


def h_modes(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, '4 modes', 'Play it your way.', 356, a=255 * k0, dy=(1 - k0) * 30)
    step = .62; i = min(3, int(t / step)); lt = t - i * step; ic, lab = MODES[i]; k = ease(lt / .2)
    c.save(); c.translate((1 - k) * 500, 0)
    card(c, 140, 600, 800, 660, 48)
    text(c, f'MODE {i + 1} OF 4', 540, 680, 32, '#5b7083', 800, 'c')
    c.drawCircle(540, 880, 150, P(RED if ic == 'firstaid' else TEAL)); icon(c, ic, 540, 880, 180)
    text(c, lab, 540, 1160, 84, INK, 900, 'c'); c.restore()
    for j in range(4): c.drawCircle(540 + (j - 1.5) * 56, 1340, 16, P(GOLD if j == i else '#ffffff', 255 if j == i else 110))
    chip(c, 60, 1440, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)


SC = [(h_hook, 2.8), (h_patients, 3.0), (h_moves, 3.2), (h_ranks, 3.2), (h_modes, 2.8),
      (cta2('Think you could run an ER?', 'Prove it.'), 3.4)]

VOICE = [(0.15, 'Think you could run an E.R.?', 2.5), (3.0, 'One hundred and sixty-three patients.', 2.6),
         (6.0, 'Four moves. Talk, examine, test, treat.', 3.0), (9.2, 'Five ranks. Intern to E.D. Director.', 2.9),
         (12.4, 'Four modes.', 2.3), (15.3, 'Prove it. Bedside Bay. Play free.', 2.9)]


def soundtrack(wav):
    import sound
    cues = [(.05 + i * .25, 'pop') for i in range(4)] + [(1.6, 'ding'), (2.55, 'whoosh'), (5.55, 'whoosh'), (8.75, 'whoosh'), (11.95, 'whoosh'), (13.8, 'riser'), (15.0, 'impact')]
    cues += [(2.8 + i * .36, 'tick') for i in range(8)] + [(6.1 + i * .55, 'pop') for i in range(4)] + [(8.1, 'ding')]
    cues += [(9.25 + i * .5, f'step:{i}') for i in range(5)] + [(12.2 + i * .62, 'pop') for i in range(4)]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=2.8, lift=9.0, cta=15.0, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 2.4), (1, 0.5), (1, 2.8), (2, 1.2), (2, 3.0), (3, 0.9), (3, 3.0), (4, 0.4), (4, 2.6)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
