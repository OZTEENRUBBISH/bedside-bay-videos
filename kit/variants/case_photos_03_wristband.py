"""Case photo set 03 — "New wristband. New patient." The patient arrives as a hospital wristband (name, age, problem, triage),
then the quote as full-screen type, the four moves as a 2x2 grid, a second wristband with the diagnosis left blank, and the
end card. Never reveals the diagnosis.
Usage: python3 case_photos_03_wristband.py <case-id> <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-5.jpg"""
from common import *
import case
from case import bg, card, chip, TRI, RED
from fullgame_07_quotes import moves_grid


def band(c, cy, ang, draw):
    """White hospital wristband running off both edges; draw(c) fills the label area (x -470..470, y -78..78)."""
    c.save(); c.translate(540, cy); c.rotate(ang)
    rr(c, -760, -78, 1520, 180, 24, P('#000000', 90, blur=24))
    rr(c, -760, -90, 1520, 180, 24, P('#ffffff'))
    for x in list(range(-740, -500, 46)) + list(range(520, 760, 46)): c.drawCircle(x, 0, 11, P('#c3cfda'))
    rr(c, -490, -90, 980, 180, 0, P('#f3f6f9'))
    draw(c); c.restore()


def label(K):
    def f(c):
        rr(c, -470, -70, 196, 140, 18, P(TRI[K['triage']]))
        text(c, 'TRIAGE', -372, -26, 28, '#ffffff', 900, 'c'); text(c, str(K['triage']), -372, 54, 84, '#ffffff', 900, 'c')
        first, last = K['name'].split()[0], K['name'].split()[-1]
        nm = f'{last.upper()}, {first}'; text(c, nm, -244, -8, fit(nm, 58, 500), INK, 900)
        sub = f"AGE {K['age']}  ·  {K['problem'].upper()}"; text(c, sub, -244, 46, fit(sub, 32, 500, 800), '#5b7083', 800)
        x = 290
        for i, w in enumerate((8, 4, 12, 4, 6, 14, 4, 8, 4, 10, 6, 4, 12)):
            c.drawRect(skia.Rect.MakeXYWH(x, -56, w, 112), P(INK)); x += w + 6
    return f


def blank(c):
    rr(c, -470, -70, 196, 140, 18, P(INK)); text(c, '?', -372, 46, 110, GOLD, 900, 'c')
    text(c, 'DIAGNOSIS', -244, -22, 34, '#5b7083', 900)
    p = P('#8a9bab', stroke=6); p.setPathEffect(skia.DashPathEffect.Make([22, 16], 0))
    c.drawLine(-244, 44, 440, 44, p)


def p_hook(K):
    def f(c, t=1.2):
        bg(c, t); brand_bar(c)
        headline(c, ['New wristband.', 'New patient.'], 372, 100)
        band(c, 690, -5, label(K))
        c.drawCircle(540, 1090, 300, P(TEAL, 70, blur=90))
        face(c, 540, 1090, 210, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, 'Just arrived. No diagnosis yet.', 540, 1410, 48, '#bfe9e4', 800, 'c')
        pill(c, 300, 1554, 'Over to you, doctor.', '#ffffff', INK, 36)
        swipe(c, 640, 1516)
    return f


def p_quote(K):
    def f(c, t=2.0):
        bg(c, t); brand_bar(c)
        first = K['name'].split()[0]
        face(c, 150, 420, 84, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, f"{K['name']}, {K['age']}", 266, 410, 54, '#ffffff', 900, shadow=.35)
        lab = f"TRIAGE {K['triage']}"; w = tw(lab, 30, 900) + 40
        rr(c, 266, 432, w, 54, 27, P(TRI[K['triage']])); text(c, lab, 266 + w / 2, 470, 30, '#ffffff', 900, 'c')
        text(c, '“', 50, 790, 300, GOLD, 900)
        size = 92; lines = wrap(K['quote'], size, 900, 940)
        while len(lines) > 5: size -= 4; lines = wrap(K['quote'], size, 900, 940)
        y = 800
        for i, ln in enumerate(lines): text(c, ln, 70, y + i * size * 1.14, size, '#ffffff', 900, shadow=.35)
        ye = y + len(lines) * size * 1.14
        rr(c, 70, ye - 20, 120, 10, 5, P(GOLD)); text(c, f'{first}, when you ask what’s wrong', 70, ye + 50, 40, '#bfe9e4', 700)
        swipe(c, 640, 1516)
    return f


def p_moves(K):
    def f(c, t=1.0):
        bg(c, t); brand_bar(c)
        headline(c, ['Your 4 moves.'], 400, 104)
        moves_grid(c, None, y0=520, th=400)
        chip(c, 60, 1420, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
        swipe(c, 640, 1516)
    return f


def p_blank(K):
    def f(c, t=1.6):
        bg(c, t); brand_bar(c)
        headline(c, ['One band', 'is still blank.'], 372, 100)
        band(c, 720, -5, label(K)); band(c, 1010, 4, blank)
        text(c, 'The game hides the diagnosis.', 540, 1270, 52, '#ffffff', 900, 'c', shadow=.35)
        text(c, 'Finding it is your job.', 540, 1340, 52, GOLD, 900, 'c', shadow=.35)
        chip(c, 60, 1420, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
        swipe(c, 640, 1516)
    return f


def slides(case_id):
    K, SC = case.build(case_id)
    return K, [lambda c: p_hook(K)(c), lambda c: p_quote(K)(c), lambda c: p_moves(K)(c), lambda c: p_blank(K)(c),
               lambda c: SC[3][0](c, 2.8)]


if __name__ == '__main__':
    K, fns = slides(sys.argv[1]); fr = save_slides(fns, sys.argv[2])
    if len(sys.argv) > 3: contact_sheet(fr, sys.argv[3], 5)
