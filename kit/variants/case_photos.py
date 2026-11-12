"""Case photo set — one patient as a 5-slide cliffhanger (never reveals the diagnosis).
Usage: python3 case_photos.py <case-id> <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-5.jpg"""
from common import *
import case
from case import bg, card, chip, TRI


def p_hook(K):
    def f(c, t=1.2):
        bg(c, t); brand_bar(c)
        lab = f"INCOMING  ·  TRIAGE {K['triage']}"; w = tw(lab, 34) + 96
        rr(c, (W - w) / 2, 300, w, 70, 35, P(TRI[K['triage']])); c.drawCircle((W - w) / 2 + 40, 335, 12, P('#ffffff'))
        text(c, lab, (W - w) / 2 + 66, 347, 34, '#ffffff', 900)
        c.drawCircle(540, 640, 250, P(TEAL, 70, blur=80))
        face(c, 540, 640, 200, K['skin'], K['hair'], K['style'], 'pain', t)
        lines = wrap('“' + K['quote'] + '”', 74, 900, 940)
        size = 74 if len(lines) <= 3 else 60
        if size == 60: lines = wrap('“' + K['quote'] + '”', 60, 900, 940)
        y = 980
        for i, ln in enumerate(lines): text(c, ln, 540, y + i * size * 1.15, size, '#ffffff', 900, 'c', shadow=.35)
        y += len(lines) * size * 1.15 + 10
        text(c, f"{K['name']}, {K['age']}", 540, y, 50, '#bfe9e4', 800, 'c')
        pill(c, 300, 1480, "You're the doctor.", '#ffffff', INK, 38)
        swipe(c, 640, 1442)
    return f


def slides(case_id):
    K, SC = case.build(case_id)
    return K, [lambda c: p_hook(K)(c), lambda c: SC[0][0](c, 3.4), lambda c: SC[1][0](c, 3.0), lambda c: SC[2][0](c, 3.4), lambda c: SC[3][0](c, 2.8)]


if __name__ == '__main__':
    K, fns = slides(sys.argv[1]); fr = save_slides(fns, sys.argv[2])
    if len(sys.argv) > 3: contact_sheet(fr, sys.argv[3], 5)
