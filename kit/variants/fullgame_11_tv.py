"""Full Game variant 11 — "Done watching medical dramas?" The hook is a TV playing a hospital drama that gets switched
off ("Your turn."), then the screen fills with patients (163, and nobody tells you the diagnosis), the four moves as the
four buttons of the remote, the five ranks as an episode list starring Dr John Smith, and the four modes as the TV menu
with Career first. Music: upbeat.
Video: python3 fullgame_11_tv.py <out.mp4>          Preview: python3 fullgame_11_tv.py preview <sheet.jpg>"""
from common import *
import json
from case import card, chip, RED

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
OUT = ['intern', 'resident', 'surgeon', 'consultant', 'director']
TVX, TVY, TVW, TVH = 70, 560, 940, 620
SX, SY, SW, SH = TVX + 22, TVY + 22, TVW - 44, TVH - 44


def room(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#17132e', '#2b1f4d']))
    c.drawCircle(540, 860, 620, P('#5a7bff', 36, blur=150))
    c.drawRect(skia.Rect.MakeXYWH(0, 1254, W, H - 1254), P('#120f24'))
    scenes._ecg(c, 0, W, 1650, t, TEAL, a=70, amp=50, w=5)


def tv(c, screen, on=True):
    rr(c, 440, TVY + TVH - 10, 200, 70, 10, P('#0c0f15')); rr(c, 300, TVY + TVH + 50, 480, 24, 12, P('#0c0f15'))
    rr(c, TVX, TVY + 14, TVW, TVH, 36, P('#000000', 120, blur=30)); rr(c, TVX, TVY, TVW, TVH, 36, P('#1a1f29')); rr(c, TVX, TVY, TVW, TVH, 36, P('#3a4756', stroke=4))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(SX, SY, SW, SH), 18, 18), True)
    c.drawRect(skia.Rect.MakeXYWH(SX, SY, SW, SH), P('#05070b'))
    screen(c)
    c.restore()
    c.drawCircle(TVX + TVW - 40, TVY + TVH - 11, 5, P('#3ee08a' if on else RED))


def remote(c, cx, cy, sc, rot, pressed):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(sc, sc)
    rr(c, -80, -180 + 12, 160, 360, 44, P('#000000', 110, blur=18)); rr(c, -80, -180, 160, 360, 44, P('#25303d')); rr(c, -80, -180, 160, 360, 44, P('#3a4756', stroke=5))
    if pressed: c.drawCircle(0, -120, 54, P(RED, 120, blur=16))
    c.drawCircle(0, -120, 30, P(RED)); c.drawArc(skia.Rect.MakeXYWH(-13, -133, 26, 26), -60, 300, False, P('#ffffff', stroke=5)); c.drawLine(0, -138, 0, -120, P('#ffffff', stroke=5))
    for r in range(3):
        for q in range(3): c.drawCircle(-44 + q * 44, -40 + r * 50, 15, P('#55657a'))
    rr(c, -40, 116, 80, 30, 15, P(TEAL)); c.restore()


def popcorn(c, x, y):
    for i, (px, py) in enumerate(((20, -214), (70, -236), (120, -220), (168, -232), (44, -250), (100, -262), (150, -254), (88, -214), (190, -210), (10, -196))):
        c.drawCircle(x + px, y + py, 30, P('#fff3c4' if i % 2 else '#ffe9a0'))
    b = skia.Path(); b.moveTo(x - 10, y - 200); b.lineTo(x + 210, y - 200); b.lineTo(x + 176, y); b.lineTo(x + 24, y); b.close()
    c.drawPath(b, P('#ffffff')); c.save(); c.clipPath(b, doAntiAlias=True)
    for i in range(5): c.drawRect(skia.Rect.MakeXYWH(x - 10 + i * 48, y - 200, 24, 200), P(RED))
    c.restore()


def f_hook(c, t):
    room(c, t); brand_bar(c)
    title2(c, 'Done watching', 'medical dramas?', 372, size=112, sub_size=100)
    off = t >= 2.3
    def screen(c):
        if off:
            k = clamp((t - 2.3) / .22); hh = max(4, SH * (1 - k)); ww = SW if k < 1 else SW * (1 - clamp((t - 2.52) / .15))
            if ww > 6: rr(c, SX + (SW - ww) / 2, SY + (SH - hh) / 2, ww, hh, 2, P('#ffffff', 255 if k >= 1 else 200))
            return
        c.drawRect(skia.Rect.MakeXYWH(SX, SY, SW, SH), grad(0, SY, 0, SY + SH, ['#17506a', '#07202c']))
        c.drawOval(skia.Rect.MakeXYWH(SX + 130, SY + 20, 380, 90), P('#c9f6fb', 150, blur=30)); c.drawOval(skia.Rect.MakeXYWH(SX + 190, SY + 34, 260, 54), P('#f3fdff'))
        scenes._ecg(c, SX + 500, SX + SW - 30, SY + 210, t, '#3ee08a', amp=44, w=6, speed=320, period=170)
        rr(c, SX + 490, SY + 110, SW - 520, 190, 16, P('#3ee08a', 60, stroke=5))
        doctor(c, SX + 320, SY + SH + 120, .66, 'surgeon', t, la=-30 + math.sin(t * 9) * 8, ra=34 - math.sin(t * 9 + 1) * 8)
        c.drawRect(skia.Rect.MakeXYWH(SX, SY, SW, 44), P('#000000')); c.drawRect(skia.Rect.MakeXYWH(SX, SY + SH - 44, SW, 44), P('#000000'))
        rr(c, SX + 24, SY + 60, 218, 56, 12, P('#000000', 170)); text(c, 'S12  ·  E247', SX + 133, SY + 100, 32, '#ffffff', 900, 'c')
        sub = '“We’re losing him!”'; text(c, sub, SX + SW / 2, SY + SH - 76, 50, '#ffe66b', 900, 'c', shadow=.9)
        if t > .9:
            n = 3 - min(2, int((t - .9) / .47)); k = pop((t - .9) / .3)
            c.save(); c.translate(SX + SW - 190, SY + 380); c.scale(k, k)
            rr(c, -160, -52, 320, 104, 18, P('#ffffff', 235)); text(c, f'Next episode in {n}', 0, 14, 36, INK, 900, 'c'); c.restore()
    tv(c, screen, on=not off)
    if t > 2.6: pill(c, 540, SY + SH / 2, 'Your turn.', GOLD, INK, 96, pop((t - 2.6) / .35))
    popcorn(c, 110, 1540)
    remote(c, 800, 1400, .78, 18, 2.2 < t < 2.6)


def f_patients(c, t):
    room(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Your turn.', '163 patients waiting.', 372, a=255 * k0, dy=(1 - k0) * 30, size=112, sub_size=88)
    def screen(c):
        c.drawRect(skia.Rect.MakeXYWH(SX, SY, SW, SH), grad(0, SY, 0, SY + SH, ['#0f2a43', '#0d3540']))
        tw_, th = (SW - 5 * 16) / 4, (SH - 84 - 4 * 14) / 3
        for i in range(12):
            a0 = .15 + i * .11
            if t < a0: continue
            K = CASES[(i * 5 + 3) % len(CASES)]; x = SX + 16 + (i % 4) * (tw_ + 16); y = SY + 14 + (i // 4) * (th + 14)
            rr(c, x, y, tw_, th, 16, P('#17405a')); face(c, x + tw_ / 2, y + th / 2, 62 * pop((t - a0) / .3), K['skin'], K['hair'], K['style'], 'pain', t + i)
        n = int(lerp(12, 163, eio((t - 1.5) / .8))) if t > 1.5 else min(12, int((t - .15) / .11) + 1) if t > .15 else 0
        c.drawRect(skia.Rect.MakeXYWH(SX, SY + SH - 84, SW, 84), P('#05070b', 235))
        c.drawCircle(SX + 40, SY + SH - 42, 11, P(RED, 255 if (t * 2) % 1 < .6 else 90)); text(c, 'NOW WAITING', SX + 64, SY + SH - 28, 34, '#bfe9e4', 900)
        text(c, f'{n} PATIENTS', SX + SW - 30, SY + SH - 24, 48, GOLD, 900, 'r')
    tv(c, screen)
    if t > 1.9:
        k = pop((t - 1.9) / .4)
        pill(c, 410, 1370, 'Nobody tells you', '#ffffff', INK, 48, k); pill(c, 410, 1466, 'the diagnosis.', GOLD, INK, 48, k)
    doctor(c, 900, 1570, .5, 'intern', t, la=10, ra=-150 + math.sin(t * 6) * 12, mood='ok')


MOVES = [('talk', 'Talk', 'Get the story'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Make the call')]


def f_moves(c, t):
    room(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Four moves.', 'No script.', 372, a=255 * k0, dy=(1 - k0) * 30, size=112, sub_size=100)
    x, y, w, h = 170, 540, 740, 990
    rr(c, x, y + 16, w, h, 80, P('#000000', 120, blur=30)); rr(c, x, y, w, h, 80, P('#25303d')); rr(c, x, y, w, h, 80, P('#3a4756', stroke=6))
    c.drawCircle(x + w / 2, y + 52, 13, P(RED, 255 if (t * 3) % 1 < .5 else 90))
    for i, (ic, lab, sub) in enumerate(MOVES):
        ti = .35 + i * .5; on = t >= ti; press = on and t - ti < .22; by = y + 100 + i * 200
        c.save(); c.translate(x + w / 2, by + 86); s = .95 if press else 1; c.scale(s, s)
        if press: rr(c, -330, -96, 660, 192, 50, P(GOLD, 200, blur=20))
        rr(c, -320, -86 + 8, 640, 172, 44, P('#000000', 90)); rr(c, -320, -86, 640, 172, 44, P(TEAL if on else '#3a4756'))
        c.drawCircle(-226, 0, 58, P('#ffffff' if on else '#55657a')); icon(c, ic, -226, 0, 70, TEAL_D if on else '#8a9bab')
        text(c, lab, -140, 6, 64, '#ffffff' if on else '#8a9bab', 900); text(c, sub, -140, 52, 32, '#d9f3ef' if on else '#6b7b8c', 700)
        text(c, str(i + 1), 280, 22, 64, '#ffffff' if on else '#55657a', 900, 'r', a=150); c.restore()
    logo(c, x + w / 2 - 26, y + h - 76, 52)


def f_ranks(c, t):
    room(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Five ranks to climb.', 'Intern to ED Director.', 372, a=255 * k0, dy=(1 - k0) * 30, size=100, sub_size=84)
    cur = min(4, int(max(0, t - .3) / .5)); lt = max(0, t - .3) - cur * .5
    for i in range(5):
        y = 548 + i * 178; done = i < cur; here = i == cur; lit = i <= cur
        k = pop(lt / .3) if (here and t >= .3) else 1
        c.save(); c.translate(540, y + 80); c.scale(k, k); c.translate(-540, -(y + 80))
        card(c, 60, y, 960, 160, 32, col=(GOLD if i == 4 else '#ffffff') if lit else '#2a2550')
        if here: rr(c, 60, y, 960, 160, 32, P(TEAL if i < 4 else '#ffffff', stroke=10))
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(76, y + 12, 200, 136), 22, 22), True)
        c.drawRect(skia.Rect.MakeXYWH(76, y + 12, 200, 136), grad(0, y, 0, y + 160, ['#dff1f4', '#9fd3db'] if lit else ['#3a3566', '#2f2a57']))
        doctor(c, 176, y + 308, .44, OUT[i], t, la=8, ra=-8, mood='tired' if i == 0 else 'happy')
        if not lit: c.drawRect(skia.Rect.MakeXYWH(76, y + 12, 200, 136), P('#17132e', 170))
        c.restore()
        text(c, f'RANK {i + 1}', 306, y + 60, 28, ('#7a5a10' if i == 4 else '#8a9bab') if lit else '#6f6a9c', 900)
        text(c, RANKS[i], 304, y + 124, 64, INK if lit else '#8f8ac0', 900)
        bx, by = 940, y + 80
        if done: c.drawCircle(bx, by, 40, P(TEAL)); check(c, bx, by + 2, 18)
        elif here:
            c.drawCircle(bx, by, 40, P(INK)); p = skia.Path(); p.moveTo(bx - 12, by - 18); p.lineTo(bx + 20, by); p.lineTo(bx - 12, by + 18); p.close(); c.drawPath(p, P('#ffffff'))
        else: c.drawCircle(bx, by, 40, P('#3a3566'))
        c.restore()
    pill(c, 540, 1500, 'Starring: Dr John Smith', '#ffffff', INK, 40)


MODES = [('career', 'Career'), ('shift', 'Quick shift'), ('practice', 'Case practice'), ('firstaid', 'First aid')]


def f_modes(c, t):
    room(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Four ways to play.', 'Start in Career.', 372, a=255 * k0, dy=(1 - k0) * 30, size=104, sub_size=92)
    def screen(c):
        c.drawRect(skia.Rect.MakeXYWH(SX, SY, SW, SH), grad(0, SY, 0, SY + SH, ['#0f2a43', '#0d3540']))
        tw_, th = (SW - 3 * 24) / 2, (SH - 3 * 24) / 2
        for i, (ic, lab) in enumerate(MODES):
            a0 = .2 + i * .25
            if t < a0: continue
            x = SX + 24 + (i % 2) * (tw_ + 24); y = SY + 24 + (i // 2) * (th + 24); k = pop((t - a0) / .35); first = i == 0
            c.save(); c.translate(x + tw_ / 2, y + th / 2); c.scale(k, k); c.translate(-tw_ / 2, -th / 2)
            rr(c, 0, 0, tw_, th, 24, P(GOLD if first else '#17405a'))
            if first and t > 1.3: rr(c, 0, 0, tw_, th, 24, P('#ffffff', 255 * (.6 + .4 * math.sin(t * 8)), stroke=10))
            c.drawCircle(84, 96, 58, P(INK if first else (RED if ic == 'firstaid' else TEAL))); icon(c, ic, 84, 96, 70)
            text(c, f'MODE {i + 1}', 164, 78, 26, '#7a5a10' if first else '#8fb7c9', 900)
            text(c, lab, 164, 132, fit(lab, 54, tw_ - 180), INK if first else '#ffffff', 900)
            if first:
                w = tw('START HERE', 26, 900) + 40; rr(c, 24, th - 70, w, 50, 25, P(INK)); text(c, 'START HERE', 24 + w / 2, th - 36, 26, '#ffffff', 900, 'c')
            c.restore()
    tv(c, screen)
    chip(c, 60, 1400, 'DR JOHN SMITH  ·  INTERN, DAY 1', '#ffffff', INK, 30, dot=TEAL)
    doctor(c, 900, 1570, .5, 'intern', t, la=10, ra=-150 + math.sin(t * 6) * 12, mood='happy')


SC = [(f_hook, 3.2), (f_patients, 3.4), (f_moves, 3.0), (f_ranks, 3.2), (f_modes, 3.0), (cta2('Stop watching.', 'Start treating.'), 3.4)]

VOICE = [(0.15, 'Done watching medical dramas?', 2.9), (3.4, 'Your turn. One hundred and sixty-three patients.', 3.1),
         (6.8, 'Four moves. No script.', 2.7), (9.8, 'Five ranks. Intern to E D Director.', 2.9),
         (13.0, 'Four ways to play. Start in Career.', 2.7), (16.1, 'Bedside Bay. Play free.', 2.9)]


def soundtrack(wav):
    import sound
    cues = [(.05, 'whoosh')] + [(.9 + i * .47, 'beep') for i in range(3)] + [(2.3, 'impact'), (2.6, 'pop'), (2.95, 'whoosh')]
    cues += [(3.35 + i * .11, 'tick') for i in range(12)] + [(4.7, 'riser'), (5.5, 'ding'), (5.1, 'pop'), (6.35, 'whoosh')]
    cues += [(6.95 + i * .5, 'pop') for i in range(4)] + [(7.0 + i * .5, 'tick') for i in range(4)] + [(9.35, 'whoosh')]
    cues += [(9.9 + i * .5, f'step:{i}') for i in range(5)] + [(11.95, 'cash'), (12.55, 'whoosh')]
    cues += [(13.0 + i * .25, 'pop') for i in range(4)] + [(14.1, 'ding'), (14.6, 'riser'), (15.8, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=3.2, lift=9.6, cta=15.8, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .16)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 1.6), (0, 2.4), (0, 3.0), (1, 0.8), (1, 3.2), (2, 1.0), (2, 2.8), (3, 0.6), (3, 3.0), (4, 2.8), (5, 3.0)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 6)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
