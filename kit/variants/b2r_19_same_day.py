"""Broke to Rich variant 19 — "Same 24 hours. Intern vs ED Director." A horizontal split: the top half is Dr John Smith
as a broke Intern, the bottom half is Dr John Smith as ED Director, living the same day. A clock in the divider ticks
through four moments and both halves change together: 6:00 AM (floor mattress and a phone alarm vs king bed and a sunrise
view), 12:00 PM (vending machine vs chef's table), 6:00 PM (bus stop in the rain vs supercar in the driveway), 11:00 PM
(still charting under a flickering light vs feet up with the gold watch). Then the divider opens into the career card
climbing Intern -> ED Director ("Same doctor. 4 promotions apart.") and the Play free card.
Bank amounts after the $2,000 start, the mansion, car and watch are illustrative. Music: bright.
Video: python3 b2r_19_same_day.py <out.mp4>          Preview: python3 b2r_19_same_day.py preview <sheet.jpg> [frames_dir]"""
from common import *
from fullgame_02 import BANK

TOP_Y, PH, BOT_Y, BH = 500, 500, 1080, 570     # top panel, its height, bottom panel, its height (divider band between them)
FL = 410                              # floor level inside a panel (panel-local y)


# ---------------------------------------------------------------- small props
def _poly(pts, close=True):
    p = skia.Path()
    for i, (x, y) in enumerate(pts): (p.lineTo if i else p.moveTo)(x, y)
    if close: p.close()
    return p


def backdrop(c, wall, floor, skirt=None):
    c.drawRect(skia.Rect.MakeLTRB(-20, -60, W + 20, FL), grad(0, 0, 0, FL, wall))
    c.drawRect(skia.Rect.MakeLTRB(-20, FL, W + 20, 700), P(floor))
    if skirt: c.drawRect(skia.Rect.MakeLTRB(-20, FL - 12, W + 20, FL + 2), P(skirt))


def lying(c, feet_x, y, sc, outfit, t, ang=-90, **kw):
    """Dr John Smith lying down, head to the left; (feet_x, y) = soles on the body's centre line."""
    c.save(); c.translate(feet_x, y); c.rotate(ang); doctor(c, 0, 0, sc, outfit, t, **kw); c.restore()


def bulb(c, x, t, drop=70):
    ang = math.sin(t * 1.7) * 6
    c.save(); c.translate(x, -10); c.rotate(ang)
    c.drawLine(0, 0, 0, drop, P('#11161c', stroke=5)); rr(c, -11, drop - 2, 22, 20, 4, P('#555f6b'))
    c.drawCircle(0, drop + 36, 110, P('#ffe7a0', 44 + 10 * math.sin(t * 9), blur=50)); c.drawCircle(0, drop + 36, 22, P('#fff0b8'))
    c.restore()


def mansion(c, x, y, s, t):
    """Modern two-storey house with glowing glass; (x, y) = bottom-left."""
    c.save(); c.translate(x, y); c.scale(s, s); c.translate(-26, -1130)
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


def supercar(c, x, y, s, t):
    """Red supercar facing left; (x, y) = bottom-left of the wheels."""
    c.save(); c.translate(x, y); c.scale(s, s); c.translate(-552, -1292)
    c.drawOval(skia.Rect.MakeXYWH(540, 1270, 440, 36), P('#000000', 80, blur=10))
    body = skia.Path(); body.moveTo(556, 1250); body.lineTo(552, 1214); body.quadTo(600, 1178, 680, 1170)
    body.quadTo(730, 1116, 810, 1116); body.quadTo(880, 1118, 910, 1166); body.quadTo(962, 1176, 966, 1214); body.lineTo(966, 1250); body.close()
    c.drawPath(body, grad(0, 1116, 0, 1250, ['#ff4d4d', '#c01f2e']))
    win = skia.Path(); win.moveTo(700, 1170); win.quadTo(738, 1132, 806, 1132); win.quadTo(858, 1134, 884, 1168); win.close()
    c.drawPath(win, P('#1c2530')); c.drawLine(796, 1132, 796, 1168, P('#c01f2e', stroke=7, cap=False))
    rr(c, 556, 1206, 34, 14, 7, P('#fff3b0')); rr(c, 944, 1204, 22, 14, 6, P('#ffb3b3'))
    c.drawLine(600, 1232, 920, 1232, P('#8f1420', stroke=5))
    for wx in (640, 880):
        c.drawCircle(wx, 1250, 42, P('#14181d')); c.drawCircle(wx, 1250, 24, P('#cfd6dd'))
        for i in range(5):
            a = i * 2 * math.pi / 5; c.drawLine(wx, 1250, wx + math.cos(a) * 22, 1250 + math.sin(a) * 22, P('#7b8894', stroke=5))
    sparkle(c, 760, 1150, 26 * abs(math.sin(t * 3)), 255)
    c.restore()


def sunset(c, sun_x, sun_y, t, cols=('#272b73', '#8a4a94', '#f2707a', '#ffc37d')):
    c.drawRect(skia.Rect.MakeLTRB(-20, -60, W + 20, FL), grad(0, -40, 0, FL, list(cols)))
    c.drawCircle(sun_x, sun_y, 150, P('#ffe2a6', 90, blur=50)); c.drawCircle(sun_x, sun_y, 74, P('#fff0c4'))
    hill = _poly([(-20, FL - 30)]); hill.quadTo(300, FL - 110, 620, FL - 40); hill.quadTo(860, FL - 90, W + 20, FL - 50); hill.lineTo(W + 20, FL + 10); hill.lineTo(-20, FL + 10)
    c.drawPath(hill, P('#5b3f86', 200))
    c.drawRect(skia.Rect.MakeLTRB(-20, FL - 6, W + 20, 700), grad(0, FL, 0, FL + 200, ['#2e9f6b', '#1c7a50']))


def palm(c, x, y, t, h=250):
    tr = skia.Path(); tr.moveTo(x - 14, y); tr.quadTo(x - 34, y - h * .6, x, y - h); c.drawPath(tr, P('#7a5636', stroke=20))
    for ang in (-150, -110, -60, -20, 30, 200):
        a = math.radians(ang + math.sin(t * 1.5 + ang) * 3); f = skia.Path(); f.moveTo(x, y - h)
        f.quadTo(x + math.cos(a) * 60, y - h + math.sin(a) * 60 - 34, x + math.cos(a) * 128, y - h + math.sin(a) * 100 + 14)
        c.drawPath(f, P('#1f8f57', stroke=17))


# ---------------------------------------------------------------- the two portraits (hook and closing)
def intern_portrait(c, t):
    backdrop(c, ['#2a333f', '#1b212a'], '#2e2620', '#39424e')
    rr(c, 700, 70, 170, 200, 8, P('#414c59')); rr(c, 712, 82, 146, 176, 5, P('#0e1522'))
    c.drawCircle(820, 130, 22, P('#dfe6f0')); c.drawCircle(830, 124, 19, P('#0e1522'))
    c.drawLine(785, 82, 785, 258, P('#414c59', stroke=8, cap=False)); c.drawLine(712, 170, 858, 170, P('#414c59', stroke=8, cap=False))
    cr = _poly([(960, 40), (940, 100), (968, 150), (946, 210)], False); c.drawPath(cr, P('#141a21', stroke=5))
    bulb(c, 470, t)
    rr(c, 60, FL - 40, 360, 62, 22, P('#b6ae9f'))
    for i in range(6): c.drawLine(100 + i * 54, FL - 32, 100 + i * 54, FL + 16, P('#9c9484', stroke=4))
    rr(c, 74, FL - 70, 130, 48, 20, P('#dcd6ca')); rr(c, 220, FL - 56, 200, 60, 26, P('#5f6f82'))
    cup = _poly([(826, FL - 60), (906, FL - 60), (894, FL + 16), (838, FL + 16)]); c.drawPath(cup, P('#f4f1ea')); rr(c, 820, FL - 68, 92, 14, 7, P('#e3ded3'))
    c.drawPath(_poly([(829, FL - 38), (903, FL - 38), (899, FL - 10), (833, FL - 10)]), P('#d64545'))
    doctor(c, 600, 462, .62, 'intern', t, la=7, ra=-7, mood='tired')


def director_portrait(c, t):
    sunset(c, 830, FL - 110, t)
    for i, (sx, sy) in enumerate(((120, 60), (980, 90), (640, 40), (420, 110))):
        c.drawCircle(sx, sy, 4, P('#ffffff', 130 + 110 * math.sin(t * 3 + i)))
    mansion(c, 50, FL + 6, .56, t); palm(c, 950, FL + 6, t)
    doctor(c, 610, 462, .62, 'director', t, la=10, ra=-158 + math.sin(t * 6) * 12)
    sparkle(c, 692, 150 + math.sin(t * 6) * 6, 26 * abs(math.sin(t * 2.6)), 255, '#fff6d8')


# ---------------------------------------------------------------- 6:00 AM
def am_intern(c, t):
    backdrop(c, ['#2a333f', '#1b212a'], '#2e2620', '#39424e')
    rr(c, 430, 60, 170, 190, 8, P('#414c59')); rr(c, 442, 72, 146, 166, 5, grad(0, 72, 0, 238, ['#141d33', '#3b3558']))
    c.drawLine(515, 72, 515, 238, P('#414c59', stroke=8, cap=False)); c.drawLine(442, 155, 588, 155, P('#414c59', stroke=8, cap=False))
    cr = _poly([(960, 30), (940, 90), (968, 140), (946, 200)], False); c.drawPath(cr, P('#141a21', stroke=5))
    # mattress on the floor, Dr John Smith under a thin blanket
    rr(c, 60, FL - 44, 560, 66, 24, P('#b6ae9f'))
    for i in range(10): c.drawLine(98 + i * 54, FL - 36, 98 + i * 54, FL + 14, P('#9c9484', stroke=4))
    rr(c, 74, FL - 96, 190, 62, 26, P('#dcd6ca'))
    lying(c, 540, FL - 92, .52, 'intern', t, la=4, ra=-4, mood='tired')
    bl = skia.Path(); bl.moveTo(322, FL - 150); bl.quadTo(450, FL - 172, 580, FL - 146); bl.lineTo(590, FL - 34); bl.lineTo(322, FL - 34); bl.close()
    c.drawPath(bl, P('#5f6f82')); c.drawLine(336, FL - 142, 336, FL - 40, P('#74859a', stroke=10))
    rr(c, 470, FL - 110, 60, 44, 6, P('#526073'))  # patch
    # phone alarm buzzing on the floor
    sh = math.sin(t * 46) * 5
    c.save(); c.translate(790 + sh, FL - 50); c.rotate(-8 + math.sin(t * 46) * 2)
    c.drawCircle(0, -60, 170, P('#9fe8ff', 46, blur=50))
    rr(c, -70, -180, 140, 250, 22, P('#10161d')); rr(c, -60, -166, 120, 222, 14, P('#bff0ff'))
    text(c, '6:00', 0, -70, 50, INK, 900, 'c'); text(c, 'ALARM', 0, -28, 24, '#d64545', 900, 'c')
    c.drawCircle(0, 12, 18, P('#d64545')); c.drawLine(-8, 12, 8, 12, P('#ffffff', stroke=5))
    bell = skia.Path(); bell.moveTo(-22, -110); bell.quadTo(-20, -148, 0, -148); bell.quadTo(20, -148, 22, -110); bell.close()
    c.drawPath(bell, P(INK)); c.drawCircle(0, -106, 6, P(INK))
    c.restore()
    for j in range(3):
        a = 230 - j * 60
        c.drawArc(skia.Rect.MakeXYWH(790 - 110 - j * 26, FL - 250 - j * 26, 220 + j * 52, 220 + j * 52), 200, 40, False, P('#ffd774', a, stroke=8))
        c.drawArc(skia.Rect.MakeXYWH(790 - 110 - j * 26, FL - 250 - j * 26, 220 + j * 52, 220 + j * 52), -60, 40, False, P('#ffd774', a, stroke=8))


def am_director(c, t):
    backdrop(c, ['#3a1f5c', '#6b2f6f'], '#4a2340', GOLD)
    # panoramic window with the sunrise
    rr(c, 560, 36, 440, 290, 10, P(GOLD)); c.save(); c.clipRect(skia.Rect.MakeXYWH(572, 48, 416, 266))
    c.drawRect(skia.Rect.MakeXYWH(572, 48, 416, 266), grad(0, 48, 0, 314, ['#5a6fd0', '#f59a8a', '#ffd88a']))
    c.drawCircle(780, 268, 120, P('#fff3c8', 110, blur=40)); c.drawCircle(780, 268, 62, P('#fff6d8'))
    for i in range(9):
        a = math.pi + i * math.pi / 8; c.drawLine(780 + math.cos(a) * 84, 268 + math.sin(a) * 84, 780 + math.cos(a) * (120 + 10 * math.sin(t * 3 + i)), 268 + math.sin(a) * (120 + 10 * math.sin(t * 3 + i)), P('#fff6d8', 200, stroke=6))
    hill = _poly([(572, 290)]); hill.quadTo(680, 240, 800, 284); hill.quadTo(900, 250, 988, 280); hill.lineTo(988, 314); hill.lineTo(572, 314); c.drawPath(hill, P('#2e9f6b'))
    c.restore()
    c.drawLine(780, 48, 780, 314, P(GOLD, stroke=8, cap=False))
    for cx_ in (548, 1010):  # curtains
        cu = _poly([(cx_ - 34, 28), (cx_ + 34, 28), (cx_ + 22, 200), (cx_ + 40, 340), (cx_ - 40, 340), (cx_ - 22, 200)]); c.drawPath(cu, P('#b3243a'))
        rr(c, cx_ - 30, 190, 60, 16, 8, P(GOLD))
    c.drawOval(skia.Rect.MakeXYWH(-40, FL + 4, 800, 60), P('#b3243a'))
    # king bed
    rr(c, 36, FL - 300, 46, 300, 16, P(GOLD)); rr(c, 50, FL - 290, 18, 150, 8, P('#ffd774'))
    for lx in (60, 650): rr(c, lx, FL - 40, 30, 44, 8, P(GOLD))
    rr(c, 50, FL - 74, 650, 40, 12, P(GOLD)); rr(c, 66, FL - 146, 624, 80, 26, P('#fff8ea'))
    rr(c, 674, FL - 150, 32, 116, 12, P(GOLD))
    for i in range(3): rr(c, 80 + i * 14, FL - 204 - i * 22, 200, 60, 28, P('#ffffff')); rr(c, 80 + i * 14, FL - 204 - i * 22, 200, 60, 28, P('#e0d6c4', stroke=3))
    lying(c, 566, FL - 196, .52, 'director', t, la=4, ra=-4)
    bl = skia.Path(); bl.moveTo(340, FL - 258); bl.quadTo(480, FL - 286, 664, FL - 250); bl.lineTo(672, FL - 96); bl.lineTo(340, FL - 96); bl.close()
    c.drawPath(bl, P('#b3243a')); rr(c, 330, FL - 262, 56, 170, 22, P('#ffd774'))
    for i in range(4): c.drawLine(420 + i * 62, FL - 236, 420 + i * 62, FL - 110, P('#9c1c30', stroke=4))
    # breakfast tray on a side table
    rr(c, 760, FL - 110, 170, 14, 6, P(GOLD)); c.drawLine(790, FL - 96, 780, FL, P(GOLD, stroke=8)); c.drawLine(900, FL - 96, 910, FL, P(GOLD, stroke=8))
    rr(c, 792, FL - 160, 54, 50, 10, P('#ffffff')); c.drawArc(skia.Rect.MakeXYWH(836, FL - 150, 30, 30), -90, 180, False, P('#ffffff', stroke=7))
    for i in range(2):
        k = (t * .5 + i / 2) % 1; sx = 808 + i * 22
        s = skia.Path(); s.moveTo(sx, FL - 170 - k * 40); s.quadTo(sx + 10, FL - 184 - k * 40, sx, FL - 198 - k * 40); c.drawPath(s, P('#ffffff', 150 * (1 - k), stroke=4))
    c.drawOval(skia.Rect.MakeXYWH(862, FL - 128, 60, 18), P('#ffffff')); c.drawCircle(892, FL - 132, 14, P('#f5b83d'))
    sparkle(c, 250, FL - 290, 20 * abs(math.sin(t * 2.4)), 255, '#fff6d8')


# ---------------------------------------------------------------- 12:00 PM
def noon_intern(c, t):
    backdrop(c, ['#dcecf0', '#bcd9e0'], '#9fb8c2', '#8ea2b1')
    c.drawRect(skia.Rect.MakeLTRB(-20, 230, W + 20, 244), P('#9fd4cf'))
    # vending machine
    x, y, w, h = 590, 24, 300, FL - 24
    rr(c, x - 8, y + 10, w + 16, h, 16, P('#000000', 50, blur=14)); rr(c, x, y, w, h, 16, P('#2b3f55'))
    rr(c, x + 16, y + 14, w - 32, 44, 10, P('#e5484d')); text(c, 'SNACKS', x + w / 2, y + 48, 32, '#ffffff', 900, 'c')
    rr(c, x + 16, y + 70, 196, 232, 10, P('#eaf6f8')); c.drawRect(skia.Rect.MakeXYWH(x + 16, y + 70, 196, 232), P('#ffffff', 60 + 20 * math.sin(t * 7)))
    cols = ['#f5b83d', '#e5484d', '#17b3a3', '#7c5cd6', '#f08a3c', '#3d8fe0']
    for r in range(4):
        c.drawRect(skia.Rect.MakeXYWH(x + 16, y + 122 + r * 56, 196, 6), P('#9fb2c2'))
        for q in range(4):
            if (r, q) == (2, 1): continue  # the one he just bought
            rr(c, x + 26 + q * 46, y + 80 + r * 56, 36, 42, 6, P(cols[(r * 2 + q) % 6])); rr(c, x + 32 + q * 46, y + 92 + r * 56, 24, 8, 3, P('#ffffff', 190))
    rr(c, x + 226, y + 76, 58, 86, 8, P('#1c2a3a')); rr(c, x + 234, y + 84, 42, 24, 4, P('#3ee08a'))
    for i in range(6): c.drawCircle(x + 243 + (i % 2) * 24, y + 122 + (i // 2) * 14, 5, P('#9fb2c2'))
    rr(c, x + 246, y + 180, 18, 44, 6, P('#0b1218')); rr(c, x + 30, y + 320, 180, 46, 10, P('#0b1218'))
    doctor(c, 400, 462, .62, 'intern', t, la=8, ra=-64 + math.sin(t * 3) * 4, mood='tired')
    # bag of chips in his raised hand
    ang = math.radians(-64 + math.sin(t * 3) * 4); hx = 400 + (84 - 170 * math.sin(ang)) * .62; hy = 462 + (-380 + 170 * math.cos(ang)) * .62 + math.sin(t * 2.4) * 2.5
    c.save(); c.translate(hx + 6, hy - 40); c.rotate(10)
    bag = _poly([(-34, -46), (34, -46), (30, 0), (34, 46), (-34, 46), (-30, 0)]); c.drawPath(bag, P('#f5b83d'))
    c.drawOval(skia.Rect.MakeXYWH(-22, -20, 44, 34), P('#e5484d')); text(c, 'CHIPS', 0, -2, 13, '#ffffff', 900, 'c')
    c.drawLine(-34, -40, 34, -40, P('#d99a1f', stroke=4)); c.drawLine(-34, 40, 34, 40, P('#d99a1f', stroke=4)); c.restore()
    for i in range(2):  # last coins
        c.drawCircle(250 + i * 44, FL + 26 - i * 6, 16, P(GOLD)); c.drawCircle(250 + i * 44, FL + 26 - i * 6, 10, P('#ffd774'))


def chef(c, x, y, s, t):
    """Chef behind the table lifting a silver cloche; (x, y) = waist."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -70, -150, 140, 190, 40, P('#ffffff')); c.drawLine(-10, -140, -10, 30, P('#d5dde5', stroke=4))
    for i in range(3): c.drawCircle(-28, -110 + i * 40, 6, P('#c3cfda')); c.drawCircle(10, -110 + i * 40, 6, P('#c3cfda'))
    rr(c, -16, -176, 32, 36, 12, P('#c98e68')); c.drawCircle(0, -214, 52, P('#d9a47c'))
    c.drawOval(skia.Rect.MakeXYWH(-24, -224, 12, 16), P('#2a1d16')); c.drawOval(skia.Rect.MakeXYWH(12, -224, 12, 16), P('#2a1d16'))
    m = skia.Path(); m.moveTo(-26, -196); m.quadTo(-12, -208, 0, -198); m.quadTo(12, -208, 26, -196); m.quadTo(12, -190, 0, -194); m.quadTo(-12, -190, -26, -196); c.drawPath(m, P('#3b2a20'))
    rr(c, -44, -304, 88, 62, 10, P('#ffffff')); rr(c, -48, -258, 96, 20, 8, P('#eef2f6'))
    for hx in (-34, 0, 34): c.drawCircle(hx, -310, 30, P('#ffffff'))
    c.restore()


def noon_director(c, t):
    backdrop(c, ['#3b2030', '#5a2c3c'], '#2a1622', '#7a4a2a')
    for lx in (480,):  # pendant lamp
        c.drawLine(lx, -20, lx, 50, P('#1a0f16', stroke=5)); c.drawCircle(lx, 96, 130, P('#ffd98a', 60, blur=50))
        c.drawPath(_poly([(lx - 50, 96), (lx + 50, 96), (lx + 24, 46), (lx - 24, 46)]), P(GOLD)); c.drawOval(skia.Rect.MakeXYWH(lx - 44, 88, 88, 18), P('#fff0b8'))
    rr(c, 560, 40, 150, 110, 8, P(GOLD)); rr(c, 570, 50, 130, 90, 4, P('#2a1622')); text(c, "CHEF'S", 635, 90, 26, GOLD, 900, 'c'); text(c, 'TABLE', 635, 122, 26, GOLD, 900, 'c')
    doctor(c, 400, 478, .62, 'director', t, la=10, ra=-12)
    chef(c, 800, 300, .78, t)
    # the table
    rr(c, 180, 292, 780, 30, 10, P('#ffffff')); c.drawRect(skia.Rect.MakeXYWH(196, 312, 748, 300), P('#f4efe6'))
    for i in range(7): c.drawLine(240 + i * 110, 322, 232 + i * 110, 600, P('#e3dccd', stroke=5))
    # steak plate, cutlery, glass, candle
    c.drawOval(skia.Rect.MakeXYWH(320, 262, 200, 44), P('#e3dccd')); c.drawOval(skia.Rect.MakeXYWH(328, 260, 184, 36), P('#ffffff'))
    c.drawOval(skia.Rect.MakeXYWH(370, 250, 90, 32), P('#7a3b22')); c.drawLine(386, 262, 440, 262, P('#5a2815', stroke=4)); c.drawCircle(480, 268, 12, P('#2e9f6b')); c.drawCircle(350, 270, 9, P('#e5484d'))
    c.drawLine(290, 236, 290, 300, P('#c9d2da', stroke=6)); c.drawLine(548, 236, 548, 300, P('#c9d2da', stroke=6)); rr(c, 282, 226, 16, 30, 6, P('#c9d2da'))
    c.drawLine(610, 292, 610, 240, P('#dfe9f0', stroke=5)); c.drawPath(_poly([(586, 180), (634, 180), (624, 240), (596, 240)]), P('#dff3fb', 220)); c.drawPath(_poly([(590, 204), (630, 204), (624, 240), (596, 240)]), P('#b3243a', 220))
    rr(c, 226, 230, 18, 64, 6, P('#fff8ea')); fl = 10 + 4 * math.sin(t * 11)
    c.drawCircle(235, 212, 46, P('#ffd98a', 80, blur=20)); c.drawOval(skia.Rect.MakeXYWH(227, 222 - fl * 2, 16, fl * 2 + 8), P('#ffb23d'))
    # cloche lifted over a second course
    lift = 16 + 10 * math.sin(t * 2.2)
    c.drawOval(skia.Rect.MakeXYWH(690, 270, 220, 34), P('#c9d2da'))
    dome = skia.Path(); dome.addArc(skia.Rect.MakeXYWH(706, 180 - lift, 188, 188), 180, 180); dome.close(); c.drawPath(dome, grad(706, 0, 894, 0, ['#f3f7fa', '#aab8c4']))
    c.drawCircle(800, 176 - lift, 14, P('#e9eef2')); c.drawLine(740, 250 - lift, 760, 214 - lift, P('#ffffff', 200, stroke=8))
    for i in range(3):
        k = (t * .6 + i / 3) % 1; sx = 770 + i * 30
        s = skia.Path(); s.moveTo(sx, 268 - k * 30); s.quadTo(sx + 10, 256 - k * 30, sx, 246 - k * 30); c.drawPath(s, P('#ffffff', 160 * (1 - k), stroke=4))
    sparkle(c, 866, 196 - lift, 22 * abs(math.sin(t * 3)), 255)


# ---------------------------------------------------------------- 6:00 PM
def rain(c, t, n=46, a=110):
    for i in range(n):
        x = (i * 137 + t * 520) % 1240 - 80; y = (i * 71 + t * 1500 + i * i * 13) % 600 - 60
        c.drawLine(x, y, x - 12, y + 40, P('#cfe2f5', a, stroke=4))


def pm_intern(c, t):
    c.drawRect(skia.Rect.MakeLTRB(-20, -60, W + 20, FL), grad(0, 0, 0, FL, ['#232b3a', '#3b475b']))
    for bx, bw, bh in ((0, 150, 190), (170, 110, 260), (700, 130, 220), (850, 250, 160)):  # far buildings
        c.drawRect(skia.Rect.MakeXYWH(bx, FL - bh, bw, bh), P('#2b3546'))
        for r in range(int(bh / 50)):
            for q in range(int(bw / 40)):
                if (r + q + bx) % 3 == 0: rr(c, bx + 12 + q * 40, FL - bh + 16 + r * 50, 16, 24, 2, P('#ffe9a8', 150))
    c.drawRect(skia.Rect.MakeLTRB(-20, FL, W + 20, 700), P('#1c222b')); c.drawRect(skia.Rect.MakeLTRB(-20, FL, W + 20, FL + 12), P('#56616f'))
    # street lamp
    c.drawLine(930, FL, 930, 60, P('#11161c', stroke=10, cap=False)); c.drawLine(930, 60, 860, 60, P('#11161c', stroke=10)); rr(c, 820, 52, 70, 22, 8, P('#11161c'))
    cone = _poly([(830, 74), (880, 74), (990, FL), (720, FL)]); c.drawPath(cone, P('#ffe7a0', 34)); c.drawOval(skia.Rect.MakeXYWH(826, 66, 58, 16), P('#fff0b8'))
    # bus shelter: roof, glass, bench, sign
    rr(c, 280, 70, 430, 22, 8, P('#4b5869')); c.drawLine(300, 92, 300, FL, P('#4b5869', stroke=12, cap=False)); c.drawLine(690, 92, 690, FL, P('#4b5869', stroke=12, cap=False))
    rr(c, 306, 100, 378, 230, 6, P('#9fc4dc', 50)); c.drawLine(330, 120, 400, 300, P('#ffffff', 40, stroke=10))
    rr(c, 330, FL - 80, 220, 16, 6, P('#6b7a8c')); c.drawLine(350, FL - 64, 350, FL, P('#6b7a8c', stroke=8)); c.drawLine(530, FL - 64, 530, FL, P('#6b7a8c', stroke=8))
    c.drawLine(760, FL, 760, 96, P('#8ea2b1', stroke=10, cap=False)); rr(c, 716, 70, 130, 100, 14, P('#2f6fd6')); rr(c, 716, 70, 130, 100, 14, P('#ffffff', stroke=6))
    rr(c, 744, 88, 74, 40, 8, P('#ffffff')); rr(c, 752, 94, 58, 16, 3, P('#2f6fd6')); c.drawCircle(760, 130, 7, P('#ffffff')); c.drawCircle(802, 130, 7, P('#ffffff'))
    text(c, 'BUS', 781, 160, 24, '#ffffff', 900, 'c')
    doctor(c, 610, 462, .62, 'intern', t, la=6, ra=-6, mood='tired')
    rain(c, t)
    for i, px in enumerate((180, 470, 840)):  # puddle ripples
        k = (t * 1.2 + i / 3) % 1
        c.drawOval(skia.Rect.MakeXYWH(px - 70, FL + 40, 140, 24), P('#2f3a48')); c.drawOval(skia.Rect.MakeXYWH(px - 50 * k, FL + 52 - 8 * k, 100 * k, 16 * k), P('#cfe2f5', 160 * (1 - k), stroke=3))
    for i in range(2):  # drips off his chin
        k = (t * 1.4 + i / 2) % 1; c.drawOval(skia.Rect.MakeXYWH(560 + i * 96, 250 + k * 120, 8, 14), P('#9fd0f2', 230 * (1 - k)))


def pm_director(c, t):
    sunset(c, 520, FL - 120, t, ('#3a2f8a', '#b0508f', '#f2707a', '#ffc37d'))
    drv = _poly([(360, FL), (760, FL), (W + 200, 620), (120, 620)]); c.drawPath(drv, P('#c9cdd3'))
    mansion(c, 20, FL + 6, .5, t); palm(c, 1010, FL + 4, t, 230)
    doctor(c, 440, 468, .6, 'director', t, la=10, ra=-150 + math.sin(t * 6) * 10)
    # key fob in the raised hand, blip
    k = (t * 1.3) % 1
    c.drawCircle(524, 150, 16 + 34 * k, P('#fff6d8', 200 * (1 - k), stroke=5))
    supercar(c, 566, 486, .98, t)
    for i in range(2):
        kk = (t * 1.3 + .1) % 1; rr(c, 582, 396, 34, 16, 8, P('#fff3b0', 255 * (1 - kk))); c.drawCircle(580, 404, 40, P('#fff3b0', 90 * (1 - kk), blur=16))


# ---------------------------------------------------------------- 11:00 PM
def night_intern(c, t):
    on = 0.0 if (int(t * 13) % 9 in (2, 3) or int(t * 29) % 17 == 5) else 1.0   # the tube light flickers
    backdrop(c, ['#1d2b33', '#16222a'], '#121b21', '#26363f')
    rr(c, 420, 20, 400, 22, 8, P('#39464f')); rr(c, 440, 34, 360, 14, 7, P('#eafcff', 90 + 165 * on))
    cone = _poly([(440, 48), (800, 48), (1000, FL), (240, FL)]); c.drawPath(cone, P('#c9f6fb', 8 + 30 * on))
    c.drawCircle(160, 160, 46, P('#26363f')); c.drawCircle(160, 160, 46, P('#3d4f5a', stroke=6))   # wall clock, hands near 11
    c.drawLine(160, 160, 146, 136, P('#9fb2c2', stroke=6)); c.drawLine(160, 160, 160, 124, P('#9fb2c2', stroke=4))
    doctor(c, 470, 470, .62, 'intern', t, la=20, ra=-26 + math.sin(t * 9) * 5, mood='tired')
    c.drawRect(skia.Rect.MakeXYWH(-20, 150, W + 40, 320), P('#0c1418', 70 * (1 - on)))
    # desk, monitor, tower of charts, cold coffee
    rr(c, 250, 300, 720, 26, 8, P('#5b6b76')); c.drawRect(skia.Rect.MakeXYWH(270, 326, 680, 300), P('#3a4852'))
    rr(c, 640, 110, 250, 170, 14, P('#0b1218')); rr(c, 652, 122, 226, 146, 8, P('#16303a'))
    c.drawCircle(765, 195, 150, P('#7fe3ff', 36, blur=40))
    text(c, 'CHARTS DUE', 664, 152, 20, '#7fe3ff', 900)
    for i in range(5):
        rr(c, 664, 166 + i * 19, 150 - (i * 37) % 70, 9, 4, P('#7fe3ff', 200)); rr(c, 838, 164 + i * 19, 14, 12, 3, P('#3ee08a' if i < 1 else '#e5484d'))
    if int(t * 2.5) % 2: rr(c, 664 + 150 - (4 * 37) % 70 + 6, 240, 4, 12, 1, P('#ffffff'))
    rr(c, 742, 280, 46, 22, 4, P('#0b1218')); rr(c, 700, 294, 130, 10, 5, P('#0b1218'))
    for i in range(9):
        rr(c, 300 + (i * 7) % 16, 284 - i * 16, 150, 14, 3, P('#f1ece2' if i % 2 else '#dcd6ca')); rr(c, 300 + (i * 7) % 16, 284 - i * 16, 20, 14, 3, P(['#e5484d', '#f5b83d', '#17b3a3'][i % 3]))
    rr(c, 560, 256, 44, 46, 8, P('#f4f1ea')); c.drawArc(skia.Rect.MakeXYWH(592, 264, 26, 26), -90, 180, False, P('#f4f1ea', stroke=6)); c.drawOval(skia.Rect.MakeXYWH(564, 258, 36, 10), P('#3b2a20'))
    rr(c, 440, 296, 150, 10, 4, P('#26323a'))  # keyboard


def night_director(c, t):
    backdrop(c, ['#2a1e3d', '#3c2750'], '#2a1a2a', GOLD)
    # night window with the moon
    rr(c, 530, 40, 170, 210, 8, P(GOLD)); rr(c, 540, 50, 150, 190, 4, P('#0e1630')); c.drawCircle(630, 110, 30, P('#fff6d8')); c.drawCircle(642, 101, 26, P('#0e1630'))
    for i, (sx, sy) in enumerate(((560, 90), (580, 190), (600, 150), (664, 200))): c.drawCircle(sx, sy, 3, P('#ffffff', 150 + 100 * math.sin(t * 3 + i)))
    c.drawLine(615, 50, 615, 240, P(GOLD, stroke=6, cap=False))
    # fireplace
    rr(c, 730, 120, 260, FL - 120, 10, P('#e9e2d4')); rr(c, 710, 104, 300, 30, 8, P('#fbf8f2')); rr(c, 772, 190, 176, FL - 190, 12, P('#1a1016'))
    c.drawCircle(860, FL - 60, 170, P('#ffb23d', 60, blur=50))
    for i in range(5):
        fx = 800 + i * 30; fh = 70 + 40 * abs(math.sin(t * 7 + i * 1.7))
        fl = skia.Path(); fl.moveTo(fx - 22, FL - 14); fl.quadTo(fx - 26, FL - fh * .5, fx, FL - 14 - fh); fl.quadTo(fx + 26, FL - fh * .5, fx + 22, FL - 14); fl.close()
        c.drawPath(fl, P('#ff7a2e' if i % 2 else '#ffb23d'))
    rr(c, 786, FL - 22, 150, 16, 8, P('#5a3a22'))
    c.drawOval(skia.Rect.MakeXYWH(40, FL + 6, 700, 56), P('#b3243a'))
    # recliner with Dr John Smith stretched out, feet up
    fx, fy, sc, ang = 640, FL - 108, .5, -72
    ux, uy = math.sin(math.radians(ang)), -math.cos(math.radians(ang))      # along the body, feet -> head
    nx, ny = -uy, ux                                                         # into the cushion
    if ny < 0: nx, ny = -nx, -ny
    a = (fx - ux * 30 + nx * 62, fy - uy * 30 + ny * 62); b = (fx + ux * 330 + nx * 62, fy + uy * 330 + ny * 62)
    c.drawLine(b[0] - 20, b[1] + 10, b[0] + 40, FL, P('#5a3a22', stroke=16)); c.drawLine(a[0], a[1], a[0] - 20, FL, P('#5a3a22', stroke=16))
    c.drawLine((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[0] + b[0]) / 2, FL, P('#5a3a22', stroke=16))
    c.drawLine(*a, *b, P('#c9975f', stroke=54)); c.drawLine(a[0] + ux * 8, a[1] + uy * 8 - 6, b[0] - ux * 8, b[1] - uy * 8 - 6, P('#e8c79a', stroke=30))
    c.drawCircle(b[0] - nx * 40, b[1] - ny * 40, 40, P('#e8c79a'))            # head rest
    rr(c, a[0] - 30, a[1] - 26, 150, 40, 18, P('#c9975f'))                    # foot rest
    ra = -112 + math.sin(t * 2.2) * 6
    lying(c, fx, fy, sc, 'director', t, ang=ang, la=14, ra=ra)
    # gold watch glint on the raised wrist
    r = math.radians(ra); dx, dy = (84 - 128 * math.sin(r)) * sc, (-380 + 128 * math.cos(r)) * sc; th = math.radians(ang)
    wx, wy = fx + dx * math.cos(th) - dy * math.sin(th), fy + dx * math.sin(th) + dy * math.cos(th)
    sparkle(c, wx, wy, 20 + 22 * abs(math.sin(t * 3)), 255, '#fff6d8'); c.drawCircle(wx, wy, 60, P('#ffd774', 60, blur=20))
    # side table: a cup of tea
    rr(c, 90, FL - 120, 150, 14, 6, P(GOLD)); c.drawLine(165, FL - 106, 165, FL, P(GOLD, stroke=10)); rr(c, 120, FL - 6, 90, 10, 5, P(GOLD))
    rr(c, 136, FL - 164, 50, 44, 10, P('#ffffff')); c.drawArc(skia.Rect.MakeXYWH(176, FL - 156, 26, 26), -90, 180, False, P('#ffffff', stroke=6))
    for i in range(2):
        k = (t * .5 + i / 2) % 1; sx = 150 + i * 22
        s = skia.Path(); s.moveTo(sx, FL - 172 - k * 40); s.quadTo(sx + 10, FL - 186 - k * 40, sx, FL - 200 - k * 40); c.drawPath(s, P('#ffffff', 150 * (1 - k), stroke=4))


# ---------------------------------------------------------------- frame layout
MOMENTS = [('6:00 AM', 6.0, am_intern, am_director, 'Wake-up call.', 'Floor mattress or king bed?'),
           ('12:00 PM', 12.0, noon_intern, noon_director, 'Lunch break.', "Vending machine or chef's table?"),
           ('6:00 PM', 18.0, pm_intern, pm_director, 'The ride home.', 'Bus stop or supercar?'),
           ('11:00 PM', 23.0, night_intern, night_director, 'Lights out?', 'Still charting or feet up?')]
DUR = [3.5, 2.6, 2.6, 2.6, 2.6, 2.6, 2.9]
START = [sum(DUR[:i]) for i in range(len(DUR))]


def panel(c, y, h, draw, t, dx=0.0, dy=0.0):
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, y, W, h)); c.translate(dx, y + dy); draw(c, t); c.restore()


def base(c, T):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#0b1624', NAVY]))
    c.drawCircle(540, 300, 420, P(TEAL, 26, blur=110))
    scenes._ecg(c, 0, W, 1750, T, TEAL, a=60, amp=40, w=5)


def clock(c, cy, label, hours, k=1.0, roll=1.0, old=None, spin=None):
    """Time stamp in the divider: analog face + digital time. roll 0..1 rolls the old label out and the new one in."""
    if k <= 0: return
    w, h = 470, 116
    c.save(); c.translate(540, cy); c.scale(k, k)
    rr(c, -w / 2, -h / 2 + 8, w, h, h / 2, P('#000000', 110, blur=18)); rr(c, -w / 2, -h / 2, w, h, h / 2, P('#ffffff')); rr(c, -w / 2, -h / 2, w, h, h / 2, P(TEAL, stroke=8))
    fx = -w / 2 + 66; c.drawCircle(fx, 0, 40, P(INK)); c.drawCircle(fx, 0, 32, P('#ffffff'))
    for i in range(12):
        a = i * math.pi / 6; c.drawLine(fx + math.cos(a) * 25, math.sin(a) * 25, fx + math.cos(a) * 29, math.sin(a) * 29, P('#8a9bab', stroke=3))
    hh = hours if spin is None else spin
    ah = math.radians((hh % 12) * 30 - 90); am = math.radians((hh % 1) * 360 - 90)
    c.drawLine(fx, 0, fx + math.cos(ah) * 16, math.sin(ah) * 16, P(INK, stroke=7)); c.drawLine(fx, 0, fx + math.cos(am) * 25, math.sin(am) * 25, P('#e5484d', stroke=5)); c.drawCircle(fx, 0, 5, P(INK))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(-w / 2 + 112, -h / 2 + 8, w - 130, h - 16))
    tx = 56
    if old is not None and roll < 1: text(c, old, tx, 24 - roll * 96, fit(old, 66, 300), INK, 900, 'c')
    text(c, label, tx, 24 + (1 - roll) * 96, fit(label, 66, 300), INK, 900, 'c')
    c.restore(); c.restore()


def split(c, T, top, bot, top_h=PH, bot_y=BOT_Y, bot_h=BH, dx=0.0, sdy=0.0, nxt=None):
    """Draw the two halves. nxt = (top, bot) of the incoming pair while both pairs slide left by -dx."""
    panel(c, TOP_Y, top_h, top, T, dx, sdy); panel(c, bot_y, bot_h, bot, T, dx, sdy)
    if nxt: panel(c, TOP_Y, top_h, nxt[0], T, dx + W, sdy); panel(c, bot_y, bot_h, nxt[1], T, dx + W, sdy)
    for y0, y1 in ((TOP_Y, TOP_Y + top_h), (bot_y, bot_y + bot_h)):
        c.drawRect(skia.Rect.MakeXYWH(0, y0 - 5, W, 10), P('#ffffff')); c.drawRect(skia.Rect.MakeXYWH(0, y1 - 5, W, 10), P('#ffffff'))
    c.drawRect(skia.Rect.MakeLTRB(0, TOP_Y + top_h + 5, W, bot_y - 5), P(NAVY))


def roles(c, bot_y=BOT_Y, k1=1.0, k2=1.0):
    pill(c, 144, TOP_Y + 58, 'INTERN', '#ffffff', INK, 38, k1); pill(c, 196, bot_y + 64, 'ED DIRECTOR', GOLD, INK, 38, k2)


def hook(c, t):
    T = START[0] + t
    base(c, T); split(c, T, intern_portrait, director_portrait)
    roles(c, BOT_Y, 1 + .12 * math.sin(clamp((t - .15) / .4) * math.pi), 1 + .12 * math.sin(clamp((t - .4) / .4) * math.pi))
    clock(c, 1040, '24 HOURS', 0, 1 + .08 * math.sin(clamp(t / .5) * math.pi), spin=t * 9)
    title2(c, 'Same 24 hours.', 'Intern vs ED Director.', 356, size=108, sub_size=84); brand_bar(c)


def moment(i):
    label, hours, top, bot, h1, h2 = MOMENTS[i]
    prev = MOMENTS[i - 1] if i else None
    def f(c, t):
        T = START[i + 1] + t; base(c, T)
        k = eio(t / .42)
        if k < 1: split(c, T, prev[2] if prev else intern_portrait, prev[3] if prev else director_portrait, dx=-W * k, nxt=(top, bot))
        else: split(c, T, top, bot)
        roles(c)
        old = prev[0] if prev else '24 HOURS'; ph = prev[1] if prev else 0.0
        if ph > hours: ph -= 24
        r = eio(t / .42)
        clock(c, 1040, label, hours, 1 + .08 * math.sin(clamp(t / .5) * math.pi), roll=r, old=old, spin=lerp(ph, hours, r))
        a = ease(t / .3)
        title2(c, h1, h2, 356, a=255 * a, dy=(1 - a) * 30, size=104, sub_size=76); brand_bar(c)
    return f


def climb_state(t):
    p = lerp(1, 5, eio((t - .55) / 1.5)); x = p - 1; j = min(3, int(x))
    return min(4, max(0, math.ceil(p - 1e-6) - 1)), lerp(BANK[j], BANK[j + 1], x - j), p


def closing(c, t):
    T = START[5] + t; base(c, T)
    e = eio((t - .1) / .45); k = eio(t / .42)
    th, by, bh = lerp(PH, 410, e), lerp(BOT_Y, 1180, e), lerp(BH, 470, e)
    if k < 1: split(c, T, MOMENTS[3][2], MOMENTS[3][3], th, by, bh, dx=-W * k, sdy=-70 * e, nxt=(intern_portrait, director_portrait))
    else: split(c, T, intern_portrait, director_portrait, th, by, bh, sdy=-70 * e)
    roles(c, by)
    clock(c, lerp(1040, 1044, e), '11:00 PM', 23.0, 1 - eio(t / .3))
    if e > 0:
        r, bank, p = climb_state(t)
        hud(c, r, bank, p, y=932, a=255 * e, bump=abs(math.sin(t * 9)) * .5 if 1 < p < 5 else 0)
    a = ease(t / .3)
    title2(c, 'Same doctor.', '4 promotions apart.', 356, a=255 * a, dy=(1 - a) * 30, size=108, sub_size=84); brand_bar(c)


SC = [(hook, DUR[0])] + [(moment(i), DUR[i + 1]) for i in range(4)] + [(closing, DUR[5]), (cta2('Start on the floor mattress.', 'Climb to ED Director.'), DUR[6])]

VOICE = [(0.12, 'Same twenty four hours. Intern, versus E.D. Director.', 3.2), (START[1] + .12, 'Six A.M. Mattress, or king bed?', 2.36),
         (START[2] + .12, 'Noon. Vending machine, or chef\'s table?', 2.36), (START[3] + .12, 'Six P.M. Bus stop, or supercar?', 2.36),
         (START[4] + .12, 'Eleven P.M. Still charting, or feet up?', 2.36), (START[5] + .12, 'Same doctor. Four promotions apart.', 2.36),
         (START[6] + .25, 'Bedside Bay. Play free.', 2.6)]


def soundtrack(wav):
    import sound
    cues = [(.15, 'pop'), (.4, 'pop'), (.1, 'tick'), (.35, 'tick'), (.6, 'tick')]
    for i in range(4):
        s = START[i + 1]; cues += [(s - .12, 'whoosh'), (s + .1, 'tick'), (s + .25, 'tick'), (s + .42, 'ding' if i % 2 == 0 else 'pop')]
    cues += [(START[1] + .5, 'beep'), (START[1] + .75, 'beep'), (START[2] + .9, 'cash')]
    s = START[5]; cues += [(s - .12, 'whoosh')] + [(s + q, f'step:{j + 1}') for j, q in enumerate((.85, 1.2, 1.55, 1.95))] + [(s + 2.0, 'cash'), (s + 1.5, 'riser')]
    cues += [(START[6], 'impact'), (START[6] + .05, 'ding')]
    return sound.build(wav, sum(DUR), 'bright', drop=START[1], lift=START[4], cta=START[6], cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i == 6: flash(c, t)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 2.0), (1, 0.2), (1, 1.6), (2, 1.6), (3, 1.6), (4, 1.6), (5, 0.3), (5, 2.3), (6, 2.5)]
        fr = [frame(compose(i), t) for i, t in pts]
        contact_sheet(fr, sys.argv[2], 5)
        if len(sys.argv) > 3:
            for n, s in enumerate(fr): save_jpg(s, f'{sys.argv[3]}/f{n}.jpg')
    elif sys.argv[1] == 'phonemes':
        import sound
        for _, line, _ in VOICE: print(line, '->', sound.phonemes(line))
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
