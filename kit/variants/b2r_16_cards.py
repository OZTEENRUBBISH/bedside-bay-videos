"""Broke to Rich variant 16 — "Every doctor starts as a common card." Dr John Smith's career as a collectible card that
flips and levels up with every rank: Common Intern, Uncommon Resident, Rare Registrar, Epic Consultant, Legendary
ED Director (gold foil, shine sweep). The card carries his bank balance and two stat rows. The rarities, stat pips,
flavour lines and the bank amounts after the $2,000 start are illustrative.
Music: upbeat.
Video: python3 b2r_16_cards.py <out.mp4>          Preview: python3 b2r_16_cards.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK, OUT

PURPLE = '#8b5cf6'
RAR = [('COMMON', '#8a9bab'), ('UNCOMMON', '#2fa36b'), ('RARE', '#3a8fd6'), ('EPIC', PURPLE), ('LEGENDARY', GOLD)]
FLAVOR = ['Owns one pair of scrubs.', 'Sleeps next to the pager.', 'Scrubbed in. Finally.', 'Has an office. With a door.', 'Runs the whole department.']
SKILL = [1, 2, 3, 4, 5]
SLEEP = [1, 1, 2, 3, 5]
ARTBG = [['#3a4654', '#1f2731'], ['#dff1f4', '#9fd4cf'], ['#f9e2b8', '#f0bd8c'], ['#17463f', '#0b2622'], ['#1b1440', '#f2707a', '#ffc37d']]
CY = 1012   # card centre


def _pips(c, y, n, col):
    for j in range(5):
        rr(c, 310 - (5 - j) * 62 + 6, y - 20, 56, 22, 11, P(col if j < n else '#dfe7ee'))


def card_face(c, i, t, bank):
    """One collectible card in local coordinates, centre (0, 0), 700 x 980."""
    name, col = RAR[i]; gold = i == 4
    rr(c, -350, -474, 700, 980, 44, P('#000000', 120, blur=30))
    rr(c, -350, -490, 700, 980, 44, grad(-350, -490, 350, 490, ['#ffe9a8', '#f5b83d', '#c98f1f', '#ffd774']) if gold else P(col))
    rr(c, -332, -472, 664, 944, 30, P('#fbf7ee'))
    text(c, 'Dr John Smith', -306, -428, 46, INK, 900)
    lv = f'LV {i + 1}'; w = tw(lv, 34, 900) + 44
    rr(c, 310 - w, -468, w, 54, 27, P(col)); text(c, lv, 310 - w / 2, -429, 34, INK if gold else '#ffffff', 900, 'c')
    # art window
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-310, -398, 620, 440), 22, 22), True)
    c.drawRect(skia.Rect.MakeXYWH(-310, -398, 620, 440), grad(0, -398, 0, 42, ARTBG[i]))
    c.drawCircle(0, -150, 230, P(col, 70, blur=70))
    if gold:
        for j in range(12):
            a = j * math.pi / 6 + t * .5; ray = skia.Path(); ray.moveTo(0, -150)
            ray.lineTo(math.cos(a - .09) * 700, -150 + math.sin(a - .09) * 700); ray.lineTo(math.cos(a + .09) * 700, -150 + math.sin(a + .09) * 700); ray.close()
            c.drawPath(ray, P('#fff0c4', 46))
    doctor(c, 0, 196, .85, OUT[i], t, la=10, ra=(-150 + math.sin(t * 6) * 12) if i >= 3 else -10, mood='tired' if i < 2 else 'happy')
    c.restore()
    rr(c, -310, -398, 620, 440, 22, P(col, stroke=6))
    # rarity banner
    rr(c, -310, 60, 620, 64, 14, P(col)); text(c, name + ' CARD', 0, 105, 36, INK if gold else '#ffffff', 900, 'c')
    text(c, RANKS[i], 0, 206, 80, INK, 900, 'c')
    text(c, FLAVOR[i], 0, 254, 32, '#5b7083', 700, 'c')
    c.drawLine(-310, 282, 310, 282, P('#e4dccb', stroke=3))
    text(c, 'BANK', -310, 336, 30, '#5b7083', 900); text(c, '$' + f'{int(bank):,}', 310, 340, 50, TEAL_D, 900, 'r')
    text(c, 'SKILL', -310, 394, 30, '#5b7083', 900); _pips(c, 394, SKILL[i], col)
    text(c, 'SLEEP', -310, 446, 30, '#5b7083', 900); _pips(c, 446, SLEEP[i], col)
    if gold:  # foil shine sweep
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-350, -490, 700, 980), 44, 44), True)
        x = lerp(-900, 900, (t * .55) % 1); sh = skia.Path(); sh.moveTo(x, -490); sh.lineTo(x + 150, -490); sh.lineTo(x - 250, 490); sh.lineTo(x - 400, 490); sh.close()
        c.drawPath(sh, P('#ffffff', 80)); c.restore()


def draw_card(c, i, t, bank, sx=1.0, dy=0.0, rot=0.0):
    c.save(); c.translate(540, CY + dy); c.rotate(rot); c.scale(max(sx, .001), 1); card_face(c, i, t, bank); c.restore()


def backdrop(c, i, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, W * .4, H, ['#0a1a2c', '#10283a']))
    c.drawCircle(540, CY, 620, P(RAR[i][1], 60, blur=160))
    for j in range(9):  # drifting dust
        x = (j * 137 + t * 22) % W; y = 300 + (j * 211 - t * 40) % 1300
        c.drawCircle(x, y, 5 + j % 3 * 2, P(RAR[i][1], 110))
    scenes._ecg(c, 0, W, 1640, t, TEAL, a=60, amp=50, w=5)


def badge(c, i, k=1.0):
    c.save(); c.translate(960, 190); c.scale(k, k); c.drawCircle(0, 0, 54, P(GOLD)); text(c, f'{i + 1}', -12, 16, 50, INK, 900, 'c'); text(c, '/5', 22, 16, 30, INK, 900, 'c'); c.restore()


def e_hook(c, t):
    backdrop(c, 0, t); k = ease(t / .45)
    title2(c, 'Every doctor starts', 'as a common card.', 356, size=96, sub_size=96)
    draw_card(c, 0, t, 2000, dy=(1 - k) * -1500, rot=(1 - k) * -14 + math.sin(t * 1.6) * 1.2)
    brand_bar(c)
    if t > 1.5: badge(c, 0, pop((t - 1.5) / .35))


def _rank(i):
    def f(c, t):
        backdrop(c, i, t); k = ease(t / .3); name = RAR[i][0].capitalize()
        title2(c, RANKS[i], f'{name} card.', 356, '#ffffff', RAR[i][1] if i != 1 else '#5fd39a', dy=(1 - k) * -30, a=255 * k, size=108, sub_size=84)
        if t < .2: draw_card(c, i - 1, t, BANK[i - 1], sx=1 - eio(t / .2))
        else:
            draw_card(c, i, t, lerp(BANK[i - 1], BANK[i], eio((t - .4) / 1.2)), sx=pop((t - .2) / .32), rot=math.sin(t * 1.6) * 1.2)
        if i == 4:
            for j in range(7):
                a = j * math.pi * 2 / 7 + t * 1.2; sparkle(c, 540 + math.cos(a) * 430, CY + math.sin(a) * 560, 30 * abs(math.sin(t * 3 + j)), 255, '#fff6d8')
        brand_bar(c)
        if t > .25: badge(c, i, pop((t - .25) / .35))
    return f


SC = [(e_hook, 3.0)] + [(_rank(i), 2.7 if i < 4 else 3.3) for i in range(1, 5)] + [(cta2('Start as a common card.', 'Go legendary.'), 3.4)]

VOICE = [(0.15, 'Every doctor starts as a common card.', 2.7), (3.2, 'Resident. Uncommon.', 2.3), (5.9, 'Registrar. Rare.', 2.3),
         (8.6, 'Consultant. Epic.', 2.3), (11.3, 'E.D. Director. Legendary.', 2.9), (14.55, 'Collect all five ranks. Bedside Bay. Play free.', 3.0)]


def soundtrack(wav):
    import sound
    st = [3.0, 5.7, 8.4, 11.1]
    cues = [(.05, 'whoosh'), (.42, 'impact'), (1.5, 'pop')] + [(s - .05, 'whoosh') for s in st] + [(s + .3, 'pop') for s in st]
    cues += [(s + .5, f'step:{i + 1}') for i, s in enumerate(st)] + [(s + .9, 'cash') for s in st]
    cues += [(11.5, 'ding'), (13.2, 'riser'), (14.4, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=3.0, lift=11.1, cta=14.4, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .12)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 0.25), (0, 2.4), (1, 0.12), (1, 0.3), (1, 2.3), (2, 2.3), (3, 2.3), (4, 3.0), (5, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
