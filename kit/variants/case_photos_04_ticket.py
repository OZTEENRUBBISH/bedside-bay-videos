"""Case photo set 04 — "Now serving: number 47." The patient is called from the waiting room: a NOW SERVING display and her
paper ticket, then her own words in a speech bubble, the four moves as a strip of numbered tickets, a ticket with the
diagnosis left for you to find, and the end card. Never reveals the diagnosis.
Usage: python3 case_photos_04_ticket.py <case-id> <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-5.jpg"""
from common import *
import case
from case import bg, card, chip, TRI, RED

NUM = 47
LED = '#ffb629'


def serving(c, y, small, big, col=LED):
    """Dark waiting-room display with LED type."""
    x, w, h = 60, 960, 250
    rr(c, x, y + 12, w, h, 40, P('#000000', 110, blur=26)); rr(c, x, y, w, h, 40, P('#0b1420')); rr(c, x, y, w, h, 40, P('#5b7083', stroke=8))
    for i in range(24):
        for j in range(5): c.drawCircle(x + 40 + i * 38.3, y + 36 + j * 44.5, 3, P('#ffffff', 10))
    text(c, small, 540, y + 82, 44, '#8fa3b5', 900, 'c')
    c.drawCircle(540, y + 160, 150, P(col, 36, blur=50))
    text(c, big, 540, y + 204, fit(big, 124, 880), col, 900, 'c')


def ticket(c, cx, cy, ang, w, h, draw, col='#fff7e2'):
    """Paper take-a-number ticket with a zig-zag torn top and bottom; draw(c) fills it around (0, 0)."""
    c.save(); c.translate(cx, cy); c.rotate(ang)
    p = skia.Path(); n = int(w / 36); sw = w / n
    p.moveTo(-w / 2, -h / 2)
    for i in range(n): p.lineTo(-w / 2 + (i + .5) * sw, -h / 2 + 16); p.lineTo(-w / 2 + (i + 1) * sw, -h / 2)
    p.lineTo(w / 2, h / 2)
    for i in range(n): p.lineTo(w / 2 - (i + .5) * sw, h / 2 - 16); p.lineTo(w / 2 - (i + 1) * sw, h / 2)
    p.close()
    c.save(); c.translate(0, 14); c.drawPath(p, P('#000000', 100, blur=22)); c.restore()
    c.drawPath(p, P(col)); draw(c); c.restore()


def t_number(K):
    def f(c):
        text(c, 'EMERGENCY  ·  WAITING ROOM', 0, -150, 30, '#8a7a55', 900, 'c')
        d = P('#c9b98f', stroke=5); d.setPathEffect(skia.DashPathEffect.Make([16, 14], 0)); c.drawLine(-270, -120, 270, -120, d)
        text(c, 'YOUR NUMBER', 0, -70, 34, '#5b7083', 900, 'c')
        text(c, str(NUM), 0, 120, 230, INK, 900, 'c')
        c.drawLine(-270, 160, 270, 160, d)
        text(c, 'Please wait to be called', 0, 208, 30, '#8a7a55', 800, 'c')
    return f


def p_hook(K):
    def f(c, t=1.2):
        bg(c, t); brand_bar(c)
        serving(c, 300, 'NOW SERVING', f'NUMBER {NUM}')
        ticket(c, 300, 890, -7, 440, 520, lambda c: (c.scale(.72, .72), t_number(K)(c)))
        c.drawCircle(790, 850, 250, P(TEAL, 70, blur=80))
        face(c, 790, 850, 170, K['skin'], K['hair'], K['style'], 'pain', t)
        nm = f"{K['name']}, {K['age']}"; pill(c, 540, 1240, nm, '#ffffff', INK, fit(nm, 72, 800))
        pill(c, 540, 1356, f"{K['problem']}  ·  Triage {K['triage']}", TRI[K['triage']], '#ffffff', 46)
        text(c, 'She’s been called. You’re the doctor.', 540, 1470, 46, '#bfe9e4', 800, 'c')
        swipe(c, 640, 1516)
    return f


def p_quote(K):
    def f(c, t=2.0):
        bg(c, t); brand_bar(c)
        first = K['name'].split()[0]
        headline(c, ['You ask', 'what’s wrong.'], 372, 96)
        q = '“' + K['quote'] + '”'; size = 98; lines = wrap(q, size, 900, 840)
        while len(lines) > 5: size -= 4; lines = wrap(q, size, 900, 840)
        bh = len(lines) * size * 1.16 + 110; by = 560
        card(c, 60, by, 960, bh, 56)
        tri = skia.Path(); tri.moveTo(190, by + bh - 4); tri.lineTo(170, by + bh + 70); tri.lineTo(290, by + bh - 4); tri.close(); c.drawPath(tri, P('#ffffff'))
        for i, ln in enumerate(lines): text(c, ln, 120, by + 60 + size * .8 + i * size * 1.16, size, INK, 900)
        fy = by + bh + 190
        face(c, 190, fy, 120, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, f"{K['name']}, {K['age']}", 340, fy - 6, 56, '#ffffff', 900, shadow=.35)
        lab = f"TICKET {NUM}  ·  TRIAGE {K['triage']}"; w = tw(lab, 30, 900) + 44
        rr(c, 340, fy + 20, w, 56, 28, P(TRI[K['triage']])); text(c, lab, 340 + w / 2, fy + 59, 30, '#ffffff', 900, 'c')
        swipe(c, 640, 1516)
    return f


STUBS = [('talk', 'Talk', 'Get the story'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Make the call')]


def p_moves(K):
    def f(c, t=1.0):
        bg(c, t); brand_bar(c)
        first = K['name'].split()[0]
        title2(c, 'Four moves.', f'{first} needs all of them.', 356, size=104, sub_size=72)
        for i, (ic, lab, sub) in enumerate(STUBS):
            def d(c, i=i, ic=ic, lab=lab, sub=sub):
                rr(c, -430, -74, 170, 148, 22, P(INK)); text(c, 'MOVE', -345, -28, 26, '#8fa3b5', 900, 'c'); text(c, str(i + 1), -345, 54, 84, LED, 900, 'c')
                dd = P('#c9b98f', stroke=5); dd.setPathEffect(skia.DashPathEffect.Make([14, 12], 0)); c.drawLine(-236, -80, -236, 80, dd)
                text(c, lab, -204, 16, 76, INK, 900); text(c, sub, -202, 62, 32, '#6f6444', 800)
                c.drawCircle(350, 0, 62, P(TEAL)); icon(c, ic, 350, 0, 74)
            ticket(c, 540 + (18 if i % 2 else -18), 626 + i * 226, -1.5 if i % 2 else 1.5, 920, 200, d)
        chip(c, 60, 1440, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
        swipe(c, 640, 1516)
    return f


def p_blank(K):
    def f(c, t=1.6):
        bg(c, t); brand_bar(c)
        serving(c, 300, 'DIAGNOSIS', 'YOURS TO FIND', '#ffffff')
        def d(c):
            text(c, f'TICKET {NUM}', 0, -150, 34, '#8a7a55', 900, 'c')
            dd = P('#c9b98f', stroke=5); dd.setPathEffect(skia.DashPathEffect.Make([16, 14], 0)); c.drawLine(-250, -120, 250, -120, dd)
            text(c, K['name'], 0, -56, fit(K['name'], 56, 500), INK, 900, 'c')
            text(c, f"{K['problem']}  ·  Triage {K['triage']}", 0, -6, 30, '#6f6444', 800, 'c')
            text(c, 'DIAGNOSIS', 0, 66, 30, '#5b7083', 900, 'c')
            rr(c, -150, 86, 300, 96, 20, P(INK)); text(c, '? ? ?', 0, 156, 70, LED, 900, 'c')
        ticket(c, 320, 870, -6, 520, 480, d)
        c.drawCircle(820, 900, 240, P(TEAL, 70, blur=80))
        doctor(c, 820, 1180, .8, 'resident', t, la=10, ra=-12, mood='ok')
        text(c, 'The game hides the diagnosis.', 540, 1290, 54, '#ffffff', 900, 'c', shadow=.35)
        text(c, 'Finding it is your job.', 540, 1362, 54, GOLD, 900, 'c', shadow=.35)
        chip(c, 60, 1440, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
        swipe(c, 640, 1516)
    return f


def slides(case_id):
    K, SC = case.build(case_id)
    return K, [lambda c: p_hook(K)(c), lambda c: p_quote(K)(c), lambda c: p_moves(K)(c), lambda c: p_blank(K)(c),
               lambda c: SC[3][0](c, 2.8)]


if __name__ == '__main__':
    K, fns = slides(sys.argv[1]); fr = save_slides(fns, sys.argv[2])
    if len(sys.argv) > 3: contact_sheet(fr, sys.argv[3], 5)
