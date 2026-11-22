"""Broke to Rich photo set 14 — "Rating every bed Dr John Smith has slept in." One slide per rank as a star-rated review:
the mattress on the floor (Intern, 1 star), the on-call bunk (Resident, 2), a first real bed frame (Registrar, 3), a
queen bed with a city view (Consultant, 4), the king canopy bed in the mansion (ED Director, 5), then the Play free card.
Bank amounts after the $2,000 start and the furniture are illustrative.
Usage: python3 b2r_14_beds_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
from fullgame_02 import OUT, BANK

GY = 1196  # floor level


def star(c, cx, cy, r, col):
    p = skia.Path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rad = r if i % 2 == 0 else r * .45
        (p.lineTo if i else p.moveTo)(cx + math.cos(a) * rad, cy + math.sin(a) * rad)
    p.close(); c.drawPath(p, P(col))


def review(c, x, y, i, quote, w=500):
    """Star-rating card: BED i OF 5, i gold stars out of five, a one-line review."""
    h = 236
    rr(c, x, y + 10, w, h, 34, P('#000000', 100, blur=22)); rr(c, x, y, w, h, 34, P('#ffffff'))
    text(c, f'BED {i} OF 5', x + 34, y + 52, 28, '#8a9bab', 900); text(c, f'{i}.0', x + w - 34, y + 58, 44, INK, 900, 'r')
    for j in range(5): star(c, x + 64 + j * 78, y + 112, 36, GOLD if j < i else '#dfe7ee')
    text(c, quote, x + 34, y + 204, fit(quote, 38, w - 68, 800), INK, 800)


def room(c, wall, floor, skirt):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, GY, wall))
    c.drawRect(skia.Rect.MakeXYWH(0, GY, W, H - GY), P(floor)); c.drawRect(skia.Rect.MakeXYWH(0, GY - 16, W, 18), P(skirt))


def bed(c, x, y, w, leg=44, frame='#8a5a34', mat=54, matc='#f4f1ea', blanket='#5f8fd9', fold='#8fb2ea', pillows=1, head=170, foot=70, headw=40):
    """Side-on bed, headboard on the left. x = left of frame, y = floor."""
    fy = y - leg - 34
    c.drawOval(skia.Rect.MakeXYWH(x - 20, y - 14, w + 40, 34), P('#000000', 60, blur=10))
    for lx in (x + 8, x + w - 40): rr(c, lx, fy + 10, 32, leg + 26, 8, P(frame))
    rr(c, x - headw + 26, fy - mat - head, headw, head + mat + 34, 14, P(frame))
    rr(c, x + w - 26, fy - mat - foot, 34, foot + mat + 34, 12, P(frame))
    rr(c, x, fy, w, 34, 10, P(frame))
    rr(c, x + 22, fy - mat, w - 44, mat + 6, 20, P(matc))
    for i in range(pillows): rr(c, x + 34 + i * 20, fy - mat - 40 - i * 26, w * .24, 50, 25, P('#ffffff')); rr(c, x + 34 + i * 20, fy - mat - 40 - i * 26, w * .24, 50, 25, P('#d5dde5', stroke=3))
    bx = x + w * .36; rr(c, bx, fy - mat - 14, w - (bx - x) - 24, mat + 36, 22, P(blanket)); rr(c, bx, fy - mat - 14, 60, mat + 36, 22, P(fold))
    return fy - mat


def finish(c, i, top, sub, col='#ffffff', top_col=GOLD, note='Swipe: it gets comfier', shadow=.45):
    title2(c, top, sub, 356, col, top_col, shadow=shadow)
    hud(c, i, BANK[i], i + 1); brand_bar(c)
    pill(c, 330, 1554, note, '#ffffff', INK, 34); swipe(c, 700, 1516)


def s1(c):
    scenes.poor(c, 1.0)
    review(c, 40, 560, 1, '“Springs included. In my back.”', 480)
    title2(c, 'Rating every bed', 'Dr John Smith has slept in.', 356, size=104, sub_size=76, shadow=.5)
    hud(c, 0, BANK[0], 1); brand_bar(c)
    pill(c, 330, 1554, '1. Intern: floor mattress', '#ffffff', INK, 34); swipe(c, 700, 1516)


def s2(c):
    room(c, ['#dcecf0', '#bcd9e0'], '#9fb8c2', '#8ea2b1')
    # bunk bed
    x, w = 70, 620
    for px in (x, x + w - 30): rr(c, px, GY - 600, 30, 600, 8, P('#7f93a3'))
    for lvl in (0, 1):
        fy = GY - 110 - lvl * 300
        rr(c, x, fy, w, 30, 8, P('#7f93a3')); rr(c, x + 34, fy - 50, w - 68, 54, 18, P('#f4f1ea'))
        rr(c, x + 50, fy - 86, 150, 44, 22, P('#ffffff')); rr(c, x + 50, fy - 86, 150, 44, 22, P('#d5dde5', stroke=3))
        rr(c, x + 240, fy - 62, w - 290, 70, 20, P('#35a39a' if lvl == 0 else '#8ea2b1')); rr(c, x + 240, fy - 62, 54, 70, 20, P('#7fd0c6' if lvl == 0 else '#b9c6d2'))
    for r in range(4): rr(c, x + w - 4, GY - 520 + r * 120, 70, 14, 6, P('#7f93a3'))
    rr(c, x + w + 56, GY - 560, 20, 560, 8, P('#7f93a3'))
    # pager on the lower pillow
    rr(c, x + 86, GY - 232, 84, 54, 10, P('#12263f')); rr(c, x + 94, GY - 224, 50, 26, 5, P('#3ee08a'))
    for j in range(3): c.drawArc(skia.Rect.MakeXYWH(x + 128 - 30 - j * 22, GY - 250 - 30 - j * 22, 60 + j * 44, 60 + j * 44), -80, 60, False, P('#e5484d', 230 - j * 60, stroke=8))
    # wall clock 3:00 and door sign
    c.drawCircle(900, 660, 84, P('#ffffff')); c.drawCircle(900, 660, 84, P('#5b7083', stroke=8))
    c.drawLine(900, 660, 900, 606, P(INK, stroke=8)); c.drawLine(900, 660, 940, 660, P(INK, stroke=10)); c.drawCircle(900, 660, 8, P(INK))
    text(c, '3:00 AM', 900, 792, 36, INK, 900, 'c')
    doctor(c, 900, GY + 50, .72, 'resident', 2.0, la=8, ra=-10, mood='tired')
    review(c, 50, 540, 2, '“The pager sleeps here too.”')
    finish(c, 1, '2. Resident', 'The on-call bunk.', INK, TEAL_D, shadow=0)


def s3(c):
    room(c, ['#f6e7d2', '#ebd3b2'], '#b98556', '#8a5a34')
    for i in range(5): c.drawLine(0, GY + 60 + i * 70, W, GY + 60 + i * 70, P('#a57448', stroke=4))
    bed(c, 90, GY, 600, frame='#8a5a34', blanket='#17a394', fold='#7fd0c6', head=190)
    # bedside crate with lamp, plant
    rr(c, 20, GY - 120, 90, 120, 8, P('#c9975f')); c.drawLine(20, GY - 80, 110, GY - 80, P('#a57448', stroke=4)); c.drawLine(20, GY - 40, 110, GY - 40, P('#a57448', stroke=4))
    c.drawLine(64, GY - 120, 64, GY - 200, P('#5b6672', stroke=8)); lamp = skia.Path(); lamp.moveTo(30, GY - 200); lamp.lineTo(98, GY - 200); lamp.lineTo(84, GY - 262); lamp.lineTo(44, GY - 262); lamp.close()
    c.drawCircle(64, GY - 220, 90, P('#ffe7a0', 90, blur=40)); c.drawPath(lamp, P('#f5b83d'))
    rr(c, 720, GY - 90, 90, 90, 12, P('#d98a5f'))
    for ang in (-130, -100, -70, -45, -155):
        a = math.radians(ang); f = skia.Path(); f.moveTo(765, GY - 90); f.quadTo(765 + math.cos(a) * 70, GY - 90 + math.sin(a) * 120, 765 + math.cos(a) * 150, GY - 90 + math.sin(a) * 190)
        c.drawPath(f, P('#1f8f57', stroke=22))
    # framed certificate
    rr(c, 640, 600, 220, 160, 8, P('#8a5a34')); rr(c, 654, 614, 192, 132, 4, P('#fbf7ee')); text(c, 'REGISTRAR', 750, 668, 26, INK, 900, 'c')
    rr(c, 690, 690, 120, 10, 5, P('#c3cfda')); rr(c, 710, 712, 80, 10, 5, P('#c3cfda'))
    doctor(c, 930, GY + 50, .72, 'surgeon', .6, la=10, ra=-150, mood='happy')
    review(c, 50, 540, 3, '“Off the floor at last.”')
    finish(c, 2, '3. Registrar', 'A real bed frame.', INK, TEAL_D, note='Swipe: bigger', shadow=0)


def s4(c):
    room(c, ['#22305a', '#3b4d80'], '#4b5568', '#2b3550')
    # big window, city at night
    rr(c, 590, 560, 440, 420, 12, P('#d5dde5')); rr(c, 606, 576, 408, 388, 6, P('#0e1630'))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(606, 576, 408, 388))
    c.drawCircle(940, 650, 34, P('#fff6d8'))
    for i, (bx, bw, bh) in enumerate(((606, 80, 200), (680, 70, 290), (756, 96, 170), (850, 64, 250), (920, 100, 210))):
        c.drawRect(skia.Rect.MakeXYWH(bx, 964 - bh, bw, bh), P('#1c2a55'))
        for r in range(int(bh / 44)):
            for q in range(int(bw / 30)):
                if (i + r + q) % 3: rr(c, bx + 8 + q * 30, 964 - bh + 14 + r * 44, 14, 22, 2, P('#ffe9a8', 220))
    c.restore()
    c.drawLine(810, 576, 810, 964, P('#d5dde5', stroke=10, cap=False))
    rr(c, 0, GY + 30, W, 60, 0, P('#566178'))
    top = bed(c, 60, GY, 720, leg=36, frame='#3a4756', mat=70, blanket='#e8eef6', fold='#ffffff', pillows=2, head=300, foot=20, headw=56)
    rr(c, 44, top - 290, 44, 290, 16, P('#8fa6c9'))
    for j in range(3): c.drawCircle(66, top - 240 + j * 80, 7, P('#6f88ad'))
    # bedside table + lamp
    rr(c, 800, GY - 130, 130, 130, 10, P('#3a4756')); c.drawCircle(865, GY - 66, 8, P(GOLD))
    c.drawLine(865, GY - 130, 865, GY - 210, P('#c9d2da', stroke=8)); c.drawCircle(865, GY - 250, 110, P('#ffe7a0', 100, blur=44))
    lamp = skia.Path(); lamp.moveTo(820, GY - 210); lamp.lineTo(910, GY - 210); lamp.lineTo(894, GY - 290); lamp.lineTo(836, GY - 290); lamp.close(); c.drawPath(lamp, P('#fff0b8'))
    doctor(c, 990, GY + 56, .7, 'consultant', 1.4, la=10, ra=-12, mood='happy')
    review(c, 50, 540, 4, '“Eight hours. Uninterrupted.”')
    finish(c, 3, '4. Consultant', 'Queen size. City view.', note='Swipe: one more')


def s5(c):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, GY, ['#3a1f5c', '#6b2f6f']))
    # arched window with sunset
    arch = skia.Path(); arch.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(610, 540, 420, 470), 210, 210)); arch.addRect(skia.Rect.MakeXYWH(610, 760, 420, 250))
    c.save(); c.clipPath(arch, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(610, 540, 420, 470), grad(0, 540, 0, 1010, ['#272b73', '#f2707a', '#ffc37d']))
    c.drawCircle(820, 900, 80, P('#fff0c4')); c.drawRect(skia.Rect.MakeXYWH(610, 950, 420, 60), P('#1c7a50'))
    c.restore(); rr(c, 610, 540, 420, 470, 210, P(GOLD, stroke=12)); c.drawRect(skia.Rect.MakeXYWH(604, 1000, 432, 16), P(GOLD))
    c.drawRect(skia.Rect.MakeXYWH(0, GY, W, H - GY), P('#4a2340')); c.drawRect(skia.Rect.MakeXYWH(0, GY - 16, W, 18), P(GOLD))
    c.drawOval(skia.Rect.MakeXYWH(-40, GY + 6, 900, 70), P('#b3243a')); c.drawOval(skia.Rect.MakeXYWH(-10, GY + 14, 840, 54), P('#d13a52'))
    # canopy bed
    x, w = 60, 720
    top = bed(c, x, GY, w, leg=40, frame=GOLD, mat=84, matc='#fff8ea', blanket='#b3243a', fold='#ffd774', pillows=3, head=250, foot=120, headw=50)
    for px in (x - 20, x + w - 22): rr(c, px, GY - 410, 30, 410, 10, P(GOLD)); c.drawCircle(px + 15, GY - 420, 24, P('#ffd774'))
    rr(c, x - 40, GY - 410, w + 68, 44, 16, P(GOLD))
    for i in range(9):
        cx_ = x - 20 + i * (w + 28) / 8; c.drawCircle(cx_, GY - 366, 44, P('#b3243a'))
    rr(c, x - 40, GY - 410, w + 68, 30, 12, P(GOLD))
    dr = skia.Path(); dr.moveTo(x + 10, GY - 370); dr.quadTo(x + 130, GY - 300, x + 10, GY - 250); dr.close(); c.drawPath(dr, P('#8f1c2e'))
    dr = skia.Path(); dr.moveTo(x + w - 10, GY - 370); dr.quadTo(x + w - 130, GY - 310, x + w - 10, GY - 280); dr.close(); c.drawPath(dr, P('#8f1c2e'))
    for sx, sy, r in ((420, 730, 30), (700, 800, 22), (240, 860, 20), (560, 560, 24)): sparkle(c, sx, sy, r, 255, '#fff6d8')
    doctor(c, 960, GY + 56, .7, 'director', 2.6, la=10, ra=-158)
    review(c, 50, 540, 5, '“Never getting up.”')
    title2(c, '5. ED Director', 'King size. Mansion wing.', 356, shadow=.5)
    hud(c, 4, BANK[4], 5); brand_bar(c)
    pill(c, 330, 1554, 'Same doctor. Better sleep.', '#ffffff', INK, 34); swipe(c, 700, 1516)


def slides():
    return [s1, s2, s3, s4, s5, lambda c: cta2('Start on the floor.', 'Wake up in the mansion.')(c, 2.8)]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
