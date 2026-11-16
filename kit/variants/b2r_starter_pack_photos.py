"""Broke to Rich photo set 07 — "Broke intern starter pack" vs "ED Director starter pack" (meme-style 2x2 item grids cut
from the career scenes), then the three ranks in between, how you climb, and the Play free card. The mansion, car and watch
are illustrative.
Usage: python3 b2r_starter_pack_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-5.jpg"""
from common import *
from case import bg, chip
from fullgame_02 import OUT, BANK
from b2r_07_versus import view

N = 5


def _rrpath(x, y, w, h, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)); return p


def tile(c, x, y, w, h, label, draw):
    """Rounded picture tile with a white caption band. draw(c, clip, sx, sy) paints the picture area."""
    rr(c, x, y + 12, w, h, 40, P('#000000', 100, blur=24))
    clip = _rrpath(x, y, w, h, 40)
    c.save(); c.clipPath(clip, doAntiAlias=True)
    draw(c, clip, x + w / 2, y + (h - 96) / 2)
    c.drawRect(skia.Rect.MakeXYWH(x, y + h - 96, w, 96), P('#ffffff')); c.restore()
    text(c, label, x + w / 2, y + h - 32, fit(label, 42, w - 40), INK, 900, 'c')
    c.drawPath(clip, P('#ffffff', stroke=8))


def crop(kind, cx, cy, zoom, t=1.8):
    return lambda c, clip, sx, sy: view(c, kind, t, clip, cx, cy, zoom, sx, sy)


def money(amount, col):
    def f(c, clip, sx, sy):
        c.drawPath(clip, grad(0, sy - 200, 0, sy + 200, ['#12303f', '#0d2230']))
        text(c, 'BANK', sx, sy - 56, 34, '#9fb2c2', 800, 'c'); text(c, amount, sx, sy + 56, fit(amount, 112, 400), col, 900, 'c')
    return f


def portrait(c, cx, cy, r, outfit, mood, ring):
    c.drawCircle(cx, cy + 8, r + 10, P('#000000', 90, blur=18))
    clip = skia.Path(); clip.addCircle(cx, cy, r); c.save(); c.clipPath(clip, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), P('#dff1f4'))
    s = r / 152; doctor(c, cx, cy + 524 * s, s, outfit, 0.5, la=10, ra=-10, mood=mood); c.restore()
    c.drawCircle(cx, cy, r, P(ring, stroke=12))


def count(c, i):
    c.drawCircle(960, 190, 50, P(GOLD)); text(c, f'{i}/{N}', 960, 205, 38, INK, 900, 'c')


GRID = [(60, 590), (560, 590), (60, 1010), (560, 1010)]


def pack(i, top, top_col, items, outfit, mood, ring, foot):
    def f(c):
        bg(c, 1.0); brand_bar(c); count(c, i)
        title2(c, top, 'starter pack', 356, top_col=top_col, size=110, sub_size=96)
        for (x, y), (label, draw) in zip(GRID, items): tile(c, x, y, 460, 390, label, draw)
        portrait(c, 134, 1554, 74, outfit, mood, ring)
        text(c, foot, 232, 1568, fit(foot, 40, 420), '#ffffff', 900, shadow=.35)
        swipe(c, 680, 1516)
    return f


def between(c):
    bg(c, 1.0); brand_bar(c); count(c, 3)
    title2(c, '3 ranks', 'in between.', 356, size=110, sub_size=96)
    for j, i in enumerate((1, 2, 3)):
        x = 60 + j * 330; y = 600; w, h = 300, 600
        rr(c, x, y + 12, w, h, 40, P('#000000', 100, blur=24)); clip = _rrpath(x, y, w, h, 40)
        c.save(); c.clipPath(clip, doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), grad(0, y, 0, y + h, ['#e3f2f5', '#b9dfe6']))
        c.drawCircle(x + w / 2, y + 250, 150, P('#ffffff', 120, blur=40))
        doctor(c, x + w / 2, y + h - 124, .66, OUT[i], 1.0 + j, la=10, ra=-12, mood='happy')
        c.drawRect(skia.Rect.MakeXYWH(x, y + h - 100, w, 100), P('#ffffff')); c.restore()
        text(c, RANKS[i], x + w / 2, y + h - 34, fit(RANKS[i], 46, w - 30), INK, 900, 'c')
        c.drawPath(clip, P('#ffffff', stroke=8))
        c.drawCircle(x + 56, y + 56, 36, P(TEAL)); text(c, str(i + 1), x + 56, y + 74, 46, '#ffffff', 900, 'c')
    hud(c, 2, BANK[2], 3, y=1270)
    swipe(c, 680, 1530)


MOVES = [('talk', 'Talk'), ('examine', 'Examine'), ('tests', 'Tests'), ('treat', 'Treat')]


def climb(c):
    bg(c, 1.0); brand_bar(c); count(c, 4)
    title2(c, 'Solve cases.', 'Get promoted.', 356, size=110, sub_size=96)
    for (x, y), (ic, lab) in zip([(60, 590), (560, 590), (60, 900), (560, 900)], MOVES):
        rr(c, x, y + 12, 460, 270, 40, P('#000000', 100, blur=24)); rr(c, x, y, 460, 270, 40, P('#ffffff'))
        c.drawCircle(x + 110, y + 135, 70, P(TEAL)); icon(c, ic, x + 110, y + 135, 84)
        text(c, lab, x + 206, y + 156, fit(lab, 62, 230), INK, 900)
    pill(c, 540, 1250, '163 patients are waiting', GOLD, INK, 50)
    doctor(c, 870, 1640, .5, 'resident', 1.0, la=10, ra=-150, mood='happy')
    chip(c, 60, 1400, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 30, dot=TEAL)
    swipe(c, 60, 1516)


def slides():
    broke = [('Mattress on the floor', crop('poor', 262, 1104, 1.0)), ('Instant noodles', crop('poor', 918, 1120, 2.3)),
             ('Rent overdue', crop('poor', 905, 692, 1.9)), ('$2,000 in the bank', money('$2,000', '#ff8f8f'))]
    boss = [('The mansion', crop('rich', 330, 880, .74, 2.6)), ('The supercar', crop('rich', 321, 1196, 1.0, 2.6)),
            ('The gold watch', crop('rich', 880, 790, 1.7, 2.6)), ('$2,480,000 in the bank', money('$2,480,000', GOLD))]
    return [pack(1, 'Broke intern', '#ffffff', broke, 'intern', 'tired', '#ffffff', 'Dr John Smith, Day 1'),
            pack(2, 'ED Director', GOLD, boss, 'director', 'happy', GOLD, 'Same doctor, later'),
            between, climb,
            lambda c: cta2('Pick up your starter pack.', 'It starts with $2,000.')(c, 3.0)]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 5)
