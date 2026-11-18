"""Full Game photo set 08 — "The bill for running your own ER." The whole game as an itemised receipt: 163 patients,
4 moves per patient, 5 ranks, 4 modes, one item per slide, then the total: $0.00 (Play free).
Usage: python3 fullgame_08_bill_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
import json
from case import bg, chip, TRI, RED
from fullgame_02 import OUT
from b2r_starter_pack_photos import portrait

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
BYID = {k['id']: k for k in CASES}
PAPER, GREY, LINE = '#fbf8f1', '#6b7785', '#b9b2a4'
N = 6


def paper(c, x, y, w, h):
    """Receipt paper with a torn zigzag bottom edge."""
    p = skia.Path(); p.moveTo(x, y); p.lineTo(x + w, y); p.lineTo(x + w, y + h)
    n = int(w // 40)
    for i in range(n):
        p.lineTo(x + w - (i + .5) * w / n, y + h + 22); p.lineTo(x + w - (i + 1) * w / n, y + h)
    p.close()
    c.save(); c.translate(0, 14); c.drawPath(p, P('#000000', 110, blur=26)); c.restore(); c.drawPath(p, P(PAPER))


def dash(c, x0, x1, y):
    x = x0
    while x < x1: c.drawLine(x, y, min(x + 16, x1), y, P(LINE, stroke=4, cap=False)); x += 28


def count(c, i):
    c.drawCircle(960, 190, 50, P(GOLD)); text(c, f'{i}/{N}', 960, 205, 38, INK, 900, 'c')


def head(c, x, y, w, label):
    """Receipt header inside the paper: small logo, shop name, item label."""
    logo(c, x + 40, y + 34, 64); text(c, 'BEDSIDE BAY ER', x + 122, y + 70, 36, INK, 900); text(c, 'Attending: Dr John Smith', x + 122, y + 104, 26, GREY, 700)
    tw_ = tw(label, 28, 900) + 44; rr(c, x + w - 40 - tw_, y + 42, tw_, 52, 26, P(INK)); text(c, label, x + w - 40 - tw_ / 2, y + 78, 28, '#ffffff', 900, 'c')
    dash(c, x + 40, x + w - 40, y + 140)


ITEMS = [('163', 'Patients'), ('4', 'Moves per patient'), ('5', 'Ranks to climb'), ('4', 'Modes')]


def b_hook(c, t=1.0):
    bg(c, t); brand_bar(c)
    title2(c, 'THE BILL', 'for running your own ER', 372, size=128, sub_size=70)
    c.save(); c.rotate(-3, 480, 1000)
    x, y, w, h = 90, 590, 780, 830
    paper(c, x, y, w, h); head(c, x, y, w, 'ITEMISED')
    for i, (q, lab) in enumerate(ITEMS):
        yy = y + 236 + i * 118
        text(c, q, x + 150, yy, 64, TEAL_D, 900, 'r'); text(c, '×', x + 170, yy - 4, 44, GREY, 800); text(c, lab, x + 216, yy, fit(lab, 54, 520), INK, 900)
    dash(c, x + 40, x + w - 40, y + 640)
    text(c, 'TOTAL DUE', x + 50, y + 742, 56, INK, 900)
    rr(c, x + w - 250, y + 672, 200, 100, 20, P(GOLD)); text(c, '$ ?', x + w - 150, y + 744, 64, INK, 900, 'c')
    c.restore()
    doctor(c, 920, 1500, .52, 'intern', t, la=10, ra=-150, mood='tired')
    pill(c, 300, 1554, 'Swipe for the total', '#ffffff', INK, 38)
    swipe(c, 640, 1516)


def sheet(c, n, top, sub, tag):
    bg(c, 1.0 + n); brand_bar(c); count(c, n + 1)
    title2(c, top, sub, 372, size=112, sub_size=72)
    paper(c, 60, 570, 960, 870); head(c, 60, 570, 960, tag)


LIST = ['victor-petrov', 'megan-lewis', 'ben-taylor', 'joan-harper', 'kai-tanaka']


def b_patients(c):
    sheet(c, 1, '163 ×', 'Patients', 'ITEM 1 of 4')
    for i, cid in enumerate(LIST):
        K = BYID[cid]; y = 740 + i * 122
        face(c, 150, y + 44, 50, K['skin'], K['hair'], K['style'], 'pain' if i % 2 == 0 else 'ok', 1.0 + i)
        text(c, f"{K['name']}, {K['age']}", 230, y + 40, 44, INK, 900); text(c, K['problem'], 230, y + 82, 30, GREY, 700)
        lab = f"Triage {K['triage']}"; w = tw(lab, 30, 900) + 44
        rr(c, 970 - w, y + 16, w, 56, 28, P(TRI[K['triage']])); text(c, lab, 970 - w / 2, y + 54, 30, '#ffffff', 900, 'c')
    dash(c, 100, 980, 1352); text(c, '+ 158 more in the waiting room', 540, 1410, 40, TEAL_D, 900, 'c')
    swipe(c, 640, 1516)


MOVES = [('talk', 'Talk', 'Take the history'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Act before it gets worse')]


def b_moves(c):
    sheet(c, 2, '4 ×', 'Moves per patient', 'ITEM 2 of 4')
    for i, (ic, lab, sub) in enumerate(MOVES):
        y = 736 + i * 148
        c.drawCircle(160, y + 60, 56, P(TEAL)); icon(c, ic, 160, y + 60, 70)
        text(c, lab, 250, y + 58, 58, INK, 900); text(c, sub, 250, y + 102, 32, GREY, 700)
        text(c, f'{i + 1}', 960, y + 80, 56, LINE, 900, 'r')
    dash(c, 100, 980, 1336); text(c, 'Diagnosis: not included.', 100, 1392, 38, INK, 900); text(c, 'You find it.', 980, 1392, 38, RED, 900, 'r')
    swipe(c, 640, 1516)


def b_ranks(c):
    sheet(c, 3, '5 ×', 'Ranks to climb', 'ITEM 3 of 4')
    for i in range(5):
        y = 738 + i * 122; top = i == 4
        portrait(c, 150, y + 46, 50, OUT[i], 'tired' if i == 0 else 'happy', GOLD if top else TEAL)
        text(c, RANKS[i], 230, y + 64, 52, INK, 900)
        lab = f'RANK {i + 1}'; w = tw(lab, 28, 900) + 44
        rr(c, 970 - w, y + 18, w, 54, 27, P(GOLD if top else '#e2f4f1')); text(c, lab, 970 - w / 2, y + 55, 28, INK if top else TEAL_D, 900, 'c')
    dash(c, 100, 980, 1352); text(c, 'You start as an Intern with $2,000.', 540, 1410, 38, TEAL_D, 900, 'c')
    swipe(c, 640, 1516)


MODES = [('career', 'Career'), ('shift', 'Quick shift'), ('practice', 'Case practice'), ('firstaid', 'First aid')]


def b_modes(c):
    sheet(c, 4, '4 ×', 'Modes', 'ITEM 4 of 4')
    for i, (ic, lab) in enumerate(MODES):
        y = 736 + i * 148
        c.drawCircle(160, y + 60, 56, P(RED if ic == 'firstaid' else (GOLD if ic == 'career' else TEAL))); icon(c, ic, 160, y + 60, 70, INK if ic == 'career' else '#ffffff')
        text(c, lab, 250, y + 80, 58, INK, 900)
        text(c, f'MODE {i + 1}', 970, y + 76, 30, GREY, 800, 'r')
    dash(c, 100, 980, 1336); text(c, 'All four on the same bill.', 540, 1394, 38, TEAL_D, 900, 'c')
    swipe(c, 640, 1516)


def b_total(c, t=2.2):
    bg(c, t); brand_bar(c); count(c, N)
    title2(c, 'TOTAL DUE', 'for all of it', 372, size=120, sub_size=70)
    x, y, w, h = 110, 580, 860, 700
    paper(c, x, y, w, h); head(c, x, y, w, 'PAID')
    for i, (q, lab) in enumerate(ITEMS):
        yy = y + 206 + i * 70
        text(c, f'{q} × {lab}', x + 50, yy, 38, INK, 800); text(c, 'included', x + w - 50, yy, 34, GREY, 700, 'r')
    dash(c, x + 40, x + w - 40, y + 452)
    text(c, 'TOTAL', x + 50, y + 540, 64, INK, 900); text(c, '$0.00', x + w - 50, y + 630, 170, TEAL_D, 900, 'r')
    c.save(); c.rotate(-8, 290, 1200); rr(c, 160, 1146, 260, 104, 18, P(RED, 235, stroke=10)); text(c, 'FREE', 290, 1228, 84, RED, 900, 'c', a=235); c.restore()
    rr(c, 150, 1386, 780, 110, 55, P('#000000', 80, blur=16)); rr(c, 150, 1376, 780, 110, 55, P(TEAL))
    text(c, 'Play free  ·  bedsidebay.com', 540, 1448, 50, '#ffffff', 900, 'c')


def slides():
    return [b_hook, b_patients, b_moves, b_ranks, b_modes, b_total]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
