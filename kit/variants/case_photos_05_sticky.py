"""Case photo set 05 — "Note from triage." The patient's own words arrive as a sticky note left on the doctor's desk
(quote first, as the hook), then a pinned photo with three small notes (problem, triage, level), the four moves as four
coloured sticky notes, one note left blank for the diagnosis, and the end card. Never reveals the diagnosis.
Usage: python3 case_photos_05_sticky.py <case-id> <prefix> [sheet.jpg] [bed-number]   -> <prefix>-1.jpg ... <prefix>-5.jpg"""
from common import *
import case
from case import bg, card, chip, TRI, RED

BED = 4
YEL, PINK, BLUE, GREEN = '#ffe66b', '#ffa9cb', '#9ad8ff', '#aee8a4'
PEN = '#1d2a4a'


def note(c, cx, cy, w, h, ang, col, draw, tape=True):
    """Square paper note with a soft shadow, a curled corner and a strip of tape; draw(c) fills it around (0, 0)."""
    c.save(); c.translate(cx, cy); c.rotate(ang)
    c.save(); c.translate(6, 18); rr(c, -w / 2, -h / 2, w, h, 6, P('#000000', 110, blur=24)); c.restore()
    p = skia.Path(); f = min(w, h) * .13
    p.moveTo(-w / 2, -h / 2); p.lineTo(w / 2, -h / 2); p.lineTo(w / 2, h / 2 - f); p.lineTo(w / 2 - f, h / 2); p.lineTo(-w / 2, h / 2); p.close()
    c.drawPath(p, P(col))
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h * .13), P('#000000', 14))
    cu = skia.Path(); cu.moveTo(w / 2, h / 2 - f); cu.lineTo(w / 2 - f, h / 2); cu.lineTo(w / 2 - f, h / 2 - f); cu.close()
    c.drawPath(cu, P('#000000', 46))
    if tape:
        tw_ = min(220, w * .42); c.save(); c.rotate(-3); rr(c, -tw_ / 2, -h / 2 - 26, tw_, 56, 6, P('#ffffff', 120)); c.restore()
    draw(c); c.restore()


def p_hook(K):
    def f(c, t=1.2):
        bg(c, t); brand_bar(c)
        text(c, 'Note from triage:', 540, 356, 84, GOLD, 900, 'c', shadow=.35)
        q = '“' + K['quote'] + '”'; size = 98; lines = wrap(q, size, 900, 700)
        while len(lines) > 4: size -= 4; lines = wrap(q, size, 900, 700)
        def d(c):
            lab = f"BED {BED}  ·  TRIAGE {K['triage']}"; w = tw(lab, 34, 900) + 48
            rr(c, -350, -340, w, 64, 32, P(TRI[K['triage']])); text(c, lab, -350 + w / 2, -297, 34, '#ffffff', 900, 'c')
            y0 = -250 + size * .95
            for i, ln in enumerate(lines): text(c, ln, -350, y0 + i * size * 1.13, size, PEN, 900)
            text(c, f"{K['name']}, {K['age']}", -350, 330, 50, '#6f6220', 900)
        note(c, 540, 850, 800, 800, -3, YEL, d)
        c.drawCircle(868, 1250, 150, P('#000000', 90, blur=30))
        face(c, 868, 1240, 132, K['skin'], K['hair'], K['style'], 'pain', t)
        chip(c, 60, 1404, f"{K['problem'].upper()}  ·  {K['level'].upper()}", '#ffffff', INK, 28, dot=TRI[K['triage']])
        pill(c, 300, 1554, "You're the doctor.", '#ffffff', INK, 38)
        swipe(c, 640, 1516)
    return f


def p_who(K):
    def f(c, t=2.0):
        bg(c, t); brand_bar(c)
        headline(c, [f'Who’s in bed {BED}?'], 400, 100)
        c.save(); c.translate(350, 900); c.rotate(-4)
        rr(c, -256, -310 + 16, 512, 640, 10, P('#000000', 110, blur=26)); rr(c, -256, -310, 512, 640, 10, P('#ffffff'))
        c.drawRect(skia.Rect.MakeXYWH(-222, -276, 444, 444), grad(0, -276, 0, 168, ['#dff1f4', '#9fd4cf']))
        face(c, 0, -54, 196, K['skin'], K['hair'], K['style'], 'pain', t)
        nm = f"{K['name']}, {K['age']}"; text(c, nm, 0, 262, fit(nm, 60, 440), PEN, 900, 'c')
        c.drawCircle(0, -310, 22, P(RED)); c.drawCircle(-6, -316, 7, P('#ffffff', 150))  # push pin
        c.restore()
        rows = [('PROBLEM', K['problem'], YEL, 3), ('TRIAGE', f"{K['triage']} of 5", PINK, -3), ('LEVEL', K['level'], BLUE, 2)]
        for i, (lab, val, col, ang) in enumerate(rows):
            def d(c, lab=lab, val=val):
                text(c, lab, 0, -42, 30, '#5b5a3a', 900, 'c'); text(c, val, 0, 42, fit(val, 64, 300), PEN, 900, 'c')
            note(c, 824, 660 + i * 252, 360, 216, ang, col, d)
        first = K['name'].split()[0]
        text(c, f'{first} is waiting on you.', 540, 1400, 60, '#ffffff', 900, 'c', shadow=.35)
        swipe(c, 640, 1516)
    return f


MOVES = [('talk', 'Talk', 'Get the story', YEL, -2), ('examine', 'Examine', 'Find the signs', PINK, 2),
         ('tests', 'Tests', 'Order what matters', BLUE, 2), ('treat', 'Treat', 'Make the call', GREEN, -2)]


def p_moves(K):
    def f(c, t=1.0):
        bg(c, t); brand_bar(c)
        first = K['name'].split()[0]
        title2(c, 'Four moves.', f'{first} needs all of them.', 356, size=104, sub_size=72)
        for i, (ic, lab, sub, col, ang) in enumerate(MOVES):
            def d(c, i=i, ic=ic, lab=lab, sub=sub):
                c.drawCircle(-150, -112, 40, P(PEN)); text(c, str(i + 1), -150, -94, 52, '#ffffff', 900, 'c')
                icon(c, ic, 96, -96, 150, PEN)
                text(c, lab, -190, 86, fit(lab, 88, 390), PEN, 900); text(c, sub, -188, 142, fit(sub, 34, 300, 800), '#4a4a3a', 800)
            note(c, 296 + (i % 2) * 488, 720 + (i // 2) * 424, 450, 384, ang, col, d)
        chip(c, 60, 1440, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
        swipe(c, 640, 1516)
    return f


def p_blank(K):
    def f(c, t=1.6):
        bg(c, t); brand_bar(c)
        headline(c, ['One note', 'is still blank.'], 372, 100)
        def d(c):
            text(c, 'DIAGNOSIS', 0, -150, 44, '#6f6220', 900, 'c')
            text(c, '?', 0, 110, 290, PEN, 900, 'c')
            dd = P(PEN, stroke=6); dd.setPathEffect(skia.DashPathEffect.Make([18, 14], 0)); c.drawLine(-180, 160, 180, 160, dd)
            text(c, f'Bed {BED}', 0, 208, 34, '#6f6220', 900, 'c')
        note(c, 320, 900, 500, 500, -5, YEL, d)
        c.drawCircle(820, 930, 240, P(TEAL, 70, blur=80))
        doctor(c, 820, 1200, .8, 'resident', t, la=10, ra=-12, mood='ok')
        text(c, 'The game hides the diagnosis.', 540, 1300, 54, '#ffffff', 900, 'c', shadow=.35)
        text(c, 'Finding it is your job.', 540, 1372, 54, GOLD, 900, 'c', shadow=.35)
        chip(c, 60, 1440, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
        swipe(c, 640, 1516)
    return f


def slides(case_id):
    K, SC = case.build(case_id)
    return K, [lambda c: p_hook(K)(c), lambda c: p_who(K)(c), lambda c: p_moves(K)(c), lambda c: p_blank(K)(c),
               lambda c: SC[3][0](c, 2.8)]


if __name__ == '__main__':
    if len(sys.argv) > 4: BED = int(sys.argv[4])
    K, fns = slides(sys.argv[1]); fr = save_slides(fns, sys.argv[2])
    if len(sys.argv) > 3 and sys.argv[3] != '-': contact_sheet(fr, sys.argv[3], 5)
