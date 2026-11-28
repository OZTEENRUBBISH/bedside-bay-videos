"""Case variant 10 — "He said one sentence." Quote first: the patient's own words fill a big speech bubble from the very
first frame (words popping in, then highlighted one by one as the voice reads them). Then a shift handover: "Bed 5 is
yours now." — a clipboard slides in with the handover sheet (name, age, problem, triage, level) and a locked diagnosis
line. Then the four moves pop in around the patient ("Four moves. One call.") as Dr John Smith steps up, and the end
card. Never reveals the diagnosis. The handover sheet and bed number are a framing device, not a game feature.
Music: tense.
Video: python3 case_10_handover.py <case-id> <out.mp4>      Preview: python3 case_10_handover.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED

D0, D1, D2, D3 = 6.0, 4.3, 3.6, 3.8
Q0, QD = 1.75, 3.6  # when the voice starts reading the quote, and for how long (checked against the sound report)
BOARD, BOARD_D, PAPER = '#b98556', '#8a5a34', '#fbf9f4'


def padlock(c, cx, cy, s, col='#ffffff'):
    c.drawArc(skia.Rect.MakeXYWH(cx - s * .3, cy - s * .78, s * .6, s * .7), 180, 180, False, P(col, stroke=s * .14))
    rr(c, cx - s * .44, cy - s * .42, s * .88, s * .72, s * .14, P(col)); c.drawCircle(cx, cy - s * .08, s * .1, P(INK))


def pronoun(K):
    return 'He' if K['id'] == 'ethan-brooks' else K['name'].split()[0]


def k_quote(K):
    q = K['quote']; words = q.split(); nm = f"{K['name']}, {K['age']}"
    size = 88; lines = wrap(q, size, 900, 800)
    while len(lines) > 5: size -= 4; lines = wrap(q, size, 900, 800)
    lh = size * 1.18; x, y, w = 60, 860, 900; bh = len(lines) * lh + 104
    # word boxes
    pos = []; sp = tw(' ', size, 900)
    for i, ln in enumerate(lines):
        xx = x + 50
        for wd in ln.split(): ww = tw(wd, size, 900); pos.append((wd, xx, y + 60 + size * .8 + i * lh, ww)); xx += ww + sp
    chars = sum(len(p[0]) + 1 for p in pos)
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, f'{pronoun(K)} said', 'one sentence.', 356, size=112, sub_size=112)
        ring = (t * .9) % 1
        c.drawCircle(200, 690, 118 + ring * 50, P(TRI[K['triage']], 170 * (1 - ring), stroke=7))
        face(c, 200, 690, 118, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, nm, 350, 676, fit(nm, 64, 590), '#ffffff', 900, shadow=.35)
        xx = 350 + chip(c, 350, 706, K['problem'], '#e2f4f1', TEAL_D, 32) + 14
        chip(c, xx, 706, f"Triage {K['triage']}", TRI[K['triage']], INK if K['triage'] == 3 else '#ffffff', 32)
        tri = skia.Path(); tri.moveTo(170, y + 6); tri.lineTo(200, y - 54); tri.lineTo(270, y + 6); tri.close(); c.drawPath(tri, P('#ffffff'))
        card(c, x, y, w, bh, 54); rr(c, x, y, w, bh, 54, P(TEAL, stroke=6))
        n = len(pos); done = 0
        for i, (wd, wx, wy, ww) in enumerate(pos):
            t0 = .02 + i * 1.45 / n; k = pop((t - t0) / .22) if t >= t0 else 0
            r0 = Q0 + QD * done / chars; r1 = Q0 + QD * (done + len(wd) + 1) / chars; done += len(wd) + 1
            if r0 <= t < r1: rr(c, wx - 12, wy - size * .82, ww + 24, size * 1.08, 16, P(GOLD))
            if k <= 0: text(c, wd, wx, wy, size, '#93a3b3', 900); continue
            c.save(); c.translate(wx + ww / 2, wy - size * .3); c.scale(k, k); text(c, wd, -ww / 2, size * .3, size, INK, 900); c.restore()
        if t > Q0 + QD - .1: pill(c, 500, y + bh + 78, 'Now you decide what it means.', GOLD, INK, 44, pop((t - Q0 - QD + .1) / .35))
    return f


def k_handover(K):
    rows = [('PATIENT', K['name']), ('AGE', K['age']), ('PROBLEM', K['problem']), ('TRIAGE', None), ('LEVEL', K['level']), ('DIAGNOSIS', None), ('HANDED TO', 'Dr John Smith')]
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, 'Bed 5 is yours now.', 'Diagnosis: blank.', 356, size=100, sub_size=84, a=255 * ease(t / .3))
        k = ease((t - .1) / .5); x, y, w, h = 90, 590, 860, 900
        c.save(); c.translate(540 + (1 - k) * 1100, 1040); c.rotate(-2 + (1 - k) * 14); c.translate(-540, -1040)
        rr(c, x + 10, y + 18, w, h, 34, P('#000000', 120, blur=28)); rr(c, x, y, w, h, 34, P(BOARD)); rr(c, x, y, w, h, 34, P(BOARD_D, stroke=6))
        px, py, pw, ph = x + 40, y + 64, w - 80, h - 104
        rr(c, px + 6, py + 8, pw, ph, 10, P('#000000', 50, blur=8)); rr(c, px, py, pw, ph, 10, P(PAPER))
        rr(c, 540 - 150, y - 26, 300, 96, 22, P('#8a9bab')); rr(c, 540 - 110, y - 46, 220, 60, 26, P('#c9d2da')); c.drawCircle(540, y - 16, 14, P('#5b7083'))
        text(c, 'SHIFT HANDOVER', px + 40, py + 104, 44, INK, 900)
        rr(c, px + pw - 210, py + 52, 170, 72, 16, P(TEAL)); text(c, 'BED 5', px + pw - 125, py + 102, 40, '#ffffff', 900, 'c')
        c.drawLine(px + 40, py + 144, px + pw - 40, py + 144, P(INK, stroke=5, cap=False))
        for i, (lab, val) in enumerate(rows):
            a = 255 * ease((t - .7 - i * .26) / .25)
            if a <= 0: continue
            ry = py + 160 + i * 88; mid = ry + 60
            if lab == 'HANDED TO': rr(c, px + 22, ry + 12, pw - 44, 76, 14, P('#e2f4f1', a))
            text(c, lab, px + 40, mid, 28, '#8a9bab', 900, a=a)
            if lab == 'TRIAGE':
                lb = f"Triage {K['triage']}"; cw = tw(lb, 36) + 44
                rr(c, px + 270, ry + 20, cw, 60, 30, P(TRI[K['triage']], a)); text(c, lb, px + 292, mid + 2, 36, INK if K['triage'] == 3 else '#ffffff', 800, a=a)
            elif lab == 'DIAGNOSIS':
                rr(c, px + 270, ry + 18, pw - 310, 64, 12, P(INK, a))
                if a > 200: padlock(c, px + 316, ry + 62, 40); text(c, 'LOCKED', px + 356, mid + 4, 36, '#ffffff', 900)
            else: text(c, val, px + 270, mid + 4, fit(val, 46, pw - 310), TEAL_D if lab == 'HANDED TO' else INK, 900, a=a)
            if i < len(rows) - 1: c.drawLine(px + 40, ry + 94, px + pw - 40, ry + 94, P('#e4e0d6', a, stroke=3, cap=False))
        c.restore()
    return f


MOVES = [('talk', 'Talk', 250, 730), ('examine', 'Examine', 750, 730), ('tests', 'Tests', 250, 1080), ('treat', 'Treat', 750, 1080)]


def k_moves(K):
    first = K['name'].split()[0]
    def f(c, t):
        bg(c, t); brand_bar(c)
        text(c, 'Four moves.', W / 2, 356, 112, GOLD, 900, 'c', a=255 * ease(t / .3), shadow=.35)
        if t > 1.9:
            k = pop((t - 1.9) / .35); c.save(); c.translate(W / 2, 430); c.scale(k, k); text(c, 'One call.', 0, 34, 104, '#ffffff', 900, 'c', shadow=.35); c.restore()
        cx, cy = 500, 890
        for i, (ic, lab, mx, my) in enumerate(MOVES):
            t0 = .3 + i * .38
            if t < t0: continue
            k = pop((t - t0) / .35); on = t - t0 < .38 or (t > 2.3 and int((t - 2.3) / .32) % 4 == i)
            c.drawLine(cx, cy, mx, my, P('#ffffff', 90, stroke=6))
            c.save(); c.translate(mx, my); c.scale(k, k)
            c.drawCircle(0, 10, 112, P('#000000', 90, blur=20)); c.drawCircle(0, 0, 112, P('#ffffff')); c.drawCircle(0, 0, 92, P(TEAL if on else TEAL_D))
            if on: c.drawCircle(0, 0, 112, P(GOLD, stroke=10))
            icon(c, ic, 0, 0, 104)
            w = tw(lab, 46, 900) + 52; rr(c, -w / 2, 96, w, 68, 34, P(INK)); text(c, lab, 0, 146, 46, '#ffffff', 900, 'c')
            c.restore()
        ring = (t * .9) % 1
        c.drawCircle(cx, cy, 104 + ring * 40, P(TRI[K['triage']], 170 * (1 - ring), stroke=7))
        face(c, cx, cy, 104 * pop(t / .35), K['skin'], K['hair'], K['style'], 'pain', t)
        k = ease((t - .9) / .7); dx = (1 - k) * 560
        doctor(c, 820 + dx, 1580, .5, 'resident', t * 2.2, la=10 + (1 - k) * math.sin(t * 12) * 16, ra=-10 - (1 - k) * math.sin(t * 12) * 16, mood='ok')
        if t > 1.5:
            k2 = pop((t - 1.5) / .4); c.save(); c.translate(60, 1440); c.scale(k2, k2); chip(c, 0, 0, f'BED 5  ·  {first.upper()}  ·  DR JOHN SMITH', '#ffffff', INK, 32, dot=TRI[K['triage']]); c.restore()
    return f


def build(case_id):
    K = case.build(case_id)[0]; first = K['name'].split()[0]
    return K, [(k_quote(K), D0), (k_handover(K), D1), (k_moves(K), D2), (cta2(f'{first} is waiting.', 'Take the case.'), D3)]


def script(K):
    first = K['name'].split()[0]; a, b, c_ = D0, D0 + D1, D0 + D1 + D2
    return [(0.15, f'{pronoun(K)} said one sentence.', 1.65), (Q0, K['quote'], QD + .2),
            (a + .2, 'Bed five is yours now. The diagnosis? Blank.', D1 - .5), (b + .2, 'Four moves. One call.', D2 - .5),
            (c_ + .25, f'{first} is waiting. Bedside Bay. Play free.', D3 - .5)]


def soundtrack(K, SC, wav):
    import sound
    a, b, c_ = D0, D0 + D1, D0 + D1 + D2; n = len(K['quote'].split())
    cues = [(.02 + i * 1.45 / n, 'pop' if i % 3 == 0 else 'tick') for i in range(n)] + [(Q0 + QD - .1, 'ding'), (a - .25, 'whoosh')]
    cues += [(a + .1, 'whoosh'), (a + .55, 'impact')] + [(a + .7 + i * .26, 'tick') for i in range(7)] + [(a + .7 + 5 * .26, 'beep'), (a + .7 + 6 * .26, 'ding'), (b - .25, 'whoosh')]
    cues += [(b + .3 + i * .38, 'pop') for i in range(4)] + [(b + 1.9, 'impact'), (c_ - 1.2, 'riser'), (c_, 'impact'), (c_ + .6, 'ding')]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=a, lift=b, cta=c_, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 0.8), (0, 3.0), (0, 5.9), (1, 0.4), (1, 1.6), (1, 4.2), (2, 0.8), (2, 1.6), (2, 3.4), (3, 0.3), (3, 3.0)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 6)
        if len(sys.argv) > 4:
            for n, (i, t) in enumerate(((0, 0.0), (0, 3.0), (1, 4.2), (2, 3.4))): save_jpg(frame(comp(i), t), f'{sys.argv[4]}-{n}.jpg')
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
