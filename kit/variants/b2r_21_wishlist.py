"""Broke to Rich variant 21 — "Dr John Smith's wish list. Day 1." A torn notebook page is taped to the wall of the
broke Intern's bare room with four unticked wishes: a real bed, a car that starts, a gold watch, the mansion. Every
promotion (Resident, Registrar, Consultant, ED Director) puts the thing next to him and lands a big tick and a
strike-through on that line; the list stays on screen the whole time so the progress is obvious. Then "List complete."
and the end card. The wishes and the bank amounts after the $2,000 start are illustrative.
Music: upbeat.
Video: python3 b2r_21_wishlist.py <out.mp4>          Preview: python3 b2r_21_wishlist.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK, OUT

WISH = ['A real bed', 'A car that starts', 'A gold watch', 'The mansion']
PEN, GREEN, RED = '#27408b', '#1f9d63', '#e5484d'
PW, PH = 480, 436    # the notebook page
DX, FOOT = 800, 1226  # the doctor
GY = 1236            # the ground the things stand on
TICK = .95           # when the tick lands in a rank scene


# ---------------------------------------------------------------- the list
def page(c, x, y, s, done, t=None, rot=-3):
    """The wish list. done = how many lines are ticked; t = seconds since the newest tick landed (None = no animation)."""
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(rot)
    if t is not None and done:  # the whole page jumps when the tick lands
        k = 1 + .09 * math.sin(clamp(t / .35) * math.pi); c.translate(PW / 2, PH / 2); c.scale(k, k); c.translate(-PW / 2, -PH / 2)
    p = skia.Path(); p.moveTo(0, 0); p.lineTo(PW, 0); p.lineTo(PW, PH - 14); n = 12
    for i in range(n, -1, -1): p.lineTo(PW * i / n, PH - (14 if i % 2 else 0) - (6 if i % 3 == 0 else 0))  # torn edge
    p.close()
    c.save(); c.translate(6, 12); c.drawPath(p, P('#000000', 90, blur=16)); c.restore()
    c.drawPath(p, P('#fdf6dc'))
    for i in range(5): c.drawLine(0, 126 + i * 74, PW, 126 + i * 74, P('#9cc4e8', 150, stroke=3, cap=False))
    c.drawLine(64, 0, 64, PH - 18, P('#f29a9a', 170, stroke=3, cap=False))
    for hy in (60, 218, 376): c.drawCircle(28, hy, 11, P('#000000', 70))
    c.save(); c.skew(-.12, 0)
    text(c, 'WISH LIST', 96 + .12 * 84, 84, 54, PEN, 900)
    c.restore()
    sq = skia.Path(); sq.moveTo(84, 100); sq.quadTo(190, 92, 360, 102); c.drawPath(sq, P(PEN, stroke=6))
    for i, w in enumerate(WISH):
        by = 174 + i * 74; on = i < done; new = on and i == done - 1 and t is not None
        rr(c, 84, by - 38, 46, 46, 8, P(PEN, stroke=5))
        c.save(); c.skew(-.12, 0); wv = text(c, w, 156 + .12 * by, by, 42, PEN if not on else '#7d8bb5', 700); c.restore()
        if on:
            k = clamp(t / .22) if new else 1
            c.drawLine(146, by - 14, 146 + (wv + 12) * k, by - 16, P(RED, 220, stroke=6))
            kk = pop(t / .3) if new else 1
            c.save(); c.translate(107, by - 15); c.scale(kk, kk); check(c, 4, -4, 30, GREEN, 13); c.restore()
            if new and t < .6:
                for j in range(6):
                    a = j * math.pi / 3 + .4; r = 40 + 90 * ease(t / .6)
                    sparkle(c, 107 + math.cos(a) * r, by - 15 + math.sin(a) * r, 18 * (1 - t / .6), 255, GOLD)
    for tx, ta in ((70, -8), (PW - 110, 6)):  # tape
        c.save(); c.translate(tx, -18); c.rotate(ta); rr(c, 0, 0, 110, 40, 4, P('#e8d9a6', 215)); c.restore()
    c.restore()


# ---------------------------------------------------------------- the four things
def bed(c, t):
    c.drawOval(skia.Rect.MakeXYWH(40, GY - 14, 580, 36), P('#000000', 80, blur=12))
    for lx in (62, 572): rr(c, lx, GY - 60, 26, 60, 6, P('#6e4a2c'))
    rr(c, 40, GY - 250, 44, 230, 14, P('#8a5a3a')); rr(c, 40, GY - 250, 44, 60, 14, P('#a06c46'))
    rr(c, 580, GY - 150, 36, 130, 12, P('#8a5a3a')); rr(c, 60, GY - 80, 540, 40, 10, P('#7a5033'))
    rr(c, 76, GY - 136, 520, 66, 22, P('#ffffff'))
    rr(c, 250, GY - 150, 350, 96, 26, P(TEAL)); rr(c, 250, GY - 150, 350, 26, 13, P('#bfe9e4'))
    rr(c, 92, GY - 188, 150, 64, 28, P('#eef4f8')); rr(c, 100, GY - 180, 134, 20, 10, P('#ffffff'))


def car(c, t):
    j = math.sin(t * 40) * 1.5  # the engine is running
    for i in range(3):  # exhaust
        k = (t * 1.2 + i / 3) % 1; c.drawCircle(52 - k * 44, GY - 54 - k * 40, 12 + k * 22, P('#ffffff', 110 * (1 - k)))
    c.drawOval(skia.Rect.MakeXYWH(60, GY - 14, 560, 36), P('#000000', 90, blur=12))
    c.drawCircle(612, GY - 86, 90, P('#fff3b0', 60, blur=40))
    c.save(); c.translate(0, j)
    cab = skia.Path(); cab.moveTo(130, GY - 122); cab.quadTo(170, GY - 226, 270, GY - 232); cab.lineTo(430, GY - 232); cab.quadTo(500, GY - 220, 548, GY - 122); cab.close()
    c.drawPath(cab, P('#3a7fc4'))
    win = skia.Path(); win.moveTo(168, GY - 126); win.quadTo(196, GY - 204, 274, GY - 208); win.lineTo(424, GY - 208); win.quadTo(480, GY - 198, 514, GY - 126); win.close()
    c.drawPath(win, P('#cfe8f7')); c.drawLine(336, GY - 208, 336, GY - 126, P('#3a7fc4', stroke=12, cap=False))
    rr(c, 70, GY - 134, 546, 96, 34, P('#3a7fc4')); rr(c, 70, GY - 70, 546, 32, 16, P('#2c659f'))
    rr(c, 586, GY - 108, 30, 30, 10, P('#fff3b0')); rr(c, 70, GY - 108, 20, 30, 8, P('#ff7a7a'))
    rr(c, 300, GY - 108, 40, 10, 5, P('#2c659f'))
    c.restore()
    for wx in (184, 506):
        c.drawCircle(wx, GY - 40, 46, P('#14181d')); c.drawCircle(wx, GY - 40, 22, P('#cfd6dd')); c.drawCircle(wx, GY - 40, 8, P('#7b8894'))


def watch(c, t):
    c.drawOval(skia.Rect.MakeXYWH(90, GY - 14, 470, 36), P('#000000', 90, blur=12))
    rr(c, 110, GY - 30, 430, 30, 10, P('#6e4a2c')); rr(c, 150, GY - 4, 30, 40, 6, P('#5a3b24')); rr(c, 470, GY - 4, 30, 40, 6, P('#5a3b24'))
    rr(c, 170, GY - 262, 310, 170, 16, P('#1a2740')); rr(c, 186, GY - 248, 278, 150, 10, P('#25365a'))   # open lid
    rr(c, 170, GY - 104, 310, 76, 14, P('#101a2e')); rr(c, 186, GY - 104, 278, 20, 8, P('#31456f'))
    c.drawCircle(325, GY - 150, 150, P('#ffe2a6', 60, blur=50))
    rr(c, 293, GY - 246, 64, 196, 22, grad(293, 0, 357, 0, ['#c98f1f', '#f5b83d', '#c98f1f']))
    for sy in (GY - 232, GY - 216, GY - 84, GY - 68): c.drawLine(299, sy, 351, sy, P('#a87414', stroke=4, cap=False))
    c.drawCircle(325, GY - 150, 66, P('#c98f1f')); c.drawCircle(325, GY - 150, 58, P(GOLD)); c.drawCircle(325, GY - 150, 44, P('#fff6dc'))
    rr(c, 388, GY - 158, 14, 16, 4, P('#c98f1f'))
    for i in range(12):
        a = i * math.pi / 6; c.drawLine(325 + math.cos(a) * 34, GY - 150 + math.sin(a) * 34, 325 + math.cos(a) * 40, GY - 150 + math.sin(a) * 40, P('#8a6a1c', stroke=4))
    c.drawLine(325, GY - 150, 325, GY - 182, P(INK, stroke=6)); c.drawLine(325, GY - 150, 349, GY - 138, P(INK, stroke=6)); c.drawCircle(325, GY - 150, 6, P(INK))
    for j, (sx, sy) in enumerate(((236, GY - 214), (420, GY - 196), (392, GY - 86))): sparkle(c, sx, sy, 30 * abs(math.sin(t * 3 + j * 1.3)), 255, '#fff6d8')


def mansion(c, t):
    """The house from scenes.rich at 0.55 scale, with the supercar parked in front."""
    c.drawOval(skia.Rect.MakeXYWH(20, GY - 16, 620, 40), P('#000000', 80, blur=12))
    c.save(); c.translate(30, GY); c.scale(.55, .55); c.translate(-26, -1130)
    rr(c, 150, 640, 330, 190, 8, P('#fbf8f2')); c.drawRect(skia.Rect.MakeXYWH(126, 622, 378, 26), P('#34414f'))
    rr(c, 50, 812, 560, 312, 8, P('#f4f0e8')); c.drawRect(skia.Rect.MakeXYWH(26, 794, 608, 28), P('#34414f'))
    glow = 220 + 30 * math.sin(t * 2)
    for wx, wy, ww, wh in ((176, 672, 130, 120), (322, 672, 130, 120), (84, 860, 150, 200), (430, 860, 150, 200)):
        rr(c, wx, wy, ww, wh, 6, P('#ffd98a', glow)); c.drawLine(wx + ww / 2, wy, wx + ww / 2, wy + wh, P('#34414f', stroke=5, cap=False))
        c.drawLine(wx, wy + wh * .5, wx + ww, wy + wh * .5, P('#34414f', stroke=5, cap=False))
    rr(c, 276, 900, 112, 224, 8, P('#34414f')); c.drawCircle(366, 1016, 7, P(GOLD))
    for px in (262, 402): rr(c, px - 10, 880, 20, 244, 6, P('#e2dccf'))
    rr(c, 30, 1108, 600, 22, 6, P('#d9d3c6'))
    c.restore()
    c.save(); c.translate(640, GY + 6); c.scale(-.74, .74); c.translate(-552, -1292)   # supercar, nose to the right
    body = skia.Path(); body.moveTo(556, 1250); body.lineTo(552, 1214); body.quadTo(600, 1178, 680, 1170)
    body.quadTo(730, 1116, 810, 1116); body.quadTo(880, 1118, 910, 1166); body.quadTo(962, 1176, 966, 1214); body.lineTo(966, 1250); body.close()
    c.drawPath(body, grad(0, 1116, 0, 1250, ['#ff4d4d', '#c01f2e']))
    win = skia.Path(); win.moveTo(700, 1170); win.quadTo(738, 1132, 806, 1132); win.quadTo(858, 1134, 884, 1168); win.close()
    c.drawPath(win, P('#1c2530')); c.drawLine(796, 1132, 796, 1168, P('#c01f2e', stroke=7, cap=False))
    rr(c, 556, 1206, 34, 14, 7, P('#fff3b0')); rr(c, 944, 1204, 22, 14, 6, P('#ffb3b3')); c.drawLine(600, 1232, 920, 1232, P('#8f1420', stroke=5))
    for wx in (640, 880): c.drawCircle(wx, 1250, 42, P('#14181d')); c.drawCircle(wx, 1250, 24, P('#cfd6dd'))
    sparkle(c, 760, 1150, 30 * abs(math.sin(t * 3)), 255)
    c.restore()


THINGS = [None, bed, car, watch, mansion]


def thing(c, i, t):
    k = pop((t - .12) / .45)
    if t < .12: return
    c.save(); c.translate(330, GY); c.scale(k, k); c.translate(-330, -GY); THINGS[i](c, t); c.restore()


# ---------------------------------------------------------------- the five places
def _floor(c, col, line, y=1160):
    c.drawRect(skia.Rect.MakeXYWH(0, y, W, H - y), P(col))
    for i in range(6): c.drawLine(0, y + 44 + i * 130, W, y + 44 + i * 130, P(line, stroke=4))


def _window(c, x, y, w, h, frame, sky, lights=True, t=0):
    rr(c, x - 14, y - 14, w + 28, h + 28, 10, P(frame)); rr(c, x, y, w, h, 6, P(sky))
    if lights:
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
        for j, (bx, bw, bh) in enumerate(((0, 70, 150), (64, 90, 230), (150, 70, 120), (214, 100, 190), (300, 80, 260))):
            rr(c, x + bx, y + h - bh, bw, bh + 10, 4, P('#0c1420'))
            for r in range(int(bh / 44)):
                for q in range(2):
                    if (j + r + q) % 3: rr(c, x + bx + 14 + q * 30, y + h - bh + 16 + r * 44, 16, 22, 3, P('#ffd98a', 200 + 40 * math.sin(t * 2 + j + r)))
        c.restore()
    c.drawLine(x + w / 2, y, x + w / 2, y + h, P(frame, stroke=10, cap=False)); c.drawLine(x, y + h * .5, x + w, y + h * .5, P(frame, stroke=10, cap=False))


def p_bare(c, t):   # intern: the bare room, mattress on the floor
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#2a333f', '#1b212a'])); _floor(c, '#2e2620', '#241d18')
    c.drawRect(skia.Rect.MakeXYWH(0, 1146, W, 16), P('#39424e'))
    cr = skia.Path(); cr.moveTo(1010, 520); cr.lineTo(984, 610); cr.lineTo(1016, 680); cr.lineTo(990, 770); cr.lineTo(1022, 850); c.drawPath(cr, P('#141a21', stroke=5))
    c.drawOval(skia.Rect.MakeXYWH(560, 980, 300, 150), P('#1d242d', 170, blur=24))
    rr(c, 50, 1126, 500, 84, 28, P('#b6ae9f'))    # mattress
    for i in range(8): c.drawLine(100 + i * 56, 1136, 100 + i * 56, 1200, P('#9c9484', stroke=4))
    rr(c, 66, 1090, 150, 58, 24, P('#dcd6ca')); rr(c, 270, 1112, 280, 74, 30, P('#5f6f82'))
    cup = skia.Path(); cup.moveTo(580, 1126); cup.lineTo(660, 1126); cup.lineTo(648, 1206); cup.lineTo(592, 1206); cup.close()   # instant noodles
    c.drawPath(cup, P('#f4f1ea')); rr(c, 574, 1116, 92, 16, 8, P('#e3ded3'))
    band = skia.Path(); band.moveTo(584, 1150); band.lineTo(656, 1150); band.lineTo(652, 1180); band.lineTo(588, 1180); band.close(); c.drawPath(band, P('#d64545'))


def p_flat(c, t):   # resident: a small rented flat
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#2b4a5c', '#1d3442'])); _floor(c, '#5a4636', '#4b3a2c')
    c.drawRect(skia.Rect.MakeXYWH(0, 1146, W, 16), P('#e9e2d4'))
    _window(c, 620, 560, 330, 360, '#e9e2d4', '#16233a', True, t)
    c.drawCircle(900, 610, 26, P('#eef2f6'))
    c.drawOval(skia.Rect.MakeXYWH(20, 1200, 660, 60), P('#c0563a', 200))  # rug


def p_lot(c, t):    # registrar: the staff parking lot at dusk
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1160, ['#1a2444', '#33457a', '#c9728a', '#ffb47d']))
    rr(c, 600, 640, 520, 540, 10, P('#18203a'))
    for r in range(6):
        for q in range(5):
            if (r * 3 + q) % 4: rr(c, 630 + q * 86, 672 + r * 80, 50, 46, 4, P('#ffd98a', 170 + 50 * math.sin(t * 2 + r + q)))
    rr(c, 600, 610, 520, 40, 6, P('#111830'))
    c.drawRect(skia.Rect.MakeXYWH(0, 1160, W, H - 1160), P('#2d3138')); c.drawRect(skia.Rect.MakeXYWH(0, 1152, W, 12), P('#4a4f58'))
    for lx in (20,): c.drawLine(lx, 1180, lx - 60, 1560, P('#f2f2f2', 190, stroke=10, cap=False))


def p_condo(c, t):  # consultant: his own apartment, evening
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#17463f', '#0b2622'])); _floor(c, '#3b2a20', '#2e2018')
    c.drawRect(skia.Rect.MakeXYWH(0, 1146, W, 16), P(GOLD))
    _window(c, 600, 540, 380, 560, '#0b1d1a', '#1b2d55', True, t)


def p_estate(c, t):  # ED Director: sunset on the lawn
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1130, ['#272b73', '#8a4a94', '#f2707a', '#ffc37d']))
    c.drawCircle(820, 960, 230, P('#ffe2a6', 90, blur=70)); c.drawCircle(820, 960, 118, P('#fff0c4'))
    for i, (sx, sy) in enumerate(((90, 520), (990, 600), (620, 540), (560, 700), (1000, 820))): c.drawCircle(sx, sy, 4, P('#ffffff', 130 + 110 * math.sin(t * 3 + i)))
    hill = skia.Path(); hill.moveTo(0, 1100); hill.quadTo(300, 1000, 620, 1090); hill.quadTo(860, 1030, W, 1080); hill.lineTo(W, 1160); hill.lineTo(0, 1160); hill.close()
    c.drawPath(hill, P('#5b3f86', 200))
    c.drawRect(skia.Rect.MakeXYWH(0, 1140, W, H - 1140), grad(0, 1140, 0, 1500, ['#2e9f6b', '#1c7a50']))


PLACES = [p_bare, p_flat, p_lot, p_condo, p_estate]
CAP = ['', 'A real bed.', 'A car that starts.', 'A gold watch.', 'The mansion.']


def wrist_watch(c, t, ra, sc=1.0):
    """A gold watch on the consultant's front wrist (same transform as lib.doctor's front arm)."""
    c.save(); c.translate(DX, FOOT); c.scale(sc, sc); c.translate(0, math.sin(t * 2.4) * 4); c.translate(84, -380); c.rotate(ra)
    rr(c, -25, 112, 50, 22, 6, P(GOLD)); c.drawCircle(0, 123, 17, P('#ffd774')); c.drawCircle(0, 123, 10, P('#fff4cf'))
    sparkle(c, 0, 123, 40 * abs(math.sin(t * 3.2)), 255, '#fff6d8')
    c.restore()


def dr(c, i, t):
    if i == 0: doctor(c, DX, FOOT, 1.0, 'intern', t, la=7, ra=-7, mood='tired')
    elif i == 3:
        ra = -128 + math.sin(t * 5) * 6
        doctor(c, DX, FOOT, 1.0, 'consultant', t, la=10, ra=ra, mood='happy'); wrist_watch(c, t, ra)
    elif i == 4: doctor(c, DX, FOOT, 1.0, 'director', t, la=10, ra=-150 + math.sin(t * 6) * 12)
    else: doctor(c, DX, FOOT, 1.0, OUT[i], t, la=10, ra=-12, mood='happy')


def e_hook(c, t):
    p_bare(c, t); dr(c, 0, t)
    page(c, 44, 520, 1.22, 0)
    title2(c, 'Dr John Smith’s wish list.', 'Day 1.', 356, size=92, sub_size=100)
    hud(c, 0, 2000, 1); brand_bar(c)


def _rank(i):
    def f(c, t):
        PLACES[i](c, t); thing(c, i, t); dr(c, i, t)
        tt = t - TICK
        page(c, 50, 510, 1.0, i if tt >= 0 else i - 1, tt if tt >= 0 else None)
        k = ease(t / .3)
        title2(c, RANKS[i], CAP[i], 356, dy=(1 - k) * -30, a=255 * k, size=112, sub_size=80)
        up = clamp((t - .3) / .5)
        hud(c, i, lerp(BANK[i - 1], BANK[i], eio((t - .3) / 1.1)), i + up, bump=math.sin(up * math.pi)); brand_bar(c)
    return f


def e_done(c, t):
    p_estate(c, t)
    for i in range(14):   # gold confetti
        k = (t * .5 + i * .173) % 1; x = (i * 197 + 61) % 1000 + 40; y = 480 + k * 760
        c.save(); c.rotate(t * 200 + i * 40, x, y); rr(c, x - 12, y - 7, 24, 14, 3, P([GOLD, '#ffffff', TEAL][i % 3], 230 * (1 - k * .6))); c.restore()
    k = pop(t / .4); s = 1.34 * k
    page(c, 540 - PW * s / 2 + 14, 560, s, 4, None, rot=-2)
    title2(c, 'List complete.', 'Every line ticked.', 356, size=112, sub_size=76, a=255 * ease(t / .25))
    if t > .45:
        kk = pop((t - .45) / .35); c.save(); c.translate(884, 1128); c.scale(kk, kk); c.rotate(-10)
        c.drawCircle(0, 0, 92, P('#000000', 80, blur=14)); c.drawCircle(0, 0, 88, P(GREEN)); c.drawCircle(0, 0, 74, P('#ffffff', 230, stroke=5)); check(c, 0, 4, 40, '#ffffff', 16); c.restore()
    hud(c, 4, BANK[4], 5); brand_bar(c)


RD = [2.7, 2.7, 2.7, 2.8]
SC = [(e_hook, 3.0)] + [(_rank(i), RD[i - 1]) for i in range(1, 5)] + [(e_done, 1.9), (cta2('Write your own list.', 'Start as a broke Intern.'), 3.3)]
ST = [sum(d for _, d in SC[:i]) for i in range(len(SC))]

VOICE = [(0.15, "Doctor John Smith's wish list. Day one.", 2.75), (ST[1] + .12, 'Resident. A real bed.', 2.4), (ST[2] + .12, 'Registrar. A car that starts.', 2.4),
         (ST[3] + .12, 'Consultant. A gold watch.', 2.4), (ST[4] + .12, 'E.D. Director. The mansion.', 2.5), (ST[5] + .1, 'List complete.', 1.6),
         (ST[6] + .12, 'Write your own. Bedside Bay. Play free.', 3.0)]


def soundtrack(wav):
    import sound
    st = ST[1:5]
    cues = [(.05, 'pop')] + [(.5 + i * .3, 'tick') for i in range(4)]
    cues += [(s - .2, 'whoosh') for s in st] + [(s + .15, 'pop') for s in st] + [(s + TICK, 'ding') for s in st]
    cues += [(s + TICK + .02, f'step:{i + 1}') for i, s in enumerate(st)] + [(s + TICK + .3, 'cash') for s in st]
    cues += [(ST[5] - .2, 'whoosh'), (ST[5] + .05, 'impact'), (ST[5] + .45, 'ding'), (ST[6] - .9, 'riser'), (ST[6], 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=ST[1], lift=ST[4], cta=ST[6], cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .12)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 2.4), (1, 0.5), (1, 1.2), (1, 2.5), (2, 2.5), (3, 1.2), (3, 2.5), (4, 2.6), (5, 1.6), (6, 2.6)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 6)
    elif sys.argv[1] == 'frame':
        save_jpg(frame(compose(int(sys.argv[2])), float(sys.argv[3])), sys.argv[4])
    elif sys.argv[1] == 'phonemes':
        import sound
        for _, l, _ in VOICE: print(l, '->', sound.phonemes(l))
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
