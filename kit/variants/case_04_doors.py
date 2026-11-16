"""Case variant 04 — "Incoming." The emergency doors slide open on the patient, then the patient's own words fill the
screen, the four moves run as a numbered path ("Four moves. One patient."), the one-call diagnosis box and the end card.
Never reveals the diagnosis.
Video: python3 case_04_doors.py <case-id> <out.mp4>      Preview: python3 case_04_doors.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED

DX, DY, DW, DH = 110, 700, 860, 800  # doorway


def d_hook(K):
    tri = TRI[K['triage']]
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ['Incoming.'], 440, 150)
        o = eio((t - .7) / .9)  # doors: 0 shut, 1 open
        # the bay behind the doors
        c.save(); c.clipRect(skia.Rect.MakeXYWH(DX, DY, DW, DH))
        c.drawRect(skia.Rect.MakeXYWH(DX, DY, DW, DH), grad(0, DY, 0, DY + DH, ['#e3f2f5', '#c6e2e8']))
        c.drawRect(skia.Rect.MakeXYWH(DX, DY + DH - 150, DW, 150), P('#aecbd4'))
        for j in range(2):
            ring = (t * .9 + j * .5) % 1
            c.drawCircle(540, DY + 380, 250 + ring * 130, P(tri, 170 * (1 - ring), stroke=10))
        face(c, 540, DY + 380, 190 + 50 * o, K['skin'], K['hair'], K['style'], 'pain', t)
        # the two door leaves
        for side in (-1, 1):
            x = (DX if side < 0 else 540) + side * o * 440
            c.drawRect(skia.Rect.MakeXYWH(x, DY, 430, DH), grad(x, 0, x + 430, 0, ['#2b7f8a', '#1f6672'] if side < 0 else ['#1f6672', '#2b7f8a']))
            c.drawRect(skia.Rect.MakeXYWH(x, DY + DH - 170, 430, 110), P('#c9d2da'))  # kick plate
            c.drawCircle(x + 215, DY + 250, 112, P('#c9d2da')); c.drawCircle(x + 215, DY + 250, 94, P('#0d2a33'))
            c.drawLine(x + 165, DY + 290, x + 235, DY + 190, P('#ffffff', 60, stroke=14))
            hx = x + 400 if side < 0 else x + 30
            rr(c, hx - 12, DY + 420, 24, 150, 12, P('#e9edf1'))
        if o < .02: c.drawLine(540, DY, 540, DY + DH, P('#12414b', stroke=6, cap=False))
        c.restore()
        rr(c, DX - 14, DY - 14, DW + 28, DH + 28, 18, P('#5b7083', stroke=28))
        # sign + flashing light above the doors
        on = (t * 3) % 1 < .5
        rr(c, 250, DY - 124, 580, 96, 20, P(RED)); text(c, 'EMERGENCY', 540, DY - 54, 66, '#ffffff', 900, 'c')
        for lx in (170, 910):
            c.drawCircle(lx, DY - 76, 70, P(RED, 150 if on else 0, blur=30)); c.drawCircle(lx, DY - 76, 30, P(RED if on else '#6b2327'))
        if t > 1.7:
            k = pop((t - 1.7) / .4)
            pill(c, 540, DY + DH - 150, f"{K['name']}, {K['age']}", '#ffffff', INK, 56, k)
        if t > 2.1:
            pill(c, 540, DY + DH - 44, f"{K['problem']}  ·  Triage {K['triage']}", tri, '#ffffff', 40, pop((t - 2.1) / .4))
    return f


def d_quote(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        k0 = ease(t / .3)
        c.save(); c.translate(0, (1 - k0) * 30)
        face(c, 190, 430, 110, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, f"{K['name']}, {K['age']}", 330, 420, fit(f"{K['name']}, {K['age']}", 64, 690), '#ffffff', 900, a=255 * k0)
        x = 330 + chip(c, 330, 452, K['problem'], '#e2f4f1', TEAL_D, 30) + 14
        chip(c, x, 452, K['level'], '#eef2f6', '#5b7083', 30)
        c.restore()
        text(c, '“', 50, 800, 260, GOLD, 900)
        q = K['quote']; size = 88; lines = wrap(q, size, 900, 940)
        if len(lines) > 5: size = 74; lines = wrap(q, size, 900, 940)
        n = int(len(q) * clamp((t - .35) / 2.6)); shown = 0; y = 800
        for i, ln in enumerate(lines):
            part = ln[:max(0, n - shown)]; shown += len(ln) + 1
            if part: text(c, part, 70, y + i * size * 1.16, size, '#ffffff', 900, shadow=.35)
        yb = y + len(lines) * size * 1.16 + 70
        if t > 3.3: pill(c, 540, max(yb, 1400), "What's your first move?", GOLD, INK, 52, pop((t - 3.3) / .4))
    return f


STEPS = [('talk', 'Talk', 'Get the story'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'),
         ('treat', 'Treat', 'Make it count')]


def d_path(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ['Four moves.', 'One patient.'], 372, 96, a=255 * ease(t / .3))
        active = int(max(0, t - 1.6) / .45) % 4 if t > 1.6 else -1
        y0 = 590; gap = 190
        n = clamp((t - .25) / 1.2) * 3
        c.drawLine(150, y0 + 75, 150, y0 + 75 + gap * 3, P('#ffffff', 50, stroke=10))
        c.drawLine(150, y0 + 75, 150, y0 + 75 + gap * n, P(GOLD, stroke=10))
        for i, (ic, lab, sub) in enumerate(STEPS):
            a0 = .25 + i * .3; y = y0 + i * gap
            if t < a0: continue
            k = ease((t - a0) / .35); on = i == active
            c.drawCircle(150, y + 75, 50, P(GOLD if on else '#ffffff')); text(c, str(i + 1), 150, y + 96, 58, INK, 900, 'c')
            c.save(); c.translate((1 - k) * 600, 0)
            card(c, 240, y, 780, 150, 40)
            if on: rr(c, 240, y, 780, 150, 40, P(GOLD, stroke=10))
            c.drawCircle(326, y + 75, 50, P(TEAL if on else TEAL_D)); icon(c, ic, 326, y + 75, 60)
            text(c, lab, 400, y + 74, 54, INK, 900); text(c, sub, 400, y + 118, 30, '#5b7083', 700)
            c.restore()
        face(c, 150, 1436, 70, K['skin'], K['hair'], K['style'], 'pain', t)
        if t > 2.2:
            first = K['name'].split()[0]
            c.save(); c.translate(250, 1396); k = pop((t - 2.2) / .4); c.scale(k, k)
            chip(c, 0, 0, f'{first} is still waiting', '#ffffff', INK, 40, dot=TRI[K['triage']]); c.restore()
    return f


def build(case_id):
    K, SC = case.build(case_id)
    return K, [(d_hook(K), 3.4), (d_quote(K), 4.6), (d_path(K), 3.8), (SC[2][0], 3.6), (SC[3][0], 3.6)]


def script(K):
    first = K['name'].split()[0]
    tri = ['one', 'two', 'three', 'four', 'five'][K['triage'] - 1]
    return [(0.15, f'Incoming. Triage {tri}.', 2.9), (3.6, f"{first}, {K['age']}. {K['quote']}", 4.2), (8.2, 'Four moves. One patient.', 3.0),
            (12.0, 'One call. Get it right.', 3.0), (15.6, f'{first} is waiting. Bedside Bay. Play free.', 3.1)]


def soundtrack(K, SC, wav):
    import sound
    cues = [(.05, 'beep'), (.35, 'beep'), (.7, 'whoosh'), (1.55, 'impact'), (1.7, 'pop'), (2.1, 'pop'), (3.15, 'whoosh')]
    cues += [(3.8 + i * .13, 'tick') for i in range(18)] + [(6.7, 'ding'), (7.75, 'whoosh')]
    cues += [(8.25 + i * .3, 'pop') for i in range(4)] + [(9.6 + i * .45, 'tick') for i in range(4)] + [(10.2, 'pop')]
    cues += [(11.55, 'whoosh'), (13.5, 'ding'), (13.9, 'beep'), (14.2, 'riser'), (15.4, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=3.4, lift=11.8, cta=15.4, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 1.1), (0, 3.0), (1, 1.5), (1, 4.2), (2, 1.0), (2, 3.4), (3, 3.2), (4, 3.0)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 5)
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
