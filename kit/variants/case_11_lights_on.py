"""Case variant 11 — "Lights on." Quote first, in the dark: a black screen with the patient's exact words arriving one
word at a time like subtitles under "Someone in bed 7 just said this." Then the lights snap on and the patient's card
is there (name, age, problem, triage and level from cases.json). "You're the doctor.": Dr John Smith and the four
moves as four light switches that flip on one by one, lighting the room. The diagnosis stays in the dark (an unlit
bulb over a blank box) and the end card closes it. Never reveals the diagnosis. "Bed 7" and the lights are a framing
device, not a game feature.
Music: upbeat.
Video: python3 case_11_lights_on.py <case-id> <out.mp4>      Preview: python3 case_11_lights_on.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import card, chip, TRI

D0, D1, D2, D3, D4 = 4.1, 4.0, 4.1, 3.2, 3.4
W0, WSTEP = .0, .255      # first word at t=0, then one word every WSTEP seconds (matches the voice)
ASK = 3.3                 # "Bed 7. Lights on?"
SW0, SWSTEP = 1.25, .52   # when the four switches flip


def dark(c, t, glow=0):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#05070b', '#0a1018']))
    if glow: c.drawCircle(540, 900, 620, P('#27405c', glow, blur=160))


def k_dark(K):
    words = ('“' + K['quote'] + '”').split(); size = 100
    lines = wrap(' '.join(words), size, 900, 830)
    while len(lines) > 6: size -= 4; lines = wrap(' '.join(words), size, 900, 830)
    def f(c, t):
        dark(c, t, 26); brand_bar(c)
        title2(c, 'Someone in bed 7', 'just said this.', 352, '#ffffff', '#9fb8c8', size=64, sub_size=64, shadow=0)
        n = min(len(words), 1 + int(max(0, t - W0) / WSTEP)); y0 = 640; lh = size * 1.18
        rr(c, 70, y0 - size * .8, 10, lh * len(lines) - size * .2, 5, P(TEAL))
        i = 0
        for li, ln in enumerate(lines):
            x = 112
            for w in ln.split():
                if i < n:
                    new = i == n - 1 and n < len(words); a = 255 * clamp((t - W0 - i * WSTEP) / .08 + .35) if i else 255
                    text(c, w, x, y0 + li * lh, size, GOLD if new else '#ffffff', 900, a=a)
                x += tw(w + ' ', size, 900); i += 1
        if t > ASK:
            k = pop((t - ASK) / .35); by = y0 + len(lines) * lh + 40
            c.save(); c.translate(540, by + 60); c.scale(k, k)
            rr(c, -330, -58, 660, 116, 58, P('#ffffff', 28)); rr(c, -330, -58, 660, 116, 58, P('#ffffff', 200, stroke=5))
            text(c, 'Bed 7. Lights on?', 0, 20, 60, '#ffffff', 900, 'c'); c.restore()
    return f


def k_lit(K):
    q = '“' + K['quote'] + '”'; nm = f"{K['name']}, {K['age']}"; tc = TRI[K['triage']]
    def f(c, t):
        c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#f3fbfb', '#cfe6ea']))
        c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, H - 1500), P('#b4d0d6')); c.drawRect(skia.Rect.MakeXYWH(0, 1490, W, 14), P('#9cc0c8'))
        rr(c, 240, 0, 600, 44, 12, P('#ffffff')); c.drawCircle(540, 60, 520, P('#ffffff', 150, blur=120))   # ceiling light
        brand_bar(c)
        k = ease(t / .3)
        title2(c, 'Lights on.', 'Meet bed 7.', 356, INK, TEAL_D, a=255 * k, shadow=0, size=116, sub_size=80)
        kk = pop(t / .45); c.save(); c.translate(540, 900); c.scale(kk, kk); c.translate(-540, -900)
        card(c, 60, 540, 900, 800, 48)
        rr(c, 96, 576, 150, 56, 28, P(INK)); text(c, 'BED 7', 171, 616, 32, '#ffffff', 900, 'c')
        ring = (t * .9) % 1
        c.drawCircle(510, 760, 150 + ring * 50, P(tc, 150 * (1 - ring), stroke=8))
        face(c, 510, 760, 150, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, nm, 510, 1000, fit(nm, 80, 820), INK, 900, 'c')
        labs = [(K['problem'], '#e2f4f1', TEAL_D), (f"Triage {K['triage']}", tc, INK if K['triage'] == 3 else '#ffffff'), (K['level'], '#eef2f6', '#5b7083')]
        tot = sum(tw(l, 34) + 44 for l, _, _ in labs) + 28; x = 510 - tot / 2
        for j, (l, b, fg) in enumerate(labs):
            if t > .35 + j * .15: chip(c, x, 1034, l, b, fg, 34)
            x += tw(l, 34) + 44 + 14
        c.drawLine(110, 1130, 910, 1130, P('#e4eaf0', stroke=3))
        size = 44; lines = wrap(q, size, 700, 800)
        for i, ln in enumerate(lines[:3]): text(c, ln, 510, 1196 + i * 58, size, '#33475b', 700, 'c', a=255 * ease((t - .6) / .4))
        c.restore()
        if t > 1.5:
            k2 = pop((t - 1.5) / .4); lab = 'DR JOHN SMITH  ·  YOUR PATIENT NOW'; w = tw(lab, 30) + 74
            c.save(); c.translate(510, 1420); c.scale(k2, k2); chip(c, -w / 2, -28, lab, INK, '#ffffff', 30, dot=TEAL); c.restore()
    return f


MOVES = [('talk', 'Talk'), ('examine', 'Examine'), ('tests', 'Tests'), ('treat', 'Treat')]


def switch(c, x, y, ic, lab, k):
    """A wall switch plate, 590x160. k = 0 off .. 1 on."""
    on = k > .5
    if on: rr(c, x - 10, y - 10, 610, 180, 50, P(GOLD, 120 * k, blur=26))
    rr(c, x, y + 8, 590, 160, 40, P('#000000', 90, blur=16)); rr(c, x, y, 590, 160, 40, P('#ffffff' if on else '#1a2634'))
    if not on: rr(c, x, y, 590, 160, 40, P('#33475b', stroke=4))
    for sx, sy in ((x + 22, y + 22), (x + 568, y + 138)): c.drawCircle(sx, sy, 6, P('#c3cfda' if on else '#33475b'))
    rr(c, x + 34, y + 30, 76, 100, 16, P('#dfe7ee' if on else '#0e1722'))            # rocker
    ry = lerp(y + 82, y + 36, eio(k)); rr(c, x + 40, ry, 64, 44, 10, P(TEAL if on else '#4a5a6b'))
    c.drawCircle(x + 190, y + 80, 52, P(TEAL_D if on else '#243445')); icon(c, ic, x + 190, y + 80, 62, '#ffffff' if on else '#5b7083')
    text(c, lab, x + 264, y + 102, 64, INK if on else '#5b7083', 900)


def k_moves(K):
    def f(c, t):
        ks = [clamp((t - SW0 - i * SWSTEP) / .14) for i in range(4)]; lit = sum(ks) / 4
        c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#12283a', '#0d3540']))
        c.drawRect(skia.Rect.MakeXYWH(0, 1250, W, H - 1250), P('#0a2029')); c.drawRect(skia.Rect.MakeXYWH(0, 1242, W, 12), P('#1d4a55'))
        c.drawCircle(830, 900, 380, P('#ffe7a0', 110 * lit, blur=120))
        doctor(c, 830, 1262, .92, 'resident', t, la=10, ra=-12 if lit < 1 else -150 + math.sin(t * 6) * 12, mood='happy')
        c.drawRect(skia.Rect.MakeWH(W, H), P('#03060a', 190 * (1 - lit)))   # the room is as bright as the switches
        brand_bar(c)
        title2(c, 'You’re the doctor.', 'Four moves.', 356, a=255 * ease(t / .3), size=104, sub_size=84)
        for i, (ic, lab) in enumerate(MOVES):
            a = ease((t - .15 - i * .1) / .3)
            if a <= 0: continue
            c.save(); c.translate((1 - a) * -700, 0); switch(c, 60, 540 + i * 180, ic, lab, ks[i]); c.restore()
        if lit >= 1:
            pill(c, 480, 1340, 'All four are yours.', GOLD, INK, 48, pop((t - SW0 - 3 * SWSTEP - .2) / .35))
    return f


def k_hidden(K):
    def f(c, t):
        dark(c, t, 40); brand_bar(c)
        title2(c, 'The diagnosis?', 'Still in the dark.', 356, a=255 * ease(t / .3), size=112, sub_size=88, shadow=0)
        ang = math.sin(t * 2.2) * 5   # an unlit bulb on a cord
        c.save(); c.translate(510, 500); c.rotate(ang)
        c.drawLine(0, 0, 0, 150, P('#2a3847', stroke=6)); rr(c, -22, 146, 44, 36, 8, P('#3a4a5c'))
        c.drawCircle(0, 228, 56, P('#16212e')); c.drawCircle(0, 228, 56, P('#3a4a5c', stroke=5))
        f_ = skia.Path(); f_.moveTo(-16, 244); f_.lineTo(-8, 212); f_.lineTo(0, 236); f_.lineTo(8, 212); f_.lineTo(16, 244); c.drawPath(f_, P('#3a4a5c', stroke=4))
        c.restore()
        k = ease((t - .15) / .4); c.save(); c.translate(0, (1 - k) * 120)
        rr(c, 60, 860, 900, 330, 44, P('#0f1a26', 255 * k)); rr(c, 60, 860, 900, 330, 44, P('#2a3847', 255 * k, stroke=5))
        text(c, 'DIAGNOSIS', 110, 936, 36, '#7d93a6', 900, a=255 * k)
        rr(c, 110, 976, 800, 160, 30, P('#070c12', 255 * k)); rr(c, 110, 976, 800, 160, 30, P('#2a3847', 255 * k, stroke=4))
        for j in range(3):
            p = .5 + .5 * math.sin(t * 5 - j * .9); text(c, '?', 360 + j * 150, 1094, 110, GOLD, 900, 'c', a=255 * k * (.35 + .65 * p))
        c.restore()
        if t > 1.3: pill(c, 510, 1320, 'Only you can switch it on.', '#ffffff', INK, 48, pop((t - 1.3) / .35))
    return f


def build(case_id):
    K, _ = case.build(case_id); first = K['name'].split()[0]
    return K, [(k_dark(K), D0), (k_lit(K), D1), (k_moves(K), D2), (k_hidden(K), D3), (cta2(f'{first} is waiting.', 'Take the case.'), D4)]


def script(K):
    first = K['name'].split()[0]; a, b, c_, e = D0, D0 + D1, D0 + D1 + D2, D0 + D1 + D2 + D3
    return [(0.1, K['quote'], 3.3), (a + .2, f"Lights on. {K['name']}, {K['age']}. {K['problem']}.", D1 - .5),
            (b + .15, "You're the doctor. Talk. Examine. Tests. Treat.", D2 - .4), (c_ + .2, 'The diagnosis? Still in the dark.', D3 - .4),
            (e + .15, f'{first} is waiting. Bedside Bay. Play free.', D4 - .3)]


def soundtrack(K, SC, wav):
    import sound
    a, b, c_, e = D0, D0 + D1, D0 + D1 + D2, D0 + D1 + D2 + D3; n = len(K['quote'].split())
    cues = [(W0 + i * WSTEP, 'tick') for i in range(n)] + [(ASK, 'pop'), (a - .5, 'riser'), (a, 'impact'), (a + .05, 'ding'), (a + 1.5, 'pop')]
    cues += [(b - .25, 'whoosh')] + [(b + SW0 + i * SWSTEP, 'tick') for i in range(4)] + [(b + SW0 + i * SWSTEP + .03, f'step:{i + 1}') for i in range(4)]
    cues += [(b + SW0 + 3 * SWSTEP + .2, 'ding'), (c_ - .1, 'tick'), (c_ + .05, 'beep'), (c_ + 1.3, 'pop'), (e - .9, 'riser'), (e, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=a, lift=b, cta=e, cues=cues, voice=script(K))


def comp(SC, i):
    def f(c, t):
        SC[i][0](c, t)
        if i == 1: flash(c, t, .5)
        elif i in (2, 4): flash(c, t, .14)
        elif i == 3 and t < .12: c.drawRect(skia.Rect.MakeWH(W, H), P('#000000', 255 * (1 - t / .12)))
    return f


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 1.5), (0, 3.9), (1, 0.1), (1, 3.5), (2, 0.9), (2, 2.1), (2, 3.9), (3, 2.8), (4, 3.0)]
        contact_sheet([frame(comp(SC, i), t) for i, t in pts], sys.argv[3], 5)
    elif sys.argv[2] == 'frame':
        save_jpg(frame(comp(SC, int(sys.argv[3])), float(sys.argv[4])), sys.argv[5])
    elif sys.argv[2] == 'phonemes':
        import sound
        for _, l, _ in script(K): print(l, '->', sound.phonemes(l))
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(SC, i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
