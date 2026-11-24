"""Case variant 09 — "Searched the symptoms first." The patient's own words are typed into a symptom search box, the
results come back as grey bars and "No clear answer. See a doctor." Then: that doctor is you. The patient card with the
quote in a speech bubble, the four moves as four search-suggestion rows ("No search bar. Just four moves."), the
one-call diagnosis box and the end card. Never reveals the diagnosis. The search is a framing device, not a game feature.
Music: upbeat.
Video: python3 case_09_search.py <case-id> <out.mp4>      Preview: python3 case_09_search.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED


def glass(c, cx, cy, s, col, w=9):
    c.drawCircle(cx - s * .12, cy - s * .12, s * .34, P(col, stroke=w)); c.drawLine(cx + s * .14, cy + s * .14, cx + s * .46, cy + s * .46, P(col, stroke=w))


D0, D1, D2 = 3.6, 5.0, 3.5


def k_search(K):
    first = K['name'].split()[0]; q = K['quote']
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, f'{first} searched', 'the symptoms first.', 356, size=104, sub_size=84)
        size = 50; lines = wrap(q, size, 700, 760)
        bh = len(lines) * 66 + 70; x, y, w = 60, 560, 960
        rr(c, x, y + 12, w, bh, 46, P('#000000', 90, blur=26)); rr(c, x, y, w, bh, 46, P('#ffffff')); rr(c, x, y, w, bh, 46, P(TEAL, stroke=6))
        glass(c, x + 74, y + 74, 62, '#5b7083')
        n = int(len(q) * clamp((t - .15) / 1.7)); shown = 0
        for i, ln in enumerate(lines):
            part = ln[:max(0, n - shown)]; shown += len(ln) + 1; by = y + 84 + i * 66
            if part or i == 0:
                wv = text(c, part, x + 140, by, size, INK, 700) if part else 0
                if len(part) < len(ln) and shown - len(ln) - 1 <= n and (t * 3) % 1 < .6: rr(c, x + 144 + wv, by - 42, 5, 52, 2, P(TEAL))
        y0 = y + bh + 44
        text(c, 'RESULTS', x + 20, y0 + 30, 28, '#9fb8c8', 900, a=255 * ease((t - 1.9) / .3))
        for j in range(3):
            a = 255 * ease((t - 2.0 - j * .12) / .3); ry = y0 + 56 + j * 136
            rr(c, x, ry, w, 116, 26, P('#ffffff', a * .16))
            rr(c, x + 34, ry + 26, 420 + j * 120, 24, 12, P('#ffffff', a * .5)); rr(c, x + 34, ry + 68, 700 - j * 90, 18, 9, P('#ffffff', a * .28))
        if t > 2.45:
            k = pop((t - 2.45) / .4); c.save(); c.translate(540, y0 + 56 + 190); c.scale(k, k); c.rotate(-3)
            rr(c, -400, -96, 800, 204, 36, P('#000000', 110, blur=24)); rr(c, -400, -108, 800, 204, 36, P('#ffffff'))
            text(c, 'No clear answer.', 0, -22, 70, RED, 900, 'c'); text(c, 'See a doctor.', 0, 56, 58, INK, 900, 'c'); c.restore()
        if t > 2.95: pill(c, 540, 1470, 'That doctor is you.', GOLD, INK, 54, pop((t - 2.95) / .4))
    return f


def k_patient(K):
    first = K['name'].split()[0]; q = '“' + K['quote'] + '”'
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, f'So {first} came', 'to your ER.', 356, size=104, sub_size=104, a=255 * ease(t / .3))
        ring = (t * .9) % 1
        c.drawCircle(250, 760, 150 + ring * 70, P(TRI[K['triage']], 170 * (1 - ring), stroke=8))
        face(c, 250, 760, 150 * pop(t / .4), K['skin'], K['hair'], K['style'], 'pain', t)
        a = 255 * ease((t - .2) / .4); nm = f"{K['name']}, {K['age']}"
        text(c, nm, 450, 730, fit(nm, 68, 570), '#ffffff', 900, a=a, shadow=.35)
        if t > .35:
            xx = 450 + chip(c, 450, 762, K['problem'], '#e2f4f1', TEAL_D, 32) + 14
            chip(c, xx, 762, f"Triage {K['triage']}", TRI[K['triage']], INK if K['triage'] == 3 else '#ffffff', 32)
        size = 68; lines = wrap(q, size, 900, 840)
        while len(lines) > 4: size -= 4; lines = wrap(q, size, 900, 840)
        bh = len(lines) * size * 1.2 + 96; by = 1000; k = ease((t - .45) / .4)
        if k > 0:
            c.save(); c.translate(0, (1 - k) * 140)
            tri = skia.Path(); tri.moveTo(210, by + 6); tri.lineTo(250, by - 60); tri.lineTo(310, by + 6); tri.close(); c.drawPath(tri, P('#ffffff', 255 * k))
            card(c, 60, by, 960, bh, 48, a=255 * k)
            n = int(len(q) * clamp((t - .7) / 2.6)); shown = 0
            for i, ln in enumerate(lines):
                part = ln[:max(0, n - shown)]; shown += len(ln) + 1
                if part: text(c, part, 120, by + 52 + size * .8 + i * size * 1.2, size, INK, 900)
            c.restore()
        if t > 3.7:
            k2 = pop((t - 3.7) / .4); c.save(); c.translate(60, 1440); c.scale(k2, k2); chip(c, 0, 0, 'DR JOHN SMITH  ·  YOUR PATIENT NOW', '#ffffff', INK, 30, dot=TEAL); c.restore()
    return f


ROWS = [('talk', 'Talk', 'Ask what the search could not'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Make the call')]


def k_moves(K):
    first = K['name'].split()[0]
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, 'No search bar.', 'Just four moves.', 356, size=108, sub_size=92, a=255 * ease(t / .3))
        active = int(max(0, t - 1.4) / .5) % 4 if t > 1.4 else -1
        for i, (ic, lab, sub) in enumerate(ROWS):
            k = ease((t - .2 - i * .2) / .35)
            if k <= 0: continue
            y = 560 + i * 196; on = i == active
            c.save(); c.translate((1 - k) * (600 if i % 2 else -600), 0)
            rr(c, 60, y + 10, 960, 164, 82, P('#000000', 90, blur=22)); rr(c, 60, y, 960, 164, 82, P('#ffffff'))
            if on: rr(c, 60, y, 960, 164, 82, P(GOLD, stroke=10))
            c.drawCircle(150, y + 82, 58, P(TEAL if on else TEAL_D)); icon(c, ic, 150, y + 82, 68)
            text(c, lab, 236, y + 80, 60, INK, 900); text(c, sub, 238, y + 126, 32, '#5b7083', 700)
            text(c, str(i + 1), 950, y + 106, 70, GOLD if on else '#c3cfda', 900, 'c')
            c.restore()
        if t > 1.9:
            lab = f'{first} is still waiting'; w = tw(lab, 40) + 74
            c.save(); c.translate(540, 1440); k = pop((t - 1.9) / .4); c.scale(k, k)
            chip(c, -w / 2, -33, lab, '#ffffff', INK, 40, dot=TRI[K['triage']]); c.restore()
    return f


def build(case_id):
    K, SC = case.build(case_id)
    return K, [(k_search(K), D0), (k_patient(K), D1), (k_moves(K), D2), (SC[2][0], 3.5), (SC[3][0], 3.6)]


def script(K):
    first = K['name'].split()[0]; a, b, c_ = D0, D0 + D1, D0 + D1 + D2
    return [(0.15, f'{first} searched the symptoms first.', 2.6), (a + .2, f"{first}, {K['age']}. {K['quote']}", D1 - .4),
            (b + .2, 'No search bar. Just four moves.', D2 - .5), (c_ + .2, 'One call. Get it right.', 3.0), (c_ + 3.7, f'{first} is waiting. Bedside Bay. Play free.', 3.1)]


def soundtrack(K, SC, wav):
    import sound
    a, b, c_ = D0, D0 + D1, D0 + D1 + D2; e = c_ + 3.5; n = 16
    cues = [(.05, 'pop')] + [(.2 + i * 1.6 / n, 'tick') for i in range(n)] + [(2.0, 'beep'), (2.45, 'impact'), (2.95, 'ding'), (a - .25, 'whoosh')]
    cues += [(a + .05, 'pop'), (a + .45, 'whoosh'), (a + 3.7, 'pop'), (b - .25, 'whoosh')]
    cues += [(b + .2 + i * .2, 'pop') for i in range(4)] + [(b + 1.4 + i * .5, 'tick') for i in range(4)] + [(b + 1.9, 'ding')]
    cues += [(c_ - .25, 'whoosh'), (c_ + 1.7, 'ding'), (c_ + 2.1, 'beep'), (e - 1.2, 'riser'), (e, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=a, lift=c_, cta=e, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 1.0), (0, 2.3), (0, 3.4), (1, 0.6), (1, 2.0), (1, 4.8), (2, 1.0), (2, 3.2), (3, 3.2), (4, 3.0)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 6)
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
