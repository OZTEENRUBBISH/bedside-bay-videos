"""Case variant 06 — "Triage 1. Drop everything." A big triage board flips 5, 4, 3, 2, 1 and locks on the patient's own
triage number, then the patient with the quote typed into a speech bubble, the four moves as a stacked run sheet with a
highlight sweeping down it ("Four moves. No time to waste."), then the one-call diagnosis box and the end card.
Never reveals the diagnosis. Music: tense. Best with Triage 1 or 2 patients.
Video: python3 case_06_triage_board.py <case-id> <out.mp4>      Preview: python3 case_06_triage_board.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED

WORD = ['one', 'two', 'three', 'four', 'five']
FLIP0, STEP = .35, .3  # first flip, seconds per flip


def k_board(K):
    T = K['triage']; seq = list(range(5, T - 1, -1)); t_lock = FLIP0 + (len(seq) - 1) * STEP
    def f(c, t):
        bg(c, t)
        i = int(clamp((t - FLIP0) / STEP + 1, 0, len(seq) - 1)) if t >= FLIP0 else 0
        n = seq[i]; col = TRI[n]; locked = t >= t_lock
        if locked:
            c.drawRect(skia.Rect.MakeWH(W, H), P(col, 46 * (.5 + .5 * math.sin((t - t_lock) * 9))))
        brand_bar(c)
        title2(c, f'Triage {T}.', 'Drop everything.', 372, top_col=col if locked else '#ffffff', size=112, sub_size=88,
               a=255)
        # the board
        bx, by, bw, bh = 240, 590, 600, 640
        if locked:
            for j in range(2):
                ring = ((t - t_lock) * .9 + j * .5) % 1
                rr(c, bx - ring * 70, by - ring * 70, bw + ring * 140, bh + ring * 140, 60 + ring * 40, P(col, 190 * (1 - ring), stroke=12))
        rr(c, bx, by + 16, bw, bh, 56, P('#000000', 110, blur=30)); rr(c, bx, by, bw, bh, 56, P('#0b1420'))
        rr(c, bx + 24, by + 24, bw - 48, bh - 48, 40, P(col))
        text(c, 'TRIAGE', 540, by + 124, 64, '#ffffff', 900, 'c', a=220)
        ph = clamp((t - FLIP0 - (i - 1) * STEP) / .14) if i > 0 else 1  # flip-in squash
        sc = 1.0 + (.18 * pop(clamp((t - t_lock) / .35)) if locked else 0)
        c.save(); c.translate(540, by + 400); c.scale(sc, sc * (.25 + .75 * ph))
        text(c, str(n), 0, 150, 430, '#ffffff', 900, 'c', shadow=.3); c.restore()
        c.drawLine(bx + 24, by + 372, bx + bw - 24, by + 372, P('#0b1420', 90, stroke=6, cap=False))  # split-flap seam
        # the scale underneath
        for j in range(1, 6):
            x = 540 + (j - 3) * 116; on = j == n
            c.drawCircle(x, 1330, 46 if on else 36, P(TRI[j], 255 if on else 90))
            if on: c.drawCircle(x, 1330, 56, P('#ffffff', stroke=6))
            text(c, str(j), x, 1346 if on else 1343, 46 if on else 38, '#ffffff', 900, 'c', a=255 if on else 150)
        if t > t_lock + .45: pill(c, 540, 1470, f"{K['name']}, {K['age']}", '#ffffff', INK, 56, pop((t - t_lock - .45) / .4))
        if t > t_lock + .8: pill(c, 540, 1574, f"{K['problem']}  ·  Triage {T}", col, '#ffffff', 40, pop((t - t_lock - .8) / .4))
    return f, t_lock


def k_quote(K, dur):
    q = K['quote']; col = TRI[K['triage']]
    def f(c, t):
        bg(c, t); brand_bar(c)
        k0 = pop(t / .4)
        for j in range(2):
            ring = (t * .9 + j * .5) % 1
            c.drawCircle(540, 500, 160 + ring * 90, P(col, 170 * (1 - ring), stroke=9))
        c.save(); c.translate(540, 500); c.scale(k0, k0); face(c, 0, 0, 160, K['skin'], K['hair'], K['style'], 'pain', t); c.restore()
        a = 255 * ease((t - .2) / .3)
        text(c, f"{K['name']}, {K['age']}", 540, 760, 64, '#ffffff', 900, 'c', a=a, shadow=.35)
        lab = f"TRIAGE {K['triage']}  ·  {K['problem'].upper()}"; w = tw(lab, 32, 900) + 56
        rr(c, 540 - w / 2, 790, w, 62, 31, P(col, a)); text(c, lab, 540, 833, 32, '#ffffff', 900, 'c', a=a)
        # speech bubble
        size = 62; lines = wrap(q, size, 800, 820)
        while len(lines) > 4: size -= 4; lines = wrap(q, size, 800, 820)
        bh = len(lines) * size * 1.2 + 110; by = 930
        kb = ease((t - .45) / .35)
        if kb > 0:
            c.save(); c.translate(540, by); c.scale(kb, kb); c.translate(-540, -by)
            tail = skia.Path(); tail.moveTo(480, by + 4); tail.lineTo(540, by - 56); tail.lineTo(600, by + 4); tail.close()
            rr(c, 70, by + 12, 940, bh, 48, P('#000000', 90, blur=24)); rr(c, 70, by, 940, bh, 48, P('#ffffff')); c.drawPath(tail, P('#ffffff'))
            n = int(len(q) * clamp((t - .9) / (dur - 2.6))); shown = 0
            for i, ln in enumerate(lines):
                part = ln[:max(0, n - shown)]; shown += len(ln) + 1
                if part: text(c, part, 130, by + 96 + i * size * 1.2, size, INK, 800)
            c.restore()
        if t > dur - 1.3: pill(c, 540, by + bh + 90, 'No diagnosis yet. That part is you.', GOLD, INK, 42, pop((t - dur + 1.3) / .4))
    return f


ROWS = [('talk', 'Talk', 'Take the history'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Act before it gets worse')]


def k_sheet(K):
    col = TRI[K['triage']]
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, 'Four moves.', 'No time to waste.', 372, size=104, sub_size=80, a=255 * ease(t / .3))
        active = int(max(0, t - 1.5) / .5) % 4 if t > 1.5 else -1
        c.drawLine(128, 640, 128, 1330, P('#ffffff', 60, stroke=8))
        for i, (ic, lab, sub) in enumerate(ROWS):
            k = ease((t - .25 - i * .22) / .4)
            if k <= 0: continue
            y = 570 + i * 210; on = i == active; dx = (1 - k) * 700 + (24 if on else 0)
            c.save(); c.translate(dx, 0)
            card(c, 190, y, 800, 180, 40)
            if on: rr(c, 190, y, 800, 180, 40, P(GOLD, stroke=10))
            c.drawCircle(290, y + 90, 60, P(TEAL if on else TEAL_D)); icon(c, ic, 290, y + 90, 72)
            text(c, lab, 380, y + 84, 62, INK, 900); text(c, sub, 382, y + 136, 34, '#5b7083', 700)
            c.restore()
            c.drawCircle(128, y + 90, 40, P(GOLD if on else '#ffffff')); text(c, str(i + 1), 128, y + 106, 44, INK, 900, 'c')
        first = K['name'].split()[0]
        if t > 2.0:
            lab = f'{first} is Triage {K["triage"]}'; w = tw(lab, 40) + 74
            c.save(); c.translate(540, 1470); k = pop((t - 2.0) / .4); c.scale(k, k)
            chip(c, -w / 2, -33, lab, '#ffffff', INK, 40, dot=col); c.restore()
        chip(c, 60, 1540, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
    return f


D_HOOK, D_Q, D_M = 3.4, 4.8, 3.8


def build(case_id):
    K, SC = case.build(case_id); hook, t_lock = k_board(K)
    return K, [(hook, D_HOOK), (k_quote(K, D_Q), D_Q), (k_sheet(K), D_M), (SC[2][0], 3.6), (SC[3][0], 3.4)], t_lock


def script(K):
    import re
    first = K['name'].split()[0]; q1 = re.split(r'(?<=[.!?,])\s+', K['quote'])[0].rstrip(',') + '.'
    t2 = D_HOOK; t3 = t2 + D_Q; t4 = t3 + D_M; t5 = t4 + 3.6
    return [(0.15, f"Triage {WORD[K['triage'] - 1]}. Drop everything.", 3.0), (t2 + .25, f"{first}, {K['age']}. {q1.replace('..', '.')}", D_Q - .6),
            (t3 + .25, 'Four moves. No time to waste.', 3.3), (t4 + .3, 'One call. Get it right.', 3.0),
            (t5 + .25, f'{first} is waiting. Bedside Bay. Play free.', 3.05)]


def soundtrack(K, SC, wav, t_lock):
    import sound
    t2 = D_HOOK; t3 = t2 + D_Q; t4 = t3 + D_M; t5 = t4 + 3.6
    nfl = int(round((t_lock - FLIP0) / STEP))
    cues = [(.05, 'beep')] + [(FLIP0 + i * STEP, 'tick') for i in range(nfl)] + [(t_lock, 'impact'), (t_lock + .45, 'pop'), (t_lock + .8, 'pop')]
    cues += [(t2 - .25, 'whoosh'), (t2 + .45, 'pop')] + [(t2 + .9 + i * .11, 'tick') for i in range(18)] + [(t3 - 1.3, 'ding'), (t3 - .25, 'whoosh')]
    cues += [(t3 + .25 + i * .22, 'pop') for i in range(4)] + [(t3 + 1.5 + i * .5, 'tick') for i in range(4)] + [(t3 + 2.0, 'ding')]
    cues += [(t4 - .25, 'whoosh'), (t4 + 1.7, 'ding'), (t4 + 2.1, 'beep'), (t5 - 1.2, 'riser'), (t5, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=D_HOOK, lift=t3, cta=t5, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC, t_lock = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 0.8), (0, 1.7), (0, 3.2), (1, 0.6), (1, 2.4), (1, 4.6), (2, 1.0), (2, 3.2), (3, 3.2), (4, 3.0)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 6)
    elif sys.argv[2] == 'voice':
        import sound
        for _, l, _ in script(K): print(l, '->', sound.phonemes(l))
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav, t_lock): print(r, round(r[0] + r[1], 2))
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
