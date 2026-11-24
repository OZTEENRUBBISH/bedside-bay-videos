"""Case photo set 06 — "What's wrong with <first name>?" Modelled on the best Case performer ("Would you catch this?",
case_photos_02): the patient's words in a big speech bubble on slide 1, then the chart with the diagnosis row locked,
the A-D "What do you do first?" choice, the one-call box and the end card. New hook, new bubble layout, new chart
headline. Never reveals the diagnosis.
Usage: python3 case_photos_06_whats_wrong.py <case-id> <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-5.jpg"""
from common import *
import case, case_02
from case import bg, card, chip, TRI, RED


def p_hook(K):
    first = K['name'].split()[0]
    def f(c, t=1.2):
        bg(c, t); brand_bar(c)
        title2(c, 'What’s wrong', f'with {first}?', 366, size=112, sub_size=112)
        q = '“' + K['quote'] + '”'; size = 92; lines = wrap(q, size, 900, 840)
        while len(lines) > 4: size -= 4; lines = wrap(q, size, 900, 840)
        bh = len(lines) * size * 1.16 + 110; by = 570
        card(c, 60, by, 960, bh, 56)
        tri = skia.Path(); tri.moveTo(190, by + bh - 4); tri.lineTo(170, by + bh + 70); tri.lineTo(290, by + bh - 4); tri.close(); c.drawPath(tri, P('#ffffff'))
        for i, ln in enumerate(lines): text(c, ln, 120, by + 60 + size * .8 + i * size * 1.16, size, INK, 900)
        fy = by + bh + 200
        c.drawCircle(200, fy, 190, P(TEAL, 70, blur=70))
        face(c, 200, fy, 130, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, f"{K['name']}, {K['age']}", 364, fy - 10, 58, '#ffffff', 900, shadow=.35)
        lab = f"JUST ARRIVED  ·  TRIAGE {K['triage']}"; w = tw(lab, 30, 900) + 48
        rr(c, 364, fy + 18, w, 58, 29, P(TRI[K['triage']])); text(c, lab, 364 + w / 2, fy + 58, 30, INK if K['triage'] == 3 else '#ffffff', 900, 'c')
        pill(c, 300, 1554, "You're the doctor.", '#ffffff', INK, 38)
        swipe(c, 640, 1516)
    return f


def p_chart(K):
    first = K['name'].split()[0]
    def f(c, t=2.0):
        bg(c, t); brand_bar(c)
        title2(c, f'{first}’s chart.', 'One line is locked.', 366, size=104, sub_size=76)
        card(c, 90, 540, 900, 930, 44)
        rr(c, 400, 508, 280, 76, 24, P('#5b7083')); rr(c, 470, 490, 140, 44, 16, P('#8a9bab'))  # clipboard clip
        rows = [('NAME', K['name']), ('AGE', K['age']), ('PROBLEM', K['problem']), ('DIFFICULTY', K['level']), ('TRIAGE', None), ('DIAGNOSIS', None)]
        for i, (lab, val) in enumerate(rows):
            y = 612 + i * 140
            if i: c.drawLine(140, y - 6, 940, y - 6, P('#e4eaf0', stroke=3))
            text(c, lab, 140, y + 44, 28, '#5b7083', 800)
            if val: text(c, val, 140, y + 106, 56, INK, 900)
            elif lab == 'TRIAGE':
                c.drawCircle(176, y + 88, 36, P(TRI[K['triage']])); text(c, str(K['triage']), 176, y + 105, 48, INK if K['triage'] == 3 else '#ffffff', 900, 'c')
                text(c, 'of 5', 230, y + 106, 44, '#5b7083', 800)
            else:
                rr(c, 140, y + 54, 800, 76, 20, P(INK))
                rr(c, 168, y + 88, 34, 28, 6, P(GOLD)); c.drawArc(skia.Rect.MakeXYWH(173, y + 68, 24, 30), 180, 180, False, P(GOLD, stroke=6))  # padlock
                text(c, 'Locked. You find it.', 226, y + 107, 40, '#ffffff', 900)
        swipe(c, 640, 1516)
    return f


def slides(case_id):
    K, SC = case.build(case_id)
    return K, [lambda c: p_hook(K)(c), lambda c: p_chart(K)(c), lambda c: case_02.q_choice(K)(c, 1.69),
               lambda c: SC[2][0](c, 3.4), lambda c: SC[3][0](c, 2.8)]


if __name__ == '__main__':
    K, fns = slides(sys.argv[1]); fr = save_slides(fns, sys.argv[2])
    if len(sys.argv) > 3: contact_sheet(fr, sys.argv[3], 5)
