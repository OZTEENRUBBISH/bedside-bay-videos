"""Broke to Rich photo set 04 — "One doctor. Five ranks." A staircase hook, then one slide per rank (numbered 1-5), the last
one carrying the Play free button. Bank amounts after the $2,000 start are illustrative.
Usage: python3 b2r_ranks_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
from case import bg, chip
from fullgame_02 import OUT, BANK
from b2r_variants import chips


def p_hook(c, t=1.0):
    bg(c, t); brand_bar(c)
    headline(c, ['One doctor.', 'Five ranks.'], 372, 100)
    for i in range(5):
        x = 60 + i * 192; top = 1270 - i * 92
        c.drawRect(skia.Rect.MakeXYWH(x, top, 192, 1400 - top), grad(0, top, 0, 1400, [GOLD, '#c98a1b'] if i == 4 else ['#1cb5a3', '#0e6f68']))
        c.drawRect(skia.Rect.MakeXYWH(x, top, 192, 12), P('#ffffff', 90))
        text(c, str(i + 1), x + 96, top + 84, 64, INK if i == 4 else '#ffffff', 900, 'c')
        if i == 4: c.drawCircle(x + 96, top - 150, 150, P(GOLD, 80, blur=60))
        doctor(c, x + 96, top, .46, OUT[i], t + i, la=10, ra=-150 if i == 4 else -12, mood='tired' if i == 0 else 'happy')
    c.drawRect(skia.Rect.MakeXYWH(60, 1400, 960, 8), P('#ffffff', 60))
    for i in range(5): text(c, RANKS[i], 60 + i * 192 + 96, 1446, 27, GOLD if i == 4 else '#ffffff', 800, 'c')
    pill(c, 300, 1554, 'Starts with $2,000', '#ffffff', INK, 36)
    swipe(c, 640, 1516)


def _consult(c, t):
    bg(c, t)
    c.drawCircle(540, 900, 320, P(TEAL, 80, blur=100))
    for j in range(6):
        a = j * math.pi / 3 + .4; sparkle(c, 540 + math.cos(a) * 330, 900 + math.sin(a) * 300, 24, 200, GOLD)
    doctor(c, 540, 1236, 1.0, 'consultant', t, la=10, ra=-12, mood='happy')


def rank(i, fn, sub, col='#ffffff', top_col=GOLD, last=False):
    def f(c):
        fn(c)
        title2(c, f'{i + 1}. {RANKS[i]}', sub, 356, col, top_col, shadow=0 if col == INK else .35)
        if last: chips(c)
        hud(c, i, BANK[i], i + 1); brand_bar(c)
        c.drawCircle(960, 190, 50, P(GOLD)); text(c, f'{i + 1}/5', 960, 205, 38, INK, 900, 'c')
        if last:
            rr(c, 150, 1526, 780, 96, 48, P('#000000', 80, blur=16)); rr(c, 150, 1516, 780, 96, 48, P(TEAL))
            text(c, 'Play free  ·  bedsidebay.com', 540, 1580, 46, '#ffffff', 900, 'c')
    return f


def slides():
    return [lambda c: p_hook(c),
            rank(0, lambda c: scenes.poor(c, 1.8), '$2,000 to your name.'),
            rank(1, lambda c: scenes.er(c, 2.2, 'resident'), 'Cases start paying.', INK, TEAL_D),
            rank(2, lambda c: scenes.theatre(c, 2.3), 'The big surgeries.'),
            rank(3, lambda c: _consult(c, 1.4), 'You call the shots.'),
            rank(4, lambda c: scenes.rich(c, 2.6, car_in=False), 'You made it.', last=True)]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
