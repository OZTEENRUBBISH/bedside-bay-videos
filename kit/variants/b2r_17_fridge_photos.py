"""Broke to Rich photo set 17 — "What's in his fridge? Dr John Smith. Every rank." One open fridge per rank, the fridge
and its contents upgrading with the career: a dented mini-fridge with one ketchup packet (Intern), takeout leftovers and
energy drinks (Resident), a proper fridge with actual vegetables and eggs (Registrar), a tidy fridge of labeled meal prep
(Consultant), a double-door fridge stocked by a private chef in the mansion kitchen (ED Director), then the Play free card.
Dr John Smith stands beside each one with a one-line comment. Bank amounts after the $2,000 start, the fridges and the
mansion are illustrative.
Usage: python3 b2r_17_fridge_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
from fullgame_02 import OUT, BANK

GY = 1196  # floor level


# ---------------------------------------------------------------- fridge
def fridge(c, x, w, h, body, edge, inner=('#f7fbff', '#dcebf5'), doors='l', dw=None, leg=14, handle='#c9d2da', glow=120):
    """Open fridge seen from the front, standing on the floor. x = left of the body. doors: 'l', 'r' or 'lr' (swung open,
    seen at an angle beside the body). Returns the interior rect (ix, iy, iw, ih)."""
    y = GY - leg - h; dw = dw or w * .34
    c.drawOval(skia.Rect.MakeXYWH(x - 30 - (dw if 'l' in doors else 0), GY - 16, w + 60 + (dw if 'l' in doors else 0) + (dw if 'r' in doors else 0), 38), P('#000000', 70, blur=12))
    for lx in (x + 14, x + w - 44): rr(c, lx, GY - leg - 6, 30, leg + 6, 5, P('#2f3b47'))
    for side in doors:
        dx = x - dw + 6 if side == 'l' else x + w - 6
        d = skia.Path()
        if side == 'l': d.moveTo(dx, y - 22); d.lineTo(dx + dw, y); d.lineTo(dx + dw, y + h); d.lineTo(dx, y + h + 26)
        else: d.moveTo(dx, y); d.lineTo(dx + dw, y - 22); d.lineTo(dx + dw, y + h + 26); d.lineTo(dx, y + h)
        d.close(); c.drawPath(d, P(body)); c.drawPath(d, P(edge, stroke=6))
        # inside face of the door: liner and bins
        ins = 16; l = skia.Path()
        if side == 'l': l.moveTo(dx + ins, y - 22 + ins + 8); l.lineTo(dx + dw - ins, y + ins + 4); l.lineTo(dx + dw - ins, y + h - ins - 4); l.lineTo(dx + ins, y + h + 26 - ins - 8)
        else: l.moveTo(dx + ins, y + ins + 4); l.lineTo(dx + dw - ins, y - 22 + ins + 8); l.lineTo(dx + dw - ins, y + h + 26 - ins - 8); l.lineTo(dx + ins, y + h - ins - 4)
        l.close(); c.drawPath(l, P(inner[1]))
    c.drawCircle(x + w / 2, y + h * .45, w * .75, P('#fff6d8', glow * .5, blur=70))
    rr(c, x, y, w, h, 26, P(body)); rr(c, x, y, w, h, 26, P(edge, stroke=6))
    m = max(18, w * .06); ix, iy, iw, ih = x + m, y + m, w - 2 * m, h - 2 * m
    rr(c, ix, iy, iw, ih, 14, grad(0, iy, 0, iy + ih, list(inner)))
    rr(c, ix + iw / 2 - 40, iy + 6, 80, 12, 6, P('#fff6d8')); c.drawCircle(ix + iw / 2, iy + 20, 70, P('#fff6d8', glow, blur=30))
    return ix, iy, iw, ih


def door_bins(c, x, w, h, n, side='l', dw=None, leg=14, col='#c9dbe8'):
    """Bin rails on the open door; returns [(bx, by, bw)] = the floor of each bin, top to bottom."""
    y = GY - leg - h; dw = dw or w * .34; dx = (x - dw + 6 if side == 'l' else x + w - 6) + 22; bw = dw - 44; out = []
    for i in range(n):
        by = y + h * (i + 1) / (n + .35)
        out.append((dx, by, bw))
    return out


def bin_front(c, bins, col='#bcd2e2'):
    for bx, by, bw in bins: rr(c, bx - 4, by - 30, bw + 8, 36, 8, P(col, 235)); rr(c, bx - 4, by - 30, bw + 8, 36, 8, P('#93adc1', stroke=3))


def shelves(c, R, n, col='#b8d0e0'):
    """n glass shelves inside rect R; returns the y of each standing surface, top to bottom (the last is the floor)."""
    ix, iy, iw, ih = R; ys = []
    for i in range(1, n + 1):
        y = iy + ih * i / (n + 1) + 8
        rr(c, ix, y, iw, 10, 4, P(col)); rr(c, ix, y + 10, iw, 5, 2, P('#ffffff', 150)); ys.append(y)
    return ys + [iy + ih - 2]


# ---------------------------------------------------------------- food
def bottle(c, x, y, h, col, fill=1.0, w=44, cap='#ffffff', glass='#dff1f4', label=None):
    bh = h * .64
    rr(c, x + w * .32, y - h, w * .36, h * .4, 6, P(glass)); rr(c, x + w * .28, y - h - 8, w * .44, 16, 5, P(cap))
    rr(c, x, y - bh, w, bh, w * .28, P(glass))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - bh, w, bh), w * .28, w * .28), True)
    c.drawRect(skia.Rect.MakeXYWH(x, y - bh * fill, w, bh * fill), P(col)); c.restore()
    if fill >= 1: rr(c, x + w * .32, y - h + 16, w * .36, h * .4 - 16, 4, P(col))
    if label: rr(c, x, y - bh * .62, w, bh * .34, 3, P(label))
    rr(c, x + 6, y - bh + 8, 6, bh - 22, 3, P('#ffffff', 130))


def can(c, x, y, col, w=40, h=84, bolt='#fff06a'):
    rr(c, x, y - h, w, h, 9, P(col)); rr(c, x + 3, y - h - 4, w - 6, 10, 4, P('#c9d2da')); rr(c, x + 5, y - h + 10, 5, h - 22, 2, P('#ffffff', 90))
    b = skia.Path(); cx, cy = x + w / 2, y - h / 2 + 4
    for i, (px, py) in enumerate(((4, -24), (-10, 4), (-1, 4), (-5, 24), (10, -6), (1, -6))): (b.lineTo if i else b.moveTo)(cx + px, cy + py)
    b.close(); c.drawPath(b, P(bolt))


def takeout(c, x, y, w=96, h=92, col='#ffffff', mark='#e5484d', flap=True):
    p = skia.Path(); p.moveTo(x + 12, y); p.lineTo(x + w - 12, y); p.lineTo(x + w, y - h); p.lineTo(x, y - h); p.close()
    c.drawArc(skia.Rect.MakeXYWH(x + 16, y - h - 44, w - 32, 80), 180, 180, False, P('#8a9bab', stroke=4))
    c.drawPath(p, P(col)); c.drawPath(p, P('#cfd9e2', stroke=3))
    if flap:
        f = skia.Path(); f.moveTo(x, y - h); f.lineTo(x + w * .3, y - h - 30); f.lineTo(x + w * .5, y - h); f.close(); c.drawPath(f, P('#eef2f6')); c.drawPath(f, P('#cfd9e2', stroke=3))
    c.drawCircle(x + w / 2, y - h * .45, w * .2, P(mark)); c.drawCircle(x + w / 2, y - h * .45, w * .09, P(col))


def foil(c, x, y, w=150, h=44):
    rr(c, x, y - h, w, h, 8, P('#c9d2da')); rr(c, x - 6, y - h - 8, w + 12, 16, 6, P('#e4eaf0'))
    for i in range(5): c.drawLine(x + 14 + i * (w - 28) / 4, y - h + 14, x + 14 + i * (w - 28) / 4, y - 8, P('#aab7c4', stroke=3))


def pizza_box(c, x, y, w=210, h=30):
    rr(c, x, y - h, w, h, 5, P('#d9b98a')); rr(c, x, y - h, w, h, 5, P('#b8935c', stroke=3)); rr(c, x + w * .38, y - h + 8, w * .24, h - 16, 4, P('#e5484d'))


def milk(c, x, y, w=62, h=120, band='#3a8fd6'):
    p = skia.Path(); p.moveTo(x, y); p.lineTo(x + w, y); p.lineTo(x + w, y - h + 26); p.lineTo(x + w / 2 + 6, y - h); p.lineTo(x + w / 2 - 6, y - h); p.lineTo(x, y - h + 26); p.close()
    c.drawPath(p, P('#ffffff')); c.drawPath(p, P('#cfd9e2', stroke=3)); c.drawRect(skia.Rect.MakeXYWH(x + 2, y - h * .52, w - 4, h * .26), P(band))


def eggs(c, x, y, n=6, r=17):
    w = n * r * 2 + 16
    for i in range(n): c.drawOval(skia.Rect.MakeXYWH(x + 8 + i * r * 2 + 2, y - 30 - r * 1.5, r * 2 - 4, r * 2.5), P('#f6e3c8'))
    rr(c, x, y - 34, w, 34, 9, P('#b9b2a4')); rr(c, x, y - 34, w, 10, 5, P('#cfc8ba'))
    return w


def carrots(c, x, y, n=3):
    """Bunch of carrots lying on a shelf, tips to the right."""
    for i in range(n):
        yy = y - i * 13; xx = x + i * 10
        for a in (-18, 0, 18):
            c.save(); c.translate(xx + 10, yy - 16); c.rotate(-90 + a); rr(c, -5, 0, 10, 38, 5, P('#2fa35b')); c.restore()
        p = skia.Path(); p.moveTo(xx + 6, yy - 30); p.quadTo(xx + 70, yy - 30, xx + 124, yy - 14); p.quadTo(xx + 70, yy - 2, xx + 6, yy - 2); p.close(); c.drawPath(p, P('#f08c2e'))
        for j in range(3): c.drawLine(xx + 30 + j * 24, yy - 24, xx + 32 + j * 24, yy - 16, P('#d2741c', stroke=3))


def lettuce(c, x, y, r=46):
    for dx, dy, rr_, col in ((0, 0, 1, '#4fb86a'), (-.45, .1, .7, '#6fd086'), (.45, .1, .7, '#6fd086'), (0, -.25, .7, '#8fe0a0'), (-.2, .2, .45, '#3ea45a'), (.25, .25, .4, '#3ea45a')):
        c.drawCircle(x + dx * r, y - r + dy * r, r * rr_, P(col))


def tomato(c, x, y, r=26, col='#e5484d'):
    c.drawCircle(x, y - r, r, P(col)); c.drawCircle(x - r * .3, y - r * 1.3, r * .22, P('#ffffff', 110))
    for a in (-60, -90, -120): c.drawLine(x, y - r * 1.9, x + math.cos(math.radians(a)) * 12, y - r * 1.9 - math.sin(math.radians(a)) * -8, P('#2fa35b', stroke=5))


def broccoli(c, x, y, s=1.0):
    rr(c, x - 9 * s, y - 44 * s, 18 * s, 44 * s, 7 * s, P('#7fc77a'))
    for dx, dy, r in ((0, -70, 30), (-26, -54, 24), (26, -54, 24), (-12, -84, 20), (14, -86, 20)): c.drawCircle(x + dx * s, y + dy * s, r * s, P('#2f8f4f'))
    for dx, dy in ((-8, -74), (12, -62), (-22, -56)): c.drawCircle(x + dx * s, y + dy * s, 6 * s, P('#4fb86a'))


def jar(c, x, y, col, w=58, h=78, lid='#e5484d'):
    rr(c, x, y - h, w, h, 10, P('#eaf4f8')); rr(c, x + 4, y - h + 16, w - 8, h - 20, 8, P(col)); rr(c, x - 3, y - h - 10, w + 6, 18, 6, P(lid)); rr(c, x + 8, y - h + 22, 6, h - 34, 3, P('#ffffff', 120))


def prep(c, x, y, day, food, w=128, h=66, lid='#17b3a3'):
    """Meal-prep box with a labeled lid."""
    rr(c, x, y - h, w, h, 10, P('#eef6fa')); rr(c, x + 6, y - h + 20, w - 12, h - 26, 7, P(food[0]))
    rr(c, x + 6 + (w - 12) * .55, y - h + 20, (w - 12) * .45, h - 26, 7, P(food[1]))
    rr(c, x - 4, y - h - 6, w + 8, 20, 7, P(lid))
    rr(c, x + w / 2 - 38, y - h + 24, 76, 30, 5, P('#ffffff')); text(c, day, x + w / 2, y - h + 47, 22, INK, 900, 'c')


def cake(c, x, y, w=150):
    rr(c, x + w * .42, y - 26, w * .16, 26, 4, P(GOLD)); rr(c, x + w * .2, y - 8, w * .6, 8, 4, P(GOLD)); rr(c, x, y - 36, w, 12, 6, P(GOLD))
    rr(c, x + 14, y - 112, w - 28, 78, 12, P('#f6c9d6')); rr(c, x + 14, y - 112, w - 28, 26, 12, P('#ffffff'))
    for i in range(5): c.drawCircle(x + 30 + i * (w - 60) / 4, y - 86, 11, P('#ffffff'))
    for i in range(4): c.drawCircle(x + 38 + i * (w - 76) / 3, y - 118, 10, P('#d13a52'))


def fruit_bowl(c, x, y, w=150):
    for dx, col, r in ((.26, '#f08c2e', 26), (.5, '#e5484d', 28), (.74, '#f5d03d', 26), (.38, '#7fc77a', 22), (.62, '#8a5ad6', 22)):
        c.drawCircle(x + w * dx, y - 50 - (14 if r == 22 else 0), r, P(col))
    b = skia.Path(); b.moveTo(x, y - 50); b.lineTo(x + w, y - 50); b.quadTo(x + w * .9, y, x + w * .5, y); b.quadTo(x + w * .1, y, x, y - 50); b.close()
    c.drawPath(b, P('#ffffff')); c.drawPath(b, P(GOLD, stroke=4))


def cheese(c, x, y, w=96):
    p = skia.Path(); p.moveTo(x, y); p.lineTo(x + w, y); p.lineTo(x + w, y - 26); p.lineTo(x, y - 64); p.close(); c.drawPath(p, P('#f5c84a'))
    for dx, dy, r in ((.3, -22, 8), (.6, -14, 6), (.78, -30 + 12, 5), (.16, -40, 6)): c.drawCircle(x + w * dx, y + dy, r, P('#dba42a'))


def cloche(c, x, y, w=150):
    rr(c, x - 8, y - 14, w + 16, 14, 7, P('#c9d2da'))
    d = skia.Path(); d.addArc(skia.Rect.MakeXYWH(x, y - 14 - w * .5, w, w), 180, 180); d.close(); c.drawPath(d, P('#e8eef4'))
    c.drawArc(skia.Rect.MakeXYWH(x + 16, y - w * .5, w - 32, w - 32), 200, 70, False, P('#ffffff', 220, stroke=7)); c.drawCircle(x + w / 2, y - 14 - w * .5 - 8, 12, P(GOLD))


def chef_hat(c, cx, cy, s=1.0, col='#ffffff'):
    for dx, r in ((-22, 20), (0, 26), (22, 20)): c.drawCircle(cx + dx * s, cy - 18 * s, r * s, P(col))
    rr(c, cx - 26 * s, cy - 12 * s, 52 * s, 34 * s, 5 * s, P(col)); c.drawLine(cx - 24 * s, cy + 12 * s, cx + 24 * s, cy + 12 * s, P('#c9d2da', stroke=3 * s))


def ketchup(c, cx, cy, rot=-12, s=1.0):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    rr(c, -62, -34, 124, 72, 8, P('#000000', 60, blur=8)); rr(c, -62, -38, 124, 72, 8, P('#d92f3a'))
    for ex in (-62, 50):
        for i in range(6): c.drawLine(ex + 2, -34 + i * 13, ex + 10, -34 + i * 13, P('#a81f2a', stroke=3))
    rr(c, -44, -24, 88, 44, 6, P('#ffffff')); text(c, 'KETCHUP', 0, 6, 17, '#d92f3a', 900, 'c')
    c.restore()


# ---------------------------------------------------------------- staging
def room(c, wall, floor, skirt):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, GY, wall))
    c.drawRect(skia.Rect.MakeXYWH(0, GY, W, H - GY), P(floor)); c.drawRect(skia.Rect.MakeXYWH(0, GY - 16, W, 18), P(skirt))


def say(c, line, y=532, tail=(840, 690), size=44, x=None):
    """White speech bubble across the top of the picture with Dr John Smith's line; tail points down to him."""
    size = fit(line, size, 820, 800); w = tw(line, size, 800) + 84; h = 104; x = max(50, min(940 - w, 520 - w / 2 + 60)) if x is None else x
    t = skia.Path(); t.moveTo(tail[0] - 60, y + h - 6); t.lineTo(tail[0], tail[1]); t.lineTo(tail[0] - 4, y + h - 6); t.close()
    rr(c, x, y + 8, w, h, 46, P('#000000', 90, blur=18)); c.drawPath(t, P('#ffffff')); rr(c, x, y, w, h, 46, P('#ffffff'))
    text(c, line, x + w / 2, y + h / 2 + size * .35, size, INK, 800, 'c')


def finish(c, i, top, sub, note, col='#ffffff', top_col=GOLD, shadow=.45, last=False):
    title2(c, top, sub, 356, col, top_col, shadow=shadow)
    hud(c, i, BANK[i], i + 1); brand_bar(c)
    pill(c, 330, 1554, note, '#ffffff', INK, fit(note, 34, 480)); swipe(c, 700, 1516)


# ---------------------------------------------------------------- slides
def s1(c):
    room(c, ['#2a333f', '#1b212a'], '#2e2620', '#39424e')
    for i in range(5): c.drawLine(0, GY + 50 + i * 120, W, GY + 50 + i * 120, P('#241d18', stroke=4))
    cr = skia.Path(); cr.moveTo(120, 640); cr.lineTo(150, 720); cr.lineTo(118, 790); cr.lineTo(146, 860); c.drawPath(cr, P('#141a21', stroke=5))
    c.drawOval(skia.Rect.MakeXYWH(520, 900, 240, 140), P('#1d242d', 170, blur=24))
    # bare bulb
    c.drawLine(700, 640, 700, 720, P('#11161c', stroke=6)); rr(c, 686, 716, 28, 26, 5, P('#555f6b')); c.drawCircle(700, 766, 130, P('#ffe7a0', 44, blur=60)); c.drawCircle(700, 766, 26, P('#fff0b8'))
    # milk crate the mini-fridge stands on
    cx0, cw, ch = 200, 400, 150
    rr(c, cx0, GY - ch, cw, ch, 10, P('#3d6fa8'))
    for r in range(2):
        for q in range(5): rr(c, cx0 + 18 + q * 76, GY - ch + 18 + r * 66, 58, 48, 6, P('#28313c'))
    c.save(); c.translate(0, -ch)
    R = fridge(c, 210, 380, 400, '#e9e4d8', '#b9b2a4', inner=('#f1f5f8', '#d3dde5'), dw=140, leg=0, glow=90)
    c.restore()
    ix, iy, iw, ih = R; iy -= ch
    # dents, tape, rust
    for dx, dy, r in ((228, GY - ch - 388, 14), (580, GY - ch - 120, 12)): c.drawCircle(dx, dy, r, P('#000000', 28)); c.drawCircle(dx - 3, dy - 3, r * .6, P('#ffffff', 60))
    c.save(); c.rotate(-10, 110, GY - ch - 250); rr(c, 76, GY - ch - 270, 110, 34, 4, P('#c9b98f', 235)); c.restore()
    c.drawOval(skia.Rect.MakeXYWH(214, GY - ch - 40, 60, 26), P('#a5663a', 150, blur=5))
    ys = [iy + ih * .52, iy + ih - 2]
    rr(c, ix, ys[0], iw, 10, 4, P('#b8c6d2'))
    for i in range(7): c.drawLine(ix + 20 + i * (iw - 40) / 6, ys[0] + 2, ix + 20 + i * (iw - 40) / 6, ys[0] + 8, P('#93a3b1', stroke=3))
    bottle(c, ix + iw - 110, ys[0], 150, '#e0a23a', fill=.45, w=56, cap='#e5484d', label='#ffffff')
    ketchup(c, ix + iw * .42, ys[1] - 44, -10, 1.25)
    c.drawCircle(ix + iw * .42, ys[1] - 40, 120, P('#fff6d8', 40, blur=30))
    # cobweb in the top corner of the fridge
    for a in (10, 40, 70): c.drawLine(ix + 4, iy + 4, ix + 4 + math.cos(math.radians(a)) * 84, iy + 4 + math.sin(math.radians(a)) * 84, P('#9fb0bd', 200, stroke=2))
    for r in (34, 62): c.drawArc(skia.Rect.MakeXYWH(ix + 4 - r, iy + 4 - r, r * 2, r * 2), 8, 66, False, P('#9fb0bd', 200, stroke=2))
    doctor(c, 850, GY + 50, .72, 'intern', 1.0, la=8, ra=-10, mood='tired')
    say(c, '“Dinner is served.”')
    title2(c, 'What’s in his fridge?', 'Dr John Smith. Every rank.', 356, size=104, sub_size=76, shadow=.5)
    hud(c, 0, BANK[0], 1); brand_bar(c)
    pill(c, 330, 1554, '1. Intern: one ketchup packet', '#ffffff', INK, 32); swipe(c, 700, 1516)


def s2(c):
    room(c, ['#dcecf0', '#bcd9e0'], '#9fb8c2', '#8ea2b1')
    for i in range(9): c.drawLine(i * 135, GY, i * 135 - 60, H, P('#8fa9b4', stroke=3))
    # pizza boxes on top of the fridge
    x, w, h = 250, 380, 470
    R = fridge(c, x, w, h, '#f4f6f8', '#aab7c4', dw=130)
    for i in range(2): pizza_box(c, x + 70 + (i % 2) * 14, GY - 14 - h - i * 32, 240)
    ys = shelves(c, R, 2); ix, iy, iw, ih = R
    takeout(c, ix + 14, ys[0], 92, 84); takeout(c, ix + 118, ys[0], 80, 70, mark='#f08c2e', flap=False); foil(c, ix + 208, ys[0], 124)
    for i, col in enumerate(('#17b3a3', '#17b3a3', '#8a5ad6', '#17b3a3', '#8a5ad6', '#17b3a3')): can(c, ix + 18 + i * 52, ys[1], col, 42, 86)
    pizza_box(c, ix + 20, ys[2], 200, 30); pizza_box(c, ix + 34, ys[2] - 30, 200, 30); takeout(c, ix + 244, ys[2], 86, 80, mark='#e5484d')
    bins = door_bins(c, x, w, h, 3, dw=130)
    for (bx, by, bw), col in zip(bins, ('#8a5ad6', '#17b3a3', '#8a5ad6')): can(c, bx + 4, by, col, 34, 70); can(c, bx + 42, by, '#17b3a3', 34, 70)
    bin_front(c, bins)
    # sticky note on the takeout
    c.save(); c.rotate(-6, ix + 250, ys[0] - 120); rr(c, ix + 196, ys[0] - 150, 140, 60, 4, P('#ffe36e')); text(c, 'TUESDAY?', ix + 266, ys[0] - 111, 22, INK, 900, 'c'); c.restore()
    doctor(c, 850, GY + 50, .72, 'resident', 2.0, la=8, ra=-10, mood='tired')
    say(c, '“Some of this is still good.”')
    finish(c, 1, '2. Resident', 'Leftovers and energy drinks.', 'Swipe: it gets fresher', INK, TEAL_D, shadow=0)


def s3(c):
    room(c, ['#f6e7d2', '#ebd3b2'], '#b98556', '#8a5a34')
    for i in range(5): c.drawLine(0, GY + 60 + i * 70, W, GY + 60 + i * 70, P('#a57448', stroke=4))
    # tiled backsplash + counter on the right
    for r in range(3):
        for q in range(5): rr(c, 664 + q * 84, 800 + r * 62, 78, 56, 6, P('#fbf3e4'))
    rr(c, 650, 990, 430, 26, 6, P('#8a5a34')); rr(c, 664, 1016, 416, GY - 1016 - 16, 0, P('#d9a877'))
    for q in range(2): rr(c, 684 + q * 200, 1040, 180, 120, 8, P('#c9935f')); c.drawCircle(774 + q * 200, 1064, 7, P('#8a5a34'))
    x, w, h = 250, 380, 500
    R = fridge(c, x, w, h, '#ffffff', '#b9c4cf', dw=130)
    ys = shelves(c, R, 3); ix, iy, iw, ih = R
    milk(c, ix + 16, ys[0], 58, 96); jar(c, ix + 92, ys[0], '#d13a52', 54, 70); jar(c, ix + 158, ys[0], '#f5c84a', 54, 70, lid='#2fa35b'); bottle(c, ix + 240, ys[0], 100, '#f08c2e', w=44, cap='#f08c2e')
    eggs(c, ix + 14, ys[1], 6, 15); tomato(c, ix + 244, ys[1], 24); tomato(c, ix + 296, ys[1], 24)
    lettuce(c, ix + 62, ys[2], 44); broccoli(c, ix + 176, ys[2], .92); broccoli(c, ix + 262, ys[2], .8)
    # crisper drawer
    carrots(c, ix + 24, ys[3] - 6, 3); tomato(c, ix + 216, ys[3] - 6, 22, '#f5d03d'); tomato(c, ix + 266, ys[3] - 6, 22, '#7fc77a')
    rr(c, ix + 4, ys[3] - 62, iw - 8, 62, 10, P('#dff1f4', 40)); rr(c, ix + 4, ys[3] - 62, iw - 8, 62, 10, P('#9cc5dc', stroke=3))
    bins = door_bins(c, x, w, h, 3, dw=130)
    for i, (bx, by, bw) in enumerate(bins):
        bottle(c, bx + 2, by, 84, ('#f08c2e', '#ffffff', '#7fc77a')[i], w=34, cap='#5b7083'); jar(c, bx + 42, by, ('#8a5ad6', '#e5484d', '#f5c84a')[i], 40, 56, lid='#5b7083')
    bin_front(c, bins)
    doctor(c, 850, GY + 50, .72, 'surgeon', .6, la=8, ra=-150, mood='happy')
    say(c, '“I own actual eggs now.”')
    finish(c, 2, '3. Registrar', 'Actual vegetables.', 'Swipe: it gets organized', INK, TEAL_D, shadow=0)


def s4(c):
    room(c, ['#22305a', '#3b4d80'], '#4b5568', '#2b3550')
    rr(c, 0, GY + 30, W, 60, 0, P('#566178'))
    # upper cabinets + counter
    for q in range(2): rr(c, 690 + q * 200, 700, 186, 170, 8, P('#2b3a66')); rr(c, 700 + q * 200, 710, 166, 150, 6, P('#34457a')); rr(c, 770 + q * 200, 840, 30, 8, 4, P('#c9d2da'))
    rr(c, 676, 1010, 420, 22, 6, P('#e8eef6')); rr(c, 690, 1032, 400, GY - 1032 - 16, 0, P('#2b3a66'))
    for q in range(2): rr(c, 704 + q * 196, 1052, 180, 112, 6, P('#34457a')); rr(c, 774 + q * 196, 1064, 40, 8, 4, P('#c9d2da'))
    x, w, h = 250, 390, 520
    R = fridge(c, x, w, h, '#c9d2da', '#8a9bab', inner=('#ffffff', '#e6f0f7'), dw=130, glow=150)
    ys = shelves(c, R, 3); ix, iy, iw, ih = R
    foods = [('#f08c2e', '#2fa35b'), ('#f5d03d', '#d13a52'), ('#c9935f', '#7fc77a'), ('#f6e3c8', '#2f8f4f'), ('#e5484d', '#f5c84a')]
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI']; pw = (iw - 30) / 2 - 6
    for i in range(4): prep(c, ix + 14 + (i % 2) * (pw + 14), ys[i // 2], days[i], foods[i], pw, 62)
    prep(c, ix + 14, ys[2], days[4], foods[4], pw, 62)
    for j, col in enumerate(('#7fc77a', '#f08c2e', '#d13a52')): bottle(c, ix + 28 + pw + j * 44, ys[2], 98, col, w=36, cap='#ffffff')
    for j, col in enumerate(('#7fc77a', '#f5d03d', '#e5484d', '#8a5ad6')): jar(c, ix + 14 + j * 80, ys[3], col, 66, 64, lid='#ffffff')
    bins = door_bins(c, x, w, h, 3, dw=130)
    for i, (bx, by, bw) in enumerate(bins):
        for j in range(2): bottle(c, bx + 2 + j * 40, by, 88, ('#dff1f4', '#7fc77a', '#f08c2e')[i], w=34, cap='#17b3a3')
    bin_front(c, bins, '#d6e4ee')
    doctor(c, 850, GY + 56, .7, 'consultant', 1.4, la=8, ra=-10, mood='happy')
    say(c, '“Monday to Friday. Handled.”')
    finish(c, 3, '4. Consultant', 'Labeled meal prep.', 'Swipe: one more')


def s5(c):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, GY, ['#3a1f5c', '#6b2f6f']))
    # marble floor, gold skirting, pendant lamps
    c.drawRect(skia.Rect.MakeXYWH(0, GY, W, H - GY), P('#efe9e2'))
    for i in range(10): c.drawLine(i * 150 - 100, GY, i * 150 - 220, H, P('#d9cfc3', stroke=3))
    for i in range(5): c.drawLine(0, GY + 60 + i * 150, W, GY + 60 + i * 150, P('#d9cfc3', stroke=3))
    c.drawRect(skia.Rect.MakeXYWH(0, GY - 16, W, 18), P(GOLD))
    # arched window with garden view
    arch = skia.Path(); arch.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(760, 690, 280, 330), 140, 140)); arch.addRect(skia.Rect.MakeXYWH(760, 840, 280, 180))
    c.save(); c.clipPath(arch, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(760, 690, 280, 330), grad(0, 690, 0, 1020, ['#272b73', '#f2707a', '#ffc37d'])); c.drawCircle(900, 950, 56, P('#fff0c4')); c.drawRect(skia.Rect.MakeXYWH(760, 980, 280, 40), P('#1c7a50'))
    c.restore(); c.drawPath(arch, P(GOLD, stroke=10))
    rr(c, 730, 1040, 360, 22, 6, P('#ffffff')); rr(c, 744, 1062, 340, GY - 1062 - 16, 0, P('#4a2340'))
    x, w, h, dw = 190, 430, 540, 130
    R = fridge(c, x, w, h, '#2b2f3a', GOLD, inner=('#ffffff', '#f3ead8'), doors='lr', dw=dw, glow=200)
    ys = shelves(c, R, 3, '#e7d6a8'); ix, iy, iw, ih = R
    cake(c, ix + 14, ys[0], 136); cloche(c, ix + 164, ys[0], 124); fruit_bowl(c, ix + 290 - 16, ys[0], 110)
    cheese(c, ix + 16, ys[1], 92)
    for j, col in enumerate(('#f6c9d6', '#f08c2e', '#7fc77a', '#f5d03d')): jar(c, ix + 124 + j * 66, ys[1], col, 54, 76, lid=GOLD)
    for j, col in enumerate(('#f08c2e', '#d13a52', '#7fc77a', '#f5d03d', '#8a5ad6', '#f08c2e')): bottle(c, ix + 14 + j * 62, ys[2], 108, col, w=46, cap=GOLD)
    lettuce(c, ix + 50, ys[3], 40); broccoli(c, ix + 128, ys[3], .8); tomato(c, ix + 190, ys[3], 22); tomato(c, ix + 236, ys[3], 22, '#f5d03d'); carrots(c, ix + 252, ys[3], 2)
    for side in 'lr':
        bins = door_bins(c, x, w, h, 3, side, dw)
        for i, (bx, by, bw) in enumerate(bins):
            for j in range(2): bottle(c, bx + 2 + j * 42, by, 90, ('#f5d03d', '#f6c9d6', '#7fc77a')[(i + (side == 'r')) % 3], w=36, cap=GOLD)
        bin_front(c, bins, '#f1e3bd')
    # chef's menu card on the wall above the left door
    c.save(); c.rotate(-4, 170, 584)
    rr(c, 44, 542, 262, 92, 10, P('#000000', 80, blur=10)); rr(c, 44, 536, 262, 92, 10, P('#fffaf0')); rr(c, 44, 536, 262, 92, 10, P(GOLD, stroke=4))
    chef_hat(c, 92, 592, .9, '#dfe7ee')
    text(c, 'CHEF’S MENU', 134, 578, 23, INK, 900); text(c, 'Restocked daily', 134, 608, 20, '#7a5a10', 800)
    c.restore()
    for sx, sy, r in ((150, 720, 24), (640, 760, 20), (700, 1120, 18)): sparkle(c, sx, sy, r, 255, '#fff6d8')
    doctor(c, 880, GY + 56, .7, 'director', 2.6, la=8, ra=-10, mood='happy')
    say(c, '“I can’t name half of this.”', tail=(870, 700), size=40, x=350)
    title2(c, '5. ED Director', 'Stocked by a private chef.', 356, shadow=.5)
    hud(c, 4, BANK[4], 5); brand_bar(c)
    pill(c, 330, 1554, 'Same doctor. Better fridge.', '#ffffff', INK, 34); swipe(c, 700, 1516)


def slides():
    return [s1, s2, s3, s4, s5, lambda c: cta2('Start with a ketchup packet.', 'Climb to ED Director.')(c, 2.8)]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
