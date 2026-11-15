"""Full Game photo set 06 — "Now hiring: emergency doctor." The whole game told as a job ad: the posting, the workload
(163 patients), the job (Talk, Examine, Tests, Treat), the career path (five ranks), the shifts (four modes), apply (Play free).
Usage: python3 fullgame_06_hiring_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
import json
from case import bg, card, chip, TRI, RED

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
BYID = {k['id']: k for k in CASES}


def tab(c, label, x=100, y=532, col=RED, fg='#ffffff'):
    w = tw(label, 30, 900) + 56
    rr(c, x, y, w, 60, 30, P(col)); text(c, label, x + w / 2, y + 41, 30, fg, 900, 'c')


def j_hook(c, t=1.0):
    bg(c, t); brand_bar(c)
    title2(c, 'NOW HIRING', 'Emergency doctor', 372, size=116, sub_size=84)
    card(c, 60, 560, 960, 800)
    tab(c, 'JOB AD  ·  OPEN TODAY')
    rows = [('ROLE', 'Intern, Day 1'), ('WORKLOAD', '163 patients'), ('CAREER PATH', 'Up to ED Director'), ('START', 'Right now')]
    for i, (lab, val) in enumerate(rows):
        y = 640 + i * 172
        if i: c.drawLine(110, y - 14, 660 if i > 1 else 970, y - 14, P('#e4eaf0', stroke=3))
        text(c, lab, 110, y + 40, 28, '#5b7083', 800); text(c, val, 110, y + 110, 60, INK, 900)
    c.drawCircle(850, 1140, 150, P(TEAL, 50, blur=40))
    doctor(c, 850, 1336, .58, 'intern', t, la=10, ra=-150, mood='happy')
    pill(c, 300, 1554, 'Could you do it?', '#ffffff', INK, 40)
    swipe(c, 640, 1516)


GRID = ['nicole-barnes', 'josh-nguyen', 'bob-harris', 'zoe-martin', 'victor-petrov', 'nina-kaur', 'ben-taylor', 'rita-alvarez', 'kai-tanaka']


def j_workload(c, t=1.3):
    bg(c, t); brand_bar(c)
    title2(c, 'THE WORKLOAD', '163 patients. Triage 1 to 5.', 372, size=104, sub_size=64)
    card(c, 60, 560, 960, 880)
    for n, cid in enumerate(GRID):
        K = BYID[cid]; x = 220 + (n % 3) * 320; y = 700 + (n // 3) * 240
        face(c, x, y, 88, K['skin'], K['hair'], K['style'], 'pain' if n % 2 == 0 else 'ok', t + n)
        c.drawCircle(x + 66, y - 66, 30, P('#ffffff')); c.drawCircle(x + 66, y - 66, 25, P(TRI[K['triage']]))
        text(c, str(K['triage']), x + 66, y - 54, 34, '#ffffff', 900, 'c')
        text(c, f"{K['name'].split()[0]}, {K['age']}", x, y + 126, 32, INK, 800, 'c')
    rr(c, 110, 1322, 860, 86, 43, P('#e2f4f1')); text(c, '+ 154 more in the waiting room', 540, 1380, 42, TEAL_D, 900, 'c')
    swipe(c, 640, 1516)


DUTIES = [('talk', 'Talk', 'Take the history'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'),
          ('treat', 'Treat', 'Act before it gets worse')]


def j_job(c, t=1.0):
    bg(c, t); brand_bar(c)
    title2(c, 'THE JOB', 'Talk. Examine. Tests. Treat.', 372, size=104, sub_size=64)
    card(c, 60, 560, 960, 860)
    tab(c, 'DUTIES  ·  EVERY PATIENT')
    for i, (ic, lab, sub) in enumerate(DUTIES):
        y = 636 + i * 190
        if i: c.drawLine(110, y - 8, 970, y - 8, P('#e4eaf0', stroke=3))
        c.drawCircle(190, y + 88, 66, P(TEAL)); icon(c, ic, 190, y + 88, 82)
        text(c, lab, 290, y + 84, 64, INK, 900); text(c, sub, 290, y + 134, 34, '#5b7083', 700)
        rr(c, 880, y + 54, 68, 68, 16, P('#c3cfda', stroke=6)); text(c, str(i + 1), 914, y + 106, 44, '#8a9bab', 900, 'c')
    pill(c, 300, 1554, 'Then make the call.', GOLD, INK, 38)
    swipe(c, 640, 1516)


def j_path(c, t=1.0):
    bg(c, t); brand_bar(c)
    title2(c, 'THE CAREER PATH', 'Five ranks. One doctor.', 372, size=96, sub_size=64)
    c.drawLine(150, 700, 150, 1420, P('#ffffff', 80, stroke=14))
    ln = skia.Paint(AntiAlias=True); ln.setShader(skia.GradientShader.MakeLinear(points=[skia.Point(0, 1420), skia.Point(0, 700)], colors=[C(TEAL), C(GOLD)]))
    ln.setStyle(skia.Paint.kStroke_Style); ln.setStrokeWidth(14); c.drawLine(150, 700, 150, 1420, ln)
    for i in range(5):
        y = 1420 - i * 180; top = i == 4
        c.drawCircle(150, y, 50, P('#ffffff')); c.drawCircle(150, y, 40, P(GOLD if top else TEAL)); text(c, str(i + 1), 150, y + 17, 48, INK if top else '#ffffff', 900, 'c')
        text(c, RANKS[i], 232, y + 22, 62, GOLD if top else '#ffffff', 900, shadow=.35)
    pill(c, 610, 1420, 'You start here', '#ffffff', INK, 28)
    c.drawCircle(840, 820, 210, P(GOLD, 70, blur=80))
    doctor(c, 840, 1030, .6, 'director', t, la=10, ra=-150, mood='happy')
    ar = skia.Path(); ar.moveTo(840, 1062); ar.lineTo(888, 1122); ar.lineTo(792, 1122); ar.close(); c.drawPath(ar, P(GOLD)); rr(c, 822, 1118, 36, 34, 0, P(GOLD))
    doctor(c, 840, 1470, .5, 'intern', t + 1, la=8, ra=-8, mood='tired')
    swipe(c, 100, 1540)


MODES = [('career', 'Career'), ('shift', 'Quick shift'), ('practice', 'Case practice'), ('firstaid', 'First aid')]


def j_shifts(c, t=1.0):
    bg(c, t); brand_bar(c)
    title2(c, 'PICK YOUR SHIFT', 'Four modes.', 372, size=100, sub_size=72)
    for i, (ic, lab) in enumerate(MODES):
        x = 60 + (i % 2) * 490; y = 580 + (i // 2) * 400
        card(c, x, y, 470, 370, 44)
        text(c, f'MODE {i + 1}', x + 40, y + 62, 28, '#5b7083', 800)
        c.drawCircle(x + 235, y + 172, 88, P(RED if ic == 'firstaid' else (GOLD if ic == 'career' else TEAL)))
        icon(c, ic, x + 235, y + 172, 104, INK if ic == 'career' else '#ffffff')
        text(c, lab, x + 235, y + 326, fit(lab, 56, 420), INK, 900, 'c')
    chip(c, 60, 1420, 'DR JOHN SMITH  ·  REPORTING FOR DUTY', '#ffffff', INK, 28, dot=TEAL)
    swipe(c, 640, 1516)


def slides():
    return [j_hook, j_workload, j_job, j_path, j_shifts, lambda c: cta2('Now hiring: you.', 'Start as an Intern today.')(c, 2.5)]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
