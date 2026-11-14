"""Case photo set 02 — "Would you catch this?" The patient's words in a speech bubble, then the chart with the diagnosis
row locked, the A-D "What do you do first?" choice, the one-call box and the end card. Never reveals the diagnosis.
Usage: python3 case_photos_02.py <case-id> <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-5.jpg"""
from common import *
import case, case_02
from case import bg, card, chip, TRI, RED


def p_hook(K):
    def f(c, t=1.2):
        bg(c, t); brand_bar(c)
        headline(c, ['Would you', 'catch this?'], 372, 104)
        c.drawCircle(290, 800, 230, P(TEAL, 70, blur=80))
        face(c, 290, 800, 180, K['skin'], K['hair'], K['style'], 'pain', t)
        lab = f"TRIAGE {K['triage']}"; w = tw(lab, 44, 900) + 64
        rr(c, 530, 700, w, 84, 42, P(TRI[K['triage']])); text(c, lab, 530 + w / 2, 758, 44, '#ffffff', 900, 'c')
        text(c, f"{K['name']}, {K['age']}", 530, 866, 54, '#ffffff', 900, shadow=.35)
        text(c, 'Just arrived.', 530, 926, 40, '#bfe9e4', 700)
        q = '“' + K['quote'] + '”'; size = 66; lines = wrap(q, size, 900, 860)
        if len(lines) > 3: size = 54; lines = wrap(q, size, 900, 860)
        h = len(lines) * size * 1.18 + 90; y = 1050
        tri = skia.Path(); tri.moveTo(250, y + 6); tri.lineTo(300, y - 56); tri.lineTo(350, y + 6); tri.close(); c.drawPath(tri, P('#ffffff'))
        card(c, 60, y, 960, h, 44)
        for i, ln in enumerate(lines): text(c, ln, 540, y + 50 + size * .8 + i * size * 1.18, size, INK, 900, 'c')
        pill(c, 300, 1554, "You're the doctor.", '#ffffff', INK, 38)
        swipe(c, 640, 1516)
    return f


def p_chart(K):
    def f(c, t=2.0):
        bg(c, t); brand_bar(c)
        headline(c, ['Read the chart.'], 400, 100)
        card(c, 90, 520, 900, 950, 44)
        rr(c, 400, 488, 280, 76, 24, P('#5b7083')); rr(c, 470, 470, 140, 44, 16, P('#8a9bab'))  # clipboard clip
        rows = [('NAME', K['name']), ('AGE', K['age']), ('PROBLEM', K['problem']), ('DIFFICULTY', K['level']), ('TRIAGE', None), ('DIAGNOSIS', None)]
        for i, (lab, val) in enumerate(rows):
            y = 600 + i * 142
            if i: c.drawLine(140, y - 6, 940, y - 6, P('#e4eaf0', stroke=3))
            text(c, lab, 140, y + 44, 28, '#5b7083', 800)
            if val: text(c, val, 140, y + 106, 56, INK, 900)
            elif lab == 'TRIAGE':
                c.drawCircle(176, y + 88, 36, P(TRI[K['triage']])); text(c, str(K['triage']), 176, y + 105, 48, '#ffffff', 900, 'c')
                text(c, 'of 5', 230, y + 106, 44, '#5b7083', 800)
            else:
                rr(c, 140, y + 58, 800, 76, 20, P(INK))
                rr(c, 168, y + 92, 34, 28, 6, P(GOLD)); c.drawArc(skia.Rect.MakeXYWH(173, y + 72, 24, 30), 180, 180, False, P(GOLD, stroke=6))  # padlock
                text(c, "Hidden. That's your job.", 226, y + 111, 40, '#ffffff', 900)
        swipe(c, 640, 1516)
    return f


def slides(case_id):
    K, SC = case.build(case_id)
    return K, [lambda c: p_hook(K)(c), lambda c: p_chart(K)(c), lambda c: case_02.q_choice(K)(c, 1.69),
               lambda c: SC[2][0](c, 3.4), lambda c: SC[3][0](c, 2.8)]


if __name__ == '__main__':
    K, fns = slides(sys.argv[1]); fr = save_slides(fns, sys.argv[2])
    if len(sys.argv) > 3: contact_sheet(fr, sys.argv[3], 5)
