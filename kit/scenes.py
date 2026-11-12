"""Illustrated career-mode scenes. Each draws the full background + stage for time t (seconds)."""
import math, skia
from lib import *


def _ecg(c, x0, x1, y, t, col, a=255, amp=46, w=6, speed=260, period=210):
    p = skia.Path(); first = True
    x = x0
    while x <= x1:
        ph = ((x + t * speed) % period) / period
        if ph < .1: dy = -math.sin(ph / .1 * math.pi) * amp * .18
        elif .2 < ph < .25: dy = (ph - .2) / .05 * amp * .25
        elif .25 <= ph < .3: dy = amp * .25 - (ph - .25) / .05 * amp * 1.25
        elif .3 <= ph < .36: dy = -amp + (ph - .3) / .06 * amp * 1.3
        elif .36 <= ph < .4: dy = amp * .3 - (ph - .36) / .04 * amp * .3
        elif .5 < ph < .68: dy = -math.sin((ph - .5) / .18 * math.pi) * amp * .28
        else: dy = 0
        (p.moveTo if first else p.lineTo)(x, y + dy); first = False; x += 4
    c.drawPath(p, P(col, a, stroke=w))


def poor(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#2a333f', '#1b212a']))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), P('#2e2620'))
    for i in range(6):
        c.drawLine(0, 1190 + i * 130, W, 1190 + i * 130, P('#241d18', stroke=4))
    c.drawRect(skia.Rect.MakeXYWH(0, 1136, W, 16), P('#39424e'))
    # wall cracks + damp patch
    cr = skia.Path(); cr.moveTo(960, 520); cr.lineTo(930, 600); cr.lineTo(965, 660); cr.lineTo(940, 740); cr.lineTo(972, 800)
    c.drawPath(cr, P('#141a21', stroke=5))
    c.drawOval(skia.Rect.MakeXYWH(40, 900, 260, 150), P('#1d242d', 160, blur=24))
    # window
    rr(c, 110, 570, 230, 280, 10, P('#414c59')); rr(c, 124, 584, 202, 252, 6, P('#0e1522'))
    c.drawCircle(270, 650, 30, P('#dfe6f0')); c.drawCircle(282, 642, 26, P('#0e1522'))
    for sx, sy in ((160, 620), (200, 700), (300, 760), (150, 790)):
        c.drawCircle(sx, sy, 3, P('#ffffff', 150 + 100 * math.sin(t * 3 + sx)))
    c.drawLine(225, 584, 225, 836, P('#414c59', stroke=10, cap=False)); c.drawLine(124, 710, 326, 710, P('#414c59', stroke=10, cap=False))
    # rent notice
    c.save(); c.rotate(5, 900, 690); rr(c, 810, 620, 190, 140, 6, P('#f1ece2'))
    text(c, 'RENT', 905, 680, 44, '#d64545', 900, 'c'); text(c, 'OVERDUE', 905, 730, 34, '#d64545', 900, 'c')
    rr(c, 880, 608, 50, 22, 4, P('#c9b98f', 220)); c.restore()
    # bare bulb
    ang = math.sin(t * 1.7) * 7
    c.save(); c.translate(470, 500); c.rotate(ang)
    c.drawLine(0, 0, 0, 150, P('#11161c', stroke=6)); rr(c, -14, 146, 28, 26, 5, P('#555f6b'))
    c.drawCircle(0, 196, 150, P('#ffe7a0', 46 + 10 * math.sin(t * 9), blur=60)); c.drawCircle(0, 196, 30, P('#fff0b8'))
    c.restore()
    # mattress on the floor
    rr(c, 50, 1096, 430, 78, 26, P('#b6ae9f'))
    for i in range(7): c.drawLine(96 + i * 54, 1104, 96 + i * 54, 1166, P('#9c9484', stroke=4))
    rr(c, 66, 1056, 150, 58, 24, P('#dcd6ca')); rr(c, 240, 1078, 240, 74, 30, P('#5f6f82'))
    # instant noodles
    cup = skia.Path(); cup.moveTo(868, 1100); cup.lineTo(968, 1100); cup.lineTo(954, 1196); cup.lineTo(882, 1196); cup.close()
    c.drawPath(cup, P('#f4f1ea')); rr(c, 862, 1090, 112, 18, 8, P('#e3ded3'))
    band = skia.Path(); band.moveTo(872, 1128); band.lineTo(964, 1128); band.lineTo(959, 1164); band.lineTo(877, 1164); band.close()
    c.drawPath(band, P('#d64545'))
    for i in range(3):
        k = (t * .5 + i / 3) % 1; sx = 890 + i * 28
        s = skia.Path(); s.moveTo(sx, 1082 - k * 70); s.quadTo(sx + 14, 1064 - k * 70, sx, 1046 - k * 70)
        s.quadTo(sx - 14, 1028 - k * 70, sx, 1010 - k * 70)
        c.drawPath(s, P('#ffffff', 120 * (1 - k), stroke=5))
    doctor(c, 640, 1218, 1.0, 'intern', t, la=7, ra=-7, mood='tired')


def er(c, t, outfit=None):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#e3f2f5', '#c6e2e8']))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), P('#aecbd4'))
    c.drawRect(skia.Rect.MakeXYWH(0, 880, W, 14), P('#9fd4cf'))
    # curtain
    rr(c, 0, 512, 210, 14, 4, P('#7f93a3'))
    for i in range(5):
        rr(c, i * 40 - 6, 524, 44, 640, 20, P('#35a39a' if i % 2 == 0 else '#2b8f87'))
    # monitor on a pole
    c.drawLine(940, 760, 940, 1150, P('#8ea2b1', stroke=12, cap=False)); rr(c, 890, 1140, 100, 16, 8, P('#8ea2b1'))
    rr(c, 800, 590, 240, 176, 20, P('#0b1218')); rr(c, 812, 602, 216, 152, 12, P('#101c24'))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(816, 606, 208, 144)); _ecg(c, 816, 1024, 668, t, '#3ee08a', amp=34, w=5, speed=200, period=150)
    c.restore(); text(c, '76', 826, 742, 40, '#3ee08a', 800); text(c, '99%', 1014, 742, 34, '#4cc3f0', 800, 'r')
    # bed with patient
    for bx in (420, 900):
        c.drawLine(bx, 1040, bx, 1140, P('#93a7b5', stroke=12, cap=False)); c.drawCircle(bx, 1150, 16, P('#5d6f7d'))
    rr(c, 372, 1010, 576, 44, 14, P('#93a7b5')); rr(c, 380, 968, 560, 56, 22, P('#ffffff'))
    rr(c, 930, 880, 22, 170, 10, P('#93a7b5'))
    rr(c, 800, 930, 130, 54, 24, P('#eef4f7'))
    c.drawCircle(858, 926, 42, P('#e6b48c')); arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(814, 880, 88, 88), 190, 170)
    c.drawPath(arc, P('#b5532c', stroke=16)); c.drawLine(846, 926, 852, 926, P('#3a2a22', stroke=5)); c.drawLine(868, 926, 874, 926, P('#3a2a22', stroke=5))
    c.drawArc(skia.Rect.MakeXYWH(848, 932, 24, 16), 20, 140, False, P('#8a4b3a', stroke=4))
    rr(c, 400, 940, 420, 84, 34, P('#8ec6ea')); rr(c, 400, 940, 420, 26, 13, P('#b9dcf3'))
    o = outfit or ('intern' if t < 1.55 else 'resident')
    doctor(c, 270, 1218, 1.0, o, t, la=8, ra=-62 + math.sin(t * 5) * 9, mood='ok' if o == 'intern' else 'happy')
    if outfit is None and 1.45 < t < 2.0:  # promotion flash
        k = (t - 1.45) / .55
        c.drawCircle(270, 900, 120 + 320 * k, P('#ffffff', 190 * (1 - k), blur=30))
        for i in range(6):
            a = i * math.pi / 3 + t; sparkle(c, 270 + math.cos(a) * (150 + 120 * k), 900 + math.sin(a) * (170 + 120 * k), 22, 255 * (1 - k), GOLD)


def theatre(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1300, ['#10424d', '#07222a']))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), P('#0a2c34'))
    for i in range(12):  # wall tiles
        c.drawLine(i * 98, 500, i * 98, 1150, P('#ffffff', 10, stroke=3))
    _ecg(c, 0, W, 1105, t, TEAL, a=70, amp=30, w=4)
    for lx in (300, 780):  # surgical lamps
        c.drawLine(lx, 480, lx, 600, P('#8fa6b3', stroke=12, cap=False))
        cone = skia.Path(); cone.moveTo(lx - 110, 640); cone.lineTo(lx + 110, 640); cone.lineTo(540 + (lx - 540) * .2 + 190, 1010)
        cone.lineTo(540 + (lx - 540) * .2 - 190, 1010); cone.close()
        c.drawPath(cone, P('#c9f6fb', 26))
        c.drawOval(skia.Rect.MakeXYWH(lx - 124, 596, 248, 76), P('#c7d6de')); c.drawOval(skia.Rect.MakeXYWH(lx - 104, 612, 208, 52), P('#f3fdff'))
        c.drawOval(skia.Rect.MakeXYWH(lx - 104, 612, 208, 52), P('#bff4fb', 120, blur=26))
    doctor(c, 540, 1218, 1.0, 'surgeon', t, la=-24 + math.sin(t * 6) * 5, ra=24 - math.sin(t * 6 + 1) * 5)
    # operating table in front of the surgeon
    rr(c, 492, 1070, 96, 90, 10, P('#73889a')); rr(c, 400, 1150, 280, 22, 11, P('#5d7082'))
    rr(c, 210, 1024, 660, 54, 20, P('#a9bbc8'))
    dr = skia.Path(); dr.moveTo(240, 1030); dr.cubicTo(300, 930, 520, 940, 600, 960); dr.cubicTo(700, 930, 800, 960, 840, 1030); dr.close()
    c.drawPath(dr, P('#2fa69c')); c.drawPath(dr, P('#208f86', stroke=5))
    rr(c, 470, 972, 140, 44, 18, P('#e9fbf9', 235))
    # instrument tray
    rr(c, 80, 1010, 110, 14, 6, P('#c8d5dd')); c.drawLine(135, 1024, 135, 1150, P('#8fa6b3', stroke=8, cap=False))
    for i in range(3): c.drawLine(100 + i * 30, 1006, 108 + i * 30, 968, P('#e9f1f5', stroke=6))


def rich(c, t, car_in=True):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1130, ['#272b73', '#8a4a94', '#f2707a', '#ffc37d']))
    c.drawCircle(800, 900, 210, P('#ffe2a6', 90, blur=70)); c.drawCircle(800, 900, 112, P('#fff0c4'))
    for i, (sx, sy) in enumerate(((90, 560), (980, 600), (620, 540), (860, 700), (400, 620))):
        c.drawCircle(sx, sy, 4, P('#ffffff', 130 + 110 * math.sin(t * 3 + i)))
    hill = skia.Path(); hill.moveTo(0, 1080); hill.quadTo(300, 980, 620, 1070); hill.quadTo(860, 1010, W, 1060); hill.lineTo(W, 1140); hill.lineTo(0, 1140); hill.close()
    c.drawPath(hill, P('#5b3f86', 200))
    c.drawRect(skia.Rect.MakeXYWH(0, 1120, W, H - 1120), grad(0, 1120, 0, 1500, ['#2e9f6b', '#1c7a50']))
    drv = skia.Path(); drv.moveTo(40, 1150); drv.lineTo(640, 1150); drv.lineTo(W + 200, 1500); drv.lineTo(-200, 1500); drv.close()
    c.drawPath(drv, P('#c9cdd3'))
    # palm
    tr = skia.Path(); tr.moveTo(1010, 1124); tr.quadTo(985, 900, 1030, 740); c.drawPath(tr, P('#7a5636', stroke=26))
    for ang in (-150, -110, -60, -20, 30, 200):
        a = math.radians(ang + math.sin(t * 1.5 + ang) * 3); f = skia.Path(); f.moveTo(1030, 740)
        f.quadTo(1030 + math.cos(a) * 90, 740 + math.sin(a) * 90 - 50, 1030 + math.cos(a) * 190, 740 + math.sin(a) * 150 + 20)
        c.drawPath(f, P('#1f8f57', stroke=24))
    # mansion: modern two-storey with glowing glass
    rr(c, 150, 640, 330, 190, 8, P('#fbf8f2')); c.drawRect(skia.Rect.MakeXYWH(126, 622, 378, 26), P('#34414f'))
    rr(c, 50, 812, 560, 312, 8, P('#f4f0e8')); c.drawRect(skia.Rect.MakeXYWH(26, 794, 608, 28), P('#34414f'))
    glow = 220 + 30 * math.sin(t * 2)
    for wx, wy, ww, wh in ((176, 672, 130, 120), (322, 672, 130, 120), (84, 860, 150, 200), (430, 860, 150, 200)):
        rr(c, wx, wy, ww, wh, 6, P('#ffd98a', glow)); c.drawLine(wx + ww / 2, wy, wx + ww / 2, wy + wh, P('#34414f', stroke=5, cap=False))
        c.drawLine(wx, wy + wh * .5, wx + ww, wy + wh * .5, P('#34414f', stroke=5, cap=False))
    rr(c, 276, 900, 112, 224, 8, P('#34414f')); c.drawCircle(366, 1016, 7, P(GOLD))
    for px in (262, 402): rr(c, px - 10, 880, 20, 244, 6, P('#e2dccf'))
    rr(c, 30, 1108, 600, 22, 6, P('#d9d3c6'))
    doctor(c, 780, 1236, .98, 'director', t, la=10, ra=-158 + math.sin(t * 6) * 14)
    k = (t * .9) % 1  # watch glint
    sparkle(c, 912, 742, 36 * math.sin(k * math.pi), 255, '#fff6d8')
    # supercar
    slide = (1 - ease((t - .25) / 1.0)) * 760 if car_in else 0
    c.save(); c.translate(-slide - 440, -26 + math.sin(t * 22) * (1.5 if slide > 4 else 0)); c.translate(1520, 0); c.scale(-1, 1)
    c.drawOval(skia.Rect.MakeXYWH(560, 1262, 400, 36), P('#000000', 70, blur=10))
    body = skia.Path(); body.moveTo(556, 1250); body.lineTo(552, 1214); body.quadTo(600, 1178, 680, 1170)
    body.quadTo(730, 1116, 810, 1116); body.quadTo(880, 1118, 910, 1166); body.quadTo(962, 1176, 966, 1214); body.lineTo(966, 1250); body.close()
    c.drawPath(body, grad(0, 1116, 0, 1250, ['#ff4d4d', '#c01f2e']))
    win = skia.Path(); win.moveTo(700, 1170); win.quadTo(738, 1132, 806, 1132); win.quadTo(858, 1134, 884, 1168); win.close()
    c.drawPath(win, P('#1c2530')); c.drawLine(796, 1132, 796, 1168, P('#c01f2e', stroke=7, cap=False))
    rr(c, 556, 1206, 34, 14, 7, P('#fff3b0')); rr(c, 944, 1204, 22, 14, 6, P('#ffb3b3'))
    c.drawLine(600, 1232, 920, 1232, P('#8f1420', stroke=5))
    for wx in (640, 880):
        c.drawCircle(wx, 1250, 42, P('#14181d')); c.drawCircle(wx, 1250, 24, P('#cfd6dd'))
        c.save(); c.rotate(-t * 300 if slide > 4 else 0, wx, 1250)
        for i in range(5):
            a = i * 2 * math.pi / 5; c.drawLine(wx, 1250, wx + math.cos(a) * 22, 1250 + math.sin(a) * 22, P('#7b8894', stroke=5))
        c.restore()
    sparkle(c, 760, 1150, 26 * abs(math.sin(t * 3)), 255)
    c.restore()
    # falling gold coins
    for i in range(9):
        k = (t * .45 + i * .137) % 1; x = (i * 211 + 97) % 1000 + 40; y = 500 + k * 640
        c.drawCircle(x, y, 20, P(GOLD, 230 * (1 - k * .5))); c.drawCircle(x, y, 13, P('#ffd774', 230 * (1 - k * .5)))


def cta(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, W, H, [NAVY, '#0e4b55']))
    c.drawCircle(540, 620, 520, P(TEAL, 34, blur=120))
    _ecg(c, 0, W, 1440, t, TEAL, a=90, amp=60, w=6)
    k = pop(t / .5)
    c.save(); c.translate(540, 560); c.scale(k, k); logo(c, -110, -110, 220); c.restore()
    a = 255 * ease((t - .2) / .4)
    text(c, 'Bedside Bay', 540, 810, 118, '#ffffff', 900, 'c', a=a)
    text(c, 'Start as a broke intern.', 540, 900, 54, '#bfe9e4', 700, 'c', a=a)
    text(c, 'Retire as ED Director.', 540, 966, 54, '#bfe9e4', 700, 'c', a=a)
    b = pop((t - .6) / .5) * (1 + .03 * math.sin(t * 6))
    if t > .6:
        c.save(); c.translate(540, 1110); c.scale(b, b)
        rr(c, -290, -62 + 10, 580, 132, 66, P('#000000', 80, blur=20)); rr(c, -290, -66, 580, 132, 66, P(TEAL))
        text(c, 'Play free', 0, 22, 66, '#ffffff', 900, 'c'); c.restore()
    text(c, 'bedsidebay.com', 540, 1260, 56, '#ffffff', 800, 'c', a=255 * ease((t - .9) / .4))
