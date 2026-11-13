"""Helpers shared by the variant scripts in this folder (each variant = one new ad)."""
import sys, os, math
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
import skia
from lib import *
import scenes


def cta2(l1, l2, button='Play free'):
    """End card like scenes.cta, with its own two lines."""
    def f(c, t):
        c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, W, H, [NAVY, '#0e4b55']))
        c.drawCircle(540, 620, 520, P(TEAL, 34, blur=120))
        scenes._ecg(c, 0, W, 1440, t, TEAL, a=90, amp=60, w=6)
        k = pop(t / .5)
        c.save(); c.translate(540, 560); c.scale(k, k); logo(c, -110, -110, 220); c.restore()
        a = 255 * ease((t - .2) / .4)
        text(c, 'Bedside Bay', 540, 810, 118, '#ffffff', 900, 'c', a=a)
        text(c, l1, 540, 900, 54, '#bfe9e4', 700, 'c', a=a)
        text(c, l2, 540, 966, 54, '#bfe9e4', 700, 'c', a=a)
        b = pop((t - .6) / .5) * (1 + .03 * math.sin(t * 6))
        if t > .6:
            c.save(); c.translate(540, 1110); c.scale(b, b)
            rr(c, -290, -62 + 10, 580, 132, 66, P('#000000', 80, blur=20)); rr(c, -290, -66, 580, 132, 66, P(TEAL))
            text(c, button, 0, 22, 66, '#ffffff', 900, 'c'); c.restore()
        text(c, 'bedsidebay.com', 540, 1260, 56, '#ffffff', 800, 'c', a=255 * ease((t - .9) / .4))
    return f


def pill(c, cx, cy, label, bgc=GOLD, fg=INK, size=36, k=1.0):
    """Centred rounded label. k = pop scale."""
    w = tw(label, size, 900) + 60; h = size + 32
    c.save(); c.translate(cx, cy); c.scale(k, k)
    rr(c, -w / 2, -h / 2 + 4, w, h, h / 2, P('#000000', 70, blur=12)); rr(c, -w / 2, -h / 2, w, h, h / 2, P(bgc))
    text(c, label, 0, size * .36, size, fg, 900, 'c'); c.restore()


def swipe(c, x=640, y=1516):
    rr(c, x, y, 300, 76, 38, P(GOLD)); text(c, 'Swipe  >', x + 150, y + 52, 40, INK, 900, 'c')


def flash(c, t, d=.28):
    if t < d: c.drawRect(skia.Rect.MakeWH(W, H), P('#ffffff', 200 * (1 - t / d)))


def frame(fn, t):
    s = new_surface(); fn(s.getCanvas(), t); return s


def save_slides(fns, prefix):
    """fns: list of draw(canvas). Writes <prefix>-<n>.jpg (1080x1920) and returns the surfaces."""
    os.makedirs(os.path.dirname(prefix) or '.', exist_ok=True); out = []
    for i, fn in enumerate(fns):
        s = new_surface(); fn(s.getCanvas()); save_jpg(s, f'{prefix}-{i + 1}.jpg'); out.append(s)
    return out


def fit(s, size, maxw=980, wt=900):
    """Largest size <= size at which s fits maxw."""
    while tw(s, size, wt) > maxw and size > 30: size -= 2
    return size


def title2(c, top, sub, y=356, col='#ffffff', top_col=GOLD, a=255, dy=0, shadow=.35, size=96, sub_size=76):
    """Two-line headline: a coloured lead line and a plain second line (each shrinks to fit)."""
    s1 = fit(top, size); text(c, top, W / 2, y + dy, s1, top_col, 900, 'c', a=a, shadow=shadow)
    s2 = fit(sub, sub_size); text(c, sub, W / 2, y + dy + 98, s2, col, 900, 'c', a=a, shadow=shadow)
