"""Broke to Rich photo set 20 — "What's in Dr John Smith's bag? Every rank." A top-down flat-lay per rank: the bag and what
he carries, laid out neatly with taped-on labels, upgrading every promotion. Intern: worn backpack, bus pass, instant
noodles, a borrowed pen, 2 coins. Resident: gym duffel, pager, energy drink, granola bar, spare scrubs. Registrar:
messenger bag, surgical cap, a real lunch box, the key to an old car. Consultant: leather satchel, a good stethoscope,
fountain pen, dinner reservation. ED Director: designer briefcase, supercar key fob, gold watch, mansion keys, sunglasses.
Then the Play free card. No real brands. Bank amounts after the $2,000 start and every prop are illustrative.
Usage: python3 b2r_20_bag_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
from fullgame_02 import OUT, BANK

TOPH = 490            # navy header (brand pill + headline); the flat-lay surface starts here
BAG = (252, 890)      # centre of the bag column
CELLS = [(596, 814), (836, 814), (596, 1066), (836, 1066)]   # 2 x 2 item grid, right of the bag
PAPER = '#f6efdc'


def _poly(pts, close=True):
    p = skia.Path()
    for i, (x, y) in enumerate(pts): (p.lineTo if i else p.moveTo)(x, y)
    if close: p.close()
    return p


def put(c, fn, x, y, rot=0.0, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); fn(c); c.restore()


def sh(c, x, y, w, h, r, a=90):
    """Soft drop shadow for something lying flat."""
    rr(c, x + 6, y + 12, w, h, r, P('#000000', a, blur=14))


def hand(c, s, x, y, size, col=INK, align='c', wt=700):
    """Slanted label lettering (the kit font, skewed) for the hand-written notes."""
    f = font(size, wt); f.setSkewX(-.2); w = f.measureText(s)
    c.drawString(s, x - (w / 2 if align == 'c' else 0), y, f, P(col)); return w


def tape(c, x, y, label, rot=-3.0, size=30, col=PAPER):
    """A torn strip of masking tape with a hand-lettered label, centred on (x, y)."""
    f = font(size, 700); f.setSkewX(-.2); w = f.measureText(label) + 44; h = size + 22
    c.save(); c.translate(x, y); c.rotate(rot)
    rr(c, -w / 2 + 3, -h / 2 + 6, w, h, 3, P('#000000', 70, blur=8))
    p = _poly([(-w / 2, -h / 2), (w / 2 - 4, -h / 2), (w / 2, -h / 6), (w / 2 - 5, h / 6), (w / 2, h / 2), (-w / 2 + 4, h / 2), (-w / 2, h / 6), (-w / 2 + 5, -h / 6)])
    c.drawPath(p, P(col)); c.drawLine(-w / 2 + 10, h / 2 - 7, w / 2 - 10, h / 2 - 7, P('#000000', 14, stroke=3))
    hand(c, label, 0, size * .36, size)
    c.restore()


def badge(c, cx, cy, r, outfit, mood, ring):
    """Small Dr John Smith in the matching outfit, in a round frame."""
    c.drawCircle(cx + 4, cy + 10, r + 8, P('#000000', 90, blur=14))
    clip = skia.Path(); clip.addCircle(cx, cy, r); c.save(); c.clipPath(clip, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), grad(0, cy - r, 0, cy + r, ['#dff1f4', '#b9dfe6']))
    s = r / 150; doctor(c, cx, cy + 530 * s, s, outfit, 0.5, la=10, ra=-10, mood=mood); c.restore()
    c.drawCircle(cx, cy, r, P(ring, stroke=10))


def nametag(c, x, y, rank, rot=-5.0):
    """Luggage tag: whose bag this is."""
    c.save(); c.translate(x, y); c.rotate(rot)
    p = _poly([(-128, -48), (96, -48), (128, 0), (96, 48), (-128, 48)])
    c.save(); c.translate(5, 9); c.drawPath(p, P('#000000', 80, blur=10)); c.restore()
    c.drawPath(p, P(PAPER)); c.drawCircle(98, 0, 10, P('#000000', 70)); c.drawCircle(98, 0, 14, P('#b9a77a', stroke=4))
    text(c, 'THIS BAG BELONGS TO', -112, -18, 15, '#8a7a55', 900); hand(c, 'Dr John Smith', -112, 12, 27, INK, 'l', 800)
    text(c, rank.upper(), -112, 36, 16, TEAL_D, 900)
    c.restore()


# ---------------------------------------------------------------- surfaces
def surface(c, kind):
    r = skia.Rect.MakeLTRB(0, TOPH, W, H)
    if kind == 'floor':      # scuffed floorboards
        c.drawRect(r, P('#4a3b30'))
        for i in range(8):
            y = TOPH + i * 190; c.drawRect(skia.Rect.MakeXYWH(0, y, W, 186), P('#54443a' if i % 2 else '#4e3f35')); c.drawLine(0, y, W, y, P('#2f251e', stroke=5, cap=False))
            for j, xx in enumerate(((i * 331) % 700 + 120, (i * 517) % 600 + 420)):
                c.drawLine(xx, y, xx, y + 186, P('#2f251e', stroke=4, cap=False)) if j == i % 2 else c.drawLine(xx, y + 60, xx + 150, y + 66, P('#3d3028', stroke=4))
        for sx, sy, sw in ((520, 610, 150), (80, 1230, 120), (700, 1640, 200)): c.drawOval(skia.Rect.MakeXYWH(sx, sy, sw, sw * .4), P('#000000', 40, blur=16))
    elif kind == 'lino':     # locker-room floor tiles
        c.drawRect(r, P('#c3d9dd'))
        for i in range(8):
            for j in range(6):
                if (i + j) % 2: c.drawRect(skia.Rect.MakeXYWH(j * 180, TOPH + i * 180, 180, 180), P('#b5ced3'))
        for i in range(9): c.drawLine(0, TOPH + i * 180, W, TOPH + i * 180, P('#a5bfc5', stroke=3, cap=False))
        for j in range(7): c.drawLine(j * 180, TOPH, j * 180, H, P('#a5bfc5', stroke=3, cap=False))
    elif kind == 'desk':     # light wooden desk
        c.drawRect(r, grad(0, TOPH, W, H, ['#e0bd90', '#d2a876']))
        for i in range(16):
            y = TOPH + 30 + i * 92; g = skia.Path(); g.moveTo(-20, y); g.cubicTo(300, y + 26 - (i % 3) * 22, 700, y - 24 + (i % 4) * 14, W + 20, y + 8); c.drawPath(g, P('#c49a68', 150, stroke=4))
        c.drawOval(skia.Rect.MakeXYWH(700, 1560, 160, 60), P('#b98a58', 140, stroke=6))
    elif kind == 'walnut':   # dark desk with a leather pad
        c.drawRect(r, grad(0, TOPH, W, H, ['#4f3222', '#3c2518']))
        for i in range(16):
            y = TOPH + 20 + i * 92; g = skia.Path(); g.moveTo(-20, y); g.cubicTo(300, y + 22 - (i % 3) * 20, 700, y - 20 + (i % 4) * 12, W + 20, y + 6); c.drawPath(g, P('#2e1b11', 150, stroke=4))
        rr(c, 26, 520, 1028, 724, 26, P('#000000', 80, blur=18)); rr(c, 22, 512, 1036, 724, 26, P('#1f4a43')); rr(c, 38, 528, 1004, 692, 16, P('#2a5f56', stroke=3))
    else:                    # marble with gold veins
        c.drawRect(r, grad(0, TOPH, W, H, ['#f5f2ec', '#e6e1d8']))
        for i, (x0, y0, x1, y1, col, wd) in enumerate(((-20, 620, 500, 1010, '#c9c4ba', 5), (300, 500, 1100, 900, '#d8d3c9', 7), (540, 1300, 1100, 1040, GOLD, 4), (-20, 1250, 600, 1700, GOLD, 4),
                                                       (700, 1500, 1100, 1800, '#c9c4ba', 6), (100, 500, 320, 760, GOLD, 3), (-20, 1560, 420, 1900, '#d8d3c9', 7))):
            v = skia.Path(); v.moveTo(x0, y0); v.cubicTo(lerp(x0, x1, .3), y0 + 90, lerp(x0, x1, .6), y1 - 130, x1, y1); c.drawPath(v, P(col, 170, stroke=wd))
            b = skia.Path(); b.moveTo(lerp(x0, x1, .45), lerp(y0, y1, .45)); b.lineTo(lerp(x0, x1, .6) + 60, lerp(y0, y1, .5) - 80); c.drawPath(b, P(col, 120, stroke=max(2, wd - 2)))
    sp = skia.Paint(AntiAlias=True); sp.setShader(skia.GradientShader.MakeLinear(points=[skia.Point(0, TOPH), skia.Point(0, TOPH + 50)], colors=[C('#000000', 90), C('#000000', 0)]))
    c.drawRect(skia.Rect.MakeXYWH(0, TOPH, W, 50), sp)


def header(c):
    c.drawRect(skia.Rect.MakeWH(W, TOPH), grad(0, 0, W, TOPH, ['#0b1624', '#0e3a48']))
    c.drawCircle(540, 260, 380, P(TEAL, 30, blur=110))
    c.drawRect(skia.Rect.MakeXYWH(0, TOPH - 8, W, 8), P(GOLD))


# ---------------------------------------------------------------- the five bags (drawn around 0, 0)
def backpack(c):
    sh(c, -170, -250, 340, 520, 90, 120)
    for sx in (-1, 1):  # shoulder straps peeking out
        st = skia.Path(); st.moveTo(sx * 120, -150); st.quadTo(sx * 230, 40, sx * 130, 250); c.drawPath(st, P('#3f4633', stroke=40))
    rr(c, -170, -250, 340, 520, 100, P('#6f7a5a')); rr(c, -170, -250, 340, 520, 100, P('#596347', stroke=6))
    c.drawArc(skia.Rect.MakeXYWH(-50, -306, 100, 110), 180, 180, False, P('#3f4633', stroke=22))        # grab handle
    z = skia.Path(); z.moveTo(-140, -90); z.quadTo(0, -250, 140, -90); c.drawPath(z, P('#3f4633', stroke=10))   # main zipper
    for i in range(11):
        k = i / 10; x = lerp(-140, 140, k); y = -90 - 80 * (1 - (2 * k - 1) ** 2); c.drawLine(x, y - 7, x, y + 7, P('#c9d2da', stroke=3))
    rr(c, 118, -100, 18, 46, 6, P('#c9d2da'))
    rr(c, -124, 0, 248, 220, 46, P('#606b4d')); rr(c, -124, 0, 248, 220, 46, P('#4e5840', stroke=5))        # front pocket
    c.drawLine(-100, 44, 100, 44, P('#3f4633', stroke=8)); rr(c, 60, 34, 40, 18, 6, P('#c9d2da'))
    # worn: a sewn-on patch, a taped rip, a stain
    c.save(); c.rotate(-8, -40, 130); rr(c, -92, 86, 104, 88, 8, P('#b9844c'))
    for i in range(6): c.drawLine(-86 + i * 18, 92, -80 + i * 18, 92, P('#f1e3c6', stroke=4)); c.drawLine(-86 + i * 18, 168, -80 + i * 18, 168, P('#f1e3c6', stroke=4))
    for i in range(4): c.drawLine(-86, 100 + i * 20, -86, 106 + i * 20, P('#f1e3c6', stroke=4)); c.drawLine(6, 100 + i * 20, 6, 106 + i * 20, P('#f1e3c6', stroke=4))
    c.restore()
    c.save(); c.rotate(24, 70, -170); rr(c, 20, -186, 120, 34, 4, P('#aeb6bd')); c.drawLine(30, -176, 130, -176, P('#ffffff', 70, stroke=3)); c.restore()
    rip = _poly([(-120, -150), (-96, -132), (-104, -108), (-78, -92)], False); c.drawPath(rip, P('#2c3224', stroke=6))
    for i, (x, y) in enumerate(((-112, -140), (-100, -120), (-92, -100))): c.drawLine(x - 12, y + 8, x + 12, y - 8, P('#f1e3c6', stroke=3))
    c.drawOval(skia.Rect.MakeXYWH(30, 130, 80, 56), P('#000000', 36, blur=6))
    rr(c, -40, 228, 80, 22, 8, P('#3f4633'))


def duffel(c):
    sh(c, -150, -260, 300, 520, 80, 110)
    rr(c, -150, -260, 300, 520, 80, P('#17a394')); rr(c, -150, -260, 300, 520, 80, P('#0f766e', stroke=6))
    for y0 in (-260, 170): rr(c, -150, y0, 300, 90, 60, P('#128778'))
    c.drawRect(skia.Rect.MakeXYWH(-150, -206, 300, 36), P('#17a394')); c.drawRect(skia.Rect.MakeXYWH(-150, 170, 300, 36), P('#17a394'))
    c.drawLine(-150, -172, 150, -172, P('#0f766e', stroke=5, cap=False)); c.drawLine(-150, 172, 150, 172, P('#0f766e', stroke=5, cap=False))
    c.drawLine(0, -160, 0, 160, P('#0b5a54', stroke=10));
    for i in range(14): c.drawLine(-8, -150 + i * 23, 8, -150 + i * 23, P('#c9d2da', stroke=3))
    rr(c, -10, 120, 20, 46, 6, P('#c9d2da'))
    for sx in (-1, 1):  # carry straps
        rr(c, sx * 86 - 17, -170, 34, 340, 8, P('#12263f'))
        hd = skia.Path(); hd.moveTo(sx * 86, -90); hd.quadTo(sx * 190, 0, sx * 86, 90); c.drawPath(hd, P('#12263f', stroke=24))
        for yy in (-150, 150): rr(c, sx * 86 - 22, yy - 14, 44, 28, 5, P('#0b1a2c')); c.drawLine(sx * 86 - 12, yy, sx * 86 + 12, yy, P('#c9d2da', stroke=3))
    rr(c, -62, 196, 124, 44, 8, P('#ffffff')); text(c, 'RESIDENT', 0, 226, 20, TEAL_D, 900, 'c')
    c.drawOval(skia.Rect.MakeXYWH(-50, -246, 100, 36), P('#0f766e'))


def messenger(c):
    st = skia.Path(); st.moveTo(-150, -150); st.cubicTo(-260, -330, 240, -350, 160, -150); c.drawPath(st, P('#000000', 70, stroke=34, blur=8)); c.drawPath(st, P('#2b3b4d', stroke=30))
    rr(c, -40, -322, 90, 34, 8, P('#c9d2da')); rr(c, -28, -314, 66, 18, 4, P('#2b3b4d'))
    sh(c, -190, -190, 380, 430, 40, 110)
    rr(c, -190, -190, 380, 430, 44, P('#4c627a')); rr(c, -190, -190, 380, 430, 44, P('#3a4d61', stroke=6))
    rr(c, -150, 130, 300, 90, 20, P('#43576d')); c.drawLine(-150, 150, 150, 150, P('#3a4d61', stroke=5))
    flap = skia.Path(); flap.moveTo(-190, -150); flap.lineTo(190, -150); flap.lineTo(190, 60); flap.quadTo(190, 110, 140, 110); flap.lineTo(-140, 110); flap.quadTo(-190, 110, -190, 60); flap.close()
    c.save(); c.translate(0, 8); c.drawPath(flap, P('#000000', 70, blur=10)); c.restore()
    rr(c, -190, -190, 380, 90, 44, P('#5d7690')); c.drawPath(flap, P('#5d7690')); c.drawPath(flap, P('#3a4d61', stroke=5))
    for i in range(18): c.drawLine(-170 + i * 20, 92, -160 + i * 20, 92, P('#c9d6e4', 190, stroke=3))
    for sx in (-110, 110):  # buckle straps
        rr(c, sx - 20, -60, 40, 220, 8, P('#2b3b4d')); rr(c, sx - 28, 70, 56, 46, 8, P('#c9d2da')); rr(c, sx - 16, 80, 32, 26, 4, P('#2b3b4d'))
    rr(c, -52, -110, 104, 60, 8, P('#e9eef2')); text(c, 'ON CALL', 0, -74, 19, '#3a4d61', 900, 'c'); c.drawLine(-40, -62, 40, -62, P('#9fb2c2', stroke=3))


def satchel(c):
    c.drawArc(skia.Rect.MakeXYWH(-80, -290, 160, 150), 180, 180, False, P('#000000', 70, stroke=30, blur=8))
    c.drawArc(skia.Rect.MakeXYWH(-80, -290, 160, 150), 180, 180, False, P('#5e3317', stroke=26))
    for sx in (-80, 80): rr(c, sx - 20, -222, 40, 30, 6, P(GOLD))
    sh(c, -196, -200, 392, 430, 36, 130)
    rr(c, -196, -200, 392, 430, 40, P('#8a4f2a')); rr(c, -196, -200, 392, 430, 40, P('#5e3317', stroke=6))
    rr(c, -150, 110, 300, 100, 18, P('#7c4625'))
    flap = skia.Path(); flap.moveTo(-196, -170); flap.lineTo(196, -170); flap.lineTo(196, 20); flap.quadTo(120, 150, 0, 150); flap.quadTo(-120, 150, -196, 20); flap.close()
    c.save(); c.translate(0, 10); c.drawPath(flap, P('#000000', 80, blur=12)); c.restore()
    rr(c, -196, -200, 392, 90, 40, P('#a4622f')); c.drawPath(flap, grad(0, -200, 0, 150, ['#a8662f', '#93552a'])); c.drawPath(flap, P('#5e3317', stroke=5))
    stitch = skia.Path(); stitch.moveTo(-176, -150); stitch.lineTo(-176, 14); stitch.quadTo(-108, 130, 0, 130); stitch.quadTo(108, 130, 176, 14); stitch.lineTo(176, -150)
    sp = P('#f1d9a8', stroke=4); sp.setPathEffect(skia.DashPathEffect.Make([12, 10], 0)); c.drawPath(stitch, sp)
    for sx in (-100, 100):  # brass buckles
        rr(c, sx - 22, -40, 44, 190, 8, P('#6f3d1d')); rr(c, sx - 32, 96, 64, 54, 8, P(GOLD)); rr(c, sx - 18, 108, 36, 30, 4, P('#6f3d1d')); c.drawLine(sx, 108, sx, 138, P('#ffd774', stroke=5))
    c.drawLine(-120, -120, 60, -120, P('#ffffff', 40, stroke=10))
    rr(c, -36, -90, 72, 44, 6, P(GOLD)); text(c, 'J.S.', 0, -59, 24, '#5e3317', 900, 'c')


def briefcase(c):
    c.drawArc(skia.Rect.MakeXYWH(-90, -254, 180, 150), 180, 180, False, P('#000000', 70, stroke=30, blur=8))
    c.drawArc(skia.Rect.MakeXYWH(-90, -254, 180, 150), 180, 180, False, P('#1c2530', stroke=28))
    for sx in (-90, 90): rr(c, sx - 22, -196, 44, 34, 6, P(GOLD))
    sh(c, -200, -170, 400, 360, 26, 110)
    rr(c, -200, -170, 400, 360, 28, grad(0, -170, 0, 190, ['#2d3947', '#161d26'])); rr(c, -200, -170, 400, 360, 28, P(GOLD, stroke=7))
    c.drawLine(-200, -40, 200, -40, P(GOLD, stroke=5, cap=False))
    for i in range(7):          # quilted leather
        c.drawLine(-190 + i * 64, -30, -190 + i * 64 + 210, 180, P('#ffffff', 16, stroke=3)); c.drawLine(190 - i * 64, -30, 190 - i * 64 - 210, 180, P('#ffffff', 16, stroke=3))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(-200, -170, 400, 360))
    for sx, sy in ((-200, -170), (200, -170), (-200, 190), (200, 190)): c.drawCircle(sx, sy, 52, P(GOLD)); c.drawCircle(sx, sy, 34, P('#ffd774'))
    c.restore()
    for sx in (-110, 110):      # combination locks
        rr(c, sx - 40, -66, 80, 52, 8, P(GOLD)); rr(c, sx - 30, -56, 60, 32, 4, P('#fff4cf'))
        for j in range(3): text(c, '0', sx - 20 + j * 20, -32, 22, INK, 900, 'c')
    rr(c, -50, -150, 100, 70, 10, P(GOLD)); rr(c, -42, -142, 84, 54, 6, P('#1c2530')); text(c, 'JS', 0, -100, 40, GOLD, 900, 'c')
    sparkle(c, 150, -120, 30, 255, '#fff6d8'); sparkle(c, -160, 150, 20, 255, '#fff6d8')


# ---------------------------------------------------------------- the things inside (drawn around 0, 0)
def bus_pass(c):
    sh(c, -100, -64, 200, 128, 14)
    rr(c, -100, -64, 200, 128, 14, P('#ffffff')); c.save(); c.clipRect(skia.Rect.MakeXYWH(-100, -64, 200, 44)); rr(c, -100, -64, 200, 128, 14, P('#2f6fd6')); c.restore()
    text(c, 'BUS PASS', -86, -32, 26, '#ffffff', 900)
    rr(c, -84, -4, 70, 44, 10, P('#2f6fd6')); rr(c, -76, 2, 54, 18, 4, P('#ffffff')); c.drawCircle(-70, 42, 8, P(INK)); c.drawCircle(-28, 42, 8, P(INK))
    text(c, 'MONTHLY', -6, 12, 19, INK, 900); text(c, 'All zones', -6, 38, 18, '#5b7083', 700)
    c.drawLine(64, -50, 86, -50, P('#ffffff', 150, stroke=4)); c.drawCircle(84, 48, 6, P('#d5dde5'))
    for i in range(3): c.drawLine(-96 + i * 6, 58 - i * 2, -80 + i * 6, 62 - i * 2, P('#c9b98f', stroke=3))   # frayed corner


def noodles(c):
    c.drawCircle(6, 12, 92, P('#000000', 90, blur=14))
    c.drawCircle(0, 0, 90, P('#f4f1ea')); c.drawCircle(0, 0, 90, P('#d64545', stroke=14)); c.drawCircle(0, 0, 70, P('#fff8ea')); c.drawCircle(0, 0, 70, P('#e3ded3', stroke=3))
    text(c, 'INSTANT', 0, -10, 24, '#d64545', 900, 'c'); text(c, 'NOODLES', 0, 20, 26, '#d64545', 900, 'c')
    for i in range(3):
        s = skia.Path(); s.moveTo(-34 + i * 26, 42); s.quadTo(-24 + i * 26, 34, -34 + i * 26 + 20, 42); c.drawPath(s, P('#f5b83d', stroke=5))
    tab = _poly([(60, -66), (96, -96), (110, -72), (78, -48)]); c.drawPath(tab, P('#c9d2da')); c.drawLine(64, -62, 80, -50, P('#aab8c4', stroke=3))


def pen_cheap(c):
    c.save(); c.rotate(-38)
    rr(c, -104, -4, 220, 24, 10, P('#000000', 80, blur=8))
    rr(c, -110, -12, 170, 24, 8, P('#eaf3fb')); rr(c, -104, -5, 150, 10, 4, P('#2f6fd6', 200)); rr(c, 50, -14, 64, 28, 10, P('#2f6fd6'))
    c.drawPath(_poly([(-110, -10), (-136, 0), (-110, 10)]), P('#c9d2da')); c.drawCircle(-134, 0, 3, P(INK))
    rr(c, 40, -24, 70, 9, 4, P('#2f6fd6'))
    for i in range(3): c.drawLine(98 + i * 5, -14, 100 + i * 5, -6, P('#1d4f9f', stroke=3))   # chewed end
    c.restore()


def two_coins(c):
    for x, y, r, col, c2, v in ((-42, 10, 46, '#c9d2da', '#eef2f6', '25'), (40, -12, 38, '#d39b4a', '#f0c27e', '5')):
        c.drawCircle(x + 5, y + 9, r, P('#000000', 90, blur=8)); c.drawCircle(x, y, r, P(col)); c.drawCircle(x, y, r - 9, P(c2)); c.drawCircle(x, y, r - 9, P(col, stroke=3))
        text(c, v, x, y + r * .3, r * .8, '#5b6672', 900, 'c')


def pager(c):
    sh(c, -86, -60, 172, 120, 18)
    rr(c, -86, -60, 172, 120, 18, P('#12263f')); rr(c, -72, -46, 144, 58, 8, P('#3ee08a')); text(c, 'PAGE x14', -62, -8, 26, '#0b3a22', 900)
    for i in range(3): rr(c, -66 + i * 48, 24, 36, 22, 8, P('#33475b'))
    c.drawCircle(70, 36, 8, P('#e5484d')); rr(c, -100, -30, 16, 60, 6, P('#33475b'))


def energy_can(c):
    c.save(); c.rotate(12)
    rr(c, -40, -96, 92, 200, 20, P('#000000', 90, blur=12))
    rr(c, -46, -104, 92, 208, 22, grad(-46, 0, 46, 0, ['#1c2530', '#3a4756', '#1c2530'])); rr(c, -46, -104, 92, 22, 10, P('#c9d2da')); rr(c, -46, 82, 92, 22, 10, P('#c9d2da'))
    c.drawPath(_poly([(8, -62), (-24, 6), (-2, 6), (-12, 60), (26, -14), (4, -14)]), P('#c6f135'))
    text(c, 'ENERGY', 0, 76, 17, '#c6f135', 900, 'c'); c.drawLine(-32, -70, -32, 60, P('#ffffff', 50, stroke=5))
    c.restore()


def granola(c):
    c.save(); c.rotate(-10)
    rr(c, -104, -34, 220, 84, 8, P('#000000', 80, blur=10))
    w = _poly([(-110, -40), (-98, -30), (-110, -20), (-98, -10), (-110, 0), (-98, 10), (-110, 20), (-98, 30), (-110, 40),
               (110, 40), (98, 30), (110, 20), (98, 10), (110, 0), (98, -10), (110, -20), (98, -30), (110, -40)])
    c.drawPath(w, P('#c98a3c')); rr(c, -80, -40, 160, 80, 0, P('#e8b25a')); rr(c, -66, -24, 132, 48, 10, P('#fff8ea'))
    text(c, 'OAT BAR', 0, 9, 26, '#8a5a1c', 900, 'c'); c.drawLine(-76, -32, 76, -32, P('#ffffff', 90, stroke=4))
    c.restore()


def scrubs(c):
    sh(c, -100, -84, 200, 168, 16)
    rr(c, -100, -84, 200, 168, 16, P('#17a394')); rr(c, -100, -84, 200, 168, 16, P('#0f766e', stroke=5))
    c.drawPath(_poly([(-38, -84), (0, -30), (38, -84)]), P('#0f766e')); c.drawPath(_poly([(-26, -84), (0, -48), (26, -84)]), P('#dff1f4'))
    c.drawLine(-100, 30, 100, 30, P('#0f766e', stroke=4)); c.drawLine(-100, 58, 100, 58, P('#0f766e', 140, stroke=3))
    rr(c, 30, -36, 50, 48, 6, P('#128778')); c.drawLine(-80, -50, -60, 10, P('#ffffff', 50, stroke=6))


def surgical_cap(c):
    c.drawOval(skia.Rect.MakeXYWH(-96, -62, 204, 150), P('#000000', 80, blur=12))
    for sx in (-1, 1):
        tie = skia.Path(); tie.moveTo(sx * 70, 50); tie.quadTo(sx * 130, 100, sx * 96, 124); c.drawPath(tie, P('#48aebb', stroke=12))
    cap = skia.Path(); cap.moveTo(-104, 54); cap.cubicTo(-110, -110, 110, -110, 104, 54); cap.close(); c.drawPath(cap, P('#5cc0cc'))
    c.save(); c.clipPath(cap, doAntiAlias=True)
    for i in range(5):
        for j in range(4):
            x, y = -84 + i * 42 + (j % 2) * 20, -56 + j * 30
            c.drawLine(x - 7, y, x + 7, y, P('#ffffff', 200, stroke=5)); c.drawLine(x, y - 7, x, y + 7, P('#ffffff', 200, stroke=5))
    c.restore()
    rr(c, -108, 40, 216, 28, 10, P('#48aebb'))


def car_key(c):
    c.save(); c.rotate(-24)
    c.drawCircle(-96, 0, 34, P('#8ea2b1', stroke=7))                                   # ring
    rr(c, -150, -84, 76, 46, 8, P('#000000', 70, blur=6)); rr(c, -154, -90, 76, 46, 8, P('#f5b83d')); text(c, 'OLD CAR', -116, -61, 15, INK, 900, 'c')
    rr(c, -64, -30, 92, 74, 16, P('#000000', 80, blur=8)); rr(c, -70, -38, 92, 76, 18, P('#2a3440')); c.drawCircle(-46, 0, 10, P('#8ea2b1'))
    c.drawLine(-20, -18, 8, -18, P('#465260', stroke=5)); c.drawLine(-20, 18, 8, 18, P('#465260', stroke=5))
    blade = _poly([(22, -11), (130, -11), (146, 0), (130, 11), (116, 11), (108, 20), (98, 11), (84, 11), (76, 22), (64, 11), (50, 11), (44, 18), (36, 11), (22, 11)])
    c.drawPath(blade, P('#b7c2cc')); c.drawLine(30, -3, 126, -3, P('#8ea2b1', stroke=3))
    for x, y in ((60, -6), (96, 4)): c.drawCircle(x, y, 4, P('#a0623a'))               # rust spots
    c.restore()


def lunch_box(c):
    sh(c, -190, -100, 380, 200, 24)
    rr(c, -190, -100, 380, 200, 26, P('#2f8f9d')); rr(c, -176, -86, 352, 172, 16, P('#e9fbf9'))
    c.drawLine(40, -86, 40, 86, P('#2f8f9d', stroke=8, cap=False)); c.drawLine(40, 0, 176, 0, P('#2f8f9d', stroke=8, cap=False))
    for dx in (0, 16):  # sandwich halves
        tri = _poly([(-160 + dx * 5, 64), (-160 + dx * 5, -66), (-70 + dx * 5, 64)]); c.drawPath(tri, P('#f1d9a8')); c.drawPath(tri, P('#c98a3c', stroke=6))
        c.drawLine(-150 + dx * 5, 40, -96 + dx * 5, 52, P('#2e9f6b', stroke=6)); c.drawLine(-150 + dx * 5, 22, -108 + dx * 5, 38, P('#e5484d', stroke=6))
    c.drawCircle(108, -44, 34, P('#e5484d')); c.drawCircle(96, -54, 10, P('#ffffff', 90)); c.drawLine(108, -76, 114, -90, P('#5a3a22', stroke=5)); c.drawOval(skia.Rect.MakeXYWH(114, -92, 22, 12), P('#2e9f6b'))
    for i in range(5): rr(c, 60 + i * 22, 18, 14, 58, 6, P('#f08a3c' if i % 2 == 0 else '#2e9f6b'))
    rr(c, -196, -24, 14, 48, 6, P('#277c89')); rr(c, 182, -24, 14, 48, 6, P('#277c89'))


def stethoscope(c):
    def shape(p1, p2):
        tube = skia.Path(); tube.moveTo(-70, -84); tube.cubicTo(-90, 40, 60, 60, 20, -10); tube.cubicTo(-10, -60, 130, -90, 150, 20)
        c.drawPath(tube, p1)
        for sx in (-1, 1):
            ear = skia.Path(); ear.moveTo(-70, -84); ear.quadTo(-70 + sx * 20, -130, -70 + sx * 62, -150); c.drawPath(ear, p2)
    c.save(); c.translate(6, 12); shape(P('#000000', 80, stroke=16, blur=8), P('#000000', 80, stroke=10, blur=8)); c.drawCircle(150, 40, 44, P('#000000', 80, blur=8)); c.restore()
    shape(P('#1f2f3f', stroke=14), P('#c9d2da', stroke=9))
    for sx in (-1, 1): c.drawCircle(-70 + sx * 66, -152, 11, P('#12263f'))
    c.drawCircle(-70, -84, 12, P('#c9d2da'))
    c.drawCircle(150, 40, 44, P(GOLD)); c.drawCircle(150, 40, 34, P('#e9eef2')); c.drawCircle(150, 40, 20, P('#c9d2da')); c.drawCircle(150, 40, 34, P('#ffd774', stroke=4))
    sparkle(c, 178, 8, 20, 255, '#ffffff')


def fountain_pen(c):
    c.save(); c.rotate(-32)
    rr(c, -110, -6, 240, 30, 12, P('#000000', 90, blur=8))
    rr(c, -96, -16, 150, 32, 12, P('#16202b')); rr(c, -96, -16, 20, 32, 8, P(GOLD)); rr(c, 30, -17, 14, 34, 4, P(GOLD)); rr(c, -40, -17, 8, 34, 3, P(GOLD))
    c.drawPath(_poly([(54, -13), (96, -9), (138, 0), (96, 9), (54, 13)]), P(GOLD)); c.drawLine(84, 0, 132, 0, P('#8a6a14', stroke=3)); c.drawCircle(82, 0, 4, P('#8a6a14'))
    c.drawLine(-80, -8, 20, -8, P('#ffffff', 60, stroke=4))
    c.restore()
    c.save(); c.rotate(-20); c.translate(-10, 86)   # the cap, beside it
    rr(c, -52, -12, 110, 30, 12, P('#000000', 80, blur=8)); rr(c, -56, -17, 110, 34, 14, P('#16202b')); rr(c, -56, -17, 14, 34, 6, P(GOLD)); rr(c, -34, -26, 76, 9, 4, P(GOLD)); c.restore()


def reservation(c):
    sh(c, -106, -76, 212, 152, 10)
    rr(c, -106, -76, 212, 152, 10, P('#fbf7ee')); rr(c, -96, -66, 192, 132, 6, P(GOLD, stroke=3))
    text(c, 'RESERVED', 0, -30, 28, '#8a6a14', 900, 'c'); c.drawLine(-60, -16, 60, -16, P(GOLD, stroke=3))
    hand(c, 'Dr J. Smith', 0, 14, 26, INK, 'c', 800); text(c, 'Table for two', 0, 40, 18, '#5b7083', 700, 'c'); text(c, '8:00 PM', 0, 60, 18, '#5b7083', 800, 'c')


def key_fob(c):
    c.drawCircle(0, -98, 34, P('#c9d2da', stroke=7))
    rr(c, -54, -70, 120, 190, 40, P('#000000', 90, blur=12))
    rr(c, -62, -80, 124, 196, 44, grad(-62, 0, 62, 0, ['#1c2530', '#3a4756', '#1c2530'])); rr(c, -62, -80, 124, 196, 44, P('#e5484d', stroke=6))
    sh_ = _poly([(0, -58), (26, -46), (22, -14), (0, 0), (-22, -14), (-26, -46)]); c.drawPath(sh_, P('#e9eef2')); c.drawPath(_poly([(0, -46), (-12, -22), (12, -22)]), P('#e5484d'))
    for i, yy in enumerate((26, 62, 96)):
        rr(c, -34, yy - 13, 68, 26, 10, P('#0f151c')); c.drawCircle(0, yy, 6, P(['#3ee08a', '#c9d2da', '#e5484d'][i]))
    sparkle(c, 50, -70, 22, 255, '#ffffff')


def gold_watch(c):
    for y0, y1 in ((-128, -52), (52, 128)):
        rr(c, -30, y0 + 8, 72, y1 - y0, 10, P('#000000', 70, blur=8)); rr(c, -34, y0, 68, y1 - y0, 10, P(GOLD))
        for i in range(4): c.drawLine(-34, y0 + 14 + i * 18, 34, y0 + 14 + i * 18, P('#b98416', stroke=3, cap=False))
        c.drawLine(-12, y0, -12, y1, P('#ffd774', stroke=3, cap=False)); c.drawLine(12, y0, 12, y1, P('#ffd774', stroke=3, cap=False))
    c.drawCircle(6, 10, 66, P('#000000', 90, blur=10)); rr(c, 60, -10, 16, 20, 5, P('#b98416'))
    c.drawCircle(0, 0, 66, P(GOLD)); c.drawCircle(0, 0, 54, P('#ffd774')); c.drawCircle(0, 0, 46, P('#fff8e0'))
    for i in range(12):
        a = i * math.pi / 6; c.drawLine(math.cos(a) * 36, math.sin(a) * 36, math.cos(a) * 42, math.sin(a) * 42, P('#8a6a14', stroke=4 if i % 3 == 0 else 2))
    c.drawLine(0, 0, -16, -20, P(INK, stroke=6)); c.drawLine(0, 0, 22, -24, P(INK, stroke=4)); c.drawCircle(0, 0, 5, P(INK))
    sparkle(c, 44, -48, 26, 255, '#ffffff')


def mansion_keys(c):
    c.drawCircle(0, -70, 36, P('#000000', 60, stroke=8, blur=5)); c.drawCircle(0, -74, 36, P(GOLD, stroke=8))
    for ang, ln in ((-28, 150), (4, 170), (34, 140)):
        c.save(); c.translate(0, -40); c.rotate(ang)
        c.drawCircle(4, 34, 22, P('#000000', 60, blur=6)); c.drawCircle(0, 28, 22, P(GOLD)); c.drawCircle(0, 28, 10, P('#fff4cf'))
        rr(c, -6, 46, 12, ln - 46, 4, P(GOLD)); rr(c, 4, ln - 34, 20, 10, 2, P(GOLD)); rr(c, 4, ln - 16, 14, 10, 2, P(GOLD)); c.drawLine(-2, 50, -2, ln - 6, P('#ffd774', stroke=3))
        c.restore()
    c.save(); c.translate(-62, -20); c.rotate(-20)   # little house charm
    c.drawPath(_poly([(-26, 0), (0, -26), (26, 0), (26, 34), (-26, 34)]), P('#fbf8f2')); c.drawPath(_poly([(-32, 2), (0, -30), (32, 2)], False), P('#34414f', stroke=6)); rr(c, -7, 12, 14, 22, 3, P('#34414f'))
    c.restore()


def sunglasses(c):
    for sx in (-1, 1):
        arm = skia.Path(); arm.moveTo(sx * 104, -20); arm.quadTo(sx * 112, -78, sx * 40, -70); c.drawPath(arm, P('#101418', stroke=9))
    for sx in (-104, 8):
        rr(c, sx + 5, -22, 96, 66, 24, P('#000000', 80, blur=8)); rr(c, sx, -30, 96, 66, 24, P('#101418')); rr(c, sx + 8, -22, 80, 50, 18, grad(sx, -30, sx + 96, 36, ['#2b3440', '#0b0e12']))
        c.drawLine(sx + 20, -12, sx + 46, -12, P('#ffffff', 110, stroke=5))
    c.drawLine(-12, -12, 12, -12, P('#101418', stroke=9)); rr(c, 84, -24, 14, 8, 3, P(GOLD)); rr(c, -98, -24, 14, 8, 3, P(GOLD))


# ---------------------------------------------------------------- slides
RANKS5 = [
    ('floor', backpack, 0, 1.0, 'worn backpack', 'tired', '#c9c2b6',
     [(bus_pass, -6, 'bus pass', 1.0), (noodles, 0, 'dinner', .84), (pen_cheap, 0, 'borrowed pen', .95), (two_coins, 0, '2 coins', 1.0)]),
    ('lino', duffel, 4, 1.0, 'gym duffel', 'ok', TEAL,
     [(pager, -5, 'pager', 1.0), (energy_can, 0, 'energy drink', .72), (granola, 0, 'granola bar', .9), (scrubs, 4, 'spare scrubs', .95)]),
    ('desk', messenger, -3, 1.0, 'messenger bag', 'happy', '#2f8f9d',
     [(surgical_cap, -6, 'surgical cap', .92), (car_key, 0, 'car key (old car)', .86), (lunch_box, -2, 'a real lunch box', .9)]),
    ('walnut', satchel, 3, 1.0, 'leather satchel', 'happy', '#ffffff',
     [(stethoscope, 0, 'the good stethoscope', 1.0), (fountain_pen, 0, 'fountain pen', .92), (reservation, 5, 'dinner at 8', .95)]),
    ('marble', briefcase, -2, .98, 'designer briefcase', 'happy', GOLD,
     [(key_fob, -8, 'supercar key', .8), (gold_watch, 6, 'gold watch', .78), (mansion_keys, 0, 'mansion keys', .9), (sunglasses, -4, 'sunglasses', .95)]),
]
SUBS = ['Worn backpack.', 'Gym duffel.', 'Messenger bag.', 'Leather satchel.', 'Designer briefcase.']
NOTES = ['1. Intern: worn backpack', 'Swipe: an actual car key', 'Swipe: it gets fancier', 'Swipe: one more bag', 'Same doctor. Better bag.']


def flatlay(c, i):
    kind, bag, rot, bs, baglabel, mood, ring, items = RANKS5[i]
    dark = kind in ('floor', 'walnut')
    surface(c, kind); header(c)
    put(c, bag, BAG[0], BAG[1] + (30 if i == 4 else 0), rot, bs)
    tape(c, BAG[0], 1204, baglabel, -3, 32)
    nametag(c, 596, 606, RANKS[i]); badge(c, 846, 606, 82, OUT[i], mood, ring)
    if len(items) == 4: spots = [(CELLS[k], 104) for k in range(4)]
    elif i == 2: spots = [(CELLS[0], 104), (CELLS[1], 104), ((716, 1048), 128)]
    else: spots = [((716, 836), 112), (CELLS[2], 104), (CELLS[3], 104)]
    for (fn, r, label, s), ((x, y), ly) in zip(items, spots):
        put(c, fn, x, y - 8, r, s); tape(c, x, y + ly, label, (-4, 3, 2, -3)[spots.index(((x, y), ly)) % 4], 28)
    hud(c, i, BANK[i], i + 1); brand_bar(c)
    pill(c, 330, 1554, NOTES[i], '#ffffff', INK, 34); swipe(c, 700, 1516)


def s1(c):
    flatlay(c, 0)
    title2(c, "What's in Dr John Smith's bag?", 'Every rank.', 352, size=96, sub_size=92, shadow=.4)


def rank_slide(i):
    def f(c):
        flatlay(c, i)
        title2(c, f'{i + 1}. {RANKS[i]}', SUBS[i], 356, shadow=.4)
    return f


def slides():
    return [s1] + [rank_slide(i) for i in range(1, 5)] + [lambda c: cta2('Start with a bus pass.', 'Climb to ED Director.')(c, 2.8)]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
