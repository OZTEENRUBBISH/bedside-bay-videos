"""Case variant 03 — "You're being paged." A buzzing pager types out the patient, then the patient speaks (speech bubble),
the four moves orbit the patient ("Your move, Dr Smith."), the one-call diagnosis box and the end card. Never reveals the diagnosis.
Video: python3 case_03.py <case-id> <out.mp4>      Preview: python3 case_03.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED

LCD = '#12301a'


def pg_hook(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ["You're being", 'paged.'], 372, 104)
        buzz = (t % 1.1) < .5
        sh = math.sin(t * 60) * 8 if buzz else 0
        for j in range(2):
            ring = (t * 1.1 + j * .5) % 1
            c.drawCircle(540, 980, 330 + ring * 170, P(TRI[K['triage']], 150 * (1 - ring), stroke=8))
        c.save(); c.translate(540 + sh, 980); c.rotate(-4 + sh * .15)
        rr(c, -380, -246, 760, 520, 70, P('#000000', 110, blur=30))
        rr(c, -380, -260, 760, 520, 70, P('#1c2530')); rr(c, -380, -260, 760, 520, 70, P('#3a4756', stroke=6))
        rr(c, -330, -212, 660, 318, 24, P('#0b1218')); rr(c, -318, -200, 636, 294, 16, grad(0, -200, 0, 94, ['#c9f2bd', '#a5dd98']))
        rows = [('PAGE FOR DR JOHN SMITH', 28, 800), (f"{K['name']}, {K['age']}".upper(), 52, 900), (K['problem'].upper(), 52, 900),
                (f"TRIAGE {K['triage']}  ·  WAITING NOW", 36, 900)]
        n = int(sum(len(r[0]) for r in rows) * clamp((t - .15) / 1.6)); shown = 0; y = -180
        for s, size, wt in rows:
            size = fit(s, size, 580, wt); part = s[:max(0, n - shown)]; shown += len(s)
            if part: text(c, part, -290, y + size * .8, size, LCD, wt)
            y += size + 16
        on = (t * 4) % 1 < .5
        c.drawCircle(-290, 186, 22, P(RED if on else '#5a2326')); c.drawCircle(-290, 186, 40, P(RED, 90 if on else 0, blur=16))
        for i in range(3): rr(c, -200 + i * 130, 160, 100, 52, 26, P('#3a4756'))
        for i in range(4): rr(c, 220 + i * 28, 150, 12, 72, 6, P('#0b1218'))
        c.restore()
        if t > 2.0: pill(c, 540, 1400, 'Your patient is waiting.', GOLD, INK, 50, pop((t - 2.0) / .4))
        chip(c, 60, 1500, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
    return f


def pg_patient(K):
    first = K['name'].split()[0]
    def f(c, t):
        bg(c, t); brand_bar(c)
        k0 = ease(t / .3)
        title2(c, f'Meet {first}.', f"{K['age']}  ·  {K['problem']}  ·  Triage {K['triage']}", 356, a=255 * k0, dy=(1 - k0) * 30, size=104, sub_size=60)
        ring = (t * .9) % 1
        c.drawCircle(540, 760, 195 + ring * 90, P(TRI[K['triage']], 170 * (1 - ring), stroke=8))
        c.drawCircle(540, 760, 240, P(TEAL, 70, blur=80))
        face(c, 540, 760, 190, K['skin'], K['hair'], K['style'], 'pain', t)
        q = '“' + K['quote'] + '”'; size = 64; lines = wrap(q, size, 900, 860)
        if len(lines) > 3: size = 54; lines = wrap(q, size, 900, 860)
        h = len(lines) * size * 1.18 + 90; y = 1030; kb = ease((t - .25) / .35)
        if t > .25:
            c.save(); c.translate(0, (1 - kb) * 80)
            tri = skia.Path(); tri.moveTo(490, y + 6); tri.lineTo(540, y - 56); tri.lineTo(590, y + 6); tri.close(); c.drawPath(tri, P('#ffffff', 255 * kb))
            card(c, 60, y, 960, h, 44, a=255 * kb)
            n = int(len(q) * clamp((t - .5) / 2.3)); shown = 0
            for i, ln in enumerate(lines):
                part = ln[:max(0, n - shown)]; shown += len(ln) + 1
                if part: text(c, part, 540 - tw(ln, size, 900) / 2, y + 50 + size * .8 + i * size * 1.18, size, INK, 900)
            c.restore()
        if t > 3.2: pill(c, 540, y + h + 96, 'Diagnosis: hidden.', GOLD, INK, 50, pop((t - 3.2) / .4))
    return f


MOVES = [('talk', 'Talk', 250, 760), ('examine', 'Examine', 830, 760), ('tests', 'Tests', 250, 1190), ('treat', 'Treat', 830, 1190)]


def pg_moves(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ['Your move,', 'Dr Smith.'], 372, 104, a=255 * ease(t / .3))
        active = int(max(0, t - 1.5) / .45) % 4 if t > 1.5 else -1
        for i, (ic, lab, x, y) in enumerate(MOVES):
            if t >= .2 + i * .28: c.drawLine(540, 975, x, y, P(GOLD if i == active else '#ffffff', 255 if i == active else 70, stroke=12))
        c.drawCircle(540, 975, 190, P(TEAL, 70, blur=70))
        face(c, 540, 975, 136, K['skin'], K['hair'], K['style'], 'pain', t)
        for i, (ic, lab, x, y) in enumerate(MOVES):
            a0 = .2 + i * .28
            if t < a0: continue
            on = i == active; k = pop((t - a0) / .35) * (1.08 if on else 1)
            c.save(); c.translate(x, y); c.scale(k, k)
            c.drawCircle(0, 8, 104, P('#000000', 80, blur=18)); c.drawCircle(0, 0, 104, P('#ffffff'))
            c.drawCircle(0, 0, 88, P(GOLD if on else TEAL)); icon(c, ic, 0, 0, 104, INK if on else '#ffffff'); c.restore()
            pill(c, x, y + 150, lab, GOLD if on else '#ffffff', INK, 40)
        if t > 2.2: pill(c, 540, 1470, 'What do you do first?', '#ffffff', INK, 50, pop((t - 2.2) / .4))
    return f


def build(case_id):
    K, SC = case.build(case_id)
    return K, [(pg_hook(K), 3.4), (pg_patient(K), 4.4), (pg_moves(K), 3.8), (SC[2][0], 3.6), (SC[3][0], 3.6)]


def script(K):
    first = K['name'].split()[0]
    return [(0.15, "Doctor Smith. You're being paged.", 3.0), (3.6, f"{first}, {K['age']}. {K['quote']}", 4.0), (8.1, 'Your move, doctor.', 3.0),
            (11.9, 'One call. Get it right.', 3.0), (15.5, f'{first} is waiting. Bedside Bay. Play free.', 3.1)]


def soundtrack(K, SC, wav):
    import sound
    cues = [(.05 + j * 1.1 + i * .16, 'beep') for j in range(3) for i in range(3)] + [(.2 + i * .1, 'tick') for i in range(16)] + [(2.0, 'pop')]
    cues += [(3.15, 'whoosh'), (7.55, 'whoosh'), (11.35, 'whoosh'), (14.0, 'riser'), (15.2, 'impact'), (6.6, 'ding')]
    cues += [(7.8 + .2 + i * .28, 'pop') for i in range(4)] + [(9.3 + i * .45, 'tick') for i in range(5)] + [(13.3, 'ding'), (13.7, 'beep')]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=3.4, lift=11.6, cta=15.2, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 1.0), (0, 3.0), (1, 0.4), (1, 4.0), (2, 1.0), (2, 3.4), (3, 3.2), (4, 3.0)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 5)
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
