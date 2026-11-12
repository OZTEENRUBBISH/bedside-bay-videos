"""Shared drawing kit for Bedside Bay ads: brand bar, HUD, Dr John Smith, scenes."""
import math, skia

W, H = 1080, 1920
import os
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts') + '/'
_tf = {}
NAVY, TEAL, TEAL_D, INK, GOLD = '#0f2a43', '#17b3a3', '#0f766e', '#12263f', '#f5b83d'


def C(h, a=255):
    h = h.lstrip('#')
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(a))


def P(col, a=255, stroke=0, blur=0, cap=True):
    p = skia.Paint(AntiAlias=True, Color=C(col, a) if isinstance(col, str) else col)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        if cap:
            p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def grad(x0, y0, x1, y1, cols, a=255):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear(points=[skia.Point(x0, y0), skia.Point(x1, y1)],
                                               colors=[C(c, a) for c in cols]))
    return p


def rr(c, x, y, w, h, r, p):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), p)


def font(size, wt=800):
    if wt not in _tf:
        _tf[wt] = skia.Typeface.MakeFromFile(f'{FD}Figtree-{wt}.ttf')
    return skia.Font(_tf[wt], size)


def tw(s, size, wt=800):
    return font(size, wt).measureText(s)


def text(c, s, x, y, size, col='#ffffff', wt=800, align='l', a=255, shadow=0):
    f = font(size, wt); w = f.measureText(s)
    if align == 'c': x -= w / 2
    elif align == 'r': x -= w
    if shadow:
        c.drawString(s, x, y + 4, f, P('#000000', a * shadow, blur=10))
    c.drawString(s, x, y, f, P(col, a))
    return w


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def pop(x):
    x = clamp(x)
    return 1 + 2.70158 * (x - 1) ** 3 + 1.70158 * (x - 1) ** 2
def lerp(a, b, t): return a + (b - a) * t


def check(c, cx, cy, s, col='#ffffff', w=8):
    p = skia.Path(); p.moveTo(cx - s, cy); p.lineTo(cx - s * .3, cy + s * .7); p.lineTo(cx + s, cy - s * .7)
    c.drawPath(p, P(col, stroke=w))


def sparkle(c, x, y, r, a=255, col='#ffffff'):
    p = skia.Path()
    for i in range(8):
        ang = i * math.pi / 4; rad = r if i % 2 == 0 else r * .28
        px, py = x + math.cos(ang) * rad, y + math.sin(ang) * rad
        p.lineTo(px, py) if i else p.moveTo(px, py)
    p.close(); c.drawPath(p, P(col, a))


# ---------------------------------------------------------------- brand
def logo(c, x, y, s):
    """Bedside Bay icon: teal rounded square with a white pulse line."""
    p = grad(x, y, x + s, y + s, ['#1cb5a3', '#0e7f76'])
    rr(c, x, y, s, s, s * .26, p)
    pa = skia.Path(); m = y + s * .52
    pts = [(.2, 0), (.36, 0), (.44, -.2), (.54, .2), (.62, -.08), (.68, 0), (.8, 0)]
    for i, (px, py) in enumerate(pts):
        (pa.lineTo if i else pa.moveTo)(x + s * px, m + s * py)
    c.drawPath(pa, P('#ffffff', stroke=s * .075))


def brand_bar(c, y=128):
    """White pill with logo + wordmark, present on every frame."""
    w = 560; x = (W - w) / 2
    rr(c, x, y + 8, w, 124, 62, P('#000000', 60, blur=18))
    rr(c, x, y, w, 124, 62, P('#ffffff'))
    logo(c, x + 22, y + 20, 84)
    text(c, 'Bedside Bay', x + 126, y + 64, 50, INK, 800)
    text(c, 'Emergency medicine career', x + 127, y + 100, 26, '#5b7083', 600)


RANKS = ['Intern', 'Resident', 'Registrar', 'Consultant', 'ED Director']


def hud(c, rank_i, bank, prog, y=1262, a=255, bump=0.0):
    """Career card: name, rank, bank balance, five-step ladder. prog = 0..5 segments filled."""
    x, w, h = 60, 860, 226
    rr(c, x, y + 10, w, h, 44, P('#000000', 70 * a / 255, blur=22))
    rr(c, x, y, w, h, 44, P('#ffffff', a))
    text(c, 'DR JOHN SMITH', x + 40, y + 58, 26, '#5b7083', 800, a=a)
    text(c, RANKS[rank_i], x + 40, y + 122, 60, INK, 900, a=a)
    bs = 62 * (1 + .08 * bump)
    text(c, '$' + f'{int(bank):,}', x + w - 40, y + 122, bs, TEAL_D, 900, 'r', a=a)
    text(c, 'BANK', x + w - 40, y + 58, 26, '#5b7083', 800, 'r', a=a)
    sw = (w - 80 - 4 * 12) / 5
    for i in range(5):
        sx = x + 40 + i * (sw + 12)
        rr(c, sx, y + 160, sw, 16, 8, P('#dfe7ee', a))
        f = clamp(prog - i)
        if f > 0:
            rr(c, sx, y + 160, sw * f, 16, 8, P(GOLD if i == 4 else TEAL, a))
        text(c, RANKS[i], sx + sw / 2, y + 204, 20, INK if i == rank_i else '#8a9bab', 800, 'c', a=a)


def headline(c, lines, y=372, size=92, col='#ffffff', a=255, dy=0, shadow=.35):
    for i, l in enumerate(lines):
        text(c, l, W / 2, y + dy + i * size * 1.08, size, col, 900, 'c', a=a, shadow=shadow)


def toast(c, label, sub, cx, cy, k, col=TEAL):
    """Pop-in result card. k = 0..1 animation progress."""
    if k <= 0: return
    s = pop(min(k * 2.2, 1)); a = 255 * clamp(k * 5) * clamp((1 - k) * 6)
    w = max(tw(label, 44) + 150, 420); h = 110
    c.save(); c.translate(cx, cy); c.scale(s, s)
    rr(c, -w / 2, -h / 2 + 8, w, h, 55, P('#000000', a * .3, blur=16))
    rr(c, -w / 2, -h / 2, w, h, 55, P('#ffffff', a))
    c.drawCircle(-w / 2 + 56, 0, 34, P(col, a)); check(c, -w / 2 + 56, 2, 15, '#ffffff', 7)
    text(c, label, -w / 2 + 108, -2, 40, INK, 800, a=a)
    text(c, sub, -w / 2 + 108, 36, 28, TEAL_D, 800, a=a)
    c.restore()


# ---------------------------------------------------------------- Dr John Smith
SKIN, SKIN_D, HAIR = '#f0c29b', '#dba57b', '#3b2a20'


def _limb(c, x, y, ang, ln, wd, col, hand=None, cuff=None):
    c.save(); c.translate(x, y); c.rotate(ang)
    rr(c, -wd / 2, -wd / 2, wd, ln, wd / 2, P(col))
    if cuff: rr(c, -wd / 2, ln - wd * .95, wd, wd * .5, 6, P(cuff))
    if hand: c.drawCircle(0, ln - wd * .15, wd * .5, P(hand))
    c.restore()


def doctor(c, cx, foot, sc, outfit, t, la=12, ra=-12, mood='ok', flip=False):
    """Original flat-style doctor. outfit: intern|resident|surgeon|consultant|director.
    la/ra = arm angles in degrees (0 = straight down, negative swings outward-right)."""
    bob = math.sin(t * 2.4) * 4
    c.save(); c.translate(cx, foot); c.scale(-sc if flip else sc, sc); c.translate(0, 0)
    top = {'intern': '#8fbdb6', 'resident': '#17a394', 'surgeon': '#2f8f9d',
           'consultant': '#ffffff', 'director': '#25303d'}[outfit]
    legs = {'intern': '#7aa9a3', 'resident': '#128778', 'surgeon': '#277c89',
            'consultant': '#33475b', 'director': '#1c2530'}[outfit]
    shoe = {'intern': '#c9c2b6', 'director': '#111111'}.get(outfit, '#e9edf1')
    c.drawOval(skia.Rect.MakeXYWH(-130, -14, 260, 34), P('#000000', 60, blur=10))
    # legs + shoes
    for sx in (-44, 44):
        rr(c, sx - 27, -200, 54, 190, 22, P(legs))
        c.drawOval(skia.Rect.MakeXYWH(sx - 38 + (8 if sx > 0 else -8), -26, 76, 34), P(shoe))
    c.translate(0, bob)
    sh_y = -410
    sleeve = top
    # back arm (left on screen)
    _limb(c, -84, sh_y + 30, la, 170, 46, sleeve, SKIN)
    # torso
    rr(c, -98, sh_y, 196, 240, 54, P(top))
    if outfit == 'consultant':
        rr(c, -98, sh_y + 150, 196, 150, 30, P('#ffffff'))
        pth = skia.Path(); pth.moveTo(-34, sh_y + 4); pth.lineTo(0, sh_y + 130); pth.lineTo(34, sh_y + 4); pth.close()
        c.drawPath(pth, P('#2b6cb0'))
        c.drawLine(0, sh_y + 130, 0, sh_y + 300, P('#d5dde5', stroke=4))
        rr(c, 40, sh_y + 150, 40, 44, 6, P('#eef2f6')); rr(c, 44, sh_y + 140, 8, 26, 3, P(TEAL))
    elif outfit == 'director':
        pth = skia.Path(); pth.moveTo(-40, sh_y + 4); pth.lineTo(0, sh_y + 150); pth.lineTo(40, sh_y + 4); pth.close()
        c.drawPath(pth, P('#ffffff'))
        tie = skia.Path(); tie.moveTo(-12, sh_y + 22); tie.lineTo(12, sh_y + 22); tie.lineTo(16, sh_y + 120)
        tie.lineTo(0, sh_y + 142); tie.lineTo(-16, sh_y + 120); tie.close(); c.drawPath(tie, P(TEAL))
        lp = skia.Path(); lp.moveTo(-40, sh_y + 4); lp.lineTo(-62, sh_y + 70); lp.lineTo(0, sh_y + 150)
        c.drawPath(lp, P('#3a4756', stroke=5))
        lp = skia.Path(); lp.moveTo(40, sh_y + 4); lp.lineTo(62, sh_y + 70); lp.lineTo(0, sh_y + 150)
        c.drawPath(lp, P('#3a4756', stroke=5))
        rr(c, 44, sh_y + 86, 34, 10, 3, P('#ffffff'))  # pocket square
    else:
        pth = skia.Path(); pth.moveTo(-30, sh_y + 2); pth.lineTo(0, sh_y + 60); pth.lineTo(30, sh_y + 2); pth.close()
        c.drawPath(pth, P(SKIN_D))
        rr(c, 34, sh_y + 96, 44, 50, 8, P('#000000', 28))  # chest pocket
        if outfit == 'intern':  # wrinkles + crooked badge
            for wy, wx in ((150, -50), (176, 10), (205, -30)):
                c.drawLine(wx, sh_y + wy, wx + 46, sh_y + wy + 8, P('#000000', 30, stroke=4))
            c.save(); c.rotate(-8, -52, sh_y + 110); rr(c, -70, sh_y + 92, 38, 48, 6, P('#f4f6f8'))
            rr(c, -64, sh_y + 100, 26, 14, 3, P('#9fb2c2')); c.restore()
    if outfit in ('resident', 'consultant'):  # stethoscope
        st = skia.Path(); st.moveTo(-36, sh_y + 6); st.cubicTo(-52, sh_y + 120, 52, sh_y + 120, 36, sh_y + 6)
        c.drawPath(st, P('#2f3b47', stroke=7)); c.drawLine(0, sh_y + 92, 0, sh_y + 150, P('#2f3b47', stroke=7))
        c.drawCircle(0, sh_y + 158, 15, P('#c9d2da')); c.drawCircle(0, sh_y + 158, 7, P('#7b8a97'))
    # neck + head
    rr(c, -24, sh_y - 34, 48, 54, 18, P(SKIN_D))
    hy = sh_y - 104
    c.drawCircle(-80, hy + 8, 16, P(SKIN_D)); c.drawCircle(80, hy + 8, 16, P(SKIN_D))
    c.drawCircle(0, hy, 82, P(SKIN))
    if outfit == 'surgeon':
        cap = skia.Path(); cap.addArc(skia.Rect.MakeXYWH(-88, hy - 92, 176, 176), 180, 180); cap.close()
        c.drawPath(cap, P('#5cc0cc')); rr(c, -88, hy - 14, 176, 20, 8, P('#48aebb'))
    else:
        hair = skia.Path(); hair.moveTo(-84, hy - 6)
        hair.cubicTo(-96, hy - 110, 60, hy - 130, 86, hy - 40)
        hair.cubicTo(88, hy - 20, 84, hy - 10, 82, hy - 2)
        hair.cubicTo(60, hy - 44, 10, hy - 58, -40, hy - 50)
        hair.cubicTo(-62, hy - 46, -76, hy - 30, -84, hy - 6); hair.close()
        c.drawPath(hair, P(HAIR))
    blink = (t * 1.0) % 3.2 < 0.12
    ey = hy + 6
    if outfit == 'director':
        rr(c, -70, ey - 20, 62, 40, 14, P('#101418')); rr(c, 8, ey - 20, 62, 40, 14, P('#101418'))
        c.drawLine(-10, ey - 8, 10, ey - 8, P('#101418', stroke=6)); c.drawLine(-70, ey - 8, -84, ey - 14, P('#101418', stroke=5))
        c.drawLine(70, ey - 8, 84, ey - 14, P('#101418', stroke=5))
        c.drawLine(-58, ey - 10, -40, ey - 10, P('#ffffff', 90, stroke=4)); c.drawLine(20, ey - 10, 38, ey - 10, P('#ffffff', 90, stroke=4))
    else:
        for ex in (-32, 32):
            if blink or mood == 'tired' and (t % 2.2) > 1.9:
                c.drawLine(ex - 10, ey, ex + 10, ey, P('#2a1d16', stroke=5))
            else:
                c.drawOval(skia.Rect.MakeXYWH(ex - 9, ey - 12, 18, 24), P('#2a1d16'))
                c.drawCircle(ex + 3, ey - 5, 3.5, P('#ffffff'))
            if mood == 'tired':
                c.drawArc(skia.Rect.MakeXYWH(ex - 15, ey + 4, 30, 18), 20, 140, False, P('#b98666', stroke=4))
                c.drawLine(ex - 16, ey - (20 if ex < 0 else 32), ex + 16, ey - (32 if ex < 0 else 20), P(HAIR, stroke=7))
            else:
                c.drawArc(skia.Rect.MakeXYWH(ex - 18, ey - 36, 36, 20), 200, 140, False, P(HAIR, stroke=7))
    if outfit == 'surgeon':
        mk = skia.Path(); mk.moveTo(-70, hy + 26); mk.quadTo(0, hy + 14, 70, hy + 26)
        mk.quadTo(64, hy + 84, 0, hy + 90); mk.quadTo(-64, hy + 84, -70, hy + 26); mk.close()
        c.drawPath(mk, P('#bfe6ec')); c.drawLine(-52, hy + 48, 52, hy + 48, P('#9fd3db', stroke=3))
        c.drawLine(-48, hy + 64, 48, hy + 64, P('#9fd3db', stroke=3))
    elif mood == 'tired':
        c.drawArc(skia.Rect.MakeXYWH(-20, hy + 40, 40, 22), 200, 140, False, P('#8a4b3a', stroke=6))
    else:
        big = outfit == 'director' or mood == 'happy'
        c.drawArc(skia.Rect.MakeXYWH(-30, hy + 18, 60, 44 if big else 34), 20, 140, False, P('#8a4b3a', stroke=7))
    # front arm (right on screen)
    cuff = '#ffffff' if outfit == 'director' else None
    _limb(c, 84, sh_y + 30, ra, 170, 46, sleeve, SKIN, cuff)
    if outfit == 'director':  # gold watch on the front wrist
        c.save(); c.translate(84, sh_y + 30); c.rotate(ra)
        rr(c, -25, 118, 50, 20, 6, P(GOLD)); c.drawCircle(0, 128, 15, P('#ffd774')); c.drawCircle(0, 128, 9, P('#fff4cf'))
        c.restore()
    c.restore()


def new_surface():
    return skia.Surface(W, H)


def to_rgba(s):
    return s.toarray(colorType=skia.kRGBA_8888_ColorType).tobytes()
