"""Full Game variant 07 — "163 patients. All of them talking." The hook is a wall of patient speech bubbles (real quotes from
cases.json, no diagnoses), then the four moves as a 2x2 tile grid, the five ranks as a ring filling round Dr John Smith, and
the four modes as a list that starts in Career. Music: upbeat.
Video: python3 fullgame_07_quotes.py <out.mp4>          Preview: python3 fullgame_07_quotes.py preview <sheet.jpg>"""
from common import *
import json
from case import bg, card, chip, TRI, RED

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
BYID = {k['id']: k for k in CASES}
TALK = ['megan-lewis', 'graham-peters', 'jack-thompson']
OUT = ['intern', 'resident', 'surgeon', 'consultant', 'director']


def bubble(c, K, y, k, right=False):
    x = 120 if right else 60; w, h = 900, 226
    c.save(); c.translate(x + (w if right else 0), y + h); c.scale(k, k); c.translate(-(x + (w if right else 0)), -(y + h))
    card(c, x, y, w, h, 44)
    tx = x + (w - 110 if right else 110)
    tri = skia.Path(); tri.moveTo(tx - 34, y + h - 4); tri.lineTo(tx, y + h + 44); tri.lineTo(tx + 34, y + h - 4); tri.close(); c.drawPath(tri, P('#ffffff'))
    face(c, x + 104, y + 113, 72, K['skin'], K['hair'], K['style'], 'pain', y * .01)
    first = K['name'].split()[0]
    text(c, f"{first}, {K['age']}", x + 204, y + 56, 30, '#5b7083', 800)
    lab = f"TRIAGE {K['triage']}"; lw = tw(lab, 24, 900) + 32
    rr(c, x + w - 36 - lw, y + 24, lw, 44, 22, P(TRI[K['triage']])); text(c, lab, x + w - 36 - lw / 2, y + 55, 24, '#ffffff', 900, 'c')
    q = '“' + K['quote'] + '”'; size = 40; lines = wrap(q, size, 800, 650)
    if len(lines) > 3: size = 34; lines = wrap(q, size, 800, 650)
    for i, ln in enumerate(lines): text(c, ln, x + 204, y + 108 + i * size * 1.2, size, INK, 800)
    c.restore()


def q_hook(c, t):
    bg(c, t); brand_bar(c)
    title2(c, '163 patients.', 'All of them talking.', 356, size=104, sub_size=80)
    for i, cid in enumerate(TALK):
        a0 = .15 + i * .55
        if t >= a0: bubble(c, BYID[cid], 560 + i * 280, pop((t - a0) / .35), right=i % 2 == 1)
    if t > 2.0: pill(c, 540, 1470, 'And 160 more.', GOLD, INK, 56, pop((t - 2.0) / .4))


MOVES = [('talk', 'Talk'), ('examine', 'Examine'), ('tests', 'Tests'), ('treat', 'Treat')]


def moves_grid(c, t, y0=600, th=350, a0=.25, step=.5):
    """2x2 tiles, each lighting up in turn. t = None draws all four lit (photo sets)."""
    for i, (ic, lab) in enumerate(MOVES):
        x = 70 + (i % 2) * 480; y = y0 + (i // 2) * (th + 30); ti = a0 + i * step
        on = t is None or t >= ti; k = 1 if t is None else (pop((t - ti) / .35) if on else 1)
        c.save(); c.translate(x + 230, y + th / 2); c.scale(k, k); c.translate(-(x + 230), -(y + th / 2))
        card(c, x, y, 460, th, 44, col='#ffffff' if on else '#d8e2ea')
        if on: rr(c, x, y, 460, th, 44, P(GOLD, stroke=10))
        cy = y + th * .42
        c.drawCircle(x + 230, cy, 92, P(TEAL if on else '#b5c3cf')); icon(c, ic, x + 230, cy, 110)
        c.drawCircle(x + 62, y + 62, 34, P(GOLD if on else '#eef2f6')); text(c, str(i + 1), x + 62, y + 78, 44, INK, 900, 'c')
        text(c, lab, x + 230, y + th - 44, 60, INK if on else '#8a9bab', 900, 'c')
        c.restore()


def q_moves(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Then it’s your move.', 'Talk. Examine. Tests. Treat.', 356, a=255 * k0, dy=(1 - k0) * 30)
    moves_grid(c, t)
    chip(c, 60, 1420, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)


def q_ranks(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Get it right.', 'Get promoted.', 356, a=255 * k0, dy=(1 - k0) * 30, size=104, sub_size=92)
    step = .52; cur = min(4, int(max(0, t - .3) / step)); lt = max(0, t - .3) - cur * step; top = cur == 4
    cx, cy, r = 540, 900, 230
    c.drawCircle(cx, cy, 330, P(GOLD if top else TEAL, 70, blur=90))
    clip = skia.Path(); clip.addCircle(cx, cy, r); c.save(); c.clipPath(clip, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), grad(0, cy - r, 0, cy + r, ['#dff1f4', '#b9dfe6']))
    doctor(c, cx, cy + 690, 1.3, OUT[cur], t, la=10, ra=-10, mood='tired' if cur == 0 else 'happy'); c.restore()
    ring = skia.Rect.MakeXYWH(cx - 276, cy - 276, 552, 552)
    for i in range(5):
        st = -90 + i * 72 + 5
        c.drawArc(ring, st, 62, False, P('#ffffff', 60, stroke=30, cap=False))
        f = 1 if i < cur else (ease(lt / .3) if i == cur and t >= .3 else 0)
        if f > 0: c.drawArc(ring, st, 62 * f, False, P(GOLD if i == 4 else TEAL, stroke=30, cap=False))
    pill(c, 540, 1270, RANKS[cur], GOLD if top else '#ffffff', INK, 76, pop(lt / .3) if t >= .3 else 1)
    text(c, f'RANK {cur + 1} OF 5', 540, 1392, 38, '#bfe9e4', 800, 'c')
    if cur > 0 and lt < .4:
        k = lt / .4
        for j in range(8):
            a = j * math.pi / 4 + t; sparkle(c, cx + math.cos(a) * (300 + 110 * k), cy + math.sin(a) * (300 + 110 * k), 24, 255 * (1 - k), GOLD)


MODES = [('career', 'Career'), ('shift', 'Quick shift'), ('practice', 'Case practice'), ('firstaid', 'First aid')]


def q_modes(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Four modes.', 'Start in Career.', 356, a=255 * k0, dy=(1 - k0) * 30, size=104, sub_size=84)
    for i, (ic, lab) in enumerate(MODES):
        a0 = .2 + i * .32
        if t < a0: continue
        k = ease((t - a0) / .3); y = 590 + i * 196; first = i == 0
        c.save(); c.translate((1 - k) * (500 if i % 2 else -500), 0)
        card(c, 60, y, 960, 168, 44, col=GOLD if first else '#ffffff')
        c.drawCircle(160, y + 84, 58, P(INK if first else (RED if ic == 'firstaid' else TEAL))); icon(c, ic, 160, y + 84, 70)
        text(c, lab, 254, y + 106, 66, INK, 900)
        if first:
            w = tw('START HERE', 26, 900) + 40; rr(c, 980 - w, y + 58, w, 52, 26, P(INK)); text(c, 'START HERE', 980 - w / 2, y + 93, 26, '#ffffff', 900, 'c')
        c.restore()
    chip(c, 60, 1420, 'DR JOHN SMITH  ·  INTERN, DAY 1', '#ffffff', INK, 28, dot=TEAL)


SC = [(q_hook, 3.4), (q_moves, 3.0), (q_ranks, 3.2), (q_modes, 2.8), (cta2('163 patients are talking.', 'Are you listening?'), 3.4)]

VOICE = [(0.15, 'One hundred and sixty-three patients. All of them talking.', 3.1), (3.6, 'Then it’s your move.', 2.6),
         (6.6, 'Get it right. Get promoted.', 2.9), (9.8, 'Four modes. Start in career.', 2.5), (12.7, 'Bedside Bay. Play free.', 2.9)]


def soundtrack(wav):
    import sound
    cues = [(.15 + i * .55, 'pop') for i in range(3)] + [(2.0, 'ding'), (3.15, 'whoosh'), (6.15, 'whoosh'), (9.35, 'whoosh'), (11.2, 'riser'), (12.4, 'impact')]
    cues += [(3.65 + i * .5, 'pop') for i in range(4)] + [(6.7 + i * .52, f'step:{i}') for i in range(5)] + [(8.8, 'cash')]
    cues += [(9.8 + i * .32, 'pop') for i in range(4)]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=3.4, lift=6.4, cta=12.4, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .16)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 1.0), (0, 3.2), (1, 0.6), (1, 2.8), (2, 0.5), (2, 3.0), (3, 0.5), (3, 2.6), (4, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
