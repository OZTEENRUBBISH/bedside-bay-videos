"""Broke to Rich variant 12 — "Going up." Dr John Smith's career as an elevator ride: steel doors slide open on a new floor
for every rank (bare room, ER, theatre, consultant, mansion) while an LED floor display names the floor and the rank and the
career card climbs. Bank amounts after the $2,000 start are illustrative. Music: upbeat, a ding on every floor.
Video: python3 b2r_12_elevator.py <out.mp4>          Preview: python3 b2r_12_elevator.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK
from b2r_ranks_photos import _consult


def doors(c, o, t):
    """Steel elevator doors over the whole frame. o = 0 shut .. 1 open."""
    if o < 1:
        g = 540 * o
        for side in (-1, 1):
            x = 0 - g if side < 0 else 540 + g
            c.drawRect(skia.Rect.MakeXYWH(x, 0, 540, H), grad(x, 0, x + 540, 0, ['#56677a', '#3d4c5d', '#4b5b6d'] if side < 0 else ['#4b5b6d', '#3d4c5d', '#56677a']))
            for j in range(1, 4): c.drawLine(x + j * 135, 0, x + j * 135, H, P('#ffffff', 16, stroke=3, cap=False))
            rr(c, x + 70, 700, 400, 460, 30, P('#2f3c4b', 150)); rr(c, x + 70, 700, 400, 460, 30, P('#7b8c9d', 120, stroke=5))
            ex = x + 540 if side < 0 else x
            c.drawRect(skia.Rect.MakeXYWH(ex - (10 if side < 0 else 0), 0, 10, H), P('#232d39'))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, 26, H), P('#1b2430')); c.drawRect(skia.Rect.MakeXYWH(W - 26, 0, 26, H), P('#1b2430'))


def display(c, floor, small, big, t, moving=False, top=False, big_col='#ffffff'):
    """LED floor display where the headline normally sits: arrow + floor number, small label, big line."""
    x, y, w, h = 60, 292, 960, 300
    rr(c, x, y + 12, w, h, 44, P('#000000', 110, blur=26)); rr(c, x, y, w, h, 44, P('#0b1420'))
    rr(c, x, y, w, h, 44, P(GOLD if top else '#5b7083', stroke=8))
    rr(c, x + 30, y + 30, 250, h - 60, 26, P('#16212e'))
    bob = math.sin(t * 9) * 8 if moving else 0
    p = skia.Path(); p.moveTo(x + 86, y + 190 + bob); p.lineTo(x + 122, y + 118 + bob); p.lineTo(x + 158, y + 190 + bob); p.close()
    c.drawPath(p, P(GOLD, 255 if (moving or top) else 120))
    c.drawCircle(x + 216, y + 150, 70, P(GOLD, 40, blur=30))
    text(c, str(floor), x + 216, y + 204, 150, GOLD, 900, 'c')
    text(c, small, x + 316, y + 96, 34, '#8fa3b5', 900)
    text(c, big, x + 314, y + 206, fit(big, 108, 620), big_col, 900)
    for i in range(5):
        c.drawCircle(x + 330 + i * 46, y + 250, 13, P(GOLD if i < floor else '#263444'))


def floor(fn, i, d, hook=False):
    """One floor: scene fn behind the doors, display + career card on top. i = rank index 0..4."""
    a0 = 1.3 if hook else .15
    def f(c, t):
        fn(c, t)
        o = eio((t - a0) / .7) * (1 - eio((t - (d - .3)) / .3))
        doors(c, o, t)
        top = i == 4
        if hook and t < a0 + .45:
            display(c, 1, 'DR JOHN SMITH  ·  HIS CAREER', 'Going up.', t, moving=True)
            if .5 < t < a0 + .1: pill(c, 540, 930, 'One career. Five floors.', GOLD, INK, 56, pop((t - .5) / .4))
        else:
            display(c, i + 1, f'FLOOR {i + 1} OF 5' if not top else 'TOP FLOOR  ·  5 OF 5', RANKS[i], t, moving=t > d - .3, top=top, big_col=GOLD if top else '#ffffff')
        if i == 0: bank, prog = 2000, 1.0
        else: bank, prog = lerp(BANK[i - 1], BANK[i], eio((t - a0 - .3) / 1.3)), lerp(i, i + 1, eio((t - a0 - .2) / 1.0))
        bump = abs(math.sin(t * 9)) * .5 if (i > 0 and a0 + .3 < t < a0 + 1.6) else 0
        hud(c, i if t > a0 + .2 or i == 0 else i - 1, bank, prog, bump=bump)
        brand_bar(c)
        if hook and t > 2.2: pill(c, 300, 760, 'Floor 1: broke', '#ffffff', INK, 46, pop((t - 2.2) / .35))
        if top and t > 1.4: pill(c, 300, 656, 'You made it.', GOLD, INK, 46, pop((t - 1.4) / .35))
    return f


D = [3.4, 2.8, 2.8, 2.6, 3.4]
SC = [(floor(scenes.poor, 0, D[0], hook=True), D[0]), (floor(lambda c, t: scenes.er(c, t + 1, 'resident'), 1, D[1]), D[1]),
      (floor(scenes.theatre, 2, D[2]), D[2]), (floor(_consult, 3, D[3]), D[3]),
      (floor(lambda c, t: scenes.rich(c, t + 1.2), 4, D[4]), D[4]), (cta2('Going up?', 'Start on the ground floor.'), 3.4)]

VOICE = [(0.15, 'Going up. Floor one. Broke intern.', 3.0), (3.6, 'Floor two. Resident.', 2.4), (6.4, 'Floor three. Registrar.', 2.4),
         (9.2, 'Floor four. Consultant.', 2.2), (11.8, 'Top floor. E.D. Director.', 2.9), (15.3, 'Bedside Bay. Play free.', 2.9)]


def soundtrack(wav):
    import sound
    st = [0, 3.4, 6.2, 9.0, 11.6]
    cues = [(.05, 'beep'), (.5, 'pop'), (1.3, 'ding'), (1.35, 'whoosh'), (2.2, 'pop')]
    cues += [(s + .12, 'ding') for s in st[1:]] + [(s + .15, 'whoosh') for s in st[1:]] + [(s + .55, f'step:{i + 1}') for i, s in enumerate(st[1:])]
    cues += [(s + .8, 'cash') for s in st[1:]] + [(s - .3, 'whoosh') for s in st[1:]] + [(13.0, 'pop'), (13.8, 'riser'), (15.0, 'impact'), (15.05, 'ding')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=1.3, lift=11.6, cta=15.0, cues=cues, voice=VOICE)


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 1.0), (0, 1.6), (0, 3.0), (1, 0.4), (1, 2.2), (2, 2.0), (3, 2.0), (4, 2.6), (5, 2.5)]
        contact_sheet([frame(SC[i][0], t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video(SC, out, wav); os.remove(wav)
