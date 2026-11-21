"""Full Game variant 09 — "The board is full." The hook is an ER tracking whiteboard filling up with real patients from
cases.json (name, age, presenting problem, triage; no diagnoses) and a "+157 more" counter, then the four moves ticked off
on the board for one patient, the five ranks as a staff roster beside Dr John Smith, and the four modes with Career as the
big tile. Music: bright.
Video: python3 fullgame_09_board.py <out.mp4>          Preview: python3 fullgame_09_board.py preview <sheet.jpg>"""
from common import *
import json
from case import bg, card, chip, TRI, RED

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
BYID = {k['id']: k for k in CASES}
ROWS = ['victor-petrov', 'nina-castillo', 'ethan-brooks', 'mark-duval', 'lucy-grant', 'josh-nguyen']
OUT = ['intern', 'resident', 'surgeon', 'consultant', 'director']
BX, BY, BW, BH = 50, 480, 980, 900  # the whiteboard


def board(c, title, h=BH):
    """Whiteboard with an aluminium frame, a title strip and a marker tray."""
    rr(c, BX - 14, BY - 2, BW + 28, h + 40, 30, P('#000000', 100, blur=26))
    rr(c, BX - 14, BY - 14, BW + 28, h + 28, 30, P('#aab7c3'))
    rr(c, BX, BY, BW, h, 18, P('#fbfdfe'))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(BX, BY, BW, h), 18, 18), True)
    c.drawRect(skia.Rect.MakeXYWH(BX, BY, BW, 84), P(INK)); c.restore()
    text(c, title, BX + 34, BY + 56, 36, '#ffffff', 900)
    for i, col in enumerate((TEAL, RED, GOLD)): c.drawCircle(BX + BW - 150 + i * 46, BY + 42, 15, P(col))
    rr(c, BX + 300, BY + h + 6, 380, 22, 8, P('#8795a3'))
    for i, col in enumerate((INK, RED, TEAL_D)): rr(c, BX + 330 + i * 110, BY + h - 6, 84, 16, 8, P(col))


def row(c, K, i, y, k, hl=False):
    """One patient line: bed number, face, name and age, presenting problem, triage chip. k = 0..1 write-in."""
    h = 116
    if hl: rr(c, BX + 12, y + 4, BW - 24, h - 8, 20, P('#fff3d0')); rr(c, BX + 12, y + 4, BW - 24, h - 8, 20, P(GOLD, stroke=6))
    c.drawLine(BX + 24, y + h, BX + BW - 24, y + h, P('#dfe7ee', stroke=3))
    a = 255 * clamp(k * 2)
    c.drawCircle(BX + 62, y + 58, 34, P(INK, a)); text(c, str(i + 1), BX + 62, y + 74, 44, '#ffffff', 900, 'c', a=a)
    if k > .15: face(c, BX + 158, y + 58, 44 * pop((k - .15) / .5), K['skin'], K['hair'], K['style'], 'pain', i * 1.3)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(BX + 214, y, (BW - 214) * clamp(k * 1.3), h))  # marker wipes in from the left
    nm = f"{K['name']}, {K['age']}"; text(c, nm, BX + 220, y + 54, fit(nm, 44, 500), INK, 900)
    text(c, K['problem'], BX + 220, y + 96, 32, '#5b7083', 700)
    lab = f"TRIAGE {K['triage']}"; w = tw(lab, 28, 900) + 44
    rr(c, BX + BW - 30 - w, y + 30, w, 58, 29, P(TRI[K['triage']])); text(c, lab, BX + BW - 30 - w / 2, y + 69, 28, '#ffffff', 900, 'c')
    c.restore()


def b_hook(c, t):
    bg(c, t); brand_bar(c)
    headline(c, ['The board is full.'], 410, 108)
    board(c, 'EMERGENCY  ·  NOW WAITING')
    text(c, 'BED', BX + 62, BY + 122, 22, '#8a9bab', 900, 'c'); text(c, 'PATIENT', BX + 220, BY + 122, 22, '#8a9bab', 900)
    text(c, 'PRIORITY', BX + BW - 40, BY + 122, 22, '#8a9bab', 900, 'r')
    for i, cid in enumerate(ROWS):
        a0 = .1 + i * .36
        if t >= a0: row(c, BYID[cid], i, BY + 136 + i * 116, clamp((t - a0) / .4))
    if t > 2.4:
        n = int(lerp(6, 163, eio((t - 2.4) / .7)))
        pill(c, 540, BY + 136 + 6 * 116 + 42, f'+ {163 - 6} more  ·  {n} patients', GOLD, INK, 44, pop((t - 2.4) / .4))
    if t > 2.9: pill(c, 540, 1490, 'Who do you see first?', '#ffffff', INK, 48, pop((t - 2.9) / .4))


MOVES = [('talk', 'Talk', 'Get the story'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Make the call')]


def b_moves(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Pick a patient.', 'Then it’s four moves.', 348, a=255 * k0, dy=(1 - k0) * 30, size=100, sub_size=72)
    board(c, 'BED 1  ·  YOUR PATIENT')
    row(c, BYID[ROWS[0]], 0, BY + 96, 1, hl=True)
    for i, (ic, lab, sub) in enumerate(MOVES):
        y = BY + 236 + i * 160; ti = .35 + i * .5; on = t >= ti
        k = pop((t - ti) / .35) if on else 1
        c.drawLine(BX + 24, y + 160, BX + BW - 24, y + 160, P('#dfe7ee', stroke=3))
        c.save(); c.translate(BX + 110, y + 80); c.scale(k, k)
        c.drawCircle(0, 0, 58, P(TEAL if on else '#c3cfda')); icon(c, ic, 0, 0, 70); c.restore()
        text(c, lab, BX + 200, y + 84, 68, INK if on else '#a9b6c2', 900)
        text(c, sub, BX + 200, y + 130, 32, '#5b7083' if on else '#c3cfda', 700)
        bx, by = BX + BW - 110, y + 80
        rr(c, bx - 40, by - 40, 80, 80, 16, P(TEAL_D if on else '#c3cfda', stroke=8))
        if on:
            kk = clamp((t - ti) / .25); p = skia.Path(); p.moveTo(bx - 26, by); p.lineTo(bx - 6, by + 22)
            if kk > .4: p.lineTo(bx - 6 + 46 * (kk - .4) / .6, by + 22 - 58 * (kk - .4) / .6)
            c.drawPath(p, P(RED, stroke=13))
    chip(c, 60, 1440, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)


def b_ranks(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Clear the board.', 'Climb five ranks.', 348, a=255 * k0, dy=(1 - k0) * 30, size=100, sub_size=84)
    step = .5; cur = min(4, int(max(0, t - .35) / step)); lt = max(0, t - .35) - cur * step; top = cur == 4
    # staff roster (left), bottom rank at the bottom
    card(c, 50, 520, 500, 870, 36)
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(50, 520, 500, 870), 36, 36), True)
    c.drawRect(skia.Rect.MakeXYWH(50, 520, 500, 84), P(INK)); c.restore()
    text(c, 'STAFF ROSTER', 300, 576, 34, '#ffffff', 900, 'c')
    for i in range(5):
        y = 620 + (4 - i) * 152; on = i <= cur; here = i == cur
        colr = (GOLD if i == 4 else TEAL) if on else '#eef2f6'
        k = pop(lt / .3) if (here and t >= .35) else 1
        c.save(); c.translate(300, y + 70); c.scale(k, k)
        rr(c, -226, -62, 452, 124, 28, P(colr))
        if here: rr(c, -226, -62, 452, 124, 28, P(INK, stroke=8))
        c.drawCircle(-170, 0, 36, P('#ffffff' if on else '#d5dde5')); text(c, str(i + 1), -170, 16, 44, INK if on else '#8a9bab', 900, 'c')
        text(c, RANKS[i], -116, 18, fit(RANKS[i], 52, 320), (INK if i == 4 else '#ffffff') if on else '#8a9bab', 900)
        c.restore()
    # Dr John Smith (right), outfit changes with the rank
    c.drawCircle(810, 1000, 300, P(GOLD if top else TEAL, 80, blur=90))
    doctor(c, 810, 1330, .98, OUT[cur], t, la=10, ra=-150 if top else -12, mood='tired' if cur == 0 else 'happy')
    pill(c, 810, 640, 'Dr John Smith', '#ffffff', INK, 40)
    if cur > 0 and lt < .4:
        k = lt / .4
        for j in range(8):
            a = j * math.pi / 4 + t; sparkle(c, 810 + math.cos(a) * (240 + 90 * k), 1000 + math.sin(a) * (300 + 90 * k), 22, 255 * (1 - k), GOLD)
    text(c, f'RANK {cur + 1} OF 5', 540, 1474, 40, '#bfe9e4', 800, 'c')


SUB = [('shift', 'Quick shift'), ('practice', 'Case practice'), ('firstaid', 'First aid')]


def b_modes(c, t):
    bg(c, t); brand_bar(c); k0 = ease(t / .3)
    title2(c, 'Four modes.', 'Career comes first.', 348, a=255 * k0, dy=(1 - k0) * 30, size=104, sub_size=84)
    if t >= .2:
        k = pop((t - .2) / .4)
        c.save(); c.translate(540, 760); c.scale(k, k); c.translate(-540, -760)
        card(c, 60, 560, 960, 400, 48, col=GOLD)
        c.drawCircle(230, 760, 116, P(INK)); icon(c, 'career', 230, 760, 140)
        text(c, 'MODE 1', 390, 680, 34, '#7a5a10', 900); text(c, 'Career', 386, 790, 124, INK, 900)
        text(c, 'Intern to ED Director', 390, 856, 42, INK, 700)
        w = tw('START HERE', 28, 900) + 44; rr(c, 980 - w, 596, w, 56, 28, P(INK)); text(c, 'START HERE', 980 - w / 2, 634, 28, '#ffffff', 900, 'c')
        c.restore()
    for i, (ic, lab) in enumerate(SUB):
        a0 = .7 + i * .3
        if t < a0: continue
        k = pop((t - a0) / .35); x = 60 + i * 326
        c.save(); c.translate(x + 154, 1180); c.scale(k, k); c.translate(-(x + 154), -1180)
        card(c, x, 1000, 308, 360, 40)
        c.drawCircle(x + 154, 1130, 82, P(RED if ic == 'firstaid' else TEAL)); icon(c, ic, x + 154, 1130, 98)
        text(c, f'MODE {i + 2}', x + 154, 1264, 26, '#8a9bab', 900, 'c')
        text(c, lab, x + 154, 1318, fit(lab, 46, 280), INK, 900, 'c'); c.restore()
    chip(c, 60, 1440, 'DR JOHN SMITH  ·  INTERN, DAY 1', '#ffffff', INK, 28, dot=TEAL)


SC = [(b_hook, 3.6), (b_moves, 3.0), (b_ranks, 3.4), (b_modes, 3.0), (cta2('The board is full.', 'Your shift starts now.'), 3.4)]

VOICE = [(0.15, 'The board is full. One hundred and sixty-three patients.', 3.3), (3.8, 'Pick one. Then it’s four moves.', 2.7),
         (6.8, 'Clear the board. Climb five ranks.', 3.1), (10.2, 'Four modes. Career comes first.', 2.7), (13.3, 'Bedside Bay. Play free.', 2.9)]


def soundtrack(wav):
    import sound
    cues = [(.1 + i * .36, 'tick') for i in range(6)] + [(.2 + i * .36, 'pop') for i in range(6)] + [(2.4, 'ding'), (2.9, 'pop'), (3.35, 'whoosh')]
    cues += [(3.95 + i * .5, 'pop') for i in range(4)] + [(4.05 + i * .5, 'tick') for i in range(4)] + [(6.35, 'whoosh')]
    cues += [(6.95 + i * .5, f'step:{i}') for i in range(5)] + [(9.0, 'cash'), (9.75, 'whoosh')]
    cues += [(10.2, 'ding')] + [(10.7 + i * .3, 'pop') for i in range(3)] + [(11.8, 'riser'), (13.0, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'bright', drop=0.0, lift=6.6, cta=13.0, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .16)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 1.2), (0, 3.4), (1, 0.6), (1, 2.8), (2, 0.5), (2, 1.6), (2, 3.2), (3, 0.5), (3, 2.8)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
