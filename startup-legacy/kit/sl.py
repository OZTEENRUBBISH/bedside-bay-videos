"""Startup Legacy drawing kit: brand, founder character, partner, HUD and illustrated scenes.
Builds on the shared helpers in ../../kit/lib.py (text, shapes, easing, render_video)."""
import os, sys, math, skia
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kit'))
from lib import *  # noqa: F401,F403  (W, H, C, P, grad, rr, text, tw, headline, ease, eio, pop, lerp, sparkle, check, render_video ...)

GREEN, GREEN_D, SUIT, LAPEL, SGOLD, BG = '#1f9a78', '#0d5a49', '#15171c', '#2c313a', '#f2c14e', '#14181f'
_svg = {}


def emblem(c, x, y, s, suit_only=False):
    """The Startup Legacy app icon (green tile, black suit, gold tie, gold up-arrow badge)."""
    f = 'emblem_suit.svg' if suit_only else 'emblem.svg'
    if f not in _svg:
        _svg[f] = skia.SVGDOM.MakeFromStream(skia.Stream.MakeFromFile(os.path.join(HERE, f)))
        _svg[f].setContainerSize(skia.Size(64, 64))
    c.save(); c.translate(x, y); c.scale(s / 64, s / 64); _svg[f].render(c); c.restore()


def brand_bar(c, y=128):
    """White pill with icon + wordmark, on every frame."""
    w = 600; x = (W - w) / 2
    rr(c, x, y + 8, w, 124, 62, P('#000000', 60, blur=18))
    rr(c, x, y, w, 124, 62, P('#ffffff'))
    emblem(c, x + 18, y + 16, 92)
    text(c, 'Startup Legacy', x + 124, y + 64, 50, BG, 800)
    text(c, 'Business career simulator', x + 125, y + 100, 26, '#5b6472', 600)


STAGES = ['Broke', 'Founder', 'CEO', 'Millionaire', 'Legacy']


def hud(c, stage_i, worth, prog, y=1262, a=255, bump=0.0, who='YOU'):
    """Career card: player, stage, net worth, five-step ladder. prog = 0..5 segments filled."""
    x, w, h = 60, 960, 226
    rr(c, x, y + 10, w, h, 44, P('#000000', 70 * a / 255, blur=22))
    rr(c, x, y, w, h, 44, P('#ffffff', a))
    text(c, who, x + 40, y + 58, 26, '#5b6472', 800, a=a)
    text(c, STAGES[stage_i], x + 40, y + 122, 60, BG, 900, a=a)
    bs = 62 * (1 + .08 * bump)
    text(c, money(worth), x + w - 40, y + 122, bs, GREEN_D, 900, 'r', a=a)
    text(c, 'NET WORTH', x + w - 40, y + 58, 26, '#5b6472', 800, 'r', a=a)
    sw = (w - 80 - 4 * 12) / 5
    for i in range(5):
        sx = x + 40 + i * (sw + 12)
        rr(c, sx, y + 160, sw, 16, 8, P('#e1e5ea', a))
        f = clamp(prog - i)
        if f > 0: rr(c, sx, y + 160, sw * f, 16, 8, P(SGOLD if i == 4 else GREEN, a))
        text(c, STAGES[i], sx + sw / 2, y + 204, 22, BG if i == stage_i else '#8a94a3', 800, 'c', a=a)


def money(v):
    v = float(v)
    if v >= 1e9: return f'${v / 1e9:.2f}B'
    if v >= 1e7: return f'${v / 1e6:.1f}M'
    if v >= 1e6: return f'${v / 1e6:.2f}M'
    return '$' + f'{int(v):,}'


def toast(c, label, sub, cx, cy, k, col=GREEN):
    if k <= 0: return
    s = pop(min(k * 2.2, 1)); a = 255 * clamp(k * 5) * clamp((1 - k) * 6)
    w = max(tw(label, 44) + 150, 420); h = 110
    c.save(); c.translate(cx, cy); c.scale(s, s)
    rr(c, -w / 2, -h / 2 + 8, w, h, 55, P('#000000', a * .3, blur=16))
    rr(c, -w / 2, -h / 2, w, h, 55, P('#ffffff', a))
    c.drawCircle(-w / 2 + 56, 0, 34, P(col, a)); check(c, -w / 2 + 56, 2, 15, '#ffffff', 7)
    text(c, label, -w / 2 + 108, -2, 40, BG, 800, a=a)
    text(c, sub, -w / 2 + 108, 36, 28, GREEN_D, 800, a=a)
    c.restore()


def tag(c, label, x, y, k):
    """Gold label that pops in (k = 0..1)."""
    if k <= 0: return
    s = pop(k); w = tw(label, 36) + 60
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -w / 2, -34, w, 68, 34, P('#000000', 70, blur=12)); rr(c, -w / 2, -38, w, 68, 34, P(SGOLD))
    text(c, label, 0, 8, 36, BG, 900, 'c'); c.restore()


# ---------------------------------------------------------------- the founder (player character)
SKIN, SKIN_D, HAIR = '#e9b98f', '#d29e72', '#2f2219'


def _limb(c, x, y, ang, ln, wd, col, hand=None, cuff=None):
    c.save(); c.translate(x, y); c.rotate(ang)
    rr(c, -wd / 2, -wd / 2, wd, ln, wd / 2, P(col))
    if cuff: rr(c, -wd / 2, ln - wd * .95, wd, wd * .5, 6, P(cuff))
    if hand: c.drawCircle(0, ln - wd * .15, wd * .5, P(hand))
    c.restore()


def founder(c, cx, foot, sc, outfit, t, la=12, ra=-12, mood='ok', flip=False, shades=None, watch=None):
    """Original flat-style founder. outfit: broke | smart | suit | mogul | groom.
    la/ra = arm angles in degrees (0 = down; negative swings the front arm out/up)."""
    bob = math.sin(t * 2.4) * 4
    c.save(); c.translate(cx, foot); c.scale(-sc if flip else sc, sc)
    top = {'broke': '#5f6b78', 'smart': '#f3f5f7', 'suit': SUIT, 'mogul': SUIT, 'groom': '#1b1e24'}[outfit]
    legs = {'broke': '#34496a', 'smart': '#2c3a4f', 'suit': SUIT, 'mogul': SUIT, 'groom': '#1b1e24'}[outfit]
    shoe = {'broke': '#c9c2b6', 'smart': '#5a3b22'}.get(outfit, '#0b0c0f')
    sleeve = {'smart': '#e8ecf0'}.get(outfit, top)
    shades = outfit == 'mogul' if shades is None else shades
    watch = outfit in ('mogul', 'groom') if watch is None else watch
    c.drawOval(skia.Rect.MakeXYWH(-130, -14, 260, 34), P('#000000', 60, blur=10))
    for sx in (-44, 44):
        rr(c, sx - 27, -200, 54, 190, 22, P(legs))
        if outfit == 'broke':  # ripped knee
            rr(c, sx - 16, -110, 30, 12, 6, P('#8aa0be'))
        c.drawOval(skia.Rect.MakeXYWH(sx - 38 + (8 if sx > 0 else -8), -26, 76, 34), P(shoe))
    c.translate(0, bob)
    sh_y = -410
    _limb(c, -84, sh_y + 30, la, 170, 46, sleeve, SKIN, '#ffffff' if outfit in ('suit', 'mogul', 'groom') else None)
    rr(c, -98, sh_y, 196, 240, 54, P(top))
    if outfit in ('suit', 'mogul', 'groom'):
        v = skia.Path(); v.moveTo(-40, sh_y + 4); v.lineTo(0, sh_y + 150); v.lineTo(40, sh_y + 4); v.close(); c.drawPath(v, P('#ffffff'))
        tie = skia.Path(); tie.moveTo(-12, sh_y + 22); tie.lineTo(12, sh_y + 22); tie.lineTo(16, sh_y + 120)
        tie.lineTo(0, sh_y + 142); tie.lineTo(-16, sh_y + 120); tie.close()
        if outfit == 'groom':  # bow tie + flower
            b = skia.Path(); b.moveTo(0, sh_y + 30); b.lineTo(-26, sh_y + 16); b.lineTo(-26, sh_y + 44); b.close()
            b.moveTo(0, sh_y + 30); b.lineTo(26, sh_y + 16); b.lineTo(26, sh_y + 44); b.close(); c.drawPath(b, P('#0b0c0f'))
            c.drawCircle(-62, sh_y + 70, 14, P('#ffffff')); c.drawCircle(-62, sh_y + 70, 6, P(SGOLD))
        else:
            c.drawPath(tie, P(SGOLD))
        for sgn in (-1, 1):
            lp = skia.Path(); lp.moveTo(40 * sgn, sh_y + 4); lp.lineTo(64 * sgn, sh_y + 76); lp.lineTo(0, sh_y + 150); lp.close()
            c.drawPath(lp, P(LAPEL))
        c.drawCircle(0, sh_y + 180, 6, P('#3a404b')); c.drawCircle(0, sh_y + 212, 6, P('#3a404b'))
        if outfit != 'groom': rr(c, 44, sh_y + 92, 34, 10, 3, P(SGOLD if outfit == 'mogul' else '#ffffff'))
    elif outfit == 'smart':
        v = skia.Path(); v.moveTo(-30, sh_y + 2); v.lineTo(0, sh_y + 46); v.lineTo(30, sh_y + 2); v.close(); c.drawPath(v, P(SKIN_D))
        c.drawLine(0, sh_y + 46, 0, sh_y + 236, P('#cfd6dd', stroke=4))
        for by in (90, 140, 190): c.drawCircle(10, sh_y + by, 5, P('#cfd6dd'))
        # lanyard + badge
        ln = skia.Path(); ln.moveTo(-34, sh_y + 6); ln.lineTo(-10, sh_y + 120); ln.lineTo(18, sh_y + 6); c.drawPath(ln, P(GREEN, stroke=6))
        rr(c, -36, sh_y + 116, 52, 64, 8, P('#ffffff')); rr(c, -30, sh_y + 124, 40, 20, 4, P(GREEN))
    else:  # hoodie
        hood = skia.Path(); hood.moveTo(-70, sh_y + 6); hood.quadTo(0, sh_y + 70, 70, sh_y + 6); c.drawPath(hood, P('#4b5562', stroke=18))
        c.drawLine(-16, sh_y + 40, -20, sh_y + 110, P('#d9dde2', stroke=5)); c.drawLine(16, sh_y + 40, 20, sh_y + 110, P('#d9dde2', stroke=5))
        rr(c, -60, sh_y + 150, 120, 60, 24, P('#535e6b'))
        rr(c, 30, sh_y + 60, 36, 28, 6, P('#000000', 30))  # patch
    rr(c, -24, sh_y - 34, 48, 54, 18, P(SKIN_D))
    hy = sh_y - 104
    c.drawCircle(-80, hy + 8, 16, P(SKIN_D)); c.drawCircle(80, hy + 8, 16, P(SKIN_D))
    c.drawCircle(0, hy, 82, P(SKIN))
    hair = skia.Path(); hair.moveTo(-84, hy - 6)
    if outfit == 'broke':  # messy
        hair.cubicTo(-100, hy - 120, 70, hy - 140, 88, hy - 34); hair.lineTo(70, hy - 52); hair.lineTo(60, hy - 30); hair.lineTo(40, hy - 60)
        hair.lineTo(10, hy - 44); hair.lineTo(-20, hy - 64); hair.lineTo(-44, hy - 42); hair.lineTo(-64, hy - 50); hair.close()
    else:  # neat side part
        hair.cubicTo(-96, hy - 112, 64, hy - 132, 86, hy - 40); hair.cubicTo(88, hy - 20, 84, hy - 10, 82, hy - 2)
        hair.cubicTo(60, hy - 48, 10, hy - 62, -40, hy - 52); hair.cubicTo(-62, hy - 48, -76, hy - 30, -84, hy - 6); hair.close()
    c.drawPath(hair, P(HAIR))
    blink = (t * 1.0) % 3.2 < 0.12; ey = hy + 6
    if shades:
        rr(c, -72, ey - 22, 64, 42, 14, P('#0b0d10')); rr(c, 8, ey - 22, 64, 42, 14, P('#0b0d10'))
        c.drawLine(-10, ey - 8, 10, ey - 8, P('#0b0d10', stroke=6))
        c.drawLine(-60, ey - 10, -42, ey - 10, P('#ffffff', 90, stroke=4)); c.drawLine(20, ey - 10, 38, ey - 10, P('#ffffff', 90, stroke=4))
    else:
        for ex in (-32, 32):
            if blink or (mood == 'tired' and (t % 2.2) > 1.9): c.drawLine(ex - 10, ey, ex + 10, ey, P('#2a1d16', stroke=5))
            else:
                c.drawOval(skia.Rect.MakeXYWH(ex - 9, ey - 12, 18, 24), P('#2a1d16')); c.drawCircle(ex + 3, ey - 5, 3.5, P('#ffffff'))
            if mood == 'tired':
                c.drawArc(skia.Rect.MakeXYWH(ex - 15, ey + 4, 30, 18), 20, 140, False, P('#b98666', stroke=4))
                c.drawLine(ex - 16, ey - (20 if ex < 0 else 32), ex + 16, ey - (32 if ex < 0 else 20), P(HAIR, stroke=7))
            else:
                c.drawArc(skia.Rect.MakeXYWH(ex - 18, ey - 36, 36, 20), 200, 140, False, P(HAIR, stroke=7))
    if mood == 'tired':
        c.drawArc(skia.Rect.MakeXYWH(-20, hy + 40, 40, 22), 200, 140, False, P('#8a4b3a', stroke=6))
        rr(c, -50, hy + 34, 100, 24, 12, P('#000000', 22))  # stubble
    else:
        big = mood == 'happy' or outfit in ('mogul', 'groom')
        c.drawArc(skia.Rect.MakeXYWH(-30, hy + 18, 60, 44 if big else 34), 20, 140, False, P('#8a4b3a', stroke=7))
    cuff = '#ffffff' if outfit in ('suit', 'mogul', 'groom') else None
    _limb(c, 84, sh_y + 30, ra, 170, 46, sleeve, SKIN, cuff)
    if watch:
        c.save(); c.translate(84, sh_y + 30); c.rotate(ra)
        rr(c, -25, 112, 50, 22, 6, P(SGOLD)); c.drawCircle(0, 123, 16, P('#ffd774')); c.drawCircle(0, 123, 10, P('#fff4cf'))
        c.restore()
    c.restore()


def partner(c, cx, foot, sc, t, dress='gown', la=10, ra=-10):
    """Original flat-style partner (wife). dress: gown | wedding."""
    bob = math.sin(t * 2.4 + 1) * 4
    c.save(); c.translate(cx, foot); c.scale(sc, sc)
    c.drawOval(skia.Rect.MakeXYWH(-130, -14, 260, 34), P('#000000', 60, blur=10))
    c.translate(0, bob)
    col = '#ffffff' if dress == 'wedding' else '#b3243c'
    col_d = '#e7ecf2' if dress == 'wedding' else '#8f1a2e'
    sh_y = -400
    _limb(c, -70, sh_y + 30, la, 160, 38, SKIN, SKIN)
    sk = skia.Path(); sk.moveTo(-80, sh_y + 10); sk.lineTo(80, sh_y + 10); sk.lineTo(84, sh_y + 160)
    sk.quadTo(150, sh_y + 300, 160, sh_y + 400); sk.lineTo(-160, sh_y + 400); sk.quadTo(-150, sh_y + 300, -84, sh_y + 160); sk.close()
    c.drawPath(sk, P(col))
    for i in range(3):
        f = skia.Path(); f.moveTo(-40 + i * 40, sh_y + 200); f.quadTo(-60 + i * 50, sh_y + 320, -90 + i * 80, sh_y + 398); c.drawPath(f, P(col_d, stroke=5))
    rr(c, -84, sh_y + 150, 168, 18, 9, P(SGOLD if dress != 'wedding' else '#f1e4c8'))
    rr(c, -22, sh_y - 34, 44, 50, 18, P(SKIN_D))
    hy = sh_y - 100
    hb = skia.Path(); hb.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-92, hy - 70, 184, 250), 80, 80)); c.drawPath(hb, P('#5a3a22'))
    c.drawCircle(0, hy, 78, P(SKIN))
    fr = skia.Path(); fr.moveTo(-82, hy + 10); fr.cubicTo(-90, hy - 110, 90, hy - 110, 82, hy + 10); fr.cubicTo(60, hy - 50, -10, hy - 70, -82, hy + 10); fr.close()
    c.drawPath(fr, P('#5a3a22'))
    if dress == 'wedding':  # veil + tiara
        vl = skia.Path(); vl.moveTo(-70, hy - 50); vl.quadTo(-170, hy + 120, -150, sh_y + 260); vl.lineTo(-100, sh_y + 250); vl.quadTo(-110, hy + 60, -40, hy - 60); vl.close()
        c.drawPath(vl, P('#ffffff', 170))
        for i in range(5): c.drawCircle(-36 + i * 18, hy - 66 - (8 if i == 2 else 0), 7, P('#fff4cf'))
    ey = hy + 6; blink = (t + .7) % 3.4 < .12
    for ex in (-30, 30):
        if blink: c.drawLine(ex - 9, ey, ex + 9, ey, P('#2a1d16', stroke=5))
        else: c.drawOval(skia.Rect.MakeXYWH(ex - 8, ey - 11, 16, 22), P('#2a1d16')); c.drawCircle(ex + 3, ey - 5, 3, P('#ffffff'))
        c.drawLine(ex - 10, ey - 10, ex - 16, ey - 16, P('#2a1d16', stroke=3)); c.drawLine(ex + 10, ey - 10, ex + 14, ey - 18, P('#2a1d16', stroke=3))
    c.drawCircle(-46, hy + 32, 12, P('#f08a8a', 90)); c.drawCircle(46, hy + 32, 12, P('#f08a8a', 90))
    c.drawArc(skia.Rect.MakeXYWH(-24, hy + 22, 48, 34), 20, 140, False, P('#b5404f', stroke=7))
    c.drawCircle(-74, hy + 28, 8, P(SGOLD)); c.drawCircle(74, hy + 28, 8, P(SGOLD))  # earrings
    _limb(c, 70, sh_y + 30, ra, 160, 38, SKIN, SKIN)
    c.restore()


# ---------------------------------------------------------------- scenes (each draws the full frame background + stage)
def broke_room(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#2a333f', '#1b212a']))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), P('#2e2620'))
    for i in range(6): c.drawLine(0, 1190 + i * 130, W, 1190 + i * 130, P('#241d18', stroke=4))
    c.drawRect(skia.Rect.MakeXYWH(0, 1136, W, 16), P('#39424e'))
    cr = skia.Path(); cr.moveTo(960, 520); cr.lineTo(930, 600); cr.lineTo(965, 660); cr.lineTo(940, 740); c.drawPath(cr, P('#141a21', stroke=5))
    c.drawOval(skia.Rect.MakeXYWH(40, 900, 260, 150), P('#1d242d', 160, blur=24))
    rr(c, 110, 570, 230, 280, 10, P('#414c59')); rr(c, 124, 584, 202, 252, 6, P('#0e1522'))
    c.drawCircle(270, 650, 30, P('#dfe6f0')); c.drawCircle(282, 642, 26, P('#0e1522'))
    for sx, sy in ((160, 620), (200, 700), (300, 760), (150, 790)): c.drawCircle(sx, sy, 3, P('#ffffff', 150 + 100 * math.sin(t * 3 + sx)))
    c.drawLine(225, 584, 225, 836, P('#414c59', stroke=10, cap=False)); c.drawLine(124, 710, 326, 710, P('#414c59', stroke=10, cap=False))
    c.save(); c.rotate(5, 900, 690); rr(c, 810, 620, 190, 140, 6, P('#f1ece2'))
    text(c, 'RENT', 905, 680, 44, '#d64545', 900, 'c'); text(c, 'OVERDUE', 905, 730, 34, '#d64545', 900, 'c'); c.restore()
    ang = math.sin(t * 1.7) * 7
    c.save(); c.translate(470, 500); c.rotate(ang)
    c.drawLine(0, 0, 0, 150, P('#11161c', stroke=6)); rr(c, -14, 146, 28, 26, 5, P('#555f6b'))
    c.drawCircle(0, 196, 150, P('#ffe7a0', 46 + 10 * math.sin(t * 9), blur=60)); c.drawCircle(0, 196, 30, P('#fff0b8')); c.restore()
    rr(c, 50, 1096, 430, 78, 26, P('#b6ae9f'))
    for i in range(7): c.drawLine(96 + i * 54, 1104, 96 + i * 54, 1166, P('#9c9484', stroke=4))
    rr(c, 66, 1056, 150, 58, 24, P('#dcd6ca')); rr(c, 240, 1078, 240, 74, 30, P('#5f6f82'))
    # empty wallet + coins on the floor
    rr(c, 820, 1150, 150, 62, 12, P('#5a3b22')); rr(c, 830, 1140, 130, 24, 8, P('#6e4a2c'))
    for i, (wx, wy) in enumerate(((800, 1206), (990, 1200), (1010, 1214))): c.drawCircle(wx, wy, 12, P('#b7a27a'))
    founder(c, 640, 1218, 1.0, 'broke', t, la=7, ra=-7, mood='tired')


def garage(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#3b4350', '#262c35']))
    for i in range(10): c.drawLine(0, 470 + i * 64, W, 470 + i * 64, P('#ffffff', 14, stroke=4))  # roller door ribs
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), P('#5b5f66'))
    c.drawOval(skia.Rect.MakeXYWH(560, 1170, 360, 60), P('#4a4e55'))  # oil stain
    # pegboard with sticky notes
    rr(c, 600, 520, 420, 300, 12, P('#a4835c'))
    for i, (nx, ny, col, lab) in enumerate(((630, 550, '#ffe066', 'IDEA'), (760, 560, '#8ce99a', 'BUILD'), (890, 548, '#74c0fc', 'LAUNCH'),
                                             (690, 680, '#ffa8a8', 'SELL'), (830, 690, '#ffe066', 'GROW'))):
        c.save(); c.rotate(math.sin(i * 2.1) * 6, nx + 50, ny + 50); rr(c, nx, ny, 104, 100, 4, P(col))
        text(c, lab, nx + 52, ny + 62, 28 if len(lab) < 6 else 24, BG, 900, 'c'); c.restore()
    # desk + laptop with rising chart
    rr(c, 300, 1010, 620, 30, 8, P('#7a5636')); rr(c, 320, 1040, 26, 110, 6, P('#5e4129')); rr(c, 874, 1040, 26, 110, 6, P('#5e4129'))
    rr(c, 560, 870, 270, 160, 14, P('#c9d1da')); rr(c, 572, 882, 246, 136, 8, P('#0f1720'))
    pts = [(.0, .8), (.2, .7), (.35, .74), (.5, .5), (.65, .55), (.8, .3), (1, .12)]
    k = clamp((t % 4) / 2.5); pth = skia.Path()
    for i, (px, py) in enumerate(pts):
        if px > k: break
        (pth.lineTo if i else pth.moveTo)(586 + px * 218, 892 + py * 112)
    c.drawPath(pth, P('#3ee08a', stroke=6))
    rr(c, 540, 1022, 310, 14, 6, P('#aab4bf'))
    # mug with steam + desk lamp
    rr(c, 380, 960, 60, 54, 10, P('#ffffff')); c.drawArc(skia.Rect.MakeXYWH(428, 970, 30, 30), -90, 180, False, P('#ffffff', stroke=7))
    for i in range(2):
        kk = (t * .6 + i / 2) % 1; sx = 398 + i * 24
        s = skia.Path(); s.moveTo(sx, 952 - kk * 60); s.quadTo(sx + 12, 936 - kk * 60, sx, 920 - kk * 60); c.drawPath(s, P('#ffffff', 120 * (1 - kk), stroke=5))
    c.drawCircle(860, 760, 160, P('#ffe7a0', 30, blur=60))
    founder(c, 240, 1218, 1.0, 'smart', t, la=10, ra=-70 + math.sin(t * 8) * 6, mood='happy')


def office(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#9fd3ec', '#e8f4fb']))
    for i, (bx, bw, bh) in enumerate(((0, 140, 360), (150, 110, 470), (270, 160, 300), (440, 120, 520), (570, 150, 380), (730, 130, 560), (870, 210, 420))):
        rr(c, bx, 1150 - bh, bw, bh, 6, P('#7fa5bd', 200))
        for wy in range(int(1150 - bh + 20), 1120, 46):
            for wx in range(bx + 16, bx + bw - 20, 34): rr(c, wx, wy, 16, 22, 3, P('#ffffff', 120))
    c.drawRect(skia.Rect.MakeXYWH(0, 470, W, 680), P('#ffffff', 40))
    for x in (0, 360, 720, 1074): c.drawRect(skia.Rect.MakeXYWH(x, 470, 10, 680), P('#2f3a46'))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), P('#3d4652'))
    # big screen with revenue chart
    rr(c, 470, 540, 540, 340, 18, P('#0f1720')); rr(c, 486, 556, 508, 308, 10, P('#16222e'))
    text(c, 'REVENUE', 512, 604, 30, '#9fb2c2', 800)
    k = clamp(t / 2.4)
    for i in range(7):
        h = (36 + i * i * 4.8) * eio(k * 1.4 - i * .08)
        rr(c, 520 + i * 66, 840 - h, 44, max(h, 0), 8, P(GREEN if i < 6 else SGOLD))
    text(c, money(lerp(18000, 2400000, eio(k))) + '/yr', 980, 604, 34, '#3ee08a', 900, 'r')
    # desk
    rr(c, 80, 1060, 900, 30, 10, P('#1d232b')); rr(c, 120, 1090, 30, 60, 6, P('#1d232b')); rr(c, 910, 1090, 30, 60, 6, P('#1d232b'))
    rr(c, 760, 990, 70, 70, 14, P('#2f8f62'))  # plant pot
    for a in (-40, -10, 20, 50):
        lf = skia.Path(); lf.moveTo(795, 990); lf.quadTo(795 + a * 1.4, 930, 795 + a * 2, 890); c.drawPath(lf, P('#3fae6a', stroke=18))
    founder(c, 300, 1218, 1.0, 'suit', t, la=10, ra=-120 + math.sin(t * 4) * 8, mood='happy')


TICKERS = [('BRVX', 12.4), ('KANO', 8.1), ('VELT', 21.7), ('QORA', 5.6), ('HALN', 14.2), ('MIRA', 9.9)]


def trading(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#0b1220', '#101a2b']))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), P('#0a0f18'))
    for row in range(2):
        for col in range(3):
            x, y = 70 + col * 320, 500 + row * 260
            rr(c, x, y, 300, 230, 14, P('#1b2333')); rr(c, x + 10, y + 10, 280, 210, 8, P('#0c1422'))
            sym, pc = TICKERS[row * 3 + col]
            text(c, sym, x + 26, y + 52, 32, '#d9e2ef', 900); text(c, f'+{pc:.1f}%', x + 280, y + 52, 30, '#3ee08a', 900, 'r')
            for i in range(9):  # candles trending up
                base = y + 200 - i * 14 - (math.sin(i * 1.7 + row + col) * 10); up = (i + row + col) % 4 != 1
                k = clamp(t * 3 - i * .25)
                if k <= 0: continue
                hh = 40 * k
                c.drawLine(x + 34 + i * 28, base - hh - 14, x + 34 + i * 28, base + 10, P('#5c6b80', stroke=3))
                rr(c, x + 24 + i * 28, base - hh, 20, hh, 3, P('#3ee08a' if up else '#ff6b6b'))
    # scrolling ticker tape
    rr(c, 0, 1040, W, 70, 0, P('#111a29'))
    s = '     '.join(f'{a}  +{b:.1f}%' for a, b in TICKERS * 2); off = (t * 220) % (tw(s, 38, 800) / 2)
    text(c, s, 40 - off, 1088, 38, '#3ee08a', 800)
    founder(c, 880, 1218, .92, 'suit', t, la=150 + math.sin(t * 7) * 10, ra=-150 - math.sin(t * 7) * 10, mood='happy')


def mansion(c, t, car_in=True, coins=True):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1130, ['#272b73', '#8a4a94', '#f2707a', '#ffc37d']))
    c.drawCircle(800, 900, 210, P('#ffe2a6', 90, blur=70)); c.drawCircle(800, 900, 112, P('#fff0c4'))
    hill = skia.Path(); hill.moveTo(0, 1080); hill.quadTo(300, 980, 620, 1070); hill.quadTo(860, 1010, W, 1060); hill.lineTo(W, 1140); hill.lineTo(0, 1140); hill.close()
    c.drawPath(hill, P('#5b3f86', 200))
    c.drawRect(skia.Rect.MakeXYWH(0, 1120, W, H - 1120), grad(0, 1120, 0, 1500, ['#2e9f6b', '#1c7a50']))
    drv = skia.Path(); drv.moveTo(40, 1150); drv.lineTo(640, 1150); drv.lineTo(W + 200, 1500); drv.lineTo(-200, 1500); drv.close(); c.drawPath(drv, P('#c9cdd3'))
    tr = skia.Path(); tr.moveTo(1010, 1124); tr.quadTo(985, 900, 1030, 740); c.drawPath(tr, P('#7a5636', stroke=26))
    for ang in (-150, -110, -60, -20, 30, 200):
        a = math.radians(ang + math.sin(t * 1.5 + ang) * 3); f = skia.Path(); f.moveTo(1030, 740)
        f.quadTo(1030 + math.cos(a) * 90, 740 + math.sin(a) * 90 - 50, 1030 + math.cos(a) * 190, 740 + math.sin(a) * 150 + 20); c.drawPath(f, P('#1f8f57', stroke=24))
    rr(c, 150, 640, 330, 190, 8, P('#fbf8f2')); c.drawRect(skia.Rect.MakeXYWH(126, 622, 378, 26), P('#34414f'))
    rr(c, 50, 812, 560, 312, 8, P('#f4f0e8')); c.drawRect(skia.Rect.MakeXYWH(26, 794, 608, 28), P('#34414f'))
    glow = 220 + 30 * math.sin(t * 2)
    for wx, wy, ww, wh in ((176, 672, 130, 120), (322, 672, 130, 120), (84, 860, 150, 200), (430, 860, 150, 200)):
        rr(c, wx, wy, ww, wh, 6, P('#ffd98a', glow)); c.drawLine(wx + ww / 2, wy, wx + ww / 2, wy + wh, P('#34414f', stroke=5, cap=False))
        c.drawLine(wx, wy + wh * .5, wx + ww, wy + wh * .5, P('#34414f', stroke=5, cap=False))
    rr(c, 276, 900, 112, 224, 8, P('#34414f')); c.drawCircle(366, 1016, 7, P(SGOLD))
    for px in (262, 402): rr(c, px - 10, 880, 20, 244, 6, P('#e2dccf'))
    rr(c, 30, 1108, 600, 22, 6, P('#d9d3c6'))
    founder(c, 780, 1236, .98, 'mogul', t, la=10, ra=-158 + math.sin(t * 6) * 14)
    k = (t * .9) % 1; sparkle(c, 912, 742, 36 * math.sin(k * math.pi), 255, '#fff6d8')
    supercar(c, t, car_in)
    if coins:
        for i in range(9):
            k = (t * .45 + i * .137) % 1; x = (i * 211 + 97) % 1000 + 40; y = 500 + k * 640
            c.drawCircle(x, y, 20, P(SGOLD, 230 * (1 - k * .5))); c.drawCircle(x, y, 13, P('#ffd774', 230 * (1 - k * .5)))


def supercar(c, t, car_in=True, col=('#ff4d4d', '#c01f2e'), dx=0):
    slide = (1 - ease((t - .25) / 1.0)) * 760 if car_in else 0
    c.save(); c.translate(-slide - 440 + dx, -26 + math.sin(t * 22) * (1.5 if slide > 4 else 0)); c.translate(1520, 0); c.scale(-1, 1)
    c.drawOval(skia.Rect.MakeXYWH(560, 1262, 400, 36), P('#000000', 70, blur=10))
    body = skia.Path(); body.moveTo(556, 1250); body.lineTo(552, 1214); body.quadTo(600, 1178, 680, 1170)
    body.quadTo(730, 1116, 810, 1116); body.quadTo(880, 1118, 910, 1166); body.quadTo(962, 1176, 966, 1214); body.lineTo(966, 1250); body.close()
    c.drawPath(body, grad(0, 1116, 0, 1250, list(col)))
    win = skia.Path(); win.moveTo(700, 1170); win.quadTo(738, 1132, 806, 1132); win.quadTo(858, 1134, 884, 1168); win.close()
    c.drawPath(win, P('#1c2530')); c.drawLine(796, 1132, 796, 1168, P(col[1], stroke=7, cap=False))
    rr(c, 556, 1206, 34, 14, 7, P('#fff3b0')); rr(c, 944, 1204, 22, 14, 6, P('#ffb3b3'))
    c.drawLine(600, 1232, 920, 1232, P('#000000', 60, stroke=5))
    for wx in (640, 880):
        c.drawCircle(wx, 1250, 42, P('#14181d')); c.drawCircle(wx, 1250, 24, P('#cfd6dd'))
        c.save(); c.rotate(-t * 300 if slide > 4 else 0, wx, 1250)
        for i in range(5):
            a = i * 2 * math.pi / 5; c.drawLine(wx, 1250, wx + math.cos(a) * 22, 1250 + math.sin(a) * 22, P('#7b8894', stroke=5))
        c.restore()
    sparkle(c, 760, 1150, 26 * abs(math.sin(t * 3)), 255)
    c.restore()


def garage_cars(c, t):
    """Showroom garage with three supercars."""
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#1a1d23', '#2b3039']))
    for i in range(4):
        x = 90 + i * 250; rr(c, x, 560, 160, 14, 7, P('#f6f8fb', 220)); c.drawCircle(x + 80, 640, 200, P('#ffffff', 12, blur=60))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), grad(0, 1150, 0, 1600, ['#3a3f48', '#22262c']))
    c.drawRect(skia.Rect.MakeXYWH(0, 980, W, 10), P('#ffffff', 30))
    for dx, col in ((-120, ('#ffd43b', '#e0a800')), (380, ('#4dabf7', '#1c6fc0'))):  # back row on a raised display
        c.save(); c.translate(540, 1010); c.scale(.72, .72); c.translate(-540, -1260); supercar(c, t + 10, False, col, dx=dx); c.restore()
    supercar(c, t, True)
    founder(c, 190, 1218, .9, 'mogul', t, la=10, ra=-60 + math.sin(t * 5) * 10)


def watch(c, t):
    """Close-up of a gold watch on the wrist."""
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, W, H, ['#1a1410', '#3a2a1c']))
    c.drawCircle(540, 820, 420, P(SGOLD, 40, blur=120))
    c.save(); c.rotate(-18, 540, 820)
    rr(c, -100, 720, 1300, 220, 110, P(SUIT)); rr(c, 560, 712, 120, 236, 30, P('#ffffff'))  # sleeve + cuff
    rr(c, 670, 740, 520, 180, 90, P(SKIN))  # wrist + hand
    rr(c, 360, 690, 160, 280, 40, P('#b88a2c')); rr(c, 370, 700, 140, 260, 36, P(SGOLD))  # strap
    c.restore()
    k = pop(clamp(t / .6)); c.save(); c.translate(500, 760); c.scale(k, k)
    c.drawCircle(0, 0, 175, P('#8a6a1c')); c.drawCircle(0, 0, 160, P(SGOLD)); c.drawCircle(0, 0, 132, P('#0f1a2a'))
    for i in range(12):
        a = i * math.pi / 6; c.drawLine(math.cos(a) * 108, math.sin(a) * 108, math.cos(a) * 122, math.sin(a) * 122, P(SGOLD, stroke=8 if i % 3 == 0 else 4))
    hm = t * 0.4; hs = t * 6.0
    c.drawLine(0, 0, math.cos(hm - 1.4) * 64, math.sin(hm - 1.4) * 64, P('#ffffff', stroke=10))
    c.drawLine(0, 0, math.cos(hs * .3 - .6) * 96, math.sin(hs * .3 - .6) * 96, P('#ffffff', stroke=6))
    c.drawLine(0, 0, math.cos(hs - 1.5) * 110, math.sin(hs - 1.5) * 110, P('#ff6b6b', stroke=3))
    c.drawCircle(0, 0, 10, P(SGOLD)); rr(c, 158, -18, 34, 36, 8, P('#b88a2c'))
    c.restore()
    for i in range(6):
        kk = (t * .7 + i / 6) % 1; a = i * 1.05
        sparkle(c, 500 + math.cos(a) * 240, 760 + math.sin(a) * 240, 30 * math.sin(kk * math.pi), 255, '#fff6d8')


def yacht(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1060, ['#1e3a8a', '#7c4d9e', '#f08a6c', '#ffd39a']))
    c.drawCircle(300, 930, 150, P('#fff1c9', 110, blur=60)); c.drawCircle(300, 930, 90, P('#fff4d6'))
    c.drawRect(skia.Rect.MakeXYWH(0, 1000, W, H - 1000), grad(0, 1000, 0, 1500, ['#2f6ea8', '#173c63']))
    for i in range(14):
        y = 1020 + i * 34; off = math.sin(t * 2 + i) * 30
        c.drawLine(80 + off + (i * 73) % 300, y, 300 + off + (i * 73) % 300, y, P('#ffffff', 60, stroke=4))
    c.save(); c.translate(0, math.sin(t * 1.6) * 8); c.rotate(math.sin(t * 1.2) * 1.2, 560, 1050)
    hull = skia.Path(); hull.moveTo(160, 980); hull.lineTo(1010, 980); hull.lineTo(930, 1090); hull.lineTo(260, 1090); hull.close()
    c.drawPath(hull, P('#ffffff')); c.drawLine(220, 1040, 960, 1040, P('#173c63', stroke=10))
    rr(c, 330, 900, 520, 86, 20, P('#f4f6f9')); rr(c, 380, 916, 420, 40, 12, P('#1c2a3a'))
    rr(c, 460, 840, 300, 66, 18, P('#f4f6f9')); rr(c, 500, 852, 220, 30, 10, P('#1c2a3a'))
    c.drawLine(640, 840, 640, 760, P('#c8d1db', stroke=8))
    founder(c, 880, 980, .5, 'mogul', t, la=10, ra=-150 + math.sin(t * 5) * 10)
    partner(c, 980, 980, .48, t, 'gown', ra=-150 + math.sin(t * 5 + 1) * 10)
    c.restore()


def jet(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1100, ['#0f2747', '#3c5e8c', '#f3a26b']))
    c.drawRect(skia.Rect.MakeXYWH(0, 1100, W, H - 1100), P('#3b4048'))
    for i in range(8): rr(c, i * 150 - (t * 120) % 150, 1250, 90, 14, 7, P('#f1f3f5', 200))
    for i in range(10): c.drawCircle(i * 120 + 30, 1110, 6, P('#ffd43b', 160 + 90 * math.sin(t * 4 + i)))
    k = ease(t / 1.2); dx = (1 - k) * 500
    c.save(); c.translate(dx, 0)
    c.drawOval(skia.Rect.MakeXYWH(120, 1110, 860, 40), P('#000000', 60, blur=14))
    body = skia.Path(); body.moveTo(110, 960); body.quadTo(160, 880, 300, 880); body.lineTo(860, 880); body.quadTo(980, 890, 1010, 940)
    body.lineTo(1000, 980); body.quadTo(900, 1020, 300, 1020); body.quadTo(150, 1020, 110, 960); body.close(); c.drawPath(body, P('#f5f7fa'))
    c.drawLine(180, 990, 950, 990, P(SGOLD, stroke=10))
    for i in range(7): rr(c, 360 + i * 70, 912, 36, 30, 12, P('#1c2a3a'))
    tl = skia.Path(); tl.moveTo(860, 880); tl.lineTo(940, 720); tl.lineTo(1000, 720); tl.lineTo(960, 900); tl.close(); c.drawPath(tl, P('#e7ebf0'))
    wg = skia.Path(); wg.moveTo(480, 1000); wg.lineTo(700, 1000); wg.lineTo(560, 1080); wg.lineTo(460, 1080); wg.close(); c.drawPath(wg, P('#d9dee5'))
    rr(c, 690, 940, 120, 46, 20, P('#cfd5dc'))
    for gx in (300, 760): c.drawLine(gx, 1020, gx, 1100, P('#555b63', stroke=10)); c.drawCircle(gx, 1104, 18, P('#14181d'))
    # stairs
    st = skia.Path(); st.moveTo(220, 1010); st.lineTo(120, 1140); st.lineTo(170, 1140); st.lineTo(260, 1010); st.close(); c.drawPath(st, P('#c4cad1'))
    c.restore()
    founder(c, 560, 1236, .9, 'mogul', t, la=10, ra=-150 + math.sin(t * 5) * 12)


def wedding(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1150, ['#fde2e4', '#fff1e6']))
    c.drawRect(skia.Rect.MakeXYWH(0, 1150, W, H - 1150), grad(0, 1150, 0, 1600, ['#a8d5ba', '#7fbf99']))
    rr(c, 300, 1130, 480, 340, 0, P('#ffffff', 160))  # aisle
    # floral arch
    arc = skia.Path(); arc.moveTo(170, 1150); arc.lineTo(170, 760); arc.cubicTo(170, 470, 910, 470, 910, 760); arc.lineTo(910, 1150)
    c.drawPath(arc, P('#f2e6d0', stroke=26))
    for i in range(26):
        u = i / 25
        if u < .3: x, y = 170, 1150 - u / .3 * 390
        elif u < .7: a = math.pi * (1 - (u - .3) / .4); x, y = 540 + math.cos(a) * 370, 760 - math.sin(a) * 250
        else: x, y = 910, 760 + (u - .7) / .3 * 390
        col = ['#f783ac', '#ffffff', '#fcc2d7', '#ffd8a8'][i % 4]
        c.drawCircle(x, y, 30, P(col)); c.drawCircle(x, y, 10, P(SGOLD))
        if i % 3 == 0: c.drawCircle(x + 26, y + 18, 18, P('#69b385'))
    founder(c, 400, 1236, .95, 'groom', t, la=10, ra=-30, mood='happy')
    partner(c, 690, 1236, .95, t, 'wedding', la=30, ra=-10)
    # rings
    k = pop(clamp((t - .4) / .5))
    if k > 0:
        c.save(); c.translate(545, 540); c.scale(k, k)
        c.drawCircle(-26, 0, 40, P(SGOLD, stroke=14)); c.drawCircle(26, 0, 40, P(SGOLD, stroke=14)); sparkle(c, 30, -44, 22, 255, '#ffffff'); c.restore()
    for i in range(30):  # confetti
        kk = (t * .35 + i * .071) % 1; x = (i * 137 + 51) % 1040 + 20 + math.sin(t * 2 + i) * 20; y = 460 + kk * 720
        c.save(); c.rotate(t * 200 + i * 40, x, y); rr(c, x - 8, y - 5, 16, 10, 2, P(['#f783ac', SGOLD, '#74c0fc', '#8ce99a'][i % 4], 230)); c.restore()


def cta(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, W, H, [BG, '#0d3d33']))
    c.drawCircle(540, 620, 520, P(GREEN, 40, blur=120))
    for i in range(14):  # rising gold sparks
        kk = (t * .4 + i * .07) % 1; x = (i * 173 + 60) % 1000 + 40
        c.drawCircle(x, 1600 - kk * 1200, 6, P(SGOLD, 200 * (1 - kk)))
    k = pop(t / .5)
    c.save(); c.translate(540, 560); c.scale(k, k); emblem(c, -130, -130, 260); c.restore()
    a = 255 * ease((t - .2) / .4)
    text(c, 'Startup Legacy', 540, 830, 112, '#ffffff', 900, 'c', a=a)
    text(c, 'Start broke. Build an empire.', 540, 912, 52, '#bfe9da', 700, 'c', a=a)
    b = pop((t - .6) / .5) * (1 + .03 * math.sin(t * 6))
    if t > .6:
        c.save(); c.translate(540, 1080); c.scale(b, b)
        rr(c, -340, -56, 680, 132, 66, P('#000000', 80, blur=20)); rr(c, -340, -66, 680, 132, 66, P('#ffffff'))
        apple(c, -250, 0, 56)
        text(c, 'Free on the', -196, -6, 34, '#5b6472', 800); text(c, 'App Store', -196, 44, 58, BG, 900); c.restore()
    text(c, 'Business career simulator for iPhone', 540, 1240, 40, '#ffffff', 700, 'c', a=255 * ease((t - .9) / .4))


def apple(c, x, y, s):
    """Simple generic download arrow badge (no third-party logos)."""
    c.drawCircle(x, y, s * .62, P(GREEN))
    c.drawLine(x, y - s * .3, x, y + s * .22, P('#ffffff', stroke=s * .14))
    ar = skia.Path(); ar.moveTo(x - s * .26, y); ar.lineTo(x, y + s * .28); ar.lineTo(x + s * .26, y); c.drawPath(ar, P('#ffffff', stroke=s * .14))


SCENES = {'broke': broke_room, 'garage': garage, 'office': office, 'trading': trading, 'mansion': mansion,
          'cars': garage_cars, 'watch': watch, 'yacht': yacht, 'jet': jet, 'wedding': wedding, 'cta': cta}
