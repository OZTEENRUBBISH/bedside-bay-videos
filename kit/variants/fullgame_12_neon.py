"""Full Game variant 12 — "Your ER just opened." The whole game as neon signs on a brick wall at night: an ER / OPEN sign
flickers on, a neon counter runs up to 163 patients, the four moves light up as a stack of signs, the five ranks light
rung by rung from Intern to ED Director while Dr John Smith's outfit upgrades, the four modes glow with Career marked
START HERE, then the end card. Only facts listed in CLAUDE.md.
Music: tense.
Video: python3 fullgame_12_neon.py <out.mp4>          Preview: python3 fullgame_12_neon.py preview <sheet.jpg>"""
from common import *
import json
from case import chip, TRI
from fullgame_02 import MODES, OUT

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
RED, PINK, CYAN, AMB = '#ff4d5e', '#ff5fa2', '#3fe0d0', '#ffc247'
OFF = '#3a3350'
_wall = None


def wall(c, t):
    """Dark brick wall, drawn once and reused."""
    global _wall
    if _wall is None:
        s = new_surface(); k = s.getCanvas()
        k.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#1a1230', '#0d0a1c']))
        for r in range(40):
            y = r * 50; off = 65 if r % 2 else 0
            for i in range(-1, 9):
                rr(k, i * 130 + off + 3, y + 3, 124, 44, 5, P('#ffffff', 5 + (3 if (i * 7 + r * 3) % 5 == 0 else 0)))
        k.drawRect(skia.Rect.MakeWH(W, H), grad(0, 1100, 0, H, ['#0d0a1c', '#0d0a1c'], 0))
        _wall = s.makeImageSnapshot()
    c.drawImage(_wall, 0, 0)
    c.drawRect(skia.Rect.MakeXYWH(0, 1610, W, H - 1610), P('#07060f')); c.drawRect(skia.Rect.MakeXYWH(0, 1606, W, 6), P('#2a2440'))


def lit(t, t0, d=.4):
    """0 before t0, a short flicker, then on (with a faint hum)."""
    if t < t0: return 0.0
    x = t - t0
    if x < d: return [1, .15, .9, .25, 1, .1, 1, 1][min(7, int(x / d * 8))]
    return .94 + .06 * math.sin(t * 31)


def neon(c, s, x, y, size, col, k=1.0, align='c', wt=900):
    f = font(size, wt); w = f.measureText(s)
    x0 = x - w / 2 if align == 'c' else (x - w if align == 'r' else x)
    if k < .5: c.drawString(s, x0, y, f, P(OFF))
    if k > 0:
        c.drawString(s, x0, y, f, P(col, 150 * k, blur=max(14, size * .2))); c.drawString(s, x0, y, f, P(col, 255 * k, blur=6))
        c.drawString(s, x0, y, f, P('#ffffff', 235 * k)); c.drawString(s, x0, y, f, P(col, 70 * k))
    return w


def tube(c, x, y, w, h, r, col, k=1.0, sw=10):
    if k < .5: rr(c, x, y, w, h, r, P(OFF, stroke=sw))
    if k > 0:
        rr(c, x, y, w, h, r, P(col, 130 * k, stroke=sw * 2.4, blur=22)); rr(c, x, y, w, h, r, P(col, 255 * k, stroke=sw, blur=4))
        rr(c, x, y, w, h, r, P('#ffffff', 220 * k, stroke=sw * .45))


def nicon(c, kind, cx, cy, s, col, k=1.0):
    if k < .5: icon(c, kind, cx, cy, s, OFF)
    if k > 0:
        c.drawCircle(cx, cy, s * .6, P(col, 70 * k, blur=30)); icon(c, kind, cx, cy, s, col if k > .5 else OFF); icon(c, kind, cx, cy, s * .999, '#ffffff') if False else None


def glow_floor(c, cx, col, a=60):
    c.drawOval(skia.Rect.MakeXYWH(cx - 260, 1560, 520, 90), P(col, a, blur=40))


def f_hook(c, t):
    wall(c, t); brand_bar(c)
    title2(c, 'Your ER', 'just opened.', 372, size=120, sub_size=104)
    k1 = lit(t + 1, 0); k2 = lit(t, .25); k3 = lit(t, .7)
    c.drawLine(300, 470, 300, 560, P('#06050c', stroke=8)); c.drawLine(780, 470, 780, 560, P('#06050c', stroke=8))
    rr(c, 150, 560, 780, 560, 50, P('#0a0814', 235)); tube(c, 150, 560, 780, 560, 50, CYAN, k1)
    neon(c, 'ER', 540, 860, 330, RED, k2)
    neon(c, 'OPEN', 540, 1060, 170, CYAN, k1)
    glow_floor(c, 790, CYAN, 70 * k1)
    doctor(c, 790, 1590, .72, 'intern', t, la=10, ra=-150 + math.sin(t * 6) * 12 if t > 1.2 else -12, mood='happy' if t > 1.2 else 'ok')
    if t > 1.1:
        c.save(); c.translate(320, 1400); c.scale(pop((t - 1.1) / .35), pop((t - 1.1) / .35)); c.translate(-320, -1400)
        chip(c, 60, 1372, 'DR JOHN SMITH  ·  INTERN, DAY 1', '#ffffff', INK, 30, dot=TEAL); c.restore()
    if t > 1.6: neon(c, 'You’re the doctor.', 60, 1520, 54, AMB, lit(t, 1.6), 'l')


def f_patients(c, t):
    wall(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, '163 patients.', 'All waiting for you.', 372, a=255 * k0, dy=(1 - k0) * 30, size=112, sub_size=84)
    n = int(round(163 * eio((t - .15) / 1.5)))
    rr(c, 110, 540, 860, 470, 50, P('#0a0814', 235)); tube(c, 110, 540, 860, 470, 50, PINK, lit(t, 0, .25))
    neon(c, str(n), 540, 850, 330, RED, 1.0 if n < 163 else lit(t, 1.65, .3))
    neon(c, 'PATIENTS WAITING', 540, 960, 66, CYAN, lit(t, .2))
    for i in range(5):
        a0 = .5 + i * .18
        if t < a0: continue
        K = CASES[(i * 5 + 2) % len(CASES)]; x = 140 + i * 200; k = pop((t - a0) / .35)
        c.drawCircle(x, 1200, 100 * k, P(TRI[K['triage']], 110, blur=26))
        face(c, x, 1200, 86 * k, K['skin'], K['hair'], K['style'], 'pain' if i % 2 == 0 else 'ok', t + i)
        c.drawCircle(x + 62, 1132, 30 * k, P(TRI[K['triage']])); text(c, str(K['triage']), x + 62, 1146, 38 * k, '#ffffff', 900, 'c')
    if t > 1.7: neon(c, 'The diagnosis? Hidden.', 540, 1420, 70, AMB, lit(t, 1.7))
    chip(c, 60, 1500, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)


SIGNS = [('talk', 'TALK', CYAN), ('examine', 'EXAMINE', AMB), ('tests', 'TESTS', PINK), ('treat', 'TREAT', RED)]


def f_moves(c, t):
    wall(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Four moves.', 'Every single patient.', 372, a=255 * k0, dy=(1 - k0) * 30, size=112, sub_size=84)
    c.drawRect(skia.Rect.MakeXYWH(150, 520, 14, 900), P('#06050c')); c.drawRect(skia.Rect.MakeXYWH(916, 520, 14, 900), P('#06050c'))
    for i, (ic, lab, col) in enumerate(SIGNS):
        y = 540 + i * 222; k = lit(t, .3 + i * .5)
        rr(c, 110, y, 860, 190, 40, P('#0a0814', 235)); tube(c, 110, y, 860, 190, 40, col, k)
        nicon(c, ic, 232, y + 95, 120, col, k)
        text(c, str(i + 1), 900, y + 62, 40, col if k > .5 else OFF, 900, 'c')
        neon(c, lab, 590, y + 134, fit(lab, 124, 520), col, k)
    chip(c, 60, 1470, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)


def f_ranks(c, t):
    wall(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Five ranks.', 'Intern to ED Director.', 372, a=255 * k0, dy=(1 - k0) * 30, size=112, sub_size=84)
    cur = 0
    c.drawRect(skia.Rect.MakeXYWH(92, 560, 12, 900), P('#06050c')); c.drawRect(skia.Rect.MakeXYWH(596, 560, 12, 900), P('#06050c'))
    for i, rk in enumerate(RANKS):
        y = 1320 - i * 190; a0 = .3 + i * .5; k = lit(t, a0); col = AMB if i == 4 else CYAN
        if t >= a0: cur = i
        rr(c, 60, y, 580, 150, 34, P('#0a0814', 235)); tube(c, 60, y, 580, 150, 34, col, k)
        text(c, str(i + 1), 112, y + 96, 54, col if k > .5 else OFF, 900, 'c')
        neon(c, rk.upper(), 380, y + 100, fit(rk.upper(), 70, 420), col, k)
    col = AMB if cur == 4 else CYAN
    c.drawCircle(860, 1100, 230, P(col, 46, blur=80)); glow_floor(c, 860, col, 70)
    doctor(c, 860, 1590, .78, OUT[cur], t, la=10, ra=-150 + math.sin(t * 6) * 12 if cur == 4 else -12, mood='tired' if cur == 0 else 'happy')
    pill(c, 860, 1010, RANKS[cur], GOLD if cur == 4 else '#ffffff', INK, 38, pop((t - (.3 + cur * .5)) / .3))


MCOL = [AMB, CYAN, PINK, RED]


def f_modes(c, t):
    wall(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Four ways to play.', 'Start in Career.', 372, a=255 * k0, dy=(1 - k0) * 30, size=104, sub_size=92)
    for i, (ic, lab) in enumerate(MODES):
        x = 70 + (i % 2) * 490; y = 550 + (i // 2) * 380; k = lit(t, .25 + i * .3); col = MCOL[i]
        rr(c, x, y, 450, 340, 44, P('#0a0814', 235)); tube(c, x, y, 450, 340, 44, col, k)
        nicon(c, ic, x + 225, y + 130, 150, col, k)
        neon(c, lab.upper(), x + 225, y + 290, fit(lab.upper(), 62, 400), col, k)
    if t > 1.5 and (t * 2.5) % 1 < .7: pill(c, 295, 550, 'START HERE', GOLD, INK, 34)
    glow_floor(c, 540, AMB, 60)
    doctor(c, 540, 1596, .5, 'intern', t, la=10, ra=-150 + math.sin(t * 6) * 12, mood='happy')


SC = [(f_hook, 3.0), (f_patients, 3.2), (f_moves, 3.2), (f_ranks, 3.4), (f_modes, 3.0), (cta2('Your ER is open.', 'Clock in as Dr John Smith.'), 3.4)]

VOICE = [(0.15, 'Your E.R. just opened.', 2.7), (3.2, 'One hundred and sixty-three patients. All waiting.', 3.0),
         (6.6, 'Four moves. Every patient.', 2.8), (9.8, 'Five ranks. Intern to E.D. Director.', 3.1),
         (13.2, 'Four ways to play. Start in Career.', 2.7), (16.3, 'Bedside Bay. Play free.', 2.7)]


def soundtrack(wav):
    import sound
    cues = [(.02, 'beep'), (.25, 'tick'), (.32, 'tick'), (.42, 'tick'), (.65, 'impact'), (1.1, 'pop'), (1.6, 'beep'), (2.8, 'whoosh')]
    cues += [(3.25 + i * .1, 'tick') for i in range(14)] + [(4.85, 'impact'), (4.9, 'ding'), (6.0, 'whoosh')]
    cues += [(6.5 + i * .5, 'beep') for i in range(4)] + [(6.55 + i * .5, 'pop') for i in range(4)] + [(9.2, 'whoosh')]
    cues += [(9.9 + i * .5, f'step:{i}') for i in range(5)] + [(11.95, 'cash'), (12.4, 'whoosh')]
    cues += [(12.85 + i * .3, 'beep') for i in range(4)] + [(14.3, 'ding'), (14.7, 'riser'), (15.8, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=3.0, lift=9.4, cta=15.8, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .12)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 0.5), (0, 2.6), (1, 0.6), (1, 3.0), (2, 1.0), (2, 3.0), (3, 1.0), (3, 3.2), (4, 0.6), (4, 2.7), (5, 3.0)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 6)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
