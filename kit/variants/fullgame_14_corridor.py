"""Full Game variant 14 — "How far would you get in the ER?" The whole game as one bright hospital corridor seen from the
side: Dr John Smith starts as an Intern on the START line and runs in place while the corridor scrolls past the game's
numbers, each with a huge number in the header: 163 patients (curtained bays flying past, the number racing up),
4 moves (four doors: Talk, Examine, Tests, Treat), 5 ranks (five doors, his outfit upgrades at each, he stops at the
gold ED Director door), 4 ways to play (four hanging signs, Career marked START HERE), then the end card.
Only facts listed in CLAUDE.md.
Music: upbeat.
Video: python3 fullgame_14_corridor.py <out.mp4>          Preview: python3 fullgame_14_corridor.py preview <sheet.jpg>"""
from common import *
import json, lib
from case import TRI
from fullgame_02 import MODES, OUT

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
CEIL, FLOOR, FOOT, DX, DSC = 560, 1400, 1500, 300, .8
WALL, WALL2, TRIM, MINT = '#e9f2f3', '#d6e6e9', '#9fb6bf', '#bfe9e4'
LEGS = {'intern': '#7aa9a3', 'resident': '#128778', 'surgeon': '#277c89', 'consultant': '#33475b', 'director': '#1c2530'}
SHOE = {'intern': '#c9c2b6', 'director': '#111111'}


def corridor(c, off):
    """Side view of the corridor, scrolled left by off pixels: navy header, wall with lights and handrail, tiled floor."""
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, CEIL), grad(0, 0, W, CEIL, [NAVY, '#0e4b55']))
    c.drawCircle(540, 380, 420, P(TEAL, 26, blur=120))
    c.drawRect(skia.Rect.MakeXYWH(0, CEIL, W, FLOOR - CEIL), grad(0, CEIL, 0, FLOOR, [WALL, WALL2]))
    c.drawRect(skia.Rect.MakeXYWH(0, CEIL, W, 26), P('#b7c9cf'))
    x = -(off % 540) - 100
    while x < W + 200:  # ceiling lights
        rr(c, x, CEIL + 4, 240, 22, 8, P('#ffffff')); c.drawOval(skia.Rect.MakeXYWH(x - 60, CEIL, 360, 150), P('#ffffff', 120, blur=40)); x += 540
    c.drawRect(skia.Rect.MakeXYWH(0, 1196, W, 22), P(TEAL, 150)); c.drawRect(skia.Rect.MakeXYWH(0, 1218, W, 6), P(TEAL_D, 110))
    c.drawRect(skia.Rect.MakeXYWH(0, FLOOR - 34, W, 34), P(TRIM))
    c.drawRect(skia.Rect.MakeXYWH(0, FLOOR, W, H - FLOOR), grad(0, FLOOR, 0, H, ['#c3d5da', '#8eaab4']))
    for y, a in ((FLOOR + 70, 60), (FLOOR + 190, 70), (FLOOR + 360, 80)): c.drawLine(0, y, W, y, P('#ffffff', a, stroke=4, cap=False))
    x = -(off % 220) - 880
    while x < W + 900:  # tile joints, fanned out for depth
        c.drawLine(x, FLOOR, 540 + (x - 540) * 1.7, H, P('#ffffff', 70, stroke=4, cap=False)); x += 220
    c.drawRect(skia.Rect.MakeXYWH(0, FLOOR, W, 10), P('#000000', 26))


def runner(c, t, outfit, k=1.0, mood='ok', ra=None, cx=DX):
    """Dr John Smith jogging in place (k = 0 standing .. 1 running). The kit doctor from the waist up, own swinging legs."""
    ph = t * 11.5; sw = math.sin(ph) * 27 * k; bounce = -abs(math.sin(ph)) * 16 * k
    c.save(); c.translate(cx, FOOT); c.scale(DSC, DSC)
    c.drawOval(skia.Rect.MakeXYWH(-130, -14, 260, 34), P('#000000', 60, blur=10))
    for sx, a in ((-36, sw), (36, -sw)):
        c.save(); c.translate(sx, -200 + bounce); c.rotate(a)
        rr(c, -27, 0, 54, 194 - bounce, 22, P(LEGS[outfit]))
        c.drawOval(skia.Rect.MakeXYWH(-30, 174 - bounce, 78, 34), P(SHOE.get(outfit, '#e9edf1'))); c.restore()
    c.restore()
    c.save(); c.rotate(3.5 * k, cx, FOOT - 190 * DSC)
    c.clipRect(skia.Rect.MakeLTRB(0, 0, W + 400, FOOT + (bounce - 176) * DSC))
    doctor(c, cx, FOOT + bounce * DSC, DSC, outfit, t, la=12 + sw * 1.1, ra=(-12 + sw * 1.1) if ra is None else ra, mood=mood)
    c.restore()


def bignum(c, num, label, sub, t, size=190):
    """Header: a huge gold number, a white label and a small line under it."""
    k = pop(t / .3); lw = tw(label, 96, 900); nw = tw(num, size, 900); tot = nw + 26 + lw; x0 = (W - tot) / 2
    c.save(); c.translate(x0 + nw / 2, 400); c.scale(k, k)
    text(c, num, 0, 46, size, GOLD, 900, 'c', shadow=.35); c.restore()
    a = 255 * ease(t / .3)
    text(c, label, x0 + nw + 26, 446, 96, '#ffffff', 900, a=a, shadow=.35)
    text(c, sub, W / 2, 526, fit(sub, 50, 960, 800), MINT, 800, 'c', a=255 * ease((t - .25) / .3))


def plate(c, cx, y, w, h, label, bgc='#ffffff', fg=INK, num=None, border=None, size=54):
    rr(c, cx - w / 2, y + 6, w, h, 20, P('#000000', 50, blur=10)); rr(c, cx - w / 2, y, w, h, 20, P(bgc))
    if border: rr(c, cx - w / 2 + 4, y + 4, w - 8, h - 8, 16, P(border, stroke=6))
    if num:
        c.drawCircle(cx - w / 2 + 46, y + h / 2, 28, P(fg)); text(c, num, cx - w / 2 + 46, y + h / 2 + 15, 40, bgc, 900, 'c')
        s = fit(label, size, w - 110); text(c, label, cx + 34, y + h / 2 + s * .35, s, fg, 900, 'c')
    else:
        s = fit(label, size, w - 40); text(c, label, cx, y + h / 2 + s * .35, s, fg, 900, 'c')


def door(c, cx, col, on=1.0, ic=None, gold=False):
    """A door on the back wall, 280 wide. on = 0..1 lights it up as the doctor reaches it."""
    fr = GOLD if gold else '#8ea5ae'
    rr(c, cx - 156, 770, 312, FLOOR - 770 - 30, 14, P(fr)); c.drawRect(skia.Rect.MakeXYWH(cx - 156, FLOOR - 60, 312, 26), P(fr))
    leaf = col if on > .5 else '#c3d2d8'
    c.drawRect(skia.Rect.MakeXYWH(cx - 140, 786, 280, FLOOR - 786 - 34), P(leaf))
    c.drawRect(skia.Rect.MakeXYWH(cx - 140, 786, 280, FLOOR - 786 - 34), grad(cx - 140, 0, cx + 140, 0, ['#ffffff', '#000000'], 28))
    rr(c, cx - 86, 830, 172, 190, 16, P('#0f2a43', 215)); rr(c, cx - 86, 830, 172, 190, 16, P('#ffffff', 150, stroke=5))
    c.drawLine(cx - 60, 990, cx - 10, 850, P('#ffffff', 50, stroke=14))
    if ic: icon(c, ic, cx, 925, 110, '#ffffff')
    rr(c, cx + 84, 1110, 34, 70, 10, P('#f4f7f8')); c.drawCircle(cx + 101, 1132, 9, P('#7b8a97'))
    c.drawRect(skia.Rect.MakeXYWH(cx - 140, FLOOR - 130, 280, 62), P('#000000', 30))
    if on > 0 and on < 1: c.drawRect(skia.Rect.MakeXYWH(cx - 140, 786, 280, FLOOR - 786 - 34), P('#ffffff', 200 * (1 - on)))


def f_hook(c, t):
    off = 330 * max(0, t - 1.45) ** 2
    corridor(c, off); brand_bar(c)
    text(c, 'How far would you get', W / 2, 356, 88, '#ffffff', 900, 'c', shadow=.35)
    text(c, 'in the ER?', W / 2, 496, 150, GOLD, 900, 'c', shadow=.35)
    for i in range(4): door(c, 760 + i * 400 - off, '#c3d2d8', 0)
    # direction sign on the wall
    sx = 700 - off * 1.0
    rr(c, sx - 250, 628 + 6, 500, 104, 22, P('#000000', 50, blur=10)); rr(c, sx - 250, 628, 500, 104, 22, P(INK))
    text(c, 'ED DIRECTOR', sx - 216, 700, 50, '#ffffff', 900)
    ax = sx + 180 + (t * 2 % 1) * 14
    arr = skia.Path(); arr.moveTo(ax - 40, 680); arr.lineTo(ax + 20, 680); arr.moveTo(ax - 4, 656); arr.lineTo(ax + 22, 680); arr.lineTo(ax - 4, 704)
    c.drawPath(arr, P(GOLD, stroke=12))
    # START line painted on the floor
    lx = DX + 150 - off * 1.25
    ln = skia.Path(); ln.moveTo(lx, FLOOR + 6); ln.lineTo(lx + 60, FLOOR + 6); ln.lineTo(lx + 60 + 190, H); ln.lineTo(lx + 190 - 60, H); ln.close(); c.drawPath(ln, P(GOLD, 235))
    text(c, 'START', lx - 270, FLOOR + 226, 84, '#ffffff', 900, a=235)
    k = eio((t - 1.3) / .5)
    runner(c, t, 'intern', k, 'tired' if t < 1.1 else 'ok')
    kp = pop((t - .25) / .35)
    if t > .25: pill(c, DX + 16, 950, 'Dr John Smith · Intern', '#ffffff', INK, 36, kp)


def bay(c, x, i, t):
    K = CASES[(i * 7 + 3) % len(CASES)]; col = [TEAL, '#3a8fd6', '#f08c2e', '#8a6fd1'][i % 4]
    rr(c, x - 160, 700, 320, FLOOR - 734, 10, P('#cfdfe3'))
    c.drawRect(skia.Rect.MakeXYWH(x - 160, 690, 320, 16), P('#7b8a97'))  # curtain rail
    # bed and patient
    rr(c, x - 120, 1120, 26, 250, 8, P('#8ea5ae')); rr(c, x - 110, 1190, 250, 120, 22, P('#ffffff')); rr(c, x - 60, 1210, 200, 100, 20, P(col, 120))
    c.drawRect(skia.Rect.MakeXYWH(x - 104, 1310, 14, 56), P('#8ea5ae')); c.drawRect(skia.Rect.MakeXYWH(x + 116, 1310, 14, 56), P('#8ea5ae'))
    face(c, x - 20, 1060, 104, K['skin'], K['hair'], K['style'], 'pain' if i % 2 == 0 else 'ok', t + i)
    # half-open curtain
    for j in range(3):
        cxx = x + 74 + j * 30
        rr(c, cxx, 704, 34, FLOOR - 760, 14, P(col, 255)); c.drawRect(skia.Rect.MakeXYWH(cxx + 22, 712, 8, FLOOR - 776), P('#000000', 36))


def f_patients(c, t):
    off = 432 + 960 * t
    corridor(c, off)
    n0 = int(off // 360)
    for i in range(n0 - 1, n0 + 5): bay(c, i * 360 - off + 240, i, t)
    brand_bar(c)
    n = max(1, int(round(163 * eio(t / 1.75))))
    k = pop(t / .3); lw = tw('patients', 96, 900); nw = tw('163', 190, 900); x0 = (W - nw - 26 - lw) / 2
    bump = 1 + .1 * clamp(1 - (t - 1.75) / .25) if t >= 1.75 else 1
    c.save(); c.translate(x0 + nw, 446); c.scale(k * bump, k * bump); text(c, str(n), 0, 0, 190, GOLD, 900, 'r', shadow=.35); c.restore()
    text(c, 'patients', x0 + nw + 26, 446, 96, '#ffffff', 900, a=255 * ease(t / .3), shadow=.35)
    text(c, 'One doctor. You.', W / 2, 526, 50, MINT, 800, 'c', a=255 * ease((t - 1.75) / .3))
    runner(c, t, 'intern', 1, 'ok')


MOVES = [('talk', 'Talk', TEAL), ('examine', 'Examine', '#3a8fd6'), ('tests', 'Tests', '#8a6fd1'), ('treat', 'Treat', '#e5484d')]


def f_moves(c, t):
    off = 480 * t
    corridor(c, off + 3024)
    for i, (ic, lab, col) in enumerate(MOVES):
        x = 600 + i * 350 - off; on = clamp((DX + 260 - x) / 90)
        door(c, x, col, on, ic)
        plate(c, x, 640, 300, 100, lab, '#ffffff' if on < .5 else col, INK if on < .5 else '#ffffff', str(i + 1))
    brand_bar(c); bignum(c, '4', 'moves', 'Talk. Examine. Tests. Treat.', t)
    runner(c, t, 'intern', 1, 'ok')


RT = .3; RSP = 610; RGAP = 380


def rank_off(t): return min(RSP * max(0, t - 0), 4 * RGAP + 640 - 470 + 0)


def f_ranks(c, t):
    off = rank_off(t); stop = off >= 4 * RGAP + 170 - 1e-6
    corridor(c, off + 4272)
    cur = 0
    for i, rk in enumerate(RANKS):
        x = 640 + i * RGAP - off; on = clamp((DX + 240 - x) / 80)
        if on > .5: cur = i
        col = GOLD if i == 4 else [TEAL, '#17a394', '#2f8f9d', '#33475b'][i]
        door(c, x, col, on, None, gold=i == 4)
        plate(c, x, 640, 356, 100, rk, (GOLD if i == 4 else INK) if on > .5 else '#ffffff', (INK if i == 4 else '#ffffff') if on > .5 else INK, str(i + 1), size=46)
    brand_bar(c); bignum(c, '5', 'ranks', 'Intern to ED Director.', t)
    ts = (4 * RGAP + 170) / RSP
    k = 1 - eio((t - ts) / .25)
    if cur == 4 and t > ts: c.drawCircle(DX, 1200, 260, P(GOLD, 70, blur=80))
    runner(c, t, OUT[cur], k, 'tired' if cur == 0 else 'happy', ra=(-150 + math.sin(t * 7) * 12) if (stop and t > ts + .15) else None)
    tc = (cur * RGAP + 100) / RSP  # when this rank's door lit up
    pill(c, DX + 16, 950, RANKS[cur], GOLD if cur == 4 else '#ffffff', INK, 40, pop((t - tc) / .25) if cur else 1)
    if cur and t - tc < .2: c.drawCircle(DX, 1220, 300 * (t - tc) / .2 + 60, P('#ffffff', 150 * (1 - (t - tc) / .2), stroke=14))


def hang(c, x, ic, lab, first, t, i):
    sway = math.sin(t * 3 + i) * 1.5
    c.save(); c.rotate(sway, x, CEIL)
    c.drawLine(x - 80, CEIL + 20, x - 80, 680, P('#7b8a97', stroke=8)); c.drawLine(x + 80, CEIL + 20, x + 80, 680, P('#7b8a97', stroke=8))
    rr(c, x - 122, 680 + 8, 244, 318, 30, P('#000000', 60, blur=14)); rr(c, x - 122, 680, 244, 318, 30, P(INK))
    if first: rr(c, x - 116, 686, 232, 306, 26, P(GOLD, stroke=10))
    c.drawCircle(x, 780, 68, P(GOLD if first else TEAL)); icon(c, ic, x, 780, 84, INK if first else '#ffffff')
    ws = lab.split()
    if len(ws) == 1: text(c, lab, x, 936, 54, '#ffffff', 900, 'c')
    else:
        text(c, ws[0], x, 906, 46, '#ffffff', 900, 'c'); text(c, ws[1], x, 958, 46, '#ffffff', 900, 'c')
    if first: pill(c, x, 676, 'START HERE', GOLD, INK, 30, 1 + .05 * math.sin(t * 9))
    c.restore()


def f_modes(c, t):
    off = 215 * t
    corridor(c, off + 6000)
    for i, (ic, lab) in enumerate(MODES): hang(c, 700 + i * 256 - off, ic, lab, i == 0, t, i)
    brand_bar(c); bignum(c, '4', 'ways to play', 'Start in Career.', t, size=170)
    runner(c, t * .8, 'director', .6, 'happy')


SC = [(f_hook, 2.6), (f_patients, 2.7), (f_moves, 2.6), (f_ranks, 3.4), (f_modes, 2.6), (cta2('Start as an Intern.', 'See how far you get.'), 3.0)]

VOICE = [(0.12, 'How far would you get in the E.R.?', 2.35), (2.72, 'One hundred sixty-three patients.', 2.45),
         (5.42, 'Four moves for every patient.', 2.35), (8.02, 'Five ranks. Intern to E.D. Director.', 3.1),
         (11.42, 'Four ways to play. Start in Career.', 2.4), (14.05, 'Bedside Bay. Play free.', 2.6)]


def soundtrack(wav):
    import sound
    cues = [(.02, 'pop'), (.25, 'pop'), (1.35, 'riser'), (2.55, 'whoosh')]
    cues += [(2.65 + i * .11, 'tick') for i in range(16)] + [(4.45, 'ding'), (5.2, 'whoosh')]
    cues += [(5.3 + .55 + i * .73, 'pop') for i in range(4)] + [(7.8, 'whoosh')]
    cues += [(7.9 + (i * RGAP + 100) / RSP, f'step:{i}') for i in range(5)] + [(7.9 + (4 * RGAP + 170) / RSP + .1, 'cash'), (11.2, 'whoosh')]
    cues += [(11.35, 'ding'), (12.3, 'pop'), (13.2, 'riser'), (13.9, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=2.6, lift=7.9, cta=13.9, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i == len(SC) - 1: flash(c, t, .15)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 0.6), (0, 2.3), (1, 0.4), (1, 1.2), (1, 2.5), (2, 0.5), (2, 1.6), (2, 2.5), (3, 0.3), (3, 1.2), (3, 2.0), (3, 3.2), (4, 0.3), (4, 1.4), (4, 2.5), (5, 0.5), (5, 2.8)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 6)
    elif sys.argv[1] == 'frame':
        save_jpg(frame(compose(int(sys.argv[2])), float(sys.argv[3])), sys.argv[4])
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'; os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
