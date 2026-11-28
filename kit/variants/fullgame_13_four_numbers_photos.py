"""Full Game photo set 13 — "4 numbers. One job. Guess them." A number-led curiosity hook: slide 1 shows 163 · 4 · 5 · 4
as four giant colour blocks with Dr John Smith puzzling over them; each following slide is one full-bleed colour with one
giant number and a small illustration: 163 patients (a crowd of the kit's patient faces), 4 moves with every patient
(Talk, Examine, Tests, Treat), 5 ranks (Intern to ED Director, a rising career climb), 4 ways to play (Career first,
then Quick shift, Case practice, First aid). A strip at the bottom fills in the four numbers as you swipe. End card.
Usage: python3 fullgame_13_four_numbers_photos.py <prefix> [sheet.jpg]   -> <prefix>-1.jpg ... <prefix>-6.jpg"""
from common import *
from fullgame_02 import CASES, OUT, STEPS, MODES
from b2r_starter_pack_photos import portrait

NUMS = ['163', '4', '5', '4']
COL = [('#12a394', '#0b5f58'), ('#f8c04a', '#eb9a1c'), ('#6a4bc4', '#3a2880'), ('#2f7fd6', '#173f85')]   # one colour per number
FG = ['#ffffff', INK, '#ffffff', '#ffffff']
ACC = [GOLD, INK, GOLD, GOLD]


def _bg(c, i):
    a, b = COL[i]
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, W * .5, H, [a, b]))
    c.drawCircle(1000, 300, 430, P('#ffffff', 22)); c.drawCircle(60, 1700, 520, P('#000000', 22)); c.drawCircle(980, 1240, 240, P('#ffffff', 14))


def strip(c, upto, cur):
    """The four numbers along the bottom: revealed ones show, the rest are still '?'."""
    for k in range(4):
        x = 60 + k * 138; on = k == cur; shown = k <= upto
        rr(c, x, 1520 + 6, 124, 72, 20, P('#000000', 50, blur=8))
        rr(c, x, 1520, 124, 72, 20, P('#ffffff' if on else COL[k][0] if shown else '#0f2a43', 255 if on or shown else 150))
        if not on: rr(c, x + 2, 1522, 120, 68, 18, P('#ffffff', 170, stroke=4))
        lab = NUMS[k] if shown else '?'
        text(c, lab, x + 62, 1572, 44, INK if on or (shown and k == 1) else '#ffffff', 900, 'c')


def count(c, i):
    c.drawCircle(960, 190, 50, P('#ffffff')); text(c, f'{i}/4', 960, 205, 38, INK, 900, 'c')


def big(c, i, word, sub, size=440):
    n = NUMS[i]
    text(c, n, 540 + 10, 700 + 12, size, '#000000', 900, 'c', a=46)
    text(c, n, 540, 700, size, FG[i], 900, 'c')
    text(c, word, 540, 826, fit(word, 116, 900), ACC[i], 900, 'c', shadow=.25 if i != 1 else 0)
    text(c, sub, 540, 900, fit(sub, 52, 900, 800), FG[i], 800, 'c')


# ---------------------------------------------------------------- slide 1: the hook
def s_hook(c, t=1.0):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, W * .4, H, ['#0d1f36', '#132c4a']))
    c.drawCircle(540, 880, 560, P('#ffffff', 10, blur=80))
    brand_bar(c)
    title2(c, '4 numbers. One job.', 'Can you guess them?', 372, size=100, sub_size=80)
    tiles = [(60, 560, -2.5), (520, 560, 2), (60, 880, 2), (520, 880, -2)]
    for k, (x, y, rot) in enumerate(tiles):
        c.save(); c.rotate(rot, x + 215, y + 145)
        rr(c, x + 8, y + 16, 430, 290, 48, P('#000000', 110, blur=20)); rr(c, x, y, 430, 290, 48, grad(x, y, x + 430, y + 290, list(COL[k])))
        sz = 196 if k == 0 else 236; nx = x + (190 if k == 0 else 205)
        text(c, NUMS[k], nx + 6, y + 224 + 8, sz, '#000000', 900, 'c', a=40)
        text(c, NUMS[k], nx, y + 224, sz, FG[k], 900, 'c')
        c.drawCircle(x + 384, y + 48, 32, P('#0f2a43')); text(c, '?', x + 384, y + 63, 42, '#ffffff', 900, 'c')
        c.restore()
    doctor(c, 196, 1590, .6, 'intern', t, la=10, ra=-146, mood='ok')
    bx, by, bw, bh = 340, 1250, 590, 190
    rr(c, bx, by + 8, bw, bh, 50, P('#000000', 90, blur=16)); rr(c, bx, by, bw, bh, 50, P('#ffffff'))
    tl = skia.Path(); tl.moveTo(bx + 30, by + 120); tl.lineTo(bx - 44, by + 150); tl.lineTo(bx + 40, by + 166); tl.close(); c.drawPath(tl, P('#ffffff'))
    text(c, 'Dr John Smith’s', bx + bw / 2, by + 82, 50, INK, 900, 'c'); text(c, 'whole job. In 4 numbers.', bx + bw / 2, by + 144, 44, TEAL_D, 900, 'c')
    swipe(c, 640, 1516)


# ---------------------------------------------------------------- slide 2: 163 patients
def s_patients(c, t=1.0):
    _bg(c, 0); brand_bar(c); count(c, 1)
    big(c, 0, 'patients.', 'All waiting for Dr John Smith.')
    rows = [(1036, 74, 176, -30, 7, 0), (1196, 88, 196, 60, 6, 7), (1364, 100, 212, -10, 5, 13)]
    for y, r, gap, x0, n, off in rows:
        for k in range(n):
            K = CASES[(off + k) % len(CASES)]
            face(c, x0 + k * gap, y, r, K['skin'], K['hair'], K['style'], 'pain' if (k + off) % 3 == 0 else 'ok', t + k)
    rr(c, 596, 1412 + 8, 330, 84, 42, P('#000000', 90, blur=14)); rr(c, 596, 1412, 330, 84, 42, P(GOLD)); text(c, '+145 more', 761, 1470, 50, INK, 900, 'c')
    strip(c, 0, 0); swipe(c, 640, 1516)


# ---------------------------------------------------------------- slide 3: 4 moves
def s_moves(c, t=1.0):
    _bg(c, 1); brand_bar(c); count(c, 2)
    big(c, 1, 'moves.', 'With every single patient.')
    for k, (ic, lab) in enumerate(STEPS):
        x = 60 + k * 222; y = 972
        rr(c, x + 6, y + 12, 204, 204, 46, P('#000000', 70, blur=14)); rr(c, x, y, 204, 204, 46, P(INK))
        icon(c, ic, x + 102, y + 106, 120, GOLD)
        c.drawCircle(x + 30, y + 30, 28, P('#ffffff')); text(c, str(k + 1), x + 30, y + 45, 40, INK, 900, 'c')
        text(c, lab, x + 102, y + 264, fit(lab, 46, 204), INK, 900, 'c')
        if k < 3:
            ar = skia.Path(); ar.moveTo(x + 207, y + 102); ar.lineTo(x + 219, y + 102); c.drawPath(ar, P(INK, stroke=8))
    K = CASES[4]
    face(c, 196, 1392, 96, K['skin'], K['hair'], K['style'], 'ok', t)
    rr(c, 320, 1340 + 6, 590, 104, 52, P('#000000', 60, blur=12)); rr(c, 320, 1340, 590, 104, 52, P('#ffffff'))
    text(c, 'Diagnosis:  ? ? ?', 615, 1410, 54, INK, 900, 'c')
    strip(c, 1, 1); rr(c, 640, 1516, 300, 76, 38, P(INK)); text(c, 'Swipe  >', 790, 1568, 40, '#ffffff', 900, 'c')


# ---------------------------------------------------------------- slide 4: 5 ranks
def s_ranks(c, t=1.0):
    _bg(c, 2); brand_bar(c); count(c, 3)
    big(c, 2, 'ranks.', 'Intern to ED Director.')
    base = 1476
    for k in range(5):
        x = 60 + k * 176; h = 136 + k * 56; top = k == 4
        rr(c, x + 6, base - h + 10, 160, h, 22, P('#000000', 70, blur=12))
        rr(c, x, base - h, 160, h, 22, P(GOLD if top else '#ffffff')); c.drawRect(skia.Rect.MakeXYWH(x, base - 30, 160, 30), P(GOLD if top else '#ffffff'))
        text(c, str(k + 1), x + 80, base - h + 64, 56, INK if top else COL[2][0], 900, 'c')
        lab = RANKS[k]; text(c, lab, x + 80, base - 14, fit(lab, 26, 148), INK, 900, 'c')
        portrait(c, x + 80, base - h - 70, 60, OUT[k], 'tired' if k == 0 else 'happy', GOLD if top else '#ffffff')
    for j in range(5):
        a = math.pi * (1.02 + j * .24); sparkle(c, 844 + math.cos(a) * 100, base - 360 - 70 + math.sin(a) * 100, 16 + 6 * (j % 2), 255, '#fff6d8')
    strip(c, 2, 2); swipe(c, 640, 1516)


# ---------------------------------------------------------------- slide 5: 4 ways to play
def s_modes(c, t=1.0):
    _bg(c, 3); brand_bar(c); count(c, 4)
    big(c, 3, 'ways to play.', 'Career comes first.')
    x, y, w, h = 60, 958, 872, 216
    rr(c, x + 6, y + 14, w, h, 50, P('#000000', 90, blur=18)); rr(c, x, y, w, h, 50, P(GOLD))
    c.drawCircle(x + 118, y + 108, 80, P(INK)); icon(c, 'career', x + 118, y + 106, 100, GOLD)
    text(c, 'Career', x + 232, y + 138, 96, INK, 900)
    rr(c, x + w - 250, y + 28, 216, 58, 29, P(INK)); text(c, 'START HERE', x + w - 142, y + 68, 30, '#ffffff', 900, 'c')
    text(c, 'Intern to ED Director', x + w - 34, y + 176, 34, INK, 800, 'r')
    for k, (ic, lab) in enumerate(MODES[1:]):
        cx = 60 + k * 298; cy = 1206
        rr(c, cx + 6, cy + 12, 276, 276, 44, P('#000000', 80, blur=14)); rr(c, cx, cy, 276, 276, 44, P('#ffffff'))
        c.drawCircle(cx + 138, cy + 108, 74, P('#e5484d' if ic == 'firstaid' else TEAL)); icon(c, ic, cx + 138, cy + 108, 92)
        text(c, lab, cx + 138, cy + 236, fit(lab, 40, 250), INK, 900, 'c')
    strip(c, 3, 3); swipe(c, 640, 1516)


def slides():
    return [s_hook, s_patients, s_moves, s_ranks, s_modes,
            lambda c: cta2('163 patients. 4 moves. 5 ranks.', '4 ways to play. One job.')(c, 2.5)]


if __name__ == '__main__':
    fr = save_slides(slides(), sys.argv[1])
    if len(sys.argv) > 2: contact_sheet(fr, sys.argv[2], 6)
