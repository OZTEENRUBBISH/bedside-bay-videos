"""Full Game photo set 10 — "Pop quiz: ER orientation." The whole game as a multiple-choice quiz sheet marked in red pen:
one question per slide (163 patients, the four moves, Intern to ED Director over five ranks, four modes), playful wrong
answers, the right one circled, then the graded sheet (4/4) and Play free.
Usage: python3 fullgame_10_quiz_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
from case import bg, chip, RED
from fullgame_02 import OUT
from b2r_starter_pack_photos import portrait
from fullgame_08_bill_photos import paper, dash, PAPER, GREY, LINE

N = 6
PEN = '#e5484d'
OKG = '#1f9d63'


def count(c, i):
    c.drawCircle(960, 190, 50, P(GOLD)); text(c, f'{i}/{N}', 960, 205, 38, INK, 900, 'c')


def head(c, x, y, w, tag):
    logo(c, x + 40, y + 34, 64); text(c, 'ER ORIENTATION QUIZ', x + 122, y + 70, 36, INK, 900); text(c, 'Name:  Dr John Smith', x + 122, y + 104, 26, GREY, 700)
    tw_ = tw(tag, 28, 900) + 44; rr(c, x + w - 40 - tw_, y + 42, tw_, 52, 26, P(INK)); text(c, tag, x + w - 40 - tw_ / 2, y + 78, 28, '#ffffff', 900, 'c')
    dash(c, x + 40, x + w - 40, y + 140)


def ring(c, x, y, w, h):
    """Hand-drawn red pen loop around a box."""
    c.save(); c.rotate(-1.5, x + w / 2, y + h / 2)
    p = skia.Path(); p.addOval(skia.Rect.MakeXYWH(x - 14, y - 10, w + 28, h + 20)); c.drawPath(p, P(PEN, 235, stroke=9))
    c.drawArc(skia.Rect.MakeXYWH(x - 26, y - 4, w + 40, h + 22), 150, 120, False, P(PEN, 200, stroke=6)); c.restore()


def tick(c, cx, cy, s, col=PEN, w=12):
    p = skia.Path(); p.moveTo(cx - s, cy); p.lineTo(cx - s * .3, cy + s * .7); p.lineTo(cx + s * 1.2, cy - s * 1.1); c.drawPath(p, P(col, stroke=w))


def question(n, q, opts, right, foot):
    """Slide n+1: question n of 4. opts: four answers, right: index of the correct one."""
    def f(c):
        bg(c, 1.0 + n); brand_bar(c); count(c, n + 1)
        title2(c, 'POP QUIZ', f'Question {n} of 4', 372, size=112, sub_size=70)
        x, y, w, h = 60, 570, 960, 870
        paper(c, x, y, w, h); head(c, x, y, w, f'Q{n}')
        size = 58; lines = wrap(q, size, 900, 860)
        while len(lines) > 2: size -= 4; lines = wrap(q, size, 900, 860)
        for i, ln in enumerate(lines): text(c, ln, x + 50, y + 216 + i * size * 1.14 + (0 if len(lines) > 1 else 30), size, INK, 900)
        for i, o in enumerate(opts):
            oy = y + 320 + i * 114; ok = i == right
            rr(c, x + 44, oy, w - 88, 92, 24, P('#e9f7f1' if ok else '#f1ede3'))
            c.drawCircle(x + 100, oy + 46, 32, P(OKG if ok else '#ffffff')); c.drawCircle(x + 100, oy + 46, 32, P(OKG if ok else LINE, stroke=5))
            text(c, 'ABCD'[i], x + 100, oy + 62, 40, '#ffffff' if ok else GREY, 900, 'c')
            s = fit(o, 46, 690 if ok else 760, 900 if ok else 700); text(c, o, x + 156, oy + 46 + s * .35, s, INK if ok else GREY, 900 if ok else 700)
            if ok: ring(c, x + 44, oy, w - 88, 92); tick(c, x + w - 96, oy + 50, 26)
        dash(c, x + 40, x + w - 40, y + 790); s = fit(foot, 36, 860, 900); text(c, foot, 540, y + 844, s, TEAL_D, 900, 'c')
        swipe(c, 640, 1516)
    return f


def q_hook(c, t=1.0):
    bg(c, t); brand_bar(c)
    title2(c, 'POP QUIZ', 'ER orientation', 372, size=132, sub_size=76)
    c.save(); c.rotate(-3, 440, 1000)
    x, y, w, h = 70, 590, 760, 830
    paper(c, x, y, w, h); head(c, x, y, w, '4 Qs')
    for i, q in enumerate(('How many patients?', 'Your four moves?', 'Where can you end up?', 'How many ways to play?')):
        yy = y + 236 + i * 112
        text(c, f'{i + 1}.', x + 50, yy, 50, TEAL_D, 900); text(c, q, x + 116, yy, fit(q, 48, 500), INK, 900)
        rr(c, x + w - 110, yy - 46, 58, 58, 12, P('#ffffff')); rr(c, x + w - 110, yy - 46, 58, 58, 12, P(LINE, stroke=5))
    dash(c, x + 40, x + w - 40, y + 660)
    text(c, 'SCORE', x + 50, y + 756, 56, INK, 900)
    rr(c, x + w - 270, y + 688, 220, 100, 20, P(GOLD)); text(c, '? / 4', x + w - 160, y + 760, 62, INK, 900, 'c')
    c.restore()
    doctor(c, 920, 1500, .52, 'intern', t, la=10, ra=-150, mood='tired')
    pill(c, 300, 1554, 'No studying needed', '#ffffff', INK, 38)
    swipe(c, 640, 1516)


def q_result(c, t=2.2):
    bg(c, t); brand_bar(c); count(c, N)
    title2(c, 'YOU PASSED', 'ER orientation', 372, size=120, sub_size=72)
    x, y, w, h = 110, 580, 860, 700
    paper(c, x, y, w, h); head(c, x, y, w, 'MARKED')
    for i, a in enumerate(('163 patients', 'Talk, Examine, Tests, Treat', 'Intern to ED Director, 5 ranks', '4 modes, starting with Career')):
        yy = y + 210 + i * 72
        text(c, f'{i + 1}.', x + 50, yy, 38, GREY, 800); text(c, a, x + 104, yy, fit(a, 40, 600, 800), INK, 800); tick(c, x + w - 80, yy - 14, 18, PEN, 9)
    dash(c, x + 40, x + w - 40, y + 462)
    text(c, 'SCORE', x + 50, y + 540, 60, INK, 900)
    text(c, '4/4', x + w - 60, y + 640, 190, PEN, 900, 'r'); c.drawArc(skia.Rect.MakeXYWH(x + w - 400, y + 480, 370, 200), 0, 340, False, P(PEN, 220, stroke=9))
    portrait(c, x + 112, y + 620, 56, 'director', 'happy', GOLD); text(c, 'Dr John Smith', x + 190, y + 632, 32, GREY, 800)
    text(c, 'Now try it on 163 patients.', 540, 1352, 46, '#bfe9e4', 800, 'c')
    rr(c, 150, 1396, 780, 110, 55, P('#000000', 80, blur=16)); rr(c, 150, 1386, 780, 110, 55, P(TEAL))
    text(c, 'Play free  ·  bedsidebay.com', 540, 1458, 50, '#ffffff', 900, 'c')


def slides():
    return [q_hook,
            question(1, 'How many patients are waiting for you?', ['3', 'A dozen, tops', '163', 'It’s a quiet day'], 2, '163 patients in the game.'),
            question(2, 'What are your four moves with every patient?', ['Panic, Google, Hope, Nap', 'Talk, Examine, Tests, Treat', 'Coffee, Coffee, Coffee, Coffee', 'Run'], 1, 'The diagnosis? You have to find it.'),
            question(3, 'You start as an Intern. Where can you end up?', ['Still an Intern', 'Head of the vending machine', 'Lost in the parking lot', 'ED Director'], 3, 'Intern, Resident, Registrar, Consultant, ED Director.'),
            question(4, 'How many ways are there to play?', ['None. It’s all paperwork', 'Eleventy', 'Ask at the front desk', 'Four'], 3, 'Career, Quick shift, Case practice, First aid.'),
            q_result]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
