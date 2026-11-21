"""Broke to Rich photo set 11 — "How Dr John Smith gets to work. At every rank." One slide per rank, told through the
commute: on foot in the rain (Intern), the early bus (Resident), a bicycle (Registrar), a first real car (Consultant), the
supercar (ED Director), then the Play free card. Bank amounts after the $2,000 start and the cars are illustrative.
Usage: python3 b2r_11_ride_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
from fullgame_02 import OUT, BANK

GY = 1190  # street level


def street(c, sky, ground, kerb, glow=None, stars=False, hospital=True):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, GY, sky))
    if glow: c.drawCircle(glow[0], glow[1], 230, P(glow[2], 110, blur=80)); c.drawCircle(glow[0], glow[1], 96, P(glow[3]))
    if stars:
        for i in range(14): c.drawCircle((i * 263 + 90) % 1040 + 20, 560 + (i * 97) % 300, 3 + i % 2, P('#ffffff', 150))
    # skyline
    for i, (x, w, h) in enumerate(((0, 150, 250), (130, 120, 360), (240, 170, 210), (400, 110, 300), (500, 160, 180))):
        c.drawRect(skia.Rect.MakeXYWH(x, GY - h, w, h), P('#000000', 46))
        for r in range(int(h / 60) - 1):
            for q in range(int(w / 50)):
                if (i + r + q) % 3: rr(c, x + 16 + q * 50, GY - h + 24 + r * 60, 22, 30, 3, P('#ffe9a8', 70))
    if hospital:  # the hospital he is heading for
        rr(c, 700, GY - 470, 380, 480, 10, P('#e9eef3')); c.drawRect(skia.Rect.MakeXYWH(684, GY - 486, 420, 26), P('#b9c6d2'))
        for r in range(4):
            for q in range(3): rr(c, 734 + q * 110, GY - 420 + r * 84, 70, 52, 6, P('#9fd3db' if (r + q) % 2 else '#c9e8ee'))
        rr(c, 800, GY - 590, 180, 110, 16, P('#ffffff')); rr(c, 800, GY - 590, 180, 110, 16, P('#b9c6d2', stroke=5))
        c.drawRect(skia.Rect.MakeXYWH(876, GY - 572, 28, 74), P('#e5484d')); c.drawRect(skia.Rect.MakeXYWH(853, GY - 549, 74, 28), P('#e5484d'))
        rr(c, 820, GY - 110, 140, 110, 8, P('#5b7083')); text(c, 'EMERGENCY', 890, GY - 124, 28, '#e5484d', 900, 'c')
    c.drawRect(skia.Rect.MakeXYWH(0, GY - 14, W, 34), P(kerb))
    c.drawRect(skia.Rect.MakeXYWH(0, GY + 20, W, H - GY), P(ground))


def wheel(c, x, y, r, rim='#cfd6dd', tyre='#14181d', spokes=5):
    c.drawCircle(x, y, r, P(tyre)); c.drawCircle(x, y, r * .58, P(rim))
    for i in range(spokes):
        a = i * 2 * math.pi / spokes + .3; c.drawLine(x, y, x + math.cos(a) * r * .52, y + math.sin(a) * r * .52, P('#7b8894', stroke=max(3, r * .1)))
    c.drawCircle(x, y, r * .14, P('#5b6672'))


def rain(c):
    for i in range(60):
        x = (i * 137 + 40) % W; y = 560 + (i * 211) % 620
        c.drawLine(x, y, x - 14, y + 44, P('#9fc4e8', 120, stroke=4))
    for x in (150, 420, 700): c.drawOval(skia.Rect.MakeXYWH(x, GY + 60, 220, 30), P('#8fb4d6', 90))


def sneakers(c):
    """Worn sneakers close-up tile."""
    x, y = 60, 620
    rr(c, x, y + 10, 330, 250, 36, P('#000000', 90, blur=20)); rr(c, x, y, 330, 250, 36, P('#ffffff'))
    for sx, sy, rot in ((120, 110, -8), (210, 150, 6)):
        c.save(); c.translate(x + sx, y + sy); c.rotate(rot)
        rr(c, -74, -6, 150, 24, 10, P('#d9d3c6'))  # sole
        b = skia.Path(); b.moveTo(-70, -4); b.lineTo(-70, -52); b.quadTo(-40, -62, -20, -40); b.quadTo(30, -34, 70, -16); b.lineTo(74, -4); b.close()
        c.drawPath(b, P('#b9b2a4'))
        for k in range(3): c.drawLine(-22 + k * 20, -36 + k * 5, -8 + k * 20, -44 + k * 5, P('#ffffff', stroke=4))
        c.drawCircle(46, -14, 9, P('#3b2a20'))  # hole in the toe
        c.drawLine(-74, 14, -40, 20, P('#8a8172', stroke=4))  # sole peeling
        c.restore()
    text(c, 'Sneakers: on their last mile', x + 165, y + 222, 23, '#5b7083', 800, 'c')


def bus(c, x, y):
    """City bus, bottom-left of body at (x, y)."""
    c.drawOval(skia.Rect.MakeXYWH(x + 10, y + 42, 640, 34), P('#000000', 70, blur=10))
    rr(c, x, y - 300, 660, 320, 36, P('#f2a43a')); rr(c, x, y - 300, 660, 70, 30, P('#d98a1f'))
    rr(c, x + 20, y - 286, 300, 44, 10, P('#12263f')); text(c, '24  HOSPITAL', x + 170, y - 252, 32, '#ffd774', 900, 'c')
    for i in range(4): rr(c, x + 30 + i * 130, y - 216, 110, 110, 12, P('#c9e8ee'))
    rr(c, x + 556, y - 216, 78, 216, 10, P('#c9e8ee')); c.drawLine(x + 595, y - 216, x + 595, y, P('#d98a1f', stroke=6, cap=False))
    c.drawRect(skia.Rect.MakeXYWH(x, y - 84, 550, 14), P('#ffffff'))
    rr(c, x + 640, y - 60, 24, 30, 6, P('#fff3b0'))
    wheel(c, x + 130, y + 26, 52); wheel(c, x + 500, y + 26, 52)


def bus_pass(c):
    x, y = 620, 610
    c.save(); c.rotate(-6, x + 170, y + 100)
    rr(c, x, y + 10, 340, 200, 24, P('#000000', 90, blur=18)); rr(c, x, y, 340, 200, 24, P('#ffffff')); rr(c, x, y, 340, 62, 24, P(TEAL))
    c.drawRect(skia.Rect.MakeXYWH(x, y + 40, 340, 22), P(TEAL))
    text(c, 'MONTHLY BUS PASS', x + 170, y + 42, 28, '#ffffff', 900, 'c')
    text(c, 'J. SMITH', x + 26, y + 116, 44, INK, 900); text(c, 'Resident  ·  Route 24', x + 26, y + 164, 28, '#5b7083', 800)
    c.restore()


def bike(c, x, y):
    """Bicycle, centre between wheels at x, ground y."""
    r = 92; ax, bx_ = x - 150, x + 150; wy = y - r
    c.drawOval(skia.Rect.MakeXYWH(x - 250, y - 10, 500, 30), P('#000000', 70, blur=10))
    for wx in (ax, bx_):
        c.drawCircle(wx, wy, r, P('#14181d', stroke=14))
        for i in range(10):
            a = i * math.pi / 5; c.drawLine(wx, wy, wx + math.cos(a) * r, wy + math.sin(a) * r, P('#cfd6dd', 200, stroke=3))
        c.drawCircle(wx, wy, 12, P('#7b8894'))
    fr = P(TEAL, stroke=16); cr = (x - 10, wy + 6); seat = (x - 50, wy - 140); head = (x + 104, wy - 150)
    for p, q in ((ax, wy), cr), (cr, seat), (seat, (ax, wy)), (seat, head), (cr, head), (head, (bx_, wy)):
        c.drawLine(p[0], p[1], q[0], q[1], fr)
    c.drawLine(seat[0], seat[1], seat[0] - 8, seat[1] - 36, P('#5b6672', stroke=10)); rr(c, seat[0] - 56, seat[1] - 56, 100, 24, 12, P('#14181d'))
    c.drawLine(head[0], head[1], head[0] - 10, head[1] - 56, P('#5b6672', stroke=10)); c.drawLine(head[0] - 46, head[1] - 60, head[0] + 30, head[1] - 52, P('#14181d', stroke=14))
    c.drawCircle(cr[0], cr[1], 26, P('#5b6672')); c.drawLine(cr[0], cr[1], cr[0] + 34, cr[1] + 40, P('#14181d', stroke=10)); rr(c, cr[0] + 16, cr[1] + 36, 50, 14, 6, P('#14181d'))


def car(c, x, y, kind):
    """Side-on car facing right, centre x, ground y. kind: sedan | super."""
    c.save(); c.translate(x, y)
    if kind == 'sedan':
        c.drawOval(skia.Rect.MakeXYWH(-330, 0, 660, 40), P('#000000', 70, blur=10))
        body = skia.Path(); body.moveTo(-320, -30); body.lineTo(-320, -120); body.quadTo(-300, -150, -230, -156); body.quadTo(-170, -262, -60, -266)
        body.lineTo(90, -266); body.quadTo(170, -260, 220, -160); body.quadTo(310, -150, 322, -110); body.lineTo(322, -30); body.close()
        c.drawPath(body, grad(0, -266, 0, -30, ['#4a8fd9', '#2b62a8']))
        win = skia.Path(); win.moveTo(-196, -160); win.quadTo(-150, -240, -60, -242); win.lineTo(84, -242); win.quadTo(150, -238, 190, -160); win.close()
        c.drawPath(win, P('#c9e8ee')); c.drawLine(-10, -242, -10, -160, P('#2b62a8', stroke=10, cap=False))
        c.drawLine(-300, -70, 300, -70, P('#1f4a82', stroke=6)); rr(c, 296, -128, 28, 22, 8, P('#fff3b0')); rr(c, -322, -126, 18, 24, 6, P('#ffb3b3'))
        rr(c, -30, -140, 44, 10, 5, P('#1f4a82')); wheel(c, -190, -30, 60); wheel(c, 200, -30, 60)
    else:
        c.drawOval(skia.Rect.MakeXYWH(-390, 0, 780, 40), P('#000000', 80, blur=10))
        body = skia.Path(); body.moveTo(-380, -24); body.lineTo(-386, -96); body.quadTo(-300, -160, -150, -170); body.quadTo(-60, -264, 90, -264)
        body.quadTo(220, -260, 276, -172); body.quadTo(372, -154, 380, -90); body.lineTo(380, -24); body.close()
        c.drawPath(body, grad(0, -264, 0, -24, ['#ff4d4d', '#c01f2e']))
        win = skia.Path(); win.moveTo(-112, -172); win.quadTo(-44, -238, 84, -238); win.quadTo(182, -234, 226, -172); win.close()
        c.drawPath(win, P('#1c2530')); c.drawLine(60, -238, 60, -172, P('#c01f2e', stroke=10, cap=False))
        rr(c, 334, -112, 46, 22, 10, P('#fff3b0')); rr(c, -386, -104, 30, 22, 8, P('#ffb3b3')); c.drawLine(-290, -56, 300, -56, P('#8f1420', stroke=8))
        rr(c, -396, -180, 80, 16, 8, P('#8f1420')); c.drawLine(-360, -170, -350, -110, P('#8f1420', stroke=10))  # spoiler
        wheel(c, -220, -30, 68, rim=GOLD); wheel(c, 236, -30, 68, rim=GOLD)
        sparkle(c, -30, -226, 34); sparkle(c, 340, -150, 22, col='#fff6d8')
    c.restore()


def tag(c, x, y, label):
    """Small white note with a gold edge."""
    w = tw(label, 34, 800) + 56
    rr(c, x, y + 6, w, 66, 18, P('#000000', 80, blur=12)); rr(c, x, y, w, 66, 18, P('#ffffff')); rr(c, x, y, 14, 66, 7, P(GOLD))
    text(c, label, x + 34, y + 45, 34, INK, 800)


def count(c, i):
    c.drawCircle(960, 190, 50, P(GOLD)); text(c, f'{i}/5', 960, 205, 38, INK, 900, 'c')


def finish(c, i, top, sub, col='#ffffff', top_col=GOLD, note='Swipe: the ride gets better'):
    title2(c, top, sub, 356, col, top_col, shadow=0 if col == INK else .45)
    hud(c, i, BANK[i], i + 1); brand_bar(c); count(c, i + 1)
    pill(c, 330, 1554, note, '#ffffff', INK, 34); swipe(c, 700, 1516)


def s1(c):
    street(c, ['#1a2130', '#2b3546'], '#20262f', '#39424e', stars=False)
    c.drawRect(skia.Rect.MakeWH(W, GY), P('#0a0f18', 70)); rain(c)
    doctor(c, 520, GY + 60, .8, 'intern', 1.0, la=24, ra=-22, mood='tired')
    sneakers(c)
    title2(c, 'How Dr John Smith', 'gets to work. Every rank.', 356, size=100, sub_size=76, shadow=.5)
    tag(c, 60, 900, '1. Intern: on foot')
    hud(c, 0, BANK[0], 1); brand_bar(c); count(c, 1)
    pill(c, 330, 1554, 'Starts with $2,000', '#ffffff', INK, 34); swipe(c, 700, 1516)


def s2(c):
    street(c, ['#2c3e6b', '#7a6f9c', '#f0a987'], '#3a414b', '#59636f', glow=(250, 1010, '#ffd9a0', '#ffe9c4'), hospital=False)
    bus(c, 350, GY - 30)
    rr(c, 250, GY - 430, 14, 440, 6, P('#8ea2b1')); rr(c, 196, GY - 500, 122, 96, 16, P('#2b62a8')); text(c, 'BUS', 257, GY - 438, 40, '#ffffff', 900, 'c')
    doctor(c, 150, GY + 50, .74, 'resident', 1.4, la=10, ra=-150, mood='happy')
    bus_pass(c)
    finish(c, 1, '2. Resident', 'The early bus.', note='Swipe: an upgrade')


def s3(c):
    street(c, ['#6fc3e8', '#bfe6f2'], '#4a525d', '#6b7682', glow=(200, 720, '#fff3c4', '#fffbe6'))
    for x in (90, 380): c.drawOval(skia.Rect.MakeXYWH(x, 600 + (x % 60), 230, 60), P('#ffffff', 210))
    bike(c, 440, GY + 60)
    doctor(c, 190, GY + 50, .74, 'surgeon', .6, la=10, ra=-40, mood='happy')
    tag(c, 420, 760, 'Own wheels. Two of them.')
    finish(c, 2, '3. Registrar', 'Bought a bike.', INK, TEAL_D, note='Swipe: more wheels')


def s4(c):
    street(c, ['#3d8fd1', '#a9dcf0'], '#454d58', '#6b7682', glow=(180, 700, '#fff3c4', '#fffbe6'))
    rr(c, 70, GY - 330, 12, 340, 6, P('#8ea2b1')); rr(c, 30, GY - 420, 220, 100, 14, P('#ffffff')); rr(c, 30, GY - 420, 220, 100, 14, P('#2b62a8', stroke=6))
    text(c, 'RESERVED', 140, GY - 376, 30, '#2b62a8', 900, 'c'); text(c, 'Dr J. Smith', 140, GY - 340, 28, INK, 800, 'c')
    car(c, 450, GY + 50, 'sedan')
    doctor(c, 900, GY + 56, .7, 'consultant', 1.4, la=10, ra=-150, mood='happy')
    finish(c, 3, '4. Consultant', 'First real car.', INK, '#1f4a82', note='Swipe: one more')


def s5(c):
    street(c, ['#272b73', '#8a4a94', '#f2707a', '#ffc37d'], '#3a3f49', '#c9cdd3', glow=(300, 960, '#ffe2a6', '#fff0c4'))
    for i in range(7):
        x = (i * 173 + 80) % 980 + 40; y = 600 + (i * 131) % 330
        c.drawCircle(x, y, 20, P(GOLD, 220)); c.drawCircle(x, y, 13, P('#ffd774', 220))
    car(c, 430, GY + 50, 'super')
    doctor(c, 930, GY + 56, .7, 'director', 2.6, la=10, ra=-158)
    title2(c, '5. ED Director', 'Parks out front.', 356, shadow=.5)
    hud(c, 4, BANK[4], 5); brand_bar(c); count(c, 5)
    pill(c, 330, 1554, 'Same doctor. Same shift.', '#ffffff', INK, 34); swipe(c, 700, 1516)


def slides():
    return [s1, s2, s3, s4, s5, lambda c: cta2('Start on foot.', 'Finish in the fast lane.')(c, 2.8)]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
