"""Case photo set 07 — "3 clues. 1 patient." Quote first: the patient's own words are CLUE 1 on a big numbered clue
card (playing-card look: corner numbers, gold tag, the other clue cards still face down behind it). Slide 2 turns over
CLUE 2 (who the patient is), slide 3 CLUE 3 (triage and difficulty), slide 4 is the fourth card, face down and locked
("The answer? That's your job.") with Dr John Smith and the four moves, slide 5 the end card.
Everything on the cards is copied from cases.json. Never reveals or hints at the diagnosis.
Usage: python3 case_photos_07_clues.py <case-id> <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-5.jpg"""
from common import *
import case
from case import bg, TRI

GREY = '#5b7083'
BACK = '#123a5a'


def card_back(c, cx, cy, w, h, ang, label):
    """A face-down clue card: navy back, teal diamond pattern, gold number."""
    c.save(); c.translate(cx, cy); c.rotate(ang)
    rr(c, -w / 2, -h / 2 + 10, w, h, 36, P('#000000', 90, blur=22))
    rr(c, -w / 2, -h / 2, w, h, 36, P('#ffffff')); rr(c, -w / 2 + 14, -h / 2 + 14, w - 28, h - 28, 26, P(BACK))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 14, -h / 2 + 14, w - 28, h - 28), 26, 26), True)
    n = int(max(w, h) / 44) + 2
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = i * 44 + (22 if j % 2 else 0), j * 44
            d = skia.Path(); d.moveTo(x, y - 13); d.lineTo(x + 13, y); d.lineTo(x, y + 13); d.lineTo(x - 13, y); d.close()
            c.drawPath(d, P(TEAL, 46))
    c.restore()
    r = min(w, h) * .26
    c.drawCircle(0, 0, r + 8, P(BACK)); c.drawCircle(0, 0, r, P(GOLD)); text(c, label, 0, r * .42, r * 1.2, INK, 900, 'c')
    c.restore()


def clue_card(c, x, y, w, h, n, tag, ang=-1.6):
    """A face-up clue card. Leaves the canvas rotated about the card centre: caller draws content, then c.restore()."""
    c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(ang); c.translate(-(x + w / 2), -(y + h / 2))
    rr(c, x, y + 14, w, h, 46, P('#000000', 100, blur=28)); rr(c, x, y, w, h, 46, P('#ffffff'))
    rr(c, x + 16, y + 16, w - 32, h - 32, 32, P(TEAL, stroke=5))
    # corner numbers, playing-card style
    c.drawCircle(x + 92, y + 96, 52, P(INK)); text(c, str(n), x + 92, y + 124, 78, GOLD, 900, 'c')
    c.save(); c.rotate(180, x + w - 92, y + h - 96)
    c.drawCircle(x + w - 92, y + h - 96, 52, P(INK)); text(c, str(n), x + w - 92, y + h - 68, 78, GOLD, 900, 'c'); c.restore()
    # gold tag
    lab = f'CLUE {n}'; lw = tw(lab, 44, 900) + 56
    rr(c, x + 168, y + 60, lw, 72, 36, P(GOLD)); text(c, lab, x + 168 + lw / 2, y + 112, 44, INK, 900, 'c')
    text(c, tag, x + 168 + lw + 22, y + 108, 30, GREY, 800)


def dots(c, n, y=1556, x=96):
    """Progress: three small cards, turned over up to n."""
    for i in range(3):
        cx = x + i * 92
        if i < n:
            rr(c, cx - 36, y - 48, 72, 96, 14, P('#ffffff')); text(c, str(i + 1), cx, y + 20, 56, INK, 900, 'c')
        else:
            rr(c, cx - 36, y - 48, 72, 96, 14, P('#ffffff', 70)); rr(c, cx - 30, y - 42, 60, 84, 10, P(BACK)); text(c, '?', cx, y + 18, 50, GOLD, 900, 'c')
    text(c, f'{n} of 3 clues', x + 250, y + 16, 40, '#ffffff', 800, shadow=.35)


def p_hook(K):
    def f(c, t=1.2):
        bg(c, t); brand_bar(c)
        title2(c, '3 clues.', '1 patient.', 380, size=132, sub_size=112, top_col=GOLD)
        card_back(c, 800, 900, 400, 560, 11, '3'); card_back(c, 700, 830, 400, 560, 5, '2')
        x, y, w, h = 60, 560, 820, 860
        clue_card(c, x, y, w, h, 1, 'WHAT THE PATIENT SAID')
        q = '“' + K['quote'] + '”'; size = 84; lines = wrap(q, size, 900, w - 130)
        while len(lines) > 5: size -= 4; lines = wrap(q, size, 900, w - 130)
        y0 = y + 190 + size * .8 + (5 - len(lines)) * size * .3
        for i, ln in enumerate(lines): text(c, ln, x + 66, y0 + i * size * 1.14, size, INK, 900)
        fy = y + h - 150
        face(c, x + 170, fy, 98, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, 'Who is the patient?', x + 296, fy - 2, 40, INK, 900)
        text(c, 'Clue 2 is next.', x + 296, fy + 50, 36, TEAL_D, 800)
        c.restore()
        dots(c, 1); swipe(c, 640, 1516)
    return f


def p_who(K):
    def f(c, t=2.0):
        bg(c, t); brand_bar(c)
        title2(c, 'Clue 2.', 'Who the patient is.', 380, size=132, sub_size=84)
        card_back(c, 800, 900, 400, 560, 9, '3')
        x, y, w, h = 60, 560, 820, 860
        clue_card(c, x, y, w, h, 2, 'THE PATIENT', ang=1.4)
        c.drawCircle(x + w / 2, y + 318, 162, P(TEAL, 60, blur=30))
        face(c, x + w / 2, y + 318, 140, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, K['name'], x + w / 2, y + 556, fit(K['name'], 92, w - 140), INK, 900, 'c')
        text(c, f"Age {K['age']}", x + w / 2, y + 626, 56, GREY, 800, 'c')
        text(c, 'PROBLEM', x + w / 2, y + 690, 28, GREY, 800, 'c')
        ps = fit(K['problem'], 60, w - 360); pw = tw(K['problem'], ps, 900) + 80
        rr(c, x + w / 2 - pw / 2, y + 706, pw, 96, 48, P('#e2f4f1')); text(c, K['problem'], x + w / 2, y + 754 + ps * .34, ps, TEAL_D, 900, 'c')
        c.restore()
        dots(c, 2); swipe(c, 640, 1516)
    return f


def p_urgent(K):
    def f(c, t=2.6):
        bg(c, t); brand_bar(c)
        title2(c, 'Clue 3.', 'How urgent. How hard.', 380, size=132, sub_size=84)
        x, y, w, h = 110, 560, 820, 860
        clue_card(c, x, y, w, h, 3, 'TRIAGE AND LEVEL', ang=-1.2)
        col = TRI[K['triage']]; fg = INK if K['triage'] == 3 else '#ffffff'
        text(c, 'TRIAGE', x + 80, y + 250, 34, GREY, 800)
        c.drawCircle(x + 210, y + 400, 128, P(col, 70, blur=24)); c.drawCircle(x + 210, y + 400, 116, P(col))
        text(c, str(K['triage']), x + 210, y + 462, 176, fg, 900, 'c')
        text(c, f"Triage {K['triage']}", x + 366, y + 396, 76, INK, 900)
        for i in range(5):  # the game's Triage 1-5 scale as five pips
            on = i + 1 == K['triage']
            c.drawCircle(x + 390 + i * 70, y + 462, 26, P(TRI[i + 1], 255 if on else 70))
            text(c, str(i + 1), x + 390 + i * 70, y + 475, 34, ('#ffffff' if on else INK), 900, 'c', a=255 if on else 150)
        c.drawLine(x + 70, y + 570, x + w - 70, y + 570, P('#e4eaf0', stroke=4))
        text(c, 'DIFFICULTY', x + 80, y + 640, 34, GREY, 800)
        text(c, K['level'], x + 80, y + 750, 104, INK, 900)
        c.restore()
        dots(c, 3); swipe(c, 640, 1516)
    return f


MOVES = [('talk', 'Talk'), ('examine', 'Examine'), ('tests', 'Tests'), ('treat', 'Treat')]


def p_answer(K):
    def f(c, t=1.0):
        bg(c, t); brand_bar(c)
        title2(c, 'The answer?', 'That’s your job.', 380, size=120, sub_size=96)
        # the fourth card: face down, locked
        x, y, w, h = 60, 550, 900, 330
        c.save(); c.rotate(-1.2, x + w / 2, y + h / 2)
        rr(c, x, y + 14, w, h, 46, P('#000000', 100, blur=28)); rr(c, x, y, w, h, 46, P('#ffffff')); rr(c, x + 14, y + 14, w - 28, h - 28, 34, P(BACK))
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 14, y + 14, w - 28, h - 28), 34, 34), True)
        for i in range(24):
            for j in range(9):
                px, py = x + i * 44 + (22 if j % 2 else 0), y + j * 44
                d = skia.Path(); d.moveTo(px, py - 13); d.lineTo(px + 13, py); d.lineTo(px, py + 13); d.lineTo(px - 13, py); d.close(); c.drawPath(d, P(TEAL, 34))
        c.restore()
        text(c, 'DIAGNOSIS', x + 70, y + 98, 40, '#bfe9e4', 900)
        text(c, '?  ?  ?', x + 70, y + 250, 170, GOLD, 900)
        lx, ly = x + w - 170, y + 170  # padlock
        c.drawArc(skia.Rect.MakeXYWH(lx - 44, ly - 96, 88, 110), 180, 180, False, P(GOLD, stroke=18))
        rr(c, lx - 70, ly - 40, 140, 116, 22, P(GOLD)); c.drawCircle(lx, ly + 8, 16, P(INK)); rr(c, lx - 6, ly + 10, 12, 34, 4, P(INK))
        c.restore()
        text(c, 'Four moves to find it:', 60, 990, 46, '#ffffff', 900, shadow=.35)
        for i, (ic, lab) in enumerate(MOVES):
            ty = 1020 + i * 116
            rr(c, 60, ty + 8, 500, 100, 30, P('#000000', 80, blur=16)); rr(c, 60, ty, 500, 100, 30, P('#ffffff'))
            c.drawCircle(120, ty + 50, 36, P(TEAL)); icon(c, ic, 120, ty + 50, 44, '#ffffff')
            text(c, lab, 180, ty + 70, 56, INK, 900)
            text(c, str(i + 1), 520, ty + 68, 44, '#c3cfd9', 900, 'c')
        c.drawCircle(770, 1250, 250, P(TEAL, 50, blur=80))
        doctor(c, 770, 1500, .86, 'resident', t, la=10, ra=-14, mood='happy')
        pill(c, 770, 1556, 'Dr John Smith', '#ffffff', INK, 34)
        swipe(c, 60, 1516)
    return f


def slides(case_id):
    K = [k for k in case.json.load(open(os.path.join(KIT, 'cases.json'))) if k['id'] == case_id][0]
    first = K['name'].split()[0]
    end = cta2(f'{first} is waiting.', 'Take the case.')
    return K, [lambda c: p_hook(K)(c), lambda c: p_who(K)(c), lambda c: p_urgent(K)(c), lambda c: p_answer(K)(c), lambda c: end(c, 3.0)]


if __name__ == '__main__':
    K, fns = slides(sys.argv[1]); fr = save_slides(fns, sys.argv[2])
    if len(sys.argv) > 3: contact_sheet(fr, sys.argv[3], 5)
